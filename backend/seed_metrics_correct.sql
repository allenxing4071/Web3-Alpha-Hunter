-- 为项目添加社交指标、链上数据和AI分析(正确的表结构)

-- 1. 为所有项目添加社交指标
INSERT INTO social_metrics (
    project_id,
    twitter_followers,
    twitter_engagement_rate,
    telegram_members,
    telegram_online_members,
    telegram_message_frequency,
    discord_members,
    discord_online_members,
    youtube_mentions,
    youtube_total_views,
    github_stars,
    github_forks,
    github_commits_last_week,
    github_contributors,
    snapshot_time
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
    FLOOR(RANDOM() * 1000 + 100)::INT as telegram_online_members,
    FLOOR(RANDOM() * 50 + 10)::INT as telegram_message_frequency,
    CASE 
        WHEN grade = 'S' THEN 80000 + FLOOR(RANDOM() * 120000)::INT
        WHEN grade = 'A' THEN 20000 + FLOOR(RANDOM() * 80000)::INT
        WHEN grade = 'B' THEN 5000 + FLOOR(RANDOM() * 25000)::INT
        ELSE 1000 + FLOOR(RANDOM() * 5000)::INT
    END as discord_members,
    FLOOR(RANDOM() * 5000 + 500)::INT as discord_online_members,
    FLOOR(RANDOM() * 50 + 5)::INT as youtube_mentions,
    FLOOR(RANDOM() * 500000 + 10000)::INT as youtube_total_views,
    CASE 
        WHEN category = 'Infrastructure' THEN 1000 + FLOOR(RANDOM() * 4000)::INT
        WHEN category = 'DeFi' THEN 500 + FLOOR(RANDOM() * 2500)::INT
        ELSE 200 + FLOOR(RANDOM() * 800)::INT
    END as github_stars,
    FLOOR(RANDOM() * 500 + 50)::INT as github_forks,
    FLOOR(RANDOM() * 100 + 10)::INT as github_commits_last_week,
    FLOOR(RANDOM() * 50 + 5)::INT as github_contributors,
    CURRENT_TIMESTAMP
FROM projects
WHERE id NOT IN (SELECT project_id FROM social_metrics);

-- 2. 为所有项目添加链上数据
INSERT INTO onchain_metrics (
    project_id,
    market_cap,
    total_supply,
    circulating_supply,
    price_usd,
    liquidity_usd,
    volume_24h,
    holder_count,
    top_10_holders_percentage,
    transaction_count_24h,
    unique_wallets_24h,
    tvl_usd,
    snapshot_time
)
SELECT 
    id,
    CASE 
        WHEN grade = 'S' THEN (5000000000.0 + RANDOM() * 15000000000.0)::NUMERIC(20,2)
        WHEN grade = 'A' THEN (500000000.0 + RANDOM() * 4500000000.0)::NUMERIC(20,2)
        WHEN grade = 'B' THEN (50000000.0 + RANDOM() * 450000000.0)::NUMERIC(20,2)
        ELSE (5000000.0 + RANDOM() * 45000000.0)::NUMERIC(20,2)
    END as market_cap,
    (1000000000.0 + RANDOM() * 9000000000.0)::NUMERIC(30,2) as total_supply,
    (500000000.0 + RANDOM() * 4500000000.0)::NUMERIC(30,2) as circulating_supply,
    (0.01 + RANDOM() * 99.99)::NUMERIC(20,8) as price_usd,
    CASE 
        WHEN grade = 'S' THEN (100000000.0 + RANDOM() * 400000000.0)::NUMERIC(20,2)
        WHEN grade = 'A' THEN (10000000.0 + RANDOM() * 90000000.0)::NUMERIC(20,2)
        WHEN grade = 'B' THEN (1000000.0 + RANDOM() * 9000000.0)::NUMERIC(20,2)
        ELSE (100000.0 + RANDOM() * 900000.0)::NUMERIC(20,2)
    END as liquidity_usd,
    CASE 
        WHEN grade = 'S' THEN (50000000.0 + RANDOM() * 200000000.0)::NUMERIC(20,2)
        WHEN grade = 'A' THEN (5000000.0 + RANDOM() * 45000000.0)::NUMERIC(20,2)
        WHEN grade = 'B' THEN (500000.0 + RANDOM() * 4500000.0)::NUMERIC(20,2)
        ELSE (50000.0 + RANDOM() * 450000.0)::NUMERIC(20,2)
    END as volume_24h,
    CASE 
        WHEN grade = 'S' THEN 500000 + FLOOR(RANDOM() * 2000000)::INT
        WHEN grade = 'A' THEN 100000 + FLOOR(RANDOM() * 900000)::INT
        WHEN grade = 'B' THEN 10000 + FLOOR(RANDOM() * 90000)::INT
        ELSE 1000 + FLOOR(RANDOM() * 9000)::INT
    END as holder_count,
    ROUND((10.0 + RANDOM() * 40.0)::NUMERIC, 2) as top_10_holders_percentage,
    CASE 
        WHEN grade = 'S' THEN 100000 + FLOOR(RANDOM() * 400000)::INT
        WHEN grade = 'A' THEN 20000 + FLOOR(RANDOM() * 180000)::INT
        WHEN grade = 'B' THEN 2000 + FLOOR(RANDOM() * 18000)::INT
        ELSE 200 + FLOOR(RANDOM() * 1800)::INT
    END as transaction_count_24h,
    CASE 
        WHEN grade = 'S' THEN 50000 + FLOOR(RANDOM() * 200000)::INT
        WHEN grade = 'A' THEN 10000 + FLOOR(RANDOM() * 90000)::INT
        WHEN grade = 'B' THEN 1000 + FLOOR(RANDOM() * 9000)::INT
        ELSE 100 + FLOOR(RANDOM() * 900)::INT
    END as unique_wallets_24h,
    CASE 
        WHEN grade = 'S' THEN (1000000000.0 + RANDOM() * 9000000000.0)::NUMERIC(20,2)
        WHEN grade = 'A' THEN (100000000.0 + RANDOM() * 900000000.0)::NUMERIC(20,2)
        WHEN grade = 'B' THEN (10000000.0 + RANDOM() * 90000000.0)::NUMERIC(20,2)
        ELSE (1000000.0 + RANDOM() * 9000000.0)::NUMERIC(20,2)
    END as tvl_usd,
    CURRENT_TIMESTAMP
FROM projects
WHERE id NOT IN (SELECT project_id FROM onchain_metrics);

-- 3. 为所有项目添加AI分析
INSERT INTO ai_analysis (
    project_id,
    whitepaper_summary,
    key_features,
    similar_projects,
    sentiment_score,
    sentiment_label,
    risk_flags,
    scam_probability,
    investment_suggestion,
    position_size,
    entry_timing,
    stop_loss_percentage,
    analyzed_at
)
SELECT 
    id,
    description || ' - AI深度分析: 该项目在' || category || '领域展现出强大的技术实力和市场潜力。' as whitepaper_summary,
    jsonb_build_array(
        '创新技术架构',
        '强大的开发团队',
        '活跃的社区支持',
        '清晰的发展路线图'
    ) as key_features,
    jsonb_build_array() as similar_projects,
    CASE 
        WHEN grade = 'S' THEN ROUND((85.0 + RANDOM() * 15.0)::NUMERIC, 2)
        WHEN grade = 'A' THEN ROUND((70.0 + RANDOM() * 20.0)::NUMERIC, 2)
        WHEN grade = 'B' THEN ROUND((55.0 + RANDOM() * 20.0)::NUMERIC, 2)
        ELSE ROUND((40.0 + RANDOM() * 20.0)::NUMERIC, 2)
    END as sentiment_score,
    CASE 
        WHEN grade IN ('S', 'A') THEN 'positive'
        WHEN grade = 'B' THEN 'neutral'
        ELSE 'negative'
    END as sentiment_label,
    CASE 
        WHEN grade IN ('S', 'A') THEN '[]'::jsonb
        WHEN grade = 'B' THEN jsonb_build_array('市场竞争激烈')
        ELSE jsonb_build_array('高风险警告', '团队背景待验证')
    END as risk_flags,
    CASE 
        WHEN grade = 'S' THEN ROUND((0.0 + RANDOM() * 5.0)::NUMERIC, 2)
        WHEN grade = 'A' THEN ROUND((5.0 + RANDOM() * 10.0)::NUMERIC, 2)
        WHEN grade = 'B' THEN ROUND((15.0 + RANDOM() * 15.0)::NUMERIC, 2)
        ELSE ROUND((30.0 + RANDOM() * 30.0)::NUMERIC, 2)
    END as scam_probability,
    CASE 
        WHEN grade = 'S' THEN '强烈推荐 - 行业龙头项目,长期持有价值高,建议重仓配置'
        WHEN grade = 'A' THEN '推荐关注 - 优质项目,技术和市场表现优秀,建议中等仓位'
        WHEN grade = 'B' THEN '谨慎关注 - 有一定潜力但需持续观察,建议小仓位试探'
        ELSE '不推荐 - 风险较高,建议观望或避开'
    END as investment_suggestion,
    CASE 
        WHEN grade = 'S' THEN '30-50%'
        WHEN grade = 'A' THEN '15-30%'
        WHEN grade = 'B' THEN '5-15%'
        ELSE '0-5%'
    END as position_size,
    CASE 
        WHEN grade IN ('S', 'A') THEN '当前是较好的进入时机,建议分批建仓'
        WHEN grade = 'B' THEN '建议等待回调后小仓位进入'
        ELSE '暂不建议进入'
    END as entry_timing,
    CASE 
        WHEN grade = 'S' THEN ROUND((15.0 + RANDOM() * 10.0)::NUMERIC, 2)
        WHEN grade = 'A' THEN ROUND((20.0 + RANDOM() * 10.0)::NUMERIC, 2)
        WHEN grade = 'B' THEN ROUND((25.0 + RANDOM() * 10.0)::NUMERIC, 2)
        ELSE ROUND((30.0 + RANDOM() * 20.0)::NUMERIC, 2)
    END as stop_loss_percentage,
    CURRENT_TIMESTAMP
FROM projects
WHERE id NOT IN (SELECT project_id FROM ai_analysis);

-- 4. 更新项目表,关联新创建的指标ID
UPDATE projects p
SET 
    social_metrics_id = sm.id,
    onchain_metrics_id = om.id,
    ai_analysis_id = ai.id,
    updated_at = CURRENT_TIMESTAMP
FROM social_metrics sm
JOIN onchain_metrics om ON om.project_id = p.id
JOIN ai_analysis ai ON ai.project_id = p.id
WHERE sm.project_id = p.id;

-- 完成提示
SELECT '✅ 所有指标数据导入完成!' AS status;
SELECT 
    '项目' as item,
    COUNT(*) as total
FROM projects
UNION ALL
SELECT '社交指标', COUNT(*) FROM social_metrics
UNION ALL
SELECT '链上数据', COUNT(*) FROM onchain_metrics
UNION ALL
SELECT 'AI分析', COUNT(*) FROM ai_analysis
UNION ALL
SELECT '完整数据项目', COUNT(*) FROM projects 
WHERE social_metrics_id IS NOT NULL 
  AND onchain_metrics_id IS NOT NULL 
  AND ai_analysis_id IS NOT NULL;


