"""add compliance_cases table

Revision ID: add_compliance_cases_table
Revises: add_iterations_table
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_compliance_cases_table'
down_revision = 'add_iterations_table'
branch_labels = None
depends_on = None

def upgrade():
    # Create compliance_cases table
    op.create_table('compliance_cases',
        sa.Column('case_id', sa.String(255), nullable=False),
        sa.Column('project_id', sa.String(255), nullable=True),
        sa.Column('case_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('result_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('geometry_url', sa.Text(), nullable=True),
        sa.Column('local_geometry_url', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True, default='pending'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('case_id')
    )

def downgrade():
    op.drop_table('compliance_cases')