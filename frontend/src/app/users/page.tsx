/**
 * 用户管理页面 - 完整的CRUD功能 (支持角色管理)
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useUserStore, UserWithPassword } from '@/store/userStore'
import { useAuthStore } from '@/store/authStore'

export default function UsersPage() {
  const router = useRouter()
  const { isAuthenticated, isAdmin } = useAuthStore()
  const { users, addUser, updateUser, deleteUser, initializeDefaultUsers } = useUserStore()

  const [showAddForm, setShowAddForm] = useState(false)
  const [editingUser, setEditingUser] = useState<UserWithPassword | null>(null)
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

    initializeDefaultUsers()
  }, [isAuthenticated, isAdmin, router, initializeDefaultUsers])

  const resetForm = () => {
    setFormData({ username: '', email: '', password: '', role: 'user' })
    setError('')
    setSuccess('')
    setShowAddForm(false)
    setEditingUser(null)
  }

  const handleSubmit = (e: React.FormEvent) => {
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

    let result = false

    if (editingUser) {
      // 更新用户
      const updates: Partial<UserWithPassword> = {
        username: formData.username,
        email: formData.email,
        role: formData.role,
      }
      
      // 如果提供了新密码,则更新密码
      if (formData.password) {
        updates.password = formData.password
      }

      result = updateUser(editingUser.id, updates)
      if (result) {
        setSuccess('用户更新成功')
      } else {
        setError('用户名已存在或更新失败')
      }
    } else {
      // 添加新用户
      result = addUser({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      })
      if (result) {
        setSuccess('用户添加成功')
      } else {
        setError('用户名已存在')
      }
    }

    if (result) {
      setTimeout(resetForm, 1500)
    }
  }

  const handleEdit = (user: UserWithPassword) => {
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

  const handleDelete = (id: string) => {
    const user = users.find(u => u.id === id)
    
    // 防止删除管理员
    if (user && user.role === 'admin') {
      setError('不能删除管理员用户')
      setTimeout(() => setError(''), 3000)
      return
    }

    if (confirm('确定要删除此用户吗?')) {
      const result = deleteUser(id)
      if (result) {
        setSuccess('用户删除成功')
        setTimeout(() => setSuccess(''), 3000)
      } else {
        setError('无法删除唯一用户或管理员')
        setTimeout(() => setError(''), 3000)
      }
    }
  }

  if (!isAuthenticated || !isAdmin()) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-gray-400">验证权限中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-8">
      <div className="max-w-6xl mx-auto">
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader className="border-b border-gray-700">
            <div className="flex justify-between items-center">
              <CardTitle className="text-2xl text-white">
                👥 用户管理 (仅管理员可见)
              </CardTitle>
              <button
                onClick={() => {
                  resetForm()
                  setShowAddForm(!showAddForm)
                }}
                className="px-4 py-2 bg-accent-primary hover:bg-accent-primary/80 text-white rounded-lg transition"
              >
                {showAddForm ? '取消' : '+ 添加用户'}
              </button>
            </div>
          </CardHeader>

          <CardContent className="p-6">
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
              <form onSubmit={handleSubmit} className="mb-6 p-6 bg-gray-700/50 rounded-lg border border-gray-600">
                <h3 className="text-lg font-semibold text-white mb-4">
                  {editingUser ? '编辑用户' : '添加新用户'}
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
            <div className="bg-gray-700/30 rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      用户名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      邮箱
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      角色
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      创建时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {users.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-700/50 transition">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-white flex items-center gap-2">
                          {user.username}
                          {user.role === 'admin' && (
                            <span className="px-2 py-0.5 text-xs bg-red-500 text-white rounded">
                              管理员
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-300">{user.email}</div>
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
                        <div className="text-sm text-gray-400">
                          {new Date(user.createdAt).toLocaleString('zh-CN')}
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
                <div className="text-center py-12 text-gray-400">
                  暂无用户数据
                </div>
              )}
            </div>

            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <p className="text-sm text-blue-200">
                <strong>提示:</strong> 管理员用户不能被删除。至少需要保留一个用户账号。
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
