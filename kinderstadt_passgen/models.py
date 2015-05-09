from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from sqlalchemy.types import DateTime, Integer
from sqlalchemy.schema import Column
from datetime import datetime


db = SQLAlchemy()
migrate = Migrate()


class Order(db.Model):

    """DB representation of a single pass order. Basically needed as a big
    counter."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    range_from = Column(Integer, nullable=True)
    range_size = Column(Integer, nullable=True)
    ordered = Column(DateTime(timezone=False), nullable=False)
    finished = Column(DateTime(timezone=False), nullable=True)

    @classmethod
    def create(cls, size=1):
        """Create a new order, put it into the database and return the id"""

        # Get range start from last ordered or just assume 1
        last_order = db.session.query(Order).order_by(
            Order.range_from.desc()).first()
        range_from = last_order.range_from + \
            last_order.range_size if last_order else 1

        order = cls()
        order.range_from = range_from
        order.range_size = size
        order.ordered = datetime.now()

        db.session.add(order)
        db.session.commit()

        return order
