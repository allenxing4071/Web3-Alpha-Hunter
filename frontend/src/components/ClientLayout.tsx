/**
 * 客户端布局组件 - 包含认证保护和导航栏
 */

"use client"

import { SimpleNavbar } from './SimpleNavbar'
import { AuthProtection } from './AuthProtection'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProtection>
      <SimpleNavbar />
      {children}
    </AuthProtection>
  )
}

