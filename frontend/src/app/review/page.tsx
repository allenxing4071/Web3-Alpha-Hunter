/**
 * AI项目审核面板
 * 用户查看AI推荐的项目并批准/拒绝
 */

"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { AuthGuard } from '@/components/AuthGuard'

interface PendingProject {
  id: number
  name: string
  symbol: string
  description: string
  discovered_from: string
  source_url: string
  ai_score: number
  ai_grade: string
  ai_recommendation_reason: any
  ai_confidence: number
  review_status: string
  created_at: string
}

export default function ReviewPage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  
  const [projects, setProjects] = useState<PendingProject[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<any>({})
  const [filter, setFilter] = useState<'pending' | 'all'>('pending')
  const [selectedProject, setSelectedProject] = useState<PendingProject | null>(null)
  const [rejectReason, setRejectReason] = useState('')

  // 加载待审核项目
  const loadProjects = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/admin/pending-projects?limit=50`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setProjects(data.projects)
          setStats(data.stats)
        }
      }
    } catch (error) {
      console.error('加载项目失败', error)
    } finally {
      setLoading(false)
    }
  }

  // 批准项目
  const approveProject = async (projectId: number) => {
    try {
      const response = await fetch(`${API_URL}/admin/pending-projects/${projectId}/approve`, {
        method: 'POST'
      })
      
      if (response.ok) {
        alert('✅ 项目已批准！')
        loadProjects()
        setSelectedProject(null)
      } else {
        alert('❌ 批准失败')
      }
    } catch (error) {
      alert('❌ 批准失败')
    }
  }

  // 拒绝项目
  const rejectProject = async (projectId: number, reason: string) => {
    try {
      const response = await fetch(`${API_URL}/admin/pending-projects/${projectId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason })
      })
      
      if (response.ok) {
        alert('✅ 项目已拒绝')
        loadProjects()
        setSelectedProject(null)
        setRejectReason('')
      } else {
        alert('❌ 拒绝失败')
      }
    } catch (error) {
      alert('❌ 拒绝失败')
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen p-8">
        <div className="max-w-7xl mx-auto">
          {/* 页面标题 */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
                🎯 AI项目审核面板
              </h1>
              <p className="text-text-secondary">
                AI智能助理为您精选的优质项目，等待您的审核确认
              </p>
            </div>
            <button
              onClick={loadProjects}
              disabled={loading}
              className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? '⏳ 加载中...' : '🔄 刷新'}
            </button>
          </div>

          {/* 统计卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="bg-gradient-to-br from-yellow-900/30 to-yellow-800/20 border-yellow-600">
              <CardHeader>
                <CardTitle className="text-base text-yellow-400">待审核</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-white">{stats.pending || 0}</div>
                <p className="text-xs text-gray-400 mt-1">个项目</p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-900/30 to-green-800/20 border-green-600">
              <CardHeader>
                <CardTitle className="text-base text-green-400">已批准</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-white">{stats.approved || 0}</div>
                <p className="text-xs text-gray-400 mt-1">个项目</p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-red-900/30 to-red-800/20 border-red-600">
              <CardHeader>
                <CardTitle className="text-base text-red-400">已拒绝</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-white">{stats.rejected || 0}</div>
                <p className="text-xs text-gray-400 mt-1">个项目</p>
              </CardContent>
            </Card>

            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle className="text-base text-gray-400">总计</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-white">
                  {(stats.pending || 0) + (stats.approved || 0) + (stats.rejected || 0)}
                </div>
                <p className="text-xs text-gray-400 mt-1">个项目</p>
              </CardContent>
            </Card>
          </div>

          {/* 筛选按钮 */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setFilter('pending')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filter === 'pending'
                  ? 'bg-accent-primary text-white'
                  : 'bg-bg-tertiary text-text-secondary hover:bg-bg-secondary'
              }`}
            >
              待审核 ({stats.pending || 0})
            </button>
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filter === 'all'
                  ? 'bg-accent-primary text-white'
                  : 'bg-bg-tertiary text-text-secondary hover:bg-bg-secondary'
              }`}
            >
              全部
            </button>
          </div>

          {/* 项目列表 */}
          {loading ? (
            <div className="text-center py-16">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
              <p className="text-text-secondary">加载项目中...</p>
            </div>
          ) : projects.length === 0 ? (
            <Card className="bg-bg-tertiary border-gray-700">
              <CardContent className="text-center py-16">
                <div className="text-6xl mb-4">🎉</div>
                <h3 className="text-xl font-bold text-white mb-2">暂无待审核项目</h3>
                <p className="text-text-secondary">AI智能助理正在为您发现新项目...</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 gap-6">
              {projects.map((project) => (
                <Card key={project.id} className="bg-bg-tertiary border-gray-700 hover:border-accent-primary/50 transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-2xl font-bold text-white">{project.name}</h3>
                          {project.symbol && (
                            <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-sm rounded">
                              ${project.symbol}
                            </span>
                          )}
                          <span className={`px-2 py-1 text-xs rounded font-bold ${
                            project.ai_grade === 'S' ? 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white' :
                            project.ai_grade === 'A' ? 'bg-green-500/20 text-green-400' :
                            project.ai_grade === 'B' ? 'bg-blue-500/20 text-blue-400' :
                            'bg-gray-500/20 text-gray-400'
                          }`}>
                            {project.ai_grade} 级
                          </span>
                        </div>
                        <p className="text-text-secondary mb-3">{project.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-400">
                          <span>🔍 发现于: {project.discovered_from}</span>
                          <span>📅 {new Date(project.created_at).toLocaleDateString('zh-CN')}</span>
                          <span>🤖 AI置信度: {(project.ai_confidence * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <div className="text-right">
                          <div className="text-3xl font-bold text-accent-primary">{project.ai_score.toFixed(1)}</div>
                          <div className="text-xs text-gray-400">AI评分</div>
                        </div>
                      </div>
                    </div>

                    {/* AI推荐理由 */}
                    {project.ai_recommendation_reason && (
                      <div className="bg-bg-secondary rounded-lg p-4 mb-4">
                        <h4 className="text-sm font-semibold text-white mb-2">🤖 AI推荐理由：</h4>
                        <ul className="space-y-1 text-sm text-text-secondary mb-3">
                          {Array.isArray(project.ai_recommendation_reason.reasons) ? (
                            project.ai_recommendation_reason.reasons.map((reason: string, idx: number) => (
                              <li key={idx} className="flex items-start gap-2">
                                <span className="text-accent-primary">•</span>
                                <span>{reason}</span>
                              </li>
                            ))
                          ) : (
                            <li>完整的AI分析报告</li>
                          )}
                        </ul>
                        
                        {/* 评分详情 */}
                        {project.ai_recommendation_reason.scores && (
                          <div className="border-t border-gray-700 pt-3 mt-3">
                            <h5 className="text-xs text-gray-400 mb-2">📊 评分详情：</h5>
                            <div className="grid grid-cols-3 gap-2 text-xs">
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">团队</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.team}</span>
                              </div>
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">技术</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.tech}</span>
                              </div>
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">社区</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.community}</span>
                              </div>
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">代币</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.tokenomics}</span>
                              </div>
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">市场</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.market}</span>
                              </div>
                              <div className="flex items-center justify-between bg-bg-primary rounded px-2 py-1">
                                <span className="text-gray-400">风险</span>
                                <span className="text-white font-semibold">{project.ai_recommendation_reason.scores.risk}</span>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* 来源链接 */}
                    {project.source_url && (
                      <div className="mb-4">
                        <a
                          href={project.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-accent-primary hover:text-accent-secondary transition-colors"
                        >
                          🔗 查看原始来源 →
                        </a>
                      </div>
                    )}

                    {/* 操作按钮 */}
                    <div className="flex gap-3">
                      <button
                        onClick={() => approveProject(project.id)}
                        className="flex-1 px-6 py-3 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-700 hover:to-green-600 text-white rounded-lg transition-all font-semibold"
                      >
                        ✓ 批准项目
                      </button>
                      <button
                        onClick={() => setSelectedProject(project)}
                        className="flex-1 px-6 py-3 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white rounded-lg transition-all font-semibold"
                      >
                        ✗ 拒绝项目
                      </button>
                      <button
                        className="px-6 py-3 bg-bg-secondary hover:bg-gray-700 text-white rounded-lg transition-colors"
                      >
                        稍后决定
                      </button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* 拒绝理由弹窗 */}
          {selectedProject && (
            <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
              <Card className="bg-bg-tertiary border-gray-700 max-w-md w-full">
                <CardHeader>
                  <CardTitle>拒绝项目：{selectedProject.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm text-gray-400 mb-2">请说明拒绝理由（可选）</label>
                      <textarea
                        value={rejectReason}
                        onChange={(e) => setRejectReason(e.target.value)}
                        placeholder="例如：项目描述不清晰、团队背景不明、技术创新不足..."
                        className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white placeholder-gray-500 h-24 resize-none focus:outline-none focus:border-accent-primary"
                      />
                    </div>
                    <div className="flex gap-3">
                      <button
                        onClick={() => rejectProject(selectedProject.id, rejectReason)}
                        className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                      >
                        确认拒绝
                      </button>
                      <button
                        onClick={() => {
                          setSelectedProject(null)
                          setRejectReason('')
                        }}
                        className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
                      >
                        取消
                      </button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </AuthGuard>
  )
}

