"""预测与行动计划数据模型"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Text, DECIMAL, 
    TIMESTAMP, Index, JSON, ForeignKey
)
from sqlalchemy.sql import func
from app.db.session import Base


class TokenLaunchPrediction(Base):
    """代币发币概率预测"""
    
    __tablename__ = "token_launch_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True)
    
    # 预测结果
    launch_probability = Column(Integer)  # 0-100
    confidence = Column(String(20))  # Very Low, Low, Medium, High, Very High
    estimated_timeline = Column(String(100))  # "1-2个月内", "2-4个月内" 等
    
    # 检测到的信号
    detected_signals = Column(JSON)  # ["已宣布快照时间", "代币经济学已公开", ...]
    signal_count = Column(Integer)
    
    # 信号详情
    has_snapshot_announced = Column(Integer, default=0)  # 0 or 1
    has_tokenomics_published = Column(Integer, default=0)
    has_points_system = Column(Integer, default=0)
    has_audit_completed = Column(Integer, default=0)
    has_mainnet_live = Column(Integer, default=0)
    has_roadmap_token_mention = Column(Integer, default=0)
    
    # 时间戳
    predicted_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_prediction_project', 'project_id', 'predicted_at'),
        Index('idx_prediction_probability', 'launch_probability'),
    )
    
    def __repr__(self):
        return f"<TokenLaunchPrediction(project_id={self.project_id}, probability={self.launch_probability}%)>"


class AirdropValueEstimate(Base):
    """空投价值估算"""
    
    __tablename__ = "airdrop_value_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True)
    
    # 估算结果
    estimated_value_usd = Column(Integer)  # 美元
    estimated_value_cny = Column(Integer)  # 人民币
    
    # 价值区间
    min_value_usd = Column(Integer)
    max_value_usd = Column(Integer)
    
    # 置信度
    confidence = Column(String(20))  # Low, Medium, High
    
    # 参考数据
    reference_category = Column(String(50))  # DeFi, Layer2, NFT 等
    historical_avg = Column(Integer)  # 历史平均值
    
    # 调整因子
    tvl_adjustment = Column(DECIMAL(5, 2))  # TVL调整系数
    funding_adjustment = Column(DECIMAL(5, 2))  # 融资调整系数
    final_adjustment = Column(DECIMAL(5, 2))  # 最终调整系数
    
    # 时间戳
    estimated_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_estimate_project', 'project_id', 'estimated_at'),
        Index('idx_estimate_value', 'estimated_value_usd'),
    )
    
    def __repr__(self):
        return f"<AirdropValueEstimate(project_id={self.project_id}, value=${self.estimated_value_usd})>"


class InvestmentActionPlan(Base):
    """投资行动计划"""
    
    __tablename__ = "investment_action_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True)
    
    # 项目信息
    project_tier = Column(String(1))  # S, A, B, C
    composite_score = Column(Integer)
    
    # 预算分配
    total_budget = Column(Integer)  # 人民币
    budget_breakdown = Column(JSON)  # {"主要资金": {"金额": 1000, "说明": "..."}, ...}
    
    # 时间规划
    start_date = Column(String(20))
    target_duration = Column(String(50))
    urgency = Column(String(20))  # Normal, High, Critical
    
    # 预期收益
    expected_roi = Column(String(20))  # "5.0倍", "10.0倍"
    airdrop_estimate = Column(Integer)  # 预估空投价值（美元）
    
    # 行动步骤
    action_steps = Column(JSON)  # [{"step_number": 1, "action": "...", ...}, ...]
    total_steps = Column(Integer)
    
    # 监控与风险
    monitoring_metrics = Column(JSON)  # ["指标1", "指标2", ...]
    alert_conditions = Column(JSON)  # ["条件1", "条件2", ...]
    risks = Column(JSON)  # ["风险1", "风险2", ...]
    stop_loss_conditions = Column(JSON)  # ["止损1", "止损2", ...]
    
    # 状态
    status = Column(String(20), default="active")  # active, completed, cancelled
    completion_percentage = Column(Integer, default=0)  # 0-100
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_plan_project', 'project_id', 'created_at'),
        Index('idx_plan_status', 'status', 'project_tier'),
    )
    
    def __repr__(self):
        return f"<InvestmentActionPlan(project_id={self.project_id}, tier={self.project_tier}, budget=¥{self.total_budget})>"


class ProjectDiscovery(Base):
    """项目发现记录"""
    
    __tablename__ = "project_discoveries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 项目信息
    project_name = Column(String(255), nullable=False, index=True)
    
    # 发现数据
    total_mentions = Column(Integer)  # 总提及次数
    platform_mentions = Column(JSON)  # {"twitter": 5, "telegram": 3, ...}
    num_platforms = Column(Integer)  # 覆盖平台数
    
    # 信号强度
    signal_strength = Column(Integer)  # 0-100
    
    # 时间
    first_discovered_at = Column(TIMESTAMP, index=True)
    last_mentioned_at = Column(TIMESTAMP)
    
    # 热度数据
    heat_score = Column(Integer)  # 0-100
    mentions_24h = Column(Integer)
    mentions_7d = Column(Integer)
    growth_rate = Column(DECIMAL(5, 2))
    is_trending = Column(Integer, default=0)  # 0 or 1
    
    # 突发检测
    is_surge = Column(Integer, default=0)  # 0 or 1
    surge_ratio = Column(DECIMAL(5, 2))
    
    # 代币状态
    has_token = Column(Integer, default=0)  # 0 or 1
    
    # 提及样本
    mention_samples = Column(JSON)  # [{"platform": "twitter", "text": "...", ...}, ...]
    
    # 状态
    discovery_status = Column(String(20), default="new")  # new, verified, false_positive
    
    # 时间戳
    discovered_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_discovery_signal', 'signal_strength', 'discovered_at'),
        Index('idx_discovery_heat', 'heat_score', 'is_trending'),
    )
    
    def __repr__(self):
        return f"<ProjectDiscovery(name='{self.project_name}', signal={self.signal_strength}, platforms={self.num_platforms})>"

