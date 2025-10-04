/**
 * 用户认证状态管理 - Zustand (支持角色)
 */

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'  // 添加角色
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
  isAdmin: () => boolean  // 新增判断管理员权限
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        try {
          // 模拟API调用延迟
          await new Promise(resolve => setTimeout(resolve, 500))

          // 只在客户端访问localStorage
          if (typeof window === 'undefined') {
            return false
          }

          // 从localStorage获取所有用户
          const usersData = localStorage.getItem('users-storage')
          if (!usersData) {
            console.error('用户数据未初始化')
            return false
          }

          const parsed = JSON.parse(usersData)
          const users: UserWithPassword[] = parsed.state?.users || parsed.users || []

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
        } catch (error) {
          console.error('登录错误:', error)
          return false
        }
      },

      logout: () => {
        set({ user: null, isAuthenticated: false })
      },

      checkAuth: () => {
        return get().isAuthenticated
      },

      isAdmin: () => {
        const state = get()
        return state.user?.role === 'admin'
      }
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => {
        if (typeof window === 'undefined') {
          return {
            getItem: () => null,
            setItem: () => {},
            removeItem: () => {},
          }
        }
        return localStorage
      }),
      skipHydration: false,
    }
  )
)
