"use client"

import { AuthGuard } from '@/components/AuthGuard'
import { Navbar } from '@/components/Navbar'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthGuard>
      <Navbar />
      {children}
    </AuthGuard>
  )
}
