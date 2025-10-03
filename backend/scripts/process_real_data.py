"""
处理真实采集的数据,转换为系统可用格式并进行AI分析
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from app.services.analyzers.scorer import ProjectScorer
from app.services.analyzers.ai_analyzer import AIAnalyzer
from app.services.analyzers.risk_detector import RiskDetector


def load_real_data():
    """加载真实采集的数据"""
    with open('backend/real_web3_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_coingecko_to_project(coin_data: dict) -> dict:
    """将CoinGecko数据转换为项目格式"""
    return {
        'project_id': f"cg_{coin_data['symbol'].lower()}",
        'name': coin_data['name'],
        'symbol': coin_data['symbol'],
        'category': 'DeFi',  # 默认分类
        'blockchain': 'Ethereum',  # 默认链
        'description': f"{coin_data['name']} is a cryptocurrency currently ranked #{coin_data.get('market_cap_rank', 'N/A')} by market cap.",
        'logo_url': coin_data.get('thumb'),
        'metrics': {
            'market_cap_rank': coin_data.get('market_cap_rank'),
            'price_btc': coin_data.get('price_btc'),
        },
        'source': coin_data['source'],
        'discovered_at': datetime.now().isoformat(),
    }


def convert_github_to_project(repo_data: dict) -> dict:
    """将GitHub仓库转换为项目格式"""
    # 根据topic判断分类
    category_map = {
        'defi': 'DeFi',
        'nft': 'NFT',
        'blockchain': 'Infrastructure',
        'web3': 'Infrastructure',
        'crypto': 'DeFi',
    }
    category = category_map.get(repo_data.get('topic', '').lower(), 'Infrastructure')
    
    return {
        'project_id': f"gh_{repo_data['full_name'].replace('/', '_')}",
        'name': repo_data['name'],
        'symbol': None,
        'category': category,
        'blockchain': 'Multi-Chain',
        'description': repo_data.get('description', ''),
        'website': repo_data.get('url'),
        'github_repo': repo_data.get('url'),
        'metrics': {
            'github_stars': repo_data.get('stars', 0),
            'programming_language': repo_data.get('language'),
        },
        'source': repo_data['source'],
        'discovered_at': datetime.now().isoformat(),
    }


def analyze_project(project_data: dict) -> dict:
    """使用AI分析器分析项目"""
    print(f"\n🤖 正在分析项目: {project_data['name']}")
    
    # 1. 风险检测
    risk_detector = RiskDetector()
    risk_result = risk_detector.detect_all_risks(project_data)
    
    # 2. 评分
    scorer = ProjectScorer()
    
    # 构建评分所需的数据
    project_info = {
        'name': project_data.get('name'),
        'description': project_data.get('description', ''),
        'github_stars': project_data.get('metrics', {}).get('github_stars', 0),
        'twitter_followers': project_data.get('metrics', {}).get('twitter_followers', 0),
        'telegram_members': project_data.get('metrics', {}).get('telegram_members', 0),
        'market_cap_rank': project_data.get('metrics', {}).get('market_cap_rank', 999),
    }
    
    scores = scorer.calculate_scores(project_info)
    grade = scorer.get_grade(scores['overall'])
    
    # 3. 合并结果
    result = {
        **project_data,
        'grade': grade,
        'overall_score': scores['overall'],
        'scores': scores,
        'risk_assessment': risk_result,
        'analyzed_at': datetime.now().isoformat(),
    }
    
    print(f"  评分: {scores['overall']}/100")
    print(f"  等级: {grade}")
    print(f"  风险等级: {risk_result['risk_level']}")
    
    return result


def main():
    """主函数"""
    print("="*80)
    print("🚀 Web3 Alpha Hunter - 真实数据处理与分析")
    print("="*80)
    
    # 1. 加载真实数据
    print("\n📥 加载真实采集数据...")
    real_data = load_real_data()
    
    print(f"  - CoinGecko热门: {len(real_data['coingecko_trending'])} 个")
    print(f"  - CoinGecko新币: {len(real_data['coingecko_new'])} 个")
    print(f"  - GitHub项目: {len(real_data['github_trending'])} 个")
    
    # 2. 转换数据格式
    print("\n🔄 转换数据格式...")
    all_projects = []
    
    # 转换CoinGecko热门币
    for coin in real_data['coingecko_trending'][:5]:  # 只取前5个
        project = convert_coingecko_to_project(coin)
        all_projects.append(project)
    
    # 转换GitHub项目
    for repo in real_data['github_trending'][:5]:  # 只取前5个
        project = convert_github_to_project(repo)
        all_projects.append(project)
    
    print(f"✅ 共转换 {len(all_projects)} 个项目")
    
    # 3. AI分析每个项目
    print("\n🤖 开始AI分析...")
    analyzed_projects = []
    
    for i, project in enumerate(all_projects, 1):
        print(f"\n[{i}/{len(all_projects)}] ", end='')
        try:
            analyzed = analyze_project(project)
            analyzed_projects.append(analyzed)
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            continue
    
    # 4. 按评分排序
    analyzed_projects.sort(key=lambda x: x['overall_score'], reverse=True)
    
    # 5. 保存结果
    output_file = 'backend/analyzed_projects.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_projects, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 分析结果已保存到: {output_file}")
    
    # 6. 输出报告
    print("\n" + "="*80)
    print("📊 分析结果摘要")
    print("="*80)
    
    # 统计各等级项目数量
    grade_stats = {}
    for project in analyzed_projects:
        grade = project['grade']
        grade_stats[grade] = grade_stats.get(grade, 0) + 1
    
    print(f"\n🏆 项目分级统计:")
    for grade in ['S', 'A', 'B', 'C']:
        count = grade_stats.get(grade, 0)
        print(f"  {grade}级: {count} 个")
    
    # 展示TOP 5项目
    print(f"\n⭐ TOP 5 高评分项目:")
    for i, project in enumerate(analyzed_projects[:5], 1):
        risk_level = project['risk_assessment']['risk_level']
        risk_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(risk_level, '⚪')
        
        print(f"\n  {i}. {project['name']} ({project['category']})")
        print(f"     评分: {project['overall_score']}/100 | 等级: {project['grade']} | 风险: {risk_emoji} {risk_level}")
        if project.get('description'):
            desc = project['description'][:80] + '...' if len(project['description']) > 80 else project['description']
            print(f"     简介: {desc}")
    
    # 高风险项目警告
    high_risk_projects = [p for p in analyzed_projects if p['risk_assessment']['risk_level'] == 'high']
    if high_risk_projects:
        print(f"\n⚠️  高风险项目警告 ({len(high_risk_projects)}个):")
        for project in high_risk_projects:
            scam_prob = project['risk_assessment']['scam_probability']
            print(f"  - {project['name']}: 骗局概率 {scam_prob:.1f}%")
    
    print("\n" + "="*80)
    print("✅ 分析完成!")
    print("="*80)
    
    return analyzed_projects


if __name__ == "__main__":
    projects = main()

