/**
 * 认证守卫组件 - 保护需要登录的页面
 */

"use client"

import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'

interface AuthGuardProps {
  children: React.ReactNode
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    // 如果未登录且不在登录页,重定向到登录页
    if (!isAuthenticated && pathname !== '/login') {
      router.push('/login')
    }
  }, [isAuthenticated, pathname, router])

  // 如果未登录,不渲染内容
  if (!isAuthenticated && pathname !== '/login') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">正在验证身份...</p>
        </div>
      </div>
    )
  }

  return <>{children}</>
}

