-- 插入Web3知名KOL数据

INSERT INTO kols (
    username,
    display_name,
    platform,
    profile_url,
    followers,
    tier,
    influence_score,
    tags,
    bio,
    verified,
    status,
    avatar_url,
    created_at,
    updated_at
) VALUES
-- Tier 1: 顶级KOL (100万+粉丝)
('VitalikButerin', 'Vitalik Buterin', 'twitter', 'https://twitter.com/VitalikButerin', 5200000, 1, 98.5, 'Ethereum,Founder,Tech', 'Ethereum co-founder', true, 'active', 'https://pbs.twimg.com/profile_images/1/vitalik.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('cz_binance', 'CZ Binance', 'twitter', 'https://twitter.com/cz_binance', 8500000, 1, 97.8, 'Binance,Exchange,CEO', 'Founder & CEO of Binance', true, 'active', 'https://pbs.twimg.com/profile_images/1/cz.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('elonmusk', 'Elon Musk', 'twitter', 'https://twitter.com/elonmusk', 170000000, 1, 99.9, 'Crypto,Doge,Tech', 'Technoking of Tesla, occasional crypto influencer', true, 'active', 'https://pbs.twimg.com/profile_images/1/elon.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('justinsuntron', 'Justin Sun', 'twitter', 'https://twitter.com/justinsuntron', 3400000, 1, 92.3, 'Tron,Founder', 'Founder of TRON', true, 'active', 'https://pbs.twimg.com/profile_images/1/justin.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('brian_armstrong', 'Brian Armstrong', 'twitter', 'https://twitter.com/brian_armstrong', 1200000, 1, 94.2, 'Coinbase,CEO', 'CEO & Co-Founder of Coinbase', true, 'active', 'https://pbs.twimg.com/profile_images/1/brian.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Tier 2: 高影响力KOL (10万-100万粉丝)
('cmsholdings', 'CMS Holdings', 'twitter', 'https://twitter.com/cmsholdings', 450000, 2, 88.7, 'Trading,Investment,DeFi', 'Crypto trading firm & investor', true, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DCinvestor', 'DCinvestor', 'twitter', 'https://twitter.com/DCinvestor', 280000, 2, 87.5, 'Ethereum,DeFi,Analysis', 'Ethereum advocate & analyst', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('santimentfeed', 'Santiment', 'twitter', 'https://twitter.com/santimentfeed', 180000, 2, 85.3, 'Analytics,Data,Research', 'Crypto market intelligence platform', true, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('TheCryptoDog', 'The Crypto Dog', 'twitter', 'https://twitter.com/TheCryptoDog', 520000, 2, 84.2, 'Trading,Memes,Market', 'Crypto trader & meme lord', true, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('AltcoinGordon', 'Altcoin Gordon', 'twitter', 'https://twitter.com/AltcoinGordon', 380000, 2, 82.8, 'Altcoins,Trading', 'Altcoin trader & analyst', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('CryptoWendyO', 'Crypto Wendy O', 'twitter', 'https://twitter.com/CryptoWendyO', 420000, 2, 86.4, 'Education,Community', 'Crypto educator & community builder', true, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('sassal0x', 'Sassal', 'twitter', 'https://twitter.com/sassal0x', 220000, 2, 83.9, 'Ethereum,Research,Education', 'Ethereum researcher & educator', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DefiIgnas', 'DeFi Ignas', 'twitter', 'https://twitter.com/DefiIgnas', 180000, 2, 85.6, 'DeFi,Research,Alpha', 'DeFi researcher sharing alpha', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Tier 3: 成长中的KOL (1万-10万粉丝)
('web3_analyst', 'Web3 Analyst', 'twitter', 'https://twitter.com/web3_analyst', 45000, 3, 75.2, 'Analysis,Web3', 'Web3 project analyst', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('nftwhale', 'NFT Whale', 'twitter', 'https://twitter.com/nftwhale', 68000, 3, 76.8, 'NFT,Collector', 'NFT collector & investor', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('defi_hunter', 'DeFi Hunter', 'twitter', 'https://twitter.com/defi_hunter', 52000, 3, 74.5, 'DeFi,Yield,Farming', 'DeFi yield hunter', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('solana_daily', 'Solana Daily', 'twitter', 'https://twitter.com/solana_daily', 38000, 3, 73.2, 'Solana,News,Updates', 'Daily Solana ecosystem updates', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('layer2_updates', 'Layer2 Updates', 'twitter', 'https://twitter.com/layer2_updates', 42000, 3, 72.9, 'Layer2,Scaling,Tech', 'Layer 2 solutions tracker', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('airdrop_alpha', 'Airdrop Alpha', 'twitter', 'https://twitter.com/airdrop_alpha', 95000, 3, 78.3, 'Airdrops,Alpha,Farming', 'Airdrop opportunities & strategies', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('crypto_gem_finder', 'Crypto Gem Finder', 'twitter', 'https://twitter.com/crypto_gem_finder', 58000, 3, 71.5, 'Gems,Early,Projects', 'Finding early-stage crypto projects', false, 'active', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 验证插入结果
SELECT '✅ KOL数据导入完成!' AS status;
SELECT tier, COUNT(*) as count FROM kols GROUP BY tier ORDER BY tier;
SELECT platform, COUNT(*) as count FROM kols GROUP BY platform;

