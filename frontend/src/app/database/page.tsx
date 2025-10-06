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

interface TableStructure {
  field: string
  type: string
  nullable: string
  description: string
}

interface TableData {
  columns: string[]
  rows: any[]
  total: number
  page: number
  limit: number
  total_pages: number
}

export default function DatabasePage() {
  const { user } = useAuthStore()
  const [activeTab, setActiveTab] = useState('projects')
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [tableData, setTableData] = useState<TableData | null>(null)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState<DatabaseStats>({
    tableCount: 9,
    projectCount: 0,
    databaseType: 'PostgreSQL',
    databasePort: 5432
  })

  useEffect(() => {
    loadDatabaseStats()
  }, [])

  useEffect(() => {
    loadTableData()
  }, [activeTab, currentPage, pageSize])

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

  const loadTableData = async () => {
    setLoading(true)
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/database/tables/${activeTab}/data?page=${currentPage}&limit=${pageSize}`
      )
      const result = await response.json()
      if (result.success) {
        setTableData(result.data)
      } else {
        setTableData(null)
      }
    } catch (error) {
      console.error('加载表数据失败:', error)
      setTableData(null)
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  const handlePageSizeChange = (size: number) => {
    setPageSize(size)
    setCurrentPage(1) // 重置到第一页
  }

  const tabs = [
    { id: 'projects', label: '📊 Projects', name: 'Projects', desc: '存储Web3项目的完整数据库，评分集结仓' },
    { id: 'projects_pending', label: '⏳ Projects Pending', name: 'Projects Pending', desc: 'AI推荐的待审核项目' },
    { id: 'social_metrics', label: '📱 Social Metrics', name: 'Social Metrics', desc: '社交媒体数据指标' },
    { id: 'onchain_metrics', label: '⛓️ Onchain Metrics', name: 'Onchain Metrics', desc: '区块链上的实际数据' },
    { id: 'ai_analysis', label: '🤖 AI Analysis', name: 'AI Analysis', desc: 'AI智能分析结果' },
    { id: 'ai_configs', label: '🔑 AI Configs', name: 'AI Configs', desc: 'AI模型配置' },
    { id: 'ai_work_config', label: '🧠 AI Work Config', name: 'AI Work Config', desc: 'AI智能助理工作参数' },
    { id: 'ai_learning_feedback', label: '📚 AI Learning Feedback', name: 'AI Learning Feedback', desc: 'AI学习反馈记录' },
    { id: 'token_launch_predictions', label: '🚀 Token Launch Predictions', name: 'Token Launch Predictions', desc: '代币发行预测' },
    { id: 'airdrop_value_estimates', label: '💰 Airdrop Value Estimates', name: 'Airdrop Value Estimates', desc: '空投价值估算' },
    { id: 'investment_action_plans', label: '📋 Investment Action Plans', name: 'Investment Action Plans', desc: '投资行动计划' },
    { id: 'project_discoveries', label: '🔍 Project Discoveries', name: 'Project Discoveries', desc: '多平台项目热度追踪' },
    { id: 'kols', label: '👤 KOLs', name: 'KOLs', desc: 'KOL数据和表现追踪' },
    { id: 'kols_pending', label: '👥 KOLs Pending', name: 'KOLs Pending', desc: 'AI推荐的待审核KOL' },
    { id: 'kol_performances', label: '📈 KOL Performances', name: 'KOL Performances', desc: 'KOL历史表现追踪' },
    { id: 'platform_search_rules', label: '🌍 Platform Search Rules', name: 'Platform Search Rules', desc: '平台搜索规则配置' },
    { id: 'twitter_keywords', label: '🐦 Twitter Keywords', name: 'Twitter Keywords', desc: 'Twitter搜索关键词库' },
    { id: 'telegram_channels', label: '💬 Telegram Channels', name: 'Telegram Channels', desc: 'Telegram监控频道列表' },
    { id: 'discord_servers', label: '🎮 Discord Servers', name: 'Discord Servers', desc: 'Discord监控服务器列表' },
    { id: 'platform_daily_stats', label: '📊 Platform Daily Stats', name: 'Platform Daily Stats', desc: '平台每日数据统计' },
  ]

  // 表结构定义
  const tableStructures: Record<string, TableStructure[]> = {
    projects: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_name', type: 'VARCHAR(255)', nullable: 'NOT NULL', description: '项目名称' },
      { field: 'symbol', type: 'VARCHAR(50)', nullable: 'NULL', description: '代币符号' },
      { field: 'blockchain', type: 'VARCHAR(50)', nullable: 'NULL', description: '区块链平台' },
      { field: 'category', type: 'VARCHAR(100)', nullable: 'NULL', description: '项目类别' },
      { field: 'overall_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '综合分值 (0-100)' },
      { field: 'grade', type: 'VARCHAR(1)', nullable: 'NULL', description: '项目分级 (S/A/B/C)' },
      { field: 'status', type: 'VARCHAR(50)', nullable: 'NULL', description: '状态' },
      { field: 'first_discovered_at', type: 'TIMESTAMP', nullable: 'NULL', description: '首次发现时间' },
      { field: 'discovered_from', type: 'VARCHAR(100)', nullable: 'NULL', description: '发现来源' },
    ],
    social_metrics: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'twitter_followers', type: 'INTEGER', nullable: 'NULL', description: 'Twitter粉丝数' },
      { field: 'telegram_members', type: 'INTEGER', nullable: 'NULL', description: 'Telegram成员数' },
      { field: 'discord_members', type: 'INTEGER', nullable: 'NULL', description: 'Discord成员数' },
      { field: 'github_stars', type: 'INTEGER', nullable: 'NULL', description: 'GitHub Star数' },
      { field: 'social_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '社交分值' },
    ],
    onchain_metrics: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'market_cap_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '市值(美元)' },
      { field: 'volume_24h_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '24小时交易量' },
      { field: 'tvl_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '锁仓量TVL' },
      { field: 'active_users_24h', type: 'INTEGER', nullable: 'NULL', description: '24小时活跃用户' },
      { field: 'onchain_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '链上分值' },
    ],
    ai_analysis: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'sentiment_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '情感分值' },
      { field: 'risk_level', type: 'VARCHAR(20)', nullable: 'NULL', description: '风险等级' },
      { field: 'innovation_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '创新分值' },
      { field: 'team_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '团队分值' },
      { field: 'summary', type: 'TEXT', nullable: 'NULL', description: 'AI总结' },
    ],
    ai_configs: [
      { field: 'id', type: 'UUID', nullable: 'NOT NULL', description: '主键' },
      { field: 'name', type: 'VARCHAR(50)', nullable: 'NOT NULL', description: 'AI名称' },
      { field: 'api_key', type: 'TEXT', nullable: 'NULL', description: 'API密钥(加密)' },
      { field: 'enabled', type: 'BOOLEAN', nullable: 'NULL', description: '是否启用' },
      { field: 'model', type: 'VARCHAR(100)', nullable: 'NULL', description: '模型名称' },
      { field: 'created_at', type: 'TIMESTAMP', nullable: 'NULL', description: '创建时间' },
      { field: 'updated_at', type: 'TIMESTAMP', nullable: 'NULL', description: '更新时间' },
    ],
    token_launch_predictions: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'launch_probability', type: 'INTEGER', nullable: 'NULL', description: '发币概率(%)' },
      { field: 'estimated_timeline', type: 'VARCHAR(100)', nullable: 'NULL', description: '预计时间' },
      { field: 'confidence', type: 'VARCHAR(20)', nullable: 'NULL', description: '置信度' },
      { field: 'signal_count', type: 'INTEGER', nullable: 'NULL', description: '信号数量' },
    ],
    airdrop_value_estimates: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'estimated_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '估值(美元)' },
      { field: 'estimated_value_cny', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '估值(人民币)' },
      { field: 'min_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '最小值(美元)' },
      { field: 'max_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '最大值(美元)' },
      { field: 'confidence', type: 'VARCHAR(20)', nullable: 'NULL', description: '置信度' },
    ],
    investment_action_plans: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'project_tier', type: 'VARCHAR(1)', nullable: 'NULL', description: '项目等级' },
      { field: 'total_budget', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '总预算(美元)' },
      { field: 'urgency', type: 'VARCHAR(20)', nullable: 'NULL', description: '紧急程度' },
      { field: 'expected_roi', type: 'VARCHAR(50)', nullable: 'NULL', description: '预期回报率' },
      { field: 'total_steps', type: 'INTEGER', nullable: 'NULL', description: '总步骤数' },
    ],
    project_discoveries: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_name', type: 'VARCHAR(255)', nullable: 'NOT NULL', description: '项目名称' },
      { field: 'total_mentions', type: 'INTEGER', nullable: 'NULL', description: '总提及数' },
      { field: 'num_platforms', type: 'INTEGER', nullable: 'NULL', description: '平台数量' },
      { field: 'heat_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '热度分值' },
      { field: 'mentions_24h', type: 'INTEGER', nullable: 'NULL', description: '24小时提及' },
      { field: 'growth_rate', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '增长率' },
      { field: 'is_trending', type: 'BOOLEAN', nullable: 'NULL', description: '是否热门' },
      { field: 'is_surge', type: 'BOOLEAN', nullable: 'NULL', description: '是否暴涨' },
    ],
    projects_pending: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_name', type: 'VARCHAR(255)', nullable: 'NOT NULL', description: '项目名称' },
      { field: 'symbol', type: 'VARCHAR(50)', nullable: 'NULL', description: '代币符号' },
      { field: 'description', type: 'TEXT', nullable: 'NULL', description: '项目描述' },
      { field: 'ai_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: 'AI评分' },
      { field: 'ai_grade', type: 'VARCHAR(1)', nullable: 'NULL', description: 'AI等级 (S/A/B/C)' },
      { field: 'review_status', type: 'VARCHAR(20)', nullable: 'NULL', description: '审核状态' },
    ],
    ai_work_config: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'primary_goal', type: 'TEXT', nullable: 'NULL', description: '主要目标' },
      { field: 'target_roi', type: 'FLOAT', nullable: 'NULL', description: '目标ROI (%)' },
      { field: 'risk_tolerance', type: 'VARCHAR(50)', nullable: 'NULL', description: '风险偏好' },
      { field: 'min_ai_score', type: 'FLOAT', nullable: 'NULL', description: '最低推荐分数' },
      { field: 'max_projects_per_day', type: 'INTEGER', nullable: 'NULL', description: '每日项目上限' },
    ],
    ai_learning_feedback: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'feedback_type', type: 'VARCHAR(50)', nullable: 'NOT NULL', description: '反馈类型' },
      { field: 'user_decision', type: 'VARCHAR(20)', nullable: 'NULL', description: '用户决策' },
      { field: 'reason', type: 'TEXT', nullable: 'NULL', description: '原因说明' },
    ],
    kols: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'twitter_handle', type: 'VARCHAR(100)', nullable: 'NOT NULL', description: 'Twitter用户名' },
      { field: 'followers_count', type: 'INTEGER', nullable: 'NULL', description: '粉丝数' },
      { field: 'tier', type: 'INTEGER', nullable: 'NULL', description: '层级 (1-3)' },
      { field: 'category', type: 'VARCHAR(100)', nullable: 'NULL', description: '分类' },
    ],
    kols_pending: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'twitter_handle', type: 'VARCHAR(100)', nullable: 'NOT NULL', description: 'Twitter用户名' },
      { field: 'ai_score', type: 'FLOAT', nullable: 'NULL', description: 'AI评分' },
      { field: 'review_status', type: 'VARCHAR(20)', nullable: 'NULL', description: '审核状态' },
    ],
    kol_performances: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'kol_id', type: 'INTEGER', nullable: 'NOT NULL', description: 'KOL ID' },
      { field: 'prediction_accuracy', type: 'FLOAT', nullable: 'NULL', description: '预测准确率' },
      { field: 'total_predictions', type: 'INTEGER', nullable: 'NULL', description: '总预测数' },
    ],
    platform_search_rules: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'platform_name', type: 'VARCHAR(50)', nullable: 'NOT NULL', description: '平台名称' },
      { field: 'enabled', type: 'BOOLEAN', nullable: 'NULL', description: '是否启用' },
      { field: 'search_frequency_hours', type: 'INTEGER', nullable: 'NULL', description: '搜索频率(小时)' },
    ],
    twitter_keywords: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'keyword', type: 'VARCHAR(100)', nullable: 'NOT NULL', description: '关键词' },
      { field: 'category', type: 'VARCHAR(50)', nullable: 'NULL', description: '类别' },
      { field: 'priority', type: 'INTEGER', nullable: 'NULL', description: '优先级 (1-3)' },
      { field: 'enabled', type: 'BOOLEAN', nullable: 'NULL', description: '是否启用' },
    ],
    telegram_channels: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'channel_id', type: 'VARCHAR(100)', nullable: 'NOT NULL', description: '频道ID' },
      { field: 'channel_name', type: 'VARCHAR(255)', nullable: 'NULL', description: '频道名称' },
      { field: 'enabled', type: 'BOOLEAN', nullable: 'NULL', description: '是否启用' },
    ],
    discord_servers: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'server_id', type: 'VARCHAR(100)', nullable: 'NOT NULL', description: '服务器ID' },
      { field: 'server_name', type: 'VARCHAR(255)', nullable: 'NULL', description: '服务器名称' },
      { field: 'enabled', type: 'BOOLEAN', nullable: 'NULL', description: '是否启用' },
    ],
    platform_daily_stats: [
      { field: 'id', type: 'SERIAL', nullable: 'NOT NULL', description: '主键' },
      { field: 'platform_name', type: 'VARCHAR(50)', nullable: 'NOT NULL', description: '平台名称' },
      { field: 'date', type: 'DATE', nullable: 'NOT NULL', description: '日期' },
      { field: 'collections', type: 'INTEGER', nullable: 'NULL', description: '采集次数' },
      { field: 'projects_discovered', type: 'INTEGER', nullable: 'NULL', description: '发现项目数' },
    ],
  }

  const currentTab = tabs.find(t => t.id === activeTab)
  const currentStructure = tableStructures[activeTab] || []

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen bg-bg-primary pb-8">
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

        <div className="max-w-7xl mx-auto px-4 py-6">
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 p-6 rounded-xl border border-purple-500/20 hover:border-purple-500/40 transition-colors">
              <div className="text-4xl font-bold text-white">{stats.tableCount}</div>
              <div className="text-sm text-gray-400 mt-2">数据表</div>
            </div>
            <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 p-6 rounded-xl border border-blue-500/20 hover:border-blue-500/40 transition-colors">
              <div className="text-4xl font-bold text-white">{stats.projectCount}</div>
              <div className="text-sm text-gray-400 mt-2">示例项目</div>
            </div>
            <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 p-6 rounded-xl border border-green-500/20 hover:border-green-500/40 transition-colors">
              <div className="text-2xl font-bold text-white">{stats.databaseType}</div>
              <div className="text-sm text-gray-400 mt-2">数据库类型</div>
            </div>
            <div className="bg-gradient-to-br from-orange-500/10 to-red-500/10 p-6 rounded-xl border border-orange-500/20 hover:border-orange-500/40 transition-colors">
              <div className="text-4xl font-bold text-white">{stats.databasePort}</div>
              <div className="text-sm text-gray-400 mt-2">端口</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="bg-bg-tertiary rounded-xl border border-gray-800 overflow-hidden">
            <div className="grid grid-cols-5 gap-2 p-4 border-b border-gray-800">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg transition-all text-sm font-medium ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="p-6">
              {/* Table Info */}
              <div className="bg-gradient-to-br from-purple-500/5 to-pink-500/5 rounded-xl p-6 border border-purple-500/10 mb-6">
                <h3 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
                  {currentTab?.label.split(' ')[0]} {currentTab?.name}
                </h3>
                <p className="text-gray-400 text-sm">{currentTab?.desc}</p>
              </div>

              {/* Table Structure */}
              <div className="bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden">
                <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 px-6 py-4 border-b border-gray-800">
                  <h4 className="text-lg font-bold text-white">表结构</h4>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="bg-gradient-to-r from-purple-500/20 to-pink-500/20">
                        <th className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider">
                          字段名
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider">
                          类型
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider">
                          可空
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider">
                          说明
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                      {currentStructure.map((field, idx) => (
                        <tr key={idx} className="hover:bg-gray-800/50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <code className="text-sm font-mono text-cyan-400">{field.field}</code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <code className="text-sm font-mono text-blue-400">{field.type}</code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`text-xs px-2 py-1 rounded ${
                              field.nullable === 'NOT NULL' 
                                ? 'bg-red-500/20 text-red-400' 
                                : 'bg-green-500/20 text-green-400'
                            }`}>
                              {field.nullable}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-300">
                            {field.description}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Table Data */}
              <div className="mt-6 bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden">
                <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 px-6 py-4 border-b border-gray-800 flex items-center justify-between">
                  <h4 className="text-lg font-bold text-white">示例数据</h4>
                  {tableData && (
                    <div className="text-sm text-gray-400">
                      显示 1-{Math.min(pageSize, tableData.total)} 条，共 {tableData.total} 条
                    </div>
                  )}
                </div>

                {loading ? (
                  <div className="p-12 text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                    <p className="mt-4 text-gray-400">加载中...</p>
                  </div>
                ) : tableData && tableData.rows.length > 0 ? (
                  <>
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="bg-gradient-to-r from-purple-500/10 to-pink-500/10">
                            {tableData.columns.map((col, idx) => (
                              <th key={idx} className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider whitespace-nowrap">
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800">
                          {tableData.rows.map((row, rowIdx) => (
                            <tr key={rowIdx} className="hover:bg-gray-800/50 transition-colors">
                              {tableData.columns.map((col, colIdx) => (
                                <td key={colIdx} className="px-6 py-4 text-sm text-gray-300 max-w-xs truncate">
                                  {row[col] !== null && row[col] !== undefined ? (
                                    typeof row[col] === 'object' ? (
                                      <code className="text-xs text-cyan-400">{JSON.stringify(row[col])}</code>
                                    ) : typeof row[col] === 'boolean' ? (
                                      <span className={`px-2 py-1 rounded text-xs ${row[col] ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                        {row[col] ? 'true' : 'false'}
                                      </span>
                                    ) : (
                                      String(row[col])
                                    )
                                  ) : (
                                    <span className="text-gray-600 italic">NULL</span>
                                  )}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {/* Pagination */}
                    <div className="bg-gray-900/80 px-6 py-4 border-t border-gray-800 flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-400">每页显示:</span>
                        <select
                          value={pageSize}
                          onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                          className="bg-gray-800 border border-gray-700 rounded px-3 py-1 text-sm text-white focus:outline-none focus:border-purple-500"
                        >
                          <option value={20}>20</option>
                          <option value={50}>50</option>
                        </select>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handlePageChange(1)}
                          disabled={currentPage === 1}
                          className="px-3 py-1 bg-gray-800 text-white rounded hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                        >
                          « 上一页
                        </button>

                        <div className="flex gap-1">
                          {Array.from({ length: Math.min(tableData.total_pages, 5) }, (_, i) => {
                            let pageNum;
                            if (tableData.total_pages <= 5) {
                              pageNum = i + 1;
                            } else if (currentPage <= 3) {
                              pageNum = i + 1;
                            } else if (currentPage >= tableData.total_pages - 2) {
                              pageNum = tableData.total_pages - 4 + i;
                            } else {
                              pageNum = currentPage - 2 + i;
                            }
                            
                            return (
                              <button
                                key={i}
                                onClick={() => handlePageChange(pageNum)}
                                className={`px-3 py-1 rounded text-sm ${
                                  currentPage === pageNum
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                                    : 'bg-gray-800 text-white hover:bg-gray-700'
                                }`}
                              >
                                {pageNum}
                              </button>
                            );
                          })}
                        </div>

                        <button
                          onClick={() => handlePageChange(currentPage + 1)}
                          disabled={currentPage >= tableData.total_pages}
                          className="px-3 py-1 bg-gray-800 text-white rounded hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                        >
                          下一页 »
                        </button>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="p-12 text-center">
                    <div className="text-6xl mb-4">📭</div>
                    <p className="text-gray-400">暂无数据</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}