/**
 * 客户端布局组件 - 包含简化导航栏
 * 只在客户端渲染,避免SSR问题
 */

"use client"

import { SimpleNavbar } from './SimpleNavbar'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SimpleNavbar />
      {children}
    </>
  )
}

