"""Progress indicator

Revision ID: 151134eaf2e9
Revises: 1e5604e79222
Create Date: 2015-06-09 23:54:32.863953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '151134eaf2e9'
down_revision = '1e5604e79222'


def upgrade():
    op.add_column(
        'orders', sa.Column('progress', sa.Integer(), server_default='0', nullable=False))

    orders = table('orders',
                   column('finished', sa.DateTime()),
                   column('progress', sa.Integer()))

    op.execute(
        orders.update().where(orders.c.finished != None).values(progress=100)
    )


def downgrade():
    op.drop_column('orders', 'progress')
