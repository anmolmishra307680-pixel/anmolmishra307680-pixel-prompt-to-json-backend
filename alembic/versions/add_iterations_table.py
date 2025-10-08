"""add iterations table

Revision ID: add_iterations_table
Revises: 0002_add_iterations_and_compliance
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_iterations_table'
down_revision = '0002_add_iterations_and_compliance'
branch_labels = None
depends_on = None

def upgrade():
    # Create iterations table
    op.create_table('iterations',
        sa.Column('iter_id', sa.Integer(), nullable=False),
        sa.Column('spec_id', sa.Text(), nullable=True),
        sa.Column('before_spec', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('after_spec', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('ts', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('iter_id')
    )
    
    # Add foreign key reference to specs table if it exists
    try:
        op.create_foreign_key(None, 'iterations', 'specs', ['spec_id'], ['spec_id'])
    except:
        # If specs table doesn't exist, skip foreign key
        pass

def downgrade():
    op.drop_table('iterations')