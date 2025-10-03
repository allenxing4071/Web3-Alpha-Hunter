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

export default function AdminPage() {
  const router = useRouter()
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

  // 模拟检查Celery状态
  const checkCeleryStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/celery-status')
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
    addLog(`[手动] 开始${source}数据采集...`)
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/admin/collect/${source}`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const data = await response.json()
        addLog(`[成功] ${source}采集完成,发现 ${data.projects_found || 0} 个项目`)
        addLog(`[系统] 正在刷新项目列表...`)
        
        // 延迟1秒后跳转到项目列表页
        setTimeout(() => {
          router.push('/projects')
        }, 1000)
      } else {
        addLog(`[错误] ${source}采集失败`)
      }
    } catch (error) {
      addLog(`[错误] 后端未启动或网络错误`)
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
    const interval = setInterval(checkCeleryStatus, 10000) // 每10秒检查一次
    return () => clearInterval(interval)
  }, [])

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
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <button
                onClick={() => triggerCollection('twitter')}
                className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                🐦 Twitter
              </button>
              <button
                onClick={() => triggerCollection('telegram')}
                className="px-4 py-3 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors font-medium"
              >
                📱 Telegram
              </button>
              <button
                onClick={() => triggerCollection('coingecko')}
                className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
              >
                🦎 CoinGecko
              </button>
              <button
                onClick={() => triggerCollection('all')}
                className="px-4 py-3 bg-gradient-to-r from-accent-primary to-accent-purple text-white rounded-lg hover:shadow-lg transition-all font-medium"
              >
                🚀 全部采集
              </button>
            </div>
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

