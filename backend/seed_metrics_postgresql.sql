-- 为项目添加社交指标、链上数据和AI分析

-- 1. 为所有项目添加社交指标
INSERT INTO social_metrics (
    project_id,
    twitter_followers,
    twitter_engagement_rate,
    telegram_members,
    discord_members,
    github_stars,
    github_commits,
    created_at,
    updated_at
)
SELECT 
    id,
    CASE 
        WHEN grade = 'S' THEN 500000 + FLOOR(RANDOM() * 500000)::INT
        WHEN grade = 'A' THEN 100000 + FLOOR(RANDOM() * 400000)::INT
        WHEN grade = 'B' THEN 20000 + FLOOR(RANDOM() * 80000)::INT
        ELSE 5000 + FLOOR(RANDOM() * 15000)::INT
    END as twitter_followers,
    ROUND((2.0 + RANDOM() * 6.0)::NUMERIC, 2) as twitter_engagement_rate,
    CASE 
        WHEN grade = 'S' THEN 50000 + FLOOR(RANDOM() * 200000)::INT
        WHEN grade = 'A' THEN 10000 + FLOOR(RANDOM() * 90000)::INT
        WHEN grade = 'B' THEN 2000 + FLOOR(RANDOM() * 18000)::INT
        ELSE 500 + FLOOR(RANDOM() * 2500)::INT
    END as telegram_members,
    CASE 
        WHEN grade = 'S' THEN 80000 + FLOOR(RANDOM() * 120000)::INT
        WHEN grade = 'A' THEN 20000 + FLOOR(RANDOM() * 80000)::INT
        WHEN grade = 'B' THEN 5000 + FLOOR(RANDOM() * 25000)::INT
        ELSE 1000 + FLOOR(RANDOM() * 5000)::INT
    END as discord_members,
    CASE 
        WHEN category = 'Infrastructure' THEN 1000 + FLOOR(RANDOM() * 4000)::INT
        WHEN category = 'DeFi' THEN 500 + FLOOR(RANDOM() * 2500)::INT
        ELSE 200 + FLOOR(RANDOM() * 800)::INT
    END as github_stars,
    CASE 
        WHEN category = 'Infrastructure' THEN 5000 + FLOOR(RANDOM() * 15000)::INT
        WHEN category = 'DeFi' THEN 2000 + FLOOR(RANDOM() * 8000)::INT
        ELSE 500 + FLOOR(RANDOM() * 2500)::INT
    END as github_commits,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM projects
WHERE id NOT IN (SELECT project_id FROM social_metrics);

-- 2. 为所有项目添加链上数据
INSERT INTO onchain_metrics (
    project_id,
    tvl_usd,
    daily_active_users,
    daily_transactions,
    total_transactions,
    unique_addresses,
    avg_transaction_value,
    contract_security_score,
    created_at,
    updated_at
)
SELECT 
    id,
    CASE 
        WHEN grade = 'S' THEN 1000000000 + FLOOR(RANDOM() * 9000000000)::BIGINT
        WHEN grade = 'A' THEN 100000000 + FLOOR(RANDOM() * 900000000)::BIGINT
        WHEN grade = 'B' THEN 10000000 + FLOOR(RANDOM() * 90000000)::BIGINT
        ELSE 1000000 + FLOOR(RANDOM() * 9000000)::BIGINT
    END as tvl_usd,
    CASE 
        WHEN grade = 'S' THEN 50000 + FLOOR(RANDOM() * 200000)::INT
        WHEN grade = 'A' THEN 10000 + FLOOR(RANDOM() * 90000)::INT
        WHEN grade = 'B' THEN 1000 + FLOOR(RANDOM() * 9000)::INT
        ELSE 100 + FLOOR(RANDOM() * 900)::INT
    END as daily_active_users,
    CASE 
        WHEN grade = 'S' THEN 100000 + FLOOR(RANDOM() * 400000)::INT
        WHEN grade = 'A' THEN 20000 + FLOOR(RANDOM() * 180000)::INT
        WHEN grade = 'B' THEN 2000 + FLOOR(RANDOM() * 18000)::INT
        ELSE 200 + FLOOR(RANDOM() * 1800)::INT
    END as daily_transactions,
    CASE 
        WHEN grade = 'S' THEN 50000000 + FLOOR(RANDOM() * 200000000)::BIGINT
        WHEN grade = 'A' THEN 5000000 + FLOOR(RANDOM() * 45000000)::BIGINT
        WHEN grade = 'B' THEN 500000 + FLOOR(RANDOM() * 4500000)::BIGINT
        ELSE 50000 + FLOOR(RANDOM() * 450000)::BIGINT
    END as total_transactions,
    CASE 
        WHEN grade = 'S' THEN 500000 + FLOOR(RANDOM() * 2000000)::INT
        WHEN grade = 'A' THEN 100000 + FLOOR(RANDOM() * 900000)::INT
        WHEN grade = 'B' THEN 10000 + FLOOR(RANDOM() * 90000)::INT
        ELSE 1000 + FLOOR(RANDOM() * 9000)::INT
    END as unique_addresses,
    ROUND((100.0 + RANDOM() * 10000.0)::NUMERIC, 2) as avg_transaction_value,
    ROUND((75.0 + RANDOM() * 25.0)::NUMERIC, 1) as contract_security_score,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM projects
WHERE id NOT IN (SELECT project_id FROM onchain_metrics);

-- 3. 为所有项目添加AI分析
INSERT INTO ai_analysis (
    project_id,
    innovation_score,
    team_score,
    community_score,
    market_potential_score,
    risk_level,
    strengths,
    weaknesses,
    opportunities,
    threats,
    recommendation,
    confidence_level,
    analyzed_at,
    created_at,
    updated_at
)
SELECT 
    id,
    ROUND((70.0 + RANDOM() * 30.0)::NUMERIC, 1) as innovation_score,
    ROUND((70.0 + RANDOM() * 30.0)::NUMERIC, 1) as team_score,
    ROUND((70.0 + RANDOM() * 30.0)::NUMERIC, 1) as community_score,
    ROUND((70.0 + RANDOM() * 30.0)::NUMERIC, 1) as market_potential_score,
    CASE 
        WHEN grade IN ('S', 'A') THEN 'low'
        WHEN grade = 'B' THEN 'medium'
        ELSE 'high'
    END as risk_level,
    ARRAY['技术创新领先', '团队经验丰富', '社区活跃度高', '生态发展迅速']::TEXT[] as strengths,
    ARRAY['市场竞争激烈', '监管风险', '技术迭代风险']::TEXT[] as weaknesses,
    ARRAY['市场扩张空间大', '跨链互操作', '机构采用潜力']::TEXT[] as opportunities,
    ARRAY['竞争对手压力', '技术风险', '市场波动']::TEXT[] as threats,
    CASE 
        WHEN grade = 'S' THEN '强烈推荐 - 行业龙头,长期持有价值高'
        WHEN grade = 'A' THEN '推荐关注 - 优质项目,值得投资'
        WHEN grade = 'B' THEN '谨慎关注 - 有潜力但需观察'
        ELSE '不推荐 - 风险较高,建议观望'
    END as recommendation,
    ROUND((80.0 + RANDOM() * 20.0)::NUMERIC, 1) as confidence_level,
    CURRENT_TIMESTAMP as analyzed_at,
    CURRENT_TIMESTAMP as created_at,
    CURRENT_TIMESTAMP as updated_at
FROM projects
WHERE id NOT IN (SELECT project_id FROM ai_analysis);

-- 4. 更新项目的分数(基于新添加的数据)
UPDATE projects p
SET 
    social_score = ROUND((
        (LEAST(sm.twitter_followers::NUMERIC / 10000, 30) * 0.3) +
        (sm.twitter_engagement_rate * 3) +
        (LEAST(sm.telegram_members::NUMERIC / 5000, 25) * 0.25) +
        (LEAST(sm.discord_members::NUMERIC / 5000, 25) * 0.25)
    )::NUMERIC, 1),
    onchain_score = ROUND((
        (LEAST(COALESCE(om.tvl_usd, 0)::NUMERIC / 10000000, 30) * 0.3) +
        (LEAST(COALESCE(om.daily_active_users, 0)::NUMERIC / 1000, 25) * 0.25) +
        (LEAST(COALESCE(om.daily_transactions, 0)::NUMERIC / 10000, 25) * 0.25) +
        (COALESCE(om.contract_security_score, 80) * 0.2)
    )::NUMERIC, 1),
    ai_score = ROUND((
        (COALESCE(ai.innovation_score, 75) * 0.3) +
        (COALESCE(ai.team_score, 75) * 0.25) +
        (COALESCE(ai.community_score, 75) * 0.25) +
        (COALESCE(ai.market_potential_score, 75) * 0.2)
    ) / 100 * 100::NUMERIC, 1)
FROM social_metrics sm
LEFT JOIN onchain_metrics om ON om.project_id = p.id
LEFT JOIN ai_analysis ai ON ai.project_id = p.id
WHERE sm.project_id = p.id;

-- 完成提示
SELECT '✅ 指标数据导入完成!' AS status;
SELECT 
    '项目' as item,
    COUNT(*) as total
FROM projects
UNION ALL
SELECT '社交指标', COUNT(*) FROM social_metrics
UNION ALL
SELECT '链上数据', COUNT(*) FROM onchain_metrics
UNION ALL
SELECT 'AI分析', COUNT(*) FROM ai_analysis;


