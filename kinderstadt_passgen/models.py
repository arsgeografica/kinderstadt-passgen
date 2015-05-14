import basehash
from flask import current_app as app
from path import Path
from sqlalchemy.types import DateTime, Integer
from sqlalchemy.schema import Column
from datetime import datetime
from kinderstadt_passgen.extensions import db, ma


_base62 = basehash.base62()


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

    @property
    def base62_id(self):
        return _base62.encode(self.id + app.config['ID_ENCODE_OFFSET'])

    @classmethod
    def get_by_base62_id(cls, base62_id):
        id = _base62.decode(base62_id) - app.config['ID_ENCODE_OFFSET']
        return cls.query.get_or_404(id)

    @property
    def storage_path(self):
        out_base = Path(app.config['FILE_STORAGE_PATH'])
        out_path = out_base / str(100*(int((self.id - 1)/100)+1))
        out_file = 'passes_%s.pdf' % self.base62_id

        return out_path / out_file


class OrderSchema(ma.Schema):

    class Meta:
        # Fields to expose
        fields = ('base62_id', 'range_size', 'ordered', 'finished', '_links')
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('order', base62_id='<base62_id>')
    })
