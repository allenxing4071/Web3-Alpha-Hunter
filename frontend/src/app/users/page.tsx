/**
 * 用户管理页面 - 连接真实数据库API
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { usersApi } from '@/lib/api'

interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'
  is_active: boolean
  created_at: string
  updated_at: string
  last_login_at?: string
}

export default function UsersPage() {
  const router = useRouter()
  const { isAuthenticated, isAdmin } = useAuthStore()
  
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'user' as 'admin' | 'user',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // 检查权限
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    
    if (!isAdmin()) {
      router.push('/')
      return
    }

    loadUsers()
  }, [isAuthenticated, isAdmin, router])

  // 加载用户列表
  const loadUsers = async () => {
    try {
      setLoading(true)
      const response = await usersApi.list()
      setUsers(response.data || response)
    } catch (error) {
      console.error('加载用户失败:', error)
      setError('加载用户列表失败')
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({ username: '', email: '', password: '', role: 'user' })
    setError('')
    setSuccess('')
    setShowAddForm(false)
    setEditingUser(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // 验证
    if (!formData.username || !formData.email) {
      setError('用户名和邮箱必填')
      return
    }

    // 编辑模式下,密码可选
    if (!editingUser && !formData.password) {
      setError('密码必填')
      return
    }

    try {
      if (editingUser) {
        // 更新用户
        const updates: any = {
          username: formData.username,
          email: formData.email,
          role: formData.role,
        }
        
        // 如果提供了新密码,则更新密码
        if (formData.password) {
          updates.password = formData.password
        }

        await usersApi.update(editingUser.id, updates)
        setSuccess('用户更新成功')
      } else {
        // 添加新用户
        await usersApi.create({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          role: formData.role,
        })
        setSuccess('用户添加成功')
      }

      // 重新加载用户列表
      await loadUsers()
      setTimeout(resetForm, 1500)
    } catch (error: any) {
      console.error('操作失败:', error)
      setError(error.response?.data?.detail || '操作失败')
    }
  }

  const handleEdit = (user: User) => {
    setEditingUser(user)
    setFormData({
      username: user.username,
      email: user.email,
      password: '', // 编辑时不显示密码
      role: user.role,
    })
    setShowAddForm(true)
    setError('')
    setSuccess('')
  }

  const handleDelete = async (id: string) => {
    const user = users.find(u => u.id === id)
    
    // 防止删除管理员
    if (user && user.role === 'admin') {
      setError('不能删除管理员用户')
      setTimeout(() => setError(''), 3000)
      return
    }

    if (confirm('确定要删除此用户吗?')) {
      try {
        await usersApi.delete(id)
        setSuccess('用户删除成功')
        setTimeout(() => setSuccess(''), 3000)
        await loadUsers()
      } catch (error: any) {
        console.error('删除失败:', error)
        setError(error.response?.data?.detail || '删除失败')
        setTimeout(() => setError(''), 3000)
      }
    }
  }

  if (!isAuthenticated || !isAdmin()) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">验证权限中...</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-bg-primary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">加载用户数据...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            👥 用户管理
          </h1>
          <p className="text-text-secondary">
            管理系统用户与权限（仅管理员可见）
          </p>
        </div>

        <div className="bg-bg-tertiary border border-gray-700 rounded-lg overflow-hidden">
          {/* Top Bar */}
          <div className="px-6 py-4 border-b border-gray-700 flex justify-between items-center">
            <div className="text-text-primary font-semibold">
              用户列表 · 共 {users.length} 个用户
            </div>
            <button
              onClick={() => {
                resetForm()
                setShowAddForm(!showAddForm)
              }}
              className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition-colors"
            >
              {showAddForm ? '✕ 取消' : '+ 添加用户'}
            </button>
          </div>

          <div className="p-6">
            {/* 成功/错误提示 */}
            {error && (
              <div className="mb-4 p-4 bg-red-500/20 border border-red-500 text-red-200 rounded-lg">
                ❌ {error}
              </div>
            )}

            {success && (
              <div className="mb-4 p-4 bg-green-500/20 border border-green-500 text-green-200 rounded-lg">
                ✅ {success}
              </div>
            )}

            {/* 添加/编辑表单 */}
            {showAddForm && (
              <form onSubmit={handleSubmit} className="mb-6 p-6 bg-bg-secondary rounded-lg border border-gray-700">
                <h3 className="text-lg font-semibold text-text-primary mb-4">
                  {editingUser ? '✏️ 编辑用户' : '➕ 添加新用户'}
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-300 mb-2">
                      用户名 <span className="text-red-400">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-600 text-white rounded-lg focus:border-accent-primary focus:outline-none"
                      placeholder="输入用户名"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">
                      邮箱 <span className="text-red-400">*</span>
                    </label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-600 text-white rounded-lg focus:border-accent-primary focus:outline-none"
                      placeholder="user@example.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">
                      密码 {editingUser && <span className="text-gray-500">(留空表示不修改)</span>}
                      {!editingUser && <span className="text-red-400">*</span>}
                    </label>
                    <input
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-600 text-white rounded-lg focus:border-accent-primary focus:outline-none"
                      placeholder={editingUser ? '留空表示不修改' : '输入密码'}
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">
                      角色 <span className="text-red-400">*</span>
                    </label>
                    <select
                      value={formData.role}
                      onChange={(e) => setFormData({ ...formData, role: e.target.value as 'admin' | 'user' })}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-600 text-white rounded-lg focus:border-accent-primary focus:outline-none"
                    >
                      <option value="user">普通用户</option>
                      <option value="admin">管理员</option>
                    </select>
                  </div>
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    type="submit"
                    className="px-6 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition"
                  >
                    {editingUser ? '更新用户' : '添加用户'}
                  </button>
                  <button
                    type="button"
                    onClick={resetForm}
                    className="px-6 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-lg transition"
                  >
                    取消
                  </button>
                </div>
              </form>
            )}

            {/* 用户列表 */}
            <div className="bg-bg-secondary rounded-lg border border-gray-700 overflow-hidden">
              <table className="w-full">
                <thead className="bg-bg-tertiary">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">
                      用户名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">
                      邮箱
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">
                      角色
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">
                      创建时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {users.map((user) => (
                    <tr key={user.id} className="hover:bg-bg-tertiary/50 transition">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-text-primary flex items-center gap-2">
                          {user.username}
                          {user.role === 'admin' && (
                            <span className="px-2 py-0.5 text-xs bg-red-500/20 text-red-400 border border-red-500/50 rounded">
                              管理员
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-text-secondary">{user.email}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-3 py-1 text-xs rounded-full ${
                            user.role === 'admin'
                              ? 'bg-red-500/20 text-red-300'
                              : 'bg-blue-500/20 text-blue-300'
                          }`}
                        >
                          {user.role === 'admin' ? '管理员' : '普通用户'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-text-tertiary">
                          {new Date(user.created_at).toLocaleString('zh-CN')}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleEdit(user)}
                            className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded transition"
                          >
                            编辑
                          </button>
                          <button
                            onClick={() => handleDelete(user.id)}
                            disabled={user.role === 'admin' || users.length <= 1}
                            className={`px-3 py-1 rounded transition ${
                              user.role === 'admin' || users.length <= 1
                                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                                : 'bg-red-600 hover:bg-red-500 text-white'
                            }`}
                            title={
                              user.role === 'admin'
                                ? '不能删除管理员'
                                : users.length <= 1
                                ? '不能删除唯一用户'
                                : '删除用户'
                            }
                          >
                            删除
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {users.length === 0 && (
                <div className="text-center py-12 text-text-secondary">
                  <div className="text-6xl mb-4">👥</div>
                  <p>暂无用户数据</p>
                </div>
              )}
            </div>

            <div className="mt-6 p-4 bg-info/10 border border-info/50 rounded-lg">
              <p className="text-sm text-info">
                <strong>💡 提示:</strong> 管理员用户不能被删除。至少需要保留一个用户账号。
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
