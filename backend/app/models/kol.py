"""
KOL (Key Opinion Leader) 模型
用于存储Web3领域的影响力人物信息
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Numeric
from sqlalchemy.sql import func
from app.db.session import Base


class KOL(Base):
    """KOL模型 - Web3影响力人物"""
    __tablename__ = "kols"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    username = Column(String(100), unique=True, nullable=False, index=True, comment="用户名/handle")
    display_name = Column(String(200), comment="显示名称")
    platform = Column(String(50), nullable=False, index=True, comment="平台: twitter, youtube, etc.")
    
    # 社交数据
    followers = Column(Integer, default=0, comment="粉丝数")
    following = Column(Integer, default=0, comment="关注数")
    total_posts = Column(Integer, default=0, comment="总帖子数")
    
    # 影响力指标
    influence_score = Column(Numeric(10, 2), default=0, index=True, comment="影响力评分 0-100")
    engagement_rate = Column(Numeric(5, 2), default=0, comment="互动率 %")
    tier = Column(Integer, default=3, index=True, comment="等级: 1-顶级, 2-优质, 3-普通")
    
    # 分类标签
    category = Column(String(100), comment="主要类别: DeFi, NFT, GameFi等")
    tags = Column(Text, comment="标签，逗号分隔")
    
    # 个人简介
    bio = Column(Text, comment="个人简介")
    location = Column(String(100), comment="地理位置")
    website = Column(String(500), comment="个人网站")
    
    # 验证状态
    verified = Column(Boolean, default=False, comment="是否认证")
    status = Column(String(20), default='active', index=True, comment="状态: active, inactive, suspended")
    
    # 链接信息
    profile_url = Column(String(500), comment="个人主页URL")
    avatar_url = Column(String(500), comment="头像URL")
    
    # 额外元数据
    extra_data = Column(Text, comment="额外数据(JSON格式)")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    last_synced_at = Column(DateTime(timezone=True), comment="最后同步时间")
    
    def __repr__(self):
        return f"<KOL {self.username} ({self.platform}) - Score: {self.influence_score}>"

