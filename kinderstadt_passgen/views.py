import basehash
from flask import abort, current_app as app, render_template, redirect, \
    request, url_for
from kinderstadt_passgen.models import Order, db
from kinderstadt_passgen.task import execute_order


base62 = basehash.base62()


def home():
    """Home route, where user enter the number of passes they want to
    generate"""
    return 'HOME'


def order(id=None):
    """Route where the user is redirected to. Creates an order and displays
    order status"""

    if id is None:
        if 'POST' == request.method:
            order = Order.create()
            try:
                execute_order.apply_async([order.id])

                id = base62.encode(order.id + app.config['ID_ENCODE_OFFSET'])
                return redirect(url_for('order', id=id))
            except Exception, e:
                # TODO: Logging
                db.session.delete(order)
                db.session.commit()
                raise e
                abort(500)
        else:
            abort(400)
    else:
        return render_template('order.html', id=id)


def download(id):
    """Download generated PDF"""
    pass
