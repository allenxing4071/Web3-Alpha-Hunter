/**
 * 登录页面
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { useUserStore } from '@/store/userStore'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function LoginPage() {
  const router = useRouter()
  const login = useAuthStore(state => state.login)
  const initializeDefaultUsers = useUserStore(state => state.initializeDefaultUsers)
  
  // 初始化默认用户
  useEffect(() => {
    // 只在客户端执行
    if (typeof window !== 'undefined') {
      initializeDefaultUsers()
    }
  }, [initializeDefaultUsers])
  
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setError('')
    setLoading(true)

    try {
      console.log('🔐 开始登录...')
      const success = await login(username, password)
      console.log('📊 登录结果:', success)
      
      if (success) {
        console.log('✅ 登录成功,跳转到首页...')
        // 登录成功后跳转到首页
        window.location.replace('/')
      } else {
        console.error('❌ 登录失败')
        setError('用户名或密码错误')
        setLoading(false)
      }
    } catch (err) {
      console.error('❌ 登录异常:', err)
      setError('登录失败,请重试')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-bg-primary via-bg-secondary to-bg-primary p-4">
      {/* 背景装饰 */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent-primary/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-purple/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* 主内容区 */}
      <div className="relative z-10 flex-1 flex items-center justify-center">
        <div className="w-full max-w-md">
          {/* Logo和标题 */}
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              Web3 Alpha Hunter
            </h1>
            <p className="text-text-secondary text-lg">
              AI驱动的Web3项目发现平台
            </p>
          </div>

          {/* 登录卡片 */}
          <Card className="bg-bg-tertiary/80 backdrop-blur-xl border-gray-700 shadow-2xl">
            <CardHeader>
              <CardTitle className="text-2xl text-center text-text-primary">
                登录系统
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={(e) => e.preventDefault()} className="space-y-6">
                {/* 用户名 */}
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-text-secondary mb-2">
                    用户名
                  </label>
                  <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full px-4 py-3 bg-bg-secondary border border-gray-700 rounded-lg text-text-primary focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/50 transition-all"
                    placeholder="请输入用户名"
                    required
                    disabled={loading}
                  />
                </div>

                {/* 密码 */}
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-text-secondary mb-2">
                    密码
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-3 bg-bg-secondary border border-gray-700 rounded-lg text-text-primary focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/50 transition-all"
                    placeholder="请输入密码"
                    required
                    disabled={loading}
                  />
                </div>

                {/* 错误提示 */}
                {error && (
                  <div className="bg-danger/10 border border-danger/50 text-danger px-4 py-3 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                {/* 登录按钮 */}
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={loading}
                  className="w-full py-3 bg-gradient-to-r from-accent-primary to-accent-purple text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-accent-primary/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? '登录中...' : '登录'}
                </button>

                {/* 提示信息 */}
                <div className="text-center text-sm text-text-tertiary mt-4 p-4 bg-bg-secondary/50 rounded-lg border border-gray-700">
                  <p className="font-semibold mb-2">测试账号:</p>
                  <p>用户名: <span className="text-accent-primary font-mono">admin</span></p>
                  <p>密码: <span className="text-accent-primary font-mono">admin123</span></p>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* 底部特性展示区 */}
      <div className="relative z-10 mt-8 mb-4">
        <div className="max-w-4xl mx-auto">
          {/* 平台特性 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-bg-tertiary/60 backdrop-blur-sm border border-gray-700 rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">🤖</div>
              <h3 className="text-text-primary font-semibold mb-1">AI智能分析</h3>
              <p className="text-text-tertiary text-xs">DeepSeek驱动的项目评估</p>
            </div>
            <div className="bg-bg-tertiary/60 backdrop-blur-sm border border-gray-700 rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">⚡</div>
              <h3 className="text-text-primary font-semibold mb-1">实时监控</h3>
              <p className="text-text-tertiary text-xs">10秒自动刷新项目数据</p>
            </div>
            <div className="bg-bg-tertiary/60 backdrop-blur-sm border border-gray-700 rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">🎯</div>
              <h3 className="text-text-primary font-semibold mb-1">精准评级</h3>
              <p className="text-text-tertiary text-xs">S/A/B/C四级评分体系</p>
            </div>
          </div>

          {/* 版权信息 */}
          <div className="text-center text-text-tertiary text-sm">
            <p>© 2025 Web3 Alpha Hunter. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

