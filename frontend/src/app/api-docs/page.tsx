"use client"

import { useState } from 'react'
import { AuthGuard } from '@/components/AuthGuard'
import { useAuthStore } from '@/store/authStore'
import { HEALTH_CHECK_URL, API_BASE_URL } from '@/lib/config'

export default function ApiDocsPage() {
  const { isAdmin } = useAuthStore()

  return (
    <AuthGuard>
      <div className="min-h-screen bg-bg-primary p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              📚 API 文档与开发工具
            </h1>
            <p className="text-text-secondary">
              API 接口文档、端点说明和开发常用命令
            </p>
          </div>

          {/* FastAPI 交互式文档 */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">🚀 FastAPI 交互式文档</h2>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6">
              <p className="text-text-secondary mb-4">
                访问以下链接查看完整的 API 文档和在线测试：
              </p>
              <div className="space-y-3">
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 p-4 bg-info/10 hover:bg-info/20 border border-info/50 rounded-lg text-info transition-all group"
                >
                  <span className="text-2xl group-hover:scale-110 transition-transform">📖</span>
                  <div className="flex-1">
                    <div className="font-bold mb-1">Swagger UI</div>
                    <div className="text-sm opacity-80">交互式 API 文档和测试工具</div>
                  </div>
                  <code className="text-xs bg-bg-primary px-3 py-1 rounded">http://localhost:8000/docs</code>
                </a>
                <a
                  href="http://localhost:8000/redoc"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 p-4 bg-success/10 hover:bg-success/20 border border-success/50 rounded-lg text-success transition-all group"
                >
                  <span className="text-2xl group-hover:scale-110 transition-transform">📑</span>
                  <div className="flex-1">
                    <div className="font-bold mb-1">ReDoc</div>
                    <div className="text-sm opacity-80">更美观的 API 文档展示</div>
                  </div>
                  <code className="text-xs bg-bg-primary px-3 py-1 rounded">http://localhost:8000/redoc</code>
                </a>
              </div>
            </div>
          </div>

          {/* API 端点列表 */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">🔌 API 端点</h2>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6">
              <div className="space-y-3">
                <ApiEndpoint
                  name="健康检查"
                  url={HEALTH_CHECK_URL}
                  method="GET"
                  description="检查后端服务运行状态"
                />
                <ApiEndpoint
                  name="项目列表"
                  url={`${API_BASE_URL}/projects`}
                  method="GET"
                  description="获取所有项目列表（支持分页和筛选）"
                />
                <ApiEndpoint
                  name="项目详情"
                  url={`${API_BASE_URL}/projects/{id}`}
                  method="GET"
                  description="获取指定项目的详细信息"
                />
                <ApiEndpoint
                  name="Dashboard统计"
                  url={`${API_BASE_URL}/dashboard/stats`}
                  method="GET"
                  description="获取项目统计数据和图表数据"
                />
                <ApiEndpoint
                  name="项目分析"
                  url={`${API_BASE_URL}/analyze/project`}
                  method="POST"
                  description="使用 AI 分析项目"
                />
                <ApiEndpoint
                  name="数据库统计"
                  url={`${API_BASE_URL}/database/stats`}
                  method="GET"
                  description="获取数据库表统计信息"
                />
                {isAdmin() && (
                  <>
                    <ApiEndpoint
                      name="Celery 状态"
                      url={`${API_BASE_URL}/admin/celery-status`}
                      method="GET"
                      description="查看任务队列状态（仅管理员）"
                      adminOnly
                    />
                    <ApiEndpoint
                      name="用户管理"
                      url={`${API_BASE_URL}/users`}
                      method="GET"
                      description="获取用户列表（仅管理员）"
                      adminOnly
                    />
                  </>
                )}
              </div>
            </div>
          </div>

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
                    title="启动 Celery Worker"
                    command="cd backend && celery -A app.tasks.celery_app worker -l info"
                  />
                  <CommandCard
                    title="启动 Celery Beat"
                    command="cd backend && celery -A app.tasks.celery_app beat -l info"
                  />
                  <CommandCard
                    title="数据库迁移"
                    command="cd backend && alembic upgrade head"
                  />
                  <CommandCard
                    title="创建迁移文件"
                    command="cd backend && alembic revision --autogenerate -m 'description'"
                  />
                  <CommandCard
                    title="查看后端日志"
                    command="tail -f /tmp/backend.log"
                  />
                  <CommandCard
                    title="查看前端日志"
                    command="tail -f /tmp/frontend.log"
                  />
                </div>
              </div>
            </div>
          )}

          {/* 环境配置信息 */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">🔧 环境配置</h2>
            <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <ConfigItem
                  label="后端端口"
                  value="8000"
                  icon="🔌"
                />
                <ConfigItem
                  label="前端端口"
                  value="3000"
                  icon="🌐"
                />
                <ConfigItem
                  label="数据库"
                  value="SQLite / PostgreSQL"
                  icon="🗄️"
                />
                <ConfigItem
                  label="任务队列"
                  value="Celery + Redis"
                  icon="⚙️"
                />
              </div>
            </div>
          </div>

          {/* 安全提示 */}
          <div className="bg-warning/10 border border-warning/50 rounded-lg p-6">
            <h3 className="text-warning font-bold mb-3 flex items-center gap-2">
              <span>⚠️</span>
              <span>安全提示</span>
            </h3>
            <div className="space-y-2 text-text-secondary text-sm">
              <p>• 默认管理员账号: <code className="bg-bg-tertiary text-warning px-2 py-1 rounded">admin</code> / <code className="bg-bg-tertiary text-warning px-2 py-1 rounded">admin123</code></p>
              <p>• 生产环境请务必修改默认密码</p>
              <p>• API 密钥请勿提交到 Git 仓库</p>
              <p>• 定期备份数据库数据</p>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}

// API端点组件
function ApiEndpoint({ 
  name, 
  url, 
  method,
  description,
  adminOnly = false
}: { 
  name: string
  url: string
  method: string
  description: string
  adminOnly?: boolean
}) {
  const methodColors: Record<string, string> = {
    GET: 'bg-success/20 text-success border-success/50',
    POST: 'bg-info/20 text-info border-info/50',
    PUT: 'bg-warning/20 text-warning border-warning/50',
    DELETE: 'bg-danger/20 text-danger border-danger/50',
  }

  return (
    <div className="flex items-start gap-3 p-4 bg-bg-secondary rounded-lg hover:bg-bg-primary transition-colors">
      <span className={`px-2 py-1 rounded text-xs font-mono border ${methodColors[method]} whitespace-nowrap`}>
        {method}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <p className="text-text-primary font-medium">{name}</p>
          {adminOnly && (
            <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded border border-red-500/50">
              管理员
            </span>
          )}
        </div>
        <p className="text-text-secondary text-sm mb-2">{description}</p>
        <a 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-accent-primary text-xs font-mono hover:underline break-all"
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

// 配置项组件
function ConfigItem({ 
  label, 
  value, 
  icon 
}: { 
  label: string
  value: string
  icon: string
}) {
  return (
    <div className="flex items-center gap-3 p-4 bg-bg-secondary rounded-lg">
      <span className="text-2xl">{icon}</span>
      <div>
        <div className="text-text-secondary text-sm">{label}</div>
        <div className="text-text-primary font-medium">{value}</div>
      </div>
    </div>
  )
}
