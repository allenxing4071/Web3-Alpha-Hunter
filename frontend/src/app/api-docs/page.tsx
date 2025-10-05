"use client"

import { AuthGuard } from '@/components/AuthGuard'

export default function ApiDocsPage() {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-bg-primary">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="bg-bg-tertiary rounded-xl border border-gray-800 p-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-6">
              📚 API 文档
            </h1>
            
            <div className="space-y-6">
              <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">FastAPI 交互式文档</h2>
                <p className="text-gray-400 mb-4">
                  访问以下链接查看完整的 API 文档和在线测试：
                </p>
                <div className="space-y-2">
                  <a
                    href="http://localhost:8000/docs"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-4 py-3 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 rounded-lg text-blue-400 transition-colors"
                  >
                    🚀 Swagger UI - http://localhost:8000/docs
                  </a>
                  <a
                    href="http://localhost:8000/redoc"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-4 py-3 bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 rounded-lg text-green-400 transition-colors"
                  >
                    📖 ReDoc - http://localhost:8000/redoc
                  </a>
                </div>
              </div>

              <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">主要 API 端点</h2>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs font-mono">GET</span>
                    <div className="flex-1">
                      <code className="text-sm text-gray-300">/api/v1/projects</code>
                      <p className="text-sm text-gray-500 mt-1">获取项目列表</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs font-mono">GET</span>
                    <div className="flex-1">
                      <code className="text-sm text-gray-300">/api/v1/projects/{'{id}'}</code>
                      <p className="text-sm text-gray-500 mt-1">获取项目详情</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs font-mono">POST</span>
                    <div className="flex-1">
                      <code className="text-sm text-gray-300">/api/v1/analyze/project</code>
                      <p className="text-sm text-gray-500 mt-1">分析项目</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs font-mono">GET</span>
                    <div className="flex-1">
                      <code className="text-sm text-gray-300">/api/v1/database/stats</code>
                      <p className="text-sm text-gray-500 mt-1">获取数据库统计</p>
                    </div>
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
