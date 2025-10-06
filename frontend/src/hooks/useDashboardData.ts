/**
 * Dashboard实时数据Hook
 * 实现10秒自动轮询，获取大屏所有数据
 */

import { useState, useEffect, useCallback } from 'react'
import { api } from '@/lib/api'

export interface DashboardStats {
  total_projects: number
  new_today: number
  s_grade: number
  a_grade: number
  b_grade: number
  pending: number
  trending: number
  total_tvl: number
  avg_score: number
  timestamp: string
}

export interface ProjectItem {
  id: number
  name: string
  symbol: string
  grade: string
  score: number
  category: string
  blockchain: string
  discovered_at: string
  is_new?: boolean
  rank?: number
  scores?: {
    team: number
    tech: number
    community: number
  }
}

export interface GradeDistribution {
  grade: string
  count: number
  percent: number
}

export interface CategoryStats {
  category: string
  count: number
  avg_score: number
  high_grade_count: number
}

export interface Activity {
  type: string
  title: string
  timestamp: string
  grade?: string
  score?: number
  sentiment?: string
  status?: string
}

export interface DashboardData {
  stats: DashboardStats
  recent: {
    items: ProjectItem[]
    count: number
  }
  top_projects: {
    items: ProjectItem[]
    count: number
  }
  distribution: {
    distribution: GradeDistribution[]
    total: number
  }
  categories: {
    categories: CategoryStats[]
    total_categories: number
  }
  timeline: {
    activities: Activity[]
    count: number
  }
  updated_at: string
}

interface UseDashboardDataReturn {
  data: DashboardData | null
  loading: boolean
  error: string | null
  lastUpdate: number
  refetch: () => Promise<void>
}

export function useDashboardData(
  interval: number = 10000 // 默认10秒
): UseDashboardDataReturn {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState(Date.now())

  const fetchData = useCallback(async () => {
    try {
      setError(null)
      
      // 使用汇总接口一次获取所有数据
      const response = await api.get('/dashboard/summary')
      
      if (response.success && response.data) {
        setData(response.data)
        setLastUpdate(Date.now())
      } else {
        throw new Error(response.error || '获取数据失败')
      }
    } catch (err: any) {
      console.error('Dashboard数据获取失败:', err)
      setError(err.message || '网络错误')
    } finally {
      setLoading(false)
    }
  }, [])

  // 初始加载
  useEffect(() => {
    fetchData()
  }, [fetchData])

  // 定时轮询
  useEffect(() => {
    if (interval <= 0) return

    const timer = setInterval(() => {
      fetchData()
    }, interval)

    return () => clearInterval(timer)
  }, [interval, fetchData])

  return {
    data,
    loading,
    error,
    lastUpdate,
    refetch: fetchData
  }
}

