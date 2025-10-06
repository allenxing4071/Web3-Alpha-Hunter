/**
 * 活动时间线组件
 * 显示最近1小时的项目活动
 */

'use client'

import { Activity as ActivityIcon, Clock, CheckCircle, AlertCircle } from 'lucide-react'
import { Activity } from '@/hooks/useDashboardData'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

interface ActivityTimelineProps {
  activities: Activity[] | null | undefined
}

function ActivityItem({ activity }: { activity: Activity }) {
  const getIcon = () => {
    switch (activity.type) {
      case 'project_discovered':
        return <ActivityIcon className="w-4 h-4 text-success" />
      case 'ai_analysis':
        return <ActivityIcon className="w-4 h-4 text-accent-purple" />
      case 'project_reviewed':
        return activity.status === 'approved' 
          ? <CheckCircle className="w-4 h-4 text-success" />
          : <AlertCircle className="w-4 h-4 text-error" />
      default:
        return <Clock className="w-4 h-4 text-text-secondary" />
    }
  }

  const getTypeLabel = () => {
    switch (activity.type) {
      case 'project_discovered':
        return '新发现'
      case 'ai_analysis':
        return 'AI分析'
      case 'project_reviewed':
        return '项目审核'
      default:
        return '活动'
    }
  }

  const getTimeAgo = () => {
    try {
      return formatDistanceToNow(new Date(activity.timestamp), {
        addSuffix: true,
        locale: zhCN
      })
    } catch {
      return '刚刚'
    }
  }

  return (
    <div className="flex items-start gap-3 p-3 bg-bg-tertiary rounded-lg hover:bg-bg-tertiary/80 transition-colors slide-in">
      <div className="flex-shrink-0 mt-1">
        {getIcon()}
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs text-text-secondary">{getTypeLabel()}</span>
          {activity.grade && (
            <span className={`
              text-xs px-1.5 py-0.5 rounded font-bold
              ${activity.grade === 'S' ? 'bg-accent-gold text-black' : ''}
              ${activity.grade === 'A' ? 'bg-accent-purple text-white' : ''}
              ${activity.grade === 'B' ? 'bg-accent-primary text-white' : ''}
            `}>
              {activity.grade}
            </span>
          )}
        </div>
        
        <div className="text-sm text-text-primary font-medium truncate mb-1">
          {activity.title}
        </div>
        
        <div className="text-xs text-text-tertiary">
          {getTimeAgo()}
        </div>
      </div>

      {activity.score > 0 && (
        <div className="flex-shrink-0 text-right">
          <div className="text-sm font-bold text-accent-gold">
            {activity.score.toFixed(1)}
          </div>
          <div className="text-xs text-text-tertiary">评分</div>
        </div>
      )}
    </div>
  )
}

export function ActivityTimeline({ activities }: ActivityTimelineProps) {
  if (!activities || activities.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2 text-accent-primary" />
          实时活动流
        </h3>
        <div className="space-y-3">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-20 bg-bg-tertiary rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6 flex flex-col h-full">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center flex-shrink-0">
        <Clock className="w-5 h-5 mr-2 text-accent-primary" />
        实时活动流
      </h3>
      
      <div className="space-y-3 overflow-y-auto pr-2 scrollbar-thin flex-1 max-h-[700px]">
        {activities.map((activity, index) => (
          <ActivityItem key={index} activity={activity} />
        ))}
      </div>

      {activities.length === 0 && (
        <div className="text-center text-text-secondary py-8">
          暂无最近活动
        </div>
      )}
    </div>
  )
}

