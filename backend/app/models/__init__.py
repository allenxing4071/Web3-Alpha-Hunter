"""数据模型"""

from app.models.project import (
    Project,
    SocialMetrics,
    OnchainMetrics,
    AIAnalysis,
)

from app.models.prediction import (
    TokenLaunchPrediction,
    AirdropValueEstimate,
    InvestmentActionPlan,
    ProjectDiscovery,
)

from app.models.pending_project import PendingProject
from app.models.user import User

from app.models.kol import (
    KOL,
    KOLPending,
    KOLPerformance,
)

from app.models.ai_system import (
    AIWorkConfig,
    AILearningFeedback,
)

from app.models.platform import (
    PlatformSearchRule,
    TwitterKeyword,
    TelegramChannel,
    DiscordServer,
    PlatformDailyStat,
)

from app.models.ai_config import AIConfig

__all__ = [
    # 项目相关
    "Project",
    "SocialMetrics",
    "OnchainMetrics",
    "AIAnalysis",
    "PendingProject",

    # 预测相关
    "TokenLaunchPrediction",
    "AirdropValueEstimate",
    "InvestmentActionPlan",
    "ProjectDiscovery",

    # 用户相关
    "User",

    # KOL相关
    "KOL",
    "KOLPending",
    "KOLPerformance",

    # AI系统相关
    "AIConfig",
    "AIWorkConfig",
    "AILearningFeedback",

    # 平台监控相关
    "PlatformSearchRule",
    "TwitterKeyword",
    "TelegramChannel",
    "DiscordServer",
    "PlatformDailyStat",
]

