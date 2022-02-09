"""create users table

Revision ID: f1e791ddf16d
Revises: 27bd2c75a1d0
Create Date: 2022-02-08 17:42:47.522405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1e791ddf16d'
down_revision = '27bd2c75a1d0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable= False, primary_key= True), sa.Column('email', sa.String(), unique= True,nullable= False), sa.Column('password', sa.String(), nullable= False), sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default= sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_table('users')
    pass
