"""Add sessions

Revision ID: 3898aa0132e
Revises: c793e120ad
Create Date: 2015-06-02 16:29:45.989068

"""

# revision identifiers, used by Alembic.
revision = '3898aa0132e'
down_revision = 'c793e120ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('sessionExpiry', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('sessionId', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'sessionId')
    op.drop_column('user', 'sessionExpiry')
    ### end Alembic commands ###
