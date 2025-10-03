/**
 * 评分雷达图组件
 */

"use client"

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts'
import { ProjectScores } from '@/types/project'

interface ScoreRadarProps {
  scores: ProjectScores
  className?: string
}

export function ScoreRadar({ scores, className }: ScoreRadarProps) {
  const data = [
    {
      dimension: '团队背景',
      score: scores.team,
      fullMark: 100,
    },
    {
      dimension: '技术创新',
      score: scores.technology,
      fullMark: 100,
    },
    {
      dimension: '社区热度',
      score: scores.community,
      fullMark: 100,
    },
    {
      dimension: '代币模型',
      score: scores.tokenomics,
      fullMark: 100,
    },
    {
      dimension: '市场时机',
      score: scores.market_timing,
      fullMark: 100,
    },
    {
      dimension: '风险控制',
      score: scores.risk,
      fullMark: 100,
    },
  ]

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={data}>
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis 
            dataKey="dimension" 
            tick={{ fill: '#9CA3AF', fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]}
            tick={{ fill: '#6B7280', fontSize: 10 }}
          />
          <Radar
            name="当前项目"
            dataKey="score"
            stroke="#00D4FF"
            fill="#00D4FF"
            fillOpacity={0.6}
          />
          <Legend 
            wrapperStyle={{ color: '#9CA3AF' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}

