from flask import abort, current_app as app, render_template, redirect, \
    request, url_for
from kinderstadt_passgen.extensions import db
from kinderstadt_passgen.models import Order
from kinderstadt_passgen.tasks import execute_order


def home():
    """Home route, where user enter the number of passes they want to
    generate"""
    return 'HOME'


def order(base62_id=None):
    """Route where the user is redirected to. Creates an order and displays
    order status"""

    if base62_id is None:
        if 'POST' == request.method:
            order = Order.create()
            try:
                execute_order.apply_async([order.id])

                return redirect(url_for('order', base62_id=order.base62_id))
            except Exception, e:
                # TODO: Logging
                db.session.delete(order)
                db.session.commit()
                raise e
                abort(500)
        else:
            abort(400)
    else:
        order = Order.get_by_base62_id(base62_id)
        return render_template('order.html', order=order)


def download(id):
    """Download generated PDF"""
    pass
