/**
 * 全局认证保护组件
 * 所有非登录页都需要认证
 */

"use client"

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'

export function AuthProtection({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const [isChecking, setIsChecking] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    // 登录页不需要检查
    if (pathname === '/login') {
      setIsChecking(false)
      setIsAuthenticated(true)
      return
    }

    // 检查认证状态
    if (typeof window !== 'undefined') {
      const token = sessionStorage.getItem('auth_token')
      
      if (token === 'authenticated') {
        setIsAuthenticated(true)
        setIsChecking(false)
      } else {
        // 未登录，强制跳转到登录页
        console.log('🔒 未登录，跳转到登录页')
        window.location.href = '/login'
      }
    }
  }, [pathname])

  // 登录页直接显示
  if (pathname === '/login') {
    return <>{children}</>
  }

  // 检查中显示加载
  if (isChecking) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">验证身份中...</p>
        </div>
      </div>
    )
  }

  // 已认证显示内容
  if (isAuthenticated) {
    return <>{children}</>
  }

  // 未认证返回null (会跳转)
  return null
}

