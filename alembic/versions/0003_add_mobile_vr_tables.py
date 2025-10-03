"""Add mobile and VR tables

Revision ID: 0003_add_mobile_vr_tables
Revises: 0002_add_iterations_and_compliance
Create Date: 2024-10-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '0003_add_mobile_vr_tables'
down_revision = '0002_add_iterations_and_compliance'
branch_labels = None
depends_on = None

def upgrade():
    # Mobile sessions table
    op.create_table('mobile_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('device_info', sa.JSON(), nullable=True),
        sa.Column('session_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_active', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # VR experiences table
    op.create_table('vr_experiences',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('spec_id', sa.String(), nullable=False),
        sa.Column('vr_platform', sa.String(), nullable=False),
        sa.Column('immersion_level', sa.String(), nullable=False),
        sa.Column('scene_config', sa.JSON(), nullable=True),
        sa.Column('export_formats', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Preview cache table
    op.create_table('preview_cache',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('spec_id', sa.String(), nullable=False),
        sa.Column('format', sa.String(), nullable=False),
        sa.Column('size', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Cost tracking table
    op.create_table('cost_tracking',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('operation_type', sa.String(), nullable=False),
        sa.Column('compute_type', sa.String(), nullable=False),
        sa.Column('tokens_used', sa.Integer(), nullable=False),
        sa.Column('cost_usd', sa.Float(), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('cost_tracking')
    op.drop_table('preview_cache')
    op.drop_table('vr_experiences')
    op.drop_table('mobile_sessions')