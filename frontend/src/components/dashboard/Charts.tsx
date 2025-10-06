/**
 * 图表组件 - 等级分布和类别统计
 * 使用Recharts实现数据可视化
 */

'use client'

import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { GradeDistribution, CategoryStats } from '@/hooks/useDashboardData'
import { TrendingUp, BarChart3 } from 'lucide-react'

interface GradeDistributionProps {
  data: {
    distribution: GradeDistribution[]
    total: number
  } | null | undefined
}

interface CategoryStatsProps {
  data: {
    categories: CategoryStats[]
    total_categories: number
  } | null | undefined
}

const GRADE_COLORS = {
  S: '#FFD700', // 金色
  A: '#A855F7', // 紫色
  B: '#3B82F6', // 蓝色
  C: '#6B7280'  // 灰色
}

export function GradeDistributionChart({ data }: GradeDistributionProps) {
  if (!data || !data.distribution || data.distribution.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 mr-2 text-accent-primary" />
          项目等级分布
        </h3>
        <div className="h-64 flex items-center justify-center">
          <div className="text-text-secondary">加载中...</div>
        </div>
      </div>
    )
  }

  const chartData = data.distribution.map(item => ({
    name: `${item.grade}级`,
    value: item.count,
    percent: item.percent
  }))

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-accent-primary" />
        项目等级分布
      </h3>

      <ResponsiveContainer width="100%" height={335}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${percent}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => {
              const grade = entry.name.charAt(0)
              return (
                <Cell 
                  key={`cell-${index}`} 
                  fill={GRADE_COLORS[grade as keyof typeof GRADE_COLORS] || GRADE_COLORS.C} 
                />
              )
            })}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1f2937', 
              border: '1px solid #374151',
              borderRadius: '8px'
            }}
          />
        </PieChart>
      </ResponsiveContainer>

      {/* 统计信息 */}
      <div className="mt-4 grid grid-cols-4 gap-2 text-center">
        {data.distribution.map(item => (
          <div key={item.grade} className="p-2 bg-bg-tertiary rounded">
            <div className="text-2xl font-bold" style={{ color: GRADE_COLORS[item.grade as keyof typeof GRADE_COLORS] }}>
              {item.count}
            </div>
            <div className="text-xs text-text-secondary">{item.grade}级项目</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export function CategoryStatsChart({ data }: CategoryStatsProps) {
  if (!data || !data.categories || data.categories.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-accent-primary" />
          类别分布统计
        </h3>
        <div className="h-64 flex items-center justify-center">
          <div className="text-text-secondary">加载中...</div>
        </div>
      </div>
    )
  }

  // 取前8个类别
  const chartData = data.categories.slice(0, 8).map(item => ({
    category: item.category,
    count: item.count,
    高分项目: item.high_grade_count,
    avgScore: item.avg_score
  }))

  return (
    <div className="bg-bg-secondary rounded-xl border border-gray-700 p-6">
      <h3 className="text-xl font-bold text-text-primary mb-4 flex items-center">
        <BarChart3 className="w-5 h-5 mr-2 text-accent-primary" />
        类别分布统计
      </h3>

      <ResponsiveContainer width="100%" height={335}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="category" 
            stroke="#9CA3AF"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#9CA3AF" style={{ fontSize: '12px' }} />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1f2937', 
              border: '1px solid #374151',
              borderRadius: '8px'
            }}
            formatter={(value: any, name: string) => {
              if (name === '高分项目') return [value, 'S/A级项目']
              return [value, name]
            }}
          />
          <Legend />
          <Bar dataKey="count" fill="#3B82F6" name="项目总数" radius={[8, 8, 0, 0]} />
          <Bar dataKey="高分项目" fill="#FFD700" name="高分项目" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      {/* 类别列表 */}
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
        {data.categories.slice(0, 6).map(item => (
          <div key={item.category} className="flex justify-between p-2 bg-bg-tertiary rounded">
            <span className="text-text-secondary">{item.category}</span>
            <span className="text-text-primary font-semibold">{item.count}个</span>
          </div>
        ))}
      </div>
    </div>
  )
}

