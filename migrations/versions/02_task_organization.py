"""Add task organization features

Revision ID: 02_task_organization
Create Date: 2024-11-29 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02_task_organization'
down_revision = '01_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Create category table
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),  # Hex color code
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_category_name', 'category', ['name'])
    op.create_index('idx_category_user_id', 'category', ['user_id'])

    # Create tag table
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tag_name', 'tag', ['name'])
    op.create_index('idx_tag_user_id', 'tag', ['user_id'])

    # Create task_tag association table
    op.create_table(
        'task_tag',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )

    # Add category_id to task table
    op.add_column('task',
        sa.Column('category_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_task_category_id', 'task',
        'category', ['category_id'], ['id']
    )
    op.create_index('idx_task_category_id', 'task', ['category_id'])


def downgrade():
    # Remove category_id from task table
    op.drop_constraint('fk_task_category_id', 'task', type_='foreignkey')
    op.drop_index('idx_task_category_id', 'task')
    op.drop_column('task', 'category_id')

    # Drop tables
    op.drop_table('task_tag')
    op.drop_table('tag')
    op.drop_table('category')