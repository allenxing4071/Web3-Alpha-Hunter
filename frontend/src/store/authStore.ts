/**
 * 用户认证状态管理 - 连接真实数据库API
 */

import { create } from 'zustand'
import { usersApi } from '@/lib/api'

export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'
  created_at: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<boolean>
  logout: () => void
  checkAuth: () => boolean
  isAdmin: () => boolean
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,

  login: async (username: string, password: string) => {
    try {
      console.log('🔐 调用API登录...')
      const response = await usersApi.login(username, password)
      console.log('📊 API响应:', response)
      
      if (response.success && response.user) {
        // 保存到 sessionStorage
        if (typeof window !== 'undefined') {
          try {
            sessionStorage.setItem('auth_user', JSON.stringify(response.user))
            sessionStorage.setItem('auth_token', response.token || 'authenticated')
          } catch (error) {
            console.error('保存认证信息失败:', error)
          }
        }
        
        set({ user: response.user, isAuthenticated: true })
        return true
      }

      return false
    } catch (error: any) {
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
        
        if (token && userStr) {
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
