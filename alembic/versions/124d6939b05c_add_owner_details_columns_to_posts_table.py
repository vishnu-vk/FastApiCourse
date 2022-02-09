"""add owner details columns to posts table

Revision ID: 124d6939b05c
Revises: ddf5b5fc3585
Create Date: 2022-02-08 17:56:16.024024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '124d6939b05c'
down_revision = 'ddf5b5fc3585'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'),nullable= False))
    pass


def downgrade():
    op.drop_column('posts','owner_id')
    pass
