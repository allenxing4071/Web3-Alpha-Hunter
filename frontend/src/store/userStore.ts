/**
 * 用户数据管理 - 简化版本
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

interface UserState {
  users: UserWithPassword[]
  addUser: (user: Omit<UserWithPassword, 'id' | 'createdAt'>) => boolean
  updateUser: (id: string, user: Partial<Omit<UserWithPassword, 'id' | 'createdAt'>>) => boolean
  deleteUser: (id: string) => boolean
  getUsers: () => UserWithPassword[]
  initializeDefaultUsers: () => void
}

// 默认用户
const DEFAULT_USERS: UserWithPassword[] = [
  {
    id: '1',
    username: 'admin',
    password: 'admin123',
    email: 'admin@web3hunter.com',
    role: 'admin',
    createdAt: new Date().toISOString()
  }
]

export const useUserStore = create<UserState>((set, get) => ({
  users: [],

  initializeDefaultUsers: () => {
    if (typeof window === 'undefined') return
    
    try {
      const stored = sessionStorage.getItem('app_users')
      if (stored) {
        const users = JSON.parse(stored)
        set({ users })
      } else {
        sessionStorage.setItem('app_users', JSON.stringify(DEFAULT_USERS))
        set({ users: DEFAULT_USERS })
      }
    } catch (error) {
      console.error('初始化用户失败:', error)
      set({ users: DEFAULT_USERS })
    }
  },

  addUser: (user) => {
    const users = get().users
    
    if (users.some(u => u.username === user.username)) {
      return false
    }

    const newUser: UserWithPassword = {
      ...user,
      id: Date.now().toString(),
      createdAt: new Date().toISOString()
    }

    const newUsers = [...users, newUser]
    set({ users: newUsers })
    
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem('app_users', JSON.stringify(newUsers))
      } catch (error) {
        console.error('保存用户失败:', error)
      }
    }
    
    return true
  },

  updateUser: (id, updates) => {
    const users = get().users
    const userIndex = users.findIndex(u => u.id === id)

    if (userIndex === -1) {
      return false
    }

    if (updates.username) {
      const exists = users.some(u => u.id !== id && u.username === updates.username)
      if (exists) {
        return false
      }
    }

    const updatedUsers = [...users]
    updatedUsers[userIndex] = {
      ...updatedUsers[userIndex],
      ...updates
    }

    set({ users: updatedUsers })
    
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem('app_users', JSON.stringify(updatedUsers))
      } catch (error) {
        console.error('更新用户失败:', error)
      }
    }
    
    return true
  },

  deleteUser: (id) => {
    const users = get().users
    
    const user = users.find(u => u.id === id)
    if (user && user.role === 'admin') {
      return false
    }
    
    if (users.length <= 1) {
      return false
    }

    const newUsers = users.filter(u => u.id !== id)
    set({ users: newUsers })
    
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem('app_users', JSON.stringify(newUsers))
      } catch (error) {
        console.error('删除用户失败:', error)
      }
    }
    
    return true
  },

  getUsers: () => {
    return get().users
  }
}))
