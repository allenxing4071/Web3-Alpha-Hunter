-- 为所有表添加示例数据

-- 1. 社交指标数据 (Social Metrics)
INSERT INTO social_metrics (project_id, twitter_followers, twitter_engagement_rate, telegram_members, telegram_active_rate, discord_members, community_sentiment, created_at) VALUES
(1, 450000, 3.5, 25000, 0.45, 35000, 0.85, NOW()),
(2, 380000, 4.2, 32000, 0.52, 28000, 0.88, NOW()),
(3, 320000, 5.1, 18000, 0.61, 15000, 0.92, NOW()),
(4, 280000, 3.8, 22000, 0.48, 20000, 0.82, NOW()),
(5, 190000, 4.5, 15000, 0.55, 12000, 0.86, NOW()),
(6, 420000, 3.9, 28000, 0.49, 32000, 0.87, NOW()),
(7, 510000, 3.2, 45000, 0.42, 48000, 0.84, NOW()),
(8, 380000, 4.1, 26000, 0.51, 22000, 0.89, NOW()),
(9, 340000, 4.3, 24000, 0.53, 25000, 0.88, NOW()),
(10, 220000, 3.7, 16000, 0.46, 14000, 0.81, NOW()),
(11, 250000, 3.6, 19000, 0.47, 17000, 0.83, NOW()),
(12, 180000, 4.8, 12000, 0.58, 10000, 0.90, NOW()),
(13, 150000, 4.2, 9000, 0.52, 8000, 0.85, NOW()),
(14, 280000, 3.9, 15000, 0.49, 18000, 0.82, NOW()),
(15, 320000, 4.0, 21000, 0.50, 23000, 0.86, NOW()),
(16, 240000, 4.4, 17000, 0.54, 16000, 0.87, NOW()),
(17, 160000, 3.8, 11000, 0.48, 9000, 0.84, NOW()),
(18, 200000, 4.1, 14000, 0.51, 13000, 0.85, NOW()),
(19, 290000, 3.7, 20000, 0.47, 19000, 0.83, NOW()),
(20, 170000, 3.5, 13000, 0.45, 11000, 0.80, NOW());

-- 2. 链上数据 (Onchain Metrics)
INSERT INTO onchain_metrics (project_id, tvl, transaction_volume, active_addresses, contract_interactions, token_holders, created_at) VALUES
(1, 4500000000, 2800000000, 125000, 850000, 420000, NOW()),
(2, 3200000000, 1900000000, 98000, 720000, 350000, NOW()),
(3, 2800000000, 2200000000, 85000, 680000, 280000, NOW()),
(4, 1500000000, 980000000, 62000, 450000, 180000, NOW()),
(5, 890000000, 520000000, 45000, 320000, 125000, NOW()),
(6, 2900000000, 1700000000, 92000, 690000, 340000, NOW()),
(7, 3800000000, 2100000000, 110000, 780000, 410000, NOW()),
(8, 3100000000, 1800000000, 95000, 710000, 360000, NOW()),
(9, 2700000000, 1600000000, 88000, 650000, 320000, NOW()),
(10, 1200000000, 780000000, 58000, 420000, 165000, NOW()),
(11, 1400000000, 850000000, 64000, 460000, 190000, NOW()),
(12, 980000000, 620000000, 48000, 350000, 140000, NOW()),
(13, 720000000, 450000000, 38000, 280000, 110000, NOW()),
(14, 850000000, 520000000, 42000, 310000, 125000, NOW()),
(15, 1900000000, 1200000000, 75000, 560000, 240000, NOW()),
(16, 1600000000, 980000000, 68000, 490000, 210000, NOW()),
(17, 680000000, 420000000, 35000, 260000, 95000, NOW()),
(18, 920000000, 580000000, 52000, 380000, 150000, NOW()),
(19, 1800000000, 1100000000, 72000, 530000, 230000, NOW()),
(20, 750000000, 480000000, 40000, 290000, 115000, NOW());

-- 3. AI分析数据 (AI Analysis)
INSERT INTO ai_analysis (project_id, tech_innovation_score, team_background_score, market_potential_score, risk_factors, opportunities, summary, created_at) VALUES
(1, 9.2, 9.5, 9.0, '{"factors": ["监管风险", "竞争激烈"]}', '{"items": ["市场份额第一", "品牌效应强"]}', 'Uniswap作为DEX龙头，技术成熟，团队优秀，市场地位稳固。主要风险来自监管和竞争。', NOW()),
(2, 9.0, 9.3, 8.8, '{"factors": ["技术复杂度", "用户教育成本"]}', '{"items": ["以太坊生态支持", "技术领先"]}', 'Arbitrum是以太坊L2的领先方案，技术先进，生态繁荣。需要持续优化用户体验。', NOW()),
(3, 8.8, 8.5, 9.1, '{"factors": ["Solana依赖", "市场波动"]}', '{"items": ["Solana生态核心", "交易量大"]}', 'Jupiter是Solana生态的关键基础设施，交易量和用户增长迅速。', NOW()),
(4, 8.2, 8.8, 8.5, '{"factors": ["跨链安全", "技术复杂"]}', '{"items": ["多链互操作", "市场需求大"]}', 'Wormhole连接多个主流公链，跨链需求持续增长，但需注意安全性。', NOW()),
(5, 7.9, 8.2, 8.3, '{"factors": ["MEV竞争", "技术门槛"]}', '{"items": ["质押市场大", "创新机制"]}', 'Jito在Solana质押领域创新，MEV优化有竞争力。', NOW()),
(6, 8.6, 9.0, 8.7, '{"factors": ["L2竞争", "去中心化权衡"]}', '{"items": ["以太坊官方支持", "生态成熟"]}', 'Optimism得到以太坊基金会支持，技术成熟，生态发展良好。', NOW()),
(7, 8.4, 8.9, 8.6, '{"factors": ["技术债务", "品牌转型"]}', '{"items": ["用户基数大", "多链布局"]}', 'Polygon用户基数大，正在向zkEVM转型，技术升级中。', NOW()),
(8, 8.7, 9.2, 8.9, '{"factors": ["监管风险", "中心化质疑"]}', '{"items": ["质押龙头", "收益稳定"]}', 'Lido是以太坊质押龙头，市场份额最大，但面临去中心化质疑。', NOW()),
(9, 8.7, 9.1, 8.8, '{"factors": ["智能合约风险", "市场竞争"]}', '{"items": ["借贷龙头", "多链部署"]}', 'Aave是DeFi借贷协议的标杆，技术成熟，多链部署成功。', NOW()),
(10, 8.0, 8.3, 8.2, '{"factors": ["Move生态小", "竞争激烈"]}', '{"items": ["技术创新", "团队强大"]}', 'Sui采用Move语言，技术创新，但生态还在早期发展阶段。', NOW()),
(11, 7.8, 8.5, 8.0, '{"factors": ["生态竞争", "代币经济"]}', '{"items": ["Meta背景", "技术先进"]}', 'Aptos团队来自Meta，技术实力强，但需要时间建立生态。', NOW()),
(12, 8.1, 8.4, 8.3, '{"factors": ["模块化复杂", "市场教育"]}', '{"items": ["技术创新", "DA需求增长"]}', 'Celestia开创模块化区块链，技术创新，DA需求持续增长。', NOW()),
(13, 7.6, 7.9, 7.8, '{"factors": ["市场小众", "流动性风险"]}', '{"items": ["利率衍生品创新", "收益优化"]}', 'Pendle在利率衍生品领域创新，适合专业用户。', NOW()),
(14, 7.3, 7.8, 7.5, '{"factors": ["NFT市场波动", "监管不确定"]}', '{"items": ["专业工具", "交易量大"]}', 'Blur为专业NFT交易者提供工具，市场份额可观。', NOW()),
(15, 8.5, 8.7, 8.4, '{"factors": ["衍生品监管", "技术复杂"]}', '{"items": ["衍生品龙头", "去中心化"]}', 'dYdX是去中心化衍生品交易所龙头，正在向自有链迁移。', NOW()),
(16, 8.3, 8.4, 8.5, '{"factors": ["Arbitrum依赖", "流动性竞争"]}', '{"items": ["GLP创新", "收益稳定"]}', 'GMX的GLP机制创新，为LP提供稳定收益。', NOW()),
(17, 7.7, 7.5, 8.0, '{"factors": ["AI竞争激烈", "代币价值捕获"]}', '{"items": ["GPU需求增长", "AI趋势"]}', 'Render受益于AI发展，GPU渲染需求增长。', NOW()),
(18, 7.9, 8.2, 7.8, '{"factors": ["NFT市场依赖", "技术门槛"]}', '{"items": ["零Gas费", "游戏NFT"]}', 'Immutable X专注游戏NFT，零Gas费是核心优势。', NOW()),
(19, 8.2, 8.6, 8.4, '{"factors": ["ZK技术复杂", "生态早期"]}', '{"items": ["技术领先", "以太坊支持"]}', 'StarkNet是ZK-Rollup领先方案，技术先进但生态还在建设中。', NOW()),
(20, 7.5, 7.8, 7.6, '{"factors": ["L2竞争", "品牌认知"]}', '{"items": ["Bybit支持", "模块化架构"]}', 'Mantle得到Bybit支持，资金充足，但需要建立品牌认知。', NOW());

-- 4. AI配置数据 (AI Config)
INSERT INTO ai_configs (id, name, api_key, enabled, model, created_at, updated_at) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'DeepSeek', 'sk-deepseek-test-key-encrypted-xxxxxxxxxxxxx', true, 'deepseek-chat', NOW(), NOW()),
('b2c3d4e5-f6g7-8901-bcde-fg2345678901', 'Claude', 'sk-ant-api-test-key-encrypted-xxxxxxxxxxxxxxxxx', false, 'claude-3-haiku-20240307', NOW(), NOW()),
('c3d4e5f6-g7h8-9012-cdef-gh3456789012', 'OpenAI', 'sk-openai-test-key-encrypted-xxxxxxxxxxxx', false, 'gpt-3.5-turbo', NOW(), NOW());

-- 5. 发币预测数据 (Token Launch Predictions)
INSERT INTO token_launch_predictions (project_id, launch_probability, predicted_timeframe, estimated_fdv_min, estimated_fdv_max, confidence_score, key_indicators, created_at) VALUES
(1, 0.0, 'Already Launched', 5000000000, 8000000000, 0.95, '{"indicators": ["已发币", "市值稳定"]}', NOW()),
(2, 0.0, 'Already Launched', 3000000000, 5000000000, 0.95, '{"indicators": ["已发币", "L2龙头"]}', NOW()),
(3, 0.0, 'Already Launched', 1500000000, 2500000000, 0.95, '{"indicators": ["已发币", "Solana生态"]}', NOW()),
(12, 0.85, 'Q2 2025', 500000000, 1200000000, 0.78, '{"indicators": ["技术成熟", "融资充足", "生态发展快"]}', NOW()),
(13, 0.72, 'Q3 2025', 200000000, 500000000, 0.68, '{"indicators": ["产品上线", "用户增长", "市场需求"]}', NOW()),
(17, 0.65, 'Q2-Q3 2025', 800000000, 1500000000, 0.72, '{"indicators": ["AI热点", "GPU需求", "合作伙伴多"]}', NOW()),
(20, 0.58, 'Q4 2025', 300000000, 800000000, 0.65, '{"indicators": ["Bybit支持", "技术进展", "生态建设"]}', NOW());

-- 6. 空投价值估算 (Airdrop Value Estimates)
INSERT INTO airdrop_value_estimates (project_id, airdrop_probability, estimated_value_min, estimated_value_max, participation_cost, roi_ratio, eligibility_criteria, created_at) VALUES
(12, 0.80, 500, 2000, 100, 15.0, '{"criteria": ["使用DA服务", "质押TIA", "参与测试网"]}', NOW()),
(13, 0.75, 300, 1200, 80, 10.0, '{"criteria": ["提供流动性", "交易量", "持有时间"]}', NOW()),
(17, 0.70, 800, 2500, 150, 12.0, '{"criteria": ["提供GPU算力", "完成任务", "社区贡献"]}', NOW()),
(19, 0.85, 1000, 3000, 200, 12.5, '{"criteria": ["部署合约", "桥接资产", "交互次数"]}', NOW()),
(20, 0.65, 400, 1500, 120, 8.0, '{"criteria": ["使用产品", "质押MNT", "推荐用户"]}', NOW());

-- 7. 投资行动计划 (Investment Action Plans)
INSERT INTO investment_action_plans (project_id, action_type, priority, action_steps, expected_outcome, time_commitment, resource_requirements, created_at) VALUES
(1, 'Hold & Stake', 'Medium', '{"steps": ["购买UNI代币", "参与流动性挖矿", "治理投票"]}', '稳定收益 + 治理权', '每周1小时', '{"capital": "1000-5000 USD", "technical": "基础"}', NOW()),
(3, 'Active Trading', 'High', '{"steps": ["使用Jupiter交易", "提供流动性", "参与IDO"]}', '交易返佣 + 空投机会', '每天2小时', '{"capital": "500-2000 USD", "technical": "中等"}', NOW()),
(12, 'Airdrop Farming', 'High', '{"steps": ["使用DA服务", "质押TIA", "参与测试网", "社区活动"]}', '空投价值 $500-2000', '每周3小时', '{"capital": "100-300 USD", "technical": "中等"}', NOW()),
(13, 'Liquidity Mining', 'Medium', '{"steps": ["提供流动性", "长期持有", "复投收益"]}', '年化收益 15-30%', '每周2小时', '{"capital": "1000-3000 USD", "technical": "中等"}', NOW()),
(17, 'GPU Mining', 'Medium', '{"steps": ["提供GPU算力", "完成渲染任务", "积累积分"]}', '挖矿收益 + 空投', '每天1小时', '{"capital": "GPU设备", "technical": "较高"}', NOW()),
(19, 'DeFi Interaction', 'High', '{"steps": ["桥接资产", "部署合约", "使用DeFi", "交互次数"]}', '空投价值 $1000-3000', '每周4小时', '{"capital": "200-500 USD", "technical": "较高"}', NOW());

-- 8. 项目发现记录 (Project Discoveries)
INSERT INTO project_discoveries (project_id, source_type, source_url, discovered_at, initial_score, discovery_context, created_at) VALUES
(1, 'coingecko_trending', 'https://coingecko.com/trending', NOW() - INTERVAL '30 days', 90.0, '{"context": "市值排名前10", "category": "DeFi"}', NOW()),
(2, 'github_trending', 'https://github.com/trending', NOW() - INTERVAL '25 days', 88.0, '{"context": "开发活跃度高", "category": "Infrastructure"}', NOW()),
(3, 'twitter_kol', 'https://twitter.com/solana', NOW() - INTERVAL '20 days', 87.0, '{"context": "KOL推荐", "category": "DeFi"}', NOW()),
(12, 'github_trending', 'https://github.com/celestiaorg', NOW() - INTERVAL '15 days', 78.0, '{"context": "技术创新", "category": "Infrastructure"}', NOW()),
(13, 'twitter_kol', 'https://twitter.com/pendle_fi', NOW() - INTERVAL '10 days', 72.0, '{"context": "DeFi创新", "category": "DeFi"}', NOW()),
(17, 'telegram_alpha', 'https://t.me/render_network', NOW() - INTERVAL '12 days', 75.0, '{"context": "AI热点", "category": "AI"}', NOW()),
(19, 'github_trending', 'https://github.com/starknet-io', NOW() - INTERVAL '18 days', 80.0, '{"context": "ZK技术", "category": "Infrastructure"}', NOW()),
(20, 'twitter_kol', 'https://twitter.com/0xMantle', NOW() - INTERVAL '8 days', 73.0, '{"context": "Bybit投资", "category": "Infrastructure"}', NOW());

-- 验证插入结果
SELECT 'Projects' as table_name, COUNT(*) as count FROM projects
UNION ALL
SELECT 'Social Metrics', COUNT(*) FROM social_metrics
UNION ALL
SELECT 'Onchain Metrics', COUNT(*) FROM onchain_metrics
UNION ALL
SELECT 'AI Analysis', COUNT(*) FROM ai_analysis
UNION ALL
SELECT 'AI Configs', COUNT(*) FROM ai_configs
UNION ALL
SELECT 'Token Launch Predictions', COUNT(*) FROM token_launch_predictions
UNION ALL
SELECT 'Airdrop Value Estimates', COUNT(*) FROM airdrop_value_estimates
UNION ALL
SELECT 'Investment Action Plans', COUNT(*) FROM investment_action_plans
UNION ALL
SELECT 'Project Discoveries', COUNT(*) FROM project_discoveries;
