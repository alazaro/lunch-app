"""empty message

Revision ID: 3d8e8f0fe79
Revises: 2ead17daf1e
Create Date: 2015-02-09 15:05:38.184212

"""

# revision identifiers, used by Alembic.
revision = '3d8e8f0fe79'
down_revision = '2ead17daf1e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('web_page', sa.String(length=100), nullable=True),
        sa.Column('address', sa.String(length=400), nullable=True),
        sa.Column('telephone', sa.String(length=20), nullable=True),
        sa.Column('date_added', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.add_column('food', sa.Column('rating', sa.Float(), nullable=True))


def downgrade():
    op.add_column(
        'mail_text_msg',
        sa.Column('blocked_user_text', sa.VARCHAR(length=800), nullable=True),
    )
    op.drop_column('food', 'rating')
    op.create_table('pizza',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('date', sa.DATETIME(), nullable=True),
        sa.Column('pizza_ordering_is_allowed', sa.BOOLEAN(), nullable=True),
        sa.Column('ordered_pizzas', sa.BLOB(), nullable=True),
        sa.Column('users_already_ordered', sa.VARCHAR(length=5000), nullable=True),
        sa.Column('who_created', sa.VARCHAR(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('companies')
