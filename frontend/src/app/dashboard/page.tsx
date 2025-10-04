"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, user, isAdmin } = useAuthStore()
  const [backendStatus, setBackendStatus] = useState<string>('检查中...')
  const [frontendStatus, setFrontendStatus] = useState<string>('运行正常')

  useEffect(() => {
    // 检查是否登录
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    // 检查后端状态
    checkBackendStatus()
    const interval = setInterval(checkBackendStatus, 30000)
    return () => clearInterval(interval)
  }, [isAuthenticated, router])

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      if (response.ok) {
        setBackendStatus('✅ 运行正常')
      } else {
        setBackendStatus('❌ 未运行')
      }
    } catch (error) {
      setBackendStatus('❌ 未运行')
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-gray-400">验证身份中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            🚀 Web3 Alpha Hunter
          </h1>
          <p className="text-xl text-text-secondary">
            AI驱动的Web3项目发现平台 - 控制面板
          </p>
          <div className="mt-4 inline-flex items-center gap-2 bg-bg-tertiary border border-gray-700 px-4 py-2 rounded-lg">
            <span className="text-sm text-text-secondary">当前用户:</span>
            <span className="text-white font-semibold">{user?.username}</span>
            <span className={`px-2 py-0.5 rounded text-xs ${
              user?.role === 'admin' 
                ? 'bg-red-500 text-white' 
                : 'bg-blue-500 text-white'
            }`}>
              {user?.role === 'admin' ? '管理员' : '普通用户'}
            </span>
          </div>
        </div>

        {/* 服务状态卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatusCard
            title="后端服务"
            status={backendStatus}
            port="8000"
          />
          <StatusCard
            title="前端服务"
            status={frontendStatus}
            port="3000"
          />
          <StatusCard
            title="项目状态"
            status="v1.0.0"
            port="Development"
          />
        </div>

        {/* 前端页面链接 */}
        <LinkSection title="🌐 前端页面">
          <LinkCard
            icon="🏠"
            title="首页"
            desc="项目介绍和快速导航"
            url="http://localhost:3000"
          />
          <LinkCard
            icon="📊"
            title="项目列表"
            desc="查看所有Web3项目"
            url="http://localhost:3000/projects"
          />
          <LinkCard
            icon="⚖️"
            title="项目对比"
            desc="多项目横向对比分析"
            url="http://localhost:3000/compare"
          />
          {isAdmin() && (
            <>
              <LinkCard
                icon="⚙️"
                title="系统管理"
                desc="数据采集与任务管理"
                url="http://localhost:3000/admin"
                adminOnly
              />
              <LinkCard
                icon="👥"
                title="用户管理"
                desc="用户增删改查"
                url="http://localhost:3000/users"
                adminOnly
              />
            </>
          )}
          <LinkCard
            icon="📚"
            title="API文档"
            desc="第三方API文档链接"
            url="http://localhost:3000/api-docs.html"
          />
        </LinkSection>

        {/* 后端API链接 */}
        <LinkSection title="🔌 后端API">
          <LinkCard
            icon="🏠"
            title="API首页"
            desc="API基本信息"
            url="http://localhost:8000"
          />
          <LinkCard
            icon="❤️"
            title="健康检查"
            desc="服务健康状态"
            url="http://localhost:8000/health"
          />
          <LinkCard
            icon="📖"
            title="Swagger文档"
            desc="交互式API文档"
            url="http://localhost:8000/docs"
          />
          <LinkCard
            icon="📑"
            title="ReDoc文档"
            desc="更美观的API文档"
            url="http://localhost:8000/redoc"
          />
          {isAdmin() && (
            <LinkCard
              icon="🔧"
              title="Celery状态"
              desc="查看任务队列状态"
              url="http://localhost:8000/api/v1/admin/celery-status"
              adminOnly
            />
          )}
          <LinkCard
            icon="🗄️"
            title="数据库管理"
            desc="查看表结构和数据"
            url="http://localhost:3000/database.html"
          />
        </LinkSection>

        {/* 项目文档 - 仅管理员可见 */}
        {isAdmin() && (
          <LinkSection title="📖 项目文档 (仅管理员)">
            <LinkCard
              icon="📚"
              title="完整文档中心"
              desc="查看所有项目文档和配置指南"
              url="http://localhost:3000/docs.html"
              adminOnly
            />
            <LinkCard
              icon="🤖"
              title="DeepSeek AI"
              desc="AI分析引擎官方文档"
              url="https://github.com/deepseek-ai/DeepSeek-V3"
              adminOnly
            />
            <LinkCard
              icon="📊"
              title="数据采集配置"
              desc="采集流程和配置说明"
              url="http://localhost:3000/admin"
              adminOnly
            />
            <LinkCard
              icon="👥"
              title="用户权限管理"
              desc="角色和权限配置指南"
              url="http://localhost:3000/users"
              adminOnly
            />
          </LinkSection>
        )}

        {/* 登录凭证 */}
        <div className="bg-yellow-500/10 border border-yellow-500/50 rounded-lg p-6 mt-8">
          <h3 className="text-yellow-400 font-bold mb-3 text-lg">👤 默认登录凭证</h3>
          <div className="space-y-2 text-text-secondary">
            <p>管理员用户名: <code className="bg-bg-tertiary text-yellow-400 px-2 py-1 rounded">admin</code></p>
            <p>管理员密码: <code className="bg-bg-tertiary text-yellow-400 px-2 py-1 rounded">admin123</code></p>
            <p className="text-sm text-yellow-500 mt-4">⚠️ 生产环境请务必修改默认密码</p>
          </div>
        </div>

        {/* 常用命令 - 仅管理员可见 */}
        {isAdmin() && (
          <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 mt-8">
            <h2 className="text-2xl font-bold text-text-primary mb-6">🛠️ 常用命令 (仅管理员)</h2>
            
            <div className="space-y-4">
              <CommandBlock title="启动服务">
                <code># 后端{'\n'}cd backend{'\n'}uvicorn app.main:app --reload --port 8000{'\n\n'}# 前端{'\n'}cd frontend{'\n'}npm run dev</code>
              </CommandBlock>

              <CommandBlock title="停止服务">
                <code>lsof -ti:8000 | xargs kill -9  # 停止后端{'\n'}lsof -ti:3000 | xargs kill -9  # 停止前端</code>
              </CommandBlock>

              <CommandBlock title="查看日志">
                <code>tail -f /tmp/backend.log  # 后端日志{'\n'}tail -f /tmp/frontend.log # 前端日志</code>
              </CommandBlock>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// 状态卡片组件
function StatusCard({ title, status, port }: { title: string; status: string; port: string }) {
  return (
    <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6 hover:border-accent-primary transition-all">
      <h3 className="text-lg font-semibold text-text-primary mb-2">{title}</h3>
      <p className="text-text-secondary text-sm mb-2">端口: {port}</p>
      <p className="text-white font-medium">{status}</p>
    </div>
  )
}

// 链接区域组件
function LinkSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6 mb-8">
      <h2 className="text-2xl font-bold text-text-primary mb-6 border-b border-gray-700 pb-3 flex items-center gap-2">
        {title}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {children}
      </div>
    </div>
  )
}

// 链接卡片组件
function LinkCard({ 
  icon, 
  title, 
  desc, 
  url, 
  adminOnly = false,
  isFile = false
}: { 
  icon: string
  title: string
  desc: string
  url: string
  adminOnly?: boolean
  isFile?: boolean
}) {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-3 p-4 bg-gradient-to-r from-accent-primary to-accent-purple rounded-lg hover:scale-105 transition-all shadow-lg hover:shadow-xl"
    >
      <div className="text-3xl">{icon}</div>
      <div className="flex-1">
        <div className="font-bold text-white mb-1 flex items-center gap-2">
          {title}
          {adminOnly && (
            <span className="text-xs bg-red-500 px-2 py-0.5 rounded">仅管理员</span>
          )}
        </div>
        <div className="text-sm text-purple-100">{desc}</div>
      </div>
    </a>
  )
}

// 命令块组件
function CommandBlock({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="text-white font-semibold mb-2">{title}</h3>
      <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-green-400 overflow-x-auto">
        <pre>{children}</pre>
      </div>
    </div>
  )
}

