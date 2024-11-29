"""Add file versions and metadata

Revision ID: 04_file_versions
Create Date: 2024-11-29 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04_file_versions'
down_revision = '03_task_history'
branch_labels = None
depends_on = None


def upgrade():
    # Create file_version table
    op.create_table(
        'file_version',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('hash', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('file_id', 'version_number', name='uq_file_version')
    )
    op.create_index('idx_file_version_file_id', 'file_version', ['file_id'])
    op.create_index('idx_file_version_user_id', 'file_version', ['user_id'])
    op.create_index('idx_file_version_created_at', 'file_version', ['created_at'])

    # Create file_metadata table
    op.create_table(
        'file_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=64), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('file_id', 'key', name='uq_file_metadata')
    )
    op.create_index('idx_file_metadata_file_id', 'file_metadata', ['file_id'])
    op.create_index('idx_file_metadata_key', 'file_metadata', ['key'])

    # Add current_version column to file table
    op.add_column('file',
        sa.Column('current_version', sa.Integer(), nullable=True, server_default='1')
    )


def downgrade():
    # Remove current_version from file table
    op.drop_column('file', 'current_version')

    # Drop tables
    op.drop_table('file_metadata')
    op.drop_table('file_version')