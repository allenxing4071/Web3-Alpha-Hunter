"""add metrics relations to projects

Revision ID: 005_add_metrics_relations
Revises: 004_fix_table_structure
Create Date: 2025-10-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_metrics_relations'
down_revision = '7758009c6345'  # 最新的migration
branch_labels = None
depends_on = None


def upgrade():
    # 添加外键列
    op.add_column('projects', sa.Column('social_metrics_id', sa.Integer(), nullable=True))
    op.add_column('projects', sa.Column('onchain_metrics_id', sa.Integer(), nullable=True))
    
    # 创建外键约束
    op.create_foreign_key(
        'fk_projects_social_metrics',
        'projects', 'social_metrics',
        ['social_metrics_id'], ['id'],
        ondelete='SET NULL'
    )
    
    op.create_foreign_key(
        'fk_projects_onchain_metrics',
        'projects', 'onchain_metrics',
        ['onchain_metrics_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # 创建索引以提升查询性能
    op.create_index('ix_projects_social_metrics_id', 'projects', ['social_metrics_id'])
    op.create_index('ix_projects_onchain_metrics_id', 'projects', ['onchain_metrics_id'])


def downgrade():
    # 删除索引
    op.drop_index('ix_projects_onchain_metrics_id', 'projects')
    op.drop_index('ix_projects_social_metrics_id', 'projects')
    
    # 删除外键
    op.drop_constraint('fk_projects_onchain_metrics', 'projects', type_='foreignkey')
    op.drop_constraint('fk_projects_social_metrics', 'projects', type_='foreignkey')
    
    # 删除列
    op.drop_column('projects', 'onchain_metrics_id')
    op.drop_column('projects', 'social_metrics_id')
