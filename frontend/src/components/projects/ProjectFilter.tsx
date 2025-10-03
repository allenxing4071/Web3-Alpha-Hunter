/**
 * 项目筛选器组件
 */

"use client"

import { useState } from 'react'
import { ProjectGrade, ProjectCategory } from '@/types/project'
import { cn } from '@/lib/utils'

export interface FilterOptions {
  grade: ProjectGrade | 'all'
  category: ProjectCategory | 'all'
  blockchain: string | 'all'
  minScore: number
  sortBy: 'score' | 'discovered_at'
  order: 'asc' | 'desc'
}

interface ProjectFilterProps {
  filters: FilterOptions
  onFilterChange: (filters: FilterOptions) => void
  className?: string
}

const gradeOptions: { value: ProjectGrade | 'all', label: string, color: string }[] = [
  { value: 'all', label: '全部等级', color: 'text-text-primary' },
  { value: 'S', label: 'S级', color: 'text-accent-gold' },
  { value: 'A', label: 'A级', color: 'text-accent-purple' },
  { value: 'B', label: 'B级', color: 'text-blue-400' },
  { value: 'C', label: 'C级', color: 'text-gray-400' },
]

const categoryOptions: { value: ProjectCategory | 'all', label: string, icon: string }[] = [
  { value: 'all', label: '全部分类', icon: '📊' },
  { value: 'DeFi', label: 'DeFi', icon: '💰' },
  { value: 'NFT', label: 'NFT', icon: '🎨' },
  { value: 'GameFi', label: 'GameFi', icon: '🎮' },
  { value: 'Infrastructure', label: '基础设施', icon: '🏗️' },
  { value: 'AI', label: 'AI', icon: '🤖' },
]

const blockchainOptions = [
  { value: 'all', label: '全部链', icon: '⛓️' },
  { value: 'Ethereum', label: 'Ethereum', icon: '◆' },
  { value: 'Solana', label: 'Solana', icon: '◎' },
  { value: 'Base', label: 'Base', icon: '🔵' },
  { value: 'Polygon', label: 'Polygon', icon: '🟣' },
]

export function ProjectFilter({ filters, onFilterChange, className }: ProjectFilterProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const updateFilter = (key: keyof FilterOptions, value: any) => {
    onFilterChange({
      ...filters,
      [key]: value,
    })
  }

  return (
    <div className={cn("bg-bg-tertiary border border-gray-700 rounded-lg p-6", className)}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-text-primary">筛选条件</h3>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="lg:hidden text-text-secondary hover:text-text-primary"
        >
          {isExpanded ? '收起 ▲' : '展开 ▼'}
        </button>
      </div>

      <div className={cn(
        "space-y-6",
        !isExpanded && "hidden lg:block"
      )}>
        {/* 评分等级 */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-3">
            🎯 评分等级
          </label>
          <div className="space-y-2">
            {gradeOptions.map((option) => (
              <label
                key={option.value}
                className="flex items-center gap-2 cursor-pointer group"
              >
                <input
                  type="radio"
                  name="grade"
                  value={option.value}
                  checked={filters.grade === option.value}
                  onChange={(e) => updateFilter('grade', e.target.value)}
                  className="w-4 h-4 text-accent-primary"
                />
                <span className={cn(
                  "text-sm group-hover:text-accent-primary transition-colors",
                  filters.grade === option.value ? option.color : 'text-text-secondary'
                )}>
                  {option.label}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* 项目分类 */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-3">
            🏷️ 项目分类
          </label>
          <div className="grid grid-cols-2 gap-2">
            {categoryOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => updateFilter('category', option.value)}
                className={cn(
                  "px-3 py-2 rounded-lg text-sm font-medium transition-all",
                  "border hover:scale-105",
                  filters.category === option.value
                    ? "bg-accent-primary/20 border-accent-primary text-accent-primary"
                    : "bg-bg-secondary border-gray-700 text-text-secondary hover:border-accent-primary"
                )}
              >
                {option.icon} {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* 区块链 */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-3">
            ⛓️ 区块链
          </label>
          <div className="space-y-2">
            {blockchainOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => updateFilter('blockchain', option.value)}
                className={cn(
                  "w-full px-3 py-2 rounded-lg text-sm font-medium transition-all text-left",
                  "border",
                  filters.blockchain === option.value
                    ? "bg-accent-purple/20 border-accent-purple text-accent-purple"
                    : "bg-bg-secondary border-gray-700 text-text-secondary hover:border-accent-purple"
                )}
              >
                {option.icon} {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* 最低评分 */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-3">
            📊 最低评分: {filters.minScore}
          </label>
          <input
            type="range"
            min="0"
            max="100"
            step="5"
            value={filters.minScore}
            onChange={(e) => updateFilter('minScore', parseInt(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-primary"
          />
          <div className="flex justify-between text-xs text-text-tertiary mt-1">
            <span>0</span>
            <span>50</span>
            <span>100</span>
          </div>
        </div>

        {/* 排序 */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-3">
            🔄 排序方式
          </label>
          <select
            value={`${filters.sortBy}_${filters.order}`}
            onChange={(e) => {
              const [sortBy, order] = e.target.value.split('_')
              updateFilter('sortBy', sortBy)
              updateFilter('order', order)
            }}
            className="w-full px-3 py-2 bg-bg-secondary border border-gray-700 rounded-lg text-sm text-text-primary focus:border-accent-primary focus:ring-1 focus:ring-accent-primary"
          >
            <option value="score_desc">评分从高到低</option>
            <option value="score_asc">评分从低到高</option>
            <option value="discovered_at_desc">最新发现</option>
            <option value="discovered_at_asc">最早发现</option>
          </select>
        </div>

        {/* 重置按钮 */}
        <button
          onClick={() => onFilterChange({
            grade: 'all',
            category: 'all',
            blockchain: 'all',
            minScore: 0,
            sortBy: 'score',
            order: 'desc',
          })}
          className="w-full px-4 py-2 bg-gray-700 hover:bg-gray-600 text-text-primary rounded-lg text-sm font-medium transition-colors"
        >
          重置筛选
        </button>
      </div>
    </div>
  )
}

