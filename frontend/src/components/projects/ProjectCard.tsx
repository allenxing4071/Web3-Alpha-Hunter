/**
 * 项目卡片组件 - 整个UI的核心
 */

"use client"

import { useRouter } from "next/navigation"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { GradeBadge } from "./GradeBadge"
import { RiskTag } from "./RiskTag"
import { cn } from "@/lib/utils"
import { Project } from "@/types/project"
import { formatDistanceToNow } from "date-fns"
import { zhCN } from "date-fns/locale"

interface ProjectCardProps {
  project: Project
  className?: string
}

export function ProjectCard({ project, className }: ProjectCardProps) {
  const router = useRouter()
  
  const {
    project_id,
    name,
    symbol,
    grade,
    overall_score,
    category,
    blockchain,
    description,
    key_highlights,
    risk_flags,
    metrics,
    first_discovered_at,
  } = project
  
  // S级卡片特殊样式
  const isS = grade === 'S'
  const isA = grade === 'A'
  
  const handleClick = () => {
    router.push(`/projects/${project_id}`)
  }
  
  return (
    <div onClick={handleClick} className="cursor-pointer">
      <Card
        className={cn(
          "group relative overflow-hidden transition-all duration-300",
          "hover:scale-[1.02] hover:shadow-2xl",
          "bg-bg-tertiary border-gray-700",
          isS && "border-accent-gold border-2 glow-gold bg-gradient-to-br from-bg-tertiary to-yellow-900/10",
          isA && "border-accent-purple border-2 hover:shadow-purple-500/20",
          className
        )}
      >
        {/* 顶部渐变条 */}
        <div
          className={cn(
            "absolute top-0 left-0 right-0 h-1",
            isS && "bg-gradient-to-r from-yellow-500 via-yellow-300 to-yellow-500",
            isA && "bg-gradient-to-r from-purple-500 via-purple-300 to-purple-500",
            !isS && !isA && "bg-gradient-to-r from-blue-500 to-blue-300"
          )}
        />
        
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-4">
            {/* 项目信息 */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {/* 项目Logo占位 */}
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-primary to-accent-purple flex items-center justify-center text-white font-bold">
                  {name?.[0] || '?'}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-bold text-text-primary truncate group-hover:text-accent-primary transition-colors">
                    {name}
                  </h3>
                  {symbol && (
                    <p className="text-sm text-text-tertiary">${symbol}</p>
                  )}
                </div>
              </div>
            </div>
            
            {/* 评分徽章 */}
            <GradeBadge grade={grade} score={overall_score} size="md" />
          </div>
          
          {/* 标签行 */}
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            {category && (
              <span className="px-2 py-1 bg-blue-900/30 text-blue-300 text-xs rounded-md border border-blue-700/50">
                💰 {category}
              </span>
            )}
            {blockchain && (
              <span className="px-2 py-1 bg-purple-900/30 text-purple-300 text-xs rounded-md border border-purple-700/50">
                ⛓️ {blockchain}
              </span>
            )}
            <span className="px-2 py-1 bg-gray-800 text-text-tertiary text-xs rounded-md">
              🕐 {formatDistanceToNow(new Date(first_discovered_at), { 
                addSuffix: true,
                locale: zhCN 
              })}
            </span>
          </div>
        </CardHeader>
        
        <CardContent className="pb-3">
          {/* 项目描述 */}
          {description && (
            <p className="text-sm text-text-secondary line-clamp-2 mb-3">
              {description}
            </p>
          )}
          
          {/* 核心亮点 */}
          {key_highlights && key_highlights.length > 0 && (
            <div className="space-y-1.5 mb-3">
              <p className="text-xs text-text-tertiary font-semibold">✨ 核心亮点</p>
              {key_highlights.slice(0, 3).map((highlight, idx) => (
                <div key={idx} className="flex items-start gap-2 text-xs text-text-secondary">
                  <span className="text-accent-primary mt-0.5">•</span>
                  <span className="line-clamp-1">{highlight}</span>
                </div>
              ))}
            </div>
          )}
          
          {/* 风险标签 */}
          {risk_flags && risk_flags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-3">
              {risk_flags.slice(0, 2).map((risk, idx) => (
                <RiskTag key={idx} risk={risk} />
              ))}
              {risk_flags.length > 2 && (
                <span className="text-xs text-text-tertiary">
                  +{risk_flags.length - 2} 更多
                </span>
              )}
            </div>
          )}
          
          {/* 关键指标 */}
          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-gray-700/50">
            {metrics?.twitter_followers && (
              <div className="text-center">
                <p className="text-xs text-text-tertiary">社区</p>
                <p className="text-sm font-semibold text-accent-primary">
                  {metrics.twitter_followers > 1000 
                    ? `${(metrics.twitter_followers / 1000).toFixed(1)}k`
                    : metrics.twitter_followers}
                </p>
              </div>
            )}
            {metrics?.tvl_usd && (
              <div className="text-center">
                <p className="text-xs text-text-tertiary">TVL</p>
                <p className="text-sm font-semibold text-success">
                  ${metrics.tvl_usd > 1000000
                    ? `${(metrics.tvl_usd / 1000000).toFixed(1)}M`
                    : `${(metrics.tvl_usd / 1000).toFixed(0)}k`}
                </p>
              </div>
            )}
            {metrics?.github_stars && (
              <div className="text-center">
                <p className="text-xs text-text-tertiary">Stars</p>
                <p className="text-sm font-semibold text-warning">
                  ⭐ {metrics.github_stars}
                </p>
              </div>
            )}
          </div>
        </CardContent>
        
        <CardFooter className="pt-3 border-t border-gray-700/50">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              {project.social_links?.twitter && (
                <a
                  href={`https://twitter.com/${project.social_links.twitter}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="text-text-tertiary hover:text-accent-primary transition-colors"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
              )}
              {project.social_links?.telegram && (
                <a
                  href={`https://t.me/${project.social_links.telegram}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="text-text-tertiary hover:text-accent-primary transition-colors"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.903-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.14.121.098.155.23.171.324.016.062.036.201.02.312z"/>
                  </svg>
                </a>
              )}
            </div>
            
            <button
              className={cn(
                "px-4 py-1.5 rounded-lg text-xs font-semibold transition-all",
                "hover:scale-105",
                isS && "bg-gradient-to-r from-yellow-500 to-yellow-600 text-gray-900 hover:shadow-lg hover:shadow-yellow-500/50",
                isA && "bg-gradient-to-r from-purple-500 to-purple-600 text-white hover:shadow-lg hover:shadow-purple-500/50",
                !isS && !isA && "bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:shadow-lg"
              )}
              onClick={(e) => {
                e.stopPropagation()
                router.push(`/projects/${project_id}`)
              }}
            >
              查看详情 →
            </button>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}

