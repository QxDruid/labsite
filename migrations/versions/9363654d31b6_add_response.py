"""add response

Revision ID: 9363654d31b6
Revises: 028a54de3070
Create Date: 2022-02-15 12:02:32.344878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9363654d31b6'
down_revision = '028a54de3070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('response', sa.Column('email', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('response', 'email')
    # ### end Alembic commands ###
