"""upgrade account_profile add new columns

Revision ID: 3772e5bcb34d
Revises: None
Create Date: 2013-08-05 13:43:55.540411

"""

# revision identifiers, used by Alembic.
revision = '3772e5bcb34d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account_profile', sa.Column('home_country', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_city', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_state', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_street', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_house', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_apartment', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_postcode', sa.String(255)))
    op.add_column('account_profile', sa.Column('home_phone', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_country', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_city', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_street', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_house', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_postcode', sa.String(255)))
    op.add_column('account_profile', sa.Column('work_phone', sa.String(255)))


def downgrade():
    pass
