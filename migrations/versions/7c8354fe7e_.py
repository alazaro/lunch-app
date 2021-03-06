"""empty message

Revision ID: 7c8354fe7e
Revises: 3d8e8f0fe79
Create Date: 2015-02-09 18:42:44.563692

"""

# revision identifiers, used by Alembic.
revision = '7c8354fe7e'
down_revision = '3d8e8f0fe79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('mail_text_msg', 'blocked_user_text')


def downgrade():
    op.add_column(
        'mail_text_msg',
        sa.Column('blocked_user_text', sa.VARCHAR(length=800), nullable=True),
    )
