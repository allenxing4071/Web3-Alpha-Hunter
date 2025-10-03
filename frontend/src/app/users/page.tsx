/**
 * 用户管理页面 - 完整的CRUD功能
 */

"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useUserStore, UserWithPassword } from '@/store/userStore'

export default function UsersPage() {
  const { users, addUser, updateUser, deleteUser, initializeDefaultUsers } = useUserStore()

  const [showAddForm, setShowAddForm] = useState(false)
  const [editingUser, setEditingUser] = useState<UserWithPassword | null>(null)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // 初始化默认用户
  useEffect(() => {
    initializeDefaultUsers()
  }, [initializeDefaultUsers])

  const resetForm = () => {
    setFormData({ username: '', email: '', password: '' })
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

    if (formData.password && formData.password.length < 6) {
      setError('密码至少6位')
      return
    }

    if (editingUser) {
      // 更新用户
      const updates: Partial<Omit<UserWithPassword, 'id' | 'createdAt'>> = {
        username: formData.username,
        email: formData.email,
      }
      if (formData.password) {
        updates.password = formData.password
      }

      const result = updateUser(editingUser.id, updates)
      if (result) {
        setSuccess(`用户 ${formData.username} 更新成功!`)
        setTimeout(resetForm, 1500)
      } else {
        setError('用户名已存在或更新失败')
      }
    } else {
      // 添加用户
      const result = addUser({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      })

      if (result) {
        setSuccess(`用户 ${formData.username} 添加成功!`)
        setTimeout(resetForm, 1500)
      } else {
        setError('用户名已存在')
      }
    }
  }

  const handleEdit = (user: UserWithPassword) => {
    setEditingUser(user)
    setFormData({
      username: user.username,
      email: user.email,
      password: '',
    })
    setShowAddForm(true)
    setError('')
    setSuccess('')
  }

  const handleDelete = (user: UserWithPassword) => {
    // 禁止删除管理员账号
    if (user.username === 'admin' || user.id === '1') {
      setError('❌ 不能删除管理员账号!')
      setTimeout(() => setError(''), 3000)
      return
    }

    if (users.length <= 1) {
      setError('不能删除最后一个用户!')
      setTimeout(() => setError(''), 3000)
      return
    }

    if (confirm(`确定要删除用户 "${user.username}" 吗?`)) {
      const result = deleteUser(user.id)
      if (result) {
        setSuccess(`用户 ${user.username} 已删除!`)
        setTimeout(() => setSuccess(''), 3000)
      } else {
        setError('删除失败')
        setTimeout(() => setError(''), 3000)
      }
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        {/* 全局提示 */}
        {(error || success) && (
          <div className="fixed top-20 right-4 z-50 animate-in slide-in-from-right">
            {error && (
              <div className="bg-danger/90 backdrop-blur-xl border border-danger text-white px-6 py-4 rounded-lg shadow-2xl mb-2">
                ❌ {error}
              </div>
            )}
            {success && (
              <div className="bg-success/90 backdrop-blur-xl border border-success text-white px-6 py-4 rounded-lg shadow-2xl">
                ✅ {success}
              </div>
            )}
          </div>
        )}

        {/* 页面标题 */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
              用户管理
            </h1>
            <p className="text-text-secondary">
              管理系统用户 - 添加、编辑、删除
            </p>
          </div>
          <button
            onClick={() => {
              if (showAddForm) {
                resetForm()
              } else {
                setShowAddForm(true)
              }
            }}
            className="px-6 py-3 bg-accent-primary text-white rounded-lg hover:bg-accent-primary/80 transition-colors"
          >
            {showAddForm ? '取消' : '+ 添加用户'}
          </button>
        </div>

        {/* 添加/编辑用户表单 */}
        {showAddForm && (
          <Card className="mb-8 bg-bg-tertiary border-gray-700 border-2">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>{editingUser ? '编辑用户' : '添加新用户'}</span>
                <button
                  onClick={resetForm}
                  className="text-sm text-text-tertiary hover:text-text-primary"
                >
                  ✕ 关闭
                </button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* 用户名 */}
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      用户名 *
                    </label>
                    <input
                      type="text"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      className="w-full px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-text-primary focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/50 transition-all"
                      placeholder="请输入用户名"
                    />
                  </div>

                  {/* 邮箱 */}
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      邮箱 *
                    </label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="w-full px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-text-primary focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/50 transition-all"
                      placeholder="user@example.com"
                    />
                  </div>

                  {/* 密码 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      密码 {editingUser ? '(留空表示不修改)' : '*'} (至少6位)
                    </label>
                    <input
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className="w-full px-4 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-text-primary focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/50 transition-all"
                      placeholder={editingUser ? '留空表示不修改密码' : '请输入密码'}
                    />
                  </div>
                </div>

                {/* 提交按钮 */}
                <div className="flex gap-3">
                  <button
                    type="submit"
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-accent-primary to-accent-purple text-white rounded-lg hover:shadow-lg hover:shadow-accent-primary/50 transition-all font-semibold"
                  >
                    {editingUser ? '💾 保存修改' : '➕ 添加用户'}
                  </button>
                  <button
                    type="button"
                    onClick={resetForm}
                    className="px-6 py-3 bg-bg-secondary text-text-secondary rounded-lg hover:bg-gray-700 transition-all"
                  >
                    取消
                  </button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* 用户列表 */}
        <Card className="bg-bg-tertiary border-gray-700">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>用户列表</span>
              <span className="text-sm text-text-secondary">共 {users.length} 个用户</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">ID</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">用户名</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">邮箱</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-semibold">创建时间</th>
                    <th className="text-right py-3 px-4 text-text-secondary font-semibold">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-12 text-center text-text-tertiary">
                        暂无用户数据
                      </td>
                    </tr>
                  ) : (
                    users.map((user) => (
                      <tr key={user.id} className="border-b border-gray-700/50 hover:bg-bg-secondary transition-colors group">
                        <td className="py-3 px-4 text-text-tertiary font-mono text-sm">{user.id}</td>
                        <td className="py-3 px-4">
                          <span className="text-text-primary font-semibold">{user.username}</span>
                          {user.id === '1' && (
                            <span className="ml-2 px-2 py-0.5 bg-accent-gold/20 text-accent-gold text-xs rounded">
                              管理员
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-text-secondary">{user.email}</td>
                        <td className="py-3 px-4 text-text-tertiary text-sm">
                          {new Date(user.createdAt).toLocaleString('zh-CN')}
                        </td>
                        <td className="py-3 px-4">
                          <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={() => handleEdit(user)}
                              className="px-3 py-1.5 bg-accent-primary/20 text-accent-primary rounded hover:bg-accent-primary/30 transition-colors text-sm font-medium"
                            >
                              ✏️ 编辑
                            </button>
                            <button
                              onClick={() => handleDelete(user)}
                              className="px-3 py-1.5 bg-danger/20 text-danger rounded hover:bg-danger/30 transition-colors text-sm font-medium disabled:opacity-30 disabled:cursor-not-allowed"
                              disabled={user.username === 'admin' || user.id === '1' || users.length <= 1}
                              title={
                                user.username === 'admin' || user.id === '1' 
                                  ? '管理员账号不能删除' 
                                  : users.length <= 1 
                                  ? '不能删除最后一个用户' 
                                  : ''
                              }
                            >
                              🗑️ 删除
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

