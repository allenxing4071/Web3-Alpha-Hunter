"""Initial tables

Revision ID: 001
Revises: 
Create Date: 2025-01-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create projects table
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('launch_date', sa.Date(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('token_launch_probability', sa.Float(), nullable=True),
        sa.Column('airdrop_value_estimate', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('investment_suggestion', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    # Create social_metrics table
    op.create_table('social_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('twitter_followers', sa.Integer(), nullable=True),
        sa.Column('twitter_engagement_rate', sa.Float(), nullable=True),
        sa.Column('telegram_members', sa.Integer(), nullable=True),
        sa.Column('telegram_active_rate', sa.Float(), nullable=True),
        sa.Column('discord_members', sa.Integer(), nullable=True),
        sa.Column('community_sentiment', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_social_metrics_id'), 'social_metrics', ['id'], unique=False)

    # Create onchain_metrics table
    op.create_table('onchain_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('tvl', sa.Float(), nullable=True),
        sa.Column('transaction_volume', sa.Float(), nullable=True),
        sa.Column('active_addresses', sa.Integer(), nullable=True),
        sa.Column('contract_interactions', sa.Integer(), nullable=True),
        sa.Column('token_holders', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_onchain_metrics_id'), 'onchain_metrics', ['id'], unique=False)

    # Create ai_analysis table
    op.create_table('ai_analysis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('tech_innovation_score', sa.Float(), nullable=True),
        sa.Column('team_background_score', sa.Float(), nullable=True),
        sa.Column('market_potential_score', sa.Float(), nullable=True),
        sa.Column('risk_factors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('opportunities', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_analysis_id'), 'ai_analysis', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_ai_analysis_id'), table_name='ai_analysis')
    op.drop_table('ai_analysis')
    op.drop_index(op.f('ix_onchain_metrics_id'), table_name='onchain_metrics')
    op.drop_table('onchain_metrics')
    op.drop_index(op.f('ix_social_metrics_id'), table_name='social_metrics')
    op.drop_table('social_metrics')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')

