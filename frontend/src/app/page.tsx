/**
 * 首页 - 实时监控大屏
 * 团队工作时实时监控，10秒自动刷新，支持交互
 */

"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Toaster } from 'react-hot-toast'
import { TrendingUp } from 'lucide-react'

// Hooks
import { useDashboardData, ProjectItem } from '@/hooks/useDashboardData'

// Components
import { StatsCards } from '@/components/dashboard/StatsCards'
import { TopProjects } from '@/components/dashboard/TopProjects'
import { GradeDistributionChart, CategoryStatsChart } from '@/components/dashboard/Charts'
import { ActivityTimeline } from '@/components/dashboard/ActivityTimeline'
import { PlatformInfluencers } from '@/components/dashboard/PlatformInfluencers'
import { NewProjectAlert } from '@/components/dashboard/NewProjectAlert'
import { RefreshIndicator } from '@/components/dashboard/RefreshIndicator'

export default function Dashboard() {
  const { data, loading, error, lastUpdate, refetch } = useDashboardData(10000) // 10秒刷新
  const [newProjects, setNewProjects] = useState<ProjectItem[]>([])
  const [previousProjects, setPreviousProjects] = useState<Set<number>>(new Set())

  // 检测新S/A级项目
  useEffect(() => {
    if (!data?.recent?.items) return

    const currentProjects = new Set(data.recent.items.map(p => p.id))
    const highGradeNewProjects = data.recent.items.filter(p => 
      p.is_new && 
      ['S', 'A'].includes(p.grade) &&
      !previousProjects.has(p.id)
    )

    if (highGradeNewProjects.length > 0) {
      setNewProjects(highGradeNewProjects)
    }

    setPreviousProjects(currentProjects)
  }, [data?.recent?.items])

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <div className="text-text-secondary">加载大屏数据中...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-4 lg:p-6">
      {/* Toast容器 */}
      <Toaster position="top-right" />

      {/* 头部 */}
      <header className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <Link href="/">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
                🚀 Web3 Alpha Hunter
              </h1>
            </Link>
            <p className="text-text-secondary text-sm mt-1">
              AI驱动的实时监控大屏 · 10秒自动刷新
            </p>
          </div>

          <div className="flex items-center gap-4">
            <RefreshIndicator 
              lastUpdate={lastUpdate} 
              onRefresh={refetch}
              error={error}
            />

            <Link
              href="/projects"
              className="px-4 py-2 bg-gradient-to-r from-accent-primary to-accent-purple rounded-lg font-semibold text-white hover:scale-105 transition-transform"
            >
              <TrendingUp className="w-4 h-4 inline mr-2" />
              查看项目列表
            </Link>
          </div>
        </div>
      </header>

      {/* 统计卡片区 */}
      <StatsCards stats={data?.stats} />

      {/* 主内容区: 3列布局 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
        {/* 左列: 热门项目 Top10 */}
        <div className="lg:col-span-4">
          <TopProjects projects={data?.top_projects?.items} />
        </div>

        {/* 中列: 图表区 */}
        <div className="lg:col-span-5 space-y-6">
          <GradeDistributionChart data={data?.distribution} />
          <CategoryStatsChart data={data?.categories} />
        </div>

        {/* 右列: 实时活动流 */}
        <div className="lg:col-span-3">
          <ActivityTimeline activities={data?.timeline?.activities} />
        </div>
      </div>

      {/* 底部: 推荐关注的Web3大V */}
      <PlatformInfluencers />

      {/* 新项目提醒 (不可见组件，只触发通知) */}
      <NewProjectAlert projects={newProjects} />

      {/* 页脚 */}
      <footer className="mt-8 text-center text-text-tertiary text-sm">
        <p>🔥 实时监控 · {data?.stats?.total_projects || 0} 个项目 · 更新于 {new Date(lastUpdate).toLocaleTimeString('zh-CN')}</p>
      </footer>
    </div>
  )
}
