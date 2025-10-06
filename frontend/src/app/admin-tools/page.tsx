"use client"

import { useState } from 'react'
import { AuthGuard } from '@/components/AuthGuard'
import { API_BASE_URL } from '@/lib/config'

export default function AdminToolsPage() {
  const [result, setResult] = useState<string>('')
  const [loading, setLoading] = useState(false)

  const fixAdminRole = async () => {
    setLoading(true)
    setResult('')
    try {
      const response = await fetch(`${API_BASE_URL}/admin/fix-admin-role`, {
        method: 'POST'
      })
      const data = await response.json()
      setResult(JSON.stringify(data, null, 2))
    } catch (error) {
      setResult(`错误: ${error}`)
    } finally {
      setLoading(false)
    }
  }

  const resetLogin = () => {
    sessionStorage.clear()
    localStorage.clear()
    setResult('✅ 已清除所有登录信息，请刷新页面重新登录')
  }

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-screen bg-bg-primary">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-bg-tertiary rounded-xl border border-gray-800 p-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent mb-6">
              🛠️ 管理员工具
            </h1>
            
            <div className="space-y-6">
              {/* 修复管理员角色 */}
              <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-3">修复管理员角色</h2>
                <p className="text-gray-400 mb-4">
                  如果管理员账户权限异常，可以使用此工具重置 admin 用户的角色为管理员。
                </p>
                <button
                  onClick={fixAdminRole}
                  disabled={loading}
                  className="px-6 py-3 bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white rounded-lg font-medium transition-all disabled:opacity-50"
                >
                  {loading ? '处理中...' : '🔧 修复管理员角色'}
                </button>
              </div>

              {/* 重置登录状态 */}
              <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-3">重置登录状态</h2>
                <p className="text-gray-400 mb-4">
                  清除所有本地存储的登录信息，用于解决登录状态异常问题。
                </p>
                <button
                  onClick={resetLogin}
                  className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white rounded-lg font-medium transition-all"
                >
                  🔄 重置登录状态
                </button>
              </div>

              {/* 结果显示 */}
              {result && (
                <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                  <h3 className="text-lg font-bold text-white mb-3">执行结果</h3>
                  <pre className="text-sm text-gray-300 bg-black/50 p-4 rounded overflow-auto">
                    {result}
                  </pre>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
