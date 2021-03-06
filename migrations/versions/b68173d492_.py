"""empty message

Revision ID: b68173d492
Revises: 3993b50e8bc
Create Date: 2015-03-30 15:06:08.245049

"""

# revision identifiers, used by Alembic.
revision = 'b68173d492'
down_revision = '3993b50e8bc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('preferred_arrival_time', sa.String(length=5), nullable=True))


def downgrade():
    op.drop_column('user', 'preferred_arrival_time')
