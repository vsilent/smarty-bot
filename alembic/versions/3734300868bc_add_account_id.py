"""add account id

Revision ID: 3734300868bc
Revises: 3772e5bcb34d
Create Date: 2013-09-30 18:07:21.729288

"""

# revision identifiers, used by Alembic.
revision = '3734300868bc'
down_revision = '3772e5bcb34d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account_profile', sa.Column('account_id', sa.Integer(11)))
    pass


def downgrade():
    pass
