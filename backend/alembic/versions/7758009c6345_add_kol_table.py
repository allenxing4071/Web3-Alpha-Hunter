"""add_kol_table

Revision ID: 7758009c6345
Revises: 004
Create Date: 2025-10-07 01:43:04.515613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7758009c6345'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 kols 表
    op.create_table(
        'kols',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False, comment='用户名/handle'),
        sa.Column('display_name', sa.String(length=200), nullable=True, comment='显示名称'),
        sa.Column('platform', sa.String(length=50), nullable=False, comment='平台: twitter, youtube, etc.'),
        sa.Column('followers', sa.Integer(), nullable=True, comment='粉丝数'),
        sa.Column('following', sa.Integer(), nullable=True, comment='关注数'),
        sa.Column('total_posts', sa.Integer(), nullable=True, comment='总帖子数'),
        sa.Column('influence_score', sa.Numeric(precision=10, scale=2), nullable=True, comment='影响力评分 0-100'),
        sa.Column('engagement_rate', sa.Numeric(precision=5, scale=2), nullable=True, comment='互动率 %'),
        sa.Column('tier', sa.Integer(), nullable=True, comment='等级: 1-顶级, 2-优质, 3-普通'),
        sa.Column('category', sa.String(length=100), nullable=True, comment='主要类别: DeFi, NFT, GameFi等'),
        sa.Column('tags', sa.Text(), nullable=True, comment='标签，逗号分隔'),
        sa.Column('bio', sa.Text(), nullable=True, comment='个人简介'),
        sa.Column('location', sa.String(length=100), nullable=True, comment='地理位置'),
        sa.Column('website', sa.String(length=500), nullable=True, comment='个人网站'),
        sa.Column('verified', sa.Boolean(), nullable=True, comment='是否认证'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='状态: active, inactive, suspended'),
        sa.Column('profile_url', sa.String(length=500), nullable=True, comment='个人主页URL'),
        sa.Column('avatar_url', sa.String(length=500), nullable=True, comment='头像URL'),
        sa.Column('extra_data', sa.Text(), nullable=True, comment='额外数据(JSON格式)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True, comment='最后同步时间'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('ix_kols_id', 'kols', ['id'], unique=False)
    op.create_index('ix_kols_username', 'kols', ['username'], unique=True)
    op.create_index('ix_kols_platform', 'kols', ['platform'], unique=False)
    op.create_index('ix_kols_influence_score', 'kols', ['influence_score'], unique=False)
    op.create_index('ix_kols_tier', 'kols', ['tier'], unique=False)
    op.create_index('ix_kols_status', 'kols', ['status'], unique=False)


def downgrade():
    # 删除索引
    op.drop_index('ix_kols_status', table_name='kols')
    op.drop_index('ix_kols_tier', table_name='kols')
    op.drop_index('ix_kols_influence_score', table_name='kols')
    op.drop_index('ix_kols_platform', table_name='kols')
    op.drop_index('ix_kols_username', table_name='kols')
    op.drop_index('ix_kols_id', table_name='kols')
    
    # 删除表
    op.drop_table('kols')

