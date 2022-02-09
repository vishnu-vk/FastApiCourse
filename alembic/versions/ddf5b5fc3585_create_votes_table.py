"""create votes table

Revision ID: ddf5b5fc3585
Revises: f1e791ddf16d
Create Date: 2022-02-08 17:48:18.156650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddf5b5fc3585'
down_revision = 'f1e791ddf16d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes', sa.Column('post_id', sa.Integer(), sa.ForeignKey('posts.id', ondelete='CASCADE'),nullable= False, primary_key= True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'),primary_key= True,nullable= False), sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default= sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_table('votes')
    pass
