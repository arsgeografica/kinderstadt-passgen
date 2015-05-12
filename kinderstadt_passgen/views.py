from flask import abort, current_app as app, render_template, redirect, \
    request, send_file, url_for
from kinderstadt_passgen.extensions import db
from kinderstadt_passgen.models import Order
from kinderstadt_passgen.tasks import execute_order
from kinderstadt_passgen.forms import OrderForm


def home():
    """Home route, where user enter the number of passes they want to
    generate"""
    return render_template('home.html', form=OrderForm())


def order(base62_id=None):
    """Route where the user is redirected to. Creates an order and displays
    order status"""

    if base62_id is None:
        form = OrderForm()
        if 'POST' == request.method:
            if form.validate_on_submit():
                order = Order.create(size=form.range_size.data)
                try:
                    execute_order.apply_async([order.id])

                    return redirect(
                        url_for('order', base62_id=order.base62_id))
                except Exception, e:
                    # TODO: Logging
                    db.session.delete(order)
                    db.session.commit()
                    raise e
                    abort(500)

        return render_template('order_form.html', form=form)
    else:
        order = Order.get_by_base62_id(base62_id)
        return render_template('order.html', order=order)


def download(base62_id):
    """Download generated PDF"""
    order = Order.get_by_base62_id(base62_id)
    return send_file(order.storage_path)
