"""
AI系统相关模型 - AI配置和学习反馈
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class AIWorkConfig(Base):
    """AI工作配置表 - AI助理的工作目标和筛选标准"""
    __tablename__ = "ai_work_config"

    id = Column(Integer, primary_key=True, index=True)

    # 工作目标
    primary_goal = Column(Text, default='发现未发币的早期优质Web3项目', comment="主要工作目标")
    target_roi = Column(Float, default=50.0, comment="目标ROI: 10-100倍")
    risk_tolerance = Column(String(50), default='aggressive', comment="风险承受度: conservative, moderate, aggressive")

    # 项目筛选标准
    min_ai_score = Column(Float, default=70.0, comment="最低AI评分，低于此分数不推荐")
    required_cross_validation = Column(Boolean, default=True, comment="是否要求多平台验证")
    min_platforms = Column(Integer, default=2, comment="至少在几个平台出现")

    # 时间窗口
    search_lookback_hours = Column(Integer, default=24, comment="搜索过去多少小时的数据")
    project_age_limit_days = Column(Integer, default=180, comment="项目年龄不超过多少天")

    # 每日配额
    max_projects_per_day = Column(Integer, default=50, comment="每天最多推荐多少个项目")
    max_kols_per_day = Column(Integer, default=20, comment="每天最多推荐多少个KOL")

    # AI行为规则 (JSON格式)
    rules = Column(JSON, comment="AI行为规则配置")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AIWorkConfig id={self.id} goal={self.primary_goal[:30]}...>"


class AILearningFeedback(Base):
    """AI学习反馈表 - 记录用户决策以供AI学习"""
    __tablename__ = "ai_learning_feedback"

    id = Column(Integer, primary_key=True, index=True)

    # 反馈类型
    feedback_type = Column(String(50), nullable=False, comment="反馈类型: project_review, kol_review, strategy_adjustment")

    # 关联对象
    related_project_id = Column(Integer, comment="关联的项目ID")
    related_kol_id = Column(Integer, comment="关联的KOL ID")

    # 用户决策
    user_decision = Column(String(50), comment="用户决策: approved, rejected, modified")
    user_reason = Column(Text, comment="用户决策理由")

    # AI学习建议 (JSON格式)
    ai_should_adjust = Column(JSON, comment="AI应该调整的内容")
    adjustment_applied = Column(Boolean, default=False, comment="调整是否已应用")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AILearningFeedback id={self.id} type={self.feedback_type} decision={self.user_decision}>"
