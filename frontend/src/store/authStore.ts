/**
 * 用户认证状态管理 - Zustand
 */

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export interface User {
  id: string
  username: string
  email: string
  createdAt: string
}

export interface UserWithPassword extends User {
  password: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<boolean>
  logout: () => void
  checkAuth: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 500))

        // 从localStorage获取所有用户
        const usersData = localStorage.getItem('users-storage')
        const users: UserWithPassword[] = usersData ? JSON.parse(usersData).state.users : []

        // 验证用户
        const user = users.find(
          u => u.username === username && u.password === password
        )

        if (user) {
          const { password: _, ...userWithoutPassword } = user
          set({ user: userWithoutPassword, isAuthenticated: true })
          return true
        }

        return false
      },

      logout: () => {
        set({ user: null, isAuthenticated: false })
      },

      checkAuth: () => {
        return get().isAuthenticated
      }
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
)

