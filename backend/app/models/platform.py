"""
平台监控相关模型 - 平台搜索规则、关键词、频道等
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, JSON, BigInteger
from sqlalchemy.sql import func
from app.db.session import Base


class PlatformSearchRule(Base):
    """平台搜索规则表 - 配置各平台的搜索策略"""
    __tablename__ = "platform_search_rules"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, unique=True, comment="平台名称: twitter, telegram, discord")

    # 搜索策略
    enabled = Column(Boolean, default=True, comment="是否启用")
    priority = Column(Integer, default=5, comment="优先级 1-10")
    frequency_minutes = Column(Integer, default=5, comment="搜索频率（分钟）")

    # 搜索范围 (JSON格式)
    search_keywords = Column(JSON, comment="关键词列表")
    monitor_kols = Column(JSON, comment="监控的KOL用户名列表")
    monitor_channels = Column(JSON, comment="Telegram频道/Discord服务器列表")

    # 数据过滤
    min_engagement = Column(Integer, default=10, comment="最低互动数")
    min_author_followers = Column(Integer, default=500, comment="作者最低粉丝数")

    # 限制
    max_results_per_run = Column(Integer, default=100, comment="每次最多抓取多少条")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PlatformSearchRule platform={self.platform} enabled={self.enabled}>"


class TwitterKeyword(Base):
    """Twitter关键词库表 - 用于Twitter内容监控的关键词"""
    __tablename__ = "twitter_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), unique=True, nullable=False, comment="关键词")
    category = Column(String(100), comment="分类: presale, funding, airdrop, launch, development")
    priority = Column(Integer, default=3, comment="优先级 1-5")
    weight = Column(Integer, default=0.5, comment="权重 0-1")
    enabled = Column(Boolean, default=True, index=True, comment="是否启用")
    match_count = Column(Integer, default=0, comment="匹配次数")
    last_matched_at = Column(DateTime(timezone=True), comment="最后匹配时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TwitterKeyword {self.keyword} category={self.category}>"


class TelegramChannel(Base):
    """Telegram频道表 - 监控的Telegram频道列表"""
    __tablename__ = "telegram_channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(String(255), unique=True, nullable=False, comment="频道用户名")
    channel_title = Column(String(255), comment="频道标题")
    channel_type = Column(String(50), default='general', comment="频道类型: news, announcements, alpha, vc, general")
    member_count = Column(Integer, default=0, comment="成员数")
    is_official = Column(Boolean, default=False, comment="是否官方频道")
    quality_score = Column(Integer, default=50, comment="质量评分 0-100")
    enabled = Column(Boolean, default=True, index=True, comment="是否启用")
    last_checked_at = Column(DateTime(timezone=True), comment="最后检查时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TelegramChannel {self.channel_username} type={self.channel_type}>"


class DiscordServer(Base):
    """Discord服务器表 - 监控的Discord服务器列表"""
    __tablename__ = "discord_servers"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(BigInteger, unique=True, nullable=False, comment="Discord服务器ID")
    server_name = Column(String(255), comment="服务器名称")
    related_project = Column(String(255), comment="关联项目名称")
    member_count = Column(Integer, default=0, comment="成员数")
    online_count = Column(Integer, default=0, comment="在线人数")
    is_official = Column(Boolean, default=False, comment="是否官方服务器")
    activity_score = Column(Integer, default=50, comment="活跃度评分 0-100")
    enabled = Column(Boolean, default=True, index=True, comment="是否启用")
    joined_at = Column(DateTime(timezone=True), comment="加入时间")
    last_checked_at = Column(DateTime(timezone=True), comment="最后检查时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DiscordServer {self.server_name} members={self.member_count}>"


class PlatformDailyStat(Base):
    """平台每日统计表 - 记录每日采集数据统计"""
    __tablename__ = "platform_daily_stats"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, comment="平台名称")
    stat_date = Column(Date, nullable=False, index=True, comment="统计日期")

    # 采集数据
    data_collected = Column(Integer, default=0, comment="采集数据条数")
    projects_discovered = Column(Integer, default=0, comment="发现项目数")
    kols_discovered = Column(Integer, default=0, comment="发现KOL数")

    # AI推荐数据
    projects_recommended = Column(Integer, default=0, comment="AI推荐项目数")
    projects_approved = Column(Integer, default=0, comment="用户批准数")
    projects_rejected = Column(Integer, default=0, comment="用户拒绝数")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PlatformDailyStat platform={self.platform} date={self.stat_date} collected={self.data_collected}>"
