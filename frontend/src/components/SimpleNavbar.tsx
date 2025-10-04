/**
 * 简化导航栏 - 避免复杂的认证逻辑
 */

"use client"

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'

export function SimpleNavbar() {
  const router = useRouter()
  const pathname = usePathname()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // 登录页不显示
  if (!mounted || pathname === '/login') {
    return null
  }

  // 检查认证状态(在渲染时实时检查)
  const token = typeof window !== 'undefined' ? sessionStorage.getItem('auth_token') : null
  if (token !== 'authenticated') {
    return null
  }

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      sessionStorage.clear()
    }
    router.push('/login')
  }

  return (
    <nav className="bg-bg-tertiary border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* Logo */}
            <Link href="/" className="flex items-center">
              <span className="text-xl font-bold bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
                Web3 Alpha Hunter
              </span>
            </Link>

            {/* 导航链接 */}
            <div className="ml-10 flex items-center space-x-4">
              <Link
                href="/projects"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/projects'
                    ? 'bg-accent-primary text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                项目列表
              </Link>

              <Link
                href="/admin"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/admin'
                    ? 'bg-accent-primary text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                管理面板
              </Link>

              <Link
                href="/users"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/users'
                    ? 'bg-accent-primary text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                用户管理
              </Link>

              <Link
                href="/dashboard"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/dashboard'
                    ? 'bg-accent-primary text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                Dashboard
              </Link>
            </div>
          </div>

          {/* 右侧按钮 */}
          <div className="flex items-center">
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-danger rounded-md hover:bg-bg-secondary"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

