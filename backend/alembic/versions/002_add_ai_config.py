"""add ai_config table

Revision ID: 002
Revises: 001
Create Date: 2025-01-08 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ai_configs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('api_key', sa.Text(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=True, default=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_configs_id'), 'ai_configs', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_ai_configs_id'), table_name='ai_configs')
    op.drop_table('ai_configs')

