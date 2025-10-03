"""
独立的分析器 - 不依赖配置文件,直接分析真实数据
"""

import json
import re
from datetime import datetime
from typing import Dict, List


class StandaloneScorer:
    """独立评分器"""
    
    def calculate_scores(self, project: Dict) -> Dict:
        """计算6维度评分"""
        
        # 1. 团队背景 (20%)
        team_score = 50  # 默认50分
        if project.get('metrics', {}).get('github_stars', 0) > 10000:
            team_score += 30
        elif project.get('metrics', {}).get('github_stars', 0) > 1000:
            team_score += 20
        
        # 2. 技术创新 (25%)
        tech_score = 60
        if 'defi' in project.get('description', '').lower():
            tech_score += 20
        if project.get('metrics', {}).get('github_stars', 0) > 5000:
            tech_score += 15
        
        # 3. 社区热度 (20%)
        community_score = 40
        stars = project.get('metrics', {}).get('github_stars', 0)
        if stars > 20000:
            community_score += 40
        elif stars > 10000:
            community_score += 30
        elif stars > 1000:
            community_score += 20
        
        # 4. 代币模型 (15%)
        tokenomics_score = 50
        if project.get('symbol'):
            tokenomics_score += 20
        market_cap_rank = project.get('metrics', {}).get('market_cap_rank', 9999)
        if market_cap_rank < 100:
            tokenomics_score += 25
        elif market_cap_rank < 500:
            tokenomics_score += 15
        
        # 5. 市场时机 (10%)
        market_timing = 65
        if 'new' in project.get('source', ''):
            market_timing += 20
        
        # 6. 风险控制 (10%)
        risk_score = 70
        
        # 综合评分
        overall = (
            team_score * 0.20 +
            tech_score * 0.25 +
            community_score * 0.20 +
            tokenomics_score * 0.15 +
            market_timing * 0.10 +
            risk_score * 0.10
        )
        
        return {
            'overall': round(overall, 2),
            'team': team_score,
            'technology': tech_score,
            'community': community_score,
            'tokenomics': tokenomics_score,
            'market_timing': market_timing,
            'risk': risk_score,
        }
    
    def get_grade(self, score: float) -> str:
        """获取评级"""
        if score >= 85:
            return 'S'
        elif score >= 70:
            return 'A'
        elif score >= 55:
            return 'B'
        else:
            return 'C'


class StandaloneRiskDetector:
    """独立风险检测器"""
    
    HIGH_RISK_KEYWORDS = [
        'scam', 'ponzi', 'rug', 'rugpull', 'fake', 'fraud',
        '100x guaranteed', 'no risk', 'easy money'
    ]
    
    def detect_risks(self, project: Dict) -> Dict:
        """检测风险"""
        description = project.get('description', '').lower()
        name = project.get('name', '').lower()
        
        scam_probability = 0.0
        risk_flags = []
        
        # 检测高风险关键词
        for keyword in self.HIGH_RISK_KEYWORDS:
            if keyword in description or keyword in name:
                scam_probability += 20.0
                risk_flags.append(f"包含高风险关键词: {keyword}")
        
        # 检测缺少审计
        if 'audit' not in description:
            scam_probability += 10.0
        
        # 检测GitHub活跃度
        stars = project.get('metrics', {}).get('github_stars', 0)
        if stars == 0:
            scam_probability += 15.0
        
        # 确定风险等级
        if scam_probability > 50:
            risk_level = 'high'
        elif scam_probability > 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'scam_probability': min(scam_probability, 100.0),
            'risk_level': risk_level,
            'risk_flags': risk_flags,
        }


def load_real_data():
    """加载真实数据"""
    with open('backend/real_web3_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_coingecko_to_project(coin: dict) -> dict:
    """转换CoinGecko数据"""
    return {
        'project_id': f"cg_{coin['symbol'].lower()}",
        'name': coin['name'],
        'symbol': coin['symbol'],
        'category': 'DeFi',
        'blockchain': 'Ethereum',
        'description': f"{coin['name']} is a cryptocurrency currently ranked #{coin.get('market_cap_rank', 'N/A')} by market cap.",
        'logo_url': coin.get('thumb'),
        'metrics': {
            'market_cap_rank': coin.get('market_cap_rank'),
            'price_btc': coin.get('price_btc'),
        },
        'source': coin['source'],
    }


def convert_github_to_project(repo: dict) -> dict:
    """转换GitHub数据"""
    category_map = {
        'defi': 'DeFi',
        'nft': 'NFT',
        'blockchain': 'Infrastructure',
        'web3': 'Infrastructure',
        'crypto': 'DeFi',
    }
    category = category_map.get(repo.get('topic', '').lower(), 'Infrastructure')
    
    return {
        'project_id': f"gh_{repo['full_name'].replace('/', '_')}",
        'name': repo['name'],
        'symbol': None,
        'category': category,
        'blockchain': 'Multi-Chain',
        'description': repo.get('description', ''),
        'website': repo.get('url'),
        'github_repo': repo.get('url'),
        'metrics': {
            'github_stars': repo.get('stars', 0),
            'programming_language': repo.get('language'),
        },
        'source': repo['source'],
    }


def main():
    """主函数"""
    print("="*80)
    print("🚀 Web3 Alpha Hunter - 真实数据深度分析")
    print("="*80)
    
    # 加载数据
    print("\n📥 加载真实采集数据...")
    data = load_real_data()
    
    # 转换数据
    print("\n🔄 转换数据格式...")
    projects = []
    
    # CoinGecko TOP 5
    for coin in data['coingecko_trending'][:5]:
        projects.append(convert_coingecko_to_project(coin))
    
    # GitHub TOP 5
    for repo in data['github_trending'][:5]:
        projects.append(convert_github_to_project(repo))
    
    print(f"✅ 共 {len(projects)} 个项目待分析")
    
    # 初始化分析器
    scorer = StandaloneScorer()
    risk_detector = StandaloneRiskDetector()
    
    # 分析每个项目
    print("\n🤖 开始AI分析...\n")
    analyzed = []
    
    for i, project in enumerate(projects, 1):
        print(f"[{i}/{len(projects)}] 分析: {project['name']}")
        
        # 评分
        scores = scorer.calculate_scores(project)
        grade = scorer.get_grade(scores['overall'])
        
        # 风险检测
        risks = risk_detector.detect_risks(project)
        
        # 合并结果
        result = {
            **project,
            'grade': grade,
            'overall_score': scores['overall'],
            'scores': scores,
            'risk_assessment': risks,
            'analyzed_at': datetime.now().isoformat(),
        }
        
        analyzed.append(result)
        
        # 打印结果
        risk_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}[risks['risk_level']]
        print(f"  ✅ 评分: {scores['overall']}/100 | 等级: {grade} | 风险: {risk_emoji} {risks['risk_level']}")
    
    # 排序
    analyzed.sort(key=lambda x: x['overall_score'], reverse=True)
    
    # 保存结果
    output = 'backend/analyzed_projects.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(analyzed, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存到: {output}")
    
    # 输出报告
    print("\n" + "="*80)
    print("📊 分析结果报告")
    print("="*80)
    
    # 统计
    grade_stats = {}
    for p in analyzed:
        g = p['grade']
        grade_stats[g] = grade_stats.get(g, 0) + 1
    
    print(f"\n🏆 评级分布:")
    for grade in ['S', 'A', 'B', 'C']:
        count = grade_stats.get(grade, 0)
        bar = '█' * count
        print(f"  {grade}级: {count:2d} {bar}")
    
    # TOP 5
    print(f"\n⭐ TOP 5 最高评分项目:\n")
    for i, p in enumerate(analyzed[:5], 1):
        risk_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}[p['risk_assessment']['risk_level']]
        grade_emoji = {'S': '👑', 'A': '⭐', 'B': '📊', 'C': '⚠️'}[p['grade']]
        
        print(f"{i}. {grade_emoji} {p['name']} ({p['category']})")
        print(f"   评分: {p['overall_score']}/100 | 等级: {p['grade']} | 风险: {risk_emoji} {p['risk_assessment']['risk_level']}")
        print(f"   来源: {p['source']}")
        if p.get('description'):
            desc = p['description'][:100] + '...' if len(p['description']) > 100 else p['description']
            print(f"   简介: {desc}")
        print()
    
    # 高风险警告
    high_risk = [p for p in analyzed if p['risk_assessment']['risk_level'] == 'high']
    if high_risk:
        print(f"⚠️  高风险项目警告 ({len(high_risk)}个):")
        for p in high_risk:
            print(f"  🔴 {p['name']}: {p['risk_assessment']['scam_probability']:.1f}% 骗局概率")
    
    print("\n" + "="*80)
    print("✅ 分析完成!")
    print("="*80)
    
    return analyzed


if __name__ == "__main__":
    results = main()

