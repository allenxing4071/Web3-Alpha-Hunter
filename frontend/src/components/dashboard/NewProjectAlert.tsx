/**
 * 新项目提醒组件
 * 当发现S/A级新项目时弹窗通知
 */

import { useEffect } from 'react'
import toast from 'react-hot-toast'
import { Trophy, Star, ExternalLink } from 'lucide-react'
import { ProjectItem } from '@/hooks/useDashboardData'

interface NewProjectAlertProps {
  projects: ProjectItem[]
}

export function NewProjectAlert({ projects }: NewProjectAlertProps) {
  useEffect(() => {
    // 只对新的S/A级项目发送通知
    const newHighGradeProjects = projects.filter(
      p => p.is_new && (p.grade === 'S' || p.grade === 'A')
    )

    newHighGradeProjects.forEach((project) => {
      const isS = project.grade === 'S'
      
      toast.custom(
        (t) => (
          <div
            className={`
              ${t.visible ? 'animate-enter' : 'animate-leave'}
              max-w-md w-full bg-bg-secondary shadow-xl rounded-xl p-4 border-2
              ${isS ? 'border-accent-gold glow-gold-pulse' : 'border-accent-purple'}
            `}
          >
            <div className="flex items-start gap-3">
              <div className={`
                p-2 rounded-lg flex-shrink-0
                ${isS ? 'bg-accent-gold/20' : 'bg-accent-purple/20'}
              `}>
                {isS ? (
                  <Trophy className="w-6 h-6 text-accent-gold" />
                ) : (
                  <Star className="w-6 h-6 text-accent-purple" />
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`
                    px-2 py-1 rounded text-xs font-bold
                    ${isS ? 'bg-accent-gold text-black' : 'bg-accent-purple text-white'}
                  `}>
                    {project.grade}级机会
                  </span>
                  <span className="text-sm text-accent-gold font-bold">
                    ⭐ {project.score.toFixed(1)}
                  </span>
                </div>

                <h4 className="font-bold text-text-primary mb-1 truncate">
                  {project.name}
                </h4>

                <div className="flex items-center gap-2 text-xs text-text-secondary mb-3">
                  <span className="px-2 py-0.5 bg-bg-primary rounded">
                    {project.category}
                  </span>
                  <span>{project.blockchain}</span>
                </div>

                <p className="text-sm text-text-secondary">
                  {isS ? '🎯 发现S级投资机会！' : '⭐ 发现A级优质项目！'}
                </p>
              </div>

              <button
                onClick={() => toast.dismiss(t.id)}
                className="flex-shrink-0 text-text-tertiary hover:text-text-primary"
              >
                ✕
              </button>
            </div>

            <div className="mt-3 pt-3 border-t border-gray-700">
              <button
                onClick={() => {
                  toast.dismiss(t.id)
                  // 这里可以跳转到项目详情页
                  window.location.href = `/projects?id=${project.id}`
                }}
                className="
                  w-full flex items-center justify-center gap-2
                  px-4 py-2 rounded-lg
                  bg-accent-primary hover:bg-accent-primary/80
                  text-white font-medium text-sm
                  transition-all
                "
              >
                <ExternalLink className="w-4 h-4" />
                查看详情
              </button>
            </div>
          </div>
        ),
        {
          duration: 5000, // 5秒后自动消失
          position: 'top-right',
        }
      )
    })
  }, [projects])

  return null // 这个组件不渲染任何UI，只负责触发通知
}

