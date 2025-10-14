/**
 * 项目相关类型定义
 */

export type ProjectGrade = 'S' | 'A' | 'B' | 'C'

export type ProjectCategory = 'DeFi' | 'NFT' | 'GameFi' | 'Infrastructure' | 'AI' | 'Social'

export interface Project {
  project_id: string
  name: string
  symbol?: string
  grade: ProjectGrade
  overall_score: number
  category?: ProjectCategory | null
  blockchain?: string | null
  description?: string
  logo_url?: string
  website?: string
  social_links: {
    twitter?: string
    telegram?: string
    discord?: string
    github?: string
  }
  key_highlights: string[]
  risk_flags: RiskFlag[]
  metrics: ProjectMetrics
  first_discovered_at: string
  last_updated_at: string
}

export interface RiskFlag {
  type: string
  severity: 'low' | 'medium' | 'high'
  message: string
}

export interface ProjectMetrics {
  market_cap?: number
  price_usd?: number
  volume_24h?: number
  tvl_usd?: number
  holder_count?: number
  twitter_followers?: number
  telegram_members?: number
  github_stars?: number
}

export interface ProjectScores {
  overall: number
  team: number
  technology: number
  community: number
  tokenomics: number
  market_timing: number
  risk: number
}

export interface ProjectDetail extends Project {
  contract_address?: string
  whitepaper_url?: string
  github_repo?: string
  source?: string
  scores: ProjectScores
  ai_analysis?: AIAnalysis
  discovery: {
    source: string
    discovered_at: string
    discovered_from?: string
  }
}

export interface AIAnalysis {
  summary: string
  key_features: string[]
  similar_projects: SimilarProject[]
  sentiment: {
    score: number
    label: string
  }
  risk_assessment: {
    flags: RiskFlag[]
    scam_probability: number
  }
  investment_suggestion: {
    action: string  // 后端返回的是action而不是recommendation
    position_size: string
    entry_timing: string
    stop_loss: number
  }
}

export interface SimilarProject {
  name: string
  similarity_score: number
  matching_features: string[]
}

