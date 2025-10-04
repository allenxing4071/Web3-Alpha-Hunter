/**
 * 用户认证状态管理 - 简化版本 (移除 persist)
 */

import { create } from 'zustand'

export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'
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
  isAdmin: () => boolean
}

// 默认用户数据
const DEFAULT_USERS: UserWithPassword[] = [
  {
    id: '1',
    username: 'admin',
    password: 'admin123',
    email: 'admin@web3hunter.com',
    role: 'admin',
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    username: 'user',
    password: 'user123',
    email: 'user@web3hunter.com',
    role: 'user',
    createdAt: new Date().toISOString()
  }
]

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,

  login: async (username: string, password: string) => {
    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 300))

      // 只在客户端执行
      if (typeof window === 'undefined') {
        return false
      }

      // 从默认用户或 sessionStorage 获取用户列表
      let users: UserWithPassword[] = DEFAULT_USERS
      
      try {
        const storedUsers = sessionStorage.getItem('app_users')
        if (storedUsers) {
          users = JSON.parse(storedUsers)
        } else {
          // 首次访问,保存默认用户
          sessionStorage.setItem('app_users', JSON.stringify(DEFAULT_USERS))
        }
      } catch (error) {
        console.error('读取用户数据失败:', error)
        // 使用默认用户
      }

      // 验证用户
      const user = users.find(
        u => u.username === username && u.password === password
      )

      if (user) {
        const { password: _, ...userWithoutPassword } = user
        
        // 保存到 sessionStorage
        try {
          sessionStorage.setItem('auth_user', JSON.stringify(userWithoutPassword))
          sessionStorage.setItem('auth_token', 'authenticated')
        } catch (error) {
          console.error('保存认证信息失败:', error)
        }
        
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
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.removeItem('auth_user')
        sessionStorage.removeItem('auth_token')
      } catch (error) {
        console.error('清除认证信息失败:', error)
      }
    }
    set({ user: null, isAuthenticated: false })
  },

  checkAuth: () => {
    const state = get()
    
    // 如果状态中已经有用户,直接返回
    if (state.isAuthenticated && state.user) {
      return true
    }
    
    // 尝试从 sessionStorage 恢复
    if (typeof window !== 'undefined') {
      try {
        const token = sessionStorage.getItem('auth_token')
        const userStr = sessionStorage.getItem('auth_user')
        
        if (token === 'authenticated' && userStr) {
          const user = JSON.parse(userStr)
          set({ user, isAuthenticated: true })
          return true
        }
      } catch (error) {
        console.error('恢复认证状态失败:', error)
      }
    }
    
    return false
  },

  isAdmin: () => {
    const state = get()
    return state.user?.role === 'admin'
  }
}))

// 初始化函数 - 在客户端启动时调用
export function initAuth() {
  if (typeof window !== 'undefined') {
    const store = useAuthStore.getState()
    store.checkAuth()
  }
}
