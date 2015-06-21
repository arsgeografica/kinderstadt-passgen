"""Single page layout

Revision ID: 35e462100bff
Revises: 151134eaf2e9
Create Date: 2015-06-20 13:06:38.398324

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '35e462100bff'
down_revision = '151134eaf2e9'


def upgrade():
    op.add_column(
        'orders',
        sa.Column('single_page', sa.Boolean(), server_default='False',
                  nullable=False))


def downgrade():
    op.drop_column('orders', 'single_page')
