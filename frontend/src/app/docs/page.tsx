"use client"

import { AuthGuard } from '@/components/AuthGuard'
import Link from 'next/link'

export default function DocsPage() {
  const docs = [
    {
      title: '📋 需求与设计',
      items: [
        { name: '项目概述', path: '/docs/01-需求与设计/01-项目概述.md' },
        { name: '功能需求清单', path: '/docs/01-需求与设计/02-功能需求清单.md' },
        { name: '数据流设计', path: '/docs/01-需求与设计/03-数据流设计.md' },
        { name: 'UI/UX设计规范', path: '/docs/01-需求与设计/04-UI-UX设计规范.md' },
      ]
    },
    {
      title: '⚙️ 技术实现',
      items: [
        { name: '技术选型', path: '/docs/02-技术实现/01-技术选型.md' },
        { name: 'API接口文档', path: '/docs/02-技术实现/02-API接口文档.md' },
        { name: '已实现功能清单', path: '/docs/02-技术实现/03-已实现功能清单.md' },
        { name: '数据库设计文档', path: '/docs/02-技术实现/04-数据库设计文档.md' },
      ]
    },
    {
      title: '📝 开发规范',
      items: [
        { name: '代码规范', path: '/docs/03-开发规范/01-代码规范.md' },
      ]
    },
    {
      title: '🚀 部署与运维',
      items: [
        { name: '部署指南', path: '/docs/04-部署与运维/01-部署指南.md' },
        { name: '服务器连接指南', path: '/docs/04-部署与运维/02-服务器连接指南.md' },
        { name: '服务器环境详情', path: '/docs/04-部署与运维/03-服务器环境详情.md' },
      ]
    },
    {
      title: '📖 操作手册',
      items: [
        { name: '用户手册', path: '/docs/05-操作手册/01-用户手册.md' },
      ]
    }
  ]

  return (
    <AuthGuard>
      <div className="min-h-screen bg-bg-primary">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="bg-bg-tertiary rounded-xl border border-gray-800 p-8">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                📚 项目文档
              </h1>
              <Link
                href="/"
                className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-lg transition-all"
              >
                ← 返回首页
              </Link>
            </div>

            <div className="space-y-8">
              {docs.map((section, idx) => (
                <div key={idx} className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">{section.title}</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {section.items.map((item, itemIdx) => (
                      <a
                        key={itemIdx}
                        href={item.path}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 px-4 py-3 bg-gray-800/50 hover:bg-gray-700/50 border border-gray-700 hover:border-purple-500/50 rounded-lg transition-all group"
                      >
                        <span className="text-2xl">📄</span>
                        <span className="text-gray-300 group-hover:text-white transition-colors">
                          {item.name}
                        </span>
                        <span className="ml-auto text-xs text-gray-500 group-hover:text-purple-400">
                          查看 →
                        </span>
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* 快速链接 */}
            <div className="mt-8 bg-gradient-to-r from-blue-500/10 to-purple-500/10 p-6 rounded-lg border border-blue-500/20">
              <h3 className="text-xl font-bold text-white mb-4">🔗 快速链接</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Link
                  href="/api-docs"
                  className="px-4 py-3 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 rounded-lg text-blue-400 transition-colors text-center"
                >
                  📚 API 文档
                </Link>
                <Link
                  href="/database"
                  className="px-4 py-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg text-purple-400 transition-colors text-center"
                >
                  🗄️ 数据库管理
                </Link>
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-3 bg-gray-500/20 hover:bg-gray-500/30 border border-gray-500/50 rounded-lg text-gray-400 transition-colors text-center"
                >
                  💻 GitHub 仓库
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
