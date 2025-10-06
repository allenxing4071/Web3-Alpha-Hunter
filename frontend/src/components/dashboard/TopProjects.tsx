/**
 * Top项目列表组件
 * 显示排名前10的高分项目
 */

'use client'

import { Trophy, Star, TrendingUp } from 'lucide-react'
import { ProjectItem } from '@/hooks/useDashboardData'

interface TopProjectsProps {
  projects: ProjectItem[] | null | undefined
}

function GradeBadge({ grade }: { grade: string }) {
  const colors = {
    S: 'bg-accent-gold text-black',
    A: 'bg-accent-purple text-white',
    B: 'bg-accent-primary text-white',
    C: 'bg-gray-600 text-white'
  }

  return (
    <span className={`px-2 py-1 rounded text-xs font-bold ${colors[grade as keyof typeof colors] || colors.C}`}>
      {grade}
    </span>
  )
}

function RankBadge({ rank }: { rank: number }) {
  if (rank === 1) {
    return <div className="text-2xl">🥇</div>
  }
  if (rank === 2) {
    return <div className="text-2xl">🥈</div>
  }
  if (rank === 3) {
    return <div className="text-2xl">🥉</div>
  }
  return <div className="text-lg font-bold text-text-secondary">#{rank}</div>
}

export function TopProjects({ projects }: TopProjectsProps) {
  if (!projects || projects.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
          <Trophy className="w-5 h-5 mr-2 text-accent-gold" />
          Top 10 热门项目
        </h3>
        <div className="space-y-3">
          {[...Array(10)].map((_, i) => (
            <div key={i} className="h-16 bg-bg-tertiary rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 flex flex-col w-full h-full min-h-[800px]">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center flex-shrink-0">
        <Trophy className="w-5 h-5 mr-2 text-accent-gold" />
        Top 10 热门项目
      </h3>
      
      <div className="space-y-3 overflow-y-auto pr-2 scrollbar-thin flex-1">
        {projects.map((project) => (
          <div
            key={project.id}
            className="bg-bg-tertiary rounded-lg p-4 border border-gray-700 hover:border-accent-primary 
                     transition-all cursor-pointer group"
          >
            <div className="flex items-start gap-3">
              {/* 排名 */}
              <div className="flex-shrink-0">
                <RankBadge rank={project.rank || 0} />
              </div>

              {/* 项目信息 */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="font-semibold text-text-primary truncate group-hover:text-accent-primary transition-colors">
                    {project.name}
                  </h4>
                  <GradeBadge grade={project.grade} />
                </div>

                <div className="flex items-center gap-3 text-xs text-text-secondary mb-2">
                  <span className="px-2 py-0.5 bg-bg-primary rounded">
                    {project.category}
                  </span>
                  <span>{project.blockchain}</span>
                </div>

                {/* 评分 */}
                <div className="flex items-center gap-2">
                  <Star className="w-4 h-4 text-accent-gold fill-accent-gold" />
                  <span className="text-lg font-bold text-accent-gold">
                    {project.score.toFixed(1)}
                  </span>
                  {project.scores && (
                    <div className="ml-auto flex gap-2 text-xs text-text-tertiary">
                      <span title="团队评分">团队 {project.scores.team.toFixed(0)}</span>
                      <span title="技术评分">技术 {project.scores.tech.toFixed(0)}</span>
                      <span title="社区评分">社区 {project.scores.community.toFixed(0)}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

