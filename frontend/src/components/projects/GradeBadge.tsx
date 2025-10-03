/**
 * 项目等级徽章组件
 * S级: 金色发光效果
 * A级: 紫色边框
 * B级: 蓝色边框
 * C级: 灰色
 */

import { cn } from "@/lib/utils"
import { ProjectGrade } from "@/types/project"

interface GradeBadgeProps {
  grade: ProjectGrade
  score: number
  size?: "sm" | "md" | "lg"
  showScore?: boolean
  className?: string
}

const gradeStyles = {
  S: {
    container: "bg-gradient-to-br from-[#FFD700] to-[#FFA500] glow-gold border-2 border-[#FFD700]",
    text: "text-gray-900 font-bold",
    icon: "👑",
    label: "强烈推荐"
  },
  A: {
    container: "bg-gradient-to-br from-[#A855F7] to-[#9333EA] border-2 border-[#A855F7]",
    text: "text-white font-semibold",
    icon: "⭐",
    label: "值得研究"
  },
  B: {
    container: "bg-gradient-to-br from-[#3B82F6] to-[#2563EB] border-2 border-[#3B82F6]",
    text: "text-white font-medium",
    icon: "📊",
    label: "观察阶段"
  },
  C: {
    container: "bg-gray-700 border-2 border-gray-600",
    text: "text-gray-300",
    icon: "⚠️",
    label: "不推荐"
  }
}

const sizeStyles = {
  sm: {
    container: "w-12 h-12 text-xs",
    score: "text-lg",
    grade: "text-xs"
  },
  md: {
    container: "w-16 h-16 text-sm",
    score: "text-2xl",
    grade: "text-sm"
  },
  lg: {
    container: "w-24 h-24 text-base",
    score: "text-4xl",
    grade: "text-lg"
  }
}

export function GradeBadge({ 
  grade, 
  score, 
  size = "md", 
  showScore = true,
  className 
}: GradeBadgeProps) {
  const style = gradeStyles[grade]
  const sizeStyle = sizeStyles[size]
  
  return (
    <div className={cn("relative", className)}>
      <div
        className={cn(
          "rounded-xl flex flex-col items-center justify-center transition-all duration-300",
          "hover:scale-105",
          style.container,
          sizeStyle.container,
          grade === 'S' && "animate-pulse-slow"
        )}
      >
        {showScore && (
          <div className={cn("font-mono", style.text, sizeStyle.score)}>
            {Math.round(score)}
          </div>
        )}
        <div className={cn("font-bold", style.text, sizeStyle.grade)}>
          {grade}
        </div>
      </div>
      
      {/* 等级说明(悬停显示) */}
      <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="bg-gray-800 text-xs text-white px-2 py-1 rounded whitespace-nowrap">
          {style.icon} {style.label}
        </div>
      </div>
    </div>
  )
}

