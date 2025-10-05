/**
 * 导航栏组件 - 支持角色权限和管理员下拉菜单
 */

"use client"

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { useState, useRef, useEffect } from 'react'

export function Navbar() {
  const router = useRouter()
  const pathname = usePathname()
  const { user, logout, isAdmin, checkAuth } = useAuthStore()
  const [adminMenuOpen, setAdminMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [mounted, setMounted] = useState(false)
  const adminMenuRef = useRef<HTMLDivElement>(null)
  const userMenuRef = useRef<HTMLDivElement>(null)

  // 客户端挂载标记并恢复认证状态
  useEffect(() => {
    setMounted(true)
    // 从sessionStorage恢复用户信息
    checkAuth()
  }, [])

  // 点击外部关闭菜单
  useEffect(() => {
    // 只在客户端执行
    if (typeof window === 'undefined') return

    const handleClickOutside = (event: MouseEvent) => {
      if (adminMenuRef.current && !adminMenuRef.current.contains(event.target as Node)) {
        setAdminMenuOpen(false)
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setUserMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  // 登录页不显示导航栏 - 必须在所有hooks之后
  if (pathname === '/login' || !mounted) {
    return null
  }

  // 普通用户可见菜单
  const publicNavItems = [
    { href: '/', label: '首页' },
    { href: '/projects', label: '项目列表' },
    { href: '/compare', label: '项目对比' },
    { href: '/api-docs', label: 'API文档' },
  ]

  // 管理员菜单项
  const adminNavItems = [
    { href: '/dashboard', label: '控制面板', icon: '📊' },
    { href: '/admin', label: '系统管理', icon: '⚙️' },
    { href: '/users', label: '用户管理', icon: '👥' },
    { href: '/database', label: '数据库管理', icon: '🗄️' },
  ]

  return (
    <nav className="bg-bg-tertiary border-b border-gray-700 sticky top-0 z-50 backdrop-blur-xl bg-bg-tertiary/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-white flex items-center gap-2 hover:opacity-80 transition-opacity">
              🚀 Web3 Alpha Hunter
            </Link>
          </div>

          {/* 导航链接 */}
          <div className="flex items-center space-x-1">
            {/* 公共菜单 */}
            {publicNavItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-4 py-2 rounded-lg transition-colors whitespace-nowrap ${
                  pathname === item.href
                    ? 'bg-accent-primary/20 text-accent-primary'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                {item.label}
              </Link>
            ))}

            {/* 管理员下拉菜单 */}
            {isAdmin() && (
              <div className="relative" ref={adminMenuRef}>
                <button
                  onClick={() => setAdminMenuOpen(!adminMenuOpen)}
                  className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5 whitespace-nowrap ${
                    adminNavItems.some(item => pathname === item.href)
                      ? 'bg-red-500/20 text-red-400'
                      : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                  }`}
                >
                  <span className="text-xs">🔒</span>
                  <span>管理员</span>
                  <svg 
                    className={`w-4 h-4 transition-transform ${adminMenuOpen ? 'rotate-180' : ''}`} 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* 下拉菜单面板 */}
                {adminMenuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-bg-secondary border border-gray-700 rounded-lg shadow-2xl py-2 z-50">
                    <div className="px-3 py-2 text-xs text-gray-400 border-b border-gray-700 mb-1">
                      🔐 管理员专属功能
                    </div>
                    {adminNavItems.map((item) => (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={`flex items-center gap-3 px-4 py-2.5 transition-colors ${
                          pathname === item.href
                            ? 'bg-accent-primary/10 text-accent-primary'
                            : 'text-text-secondary hover:text-text-primary hover:bg-bg-tertiary'
                        }`}
                        onClick={() => setAdminMenuOpen(false)}
                      >
                        <span className="text-lg">{item.icon}</span>
                        <span>{item.label}</span>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 用户信息和登出 - 也做成下拉菜单 */}
          <div className="relative" ref={userMenuRef}>
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-bg-secondary transition-colors"
            >
              <div className="flex items-center gap-2 text-sm text-gray-300">
                <span>👤 {user?.username}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                  user?.role === 'admin' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-blue-500 text-white'
                }`}>
                  {user?.role === 'admin' ? '管理员' : '用户'}
                </span>
              </div>
              <svg 
                className={`w-4 h-4 text-gray-400 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* 用户下拉菜单 */}
            {userMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-bg-secondary border border-gray-700 rounded-lg shadow-2xl py-2 z-50">
                <div className="px-4 py-2 text-xs text-gray-400 border-b border-gray-700 mb-1">
                  账户信息
                </div>
                <div className="px-4 py-2 text-sm text-gray-300">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-gray-500">用户名:</span>
                    <span className="text-white">{user?.username}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">邮箱:</span>
                    <span className="text-white text-xs">{user?.email}</span>
                  </div>
                </div>
                <div className="border-t border-gray-700 mt-2 pt-2">
                  <button
                    onClick={() => {
                      setUserMenuOpen(false)
                      handleLogout()
                    }}
                    className="w-full px-4 py-2 text-left text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-2"
                  >
                    <span>🚪</span>
                    <span>退出登录</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
