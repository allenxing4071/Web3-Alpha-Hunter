/**
 * 项目对比页面
 */

"use client"

import { useState, useEffect } from 'react'
import { API_BASE_URL } from '@/lib/config'
import { Project } from '@/types/project'
import { ProjectComparison } from '@/components/projects/ProjectComparison'
import { GradeBadge } from '@/components/projects/GradeBadge'

export default function ComparePage() {
  const [allProjects, setAllProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedProjects, setSelectedProjects] = useState<Project[]>([])
  
  // 从API加载项目列表
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/projects?limit=100`)
        if (!response.ok) throw new Error('Failed to fetch')
        const data = await response.json()
        
        // API返回格式: { success: true, data: { projects: [...] } }
        const projectsData = data.data?.projects || data.projects || []
        
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
          key_highlights: [],
          risk_flags: [],
          metrics: {},
          first_discovered_at: p.first_discovered_at || p.created_at,
          last_updated_at: p.last_updated_at || p.updated_at,
        }))
        
        setAllProjects(projects)
      } catch (error) {
        console.error('Failed to load projects:', error)
        setAllProjects([])
      } finally {
        setLoading(false)
      }
    }
    
    fetchProjects()
  }, [])

  const toggleProject = (project: Project) => {
    if (selectedProjects.find(p => p.project_id === project.project_id)) {
      setSelectedProjects(selectedProjects.filter(p => p.project_id !== project.project_id))
    } else {
      if (selectedProjects.length < 4) {
        setSelectedProjects([...selectedProjects, project])
      }
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
          项目对比
        </h1>
        <p className="text-text-secondary mb-8">
          选择2-4个项目进行多维度对比分析
        </p>

        {/* 已选项目 */}
        {selectedProjects.length > 0 && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-text-primary mb-4">
              已选择 ({selectedProjects.length}/4)
            </h2>
            <div className="flex flex-wrap gap-2">
              {selectedProjects.map((project) => (
                <button
                  key={project.project_id}
                  onClick={() => toggleProject(project)}
                  className="px-4 py-2 bg-accent-primary/20 border border-accent-primary text-accent-primary rounded-lg hover:bg-accent-primary/30 transition-colors flex items-center gap-2"
                >
                  {project.name}
                  <span className="text-xs">✕</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* 对比结果 */}
        {selectedProjects.length >= 2 && (
          <div className="mb-8 bg-bg-tertiary border border-gray-700 rounded-lg p-6">
            <ProjectComparison projects={selectedProjects} />
          </div>
        )}

        {/* 项目选择列表 */}
        <div>
          <h2 className="text-lg font-semibold text-text-primary mb-4">
            选择项目
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {allProjects.map((project) => {
              const isSelected = !!selectedProjects.find(p => p.project_id === project.project_id)
              const canSelect = selectedProjects.length < 4 || isSelected

              return (
                <button
                  key={project.project_id}
                  onClick={() => canSelect && toggleProject(project)}
                  disabled={!canSelect}
                  className={`
                    p-4 rounded-lg border transition-all text-left
                    ${isSelected 
                      ? 'bg-accent-primary/10 border-accent-primary' 
                      : canSelect
                        ? 'bg-bg-secondary border-gray-700 hover:border-accent-primary'
                        : 'bg-bg-secondary border-gray-700 opacity-50 cursor-not-allowed'
                    }
                  `}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-text-primary">{project.name}</h3>
                      <p className="text-sm text-text-tertiary">{project.category}</p>
                    </div>
                    <GradeBadge grade={project.grade} score={project.overall_score} size="sm" />
                  </div>
                  <p className="text-sm text-text-secondary line-clamp-2">
                    {project.description}
                  </p>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}

