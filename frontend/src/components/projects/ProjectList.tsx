/**
 * 项目列表组件
 */

import { ProjectCard } from "./ProjectCard"
import { ProjectCardSkeleton } from "./ProjectCardSkeleton"
import { Project } from "@/types/project"

interface ProjectListProps {
  projects: Project[]
  loading?: boolean
}

export function ProjectList({ projects, loading }: ProjectListProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <ProjectCardSkeleton key={i} />
        ))}
      </div>
    )
  }
  
  if (projects.length === 0) {
    return (
      <div className="text-center py-20">
        <div className="text-6xl mb-4">🔍</div>
        <h3 className="text-xl font-semibold text-text-primary mb-2">
          暂无项目
        </h3>
        <p className="text-text-secondary">
          继续监控中,发现后将第一时间推送
        </p>
      </div>
    )
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {projects.map((project) => (
        <ProjectCard key={project.project_id} project={project} />
      ))}
    </div>
  )
}

