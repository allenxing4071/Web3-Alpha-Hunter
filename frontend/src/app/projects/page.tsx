/**
 * 项目列表页面 (带筛选功能)
 */

"use client"

import { useState, useEffect, useMemo } from "react"
import { ProjectList } from "@/components/projects/ProjectList"
import { ProjectFilter, FilterOptions } from "@/components/projects/ProjectFilter"
import { Project } from "@/types/project"
import { API_BASE_URL } from "@/lib/config"

// 不再使用硬编码数据，改为从API获取
// const realProjects = getRealProjects()

// Mock数据(仅在API失败时使用)
const mockProjects: Project[] = [
  {
    project_id: "proj_1",
    name: "XXX Protocol",
    symbol: "XXX",
    grade: "S",
    overall_score: 92,
    category: "DeFi",
    blockchain: "Ethereum",
    description: "革命性的跨链流动性聚合协议,通过创新的AMM算法实现低滑点交易。",
    logo_url: null,
    website: "https://xxx-protocol.io",
    social_links: {
      twitter: "xxx_protocol",
      telegram: "xxx_community",
    },
    key_highlights: [
      "a16z领投 $50M A轮融资",
      "团队来自Uniswap核心开发",
      "已获得Certik、PeckShield、OpenZeppelin三家审计"
    ],
    risk_flags: [
      {
        type: "tokenomics",
        severity: "medium",
        message: "团队代币占比25%偏高"
      }
    ],
    metrics: {
      twitter_followers: 45000,
      telegram_members: 12000,
      tvl_usd: 5000000,
      github_stars: 320
    },
    first_discovered_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    last_updated_at: new Date().toISOString(),
  },
  {
    project_id: "proj_2",
    name: "NextGen Finance",
    symbol: "NGF",
    grade: "A",
    overall_score: 78,
    category: "DeFi",
    blockchain: "Solana",
    description: "下一代去中心化借贷协议,支持多种资产抵押。",
    logo_url: null,
    website: null,
    social_links: {
      twitter: "nextgen_fi",
    },
    key_highlights: [
      "Binance Labs投资",
      "主网上线3天TVL突破$2M",
      "独特的动态利率模型"
    ],
    risk_flags: [],
    metrics: {
      twitter_followers: 8500,
      tvl_usd: 2000000,
    },
    first_discovered_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    last_updated_at: new Date().toISOString(),
  },
  {
    project_id: "proj_3",
    name: "MetaVerse Gaming",
    symbol: "MVG",
    grade: "B",
    overall_score: 65,
    category: "GameFi",
    blockchain: "Polygon",
    description: "Web3游戏平台,提供Play-to-Earn和NFT市场。",
    logo_url: null,
    website: null,
    social_links: {},
    key_highlights: [
      "团队有游戏行业经验",
      "测试网现已上线",
      "NFT市场集成"
    ],
    risk_flags: [
      {
        type: "no_audit",
        severity: "medium",
        message: "未发现审计信息"
      }
    ],
    metrics: {
      twitter_followers: 2500,
    },
    first_discovered_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    last_updated_at: new Date().toISOString(),
  },
  {
    project_id: "proj_4",
    name: "AI Data Network",
    symbol: "ADN",
    grade: "A",
    overall_score: 82,
    category: "AI",
    blockchain: "Ethereum",
    description: "去中心化AI数据网络,为AI模型提供高质量训练数据。",
    logo_url: null,
    website: null,
    social_links: {
      twitter: "ai_data_network",
    },
    key_highlights: [
      "AI赛道热门项目",
      "已获种子轮融资",
      "测试网用户破万"
    ],
    risk_flags: [],
    metrics: {
      twitter_followers: 15000,
    },
    first_discovered_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    last_updated_at: new Date().toISOString(),
  },
]

export default function ProjectsPage() {
  const [allProjects, setAllProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<FilterOptions>({
    grade: 'all',
    category: 'all',
    blockchain: 'all',
    minScore: 0,
    sortBy: 'score',
    order: 'desc',
  })
  
  useEffect(() => {
    // 从后端API加载真实数据
    const fetchProjects = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${API_BASE_URL}/projects?limit=100`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch projects')
        }
        
        const data = await response.json()
        
        // API返回格式: { success: true, data: { projects: [...] } }
        const projectsData = data.data?.projects || data.projects || []
        
        // 转换后端数据格式为前端Project类型
        const projects: Project[] = projectsData.map((p: any) => ({
          project_id: String(p.id),
          name: p.project_name,
          symbol: p.symbol,
          grade: p.grade || '?',
          overall_score: p.overall_score || 0,
          category: p.category || 'Unknown',
          blockchain: p.blockchain || 'Unknown',
          description: p.description || '',
          logo_url: p.logo_url,
          website: p.website,
          social_links: {
            twitter: p.twitter_handle,
            telegram: p.telegram_channel,
            github: p.github_repo,
          },
          key_highlights: [], // 后续可从AI分析获取
          risk_flags: [],
          metrics: {},
          first_discovered_at: p.first_discovered_at || p.created_at,
          last_updated_at: p.last_updated_at || p.updated_at,
        }))
        
        setAllProjects(projects)
      } catch (error) {
        console.error('Failed to load projects from API:', error)
        // API失败时使用Mock数据作为fallback
        setAllProjects(mockProjects)
      } finally {
        setLoading(false)
      }
    }
    
    fetchProjects()
  }, [])
  
  // 筛选和排序项目
  const filteredProjects = useMemo(() => {
    let filtered = [...allProjects]
    
    // 按等级筛选
    if (filters.grade !== 'all') {
      filtered = filtered.filter(p => p.grade === filters.grade)
    }
    
    // 按分类筛选
    if (filters.category !== 'all') {
      filtered = filtered.filter(p => p.category === filters.category)
    }
    
    // 按区块链筛选
    if (filters.blockchain !== 'all') {
      filtered = filtered.filter(p => p.blockchain === filters.blockchain)
    }
    
    // 按最低评分筛选
    filtered = filtered.filter(p => p.overall_score >= filters.minScore)
    
    // 排序
    filtered.sort((a, b) => {
      let compareValue = 0
      
      if (filters.sortBy === 'score') {
        compareValue = a.overall_score - b.overall_score
      } else if (filters.sortBy === 'discovered_at') {
        compareValue = new Date(a.first_discovered_at).getTime() - new Date(b.first_discovered_at).getTime()
      }
      
      return filters.order === 'desc' ? -compareValue : compareValue
    })
    
    return filtered
  }, [allProjects, filters])
  
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            项目列表
          </h1>
          <p className="text-text-secondary">
            AI发现的优质Web3项目 · 共 {filteredProjects.length} 个结果
          </p>
        </div>
        
        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-4">
            <div className="text-text-tertiary text-sm mb-1">总项目</div>
            <div className="text-2xl font-bold text-text-primary">
              {allProjects.length}
            </div>
          </div>
          <div className="bg-bg-tertiary border border-accent-gold rounded-lg p-4 glow-gold">
            <div className="text-text-tertiary text-sm mb-1">S级项目</div>
            <div className="text-2xl font-bold text-accent-gold">
              {allProjects.filter(p => p.grade === 'S').length}
            </div>
          </div>
          <div className="bg-bg-tertiary border border-accent-purple rounded-lg p-4">
            <div className="text-text-tertiary text-sm mb-1">A级项目</div>
            <div className="text-2xl font-bold text-accent-purple">
              {allProjects.filter(p => p.grade === 'A').length}
            </div>
          </div>
          <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-4">
            <div className="text-text-tertiary text-sm mb-1">今日新增</div>
            <div className="text-2xl font-bold text-success">
              {allProjects.filter(p => {
                const discovered = new Date(p.first_discovered_at)
                const today = new Date()
                return discovered.toDateString() === today.toDateString()
              }).length}
            </div>
          </div>
        </div>
        
        {/* 筛选器 + 项目列表 */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* 筛选器 (左侧) */}
          <div className="lg:col-span-1">
            <ProjectFilter 
              filters={filters}
              onFilterChange={setFilters}
            />
          </div>
          
          {/* 项目列表 (右侧) */}
          <div className="lg:col-span-3">
            <ProjectList projects={filteredProjects} loading={loading} />
          </div>
        </div>
      </div>
    </div>
  )
}
