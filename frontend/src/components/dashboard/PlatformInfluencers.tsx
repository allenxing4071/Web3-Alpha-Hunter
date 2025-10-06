/**
 * 平台大V推荐组件
 * 展示各个Web3平台的知名KOL和推荐关注账号
 */

'use client'

import { ExternalLink, Users } from 'lucide-react'

interface Influencer {
  id: string
  name: string
  platform: string
  platformIcon: string
  handle: string
  url: string
  followers: string
  category: string
  description: string
  verified?: boolean
}

const influencers: Influencer[] = [
  {
    id: '1',
    name: 'Vitalik Buterin',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@VitalikButerin',
    url: 'https://twitter.com/VitalikButerin',
    followers: '5.2M',
    category: 'Ethereum',
    description: '以太坊创始人，区块链技术先驱',
    verified: true
  },
  {
    id: '2',
    name: 'CZ (Binance)',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@cz_binance',
    url: 'https://twitter.com/cz_binance',
    followers: '8.7M',
    category: 'CEX/DeFi',
    description: 'Binance创始人，加密货币领袖',
    verified: true
  },
  {
    id: '3',
    name: 'Messari',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@messaricrypto',
    url: 'https://twitter.com/messaricrypto',
    followers: '589K',
    category: 'Research',
    description: '加密研究机构，深度行业分析',
    verified: true
  },
  {
    id: '4',
    name: 'DeFi Llama',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@DefiLlama',
    url: 'https://twitter.com/DefiLlama',
    followers: '342K',
    category: 'DeFi',
    description: 'DeFi数据聚合平台，TVL追踪专家',
    verified: true
  },
  {
    id: '5',
    name: 'The Block',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@TheBlock__',
    url: 'https://twitter.com/TheBlock__',
    followers: '823K',
    category: 'News',
    description: '加密新闻媒体，实时行业动态',
    verified: true
  },
  {
    id: '6',
    name: 'Bankless',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@BanklessHQ',
    url: 'https://twitter.com/BanklessHQ',
    followers: '614K',
    category: 'Education',
    description: 'Web3教育平台，DeFi深度内容',
    verified: true
  },
  {
    id: '7',
    name: 'Dune Analytics',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@DuneAnalytics',
    url: 'https://twitter.com/DuneAnalytics',
    followers: '287K',
    category: 'Analytics',
    description: '链上数据分析，可视化工具',
    verified: true
  },
  {
    id: '8',
    name: 'Coingecko',
    platform: 'Twitter',
    platformIcon: '𝕏',
    handle: '@coingecko',
    url: 'https://twitter.com/coingecko',
    followers: '1.2M',
    category: 'Data',
    description: '加密货币数据平台，市场追踪',
    verified: true
  }
]

function InfluencerCard({ influencer }: { influencer: Influencer }) {
  const handleClick = () => {
    window.open(influencer.url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div 
      onClick={handleClick}
      className="flex-shrink-0 w-80 p-5 rounded-xl border-2 border-gray-700 bg-bg-tertiary
                 hover:border-accent-primary hover:scale-105 transition-all cursor-pointer group"
    >
      {/* 头部：平台和验证标识 */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{influencer.platformIcon}</span>
          <span className="text-sm text-text-secondary">{influencer.platform}</span>
        </div>
        {influencer.verified && (
          <div className="flex items-center gap-1 text-accent-primary">
            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>
            <span className="text-xs">已验证</span>
          </div>
        )}
      </div>

      {/* 主要信息 */}
      <div className="mb-3">
        <h4 className="font-bold text-lg text-text-primary mb-1 group-hover:text-accent-primary transition-colors">
          {influencer.name}
        </h4>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-accent-primary font-mono text-sm">{influencer.handle}</span>
          <ExternalLink className="w-3 h-3 text-text-tertiary" />
        </div>
        <p className="text-sm text-text-secondary line-clamp-2">
          {influencer.description}
        </p>
      </div>

      {/* 底部：分类和粉丝数 */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-700">
        <span className="px-3 py-1 bg-bg-primary rounded-full text-xs text-text-secondary">
          {influencer.category}
        </span>
        <div className="flex items-center gap-1 text-text-tertiary text-sm">
          <Users className="w-4 h-4" />
          <span>{influencer.followers}</span>
        </div>
      </div>
    </div>
  )
}

export function PlatformInfluencers() {
  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 mt-6">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
        <Users className="w-5 h-5 mr-2 text-accent-purple" />
        推荐关注
        <span className="ml-2 text-sm text-text-secondary font-normal">
          (Web3 影响力大V)
        </span>
        <span className="ml-auto text-sm text-text-tertiary">
          点击卡片访问主页
        </span>
      </h3>

      <div className="overflow-x-auto pb-2 scrollbar-thin">
        <div className="flex gap-4">
          {influencers.map((influencer) => (
            <InfluencerCard key={influencer.id} influencer={influencer} />
          ))}
        </div>
      </div>
    </div>
  )
}

