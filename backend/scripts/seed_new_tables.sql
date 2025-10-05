-- 为新的4张表添加示例数据（根据实际表结构）

-- 1. 发币预测数据 (Token Launch Predictions)
INSERT INTO token_launch_predictions (
    project_id, launch_probability, confidence, estimated_timeline, 
    detected_signals, signal_count, has_snapshot_announced, has_tokenomics_published,
    has_points_system, has_audit_completed, has_mainnet_live, has_roadmap_token_mention
) VALUES
(12, 85, 'High', 'Q2 2025 (3-6个月)', 
 '{"signals": ["测试网活跃", "融资完成", "路线图明确"]}', 3, 0, 1, 1, 1, 1, 1),
(13, 72, 'Medium', 'Q3 2025 (6-9个月)', 
 '{"signals": ["产品上线", "用户增长"]}', 2, 0, 0, 1, 0, 1, 0),
(17, 65, 'Medium', 'Q2-Q3 2025 (4-8个月)', 
 '{"signals": ["AI热点", "合作伙伴", "积分系统"]}', 3, 0, 0, 1, 0, 1, 1),
(20, 58, 'Medium-Low', 'Q4 2025 (9-12个月)', 
 '{"signals": ["Bybit支持", "技术进展"]}', 2, 0, 0, 0, 0, 1, 0);

-- 2. 空投价值估算 (Airdrop Value Estimates)
INSERT INTO airdrop_value_estimates (
    project_id, estimated_value_usd, estimated_value_cny, min_value_usd, max_value_usd,
    confidence, reference_category, historical_avg, tvl_adjustment, funding_adjustment, final_adjustment
) VALUES
(12, 1200, 8400, 500, 2000, 'High', 'Infrastructure', 800, 1.2, 1.3, 1.25),
(13, 750, 5250, 300, 1200, 'Medium', 'DeFi', 600, 1.0, 1.1, 1.05),
(17, 1500, 10500, 800, 2500, 'High', 'AI', 1000, 1.3, 1.4, 1.35),
(19, 1800, 12600, 1000, 3000, 'High', 'Infrastructure', 1200, 1.4, 1.3, 1.35),
(20, 900, 6300, 400, 1500, 'Medium', 'Infrastructure', 700, 1.1, 1.2, 1.15);

-- 3. 投资行动计划 (Investment Action Plans)
INSERT INTO investment_action_plans (
    project_id, project_tier, composite_score, total_budget, budget_breakdown,
    start_date, target_duration, urgency, expected_roi, airdrop_estimate,
    action_steps, total_steps, monitoring_metrics, alert_conditions, risks, stop_loss_conditions
) VALUES
(1, 'S', 92, 5000, 
 '{"trading": 2000, "staking": 2000, "liquidity": 1000}',
 '立即开始', '长期持有 (12个月+)', 'Medium', '15-25%', 0,
 '{"steps": ["购买UNI", "参与流动性挖矿", "治理投票", "定期复投"]}', 4,
 '{"metrics": ["价格", "TVL", "交易量", "治理提案"]}',
 '{"alerts": ["价格跌破20%", "TVL下降30%"]}',
 '{"risks": ["监管风险", "竞争加剧", "市场波动"]}',
 '{"conditions": ["价格跌破30%", "基本面恶化"]}'),

(3, 'S', 88, 2000,
 '{"trading": 1000, "liquidity": 800, "reserve": 200}',
 '立即开始', '中期 (6-12个月)', 'High', '20-40%', 0,
 '{"steps": ["使用Jupiter交易", "提供流动性", "参与IDO", "积累积分"]}', 4,
 '{"metrics": ["交易量", "用户数", "生态项目数"]}',
 '{"alerts": ["Solana网络问题", "竞争对手崛起"]}',
 '{"risks": ["Solana依赖", "市场波动", "流动性风险"]}',
 '{"conditions": ["Solana重大问题", "竞品超越"]}'),

(12, 'A', 80, 300,
 '{"gas": 100, "staking": 150, "reserve": 50}',
 '立即开始', '短期 (3-6个月)', 'High', '300-600%', 1200,
 '{"steps": ["使用DA服务", "质押TIA", "参与测试网", "社区活动", "推荐用户"]}', 5,
 '{"metrics": ["DA使用量", "质押量", "社区活跃度"]}',
 '{"alerts": ["发币公告", "快照通知", "规则变更"]}',
 '{"risks": ["空投取消", "价值低于预期", "资格不符"]}',
 '{"conditions": ["官方否认空投", "项目停滞"]}'),

(13, 'B', 75, 1000,
 '{"liquidity": 700, "trading": 200, "reserve": 100}',
 '1周内', '中期 (6-9个月)', 'Medium', '50-100%', 750,
 '{"steps": ["提供流动性", "长期持有", "参与治理", "推荐用户"]}', 4,
 '{"metrics": ["TVL", "交易量", "用户数", "收益率"]}',
 '{"alerts": ["收益率大幅下降", "TVL流失"]}',
 '{"risks": ["流动性风险", "无常损失", "项目风险"]}',
 '{"conditions": ["收益率低于5%", "TVL下降50%"]}'),

(17, 'B', 76, 500,
 '{"hardware": 300, "gas": 100, "reserve": 100}',
 '设备就绪后', '中长期 (6-12个月)', 'Medium', '100-200%', 1500,
 '{"steps": ["配置GPU", "提供算力", "完成任务", "积累积分", "社区贡献"]}', 5,
 '{"metrics": ["算力贡献", "任务完成数", "积分累积"]}',
 '{"alerts": ["积分规则变更", "发币公告"]}',
 '{"risks": ["硬件成本", "电费成本", "空投不确定"]}',
 '{"conditions": ["ROI为负", "项目停滞"]}'),

(19, 'A', 81, 500,
 '{"bridge": 200, "gas": 200, "reserve": 100}',
 '立即开始', '短期 (3-6个月)', 'High', '200-500%', 1800,
 '{"steps": ["桥接资产", "部署合约", "使用DeFi", "增加交互", "参与测试"]}', 5,
 '{"metrics": ["交互次数", "资产规模", "合约数量"]}',
 '{"alerts": ["快照通知", "规则更新", "发币公告"]}',
 '{"risks": ["Gas费高", "技术门槛", "空投竞争"]}',
 '{"conditions": ["Gas费超预算", "官方否认空投"]}');

-- 4. 项目发现记录 (Project Discoveries)
INSERT INTO project_discoveries (
    project_name, total_mentions, platform_mentions, num_platforms, signal_strength,
    first_discovered_at, last_mentioned_at, heat_score, mentions_24h, mentions_7d,
    growth_rate, is_trending, is_surge, surge_ratio, has_token, mention_samples
) VALUES
('Uniswap', 1250, 
 '{"twitter": 450, "telegram": 380, "discord": 280, "reddit": 140}', 4, 95,
 NOW() - INTERVAL '30 days', NOW(), 92, 85, 580, 1.45, 1, 0, 1.2, 1,
 '{"samples": ["DEX龙头", "V4即将发布", "治理提案通过"]}'),

('Arbitrum', 980,
 '{"twitter": 380, "telegram": 320, "discord": 200, "reddit": 80}', 4, 88,
 NOW() - INTERVAL '25 days', NOW(), 89, 72, 490, 1.52, 1, 0, 1.3, 1,
 '{"samples": ["L2领先", "生态爆发", "TVL增长"]}'),

('Jupiter', 850,
 '{"twitter": 320, "telegram": 280, "discord": 180, "reddit": 70}', 4, 86,
 NOW() - INTERVAL '20 days', NOW(), 88, 68, 450, 1.48, 1, 0, 1.25, 1,
 '{"samples": ["Solana生态核心", "交易量第一", "用户体验好"]}'),

('Celestia', 520,
 '{"twitter": 180, "telegram": 150, "discord": 140, "reddit": 50}', 4, 78,
 NOW() - INTERVAL '15 days', NOW(), 80, 45, 320, 1.85, 1, 1, 2.1, 1,
 '{"samples": ["模块化创新", "DA需求增长", "技术领先"]}'),

('Pendle', 380,
 '{"twitter": 150, "telegram": 120, "discord": 80, "reddit": 30}', 4, 72,
 NOW() - INTERVAL '10 days', NOW(), 75, 32, 240, 1.65, 1, 0, 1.4, 1,
 '{"samples": ["利率衍生品", "收益优化", "TVL增长"]}'),

('Render', 420,
 '{"twitter": 160, "telegram": 130, "discord": 90, "reddit": 40}', 4, 75,
 NOW() - INTERVAL '12 days', NOW(), 76, 38, 280, 1.92, 1, 1, 2.3, 1,
 '{"samples": ["AI热点", "GPU需求", "合作伙伴多"]}'),

('StarkNet', 680,
 '{"twitter": 290, "telegram": 200, "discord": 140, "reddit": 50}', 4, 80,
 NOW() - INTERVAL '18 days', NOW(), 81, 58, 420, 1.72, 1, 0, 1.6, 1,
 '{"samples": ["ZK技术领先", "生态发展", "空投预期"]}'),

('Mantle', 340,
 '{"twitter": 170, "telegram": 100, "discord": 50, "reddit": 20}', 4, 73,
 NOW() - INTERVAL '8 days', NOW(), 74, 28, 210, 1.58, 1, 0, 1.35, 1,
 '{"samples": ["Bybit支持", "资金充足", "生态建设"]}');

-- 验证插入结果
SELECT '新表数据统计' as title;
SELECT 'Token Launch Predictions' as table_name, COUNT(*) as count FROM token_launch_predictions
UNION ALL
SELECT 'Airdrop Value Estimates', COUNT(*) FROM airdrop_value_estimates
UNION ALL
SELECT 'Investment Action Plans', COUNT(*) FROM investment_action_plans
UNION ALL
SELECT 'Project Discoveries', COUNT(*) FROM project_discoveries;
