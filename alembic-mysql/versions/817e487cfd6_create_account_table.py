"""create account table

Revision ID: 817e487cfd6
Revises: None
Create Date: 2013-10-05 23:59:29.076673

"""

# revision identifiers, used by Alembic.
revision = '817e487cfd6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'account',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('description', sa.Unicode(200)),
            )



def downgrade():
    op.drop_table('account')
