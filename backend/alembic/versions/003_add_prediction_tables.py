"""add prediction tables

Revision ID: 003
Revises: 002
Create Date: 2025-10-05

添加新功能相关的数据库表:
- token_launch_predictions: 代币发币概率预测
- airdrop_value_estimates: 空投价值估算
- investment_action_plans: 投资行动计划
- project_discoveries: 项目发现记录
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # 1. 代币发币概率预测表
    op.create_table(
        'token_launch_predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('launch_probability', sa.Integer()),
        sa.Column('confidence', sa.String(20)),
        sa.Column('estimated_timeline', sa.String(100)),
        sa.Column('detected_signals', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('signal_count', sa.Integer()),
        sa.Column('has_snapshot_announced', sa.Integer(), server_default='0'),
        sa.Column('has_tokenomics_published', sa.Integer(), server_default='0'),
        sa.Column('has_points_system', sa.Integer(), server_default='0'),
        sa.Column('has_audit_completed', sa.Integer(), server_default='0'),
        sa.Column('has_mainnet_live', sa.Integer(), server_default='0'),
        sa.Column('has_roadmap_token_mention', sa.Integer(), server_default='0'),
        sa.Column('predicted_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_prediction_project', 'token_launch_predictions', ['project_id', 'predicted_at'])
    op.create_index('idx_prediction_probability', 'token_launch_predictions', ['launch_probability'])
    
    # 2. 空投价值估算表
    op.create_table(
        'airdrop_value_estimates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('estimated_value_usd', sa.Integer()),
        sa.Column('estimated_value_cny', sa.Integer()),
        sa.Column('min_value_usd', sa.Integer()),
        sa.Column('max_value_usd', sa.Integer()),
        sa.Column('confidence', sa.String(20)),
        sa.Column('reference_category', sa.String(50)),
        sa.Column('historical_avg', sa.Integer()),
        sa.Column('tvl_adjustment', sa.DECIMAL(5, 2)),
        sa.Column('funding_adjustment', sa.DECIMAL(5, 2)),
        sa.Column('final_adjustment', sa.DECIMAL(5, 2)),
        sa.Column('estimated_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_estimate_project', 'airdrop_value_estimates', ['project_id', 'estimated_at'])
    op.create_index('idx_estimate_value', 'airdrop_value_estimates', ['estimated_value_usd'])
    
    # 3. 投资行动计划表
    op.create_table(
        'investment_action_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('project_tier', sa.String(1)),
        sa.Column('composite_score', sa.Integer()),
        sa.Column('total_budget', sa.Integer()),
        sa.Column('budget_breakdown', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('start_date', sa.String(20)),
        sa.Column('target_duration', sa.String(50)),
        sa.Column('urgency', sa.String(20)),
        sa.Column('expected_roi', sa.String(20)),
        sa.Column('airdrop_estimate', sa.Integer()),
        sa.Column('action_steps', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('total_steps', sa.Integer()),
        sa.Column('monitoring_metrics', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('alert_conditions', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('risks', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('stop_loss_conditions', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('completion_percentage', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_plan_project', 'investment_action_plans', ['project_id', 'created_at'])
    op.create_index('idx_plan_status', 'investment_action_plans', ['status', 'project_tier'])
    
    # 4. 项目发现记录表
    op.create_table(
        'project_discoveries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_name', sa.String(255), nullable=False),
        sa.Column('total_mentions', sa.Integer()),
        sa.Column('platform_mentions', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('num_platforms', sa.Integer()),
        sa.Column('signal_strength', sa.Integer()),
        sa.Column('first_discovered_at', sa.TIMESTAMP()),
        sa.Column('last_mentioned_at', sa.TIMESTAMP()),
        sa.Column('heat_score', sa.Integer()),
        sa.Column('mentions_24h', sa.Integer()),
        sa.Column('mentions_7d', sa.Integer()),
        sa.Column('growth_rate', sa.DECIMAL(5, 2)),
        sa.Column('is_trending', sa.Integer(), server_default='0'),
        sa.Column('is_surge', sa.Integer(), server_default='0'),
        sa.Column('surge_ratio', sa.DECIMAL(5, 2)),
        sa.Column('has_token', sa.Integer(), server_default='0'),
        sa.Column('mention_samples', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('discovery_status', sa.String(20), server_default='new'),
        sa.Column('discovered_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_discovery_project_name', 'project_discoveries', ['project_name'])
    op.create_index('idx_discovery_discovered_at', 'project_discoveries', ['discovered_at'])
    op.create_index('idx_discovery_signal', 'project_discoveries', ['signal_strength', 'discovered_at'])
    op.create_index('idx_discovery_heat', 'project_discoveries', ['heat_score', 'is_trending'])


def downgrade():
    op.drop_table('project_discoveries')
    op.drop_table('investment_action_plans')
    op.drop_table('airdrop_value_estimates')
    op.drop_table('token_launch_predictions')

