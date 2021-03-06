"""add columns to story and task models

Revision ID: 7dadbc698a94
Revises: 0aef1df2acdf
Create Date: 2018-07-07 14:11:16.300918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dadbc698a94'
down_revision = '0aef1df2acdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('sprint', sa.String(length=300), nullable=True))
    op.add_column('task', sa.Column('task_hours', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('task_notes', sa.String(length=2000), nullable=True))
    op.drop_column('task', 'sprint_number')
    op.add_column('user_story', sa.Column('epic', sa.String(length=20), nullable=True))
    op.add_column('user_story', sa.Column('points', sa.Integer(), nullable=True))
    op.add_column('user_story', sa.Column('size', sa.String(length=10), nullable=True))
    op.add_column('user_story', sa.Column('sprint', sa.String(length=300), nullable=True))
    op.add_column('user_story', sa.Column('story_notes', sa.String(length=3000), nullable=True))
    op.drop_column('user_story', 'sprint_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_story', sa.Column('sprint_number', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('user_story', 'story_notes')
    op.drop_column('user_story', 'sprint')
    op.drop_column('user_story', 'size')
    op.drop_column('user_story', 'points')
    op.drop_column('user_story', 'epic')
    op.add_column('task', sa.Column('sprint_number', sa.VARCHAR(length=300), autoincrement=False, nullable=True))
    op.drop_column('task', 'task_notes')
    op.drop_column('task', 'task_hours')
    op.drop_column('task', 'sprint')
    # ### end Alembic commands ###
