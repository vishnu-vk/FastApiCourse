"""create posts table

Revision ID: 27bd2c75a1d0
Revises: 
Create Date: 2022-02-08 17:19:55.551988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27bd2c75a1d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable= False, primary_key= True), sa.Column('title', sa.String(), nullable= False), sa.Column('content', sa.String(), nullable= False),
    sa.Column('published', sa.Boolean(), nullable= False, server_default= 'True'), sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default= sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_table('posts')
    pass
