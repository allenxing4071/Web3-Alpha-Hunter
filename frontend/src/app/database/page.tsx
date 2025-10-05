"use client"

import { useState, useEffect } from 'react'
import { useAuthStore } from '@/store/authStore'
import { AuthGuard } from '@/components/AuthGuard'

interface DatabaseStats {
  tableCount: number
  projectCount: number
  databaseType: string
  databasePort: number
}

export default function DatabasePage() {
  const { user } = useAuthStore()
  const [activeTab, setActiveTab] = useState('projects')
  const [stats, setStats] = useState<DatabaseStats>({
    tableCount: 9,
    projectCount: 0,
    databaseType: 'PostgreSQL',
    databasePort: 5432
  })

  useEffect(() => {
    loadDatabaseStats()
  }, [])

  const loadDatabaseStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/database/stats')
      const result = await response.json()
      if (result.success) {
        setStats({
          tableCount: result.data.table_count,
          projectCount: result.data.project_count,
          databaseType: result.data.database_type,
          databasePort: result.data.database_port
        })
      }
    } catch (error) {
      console.error('加载数据库统计失败:', error)
    }
  }

  const tabs = [
    { id: 'projects', label: '📊 Projects', name: '项目表' },
    { id: 'social', label: '📱 Social Metrics', name: '社交指标' },
    { id: 'onchain', label: '⛓️ Onchain Metrics', name: '链上数据' },
    { id: 'ai', label: '🤖 AI Analysis', name: 'AI分析' },
    { id: 'aiconfig', label: '🔑 AI Configs', name: 'AI配置' },
    { id: 'tokenlaunch', label: '🚀 Token Launch', name: '发币预测' },
    { id: 'airdrop', label: '💰 Airdrop', name: '空投估算' },
    { id: 'investment', label: '📋 Investment', name: '投资计划' },
    { id: 'discovery', label: '🔍 Discovery', name: '项目发现' },
  ]

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen bg-bg-primary">
        {/* Header */}
        <div className="bg-bg-tertiary border-b border-gray-800 sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  🗄️ 数据库管理
                </h1>
                <p className="text-text-secondary mt-1">查看和管理系统数据库表结构与数据</p>
              </div>
              {user && (
                <div className="text-sm text-text-secondary">
                  欢迎，<span className="text-accent-primary font-medium">{user.username}</span>
                  {user.role === 'admin' && (
                    <span className="ml-2 px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">管理员</span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 p-6 rounded-xl border border-purple-500/20">
              <div className="text-4xl font-bold text-white">{stats.tableCount}</div>
              <div className="text-sm text-gray-400 mt-2">数据表</div>
            </div>
            <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 p-6 rounded-xl border border-blue-500/20">
              <div className="text-4xl font-bold text-white">{stats.projectCount}</div>
              <div className="text-sm text-gray-400 mt-2">示例项目</div>
            </div>
            <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 p-6 rounded-xl border border-green-500/20">
              <div className="text-2xl font-bold text-white">{stats.databaseType}</div>
              <div className="text-sm text-gray-400 mt-2">数据库类型</div>
            </div>
            <div className="bg-gradient-to-br from-orange-500/10 to-red-500/10 p-6 rounded-xl border border-orange-500/20">
              <div className="text-4xl font-bold text-white">{stats.databasePort}</div>
              <div className="text-sm text-gray-400 mt-2">端口</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="bg-bg-tertiary rounded-xl border border-gray-800 overflow-hidden">
            <div className="flex gap-2 p-4 border-b border-gray-800 overflow-x-auto">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="p-6">
              <div className="bg-gray-900/50 rounded-xl p-8 border border-gray-800">
                <h3 className="text-xl font-bold text-white mb-4">
                  {tabs.find(t => t.id === activeTab)?.name}
                </h3>
                <div className="text-gray-400 space-y-4">
                  <p>表结构和数据内容展示区域</p>
                  <div className="bg-bg-tertiary p-4 rounded-lg border border-gray-700">
                    <p className="text-sm text-gray-500">
                      💡 提示: 完整的表结构和数据查询功能正在开发中...
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      当前显示的是 <span className="text-accent-primary font-mono">{activeTab}</span> 表
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
