/**
 * 活动时间线组件
 * 显示最近活动，自动滚动展示实时数据
 */

'use client'

import { Activity as ActivityIcon, Clock, CheckCircle, AlertCircle } from 'lucide-react'
import { Activity } from '@/hooks/useDashboardData'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import { useEffect, useRef } from 'react'

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
  const containerRef = useRef<HTMLDivElement>(null)
  const prevActivitiesRef = useRef<Activity[]>([])

  // 自动滚动动画
  useEffect(() => {
    if (!containerRef.current || !activities || activities.length === 0) return

    // 检测是否有新活动
    const hasNewActivity = activities.length > prevActivitiesRef.current.length
    
    if (hasNewActivity) {
      // 新活动时滚动到顶部
      containerRef.current.scrollTo({ top: 0, behavior: 'smooth' })
    }

    prevActivitiesRef.current = activities
  }, [activities])

  // 自动滚动效果 - 每5秒向下滚动一个活动
  useEffect(() => {
    if (!containerRef.current || !activities || activities.length <= 5) return

    const interval = setInterval(() => {
      if (containerRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = containerRef.current
        
        // 如果滚动到底部，回到顶部
        if (scrollTop + clientHeight >= scrollHeight - 10) {
          containerRef.current.scrollTo({ top: 0, behavior: 'smooth' })
        } else {
          // 否则向下滚动一个活动的高度（约100px）
          containerRef.current.scrollBy({ top: 100, behavior: 'smooth' })
        }
      }
    }, 5000) // 每5秒滚动一次

    return () => clearInterval(interval)
  }, [activities])

  if (!activities || activities.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2 text-accent-primary" />
          实时活动流
        </h3>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-20 bg-bg-tertiary rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  // 只显示最近10条活动
  const displayActivities = activities.slice(0, 10)

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
        <Clock className="w-5 h-5 mr-2 text-accent-primary" />
        实时活动流
        <span className="ml-auto text-xs text-text-tertiary">自动滚动</span>
      </h3>
      
      <div 
        ref={containerRef}
        className="space-y-3 max-h-[996px] overflow-y-auto scrollbar-hide"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {displayActivities.map((activity, index) => (
          <ActivityItem key={`${activity.timestamp}-${index}`} activity={activity} />
        ))}
      </div>
    </div>
  )
}

