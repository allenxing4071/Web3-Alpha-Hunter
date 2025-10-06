/**
 * 项目详情页
 */

"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ProjectDetail, ProjectScores } from '@/types/project'
import { API_BASE_URL } from '@/lib/config'
import { GradeBadge } from '@/components/projects/GradeBadge'
import { RiskTag } from '@/components/projects/RiskTag'
import { ScoreRadar } from '@/components/projects/ScoreRadar'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

// Mock详情数据（仅作为API失败时的fallback）
const mockProjectDetail: ProjectDetail = {
  project_id: "proj_1",
  name: "XXX Protocol",
  symbol: "XXX",
  grade: "S",
  overall_score: 92,
  category: "DeFi",
  blockchain: "Ethereum",
  description: "革命性的跨链流动性聚合协议,通过创新的zkp技术实现即时跨链交换,Gas费用优化30-50%。",
  logo_url: undefined,
  website: "https://xxx-protocol.io",
  contract_address: "0x1234567890abcdef1234567890abcdef12345678",
  whitepaper_url: "https://xxx-protocol.io/whitepaper.pdf",
  github_repo: "https://github.com/xxx-protocol/core",
  social_links: {
    twitter: "xxx_protocol",
    telegram: "xxx_community",
    discord: "xxx_discord",
    github: "xxx-protocol",
  },
  key_highlights: [
    "a16z和Paradigm联合领投$50M A轮融资",
    "核心团队来自Uniswap、Aave和Curve",
    "已获得Certik、PeckShield、OpenZeppelin三家顶级审计机构审计",
    "主网上线3天TVL突破$5M,增长迅猛",
    "创新的zkp跨链技术,交易确认时间<1秒",
  ],
  risk_flags: [
    {
      type: "tokenomics",
      severity: "medium",
      message: "团队代币占比25%偏高,需关注锁仓条款"
    },
    {
      type: "transparency",
      severity: "low",
      message: "代币经济学未完全公开,等待完整披露"
    }
  ],
  metrics: {
    market_cap: 50000000,
    price_usd: 0.25,
    volume_24h: 2500000,
    tvl_usd: 5000000,
    holder_count: 8500,
    twitter_followers: 45000,
    telegram_members: 12000,
    github_stars: 320,
  },
  scores: {
    overall: 92,
    team: 95,
    technology: 90,
    community: 88,
    tokenomics: 85,
    market_timing: 80,
    risk: 90,
  },
  ai_analysis: {
    summary: "XXX Protocol是一个极具潜力的DeFi项目,技术团队背景优秀,融资实力雄厚,技术创新度高。项目采用zkp技术实现跨链流动性聚合,解决了当前DeFi领域的痛点问题。虽然存在一些代币经济学方面的不确定性,但整体风险可控,建议重点关注。",
    key_features: [
      "Multi-Chain Aggregation: 支持8条主流区块链的流动性聚合",
      "Smart Routing: AI驱动的最优路径算法,降低滑点",
      "Gas Optimization: 采用批量交易技术,节省30-50%交易成本",
      "zkp Technology: 零知识证明技术保证跨链安全性"
    ],
    similar_projects: [
      {
        name: "Solana",
        similarity_score: 0.85,
        matching_features: ["技术团队背景优秀", "早期社区增长迅猛", "投资机构质量顶级"]
      },
      {
        name: "Uniswap V3",
        similarity_score: 0.78,
        matching_features: ["AMM创新", "开发者活跃度高"]
      }
    ],
    sentiment: {
      score: 0.75,
      label: "positive"
    },
    risk_assessment: {
      scam_probability: 5.2,
      risk_level: "low"
    },
    investment_suggestion: {
      recommendation: "强烈推荐",
      position_size: "3-5%",
      entry_timing: "立即小仓位埋伏,等待主网正式上线前加仓",
      stop_loss: 30
    }
  },
  discovery: {
    source: "twitter",
    discovered_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    discovered_from: "@VitalikButerin 转发推荐"
  },
  first_discovered_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  last_updated_at: new Date().toISOString(),
}

export default function ProjectDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [project, setProject] = useState<ProjectDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [activeTab, setActiveTab] = useState<'overview' | 'analysis' | 'data'>('overview')

  // 加载项目数据
  const loadProjectData = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/projects/${params.id}`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch project')
      }
      
      const data = await response.json()
      
      // 转换后端数据格式
      const projectDetail: ProjectDetail = {
        project_id: data.project_id || String(data.id),
        name: data.project_name,
        symbol: data.symbol,
        grade: data.grade || '?',
        overall_score: data.overall_score || 0,
        category: data.category || 'Unknown',
        blockchain: data.blockchain || 'Unknown',
        description: data.description || '',
        logo_url: data.logo_url,
        website: data.website,
        contract_address: data.contract_address,
        whitepaper_url: data.whitepaper_url,
        github_repo: data.github_repo,
        social_links: {
          twitter: data.twitter_handle,
          telegram: data.telegram_channel,
          discord: data.discord_link,
          github: data.github_repo,
        },
        key_highlights: [],
        risk_flags: [],
        metrics: {},
        scores: {
          overall: data.overall_score || 0,
          team: data.team_score || 0,
          technology: data.tech_score || 0,
          community: data.community_score || 0,
          tokenomics: data.tokenomics_score || 0,
          market_timing: data.market_timing_score || 0,
          risk: data.risk_score || 0,
        },
        ai_analysis: {
          summary: '正在加载AI分析...',
          key_features: [],
          similar_projects: [],
          sentiment: { score: 0.5, label: 'neutral' },
          risk_assessment: {
            scam_probability: data.risk_score || 50,
            risk_level: 'medium'
          },
          investment_suggestion: {
            recommendation: '数据加载中',
            position_size: '-',
            entry_timing: '-',
            stop_loss: 30
          }
        },
        discovery: {
          source: data.discovered_from || 'unknown',
          discovered_at: data.first_discovered_at || data.created_at,
          discovered_from: data.discovered_from || '未知来源'
        },
        first_discovered_at: data.first_discovered_at || data.created_at,
        last_updated_at: data.last_updated_at || data.updated_at,
        source: data.discovered_from
      }
      
      setProject(projectDetail)
    } catch (error) {
      console.error('Failed to load project from API:', error)
      // API失败时使用Mock数据
      setProject(mockProjectDetail)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }
  
  useEffect(() => {
    loadProjectData()
  }, [params.id])
  
  // 刷新数据函数
  const handleRefresh = () => {
    setRefreshing(true)
    // 模拟数据刷新
    setTimeout(() => {
      loadProjectData()
      router.refresh()
    }, 800)
  }

  if (loading) {
    return (
      <div className="min-h-screen p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            <div className="h-32 bg-bg-tertiary rounded-lg"></div>
            <div className="h-96 bg-bg-tertiary rounded-lg"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="min-h-screen p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-2xl font-bold text-text-primary mb-2">项目未找到</h2>
          <button
            onClick={() => router.push('/projects')}
            className="mt-4 px-6 py-2 bg-accent-primary text-white rounded-lg hover:bg-accent-primary/80"
          >
            返回列表
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* 返回按钮 */}
        <button
          onClick={() => router.push('/projects')}
          className="mb-6 text-text-secondary hover:text-accent-primary transition-colors flex items-center gap-2"
        >
          ← 返回列表
        </button>

        {/* 项目头部 */}
        <Card className="mb-6 bg-bg-tertiary border-gray-700">
          <CardHeader>
            <div className="flex items-start justify-between gap-6">
              <div className="flex items-start gap-4 flex-1">
                {/* Logo */}
                <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-accent-primary to-accent-purple flex items-center justify-center text-white text-3xl font-bold">
                  {project.name?.[0] || '?'}
                </div>
                
                {/* 基本信息 */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h1 className="text-3xl font-bold text-text-primary">
                      {project.name}
                    </h1>
                    {project.symbol && (
                      <span className="px-3 py-1 bg-gray-700 text-text-secondary rounded-lg text-sm font-mono">
                        ${project.symbol}
                      </span>
                    )}
                  </div>
                  
                  <p className="text-text-secondary mb-3">
                    {project.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-blue-900/30 text-blue-300 text-sm rounded-md border border-blue-700/50">
                      💰 {project.category}
                    </span>
                    <span className="px-3 py-1 bg-purple-900/30 text-purple-300 text-sm rounded-md border border-purple-700/50">
                      ⛓️ {project.blockchain}
                    </span>
                    <span className="px-3 py-1 bg-gray-800 text-text-tertiary text-sm rounded-md">
                      🕐 发现于 {formatDistanceToNow(new Date(project.first_discovered_at), { 
                        addSuffix: true,
                        locale: zhCN 
                      })}
                    </span>
                  </div>
                </div>
              </div>
              
              {/* 评分徽章 */}
              <GradeBadge grade={project.grade} score={project.overall_score} size="lg" />
            </div>
          </CardHeader>
        </Card>

        {/* 标签页 */}
        <div className="mb-6 border-b border-gray-700">
          <div className="flex gap-6">
            {[
              { key: 'overview', label: '概览', icon: '📊' },
              { key: 'analysis', label: 'AI分析', icon: '🤖' },
              { key: 'data', label: '数据指标', icon: '📈' },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`px-4 py-3 font-medium transition-colors border-b-2 ${
                  activeTab === tab.key
                    ? 'border-accent-primary text-accent-primary'
                    : 'border-transparent text-text-secondary hover:text-text-primary'
                }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* 标签页内容 */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* 左侧 - 评分雷达图 */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>评分雷达图</CardTitle>
                </CardHeader>
                <CardContent>
                  <ScoreRadar scores={project.scores} />
                </CardContent>
              </Card>

              {/* 核心亮点 */}
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>✨ 核心亮点</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {project.key_highlights.map((highlight, idx) => (
                      <li key={idx} className="flex items-start gap-3">
                        <span className="text-accent-primary mt-1">•</span>
                        <span className="text-text-secondary">{highlight}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* 风险提示 */}
              {project.risk_flags.length > 0 && (
                <Card className="bg-bg-tertiary border-gray-700">
                  <CardHeader>
                    <CardTitle>⚠️ 风险提示</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {project.risk_flags.map((risk, idx) => (
                        <RiskTag key={idx} risk={risk} className="block" />
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* 右侧 - 快速链接和信息 */}
            <div className="space-y-6">
              {/* 快速链接 */}
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>🔗 快速链接</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {project.website && (
                    <a href={project.website} target="_blank" rel="noopener noreferrer"
                       className="block px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors">
                      🌐 官方网站
                    </a>
                  )}
                  {project.whitepaper_url && (
                    <a href={project.whitepaper_url} target="_blank" rel="noopener noreferrer"
                       className="block px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors">
                      📄 白皮书
                    </a>
                  )}
                  {project.github_repo && (
                    <a href={project.github_repo} target="_blank" rel="noopener noreferrer"
                       className="block px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors">
                      💻 GitHub
                    </a>
                  )}
                  {project.social_links.twitter && (
                    <a href={`https://twitter.com/${project.social_links.twitter}`} target="_blank" rel="noopener noreferrer"
                       className="block px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors">
                      🐦 Twitter
                    </a>
                  )}
                  {project.social_links.telegram && (
                    <a href={`https://t.me/${project.social_links.telegram}`} target="_blank" rel="noopener noreferrer"
                       className="block px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors">
                      📱 Telegram
                    </a>
                  )}
                </CardContent>
              </Card>

              {/* 数据来源 */}
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>📊 数据来源</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {/* CoinGecko */}
                  {project.source === 'coingecko_trending' && (
                    <a 
                      href={`https://www.coingecko.com/en/coins/${project.name.toLowerCase()}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors group"
                    >
                      <span className="text-sm">🦎 CoinGecko</span>
                      <span className="text-xs text-text-tertiary group-hover:text-accent-primary">查看详情 →</span>
                    </a>
                  )}
                  
                  {/* GitHub */}
                  {project.github_repo && (
                    <a 
                      href={project.github_repo}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors group"
                    >
                      <span className="text-sm">💻 GitHub</span>
                      <span className="text-xs text-text-tertiary group-hover:text-accent-primary">查看代码 →</span>
                    </a>
                  )}
                  
                  {/* DeFiLlama (for DeFi projects) */}
                  {project.category === 'DeFi' && (
                    <a 
                      href={`https://defillama.com/protocol/${project.name.toLowerCase()}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors group"
                    >
                      <span className="text-sm">🦙 DefiLlama</span>
                      <span className="text-xs text-text-tertiary group-hover:text-accent-primary">查看TVL →</span>
                    </a>
                  )}
                  
                  {/* Dune Analytics */}
                  <a 
                    href={`https://dune.com/search?q=${project.name}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg hover:border-accent-primary transition-colors group"
                  >
                    <span className="text-sm">🔮 Dune Analytics</span>
                    <span className="text-xs text-text-tertiary group-hover:text-accent-primary">链上数据 →</span>
                  </a>
                </CardContent>
              </Card>

              {/* 更新信息 */}
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>🔄 更新信息</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-text-tertiary">最后更新</span>
                    <span className="text-text-primary font-mono">
                      {formatDistanceToNow(new Date(project.last_updated_at), { 
                        addSuffix: true,
                        locale: zhCN 
                      })}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-tertiary">更新频率</span>
                    <span className="text-accent-primary">每24小时</span>
                  </div>
                  <div className="pt-2 border-t border-gray-700">
                    <button 
                      className="w-full px-4 py-2 bg-accent-primary/20 text-accent-primary rounded-lg hover:bg-accent-primary/30 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                      onClick={handleRefresh}
                      disabled={refreshing}
                    >
                      {refreshing ? '🔄 正在刷新...' : '🔄 立即刷新数据'}
                    </button>
                  </div>
                </CardContent>
              </Card>

              {/* 发现信息 */}
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle>📍 发现信息</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-text-tertiary">来源</span>
                    <span className="text-text-primary capitalize">{project.discovery.source}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-tertiary">发现于</span>
                    <span className="text-text-primary">
                      {formatDistanceToNow(new Date(project.discovery.discovered_at), { 
                        addSuffix: true,
                        locale: zhCN 
                      })}
                    </span>
                  </div>
                  {project.discovery.discovered_from && (
                    <div className="pt-2 border-t border-gray-700">
                      <span className="text-text-tertiary">发现来源</span>
                      <p className="text-text-primary mt-1">{project.discovery.discovered_from}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && project.ai_analysis && (
          <div className="space-y-6">
            {/* AI分析说明 */}
            <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <span className="text-2xl">🤖</span>
                <div className="flex-1">
                  <h3 className="text-blue-300 font-semibold mb-1">AI分析说明</h3>
                  <p className="text-sm text-blue-200/80">
                    以下分析由Claude/GPT-4生成,综合了来自<strong>CoinGecko、GitHub、DefiLlama、Dune Analytics</strong>等多个数据源的实时信息。
                    数据每24小时自动更新一次,最后更新于 {formatDistanceToNow(new Date(project.last_updated_at), { locale: zhCN, addSuffix: true })}。
                  </p>
                </div>
              </div>
            </div>
            
            {/* AI总结 */}
            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle>🤖 AI分析摘要</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-text-secondary leading-relaxed">
                  {project.ai_analysis.summary}
                </p>
              </CardContent>
            </Card>

            {/* 技术特点 */}
            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle>💡 技术创新点</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {project.ai_analysis.key_features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="text-accent-primary mt-1">•</span>
                      <span className="text-text-secondary">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* 相似项目 */}
            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle>🔄 相似项目对比</CardTitle>
              </CardHeader>
              <CardContent>
                {project.ai_analysis.similar_projects.map((similar, idx) => (
                  <div key={idx} className="mb-4 last:mb-0 pb-4 last:pb-0 border-b last:border-0 border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-text-primary">{similar.name}</span>
                      <span className="text-accent-primary">相似度: {(similar.similarity_score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {similar.matching_features.map((feature, fidx) => (
                        <span key={fidx} className="px-2 py-1 bg-blue-900/30 text-blue-300 text-xs rounded">
                          {feature}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* 投资建议 */}
            <Card className="bg-bg-tertiary border-accent-gold border-2 glow-gold">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>💡 AI投资建议</CardTitle>
                  <span className="text-xs text-yellow-500">⚠️ 仅供参考,非投资建议</span>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-text-tertiary text-sm">推荐度</span>
                    <p className="text-lg font-semibold text-accent-gold">
                      {project.ai_analysis.investment_suggestion.recommendation}
                    </p>
                  </div>
                  <div>
                    <span className="text-text-tertiary text-sm">建议仓位</span>
                    <p className="text-lg font-semibold text-accent-primary">
                      {project.ai_analysis.investment_suggestion.position_size}
                    </p>
                  </div>
                  <div>
                    <span className="text-text-tertiary text-sm">入场时机</span>
                    <p className="text-sm text-text-secondary">
                      {project.ai_analysis.investment_suggestion.entry_timing}
                    </p>
                  </div>
                  <div>
                    <span className="text-text-tertiary text-sm">止损线</span>
                    <p className="text-lg font-semibold text-danger">
                      -{project.ai_analysis.investment_suggestion.stop_loss}%
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'data' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* 市场数据 */}
            {project.metrics.market_cap && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">市值</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-accent-primary">
                    ${(project.metrics.market_cap / 1000000).toFixed(1)}M
                  </p>
                </CardContent>
              </Card>
            )}
            
            {project.metrics.tvl_usd && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">TVL</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-success">
                    ${(project.metrics.tvl_usd / 1000000).toFixed(1)}M
                  </p>
                </CardContent>
              </Card>
            )}
            
            {project.metrics.volume_24h && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">24h交易量</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-warning">
                    ${(project.metrics.volume_24h / 1000000).toFixed(1)}M
                  </p>
                </CardContent>
              </Card>
            )}
            
            {project.metrics.twitter_followers && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">Twitter粉丝</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-text-primary">
                    {(project.metrics.twitter_followers / 1000).toFixed(1)}k
                  </p>
                </CardContent>
              </Card>
            )}
            
            {project.metrics.telegram_members && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">Telegram成员</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-text-primary">
                    {(project.metrics.telegram_members / 1000).toFixed(1)}k
                  </p>
                </CardContent>
              </Card>
            )}
            
            {project.metrics.github_stars && (
              <Card className="bg-bg-tertiary border-gray-700">
                <CardHeader>
                  <CardTitle className="text-sm text-text-tertiary">GitHub Stars</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-2xl font-bold text-text-primary">
                    ⭐ {project.metrics.github_stars}
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

