"""测试AI分析器"""

from app.services.analyzers.ai_analyzer import ai_analyzer
from app.services.analyzers.risk_detector import risk_detector

# 测试项目1: 优质项目
print("=" * 80)
print("测试1: 优质DeFi项目")
print("=" * 80)

good_project = {
    "text": """Excited to announce our new cross-chain DeFi protocol! 
    
    ✅ Audited by Certik and PeckShield
    ✅ Team from Uniswap and Aave
    ✅ Backed by a16z and Paradigm ($50M Series A)
    ✅ Fair launch, no presale
    ✅ Liquidity locked for 2 years
    
    Revolutionary zkp technology for instant cross-chain swaps.
    Mainnet launching next month! #DeFi #Web3
    """,
    "source": "twitter",
    "author": {
        "username": "VitalikButerin",
        "followers": 5000000,
        "verified": True,
    },
    "engagement": {
        "likes": 15000,
        "retweets": 3500,
        "replies": 800,
    },
    "contracts": ["0x1234567890abcdef1234567890abcdef12345678"],
}

result1 = ai_analyzer.analyze_full_project(good_project)
risks1 = risk_detector.detect_risks(good_project)

print(f"\n✅ 综合评分: {result1['overall_score']:.1f}/100")
print(f"✅ 等级: {result1['grade']}")
print(f"\n各维度评分:")
for dim, score in result1['scores'].items():
    print(f"  - {dim}: {score:.1f}")
print(f"\n风险数量: {len(risks1)}")
for risk in risks1:
    print(f"  - [{risk['severity']}] {risk['message']}")

# 测试项目2: 可疑项目
print("\n" + "=" * 80)
print("测试2: 可疑骗局项目")
print("=" * 80)

scam_project = {
    "text": """🚀 NEW 100X GUARANTEED TOKEN! 🚀
    
    💰 Guaranteed returns! No risk!
    💰 First 100 get 3x bonus!
    💰 Anonymous team for your privacy
    💰 Send 1 ETH, get 3 ETH back!
    
    Join now before it's too late! #crypto #100x
    """,
    "source": "telegram",
    "author": {
        "username": "CryptoGem123",
        "followers": 500,
        "verified": False,
    },
    "engagement": {
        "likes": 50,
        "retweets": 10,
        "replies": 5,
    },
}

result2 = ai_analyzer.analyze_full_project(scam_project)
risks2 = risk_detector.detect_risks(scam_project)
scam_prob = risk_detector.calculate_scam_probability(risks2)

print(f"\n⚠️ 综合评分: {result2['overall_score']:.1f}/100")
print(f"⚠️ 等级: {result2['grade']}")
print(f"\n各维度评分:")
for dim, score in result2['scores'].items():
    print(f"  - {dim}: {score:.1f}")
print(f"\n🚨 骗局概率: {scam_prob:.1f}%")
print(f"🚨 风险数量: {len(risks2)}")
for risk in risks2:
    print(f"  - [{risk['severity']}] {risk['message']}")

# 测试项目3: 中等项目
print("\n" + "=" * 80)
print("测试3: 中等GameFi项目")
print("=" * 80)

medium_project = {
    "text": """New GameFi project launching next week!
    
    Play-to-earn mechanics
    NFT marketplace integrated
    Team has gaming industry experience
    Testnet now live
    
    Join our community! #GameFi #NFT
    """,
    "source": "twitter",
    "author": {
        "username": "GameFiStudio",
        "followers": 25000,
        "verified": False,
    },
    "engagement": {
        "likes": 800,
        "retweets": 200,
        "replies": 45,
    },
}

result3 = ai_analyzer.analyze_full_project(medium_project)
risks3 = risk_detector.detect_risks(medium_project)

print(f"\n📊 综合评分: {result3['overall_score']:.1f}/100")
print(f"📊 等级: {result3['grade']}")
print(f"\n各维度评分:")
for dim, score in result3['scores'].items():
    print(f"  - {dim}: {score:.1f}")
print(f"\n风险数量: {len(risks3)}")

print("\n" + "=" * 80)
print("测试完成!")
print("=" * 80)

