"""fix iteration_logs table schema

Revision ID: fix_iteration_logs
Revises: c98f53a427bc
Create Date: 2025-09-23 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_iteration_logs'
down_revision: Union[str, None] = 'c98f53a427bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to iteration_logs table
    try:
        op.add_column('iteration_logs', sa.Column('iteration_number', sa.Integer(), nullable=True))
        op.add_column('iteration_logs', sa.Column('prompt', sa.Text(), nullable=True))
        op.add_column('iteration_logs', sa.Column('spec_before', sa.JSON(), nullable=True))
        op.add_column('iteration_logs', sa.Column('spec_after', sa.JSON(), nullable=True))
        op.add_column('iteration_logs', sa.Column('evaluation_data', sa.JSON(), nullable=True))
        op.add_column('iteration_logs', sa.Column('feedback_data', sa.JSON(), nullable=True))
        op.add_column('iteration_logs', sa.Column('score_before', sa.Float(), nullable=True))
        op.add_column('iteration_logs', sa.Column('score_after', sa.Float(), nullable=True))
        op.add_column('iteration_logs', sa.Column('reward', sa.Float(), nullable=True))
    except Exception as e:
        print(f"Column addition failed (may already exist): {e}")


def downgrade() -> None:
    # Remove added columns
    try:
        op.drop_column('iteration_logs', 'reward')
        op.drop_column('iteration_logs', 'score_after')
        op.drop_column('iteration_logs', 'score_before')
        op.drop_column('iteration_logs', 'feedback_data')
        op.drop_column('iteration_logs', 'evaluation_data')
        op.drop_column('iteration_logs', 'spec_after')
        op.drop_column('iteration_logs', 'spec_before')
        op.drop_column('iteration_logs', 'prompt')
        op.drop_column('iteration_logs', 'iteration_number')
    except Exception as e:
        print(f"Column removal failed: {e}")