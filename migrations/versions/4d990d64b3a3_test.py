"""test

Revision ID: 4d990d64b3a3
Revises: 
Create Date: 2020-05-07 15:04:06.277062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d990d64b3a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entries_text'), 'entries', ['text'], unique=False)
    op.create_index(op.f('ix_entries_title'), 'entries', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_entries_title'), table_name='entries')
    op.drop_index(op.f('ix_entries_text'), table_name='entries')
    op.drop_table('entries')
    # ### end Alembic commands ###
