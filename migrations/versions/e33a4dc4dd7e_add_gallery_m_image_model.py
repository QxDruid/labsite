"""add gallery m_image model

Revision ID: e33a4dc4dd7e
Revises: f014999198c7
Create Date: 2021-04-02 13:48:06.805825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e33a4dc4dd7e'
down_revision = 'f014999198c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gallery_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Image', sa.String(length=32), nullable=True),
    sa.Column('Description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gallery_image')
    # ### end Alembic commands ###
