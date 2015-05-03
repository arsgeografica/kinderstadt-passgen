"""Create order table

Revision ID: 3804dfbcd1d
Revises:
Create Date: 2015-05-01 17:25:02.712412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3804dfbcd1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('range_from', sa.Integer, nullable=False),
        sa.Column('range_size', sa.Integer, nullable=False),
        sa.Column('ordered', sa.DateTime(timezone=False), nullable=False),
        sa.Column('finished', sa.DateTime(timezone=False), nullable=True),
    )


def downgrade():
    op.drop_table('orders')
