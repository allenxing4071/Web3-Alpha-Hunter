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
    { id: 'projects', label: '📊 Projects', name: 'Projects - 项目主表', desc: '存储Web3项目的完整数据库，评分集结仓' },
    { id: 'social', label: '📱 Social Metrics', name: 'Social Metrics (社交指标)', desc: '社交媒体数据指标' },
    { id: 'onchain', label: '⛓️ Onchain Metrics', name: 'Onchain Metrics (链上数据)', desc: '区块链上的实际数据' },
    { id: 'ai', label: '🤖 AI Analysis', name: 'AI Analysis (AI分析)', desc: 'AI智能分析结果' },
    { id: 'aiconfig', label: '🔑 AI Configs', name: 'AI Configs (AI配置)', desc: 'AI模型配置' },
    { id: 'tokenlaunch', label: '🚀 Token Launch', name: 'Token Launch Predictions (发币预测)', desc: '代币发行预测' },
    { id: 'airdrop', label: '💰 Airdrop', name: 'Airdrop Value Estimates (空投估算)', desc: '空投价值估算' },
    { id: 'investment', label: '📋 Investment', name: 'Investment Action Plans (行动计划)', desc: '投资行动计划' },
    { id: 'discovery', label: '🔍 Discovery', name: 'Project Discoveries (项目发现)', desc: '多平台项目热度追踪' },
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
    social: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'twitter_followers', type: 'INTEGER', nullable: 'NULL', description: 'Twitter粉丝数' },
      { field: 'telegram_members', type: 'INTEGER', nullable: 'NULL', description: 'Telegram成员数' },
      { field: 'discord_members', type: 'INTEGER', nullable: 'NULL', description: 'Discord成员数' },
      { field: 'github_stars', type: 'INTEGER', nullable: 'NULL', description: 'GitHub Star数' },
      { field: 'social_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '社交分值' },
    ],
    onchain: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'market_cap_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '市值(美元)' },
      { field: 'volume_24h_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '24小时交易量' },
      { field: 'tvl_usd', type: 'DECIMAL(20,2)', nullable: 'NULL', description: '锁仓量TVL' },
      { field: 'active_users_24h', type: 'INTEGER', nullable: 'NULL', description: '24小时活跃用户' },
      { field: 'onchain_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '链上分值' },
    ],
    ai: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'sentiment_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '情感分值' },
      { field: 'risk_level', type: 'VARCHAR(20)', nullable: 'NULL', description: '风险等级' },
      { field: 'innovation_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '创新分值' },
      { field: 'team_score', type: 'DECIMAL(5,2)', nullable: 'NULL', description: '团队分值' },
      { field: 'summary', type: 'TEXT', nullable: 'NULL', description: 'AI总结' },
    ],
    aiconfig: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'provider', type: 'VARCHAR(50)', nullable: 'NOT NULL', description: '提供商(openai/claude)' },
      { field: 'api_key', type: 'VARCHAR(255)', nullable: 'NOT NULL', description: 'API密钥' },
      { field: 'model_name', type: 'VARCHAR(100)', nullable: 'NULL', description: '模型名称' },
      { field: 'base_url', type: 'VARCHAR(255)', nullable: 'NULL', description: 'API基础URL' },
      { field: 'is_active', type: 'BOOLEAN', nullable: 'NULL', description: '是否激活' },
    ],
    tokenlaunch: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'launch_probability', type: 'INTEGER', nullable: 'NULL', description: '发币概率(%)' },
      { field: 'estimated_timeline', type: 'VARCHAR(100)', nullable: 'NULL', description: '预计时间' },
      { field: 'confidence', type: 'VARCHAR(20)', nullable: 'NULL', description: '置信度' },
      { field: 'signal_count', type: 'INTEGER', nullable: 'NULL', description: '信号数量' },
    ],
    airdrop: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'estimated_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '估值(美元)' },
      { field: 'estimated_value_cny', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '估值(人民币)' },
      { field: 'min_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '最小值(美元)' },
      { field: 'max_value_usd', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '最大值(美元)' },
      { field: 'confidence', type: 'VARCHAR(20)', nullable: 'NULL', description: '置信度' },
    ],
    investment: [
      { field: 'id', type: 'INTEGER', nullable: 'NOT NULL', description: '主键' },
      { field: 'project_id', type: 'INTEGER', nullable: 'NOT NULL', description: '项目ID' },
      { field: 'project_tier', type: 'VARCHAR(1)', nullable: 'NULL', description: '项目等级' },
      { field: 'total_budget', type: 'DECIMAL(10,2)', nullable: 'NULL', description: '总预算(美元)' },
      { field: 'urgency', type: 'VARCHAR(20)', nullable: 'NULL', description: '紧急程度' },
      { field: 'expected_roi', type: 'VARCHAR(50)', nullable: 'NULL', description: '预期回报率' },
      { field: 'total_steps', type: 'INTEGER', nullable: 'NULL', description: '总步骤数' },
    ],
    discovery: [
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
            <div className="flex gap-2 p-4 border-b border-gray-800 overflow-x-auto">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all text-sm font-medium ${
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

              {/* Sample Data Info */}
              <div className="mt-6 bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">💡</span>
                  <div>
                    <h5 className="font-bold text-blue-400 mb-1">提示</h5>
                    <p className="text-sm text-gray-400">
                      当前显示的是 <code className="px-2 py-1 bg-gray-800 rounded text-cyan-400 font-mono text-xs">{activeTab}</code> 表的结构信息。
                      完整的数据查询和管理功能正在开发中...
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