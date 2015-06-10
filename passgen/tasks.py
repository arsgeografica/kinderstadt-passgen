from datetime import datetime
import errno
import os
import os.path
import shutil
import tempfile
import time
from cairosvg import svg2pdf
from celery.utils.log import get_task_logger
from flask import current_app as app, render_template
from path import Path
from PyPDF2 import PdfFileMerger
from stdnum import luhn
from passgen import __version__
from passgen.nup import generateNup
from passgen.models import Order
from passgen.extensions import db, celery

CHECK_ALPHABET = '0123456789ABCDEFGHJKLMNPQRSTUVWXY'

logger = get_task_logger(__name__)


@celery.task
def execute_order(id):
    """
    Create PDF given from order id.

    This loads the order details from the DB using the given id and uses
    the PassGen class to generate the result PDF. Finally, the result PDF
    is copied to the path the web app is looking into.
    """

    logger.info('Started job {id}'.format(id=id))
    _start = time.time()

    order = Order.query.get(id)

    generator = PassGen(order)
    generator.execute()

    out_path = os.path.dirname(order.storage_path)
    try:
        os.makedirs(out_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(out_path):
            pass
        else:
            generator.cleanup()
            raise

    shutil.copyfile(generator.result_file, order.storage_path)
    generator.cleanup()

    order.finished = datetime.now()
    db.session.commit()

    _end = time.time()
    logger.info('Finished job {id}, created {num} passes in {duration:.0f}ms'
                .format(id=id, num=order.range_size,
                        duration=(_end - _start)*1000))

    return out_path


def check(value):
    """
    Creates two-digit check value for given input value
    """

    def _check(value):
        return luhn.calc_check_digit(value, alphabet=CHECK_ALPHABET)

    a = _check(value)
    b = _check(str(value) + str(a))

    return a + b


class PassGen(object):

    """Generator for printable passes as PDFs"""

    work_dir = None
    result_file = None

    def __init__(self, order):
        self.order = order

    def init(self):
        """Create temporary working directory"""
        if not self.work_dir:
            self.work_dir = Path(tempfile.mkdtemp(suffix='passgen'))

        pass_nup = app.config['PASS_NUP']
        pass_steps = self.order.range_size + (2 if pass_nup > 1 else + 1)
        agreement_nup = app.config['AGREEMENT_NUP']
        agreement_steps = self.order.range_size + (2 if agreement_nup > 1 else + 1)
        self._num_steps = 1 + pass_steps + agreement_steps
        self._done_steps = 0

    def cleanup(self):
        """Delete (temporary) files"""

        if self.work_dir:
            shutil.rmtree(self.work_dir)
            self.work_dir = None

    def execute(self):
        """Create PDF file with passes and agreement forms"""
        self.init()

        passes = self._create_passes()
        agreements = self._create_agreements()

        merger = PdfFileMerger()
        merger.append(str(app.config['COVER_PDF']))
        merger.append(passes)
        merger.append(agreements)
        result_file = str(self.work_dir / 'passes.pdf')
        merger.write(result_file)
        self._add_step()

        self.result_file = result_file

    def _add_step(self):
        value = self._done_steps + 1
        self._done_steps = value
        self.order.progess = int(value / self._num_steps * 100)
        logger.debug('Progress for order %d: %d out of %d', self.order.id, value, self._num_steps)
        db.session.add(self.order)
        db.session.flush()

    def _create_passes(self):
        """Create passes PDF file"""
        merger = PdfFileMerger()
        for i in range(self.order.range_from, self.order.range_from +
                       self.order.range_size):
            pass_file = self.work_dir / 'pass_%d.pdf' % i
            self._svg2pdf('pass.svg', pass_file,
                          pi=i, pc=check(i))
            self._add_step()
            merger.append(pass_file)

        _passes_file = str(self.work_dir / '_passes.pdf')
        merger.write(_passes_file)
        self._add_step()

        if app.config['PASS_NUP'] > 1:
            nup_file = str(self.work_dir / '_passes_nup.pdf')
            generateNup(_passes_file, app.config['PASS_NUP'], nup_file)
            self._add_step()
            return nup_file
        return _passes_file

    def _create_agreements(self):
        """Create agreement forms PDF file"""

        merger = PdfFileMerger()
        for i in range(self.order.range_from, self.order.range_from +
                       self.order.range_size):
            agreement_file = self.work_dir / 'agreement_%d.pdf' % i
            self._svg2pdf('agreement.svg', agreement_file,
                          pi=i, pc=check(i))
            self._add_step()
            merger.append(agreement_file)

        _agreements_file = str(self.work_dir / '_agreements.pdf')
        merger.write(_agreements_file)
        self._add_step()

        if app.config['AGREEMENT_NUP'] > 1:
            nup_file = str(self.work_dir / '_agreements_nup.pdf')
            generateNup(_agreements_file, app.config['AGREEMENT_NUP'],
                        nup_file)
            self._add_step()
            return nup_file
        return _agreements_file

    def _svg2pdf(self, template, out_file, **kwargs):
        """Render SVG template to outfile using Jinja2, passing kwargs"""

        svg = render_template(
            template, __version__=__version__, **kwargs).encode('utf-8')
        svg2pdf(bytestring=svg, write_to=out_file)
