/**
 * 用户数据管理 - Zustand
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

interface UserState {
  users: UserWithPassword[]
  addUser: (user: Omit<UserWithPassword, 'id' | 'createdAt'>) => boolean
  updateUser: (id: string, user: Partial<Omit<UserWithPassword, 'id' | 'createdAt'>>) => boolean
  deleteUser: (id: string) => boolean
  getUsers: () => UserWithPassword[]
  initializeDefaultUsers: () => void
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      users: [],

      initializeDefaultUsers: () => {
        const currentUsers = get().users
        if (currentUsers.length === 0) {
          set({
            users: [
              {
                id: '1',
                username: 'admin',
                password: 'admin123',
                email: 'admin@web3hunter.com',
                createdAt: new Date().toISOString()
              }
            ]
          })
        }
      },

      addUser: (user) => {
        const users = get().users
        
        // 检查用户名是否已存在
        if (users.some(u => u.username === user.username)) {
          return false
        }

        const newUser: UserWithPassword = {
          ...user,
          id: Date.now().toString(),
          createdAt: new Date().toISOString()
        }

        set({ users: [...users, newUser] })
        return true
      },

      updateUser: (id, updates) => {
        const users = get().users
        const userIndex = users.findIndex(u => u.id === id)

        if (userIndex === -1) {
          return false
        }

        // 如果更新用户名,检查是否与其他用户冲突
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
        return true
      },

      deleteUser: (id) => {
        const users = get().users
        
        // 不允许删除最后一个用户
        if (users.length <= 1) {
          return false
        }

        set({ users: users.filter(u => u.id !== id) })
        return true
      },

      getUsers: () => {
        return get().users
      }
    }),
    {
      name: 'users-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
)

