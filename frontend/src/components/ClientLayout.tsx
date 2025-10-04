/**
 * 客户端布局组件 - 测试版
 */

"use client"

import { TestNav } from './TestNav'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <TestNav />
      {children}
    </>
  )
}

