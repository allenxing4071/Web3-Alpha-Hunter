-- Web3 Alpha Hunter 数据库完整初始化脚本
-- 删除所有表（如果存在）
DROP TABLE IF EXISTS investment_action_plans CASCADE;
DROP TABLE IF EXISTS airdrop_value_estimates CASCADE;
DROP TABLE IF EXISTS token_launch_predictions CASCADE;
DROP TABLE IF EXISTS project_discoveries CASCADE;
DROP TABLE IF EXISTS projects_pending CASCADE;
DROP TABLE IF EXISTS ai_analysis CASCADE;
DROP TABLE IF EXISTS onchain_metrics CASCADE;
DROP TABLE IF EXISTS social_metrics CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS kols CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. 用户表
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- 2. KOL表
CREATE TABLE kols (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200),
    platform VARCHAR(50) NOT NULL,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    total_posts INTEGER DEFAULT 0,
    influence_score NUMERIC(10,2) DEFAULT 0,
    engagement_rate NUMERIC(5,2) DEFAULT 0,
    tier INTEGER DEFAULT 3,
    category VARCHAR(100),
    tags TEXT,
    bio TEXT,
    location VARCHAR(100),
    website VARCHAR(500),
    verified BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    profile_url VARCHAR(500),
    avatar_url VARCHAR(500),
    extra_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_synced_at TIMESTAMP
);

CREATE INDEX idx_kols_username ON kols(username);
CREATE INDEX idx_kols_platform ON kols(platform);
CREATE INDEX idx_kols_influence_score ON kols(influence_score);
CREATE INDEX idx_kols_tier ON kols(tier);
CREATE INDEX idx_kols_status ON kols(status);

-- 3. 社交指标表
CREATE TABLE social_metrics (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    twitter_followers INTEGER,
    twitter_engagement_rate NUMERIC(5,2),
    telegram_members INTEGER,
    telegram_online_members INTEGER,
    telegram_message_frequency INTEGER,
    discord_members INTEGER,
    discord_online_members INTEGER,
    youtube_mentions INTEGER,
    youtube_total_views INTEGER,
    github_stars INTEGER,
    github_forks INTEGER,
    github_commits_last_week INTEGER,
    github_contributors INTEGER,
    snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_social_metrics_project ON social_metrics(project_id, snapshot_time);

-- 4. 链上指标表
CREATE TABLE onchain_metrics (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    market_cap NUMERIC(20,2),
    total_supply NUMERIC(30,2),
    circulating_supply NUMERIC(30,2),
    price_usd NUMERIC(20,8),
    liquidity_usd NUMERIC(20,2),
    volume_24h NUMERIC(20,2),
    holder_count INTEGER,
    top_10_holders_percentage NUMERIC(5,2),
    transaction_count_24h INTEGER,
    unique_wallets_24h INTEGER,
    tvl_usd NUMERIC(20,2),
    snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_onchain_metrics_project ON onchain_metrics(project_id, snapshot_time);

-- 5. 项目主表
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    symbol VARCHAR(50),
    contract_address VARCHAR(255) UNIQUE,
    blockchain VARCHAR(50),
    category VARCHAR(100),
    description TEXT,
    website VARCHAR(500),
    whitepaper_url VARCHAR(500),
    twitter_handle VARCHAR(100),
    telegram_channel VARCHAR(100),
    discord_link VARCHAR(500),
    github_repo VARCHAR(500),
    overall_score NUMERIC(5,2),
    team_score NUMERIC(5,2),
    tech_score NUMERIC(5,2),
    community_score NUMERIC(5,2),
    tokenomics_score NUMERIC(5,2),
    market_timing_score NUMERIC(5,2),
    risk_score NUMERIC(5,2),
    grade VARCHAR(1),
    social_metrics_id INTEGER REFERENCES social_metrics(id) ON DELETE SET NULL,
    onchain_metrics_id INTEGER REFERENCES onchain_metrics(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'discovered',
    first_discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discovered_from VARCHAR(100),
    logo_url VARCHAR(500),
    extra_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_name ON projects(project_name);
CREATE INDEX idx_projects_blockchain ON projects(blockchain);
CREATE INDEX idx_projects_category ON projects(category);
CREATE INDEX idx_projects_score ON projects(overall_score);
CREATE INDEX idx_projects_grade ON projects(grade);
CREATE INDEX idx_projects_score_grade ON projects(overall_score, grade);
CREATE INDEX idx_projects_discovered_at ON projects(first_discovered_at);
CREATE INDEX idx_projects_social_metrics ON projects(social_metrics_id);
CREATE INDEX idx_projects_onchain_metrics ON projects(onchain_metrics_id);

-- 6. AI分析表
CREATE TABLE ai_analysis (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    whitepaper_summary TEXT,
    key_features JSONB,
    similar_projects JSONB,
    sentiment_score NUMERIC(5,2),
    sentiment_label VARCHAR(20),
    risk_flags JSONB,
    scam_probability NUMERIC(5,2),
    investment_suggestion TEXT,
    position_size VARCHAR(50),
    entry_timing VARCHAR(100),
    stop_loss_percentage NUMERIC(5,2),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_analysis_project ON ai_analysis(project_id);

-- 7. 待审核项目表
CREATE TABLE projects_pending (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    symbol VARCHAR(50),
    description TEXT,
    discovered_from VARCHAR(100),
    source_url VARCHAR(500),
    ai_score NUMERIC(5,2),
    ai_grade VARCHAR(1),
    ai_confidence NUMERIC(5,2),
    ai_recommendation_reason JSONB,
    ai_extracted_info JSONB,
    review_status VARCHAR(20) DEFAULT 'pending',
    reviewed_at TIMESTAMP,
    reviewed_by VARCHAR(100),
    reject_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pending_name ON projects_pending(project_name);
CREATE INDEX idx_pending_status ON projects_pending(review_status);
CREATE INDEX idx_pending_status_score ON projects_pending(review_status, ai_score);
CREATE INDEX idx_pending_created ON projects_pending(created_at);

-- 8. 项目发现记录表
CREATE TABLE project_discoveries (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    total_mentions INTEGER,
    platform_mentions JSONB,
    num_platforms INTEGER,
    signal_strength INTEGER,
    first_discovered_at TIMESTAMP,
    last_mentioned_at TIMESTAMP,
    heat_score INTEGER,
    mentions_24h INTEGER,
    mentions_7d INTEGER,
    growth_rate NUMERIC(5,2),
    is_trending INTEGER DEFAULT 0,
    is_surge INTEGER DEFAULT 0,
    surge_ratio NUMERIC(5,2),
    has_token INTEGER DEFAULT 0,
    mention_samples JSONB,
    discovery_status VARCHAR(20) DEFAULT 'new',
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_discoveries_name ON project_discoveries(project_name);
CREATE INDEX idx_discoveries_signal ON project_discoveries(signal_strength, discovered_at);
CREATE INDEX idx_discoveries_heat ON project_discoveries(heat_score, is_trending);
CREATE INDEX idx_discoveries_discovered ON project_discoveries(discovered_at);

-- 9. 代币发币预测表
CREATE TABLE token_launch_predictions (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) NOT NULL,
    launch_probability INTEGER,
    confidence VARCHAR(20),
    estimated_timeline VARCHAR(100),
    detected_signals JSONB,
    signal_count INTEGER,
    has_snapshot_announced INTEGER DEFAULT 0,
    has_tokenomics_published INTEGER DEFAULT 0,
    has_points_system INTEGER DEFAULT 0,
    has_audit_completed INTEGER DEFAULT 0,
    has_mainnet_live INTEGER DEFAULT 0,
    has_roadmap_token_mention INTEGER DEFAULT 0,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prediction_project ON token_launch_predictions(project_id, predicted_at);
CREATE INDEX idx_prediction_probability ON token_launch_predictions(launch_probability);

-- 10. 空投价值估算表
CREATE TABLE airdrop_value_estimates (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) NOT NULL,
    estimated_value_usd INTEGER,
    estimated_value_cny INTEGER,
    min_value_usd INTEGER,
    max_value_usd INTEGER,
    confidence VARCHAR(20),
    reference_category VARCHAR(50),
    historical_avg INTEGER,
    tvl_adjustment NUMERIC(5,2),
    funding_adjustment NUMERIC(5,2),
    final_adjustment NUMERIC(5,2),
    estimated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_estimate_project ON airdrop_value_estimates(project_id, estimated_at);
CREATE INDEX idx_estimate_value ON airdrop_value_estimates(estimated_value_usd);

-- 11. 投资行动计划表
CREATE TABLE investment_action_plans (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) NOT NULL,
    project_tier VARCHAR(1),
    composite_score INTEGER,
    total_budget INTEGER,
    budget_breakdown JSONB,
    start_date VARCHAR(20),
    target_duration VARCHAR(50),
    urgency VARCHAR(20),
    expected_roi VARCHAR(20),
    airdrop_estimate INTEGER,
    action_steps JSONB,
    total_steps INTEGER,
    monitoring_metrics JSONB,
    alert_conditions JSONB,
    risks JSONB,
    stop_loss_conditions JSONB,
    status VARCHAR(20) DEFAULT 'active',
    completion_percentage INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_plan_project ON investment_action_plans(project_id, created_at);
CREATE INDEX idx_plan_status ON investment_action_plans(status, project_tier);

-- 插入默认管理员用户
INSERT INTO users (id, username, email, password_hash, role, is_active, created_at, updated_at)
VALUES (
    'admin-001',
    'admin',
    'admin@web3hunter.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWEgaSIO', -- admin123
    'admin',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (id) DO NOTHING;

-- 完成
SELECT 'Database initialization completed!' AS status;

