"""Add iterations and compliance tables

Revision ID: 0002_add_iterations_and_compliance
Revises: 85cc95e2c35b
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_add_iterations_and_compliance'
down_revision = '85cc95e2c35b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create iterations and compliance_cases tables"""
    
    # Create iterations table
    op.create_table('iterations',
        sa.Column('iter_id', sa.String(), nullable=False),
        sa.Column('spec_id', sa.String(), nullable=False),
        sa.Column('before_spec', sa.JSON(), nullable=True),
        sa.Column('after_spec', sa.JSON(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('ts', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('instruction', sa.Text(), nullable=True),
        sa.Column('object_id', sa.String(), nullable=True),
        sa.Column('score_before', sa.Float(), nullable=True),
        sa.Column('score_after', sa.Float(), nullable=True),
        sa.Column('improvement', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('iter_id')
    )
    
    # Create foreign key constraint to specs table
    op.create_foreign_key(
        'fk_iterations_spec_id',
        'iterations', 'specs',
        ['spec_id'], ['spec_id'],
        ondelete='CASCADE'
    )
    
    # Create compliance_cases table
    op.create_table('compliance_cases',
        sa.Column('case_id', sa.String(), nullable=False),
        sa.Column('spec_id', sa.String(), nullable=False),
        sa.Column('geometry_url', sa.String(), nullable=True),
        sa.Column('ts', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('project_id', sa.String(), nullable=True),
        sa.Column('compliance_rules', sa.JSON(), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('case_id')
    )
    
    # Create foreign key constraint to specs table
    op.create_foreign_key(
        'fk_compliance_cases_spec_id',
        'compliance_cases', 'specs',
        ['spec_id'], ['spec_id'],
        ondelete='CASCADE'
    )
    
    # Create compliance_feedback table
    op.create_table('compliance_feedback',
        sa.Column('feedback_id', sa.String(), nullable=False),
        sa.Column('case_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('suggestions', sa.JSON(), nullable=True),
        sa.Column('ts', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('feedback_id')
    )
    
    # Create foreign key constraint to compliance_cases table
    op.create_foreign_key(
        'fk_compliance_feedback_case_id',
        'compliance_feedback', 'compliance_cases',
        ['case_id'], ['case_id'],
        ondelete='CASCADE'
    )
    
    # Create usage_logs table for compute routing
    op.create_table('usage_logs',
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('route', sa.String(), nullable=False),
        sa.Column('cost_estimate', sa.Float(), nullable=True),
        sa.Column('ts', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('spec_id', sa.String(), nullable=True),
        sa.Column('processing_time', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('job_id')
    )
    
    # Create indexes for better performance
    op.create_index('idx_iterations_spec_id', 'iterations', ['spec_id'])
    op.create_index('idx_iterations_ts', 'iterations', ['ts'])
    op.create_index('idx_compliance_cases_spec_id', 'compliance_cases', ['spec_id'])
    op.create_index('idx_compliance_cases_ts', 'compliance_cases', ['ts'])
    op.create_index('idx_compliance_feedback_case_id', 'compliance_feedback', ['case_id'])
    op.create_index('idx_usage_logs_route', 'usage_logs', ['route'])
    op.create_index('idx_usage_logs_ts', 'usage_logs', ['ts'])


def downgrade() -> None:
    """Drop iterations and compliance tables"""
    
    # Drop indexes
    op.drop_index('idx_usage_logs_ts', table_name='usage_logs')
    op.drop_index('idx_usage_logs_route', table_name='usage_logs')
    op.drop_index('idx_compliance_feedback_case_id', table_name='compliance_feedback')
    op.drop_index('idx_compliance_cases_ts', table_name='compliance_cases')
    op.drop_index('idx_compliance_cases_spec_id', table_name='compliance_cases')
    op.drop_index('idx_iterations_ts', table_name='iterations')
    op.drop_index('idx_iterations_spec_id', table_name='iterations')
    
    # Drop tables (foreign keys will be dropped automatically)
    op.drop_table('usage_logs')
    op.drop_table('compliance_feedback')
    op.drop_table('compliance_cases')
    op.drop_table('iterations')