"""Fix table structure to match models

Revision ID: 004
Revises: 003
Create Date: 2025-01-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    """
    统一表结构，使其与 Model 定义完全一致
    """
    
    # ============ 修复 projects 表 ============
    
    # 检查并重命名列（如果存在旧的列名）
    # 从 name -> project_name
    connection = op.get_bind()
    
    # 检查是否存在 'name' 列
    result = connection.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='projects' AND column_name='name'
    """))
    
    if result.fetchone():
        # 如果存在 name 列，重命名为 project_name
        op.alter_column('projects', 'name', 
                       new_column_name='project_name',
                       existing_type=sa.String())
    
    # 添加缺失的列（如果不存在）
    try:
        op.add_column('projects', sa.Column('symbol', sa.String(50), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('contract_address', sa.String(255), nullable=True, unique=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('blockchain', sa.String(50), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('website', sa.String(500), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('whitepaper_url', sa.String(500), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('twitter_handle', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('telegram_channel', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('discord_link', sa.String(500), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('github_repo', sa.String(500), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('team_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('tech_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('community_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('tokenomics_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('market_timing_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('risk_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('grade', sa.String(1), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('status', sa.String(50), nullable=True, server_default='discovered'))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('first_discovered_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('discovered_from', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('logo_url', sa.String(500), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('projects', sa.Column('extra_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    except Exception:
        pass
    
    # 修改数据类型：overall_score 从 Float 改为 DECIMAL
    try:
        op.alter_column('projects', 'overall_score',
                       type_=sa.DECIMAL(5, 2),
                       existing_type=sa.Float())
    except Exception:
        pass
    
    # 添加索引
    try:
        op.create_index('ix_projects_project_name', 'projects', ['project_name'])
    except Exception:
        pass
    
    try:
        op.create_index('ix_projects_blockchain', 'projects', ['blockchain'])
    except Exception:
        pass
    
    try:
        op.create_index('ix_projects_category', 'projects', ['category'])
    except Exception:
        pass
    
    try:
        op.create_index('ix_projects_overall_score', 'projects', ['overall_score'])
    except Exception:
        pass
    
    try:
        op.create_index('ix_projects_grade', 'projects', ['grade'])
    except Exception:
        pass
    
    try:
        op.create_index('ix_projects_first_discovered_at', 'projects', ['first_discovered_at'])
    except Exception:
        pass
    
    try:
        op.create_index('idx_score_grade', 'projects', ['overall_score', 'grade'])
    except Exception:
        pass
    
    # ============ 修复 social_metrics 表 ============
    
    try:
        op.add_column('social_metrics', sa.Column('telegram_online_members', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('telegram_message_frequency', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('discord_online_members', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('youtube_mentions', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('youtube_total_views', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('github_stars', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('github_forks', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('github_commits_last_week', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('github_contributors', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('social_metrics', sa.Column('snapshot_time', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()))
    except Exception:
        pass
    
    # 修改 twitter_engagement_rate 数据类型
    try:
        op.alter_column('social_metrics', 'twitter_engagement_rate',
                       type_=sa.DECIMAL(5, 2),
                       existing_type=sa.Float())
    except Exception:
        pass
    
    # ============ 修复 onchain_metrics 表 ============
    
    # 重命名和添加缺失列
    try:
        op.add_column('onchain_metrics', sa.Column('market_cap', sa.DECIMAL(20, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('total_supply', sa.DECIMAL(30, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('circulating_supply', sa.DECIMAL(30, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('price_usd', sa.DECIMAL(20, 8), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('liquidity_usd', sa.DECIMAL(20, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('volume_24h', sa.DECIMAL(20, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('holder_count', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('top_10_holders_percentage', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('transaction_count_24h', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('unique_wallets_24h', sa.Integer(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('tvl_usd', sa.DECIMAL(20, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('onchain_metrics', sa.Column('snapshot_time', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()))
    except Exception:
        pass
    
    # ============ 修复 ai_analysis 表 ============
    
    try:
        op.add_column('ai_analysis', sa.Column('whitepaper_summary', sa.Text(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('key_features', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('similar_projects', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('sentiment_score', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('sentiment_label', sa.String(20), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('risk_flags', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('scam_probability', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('investment_suggestion', sa.Text(), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('position_size', sa.String(50), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('entry_timing', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('stop_loss_percentage', sa.DECIMAL(5, 2), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('ai_analysis', sa.Column('analyzed_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()))
    except Exception:
        pass


def downgrade():
    """
    回滚操作 - 如需要可以实现
    """
    pass

