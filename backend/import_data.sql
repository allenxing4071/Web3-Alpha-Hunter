-- 导入本地数据到云服务器PostgreSQL

-- 1. 创建 platform_search_rules 表
CREATE TABLE IF NOT EXISTS platform_search_rules (
    platform VARCHAR(50) PRIMARY KEY,
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 5,
    frequency_minutes INTEGER DEFAULT 60,
    search_keywords JSONB DEFAULT '[]',
    min_engagement INTEGER DEFAULT 10,
    min_author_followers INTEGER DEFAULT 500,
    max_results_per_run INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 创建 ai_configs 表
CREATE TABLE IF NOT EXISTS ai_configs (
    id VARCHAR(50) PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    api_key_encrypted TEXT NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 创建 platform_daily_stats 表
CREATE TABLE IF NOT EXISTS platform_daily_stats (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    stat_date DATE NOT NULL,
    collections_count INTEGER DEFAULT 0,
    projects_found INTEGER DEFAULT 0,
    kols_found INTEGER DEFAULT 0,
    ai_recommendations INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, stat_date)
);

-- 4. 插入平台配置数据
INSERT INTO platform_search_rules (platform, enabled, priority, frequency_minutes, search_keywords, min_engagement, min_author_followers, max_results_per_run, created_at, updated_at)
VALUES 
    ('twitter', TRUE, 5, 5, '[]'::jsonb, 10, 500, 100, '2025-10-07 05:07:18', '2025-10-07 05:07:18'),
    ('telegram', TRUE, 5, 15, '[]'::jsonb, 10, 500, 100, '2025-10-07 05:07:18', '2025-10-07 05:07:18'),
    ('discord', TRUE, 5, 30, '[]'::jsonb, 10, 500, 100, '2025-10-07 05:07:18', '2025-10-07 05:07:18')
ON CONFLICT (platform) DO UPDATE SET
    enabled = EXCLUDED.enabled,
    priority = EXCLUDED.priority,
    frequency_minutes = EXCLUDED.frequency_minutes,
    updated_at = CURRENT_TIMESTAMP;

-- 5. 插入AI配置数据
INSERT INTO ai_configs (id, provider, api_key_encrypted, enabled, model, created_at, updated_at)
VALUES 
    ('c7c8e93d-a694-47bb-895b-269c4c069afa', 'DeepSeek', 'gAAAAABo4UADZXdlZxlA4pucqlqAQf81yEmzoJjNkOlng4BjSYz_ISqZp9zIqtfVJ2EEvhq5tOSfK1hVLBYw21rEOqbDYn0woZu7Vx_spampwStNCcyk7bl1VxCApeS41hk4Gxj30-I2', TRUE, 'deepseek-chat', '2025-10-04 15:26:19', '2025-10-04 15:40:51'),
    ('12c02b73-1bb2-48bb-b77c-8c59a27dae1b', 'Claude', 'gAAAAABo4UADlPmdfh7owYFmaP9o_tsYSyBeJqSqTmbulYV5G96UHFQ95noiDIBm_21RALS4tckX8yhyvzqwDm7pEEEKP-1KffW24S1DCwDaPepZW8RttSd60dFK7EDrAwBftEpzfNz8zdfS-HyLxKUicqNzp5w5PQ==', TRUE, 'claude-3-5-sonnet-20241022', '2025-10-04 15:26:19', '2025-10-04 15:40:51'),
    ('830b09d3-df28-42b5-b6d7-bae3514329e8', 'OpenAI', 'gAAAAABo4UADY7WCBdpDjJUjoER_taNvajVuaWhkLBwuRkMusNASO4jU1aAq99gYcmmd00ieodR86AJkFuc-_SZPSUTsqiRqfcRU1G3idgajA9FUIyv9-gBZMzTgwOp6jCuMxIDTACFejqx7N7Oao1QHw7wDjV2sGw==', TRUE, 'gpt-3.5-turbo', '2025-10-04 15:26:19', '2025-10-04 15:40:51')
ON CONFLICT (id) DO UPDATE SET
    provider = EXCLUDED.provider,
    api_key_encrypted = EXCLUDED.api_key_encrypted,
    enabled = EXCLUDED.enabled,
    model = EXCLUDED.model,
    updated_at = CURRENT_TIMESTAMP;

-- 完成
SELECT '✅ 数据导入完成!' AS status;
SELECT COUNT(*) AS platform_count FROM platform_search_rules;
SELECT COUNT(*) AS ai_config_count FROM ai_configs;


