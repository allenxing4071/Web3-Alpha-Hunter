/**
 * 实时统计卡片组件
 * 显示6个核心指标
 */

'use client'

import { TrendingUp, Trophy, Star, Clock, AlertCircle, DollarSign } from 'lucide-react'
import { DashboardStats } from '@/hooks/useDashboardData'

interface StatsCardsProps {
  stats: DashboardStats | null | undefined
}

interface StatCardProps {
  title: string
  value: number | string
  icon: React.ReactNode
  trend?: number
  highlight?: boolean
  color?: string
}

function StatCard({ title, value, icon, trend, highlight, color = 'blue' }: StatCardProps) {
  const colorClasses = {
    blue: 'border-accent-primary bg-accent-primary/5',
    gold: 'border-accent-gold bg-accent-gold/5 glow-gold-pulse',
    green: 'border-success bg-success/5',
    orange: 'border-warning bg-warning/5',
    purple: 'border-accent-purple bg-accent-purple/5'
  }

  const iconColorClasses = {
    blue: 'text-accent-primary',
    gold: 'text-accent-gold',
    green: 'text-success',
    orange: 'text-warning',
    purple: 'text-accent-purple'
  }

  return (
    <div 
      className={`
        rounded-xl border-2 p-6 transition-all duration-300
        hover:scale-105 hover:shadow-xl
        ${colorClasses[color as keyof typeof colorClasses] || colorClasses.blue}
        ${highlight ? 'animate-pulse-slow' : ''}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="text-text-secondary text-sm font-medium mb-2">
            {title}
          </div>
          <div className="text-4xl font-bold text-text-primary mb-1">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </div>
          {trend !== undefined && (
            <div className={`flex items-center text-sm ${trend >= 0 ? 'text-success' : 'text-error'}`}>
              <TrendingUp className={`w-4 h-4 mr-1 ${trend < 0 ? 'rotate-180' : ''}`} />
              <span>{Math.abs(trend)}%</span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-lg bg-bg-tertiary ${iconColorClasses[color as keyof typeof iconColorClasses]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

export function StatsCards({ stats }: StatsCardsProps) {
  if (!stats) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-32 bg-bg-tertiary rounded-xl animate-pulse" />
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
      {/* 总项目数 */}
      <StatCard
        title="总项目数"
        value={stats.total_projects}
        icon={<DollarSign className="w-6 h-6" />}
        color="blue"
      />

      {/* S级机会 - 金色高亮 */}
      <StatCard
        title="S级机会"
        value={stats.s_grade}
        icon={<Trophy className="w-6 h-6" />}
        highlight={stats.s_grade > 0}
        color="gold"
      />

      {/* A级项目 */}
      <StatCard
        title="A级项目"
        value={stats.a_grade}
        icon={<Star className="w-6 h-6" />}
        color="purple"
      />

      {/* 待审核 */}
      <StatCard
        title="待审核"
        value={stats.pending}
        icon={<AlertCircle className="w-6 h-6" />}
        color="orange"
      />

      {/* 今日发现 */}
      <StatCard
        title="今日发现"
        value={stats.new_today}
        icon={<Clock className="w-6 h-6" />}
        trend={stats.new_today > 0 ? 15 : 0}
        color="green"
      />

      {/* 平均评分 */}
      <StatCard
        title="平均评分"
        value={stats.avg_score.toFixed(1)}
        icon={<TrendingUp className="w-6 h-6" />}
        color="blue"
      />
    </div>
  )
}

