"""Add task history tracking

Revision ID: 03_task_history
Create Date: 2024-11-29 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03_task_history'
down_revision = '02_task_organization'
branch_labels = None
depends_on = None


def upgrade():
    # Create task_history table
    op.create_table(
        'task_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('field_name', sa.String(length=64), nullable=False),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('action', sa.String(length=16), nullable=False),  # 'create', 'update', 'delete'
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_history_task_id', 'task_history', ['task_id'])
    op.create_index('idx_task_history_user_id', 'task_history', ['user_id'])
    op.create_index('idx_task_history_timestamp', 'task_history', ['timestamp'])

    # Create task_comment table for standalone comments
    op.create_table(
        'task_comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['task_comment.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_comment_task_id', 'task_comment', ['task_id'])
    op.create_index('idx_task_comment_user_id', 'task_comment', ['user_id'])
    op.create_index('idx_task_comment_created_at', 'task_comment', ['created_at'])


def downgrade():
    # Drop tables
    op.drop_table('task_comment')
    op.drop_table('task_history')