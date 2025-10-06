/**
 * 系统管理后台 - AI智能助理控制中心
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { AuthGuard } from '@/components/AuthGuard'

interface Platform {
  id: string
  name: string
  enabled: boolean
  priority: number
  frequency_minutes: number
  search_keywords: any[]
  min_engagement: number
  min_author_followers: number
  max_results_per_run: number
  today_collected: number
  today_projects: number
  today_kols: number
  today_recommended: number
  last_collected_at: string | null
}

interface AIConfig {
  name: string
  key: string
  enabled: boolean
  model: string
  testing?: boolean
  testResult?: 'success' | 'error' | null
}

interface AIWorkConfig {
  primary_goal: string
  target_roi: number
  risk_tolerance: string
  min_ai_score: number
  required_cross_validation: boolean
  min_platforms: number
  search_lookback_hours: number
  project_age_limit_days: number
  max_projects_per_day: number
  max_kols_per_day: number
  rules: any
}

export default function AdminPage() {
  const router = useRouter()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  
  // Celery状态
  const [celeryRunning, setCeleryRunning] = useState(false)
  const [beatRunning, setBeatRunning] = useState(false)
  
  // 平台数据
  const [platforms, setPlatforms] = useState<Platform[]>([])
  const [loadingPlatforms, setLoadingPlatforms] = useState(true)
  
  // AI配置
  const [aiConfigs, setAiConfigs] = useState<AIConfig[]>([
    { name: 'DeepSeek', key: '', enabled: false, model: 'deepseek-chat' },
    { name: 'Claude', key: '', enabled: false, model: 'claude-3-haiku-20240307' },
    { name: 'OpenAI', key: '', enabled: false, model: 'gpt-3.5-turbo' },
  ])
  const [showAiConfig, setShowAiConfig] = useState(false)
  const [showKeys, setShowKeys] = useState<{[key: number]: boolean}>({})
  
  // AI工作配置
  const [aiWorkConfig, setAiWorkConfig] = useState<AIWorkConfig | null>(null)
  const [showAiWorkConfig, setShowAiWorkConfig] = useState(false)
  
  // 日志
  const [logs, setLogs] = useState<string[]>([
    '[系统] AI智能助理控制中心已启动',
    '[提示] 系统正在加载平台配置...',
  ])

  // 添加日志
  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString('zh-CN')
    setLogs(prev => [`[${timestamp}] ${message}`, ...prev].slice(0, 50))
  }

  // 检查Celery状态
  const checkCeleryStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/celery-status`)
      if (response.ok) {
        const data = await response.json()
        setCeleryRunning(data.worker_running)
        setBeatRunning(data.beat_running)
      }
    } catch (error) {
      setCeleryRunning(false)
      setBeatRunning(false)
    }
  }

  // 加载平台列表
  const loadPlatforms = async () => {
    try {
      setLoadingPlatforms(true)
      const response = await fetch(`${API_URL}/platforms/`)
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.platforms) {
          setPlatforms(data.platforms)
          addLog(`[平台] 成功加载${data.platforms.length}个平台配置`)
        }
      }
    } catch (error) {
      addLog('[错误] 平台配置加载失败')
    } finally {
      setLoadingPlatforms(false)
    }
  }

  // 切换平台启用状态
  const togglePlatform = async (platformId: string, enabled: boolean) => {
    try {
      const response = await fetch(`${API_URL}/platforms/${platformId}/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled })
      })
      
      if (response.ok) {
        addLog(`[平台] ${platformId} ${enabled ? '已启用' : '已停用'}`)
        loadPlatforms()
      }
    } catch (error) {
      addLog(`[错误] ${platformId} 状态切换失败`)
    }
  }

  // 手动触发平台采集
  const triggerPlatformCollection = async (platformId: string) => {
    try {
      addLog(`[采集] 正在触发 ${platformId} 数据采集...`)
      const response = await fetch(`${API_URL}/platforms/${platformId}/collect`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const data = await response.json()
        addLog(`[成功] ${platformId} 采集任务已提交: ${data.task_id}`)
      }
    } catch (error) {
      addLog(`[错误] ${platformId} 采集触发失败`)
    }
  }

  // 加载AI配置
  const loadAiConfigs = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ai-configs`)
      if (response.ok) {
        const data = await response.json()
        if (data.configs && data.configs.length > 0) {
          setAiConfigs(data.configs)
          addLog('[AI配置] 已从数据库加载')
        }
      }
    } catch (error) {
      // Fallback to localStorage
      const saved = localStorage.getItem('ai-configs')
      if (saved) {
        setAiConfigs(JSON.parse(saved))
        addLog('[AI配置] 已从本地缓存加载')
      }
    }
  }

  // 加载AI工作配置
  const loadAiWorkConfig = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ai-work-config`)
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.config) {
          setAiWorkConfig(data.config)
          addLog('[AI配置] 工作配置已加载')
        }
      }
    } catch (error) {
      addLog('[错误] AI工作配置加载失败')
    }
  }

  // 保存AI工作配置
  const saveAiWorkConfig = async () => {
    if (!aiWorkConfig) return
    
    try {
      const response = await fetch(`${API_URL}/admin/ai-work-config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(aiWorkConfig)
      })
      
      if (response.ok) {
        addLog('[AI配置] 工作配置已保存')
        alert('✅ 配置已保存')
      }
    } catch (error) {
      addLog('[错误] AI工作配置保存失败')
    }
  }

  // 测试AI连接
  const testAiConnection = async (index: number) => {
    const config = aiConfigs[index]
    if (!config.key) {
      addLog(`[AI测试] ${config.name} - 请先配置API密钥`)
      return
    }

    const newConfigs = [...aiConfigs]
    newConfigs[index].testing = true
    newConfigs[index].testResult = null
    setAiConfigs(newConfigs)

    addLog(`[AI测试] 正在测试 ${config.name} 连接...`)

    try {
      const response = await fetch(`${API_URL}/admin/test-ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider: config.name.toLowerCase(),
          api_key: config.key,
          model: config.model
        })
      })

      const data = await response.json()

      newConfigs[index].testing = false
      if (response.ok && data.success) {
        newConfigs[index].testResult = 'success'
        addLog(`[AI测试] ✅ ${config.name} 连接成功`)
      } else {
        newConfigs[index].testResult = 'error'
        addLog(`[AI测试] ❌ ${config.name} 连接失败`)
      }
    } catch (error) {
      newConfigs[index].testing = false
      newConfigs[index].testResult = 'error'
      addLog(`[AI测试] ❌ ${config.name} 网络错误`)
    }

    setAiConfigs(newConfigs)
  }

  // 保存AI配置到数据库
  const saveAiConfigs = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ai-configs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ configs: aiConfigs })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        addLog(`[AI配置] ✅ 已保存到数据库 (${data.saved_count}个)`)
        alert('✅ 配置已成功保存到数据库！')
        return true
      } else {
        addLog('[AI配置] ❌ 保存失败')
        alert('❌ 保存失败')
        return false
      }
    } catch (error) {
      addLog('[AI配置] ⚠️ 保存失败')
      alert('❌ 保存失败')
      return false
    }
  }

  // 初始化
  useEffect(() => {
    checkCeleryStatus()
    loadPlatforms()
    loadAiConfigs()
    loadAiWorkConfig()
    const interval = setInterval(checkCeleryStatus, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen p-8">
        <div className="max-w-7xl mx-auto">
          {/* 页面标题 */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              🤖 AI智能助理控制中心
            </h1>
            <p className="text-text-secondary">
              Web3 Alpha Hunter - 自主运行 · 智能学习 · 精准推荐
            </p>
          </div>

          {/* AI模型配置（保持原有功能） */}
          <Card className="bg-bg-tertiary border-gray-700 mb-8">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl flex items-center gap-2">
                  🤖 AI模型配置
                </CardTitle>
                <button
                  onClick={() => setShowAiConfig(!showAiConfig)}
                  className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition-colors text-sm"
                >
                  {showAiConfig ? '收起配置' : '展开配置'}
                </button>
              </div>
            </CardHeader>
            {showAiConfig && (
              <CardContent>
                <div className="space-y-4">
                  <div className="bg-blue-500/10 border border-blue-500/50 rounded-lg p-4 mb-4">
                    <p className="text-blue-400 text-sm">
                      <strong>💡 说明:</strong> 
                      {aiConfigs.filter(c => c.enabled).length === 0 && ' 请至少启用一个AI模型以使用分析功能'}
                      {aiConfigs.filter(c => c.enabled).length === 1 && ' 当前为单模型模式'}
                      {aiConfigs.filter(c => c.enabled).length > 1 && ' 当前为多模型综合分析模式'}
                    </p>
                  </div>

                  {aiConfigs.map((config, index) => (
                    <div key={config.name} className="border border-gray-700 rounded-lg p-4 hover:border-accent-primary/50 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="flex items-center pt-1">
                          <input
                            type="checkbox"
                            checked={config.enabled}
                            onChange={() => {
                              const newConfigs = [...aiConfigs]
                              newConfigs[index].enabled = !newConfigs[index].enabled
                              setAiConfigs(newConfigs)
                            }}
                            className="w-5 h-5 rounded border-gray-600 text-accent-primary focus:ring-accent-primary focus:ring-offset-gray-800"
                          />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h3 className="text-lg font-semibold text-white">{config.name}</h3>
                            <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded">
                              {config.model}
                            </span>
                            {config.enabled && (
                              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                                ✓ 已启用
                              </span>
                            )}
                          </div>

                          <div className="space-y-2">
                            <label className="text-sm text-gray-400">API密钥</label>
                            <div className="flex gap-2">
                              <div className="flex-1 relative">
                                <input
                                  type={showKeys[index] ? "text" : "password"}
                                  value={config.key}
                                  onChange={(e) => {
                                    const newConfigs = [...aiConfigs]
                                    newConfigs[index].key = e.target.value
                                    newConfigs[index].testResult = null
                                    setAiConfigs(newConfigs)
                                  }}
                                  placeholder={`请输入${config.name} API Key`}
                                  className="w-full px-3 py-2 pr-10 bg-bg-secondary border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
                                  disabled={!config.enabled}
                                />
                                <button
                                  type="button"
                                  onClick={() => setShowKeys(prev => ({ ...prev, [index]: !prev[index] }))}
                                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors p-1"
                                  title={showKeys[index] ? "隐藏密钥" : "显示密钥"}
                                >
                                  {showKeys[index] ? "🙈" : "👁️"}
                                </button>
                              </div>
                              <button
                                onClick={() => testAiConnection(index)}
                                disabled={!config.enabled || !config.key || config.testing}
                                className={`px-4 py-2 rounded-lg transition-colors whitespace-nowrap ${
                                  config.testing
                                    ? 'bg-gray-600 cursor-wait'
                                    : config.testResult === 'success'
                                    ? 'bg-green-600 hover:bg-green-700'
                                    : config.testResult === 'error'
                                    ? 'bg-red-600 hover:bg-red-700'
                                    : 'bg-accent-primary hover:bg-accent-primary/80'
                                } text-white disabled:opacity-50 disabled:cursor-not-allowed`}
                              >
                                {config.testing ? '测试中...' : config.testResult === 'success' ? '✓ 成功' : config.testResult === 'error' ? '✗ 失败' : '测试连接'}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}

                  <div className="mt-6 pt-4 border-t border-gray-700 flex items-center justify-between">
                    <div className="text-sm text-gray-400">
                      <p>💾 配置自动保存到浏览器本地</p>
                    </div>
                    <button
                      onClick={saveAiConfigs}
                      className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors flex items-center gap-2"
                    >
                      <span>💾</span>
                      <span>保存到数据库</span>
                    </button>
                  </div>
                </div>
              </CardContent>
            )}
          </Card>

          {/* Celery系统状态 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle className="text-base">Celery Worker</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${celeryRunning ? 'bg-success animate-pulse' : 'bg-gray-600'}`}></div>
                    <span className={celeryRunning ? 'text-success' : 'text-text-tertiary'}>
                      {celeryRunning ? '运行中' : '已停止'}
                    </span>
                  </div>
                  <span className="text-2xl">{celeryRunning ? '✅' : '⏸️'}</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-bg-tertiary border-gray-700">
              <CardHeader>
                <CardTitle className="text-base">Celery Beat</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${beatRunning ? 'bg-success animate-pulse' : 'bg-gray-600'}`}></div>
                    <span className={beatRunning ? 'text-success' : 'text-text-tertiary'}>
                      {beatRunning ? '运行中' : '已停止'}
                    </span>
                  </div>
                  <span className="text-2xl">{beatRunning ? '⏰' : '⏸️'}</span>
                </div>
              </CardContent>
            </Card>

            <Card className={`border-2 ${celeryRunning && beatRunning ? 'bg-gradient-to-br from-green-900/20 to-blue-900/20 border-success' : 'bg-bg-tertiary border-gray-700'}`}>
              <CardHeader>
                <CardTitle className="text-base">AI自动运行</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${celeryRunning && beatRunning ? 'bg-success animate-pulse' : 'bg-gray-600'}`}></div>
                    <span className={celeryRunning && beatRunning ? 'text-success font-semibold' : 'text-text-tertiary'}>
                      {celeryRunning && beatRunning ? '已启用' : '未启用'}
                    </span>
                  </div>
                  <span className="text-2xl">{celeryRunning && beatRunning ? '🚀' : '💤'}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* 平台管理（新增） */}
          <Card className="bg-bg-tertiary border-gray-700 mb-8">
            <CardHeader>
              <CardTitle className="text-xl">🌍 国际平台数据采集系统</CardTitle>
            </CardHeader>
            <CardContent>
              {loadingPlatforms ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent-primary mx-auto"></div>
                  <p className="text-text-secondary mt-2">加载平台配置中...</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {platforms.map((platform) => (
                    <div key={platform.id} className="border border-gray-700 rounded-lg p-5 hover:border-accent-primary/50 transition-all">
                      {/* 平台标题行 */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">
                            {platform.id === 'twitter' && '🐦'}
                            {platform.id === 'telegram' && '💬'}
                            {platform.id === 'discord' && '🎮'}
                          </span>
                          <h3 className="text-xl font-bold text-white">
                            {platform.id === 'twitter' && 'Twitter/X'}
                            {platform.id === 'telegram' && 'Telegram'}
                            {platform.id === 'discord' && 'Discord'}
                          </h3>
                          <div className="flex items-center gap-2 ml-2">
                            <label className="relative inline-flex items-center cursor-pointer">
                              <input
                                type="checkbox"
                                checked={platform.enabled}
                                onChange={() => togglePlatform(platform.id, !platform.enabled)}
                                className="sr-only peer"
                              />
                              <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-accent-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-primary"></div>
                            </label>
                            <span className={`text-sm font-medium ${platform.enabled ? 'text-success' : 'text-gray-500'}`}>
                              {platform.enabled ? '启用' : '停用'}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => triggerPlatformCollection(platform.id)}
                          disabled={!platform.enabled}
                          className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          立即采集
                        </button>
                      </div>

                      {/* 平台策略 */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-400 mb-1">采集策略</p>
                          <div className="flex flex-wrap gap-2">
                            {platform.id === 'twitter' && (
                              <>
                                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">✓ 关键词监控</span>
                                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">✓ KOL追踪</span>
                                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">✓ 评论区挖掘</span>
                              </>
                            )}
                            {platform.id === 'telegram' && (
                              <>
                                <span className="px-2 py-1 bg-sky-500/20 text-sky-400 text-xs rounded">✓ 频道订阅(120+)</span>
                                <span className="px-2 py-1 bg-sky-500/20 text-sky-400 text-xs rounded">✓ 群组监控</span>
                                <span className="px-2 py-1 bg-sky-500/20 text-sky-400 text-xs rounded">✓ 官方验证</span>
                              </>
                            )}
                            {platform.id === 'discord' && (
                              <>
                                <span className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded">Bot实时监听(50+服务器)</span>
                              </>
                            )}
                          </div>
                        </div>
                        <div>
                          <p className="text-sm text-gray-400 mb-1">运行状态</p>
                          <p className="text-white">
                            频率: 每{platform.frequency_minutes}分钟 | 
                            最后采集: {platform.last_collected_at || '从未'}
                          </p>
                        </div>
                      </div>

                      {/* 今日统计 */}
                      <div className="grid grid-cols-4 gap-4 bg-bg-secondary rounded-lg p-3">
                        <div>
                          <p className="text-xs text-gray-400 mb-1">采集数据</p>
                          <p className="text-lg font-bold text-white">{platform.today_collected}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 mb-1">发现项目</p>
                          <p className="text-lg font-bold text-green-400">{platform.today_projects}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 mb-1">发现KOL</p>
                          <p className="text-lg font-bold text-blue-400">{platform.today_kols}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 mb-1">AI推荐</p>
                          <p className="text-lg font-bold text-purple-400">{platform.today_recommended}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* AI工作配置（新增） */}
          <Card className="bg-bg-tertiary border-gray-700 mb-8">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl">🎯 AI工作配置</CardTitle>
                <button
                  onClick={() => setShowAiWorkConfig(!showAiWorkConfig)}
                  className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition-colors text-sm"
                >
                  {showAiWorkConfig ? '收起' : '展开配置'}
                </button>
              </div>
            </CardHeader>
            {showAiWorkConfig && aiWorkConfig && (
              <CardContent>
                <div className="space-y-6">
                  {/* 工作目标 */}
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">主要目标</label>
                    <input
                      type="text"
                      value={aiWorkConfig.primary_goal}
                      onChange={(e) => setAiWorkConfig({...aiWorkConfig, primary_goal: e.target.value})}
                      className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                    />
                  </div>

                  {/* 筛选标准 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm text-gray-400 mb-2">AI推荐最低分数 (0-100)</label>
                      <input
                        type="number"
                        value={aiWorkConfig.min_ai_score}
                        onChange={(e) => setAiWorkConfig({...aiWorkConfig, min_ai_score: parseFloat(e.target.value)})}
                        min="0"
                        max="100"
                        className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-gray-400 mb-2">目标ROI倍数</label>
                      <input
                        type="number"
                        value={aiWorkConfig.target_roi}
                        onChange={(e) => setAiWorkConfig({...aiWorkConfig, target_roi: parseFloat(e.target.value)})}
                        min="1"
                        className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                  </div>

                  {/* 每日配额 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm text-gray-400 mb-2">每日推荐项目上限</label>
                      <input
                        type="number"
                        value={aiWorkConfig.max_projects_per_day}
                        onChange={(e) => setAiWorkConfig({...aiWorkConfig, max_projects_per_day: parseInt(e.target.value)})}
                        min="1"
                        className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-gray-400 mb-2">每日推荐KOL上限</label>
                      <input
                        type="number"
                        value={aiWorkConfig.max_kols_per_day}
                        onChange={(e) => setAiWorkConfig({...aiWorkConfig, max_kols_per_day: parseInt(e.target.value)})}
                        min="1"
                        className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                  </div>

                  {/* 风险偏好 */}
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">风险偏好</label>
                    <select
                      value={aiWorkConfig.risk_tolerance}
                      onChange={(e) => setAiWorkConfig({...aiWorkConfig, risk_tolerance: e.target.value})}
                      className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white"
                    >
                      <option value="conservative">保守</option>
                      <option value="moderate">中等</option>
                      <option value="aggressive">激进</option>
                    </select>
                  </div>

                  {/* 保存按钮 */}
                  <div className="flex justify-end">
                    <button
                      onClick={saveAiWorkConfig}
                      className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                    >
                      💾 保存配置
                    </button>
                  </div>
                </div>
              </CardContent>
            )}
          </Card>

          {/* 系统日志 */}
          <Card className="bg-bg-tertiary border-gray-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>系统日志</CardTitle>
                <button
                  onClick={() => setLogs(['[系统] 日志已清空'])}
                  className="text-xs text-text-tertiary hover:text-text-primary transition-colors"
                >
                  清空日志
                </button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-900 rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
                {logs.map((log, index) => (
                  <div
                    key={index}
                    className={`mb-1 ${
                      log.includes('[错误]') ? 'text-danger' :
                      log.includes('[成功]') ? 'text-success' :
                      log.includes('[平台]') || log.includes('[采集]') ? 'text-accent-primary' :
                      log.includes('[AI配置]') ? 'text-purple-400' :
                      'text-text-tertiary'
                    }`}
                  >
                    {log}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  )
}
