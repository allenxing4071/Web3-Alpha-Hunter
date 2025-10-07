#!/usr/bin/env python3
"""
为现有项目生成AI分析数据
使用模板生成合理的AI分析结果
"""

import sys
import os
from pathlib import Path
import random
from datetime import datetime
from decimal import Decimal

# 添加项目路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.project import Project, AIAnalysis

# AI分析模板
ANALYSIS_TEMPLATES = {
    "DeFi": {
        "whitepaper_summary": "该项目提出了创新的去中心化金融解决方案，通过智能合约实现自动化的流动性管理和收益优化。核心技术采用先进的AMM算法，能够有效降低无常损失，同时提供更好的资金利用率。",
        "key_features": [
            "创新的流动性挖矿机制",
            "多链部署支持",
            "低Gas费优化",
            "安全审计通过",
            "DAO治理机制"
        ],
        "investment_suggestion": "该项目在DeFi赛道具有明显的技术优势，团队背景优秀，产品已上线并获得市场验证。建议关注其TVL增长情况和社区活跃度。短期内可能受市场波动影响，适合中长期持有。",
    },
    "Layer2": {
        "whitepaper_summary": "该Layer2解决方案采用先进的零知识证明技术，能够大幅提升以太坊网络的交易吞吐量，同时保持与主网相同的安全性。通过创新的状态压缩技术，实现了超低的交易成本。",
        "key_features": [
            "ZK-Rollup技术",
            "EVM兼容性",
            "秒级确认时间",
            "极低交易费用",
            "去中心化排序器"
        ],
        "investment_suggestion": "Layer2是以太坊扩容的重要方向，该项目技术实力雄厚，已获得顶级机构投资。随着以太坊生态的持续增长，Layer2解决方案将迎来爆发期。建议重点关注其生态项目发展和TVL增长。",
    },
    "AI": {
        "whitepaper_summary": "该项目构建了去中心化的AI训练和推理网络，通过区块链技术实现AI模型的透明化和可验证性。创新的激励机制吸引全球算力贡献者，打造开放的AI基础设施。",
        "key_features": [
            "去中心化AI训练",
            "可验证的推理结果",
            "激励机制完善",
            "多模型支持",
            "数据隐私保护"
        ],
        "investment_suggestion": "AI+Crypto是新兴热门赛道，该项目结合了两个高增长领域。技术路线清晰，团队有AI和区块链双重背景。建议关注其生态合作和实际应用落地情况。",
    },
    "GameFi": {
        "whitepaper_summary": "该GameFi项目采用创新的Play-to-Earn模式，结合高品质游戏体验和可持续的经济模型。通过NFT实现游戏资产的真正所有权，玩家可以通过游戏获得真实收益。",
        "key_features": [
            "AAA级游戏画质",
            "可持续经济模型",
            "NFT资产所有权",
            "多平台支持",
            "公会系统完善"
        ],
        "investment_suggestion": "GameFi市场竞争激烈，但该项目在游戏性和经济模型上都有创新。团队有游戏开发经验，已发布可玩版本。建议关注其DAU增长和代币流通情况，注意防范经济模型崩盘风险。",
    },
    "NFT": {
        "whitepaper_summary": "该NFT项目不仅仅是数字收藏品，而是构建了完整的数字身份和社交系统。持有者可以获得独特的权益和社区准入资格，NFT成为Web3时代的数字身份证明。",
        "key_features": [
            "独特艺术风格",
            "社区权益绑定",
            "元宇宙集成",
            "IP运营计划",
            "持续空投奖励"
        ],
        "investment_suggestion": "NFT市场波动较大，该项目在社区运营和IP打造上有独特优势。建议关注其社区活跃度和二级市场表现。适合对NFT文化有认同感的投资者参与。",
    },
}

def get_sentiment(overall_score: float) -> tuple:
    """根据综合评分返回情感分析结果"""
    if overall_score >= 85:
        return (0.8, "positive")
    elif overall_score >= 70:
        return (0.5, "neutral")
    elif overall_score >= 50:
        return (0.2, "neutral")
    else:
        return (-0.3, "negative")

def get_position_size(grade: str, overall_score: float) -> str:
    """根据等级和评分推荐仓位大小"""
    if grade == 'S' and overall_score >= 90:
        return "5-10%"
    elif grade in ['S', 'A'] and overall_score >= 80:
        return "3-5%"
    elif grade in ['A', 'B'] and overall_score >= 70:
        return "1-3%"
    else:
        return "<1%"

def get_entry_timing(grade: str) -> str:
    """根据等级推荐入场时机"""
    timings = {
        'S': "立即关注，分批建仓",
        'A': "等待回调，逢低布局",
        'B': "观察为主，小额试探",
        'C': "谨慎观望，等待更多信息",
        'D': "建议避免，风险较高"
    }
    return timings.get(grade, "谨慎观望")

def generate_risk_flags(grade: str, overall_score: float) -> list:
    """根据等级和评分生成风险标志"""
    risk_flags = []
    
    if overall_score < 60:
        risk_flags.append({
            "type": "low_score",
            "severity": "high",
            "message": "综合评分较低，存在较大风险"
        })
    
    if grade in ['C', 'D']:
        risk_flags.append({
            "type": "low_grade",
            "severity": "medium",
            "message": "项目评级较低，建议谨慎投资"
        })
    
    # 随机添加一些通用风险
    common_risks = [
        {"type": "market_volatility", "severity": "medium", "message": "加密市场波动较大，注意风险控制"},
        {"type": "smart_contract", "severity": "low", "message": "智能合约风险，建议关注审计报告"},
        {"type": "regulatory", "severity": "low", "message": "注意监管政策变化"},
    ]
    
    # 根据评分随机选择1-2个风险
    num_risks = 1 if overall_score >= 80 else 2
    risk_flags.extend(random.sample(common_risks, num_risks))
    
    return risk_flags

def generate_ai_analysis(db: Session):
    """为所有项目生成AI分析"""
    
    # 查询所有还没有AI分析的项目
    projects = db.query(Project).all()
    
    print(f"找到 {len(projects)} 个项目\n")
    
    generated_count = 0
    skipped_count = 0
    
    for project in projects:
        # 检查是否已有AI分析
        existing = db.query(AIAnalysis).filter(
            AIAnalysis.project_id == project.id
        ).first()
        
        if existing:
            print(f"⏭️  跳过 {project.project_name} (ID: {project.id}) - 已有AI分析")
            skipped_count += 1
            continue
        
        print(f"🤖 生成 {project.project_name} (ID: {project.id}) 的AI分析...")
        
        # 获取项目类别对应的模板
        category = project.category or "DeFi"
        template = ANALYSIS_TEMPLATES.get(category, ANALYSIS_TEMPLATES["DeFi"])
        
        # 计算情感分析
        overall_score = float(project.overall_score or 70)
        sentiment_score, sentiment_label = get_sentiment(overall_score)
        
        # 创建AI分析
        ai_analysis = AIAnalysis(
            project_id=project.id,
            whitepaper_summary=template["whitepaper_summary"],
            key_features=template["key_features"],
            similar_projects=None,  # 可以后续完善
            sentiment_score=Decimal(str(sentiment_score)),
            sentiment_label=sentiment_label,
            risk_flags=generate_risk_flags(project.grade or 'B', overall_score),
            scam_probability=Decimal(str(max(0, 100 - overall_score))),
            investment_suggestion=template["investment_suggestion"],
            position_size=get_position_size(project.grade or 'B', overall_score),
            entry_timing=get_entry_timing(project.grade or 'B'),
            stop_loss_percentage=Decimal("15.00"),  # 默认15%止损
            analyzed_at=datetime.now()
        )
        
        db.add(ai_analysis)
        generated_count += 1
        
        print(f"  ✅ 情感: {sentiment_label}, 建议仓位: {ai_analysis.position_size}")
        print()
    
    # 提交所有更改
    try:
        db.commit()
        print("=" * 60)
        print(f"✅ AI分析生成完成！")
        print(f"   新生成: {generated_count} 个")
        print(f"   已跳过: {skipped_count} 个")
        print("=" * 60)
    except Exception as e:
        db.rollback()
        print(f"❌ 保存失败: {e}")
        raise

def main():
    """主函数"""
    print("=" * 60)
    print("AI分析生成工具")
    print("=" * 60)
    print()
    
    db = next(get_db())
    try:
        generate_ai_analysis(db)
        print("\n提示: 重启前端页面查看AI分析结果")
    finally:
        db.close()

if __name__ == "__main__":
    main()
