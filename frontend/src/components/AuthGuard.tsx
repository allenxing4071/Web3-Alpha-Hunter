/**
 * 认证守卫组件 - 保护需要登录的页面
 */

"use client"

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'

interface AuthGuardProps {
  children: React.ReactNode
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { isAuthenticated } = useAuthStore()
  const [isLoading, setIsLoading] = useState(true)
  const [isMounted, setIsMounted] = useState(false)

  // 第一个 useEffect: 标记组件已挂载（只在客户端运行）
  useEffect(() => {
    setIsMounted(true)
    // 给一个短暂的时间让Zustand从localStorage恢复状态
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 100)

    return () => clearTimeout(timer)
  }, [])

  // 第二个 useEffect: 处理路由跳转（只在客户端且挂载后）
  useEffect(() => {
    if (!isMounted || isLoading) return

    // 只在加载完成后才检查认证状态
    if (!isAuthenticated && pathname !== '/login') {
      router.push('/login')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoading, isAuthenticated, pathname, isMounted])

  // 服务端渲染或未挂载时，显示加载状态
  if (!isMounted || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">正在加载...</p>
        </div>
      </div>
    )
  }

  // 如果未登录且不在登录页,显示加载界面(即将跳转)
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

