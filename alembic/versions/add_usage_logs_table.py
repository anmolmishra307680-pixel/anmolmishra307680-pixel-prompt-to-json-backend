"""add usage_logs table

Revision ID: add_usage_logs_table
Revises: add_compliance_cases_table
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_usage_logs_table'
down_revision = 'add_compliance_cases_table'
branch_labels = None
depends_on = None

def upgrade():
    # Create usage_logs table
    op.create_table('usage_logs',
        sa.Column('log_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.String(255), nullable=True),
        sa.Column('provider', sa.String(50), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.Column('prompt_length', sa.Integer(), nullable=True),
        sa.Column('params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('log_id')
    )

def downgrade():
    op.drop_table('usage_logs')