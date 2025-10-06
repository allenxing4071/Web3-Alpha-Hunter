/**
 * API客户端
 */

import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use((config) => {
  // 可以在这里添加token
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 统一错误处理
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API方法
export const projectsApi = {
  list: (params: any) => api.get('/projects', { params }),
  getById: (id: string) => api.get(`/projects/${id}`),
  getHistory: (id: string, params: any) => api.get(`/projects/${id}/history`, { params }),
}

// 用户API
export const usersApi = {
  login: (username: string, password: string) => 
    api.post('/users/login', { username, password }),
  list: () => api.get('/users'),
  getById: (id: string) => api.get(`/users/${id}`),
  create: (data: any) => api.post('/users', data),
  update: (id: string, data: any) => api.put(`/users/${id}`, data),
  delete: (id: string) => api.delete(`/users/${id}`),
  initDefault: () => api.post('/users/init-default'),
}

