"""完整工作流演示"""

from app.services.project_discovery import project_discovery_service
from app.services.scoring_engine import scoring_engine
from app.services.action_plan_generator import action_plan_generator
from datetime import datetime

print('🚀 Web3 Alpha Hunter - 完整工作流演示')
print('=' * 80)

# 1. 模拟多平台数据采集
print('\n📥 步骤1: 多平台数据采集')
print('-' * 80)

mock_data = {
    'twitter': [
        {
            'text': 'Excited about ZkFlow Protocol! Revolutionary Layer2 solution with zkRollup technology. Team from Google and Ethereum Foundation. #Web3 #Layer2',
            'created_at': datetime(2025, 1, 1),
            'author': 'crypto_expert'
        },
        {
            'text': 'BREAKING: ZkFlow Protocol raised $30M from Paradigm and a16z. Testnet launching next week. This will be huge! 🚀',
            'created_at': datetime(2025, 1, 1),
            'author': 'vc_insider'
        },
        {
            'text': 'Just deployed my first transaction on ZkFlow testnet. Gas fees are incredibly low! No token yet but probably airdrop coming.',
            'created_at': datetime(2025, 1, 1),
            'author': 'defi_degen'
        },
        {
            'text': 'ZkFlow Protocol documentation is impressive. They solved the data availability problem elegantly. Contract: 0x1234567890123456789012345678901234567890',
            'created_at': datetime(2025, 1, 1),
            'author': 'blockchain_dev'
        },
    ],
    'telegram': [
        {
            'content': 'Alpha leak: ZkFlow snapshot might happen in 2-3 months according to insider. Start using testnet NOW!',
            'date': datetime(2025, 1, 1)
        },
        {
            'content': 'ZkFlow team just announced tokenomics will be revealed in Q2. Airdrop allocation for early users confirmed.',
            'date': datetime(2025, 1, 1)
        },
    ],
    'medium': [
        {
            'text': 'Technical Deep Dive: How ZkFlow Protocol Achieves 10,000 TPS - An analysis of the ZkFlow architecture and its innovative approach to Layer2 scaling.',
            'created_at': datetime(2025, 1, 1)
        },
    ]
}

print(f'   ✓ Twitter: {len(mock_data["twitter"])} 条推文')
print(f'   ✓ Telegram: {len(mock_data["telegram"])} 条消息') 
print(f'   ✓ Medium: {len(mock_data["medium"])} 篇文章')

# 2. 项目发现与聚合
print('\n🔍 步骤2: 项目发现与聚合')
print('-' * 80)

discovered_projects = project_discovery_service.aggregate_multi_source_data(mock_data)
print(f'   ✓ 发现 {len(discovered_projects)} 个唯一项目')

# 显示top 3
for i, project in enumerate(discovered_projects[:3], 1):
    print(f'   {i}. {project["project_name"]}')
    print(f'      - 提及次数: {project["total_mentions"]}')
    print(f'      - 覆盖平台: {project["num_platforms"]}')
    print(f'      - 信号强度: {project["signal_strength"]}/100')

# 3. 选择最热门项目进行深度分析
if discovered_projects:
    print('\n🤖 步骤3: AI深度分析')
    print('-' * 80)
    
    top_project = discovered_projects[0]
    project_name = top_project["project_name"]
    
    # 模拟补充项目详细数据（实际会从各个API获取）
    top_project.update({
        'category': 'Layer2',
        'blockchain': 'Ethereum',
        
        # 团队信息
        'team_info': {
            'members': [
                {'from_faang': True, 'web3_success': True, 'top_education': True},
                {'from_faang': True, 'web3_success': False},
                {'from_faang': False, 'web3_success': True},
            ],
            'roles': ['CEO', 'CTO', 'CMO'],
            'social_reach': 25000,
            'transparency_score': 0.75
        },
        
        # GitHub数据
        'github': {
            'commits_30d': 95,
            'contributors': 6,
            'stars': 1800
        },
        
        # 社交媒体数据
        'twitter': {
            'followers': 12000,
            'engagement_rate': 0.045
        },
        'telegram': {
            'members': 6500,
            'daily_messages': 350
        },
        'discord': {
            'activity_score': 70
        },
        
        # 增长数据
        'growth_data': {
            'twitter_growth_30d': 0.12,
            'telegram_growth_30d': 0.10
        },
        
        # 技术与安全
        'docs_quality': 0.8,
        'innovation_score': 0.85,
        'audit_status': {
            'has_audit': True,
            'top_auditor': True
        },
        
        # 融资与背书
        'funding_amount': 30000000,
        'has_top_tier_vc': True,
        'competitors': ['Arbitrum', 'Optimism'],
        'competitor_count': 2,
        
        # 风险因素
        'team_anonymous': False,
        'token_concentration': 0.25,
        'bot_suspicion': 0.1,
        'domain_age_days': 120,
        
        # 代币相关
        'snapshot_announced': False,
        'tokenomics_published': False,
        'points_system_live': True,
        'audit_completed': True,
        'mainnet_live': True,
        'roadmap_mentions_token': True,
    })
    
    print(f'   分析项目: {project_name}')
    
    # 3.1 六维度评分
    print(f'\n   📊 六维度评分:')
    score = scoring_engine.calculate_comprehensive_score(top_project)
    
    print(f'      团队背景: {score.team_score}/100')
    print(f'      技术创新: {score.tech_score}/100')
    print(f'      社区热度: {score.community_score}/100')
    print(f'      代币经济: {score.tokenomics_score}/100')
    print(f'      市场时机: {score.market_score}/100')
    print(f'      风险评估: {score.risk_score}/100')
    print(f'      ─────────────────────')
    print(f'      综合评分: {score.composite_score}/100')
    print(f'      项目分级: {score.grade}')
    print(f'      投资建议: {score.recommendation}')
    
    # 3.2 发币概率预测
    print(f'\n   🎯 发币概率预测:')
    launch_prob = scoring_engine.predict_token_launch_probability(top_project)
    
    print(f'      发币概率: {launch_prob["launch_probability"]}%')
    print(f'      置信度: {launch_prob["confidence"]}')
    print(f'      预估时间: {launch_prob["estimated_timeline"]}')
    print(f'      检测到的信号:')
    for signal in launch_prob['detected_signals']:
        print(f'        ✓ {signal}')
    
    # 3.3 空投价值估算
    print(f'\n   💰 空投价值估算:')
    top_project['tvl'] = 120000000  # 添加TVL数据
    airdrop_value = scoring_engine.estimate_airdrop_value(top_project)
    
    print(f'      预估价值: ${airdrop_value["estimated_value_usd"]} USD')
    print(f'      价值区间: ${airdrop_value["value_range_usd"]["min"]} - ${airdrop_value["value_range_usd"]["max"]} USD')
    print(f'      折合人民币: ¥{airdrop_value["estimated_value_usd"] * 6.5:.0f}')
    print(f'      置信度: {airdrop_value["confidence"]}')
    
    # 4. 生成投资行动指南（仅S/A级）
    if score.grade in ['S', 'A']:
        print(f'\n📋 步骤4: 生成投资行动指南')
        print('-' * 80)
        
        action_plan = action_plan_generator.generate_action_plan(
            project=top_project,
            score=score.dict(),
            launch_prob=launch_prob,
            airdrop_value=airdrop_value
        )
        
        print(f'   项目: {action_plan.project_name}')
        print(f'   分级: {action_plan.project_tier}')
        print(f'   评分: {action_plan.composite_score}/100')
        
        print(f'\n   💰 预算分配:')
        print(f'      总预算: ¥{action_plan.total_budget}')
        for item, detail in action_plan.budget_breakdown.items():
            print(f'      - {item}: ¥{detail["金额"]} ({detail["说明"]})')
        
        print(f'\n   ⏰ 时间规划:')
        print(f'      开始日期: {action_plan.start_date}')
        print(f'      预估周期: {action_plan.target_duration}')
        print(f'      紧迫性: {action_plan.urgency}')
        
        print(f'\n   🎯 预期收益:')
        print(f'      预期ROI: {action_plan.expected_roi}')
        print(f'      预估空投: ${action_plan.airdrop_estimate}')
        
        print(f'\n   📝 行动步骤 (共{len(action_plan.action_steps)}步):')
        for step in action_plan.action_steps:
            print(f'      {step.step_number}. [{step.priority.upper()}] {step.action}')
            print(f'         截止: {step.deadline} | 预算: {step.cost_estimate}')
        
        print(f'\n   📊 监控指标 (共{len(action_plan.monitoring_metrics)}个):')
        for metric in action_plan.monitoring_metrics[:5]:
            print(f'      • {metric}')
        if len(action_plan.monitoring_metrics) > 5:
            print(f'      ... 还有 {len(action_plan.monitoring_metrics) - 5} 个')
        
        print(f'\n   ⚠️  风险提示 (共{len(action_plan.risks)}个):')
        for risk in action_plan.risks:
            print(f'      {risk}')
        
        print(f'\n   🛑 止损条件 (共{len(action_plan.stop_loss_conditions)}个):')
        for condition in action_plan.stop_loss_conditions[:3]:
            print(f'      {condition}')
        if len(action_plan.stop_loss_conditions) > 3:
            print(f'      ... 还有 {len(action_plan.stop_loss_conditions) - 3} 个')

print('\n' + '=' * 80)
print('✅ 完整工作流演示完成！')
print('=' * 80)
print('\n🎉 从数据采集 → 项目发现 → AI评分 → 投资指南 全流程运行成功！')
print('   系统已准备就绪，可以开始实际运行。')
print('\n💡 下一步:')
print('   1. 配置真实的Twitter/Telegram API密钥')
print('   2. 启动Celery定时任务')
print('   3. 部署Discord Bot')
print('   4. 设置实时推送通知')

