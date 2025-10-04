/**
 * 客户端布局组件 - 包含导航栏
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

