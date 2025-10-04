"use client"

import { AuthProtection } from '@/components/AuthProtection'
import { Navbar } from '@/components/Navbar'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProtection>
      <Navbar />
      {children}
    </AuthProtection>
  )
}
