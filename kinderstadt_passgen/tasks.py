from datetime import datetime
from kinderstadt_passgen.models import Order
from kinderstadt_passgen.extensions import db, celery


@celery.task
def execute_order(id):
    order = Order.query.get(id)
    order.finished = datetime.now()
    db.session.commit()
