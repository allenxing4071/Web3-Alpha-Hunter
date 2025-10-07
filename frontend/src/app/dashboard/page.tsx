"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/store/authStore'
import { HEALTH_CHECK_URL, API_BASE_URL } from '@/lib/config'

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, user, isAdmin } = useAuthStore()
  const [backendStatus, setBackendStatus] = useState<string>('检查中...')
  const [projectStats, setProjectStats] = useState({ total: 0, s: 0, a: 0, today: 0 })

  useEffect(() => {
    // 检查是否登录
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    // 检查后端状态和获取统计数据
    checkBackendStatus()
    fetchProjectStats()
    const interval = setInterval(() => {
      checkBackendStatus()
      fetchProjectStats()
    }, 30000)
    return () => clearInterval(interval)
  }, [isAuthenticated, router])

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(HEALTH_CHECK_URL)
      if (response.ok) {
        setBackendStatus('运行正常')
      } else {
        setBackendStatus('未运行')
      }
    } catch (error) {
      setBackendStatus('未运行')
    }
  }

  const fetchProjectStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard/stats`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setProjectStats({
            total: data.data.total_projects || 0,
            s: data.data.grade_stats?.S || 0,
            a: data.data.grade_stats?.A || 0,
            today: data.data.new_today || 0,
          })
        }
      }
    } catch (error) {
      console.error('Failed to fetch project stats:', error)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">验证身份中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            📊 控制面板
          </h1>
          <p className="text-text-secondary">
            系统管理与监控中心 · 欢迎回来, {user?.username}
          </p>
        </div>

        {/* 用户信息卡片 */}
        <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-accent-primary to-accent-purple rounded-full flex items-center justify-center text-3xl">
                👤
              </div>
              <div>
                <h2 className="text-xl font-bold text-text-primary mb-1">{user?.username}</h2>
                <p className="text-text-secondary text-sm">{user?.email}</p>
              </div>
            </div>
            <div>
              <span className={`px-4 py-2 rounded-lg text-sm font-semibold ${
                user?.role === 'admin' 
                  ? 'bg-red-500/20 text-red-400 border border-red-500/50' 
                  : 'bg-blue-500/20 text-blue-400 border border-blue-500/50'
              }`}>
                {user?.role === 'admin' ? '🔒 管理员' : '👤 普通用户'}
              </span>
            </div>
          </div>
        </div>

        {/* 系统状态卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatusCard
            title="后端服务"
            value={backendStatus}
            icon="🔌"
            status={backendStatus === '运行正常' ? 'success' : 'error'}
            detail="Port 8000"
          />
          <StatusCard
            title="前端服务"
            value="运行正常"
            icon="🌐"
            status="success"
            detail="Port 3000"
          />
          <StatusCard
            title="项目总数"
            value={projectStats.total.toString()}
            icon="📊"
            status="info"
            detail={`S级: ${projectStats.s} | A级: ${projectStats.a}`}
          />
          <StatusCard
            title="今日新增"
            value={projectStats.today.toString()}
            icon="🆕"
            status="success"
            detail="实时监控中"
          />
        </div>

        {/* 快速导航 */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-text-primary mb-4">🚀 快速导航</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <NavCard
              icon="🏠"
              title="实时监控大屏"
              desc="查看项目实时数据与统计"
              href="/"
            />
            <NavCard
              icon="📋"
              title="项目列表"
              desc="浏览所有发现的Web3项目"
              href="/projects"
            />
            <NavCard
              icon="⚖️"
              title="项目对比"
              desc="多项目横向对比分析"
              href="/compare"
            />
            {isAdmin() && (
              <>
                <NavCard
                  icon="⚙️"
                  title="系统管理"
                  desc="数据采集与任务配置"
                  href="/admin"
                  adminOnly
                />
                <NavCard
                  icon="🎯"
                  title="项目审核"
                  desc="待审核项目列表"
                  href="/review"
                  adminOnly
                />
                <NavCard
                  icon="👥"
                  title="用户管理"
                  desc="管理系统用户与权限"
                  href="/users"
                  adminOnly
                />
                <NavCard
                  icon="🗄️"
                  title="数据库管理"
                  desc="查看数据库表结构"
                  href="/database"
                  adminOnly
                />
              </>
            )}
            <NavCard
              icon="📚"
              title="API文档"
              desc="查看API接口文档"
              href="/api-docs"
            />
          </div>
        </div>

        {/* API 端点 - 仅管理员可见 */}
        {isAdmin() && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">🔌 API 端点</h2>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6">
              <div className="space-y-3">
                <ApiEndpoint
                  name="健康检查"
                  url={`${HEALTH_CHECK_URL}`}
                  method="GET"
                />
                <ApiEndpoint
                  name="Swagger文档"
                  url="http://localhost:8000/docs"
                  method="GET"
                />
                <ApiEndpoint
                  name="ReDoc文档"
                  url="http://localhost:8000/redoc"
                  method="GET"
                />
                <ApiEndpoint
                  name="项目列表"
                  url={`${API_BASE_URL}/projects`}
                  method="GET"
                />
                <ApiEndpoint
                  name="Dashboard统计"
                  url={`${API_BASE_URL}/dashboard/stats`}
                  method="GET"
                />
              </div>
            </div>
          </div>
        )}

        {/* 快速命令 - 仅管理员可见 */}
        {isAdmin() && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">⚡ 快速命令</h2>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <CommandCard
                  title="启动后端"
                  command="cd backend && uvicorn app.main:app --reload"
                />
                <CommandCard
                  title="启动前端"
                  command="cd frontend && npm run dev"
                />
                <CommandCard
                  title="启动Celery"
                  command="cd backend && celery -A app.tasks.celery_app worker -l info"
                />
                <CommandCard
                  title="数据库迁移"
                  command="cd backend && alembic upgrade head"
                />
              </div>
            </div>
          </div>
        )}

        {/* 安全提示 */}
        <div className="bg-warning/10 border border-warning/50 rounded-lg p-6">
          <h3 className="text-warning font-bold mb-3 flex items-center gap-2">
            <span>⚠️</span>
            <span>安全提示</span>
          </h3>
          <div className="space-y-2 text-text-secondary text-sm">
            <p>• 默认管理员账号: <code className="bg-bg-tertiary text-warning px-2 py-1 rounded">admin</code> / <code className="bg-bg-tertiary text-warning px-2 py-1 rounded">admin123</code></p>
            <p>• 生产环境请务必修改默认密码</p>
            <p>• 定期备份数据库数据</p>
            <p>• 注意保护API密钥和配置信息</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// 状态卡片组件
function StatusCard({ 
  title, 
  value, 
  icon, 
  status, 
  detail 
}: { 
  title: string
  value: string
  icon: string
  status: 'success' | 'error' | 'info'
  detail: string
}) {
  const statusColors = {
    success: 'border-success/50 bg-success/5',
    error: 'border-danger/50 bg-danger/5',
    info: 'border-info/50 bg-info/5',
  }

  const valueColors = {
    success: 'text-success',
    error: 'text-danger',
    info: 'text-info',
  }

  return (
    <div className={`bg-bg-tertiary border ${statusColors[status]} rounded-lg p-6 hover:border-opacity-100 transition-all`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-text-secondary text-sm font-medium">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className={`text-3xl font-bold ${valueColors[status]} mb-2`}>
        {value}
      </div>
      <p className="text-text-tertiary text-xs">{detail}</p>
    </div>
  )
}

// 导航卡片组件
function NavCard({ 
  icon, 
  title, 
  desc, 
  href,
  adminOnly = false
}: { 
  icon: string
  title: string
  desc: string
  href: string
  adminOnly?: boolean
}) {
  return (
    <Link
      href={href}
      className="bg-bg-tertiary border border-gray-700 rounded-lg p-5 hover:border-accent-primary hover:bg-bg-secondary transition-all group"
    >
      <div className="flex items-start gap-3">
        <div className="text-3xl group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-bold text-text-primary group-hover:text-accent-primary transition-colors">
              {title}
            </h3>
            {adminOnly && (
              <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded border border-red-500/50">
                管理员
              </span>
            )}
          </div>
          <p className="text-text-secondary text-sm">{desc}</p>
        </div>
      </div>
    </Link>
  )
}

// API端点组件
function ApiEndpoint({ 
  name, 
  url, 
  method 
}: { 
  name: string
  url: string
  method: string
}) {
  const methodColors: Record<string, string> = {
    GET: 'bg-success/20 text-success border-success/50',
    POST: 'bg-info/20 text-info border-info/50',
    PUT: 'bg-warning/20 text-warning border-warning/50',
    DELETE: 'bg-danger/20 text-danger border-danger/50',
  }

  return (
    <div className="flex items-center gap-3 p-3 bg-bg-secondary rounded-lg hover:bg-bg-primary transition-colors">
      <span className={`px-2 py-1 rounded text-xs font-mono border ${methodColors[method]}`}>
        {method}
      </span>
      <div className="flex-1">
        <p className="text-text-primary font-medium text-sm mb-1">{name}</p>
        <a 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-accent-primary text-xs font-mono hover:underline"
        >
          {url}
        </a>
      </div>
    </div>
  )
}

// 命令卡片组件
function CommandCard({ 
  title, 
  command 
}: { 
  title: string
  command: string
}) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(command)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="bg-bg-secondary border border-gray-700 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-text-primary font-semibold text-sm">{title}</h3>
        <button
          onClick={handleCopy}
          className="px-2 py-1 bg-accent-primary/20 text-accent-primary text-xs rounded hover:bg-accent-primary/30 transition-colors"
        >
          {copied ? '✓ 已复制' : '📋 复制'}
        </button>
      </div>
      <div className="bg-gray-900 rounded p-3 font-mono text-xs text-success overflow-x-auto">
        {command}
      </div>
    </div>
  )
}

