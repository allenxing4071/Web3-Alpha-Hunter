/**
 * 风险标签组件
 */

import { cn } from "@/lib/utils"
import { RiskFlag } from "@/types/project"

interface RiskTagProps {
  risk: RiskFlag
  className?: string
}

const severityStyles = {
  high: {
    bg: "bg-red-900/20",
    border: "border-red-500/40",
    text: "text-red-400",
    icon: "🔴"
  },
  medium: {
    bg: "bg-yellow-900/20",
    border: "border-yellow-500/40",
    text: "text-yellow-400",
    icon: "⚠️"
  },
  low: {
    bg: "bg-green-900/20",
    border: "border-green-500/40",
    text: "text-green-400",
    icon: "✅"
  }
}

export function RiskTag({ risk, className }: RiskTagProps) {
  const style = severityStyles[risk.severity]
  
  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full border text-xs font-medium",
        style.bg,
        style.border,
        style.text,
        className
      )}
    >
      <span>{style.icon}</span>
      <span>{risk.message}</span>
    </div>
  )
}

