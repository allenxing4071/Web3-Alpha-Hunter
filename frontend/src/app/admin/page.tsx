/**
 * 系统管理后台
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface TaskStatus {
  name: string
  status: 'running' | 'stopped' | 'error'
  lastRun?: string
  nextRun?: string
  projectsFound?: number
}

interface AIConfig {
  name: string
  key: string
  enabled: boolean
  model: string
  testing?: boolean
  testResult?: 'success' | 'error' | null
}

export default function AdminPage() {
  const router = useRouter()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  const [celeryRunning, setCeleryRunning] = useState(false)
  const [beatRunning, setBeatRunning] = useState(false)
  const [tasks, setTasks] = useState<TaskStatus[]>([
    { name: 'Twitter采集器', status: 'stopped', lastRun: '从未运行' },
    { name: 'Telegram采集器', status: 'stopped', lastRun: '从未运行' },
    { name: 'CoinGecko采集器', status: 'stopped', lastRun: '从未运行' },
    { name: 'AI分析引擎', status: 'stopped', lastRun: '从未运行' },
  ])
  const [logs, setLogs] = useState<string[]>([
    '[系统] 管理后台已启动',
    '[提示] 请先启动Celery Worker和Beat以启用自动更新功能',
  ])
  const [collectionResult, setCollectionResult] = useState<any>(null)
  const [isCollecting, setIsCollecting] = useState(false)
  
  // AI模型配置
  const [aiConfigs, setAiConfigs] = useState<AIConfig[]>([
    { name: 'DeepSeek', key: '', enabled: false, model: 'deepseek-chat' },
    { name: 'Claude', key: '', enabled: false, model: 'claude-3-haiku-20240307' },
    { name: 'OpenAI', key: '', enabled: false, model: 'gpt-3.5-turbo' },
  ])
  const [showAiConfig, setShowAiConfig] = useState(false)

  // 模拟检查Celery状态
  const checkCeleryStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/celery-status`)
      if (response.ok) {
        const data = await response.json()
        setCeleryRunning(data.worker_running)
        setBeatRunning(data.beat_running)
      }
    } catch (error) {
      // 后端未启动或网络错误
      setCeleryRunning(false)
      setBeatRunning(false)
    }
  }

  // 手动触发数据采集
  const triggerCollection = async (source: string) => {
    setIsCollecting(true)
    setCollectionResult(null)
    addLog(`[手动] 开始${source}数据采集...`)
    
    try {
      const response = await fetch(`${API_URL}/admin/collect/${source}`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const data = await response.json()
        addLog(`[成功] ${source}采集完成,发现 ${data.projects_found || 0} 个项目`)
        setCollectionResult({
          source,
          success: true,
          projectsFound: data.projects_found || 0,
          message: data.message || '采集成功',
          timestamp: new Date().toLocaleString('zh-CN')
        })
      } else {
        addLog(`[错误] ${source}采集失败`)
        setCollectionResult({
          source,
          success: false,
          message: '采集失败,请检查后端服务',
          timestamp: new Date().toLocaleString('zh-CN')
        })
      }
    } catch (error) {
      addLog(`[错误] 后端未启动或网络错误`)
      setCollectionResult({
        source,
        success: false,
        message: '后端服务未启动或网络错误',
        timestamp: new Date().toLocaleString('zh-CN')
      })
    } finally {
      setIsCollecting(false)
    }
  }

  // 添加日志
  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString('zh-CN')
    setLogs(prev => [`[${timestamp}] ${message}`, ...prev].slice(0, 50))
  }

  // 定期检查状态
  useEffect(() => {
    checkCeleryStatus()
    loadAiConfigs()
    const interval = setInterval(checkCeleryStatus, 10000) // 每10秒检查一次
    return () => clearInterval(interval)
  }, [])

  // 加载AI配置 (优先从数据库加载)
  const loadAiConfigs = async () => {
    // 先尝试从数据库加载
    const loadedFromDB = await loadFromDatabase()
    
    // 如果数据库加载失败,从localStorage加载
    if (!loadedFromDB) {
      const saved = localStorage.getItem('ai-configs')
      if (saved) {
        try {
          setAiConfigs(JSON.parse(saved))
          addLog('[配置] 已从本地缓存加载AI配置')
        } catch (e) {
          console.error('Failed to load AI configs', e)
        }
      }
    }
  }

  // 保存AI配置
  const saveAiConfigs = (configs: AIConfig[]) => {
    setAiConfigs(configs)
    localStorage.setItem('ai-configs', JSON.stringify(configs))
    
    const enabledCount = configs.filter(c => c.enabled).length
    if (enabledCount === 0) {
      addLog('[AI配置] 已禁用所有AI模型')
    } else if (enabledCount === 1) {
      const model = configs.find(c => c.enabled)?.name
      addLog(`[AI配置] 使用单一模型: ${model}`)
    } else {
      const models = configs.filter(c => c.enabled).map(c => c.name).join(', ')
      addLog(`[AI配置] 多模型综合分析模式已启用: ${models}`)
    }
  }

  // 切换AI模型启用状态
  const toggleAiModel = (index: number) => {
    const newConfigs = [...aiConfigs]
    newConfigs[index].enabled = !newConfigs[index].enabled
    saveAiConfigs(newConfigs)
  }

  // 更新AI API密钥
  const updateAiKey = (index: number, key: string) => {
    const newConfigs = [...aiConfigs]
    newConfigs[index].key = key
    newConfigs[index].testResult = null // 重置测试结果
    saveAiConfigs(newConfigs)
  }

  // 测试AI API连接
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
      // 调用后端测试接口
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
        addLog(`[AI测试] ✅ ${config.name} 连接成功 - ${data.message || '模型可用'}`)
      } else {
        newConfigs[index].testResult = 'error'
        addLog(`[AI测试] ❌ ${config.name} 连接失败 - ${data.error || '请检查API密钥'}`)
      }
    } catch (error) {
      newConfigs[index].testing = false
      newConfigs[index].testResult = 'error'
      addLog(`[AI测试] ❌ ${config.name} 连接失败 - 网络错误或后端未启动`)
    }

    setAiConfigs(newConfigs)
  }

  // 保存配置到后端数据库
  const saveToDatabase = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ai-configs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ configs: aiConfigs })
      })

      if (response.ok) {
        addLog('[配置] ✅ AI配置已保存到数据库')
        return true
      } else {
        addLog('[配置] ❌ 保存到数据库失败')
        return false
      }
    } catch (error) {
      addLog('[配置] ⚠️ 数据库保存失败,已保存到本地')
      return false
    }
  }

  // 从后端加载配置
  const loadFromDatabase = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ai-configs`)
      if (response.ok) {
        const data = await response.json()
        if (data.configs && data.configs.length > 0) {
          setAiConfigs(data.configs)
          addLog('[配置] ✅ 已从数据库加载AI配置')
          return true
        }
      }
    } catch (error) {
      // 数据库加载失败,使用localStorage
    }
    return false
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            系统管理后台
          </h1>
          <p className="text-text-secondary">
            Web3 Alpha Hunter - 自动化数据采集与分析系统
          </p>
        </div>

        {/* AI模型配置 */}
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
                    {aiConfigs.filter(c => c.enabled).length === 1 && ' 当前为单模型模式,使用一个AI引擎进行分析'}
                    {aiConfigs.filter(c => c.enabled).length > 1 && ' 当前为多模型综合分析模式,将使用多个AI引擎进行交叉验证和综合评分'}
                  </p>
                </div>

                {aiConfigs.map((config, index) => (
                  <div key={config.name} className="border border-gray-700 rounded-lg p-4 hover:border-accent-primary/50 transition-colors">
                    <div className="flex items-start gap-4">
                      {/* 启用开关 */}
                      <div className="flex items-center pt-1">
                        <input
                          type="checkbox"
                          checked={config.enabled}
                          onChange={() => toggleAiModel(index)}
                          className="w-5 h-5 rounded border-gray-600 text-accent-primary focus:ring-accent-primary focus:ring-offset-gray-800"
                        />
                      </div>

                      {/* 模型信息 */}
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

                        {/* API密钥输入 */}
                        <div className="space-y-2">
                          <label className="text-sm text-gray-400">API密钥</label>
                          <div className="flex gap-2">
                            <input
                              type="password"
                              value={config.key}
                              onChange={(e) => updateAiKey(index, e.target.value)}
                              placeholder={`请输入${config.name} API Key`}
                              className="flex-1 px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
                              disabled={!config.enabled}
                            />
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
                          {config.enabled && !config.key && (
                            <p className="text-xs text-yellow-500">⚠️ 请配置API密钥后才能使用此模型</p>
                          )}
                          {config.testResult === 'success' && (
                            <p className="text-xs text-green-400">✅ API密钥验证成功,可以正常使用</p>
                          )}
                          {config.testResult === 'error' && (
                            <p className="text-xs text-red-400">❌ API密钥验证失败,请检查密钥是否正确</p>
                          )}
                        </div>

                        {/* 模型特点说明 */}
                        <div className="mt-2 text-xs text-gray-400">
                          {config.name === 'DeepSeek' && '🚀 推荐 - 国内访问快,性价比高,v3模型性能优异'}
                          {config.name === 'Claude' && '🎯 Anthropic Claude - 推理能力强,安全性高'}
                          {config.name === 'OpenAI' && '⭐ GPT系列 - 通用性强,生态完善'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {/* 保存到数据库按钮 */}
                <div className="mt-6 pt-4 border-t border-gray-700 flex items-center justify-between">
                  <div className="text-sm text-gray-400">
                    <p>💾 配置自动保存到浏览器本地</p>
                    <p className="text-xs text-gray-500 mt-1">建议保存到数据库以便多设备同步和更安全的存储</p>
                  </div>
                  <button
                    onClick={saveToDatabase}
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

        {/* 系统状态概览 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Celery Worker 状态 */}
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
              {!celeryRunning && (
                <p className="text-xs text-text-tertiary mt-3">
                  需要执行任务,请启动Worker
                </p>
              )}
            </CardContent>
          </Card>

          {/* Celery Beat 状态 */}
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
              {!beatRunning && (
                <p className="text-xs text-text-tertiary mt-3">
                  定时调度器,启动后自动采集
                </p>
              )}
            </CardContent>
          </Card>

          {/* 自动更新状态 */}
          <Card className={`border-2 ${celeryRunning && beatRunning ? 'bg-gradient-to-br from-green-900/20 to-blue-900/20 border-success' : 'bg-bg-tertiary border-gray-700'}`}>
            <CardHeader>
              <CardTitle className="text-base">自动更新</CardTitle>
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
              {celeryRunning && beatRunning && (
                <p className="text-xs text-success mt-3">
                  ✨ 系统正在自动发现新项目
                </p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* 启动指南 */}
        {(!celeryRunning || !beatRunning) && (
          <Card className="mb-8 bg-yellow-900/20 border-2 border-yellow-600">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-yellow-500">
                ⚠️ 系统未完全启动
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-text-secondary">
                要启用自动更新功能,请在后端服务器执行以下命令:
              </p>
              
              <div className="bg-bg-primary rounded-lg p-4 space-y-3">
                {!celeryRunning && (
                  <div>
                    <p className="text-sm text-text-tertiary mb-2">1️⃣ 启动 Celery Worker (执行任务):</p>
                    <code className="block bg-gray-900 text-accent-primary px-4 py-2 rounded font-mono text-sm">
                      cd backend && celery -A app.tasks.celery_app worker --loglevel=info
                    </code>
                  </div>
                )}
                
                {!beatRunning && (
                  <div>
                    <p className="text-sm text-text-tertiary mb-2">2️⃣ 启动 Celery Beat (定时调度):</p>
                    <code className="block bg-gray-900 text-accent-primary px-4 py-2 rounded font-mono text-sm">
                      cd backend && celery -A app.tasks.celery_app beat --loglevel=info
                    </code>
                  </div>
                )}
              </div>

              <div className="flex items-start gap-2 text-sm text-yellow-400 bg-yellow-900/30 p-3 rounded">
                <span>💡</span>
                <p>提示: 建议在两个独立的终端窗口中分别运行这两个命令</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* 手动采集控制 */}
        <Card className="mb-8 bg-bg-tertiary border-gray-700">
          <CardHeader>
            <CardTitle>手动触发数据采集</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <button
                onClick={() => triggerCollection('twitter')}
                disabled={isCollecting}
                className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCollecting ? '⏳ 采集中...' : '🐦 Twitter'}
              </button>
              <button
                onClick={() => triggerCollection('telegram')}
                disabled={isCollecting}
                className="px-4 py-3 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCollecting ? '⏳ 采集中...' : '📱 Telegram'}
              </button>
              <button
                onClick={() => triggerCollection('coingecko')}
                disabled={isCollecting}
                className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCollecting ? '⏳ 采集中...' : '🦎 CoinGecko'}
              </button>
              <button
                onClick={() => triggerCollection('all')}
                disabled={isCollecting}
                className="px-4 py-3 bg-gradient-to-r from-accent-primary to-accent-purple text-white rounded-lg hover:shadow-lg transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCollecting ? '⏳ 采集中...' : '🚀 全部采集'}
              </button>
            </div>

            {/* 采集结果展示 */}
            {collectionResult && (
              <div className={`p-4 rounded-lg border-2 ${
                collectionResult.success 
                  ? 'bg-green-900/20 border-green-600' 
                  : 'bg-red-900/20 border-red-600'
              }`}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">
                      {collectionResult.success ? '✅' : '❌'}
                    </span>
                    <div>
                      <h3 className={`font-semibold ${
                        collectionResult.success ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {collectionResult.success ? '采集成功!' : '采集失败'}
                      </h3>
                      <p className="text-sm text-text-tertiary">
                        来源: {collectionResult.source} | {collectionResult.timestamp}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => setCollectionResult(null)}
                    className="text-text-tertiary hover:text-text-primary"
                  >
                    ✕
                  </button>
                </div>
                
                {collectionResult.success && (
                  <div className="bg-bg-secondary rounded p-3 mb-3">
                    <div className="text-3xl font-bold text-green-400 mb-1">
                      {collectionResult.projectsFound}
                    </div>
                    <div className="text-sm text-text-secondary">
                      个项目已发现
                    </div>
                  </div>
                )}
                
                <p className="text-sm text-text-secondary mb-3">
                  {collectionResult.message}
                </p>
                
                {collectionResult.success && collectionResult.projectsFound > 0 && (
                  <button
                    onClick={() => router.push('/projects')}
                    className="w-full px-4 py-2 bg-accent-primary text-white rounded-lg hover:bg-accent-primary/80 transition-colors font-medium"
                  >
                    📊 查看项目列表
                  </button>
                )}
              </div>
            )}

            {/* 采集中的加载状态 */}
            {isCollecting && (
              <div className="flex items-center justify-center p-6 bg-bg-secondary rounded-lg">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
                  <p className="text-text-secondary">正在采集数据,请稍候...</p>
                  <p className="text-xs text-text-tertiary mt-2">这可能需要几秒钟</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 定时任务状态 */}
        <Card className="mb-8 bg-bg-tertiary border-gray-700">
          <CardHeader>
            <CardTitle>定时任务状态</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">任务名称</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">执行频率</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">状态</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">最后运行</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-700/50">
                    <td className="py-3 px-4 text-text-primary">🐦 Twitter数据采集</td>
                    <td className="py-3 px-4 text-text-secondary">每5分钟</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${beatRunning ? 'bg-success/20 text-success' : 'bg-gray-700 text-text-tertiary'}`}>
                        {beatRunning ? '运行中' : '未启动'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-text-tertiary text-sm">-</td>
                  </tr>
                  <tr className="border-b border-gray-700/50">
                    <td className="py-3 px-4 text-text-primary">📱 Telegram数据采集</td>
                    <td className="py-3 px-4 text-text-secondary">每15分钟</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${beatRunning ? 'bg-success/20 text-success' : 'bg-gray-700 text-text-tertiary'}`}>
                        {beatRunning ? '运行中' : '未启动'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-text-tertiary text-sm">-</td>
                  </tr>
                  <tr className="border-b border-gray-700/50">
                    <td className="py-3 px-4 text-text-primary">🤖 AI项目分析</td>
                    <td className="py-3 px-4 text-text-secondary">每1小时</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${beatRunning ? 'bg-success/20 text-success' : 'bg-gray-700 text-text-tertiary'}`}>
                        {beatRunning ? '运行中' : '未启动'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-text-tertiary text-sm">-</td>
                  </tr>
                  <tr className="border-b border-gray-700/50">
                    <td className="py-3 px-4 text-text-primary">📊 每日Alpha报告</td>
                    <td className="py-3 px-4 text-text-secondary">每天 09:00</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${beatRunning ? 'bg-success/20 text-success' : 'bg-gray-700 text-text-tertiary'}`}>
                        {beatRunning ? '运行中' : '未启动'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-text-tertiary text-sm">-</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </CardContent>
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
                    log.includes('[手动]') ? 'text-accent-primary' :
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
  )
}

