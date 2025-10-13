"use client"

import { useState, useEffect } from 'react'
import { AuthGuard } from '@/components/AuthGuard'
import { API_BASE_URL } from '@/lib/config'

interface DatabaseStats {
  tableCount: number
  projectCount: number
  databaseType: string
  databasePort: number
}

interface TableStructure {
  name: string
  type: string
  nullable: boolean
  default: string | null
  description: string
}

interface TableInfo {
  table_name: string
  columns: TableStructure[]
  indexes: any[]
  foreign_keys: any[]
  row_count: number
}

interface TableData {
  table_name: string
  columns: string[]
  rows: any[]
  total: number
  page: number
  limit: number
  total_pages: number
}

export default function DatabasePage() {
  const [activeTab, setActiveTab] = useState('projects')
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [tableData, setTableData] = useState<TableData | null>(null)
  const [tableInfo, setTableInfo] = useState<TableInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [availableTables, setAvailableTables] = useState<string[]>([])
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
    loadTableInfo()
    loadTableData()
  }, [activeTab, currentPage, pageSize])

  const loadDatabaseStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/database/stats`)
      const result = await response.json()
      if (result.success) {
        setStats({
          tableCount: result.data.table_count,
          projectCount: result.data.project_count,
          databaseType: result.data.database_type,
          databasePort: result.data.database_port
        })
        // 设置可用表列表
        setAvailableTables(result.data.tables || [])
      }
    } catch (error) {
      console.error('加载数据库统计失败:', error)
    }
  }

  const loadTableInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/database/tables/${activeTab}/info`)
      const result = await response.json()
      if (result.success) {
        setTableInfo(result.data)
      } else {
        setTableInfo(null)
      }
    } catch (error) {
      console.error('加载表结构失败:', error)
      setTableInfo(null)
    }
  }

  const loadTableData = async () => {
    setLoading(true)
    try {
      const response = await fetch(
        `${API_BASE_URL}/database/tables/${activeTab}/data?page=${currentPage}&limit=${pageSize}`
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

  // 表分类定义
  const tableCategories = {
    core: {
      name: '核心表',
      emoji: '⭐',
      tables: ['projects', 'social_metrics', 'onchain_metrics', 'ai_analysis']
    },
    aiConfig: {
      name: 'AI配置表',
      emoji: '⚙️',
      tables: ['ai_configs', 'ai_work_config', 'ai_learning_feedback']
    },
    prediction: {
      name: '预测表',
      emoji: '🔮',
      tables: ['token_launch_predictions', 'airdrop_value_estimates', 'investment_action_plans']
    },
    discovery: {
      name: '发现表',
      emoji: '🔍',
      tables: ['project_discoveries', 'projects_pending']
    },
    kol: {
      name: 'KOL表',
      emoji: '👥',
      tables: ['kols', 'kols_pending', 'kol_performances']
    },
    platform: {
      name: '平台监控表',
      emoji: '🌐',
      tables: ['platform_search_rules', 'platform_daily_stats', 'twitter_keywords', 'telegram_channels', 'discord_servers']
    },
    system: {
      name: '系统表',
      emoji: '🔐',
      tables: ['users']
    }
  }

  // 表名映射（emoji和描述）
  const tableMetadata: Record<string, { emoji: string; desc: string; name: string; category: string }> = {
    'projects': { emoji: '📊', desc: '存储Web3项目的完整数据库', name: '项目表', category: 'core' },
    'social_metrics': { emoji: '📱', desc: '社交媒体数据指标', name: '社交指标', category: 'core' },
    'onchain_metrics': { emoji: '⛓️', desc: '区块链上的实际数据', name: '链上数据', category: 'core' },
    'ai_analysis': { emoji: '🤖', desc: 'AI智能分析结果', name: 'AI分析', category: 'core' },
    'ai_configs': { emoji: '🔑', desc: 'AI模型配置', name: 'AI配置', category: 'aiConfig' },
    'ai_work_config': { emoji: '🧠', desc: 'AI智能助理工作参数', name: 'AI工作配置', category: 'aiConfig' },
    'ai_learning_feedback': { emoji: '📚', desc: 'AI学习反馈记录', name: 'AI学习反馈', category: 'aiConfig' },
    'platform_search_rules': { emoji: '🔍', desc: '平台搜索规则配置', name: '平台规则', category: 'platform' },
    'token_launch_predictions': { emoji: '🚀', desc: '代币发行预测', name: '发币预测', category: 'prediction' },
    'airdrop_value_estimates': { emoji: '💰', desc: '空投价值估算', name: '空投估值', category: 'prediction' },
    'investment_action_plans': { emoji: '📋', desc: 'AI生成的投资行动计划', name: '投资计划', category: 'prediction' },
    'project_discoveries': { emoji: '🔭', desc: '多平台项目热度追踪', name: '项目发现', category: 'discovery' },
    'projects_pending': { emoji: '⏳', desc: 'AI推荐的待审核项目', name: '待审核项目', category: 'discovery' },
    'kols': { emoji: '👤', desc: 'KOL数据和表现追踪', name: 'KOL列表', category: 'kol' },
    'kols_pending': { emoji: '⏰', desc: 'AI推荐的待审核KOL', name: '待审核KOL', category: 'kol' },
    'kol_performances': { emoji: '📈', desc: 'KOL历史表现追踪', name: 'KOL表现', category: 'kol' },
    'twitter_keywords': { emoji: '🐦', desc: 'Twitter搜索关键词库', name: 'Twitter关键词', category: 'platform' },
    'telegram_channels': { emoji: '💬', desc: 'Telegram监控频道列表', name: 'Telegram频道', category: 'platform' },
    'discord_servers': { emoji: '🎮', desc: 'Discord监控服务器列表', name: 'Discord服务器', category: 'platform' },
    'platform_daily_stats': { emoji: '📊', desc: '平台每日数据统计', name: '平台统计', category: 'platform' },
    'users': { emoji: '👥', desc: '系统用户权限管理', name: '用户表', category: 'system' },
  }

  // 按分类组织表
  const groupedTables = Object.entries(tableCategories).map(([key, category]) => ({
    key,
    name: category.name,
    emoji: category.emoji,
    tables: availableTables
      .filter(tableName => category.tables.includes(tableName))
      .map(tableName => {
        const meta = tableMetadata[tableName] || { emoji: '📄', desc: '数据表', name: tableName, category: 'other' }
        return {
          id: tableName,
          label: `${meta.emoji} ${tableName}`,
          name: `${tableName} (${meta.name})`,
          desc: meta.desc
        }
      })
  })).filter(group => group.tables.length > 0)

  const currentTableMeta = tableMetadata[activeTab]

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen bg-bg-primary p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              🗄️ 数据库管理
            </h1>
            <p className="text-text-secondary">
              查看和管理系统数据库表结构与数据
            </p>
          </div>

          <div>
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 hover:border-accent-primary transition-all">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-text-secondary text-sm font-medium">数据表</h3>
                <span className="text-2xl">📊</span>
              </div>
              <div className="text-3xl font-bold text-accent-primary mb-2">{stats.tableCount}</div>
              <p className="text-text-tertiary text-xs">系统表总数</p>
            </div>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 hover:border-success transition-all">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-text-secondary text-sm font-medium">示例项目</h3>
                <span className="text-2xl">📋</span>
              </div>
              <div className="text-3xl font-bold text-success mb-2">{stats.projectCount}</div>
              <p className="text-text-tertiary text-xs">数据行数</p>
            </div>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 hover:border-info transition-all">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-text-secondary text-sm font-medium">数据库类型</h3>
                <span className="text-2xl">🗄️</span>
              </div>
              <div className="text-xl font-bold text-info mb-2">{stats.databaseType}</div>
              <p className="text-text-tertiary text-xs">当前使用</p>
            </div>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 hover:border-warning transition-all">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-text-secondary text-sm font-medium">端口</h3>
                <span className="text-2xl">🔌</span>
              </div>
              <div className="text-3xl font-bold text-warning mb-2">{stats.databasePort}</div>
              <p className="text-text-tertiary text-xs">监听端口</p>
            </div>
          </div>

          {/* Tabs - 分类显示 */}
          <div className="bg-bg-tertiary rounded-lg border border-gray-700 overflow-hidden">
            <div className="p-4 border-b border-gray-700 max-h-96 overflow-y-auto space-y-4">
              {groupedTables.map(group => (
                <div key={group.key} className="space-y-2">
                  {/* 分类标题 */}
                  <div className="flex items-center gap-2 px-2">
                    <span className="text-lg">{group.emoji}</span>
                    <h3 className="text-sm font-bold text-purple-300">{group.name}</h3>
                    <span className="text-xs text-gray-500">({group.tables.length}个表)</span>
                  </div>
                  
                  {/* 该分类下的表 */}
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-2">
                    {group.tables.map(tab => (
                <button
                  key={tab.id}
                        onClick={() => {
                          setActiveTab(tab.id)
                          setCurrentPage(1)
                        }}
                        className={`px-3 py-2 rounded-lg transition-all text-xs font-medium truncate ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-300'
                  }`}
                        title={tab.name}
                >
                  {tab.label}
                </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Content */}
            <div className="p-6">
              {/* Table Info */}
              <div className="bg-gradient-to-br from-purple-500/5 to-pink-500/5 rounded-xl p-6 border border-purple-500/10 mb-6">
                <div className="flex items-center gap-3 mb-2">
                  {currentTableMeta && (
                    <>
                      <span className="text-3xl">{currentTableMeta.emoji}</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="text-2xl font-bold text-white">{activeTab}</h3>
                          <span className="text-sm text-gray-400">({currentTableMeta.name})</span>
                          {currentTableMeta.category && (
                            <span className="px-2 py-1 bg-purple-500/20 text-purple-300 rounded text-xs">
                              {tableCategories[currentTableMeta.category as keyof typeof tableCategories]?.emoji} {tableCategories[currentTableMeta.category as keyof typeof tableCategories]?.name}
                            </span>
                          )}
                        </div>
                        <p className="text-gray-400 text-sm mt-1">{currentTableMeta.desc}</p>
                      </div>
                    </>
                  )}
                </div>
              </div>

              {/* Table Structure */}
              <div className="bg-bg-secondary rounded-lg border border-gray-700 overflow-hidden">
                <div className="bg-bg-tertiary px-6 py-4 border-b border-gray-700 flex items-center justify-between">
                  <h4 className="text-lg font-bold text-white">表结构</h4>
                  {tableInfo && (
                    <span className="text-sm text-gray-400">
                      共 {tableInfo.columns.length} 个字段，{tableInfo.row_count} 行数据
                    </span>
                  )}
                </div>
                {tableInfo ? (
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
                            默认值
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-bold text-purple-300 uppercase tracking-wider">
                          说明
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                        {tableInfo.columns.map((field, idx) => (
                        <tr key={idx} className="hover:bg-gray-800/50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap">
                              <code className="text-sm font-mono text-cyan-400">{field.name}</code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <code className="text-sm font-mono text-blue-400">{field.type}</code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`text-xs px-2 py-1 rounded ${
                                !field.nullable
                                ? 'bg-red-500/20 text-red-400' 
                                : 'bg-green-500/20 text-green-400'
                            }`}>
                                {field.nullable ? 'NULL' : 'NOT NULL'}
                            </span>
                          </td>
                            <td className="px-6 py-4 text-sm text-gray-300 max-w-xs truncate">
                              {field.default ? (
                                <code className="text-xs text-yellow-400">{field.default}</code>
                              ) : (
                                <span className="text-gray-600 italic">-</span>
                              )}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-300">
                              <span className="text-purple-300">{field.description}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                ) : (
                  <div className="p-12 text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                    <p className="mt-4 text-gray-400">加载表结构...</p>
                  </div>
                )}
              </div>

              {/* Table Data */}
              <div className="mt-6 bg-bg-secondary rounded-lg border border-gray-700 overflow-hidden">
                <div className="bg-bg-tertiary px-6 py-4 border-b border-gray-700 flex items-center justify-between">
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
                    <div className="bg-bg-tertiary px-6 py-4 border-t border-gray-700 flex items-center justify-between">
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
      </div>
    </AuthGuard>
  )
}