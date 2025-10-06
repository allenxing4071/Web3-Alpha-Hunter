/**
 * 平台大V推荐组件
 * 展示各个Web3平台的知名KOL和推荐关注账号
 */

'use client'

import { ExternalLink, Users, ChevronLeft, ChevronRight } from 'lucide-react'
import { useRef, useState, useEffect, useCallback } from 'react'
import { API_BASE_URL } from '@/lib/config'

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
  tier?: number
  influenceScore?: number
}

function InfluencerCard({ influencer }: { influencer: Influencer }) {
  const handleClick = () => {
    window.open(influencer.url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div 
      onClick={handleClick}
      className="flex-shrink-0 w-80 p-6 rounded-xl border-2 border-gray-700 bg-bg-tertiary
                 hover:border-accent-primary transition-colors cursor-pointer group my-2"
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
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const [scrollPosition, setScrollPosition] = useState(0)
  const [influencers, setInfluencers] = useState<Influencer[]>([])
  const [loading, setLoading] = useState(true)

  // 使用useCallback确保handleScroll函数稳定
  const handleScroll = useCallback(() => {
    if (scrollContainerRef.current) {
      setScrollPosition(scrollContainerRef.current.scrollLeft)
    }
  }, [])

  // 从API加载KOL数据
  useEffect(() => {
    const loadInfluencers = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${API_BASE_URL}/kols/top-influencers?limit=15&tier=1`)
        const data = await response.json()
        
        if (data.success && data.influencers) {
          setInfluencers(data.influencers)
        }
      } catch (error) {
        console.error('加载KOL数据失败:', error)
        // 如果加载失败，使用默认数据
        setInfluencers([])
      } finally {
        setLoading(false)
      }
    }

    loadInfluencers()
  }, [])

  // 初始化时触发一次滚动位置计算，确保3D效果正确显示
  useEffect(() => {
    if (!loading && influencers.length > 0 && scrollContainerRef.current) {
      // 多次触发确保效果生效
      handleScroll()
      
      const timer1 = setTimeout(() => handleScroll(), 50)
      const timer2 = setTimeout(() => handleScroll(), 150)
      const timer3 = setTimeout(() => handleScroll(), 300)
      
      return () => {
        clearTimeout(timer1)
        clearTimeout(timer2)
        clearTimeout(timer3)
      }
    }
  }, [loading, influencers, handleScroll])

  // 监听窗口大小变化，重新计算
  useEffect(() => {
    const handleResize = () => {
      handleScroll()
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [handleScroll])

  const scroll = (direction: 'left' | 'right') => {
    if (scrollContainerRef.current) {
      const scrollAmount = 400 // 滚动距离
      const newScrollLeft = scrollContainerRef.current.scrollLeft + (direction === 'left' ? -scrollAmount : scrollAmount)
      scrollContainerRef.current.scrollTo({
        left: newScrollLeft,
        behavior: 'smooth'
      })
    }
  }

  // 计算卡片的样式（缩放和透明度）
  const getCardStyle = useCallback((index: number) => {
    if (!scrollContainerRef.current) {
      // 返回默认样式，确保至少有基础样式
      return {
        transform: 'scale(1)',
        opacity: 1,
        transition: 'all 0.3s ease-out'
      }
    }
    
    const container = scrollContainerRef.current
    const cardWidth = 320 + 16 // 卡片宽度 320px + gap 16px
    const containerWidth = container.clientWidth
    const padding = 64 // px-16 = 64px padding
    const scrollLeft = scrollPosition
    
    // 计算卡片左边缘位置（考虑padding）
    const cardLeft = padding + index * cardWidth
    // 计算卡片中心位置
    const cardCenter = cardLeft + 160 - scrollLeft
    // 可视区域中心
    const viewportCenter = containerWidth / 2
    // 卡片中心到可视区域中心的距离
    const distanceFromCenter = Math.abs(cardCenter - viewportCenter)
    
    // 计算缩放比例（中间1.0，两边0.85）
    const maxDistance = containerWidth / 2
    const normalizedDistance = Math.min(distanceFromCenter / maxDistance, 1)
    const scale = 1 - (normalizedDistance * 0.15)  // 1.0 → 0.85
    
    // 计算透明度（中间1.0，两边0.5）
    const opacity = 1 - (normalizedDistance * 0.5)  // 1.0 → 0.5
    
    return {
      transform: `scale(${scale})`,
      opacity: opacity,
      transition: 'all 0.3s ease-out'
    }
  }, [scrollPosition])

  // 加载状态
  if (loading) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 mt-6">
        <h3 className="text-xl font-bold text-text-primary mb-6 flex items-center">
          <Users className="w-5 h-5 mr-2 text-accent-purple" />
          推荐关注
          <span className="ml-2 text-sm text-text-secondary font-normal">
            (Web3 影响力大V)
          </span>
        </h3>
        <div className="flex gap-4 overflow-hidden">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex-shrink-0 w-80 h-48 bg-bg-tertiary/50 rounded-xl animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 mt-6">
      <h3 className="text-xl font-bold text-text-primary mb-6 flex items-center">
        <Users className="w-5 h-5 mr-2 text-accent-purple" />
        推荐关注
        <span className="ml-2 text-sm text-text-secondary font-normal">
          (Web3 影响力大V)
        </span>
        <span className="ml-auto text-sm text-text-tertiary">
          点击卡片访问主页 · 共 {influencers.length} 位
        </span>
      </h3>

      <div className="relative">
        {/* 左箭头 - 始终显示 */}
        <button
          onClick={() => scroll('left')}
          className="absolute left-0 top-1/2 -translate-y-1/2 z-10 
                   bg-accent-primary/90 hover:bg-accent-primary
                   text-white rounded-full p-3 shadow-lg
                   transition-all hover:scale-110"
          aria-label="向左滚动"
        >
          <ChevronLeft className="w-6 h-6 stroke-[3]" />
        </button>

        {/* 右箭头 - 始终显示 */}
        <button
          onClick={() => scroll('right')}
          className="absolute right-0 top-1/2 -translate-y-1/2 z-10
                   bg-accent-primary/90 hover:bg-accent-primary
                   text-white rounded-full p-3 shadow-lg
                   transition-all hover:scale-110"
          aria-label="向右滚动"
        >
          <ChevronRight className="w-6 h-6 stroke-[3]" />
        </button>

        {/* 左侧渐变遮罩 */}
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-bg-secondary to-transparent pointer-events-none z-[5]" />
        
        {/* 右侧渐变遮罩 */}
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-bg-secondary to-transparent pointer-events-none z-[5]" />

        {/* 滚动容器 - 隐藏滚动条 */}
        <div 
          ref={scrollContainerRef}
          onScroll={handleScroll}
          className="overflow-x-auto pb-4 scrollbar-hide px-16"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          <div className="flex gap-4 py-2">
            {influencers.map((influencer, index) => {
              const cardStyle = getCardStyle(index)
              if (index === 0) {
                console.log('🎯 Applying style to card 0:', cardStyle)
              }
              return (
                <div key={influencer.id} style={cardStyle}>
                  <InfluencerCard influencer={influencer} />
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}

