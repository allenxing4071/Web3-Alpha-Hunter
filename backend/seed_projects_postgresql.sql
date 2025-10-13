-- 插入真实Web3项目测试数据到PostgreSQL

INSERT INTO projects (
    project_name, 
    category, 
    description, 
    overall_score, 
    grade,
    blockchain,
    status,
    first_discovered_at,
    last_updated_at,
    created_at, 
    updated_at
) VALUES
('Uniswap', 'DeFi', '去中心化交易协议,AMM龙头', 92.5, 'S', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Arbitrum', 'Infrastructure', '以太坊L2扩容方案,Optimistic Rollup', 89.3, 'S', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '9 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Jupiter', 'DeFi', 'Solana生态最大DEX聚合器', 88.7, 'A', 'Solana', 'published', CURRENT_TIMESTAMP - INTERVAL '8 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Wormhole', 'Infrastructure', '跨链通信协议,连接各大公链', 81.2, 'A', 'Multi-chain', 'published', CURRENT_TIMESTAMP - INTERVAL '7 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Jito', 'DeFi', 'Solana流动性质押协议,MEV优化', 78.9, 'B', 'Solana', 'published', CURRENT_TIMESTAMP - INTERVAL '6 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Optimism', 'Infrastructure', '以太坊L2,Optimistic Rollup方案', 85.6, 'A', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Polygon', 'Infrastructure', '以太坊侧链,多链扩容方案', 83.4, 'A', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '4 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Lido', 'DeFi', '流动性质押协议,stETH发行方', 87.2, 'A', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Aave', 'DeFi', '去中心化借贷协议龙头', 86.8, 'A', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Sui', 'Infrastructure', 'Move语言新公链,高性能L1', 79.5, 'B', 'Sui', 'analyzing', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Aptos', 'Infrastructure', 'Move语言新公链,前Meta团队', 77.3, 'B', 'Aptos', 'analyzing', CURRENT_TIMESTAMP - INTERVAL '12 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Celestia', 'Infrastructure', '模块化区块链,数据可用性层', 80.1, 'B', 'Celestia', 'published', CURRENT_TIMESTAMP - INTERVAL '10 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Pendle', 'DeFi', '利率衍生品协议,yield trading', 75.8, 'B', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '8 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Blur', 'NFT', 'NFT交易聚合平台,专业交易工具', 72.4, 'B', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '6 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('dYdX', 'DeFi', '去中心化衍生品交易所', 84.2, 'A', 'dYdX Chain', 'published', CURRENT_TIMESTAMP - INTERVAL '5 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('GMX', 'DeFi', '去中心化永续合约交易所', 82.7, 'A', 'Arbitrum', 'published', CURRENT_TIMESTAMP - INTERVAL '4 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Render', 'AI', '去中心化GPU渲染网络', 76.9, 'B', 'Solana', 'published', CURRENT_TIMESTAMP - INTERVAL '3 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Immutable X', 'NFT', 'NFT专用L2,零Gas费', 78.5, 'B', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('StarkNet', 'Infrastructure', 'ZK-Rollup L2,Cairo语言', 81.8, 'A', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '1 hour', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Mantle', 'Infrastructure', '模块化L2,Bybit投资', 74.6, 'B', 'Ethereum', 'published', CURRENT_TIMESTAMP - INTERVAL '30 minutes', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 完成提示
SELECT '✅ 项目数据导入完成!' AS status;
SELECT COUNT(*) AS total_projects FROM projects;
SELECT grade, COUNT(*) AS count FROM projects GROUP BY grade ORDER BY grade;
SELECT category, COUNT(*) AS count FROM projects GROUP BY category ORDER BY count DESC;


