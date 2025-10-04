/**
 * 客户端布局组件 - 包含导航栏
 * 只在客户端渲染,避免SSR问题
 */

"use client"

import { Navbar } from './Navbar'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Navbar />
      {children}
    </>
  )
}

