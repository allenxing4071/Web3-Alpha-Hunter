-- =====================================================
-- AI智能助理系统 - 数据库表结构
-- =====================================================

-- 1. AI工作配置表
CREATE TABLE IF NOT EXISTS ai_work_config (
    id SERIAL PRIMARY KEY,
    
    -- 工作目标
    primary_goal TEXT DEFAULT '发现未发币的早期优质Web3项目',
    target_roi FLOAT DEFAULT 50.0, -- 目标ROI: 10-100倍
    risk_tolerance VARCHAR(50) DEFAULT 'aggressive', -- conservative, moderate, aggressive
    
    -- 项目筛选标准
    min_ai_score FLOAT DEFAULT 70.0, -- 低于此分数不推荐
    required_cross_validation BOOLEAN DEFAULT TRUE, -- 是否要求多平台验证
    min_platforms INTEGER DEFAULT 2, -- 至少在几个平台出现
    
    -- 时间窗口
    search_lookback_hours INTEGER DEFAULT 24, -- 搜索过去多少小时的数据
    project_age_limit_days INTEGER DEFAULT 180, -- 项目年龄不超过多少天
    
    -- 每日配额
    max_projects_per_day INTEGER DEFAULT 50, -- 每天最多推荐多少个项目
    max_kols_per_day INTEGER DEFAULT 20, -- 每天最多推荐多少个KOL
    
    -- AI行为规则 (JSON格式)
    rules JSONB DEFAULT '{
        "focus_areas": ["DeFi", "Layer2", "Infrastructure", "Gaming"],
        "exclude_categories": ["Meme币", "仿盘"],
        "project_criteria": {
            "must_have": ["团队公开", "有官方网站或GitHub", "社交媒体活跃"],
            "red_flags": ["承诺guaranteed returns", "白皮书抄袭率>80%", "域名注册<7天"]
        },
        "scoring_weights": {
            "team": 0.20,
            "tech": 0.25,
            "community": 0.20,
            "tokenomics": 0.15,
            "market": 0.10,
            "risk": 0.10
        }
    }'::jsonb,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认配置
INSERT INTO ai_work_config (id) VALUES (1)
ON CONFLICT (id) DO NOTHING;


-- 2. 平台搜索规则表
CREATE TABLE IF NOT EXISTS platform_search_rules (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL, -- twitter, telegram, discord
    
    -- 搜索策略
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 5, -- 1-10，优先级
    frequency_minutes INTEGER DEFAULT 5, -- 搜索频率（分钟）
    
    -- 搜索范围 (JSON格式)
    search_keywords JSONB, -- 关键词列表
    monitor_kols JSONB, -- KOL用户名列表
    monitor_channels JSONB, -- Telegram频道/Discord服务器
    
    -- 数据过滤
    min_engagement INTEGER DEFAULT 10, -- 最低互动数
    min_author_followers INTEGER DEFAULT 500, -- 作者最低粉丝数
    
    -- 限制
    max_results_per_run INTEGER DEFAULT 100, -- 每次最多抓取多少条
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(platform)
);

-- 插入默认平台规则
INSERT INTO platform_search_rules (platform, frequency_minutes, search_keywords, min_engagement, min_author_followers) VALUES
('twitter', 5, '[
    {"keyword": "presale", "category": "launch", "weight": 0.8},
    {"keyword": "airdrop", "category": "reward", "weight": 0.6},
    {"keyword": "testnet", "category": "development", "weight": 0.7},
    {"keyword": "fair launch", "category": "launch", "weight": 0.8},
    {"keyword": "new token", "category": "launch", "weight": 0.5},
    {"keyword": "seed round", "category": "funding", "weight": 0.9},
    {"keyword": "series A", "category": "funding", "weight": 0.9},
    {"keyword": "IDO", "category": "launch", "weight": 0.7},
    {"keyword": "TGE", "category": "launch", "weight": 0.8}
]'::jsonb, 10, 500),

('telegram', 15, '[
    {"keyword": "announcement", "category": "official", "weight": 0.9},
    {"keyword": "whitelist", "category": "opportunity", "weight": 0.8},
    {"keyword": "launch", "category": "launch", "weight": 0.7}
]'::jsonb, 0, 0),

('discord', 30, '[
    {"keyword": "announcement", "category": "official", "weight": 0.9},
    {"keyword": "alpha", "category": "opportunity", "weight": 0.8}
]'::jsonb, 0, 0)
ON CONFLICT (platform) DO NOTHING;


-- 3. AI学习反馈表
CREATE TABLE IF NOT EXISTS ai_learning_feedback (
    id SERIAL PRIMARY KEY,
    
    -- 反馈类型
    feedback_type VARCHAR(50) NOT NULL, -- project_review, kol_review, strategy_adjustment
    
    -- 关联对象
    related_project_id INTEGER,
    related_kol_id INTEGER,
    
    -- 用户决策
    user_decision VARCHAR(50), -- approved, rejected, modified
    user_reason TEXT,
    
    -- AI学习建议 (JSON格式)
    ai_should_adjust JSONB,
    adjustment_applied BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ai_feedback_type ON ai_learning_feedback(feedback_type);
CREATE INDEX IF NOT EXISTS idx_ai_feedback_decision ON ai_learning_feedback(user_decision);


-- 4. 待审核项目表（AI推荐的准信息）
CREATE TABLE IF NOT EXISTS projects_pending (
    id SERIAL PRIMARY KEY,
    
    -- 基础信息
    project_name VARCHAR(255) NOT NULL,
    symbol VARCHAR(50),
    description TEXT,
    
    -- 来源信息
    discovered_from VARCHAR(50), -- twitter, telegram, discord
    source_url TEXT, -- 原始推文/消息链接
    source_content TEXT, -- 原始内容
    
    -- AI分析结果
    ai_score FLOAT, -- AI初步评分（0-100）
    ai_grade VARCHAR(1), -- S, A, B, C
    ai_recommendation_reason JSONB, -- AI推荐理由 (JSON格式)
    ai_extracted_info JSONB, -- AI提取的信息（官网、社交媒体等）
    ai_confidence FLOAT, -- AI置信度（0-1）
    
    -- AI评分细节
    ai_team_score FLOAT,
    ai_tech_score FLOAT,
    ai_community_score FLOAT,
    ai_tokenomics_score FLOAT,
    ai_market_score FLOAT,
    ai_risk_score FLOAT,
    
    -- 审核状态
    review_status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    reviewed_by VARCHAR(255),
    reviewed_at TIMESTAMP,
    reject_reason TEXT,
    
    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_projects_pending_status ON projects_pending(review_status);
CREATE INDEX IF NOT EXISTS idx_projects_pending_score ON projects_pending(ai_score DESC);
CREATE INDEX IF NOT EXISTS idx_projects_pending_created ON projects_pending(created_at DESC);


-- 5. 待审核KOL表（AI发现的准信息）
CREATE TABLE IF NOT EXISTS kols_pending (
    id SERIAL PRIMARY KEY,
    
    platform VARCHAR(50) DEFAULT 'twitter',
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    
    -- 账号数据
    followers INTEGER,
    following INTEGER,
    tweets_count INTEGER,
    account_created_at TIMESTAMP,
    
    -- AI评估
    ai_recommendation_score FLOAT, -- 0-100
    ai_recommendation_reason JSONB, -- AI推荐理由 (JSON格式)
    ai_discovery_method VARCHAR(100), -- from_tier1_mention, from_comment, high_engagement, etc.
    
    -- 原始数据
    source_tweet_id VARCHAR(255),
    source_context TEXT,
    
    -- 审核状态
    review_status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    reviewed_by VARCHAR(255),
    reviewed_at TIMESTAMP,
    reject_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kols_pending_status ON kols_pending(review_status);
CREATE INDEX IF NOT EXISTS idx_kols_pending_score ON kols_pending(ai_recommendation_score DESC);


-- 6. 正式KOL表（添加新字段，兼容现有表）
-- 如果kols表不存在，则创建；如果存在，则添加缺失字段
CREATE TABLE IF NOT EXISTS kols (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) DEFAULT 'twitter',
    username VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    
    -- 账号数据
    followers INTEGER,
    following INTEGER,
    tweets_count INTEGER,
    account_created_at TIMESTAMP,
    
    -- 分级
    tier INTEGER DEFAULT 3, -- 1, 2, 3
    influence_score FLOAT DEFAULT 50.0, -- 0-100
    
    -- 标签
    tags JSONB DEFAULT '[]'::jsonb, -- ["DeFi", "NFT", "L2"]
    
    -- 统计
    total_mentions INTEGER DEFAULT 0,
    this_week_mentions INTEGER DEFAULT 0,
    avg_engagement_rate FLOAT DEFAULT 0.0,
    
    -- AI学习
    discovery_method VARCHAR(50) DEFAULT 'manual', -- manual, ai_discovered
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discovered_by VARCHAR(255) DEFAULT 'system',
    
    -- AI评估
    prediction_accuracy FLOAT DEFAULT 0.0, -- 预测准确率
    quality_score FLOAT DEFAULT 50.0, -- 内容质量
    
    -- 状态
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, deprecated
    is_verified BOOLEAN DEFAULT FALSE,
    
    last_checked_at TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kols_username ON kols(username);
CREATE INDEX IF NOT EXISTS idx_kols_tier ON kols(tier);
CREATE INDEX IF NOT EXISTS idx_kols_status ON kols(status);


-- 7. KOL表现追踪表
CREATE TABLE IF NOT EXISTS kol_performances (
    id SERIAL PRIMARY KEY,
    kol_id INTEGER REFERENCES kols(id) ON DELETE CASCADE,
    
    predicted_project VARCHAR(255),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    did_succeed BOOLEAN,
    
    tweet_id VARCHAR(255),
    likes INTEGER DEFAULT 0,
    retweets INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kol_perf_kol ON kol_performances(kol_id);
CREATE INDEX IF NOT EXISTS idx_kol_perf_date ON kol_performances(prediction_date DESC);


-- 8. Twitter关键词库表
CREATE TABLE IF NOT EXISTS twitter_keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100), -- presale, funding, airdrop, launch, development
    priority INTEGER DEFAULT 3, -- 1-5
    weight FLOAT DEFAULT 0.5, -- 0-1
    enabled BOOLEAN DEFAULT TRUE,
    match_count INTEGER DEFAULT 0,
    last_matched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认关键词
INSERT INTO twitter_keywords (keyword, category, priority, weight) VALUES
('presale', 'launch', 5, 0.8),
('airdrop', 'reward', 4, 0.6),
('testnet', 'development', 4, 0.7),
('mainnet', 'launch', 5, 0.9),
('fair launch', 'launch', 5, 0.8),
('stealth launch', 'launch', 4, 0.7),
('seed round', 'funding', 5, 0.9),
('series A', 'funding', 5, 0.9),
('raised $', 'funding', 4, 0.8),
('IDO', 'launch', 4, 0.7),
('ICO', 'launch', 3, 0.5),
('IEO', 'launch', 3, 0.5),
('TGE', 'launch', 4, 0.8),
('token launch', 'launch', 4, 0.7),
('whitelist', 'opportunity', 4, 0.6),
('early access', 'opportunity', 3, 0.5),
('no token yet', 'discovery', 5, 0.9),
('pre-token', 'discovery', 5, 0.9),
('未发币', 'discovery', 5, 0.9)
ON CONFLICT (keyword) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_twitter_keywords_enabled ON twitter_keywords(enabled);
CREATE INDEX IF NOT EXISTS idx_twitter_keywords_priority ON twitter_keywords(priority DESC);


-- 9. Telegram频道表
CREATE TABLE IF NOT EXISTS telegram_channels (
    id SERIAL PRIMARY KEY,
    channel_username VARCHAR(255) UNIQUE NOT NULL,
    channel_title VARCHAR(255),
    channel_type VARCHAR(50) DEFAULT 'general', -- news, announcements, alpha, vc, general
    member_count INTEGER DEFAULT 0,
    is_official BOOLEAN DEFAULT FALSE,
    quality_score INTEGER DEFAULT 50, -- 0-100
    enabled BOOLEAN DEFAULT TRUE,
    last_checked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_telegram_channels_enabled ON telegram_channels(enabled);
CREATE INDEX IF NOT EXISTS idx_telegram_channels_quality ON telegram_channels(quality_score DESC);


-- 10. Discord服务器表
CREATE TABLE IF NOT EXISTS discord_servers (
    id SERIAL PRIMARY KEY,
    server_id BIGINT UNIQUE NOT NULL,
    server_name VARCHAR(255),
    related_project VARCHAR(255),
    member_count INTEGER DEFAULT 0,
    online_count INTEGER DEFAULT 0,
    is_official BOOLEAN DEFAULT FALSE,
    activity_score INTEGER DEFAULT 50, -- 0-100
    enabled BOOLEAN DEFAULT TRUE,
    joined_at TIMESTAMP,
    last_checked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discord_servers_enabled ON discord_servers(enabled);
CREATE INDEX IF NOT EXISTS idx_discord_servers_activity ON discord_servers(activity_score DESC);


-- 11. 平台统计表（记录每日采集数据）
CREATE TABLE IF NOT EXISTS platform_daily_stats (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    stat_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- 采集数据
    data_collected INTEGER DEFAULT 0, -- 采集数据条数
    projects_discovered INTEGER DEFAULT 0, -- 发现项目数
    kols_discovered INTEGER DEFAULT 0, -- 发现KOL数
    
    -- AI推荐数据
    projects_recommended INTEGER DEFAULT 0, -- AI推荐项目数
    projects_approved INTEGER DEFAULT 0, -- 用户批准数
    projects_rejected INTEGER DEFAULT 0, -- 用户拒绝数
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(platform, stat_date)
);

CREATE INDEX IF NOT EXISTS idx_platform_stats_date ON platform_daily_stats(stat_date DESC);


-- =====================================================
-- 初始化默认数据
-- =====================================================

-- 插入15个Tier1 KOL（示例数据）
INSERT INTO kols (username, display_name, tier, influence_score, discovery_method, discovered_by, status, followers) VALUES
('VitalikButerin', 'Vitalik Buterin', 1, 98, 'manual', 'system', 'active', 5200000),
('cz_binance', 'CZ Binance', 1, 96, 'manual', 'system', 'active', 8700000),
('brian_armstrong', 'Brian Armstrong', 1, 94, 'manual', 'system', 'active', 1100000),
('APompliano', 'Anthony Pompliano', 1, 92, 'manual', 'system', 'active', 1800000),
('RaoulGMI', 'Raoul Pal', 1, 91, 'manual', 'system', 'active', 1200000),
('TheCryptoLark', 'Lark Davis', 1, 88, 'manual', 'system', 'active', 580000),
('CryptoCred', 'Crypto Cred', 1, 87, 'manual', 'system', 'active', 420000),
('IvanOnTech', 'Ivan on Tech', 1, 86, 'manual', 'system', 'active', 650000),
('CryptoWendyO', 'Wendy O', 1, 85, 'manual', 'system', 'active', 380000),
('hasufl', 'Hasu', 1, 89, 'manual', 'system', 'active', 180000),
('0xMaki', 'Maki', 1, 84, 'manual', 'system', 'active', 220000),
('DCinvestor', 'DCinvestor', 1, 86, 'manual', 'system', 'active', 160000),
('sassal0x', 'Sassal', 1, 85, 'manual', 'system', 'active', 140000),
('trentmc0', 'Trent McConaghy', 1, 83, 'manual', 'system', 'active', 95000),
('econoar', 'Ryan Sean Adams', 1, 87, 'manual', 'system', 'active', 280000)
ON CONFLICT (username) DO NOTHING;


-- 完成提示
SELECT 'AI智能助理系统数据库表创建完成!' as status;
SELECT COUNT(*) as kols_count FROM kols WHERE tier = 1;
SELECT COUNT(*) as keywords_count FROM twitter_keywords WHERE enabled = TRUE;

