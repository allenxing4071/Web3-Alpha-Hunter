/**
 * 导航栏组件 - 包含登出按钮
 */

"use client"

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'

export function Navbar() {
  const router = useRouter()
  const pathname = usePathname()
  const { user, logout, isAuthenticated } = useAuthStore()

  // 登录页不显示导航栏
  if (pathname === '/login' || !isAuthenticated) {
    return null
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  const navItems = [
    { href: '/', label: '首页' },
    { href: '/projects', label: '项目列表' },
    { href: '/compare', label: '项目对比' },
    { href: '/admin', label: '系统管理' },
    { href: '/users', label: '用户管理' },
    { href: '/api-docs.html', label: 'API文档', external: true },
  ]

  return (
    <nav className="bg-bg-tertiary border-b border-gray-700 sticky top-0 z-50 backdrop-blur-xl bg-bg-tertiary/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              Web3 Alpha Hunter
            </span>
          </Link>

          {/* 导航链接 */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              item.external ? (
                <a
                  key={item.href}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-lg transition-colors text-text-secondary hover:text-text-primary hover:bg-bg-secondary"
                >
                  {item.label} 🔗
                </a>
              ) : (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    pathname === item.href
                      ? 'bg-accent-primary/20 text-accent-primary'
                      : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                  }`}
                >
                  {item.label}
                </Link>
              )
            ))}
          </div>

          {/* 用户信息和登出 */}
          <div className="flex items-center space-x-4">
            <div className="text-sm">
              <p className="text-text-secondary">欢迎,</p>
              <p className="text-text-primary font-semibold">{user?.username}</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-danger/20 text-danger rounded-lg hover:bg-danger/30 transition-colors"
            >
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

