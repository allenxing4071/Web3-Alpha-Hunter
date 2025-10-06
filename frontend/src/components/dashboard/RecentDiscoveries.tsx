/**
 * 最新发现项目组件
 * 横向滚动展示最近24小时发现的项目
 */

'use client'

import { Sparkles, TrendingUp } from 'lucide-react'
import { ProjectItem } from '@/hooks/useDashboardData'

interface RecentDiscoveriesProps {
  projects: ProjectItem[] | null | undefined
}

function ProjectCard({ project }: { project: ProjectItem }) {
  const gradeColors = {
    S: 'border-accent-gold bg-accent-gold/10',
    A: 'border-accent-purple bg-accent-purple/10',
    B: 'border-accent-primary bg-accent-primary/10',
    C: 'border-gray-600 bg-gray-600/10'
  }

  return (
    <div className={`
      flex-shrink-0 w-72 p-4 rounded-xl border-2 
      ${gradeColors[project.grade as keyof typeof gradeColors] || gradeColors.C}
      ${project.is_new ? 'animate-pulse-slow glow-gold' : ''}
      hover:scale-105 transition-transform cursor-pointer
    `}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h4 className="font-bold text-text-primary truncate mb-1">
            {project.name}
          </h4>
          <div className="text-xs text-text-secondary">
            {project.symbol}
          </div>
        </div>
        
        {project.is_new && (
          <div className="flex-shrink-0 ml-2">
            <Sparkles className="w-5 h-5 text-accent-gold animate-pulse" />
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 mb-3">
        <span className={`
          px-2 py-1 rounded text-xs font-bold
          ${project.grade === 'S' ? 'bg-accent-gold text-black' : ''}
          ${project.grade === 'A' ? 'bg-accent-purple text-white' : ''}
          ${project.grade === 'B' ? 'bg-accent-primary text-white' : ''}
          ${project.grade === 'C' ? 'bg-gray-600 text-white' : ''}
        `}>
          {project.grade}级
        </span>
        
        <span className="text-lg font-bold text-accent-gold">
          {project.score.toFixed(1)}
        </span>
      </div>

      <div className="flex items-center gap-2 text-xs">
        <span className="px-2 py-1 bg-bg-primary rounded text-text-secondary">
          {project.category}
        </span>
        <span className="text-text-tertiary">
          {project.blockchain}
        </span>
      </div>
    </div>
  )
}

export function RecentDiscoveries({ projects }: RecentDiscoveriesProps) {
  if (!projects || projects.length === 0) {
    return null
  }

  // 只显示最近的10个项目
  const recentProjects = projects.slice(0, 10)

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 mt-6">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-success" />
        最新发现
        <span className="ml-2 text-sm text-text-secondary font-normal">
          (最近24小时)
        </span>
        {projects.filter(p => p.is_new).length > 0 && (
          <span className="ml-auto flex items-center text-sm text-accent-gold">
            <Sparkles className="w-4 h-4 mr-1" />
            {projects.filter(p => p.is_new).length} 个新项目
          </span>
        )}
      </h3>

      <div className="overflow-x-auto pb-2 scrollbar-thin">
        <div className="flex gap-4">
          {recentProjects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </div>
  )
}

