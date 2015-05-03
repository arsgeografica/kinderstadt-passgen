from datetime import datetime
from flask.ext.celery import Celery
from kinderstadt_passgen.models import Order, db


celery = Celery()


@celery.task
def execute_order(id):
    order = Order.query.get(id)
    order.finished = datetime.now()
    db.session.commit()
