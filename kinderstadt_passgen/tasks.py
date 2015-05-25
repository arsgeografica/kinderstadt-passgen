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
from kinderstadt_passgen.nup import generateNup
from kinderstadt_passgen.models import Order
from kinderstadt_passgen.extensions import db, celery

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
    logger.info('Created {0} passes in {1:.0f}ms'
                .format(order.range_size, (_end-_start)*1000))

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

        self.result_file = result_file

    def _create_passes(self):
        """Create passes PDF file"""
        merger = PdfFileMerger()
        for i in range(self.order.range_from, self.order.range_from
                       + self.order.range_size):
            pass_file = self.work_dir / 'pass_%d.pdf' % i
            self._svg2pdf('pass.svg', pass_file,
                          pi=i, pc=check(i))
            merger.append(pass_file)

        _passes_file = str(self.work_dir / '_passes.pdf')
        merger.write(_passes_file)

        if app.config['PASS_NUP'] > 1:
            nup_file = str(self.work_dir / '_passes_nup.pdf')
            generateNup(_passes_file, app.config['PASS_NUP'], nup_file)
            return nup_file
        return _passes_file

    def _create_agreements(self):
        """Create agreement forms PDF file"""

        merger = PdfFileMerger()
        for i in range(self.order.range_from, self.order.range_from
                       + self.order.range_size):
            agreement_file = self.work_dir / 'agreement_%d.pdf' % i
            self._svg2pdf('agreement.svg', agreement_file,
                          pi=i, pc=check(i))
            merger.append(agreement_file)

        _agreements_file = str(self.work_dir / '_agreements.pdf')
        merger.write(_agreements_file)

        if app.config['AGREEMENT_NUP'] > 1:
            nup_file = str(self.work_dir / '_agreements_nup.pdf')
            generateNup(_agreements_file, app.config['AGREEMENT_NUP'],
                        nup_file)
            return nup_file
        return _agreements_file

    def _svg2pdf(self, template, out_file, **kwargs):
        """Render SVG template to outfile using Jinja2, passing kwargs"""

        svg = render_template(template, **kwargs)
        svg2pdf(bytestring=svg, write_to=out_file)
