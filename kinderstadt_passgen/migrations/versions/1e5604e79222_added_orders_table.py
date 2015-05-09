"""Added orders table

Revision ID: 1e5604e79222
Revises: None
Create Date: 2015-05-09 21:04:22.406078

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1e5604e79222'
down_revision = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('range_from', sa.Integer(), nullable=True),
        sa.Column('range_size', sa.Integer(), nullable=True),
        sa.Column('ordered', sa.DateTime(), nullable=False),
        sa.Column('finished', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('orders')
