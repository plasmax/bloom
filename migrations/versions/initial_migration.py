"""Initial database migration

Revision ID: 01_initial
Create Date: 2024-11-29 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision = '01_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum types first (for PostgreSQL compatibility)
    task_status = sa.Enum('pending', 'in_progress', 'completed', 'failed', name='taskstatus')
    task_priority = sa.Enum('low', 'medium', 'high', name='taskpriority')
    file_type = sa.Enum('python', 'text', 'markdown', 'json', 'other', name='filetype')
    
    task_status.create(op.get_bind())
    task_priority.create(op.get_bind())
    file_type.create(op.get_bind())
    
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_username', 'user', ['username'], unique=True)
    op.create_index('idx_user_email', 'user', ['email'], unique=True)

    # Create task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=140), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', 'failed', name='taskstatus'), nullable=True),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='taskpriority'), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['task.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_created_at', 'task', ['created_at'])
    op.create_index('idx_task_user_id', 'task', ['user_id'])

    # Create file table
    op.create_table(
        'file',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.Enum('python', 'text', 'markdown', 'json', 'other', name='filetype'), nullable=True),
        sa.Column('mime_type', sa.String(length=128), nullable=True),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('hash', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_file_created_at', 'file', ['created_at'])
    op.create_index('idx_file_user_id', 'file', ['user_id'])
    op.create_index('idx_file_task_id', 'file', ['task_id'])


def downgrade():
    # Drop tables
    op.drop_table('file')
    op.drop_table('task')
    op.drop_table('user')
    
    # Drop enum types
    sa.Enum(name='filetype').drop(op.get_bind())
    sa.Enum(name='taskpriority').drop(op.get_bind())
    sa.Enum(name='taskstatus').drop(op.get_bind())