/**
 * 项目对比组件
 */

"use client"

import { Project } from '@/types/project'
import { GradeBadge } from './GradeBadge'

interface ProjectComparisonProps {
  projects: Project[]
  className?: string
}

export function ProjectComparison({ projects, className }: ProjectComparisonProps) {
  if (projects.length < 2) {
    return (
      <div className="text-center text-text-secondary py-8">
        请选择至少2个项目进行对比
      </div>
    )
  }

  const metrics = [
    { key: 'overall_score', label: '综合评分', suffix: '/100' },
    { key: 'category', label: '分类', suffix: '' },
    { key: 'blockchain', label: '区块链', suffix: '' },
  ]

  return (
    <div className={className}>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="p-4 text-left text-text-secondary">指标</th>
              {projects.map((project) => (
                <th key={project.project_id} className="p-4 text-center">
                  <div className="space-y-2">
                    <div className="font-bold text-text-primary">{project.name}</div>
                    <GradeBadge grade={project.grade} score={project.overall_score} size="sm" />
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric) => (
              <tr key={metric.key} className="border-b border-gray-700/50">
                <td className="p-4 text-text-secondary font-medium">{metric.label}</td>
                {projects.map((project) => (
                  <td key={project.project_id} className="p-4 text-center text-text-primary">
                    {project[metric.key as keyof Project]}{metric.suffix}
                  </td>
                ))}
              </tr>
            ))}
            
            {/* GitHub Stars */}
            <tr className="border-b border-gray-700/50">
              <td className="p-4 text-text-secondary font-medium">GitHub Stars</td>
              {projects.map((project) => (
                <td key={project.project_id} className="p-4 text-center text-text-primary">
                  {project.metrics?.github_stars 
                    ? `⭐ ${(project.metrics.github_stars / 1000).toFixed(1)}k`
                    : '-'}
                </td>
              ))}
            </tr>
            
            {/* 风险等级 */}
            <tr className="border-b border-gray-700/50">
              <td className="p-4 text-text-secondary font-medium">风险提示</td>
              {projects.map((project) => (
                <td key={project.project_id} className="p-4 text-center">
                  {project.risk_flags.length > 0 ? (
                    <span className="text-warning">⚠️ {project.risk_flags.length}个</span>
                  ) : (
                    <span className="text-success">✅ 无</span>
                  )}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

