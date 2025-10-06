/**
 * 数据刷新指示器
 * 显示最后更新时间和手动刷新按钮
 */

import { RefreshCw, WifiOff } from 'lucide-react'
import { useState, useEffect } from 'react'

interface RefreshIndicatorProps {
  lastUpdate: number
  onRefresh: () => Promise<void>
  error?: string | null
}

export function RefreshIndicator({ lastUpdate, onRefresh, error }: RefreshIndicatorProps) {
  const [secondsAgo, setSecondsAgo] = useState(0)
  const [isRefreshing, setIsRefreshing] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      setSecondsAgo(Math.floor((Date.now() - lastUpdate) / 1000))
    }, 1000)

    return () => clearInterval(interval)
  }, [lastUpdate])

  const handleRefresh = async () => {
    setIsRefreshing(true)
    try {
      await onRefresh()
    } finally {
      setIsRefreshing(false)
    }
  }

  const getTimeLabel = () => {
    if (secondsAgo < 10) return '刚刚更新'
    if (secondsAgo < 60) return `${secondsAgo}秒前更新`
    const minutes = Math.floor(secondsAgo / 60)
    return `${minutes}分钟前更新`
  }

  return (
    <div className="flex items-center gap-4">
      {/* 状态指示 */}
      <div className="flex items-center gap-2">
        {error ? (
          <>
            <WifiOff className="w-4 h-4 text-error animate-pulse" />
            <span className="text-sm text-error">连接失败</span>
          </>
        ) : (
          <>
            <div className={`w-2 h-2 rounded-full ${secondsAgo < 15 ? 'bg-success' : 'bg-warning'} animate-pulse`} />
            <span className="text-sm text-text-secondary">
              {getTimeLabel()}
            </span>
          </>
        )}
      </div>

      {/* 手动刷新按钮 */}
      <button
        onClick={handleRefresh}
        disabled={isRefreshing}
        className="
          flex items-center gap-2 px-4 py-2 rounded-lg
          bg-accent-primary hover:bg-accent-primary/80
          text-white font-medium text-sm
          transition-all disabled:opacity-50
        "
      >
        <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
        {isRefreshing ? '刷新中...' : '手动刷新'}
      </button>
    </div>
  )
}

