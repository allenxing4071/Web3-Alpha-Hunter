/**
 * 项目卡片骨架屏组件
 * 用于优化加载体验
 */

export function ProjectCardSkeleton() {
  return (
    <div className="bg-bg-tertiary border border-gray-700 rounded-lg p-6 animate-pulse">
      {/* 头部 - 等级和评分 */}
      <div className="flex items-start justify-between mb-4">
        <div className="w-12 h-12 bg-gray-700 rounded-full"></div>
        <div className="text-right">
          <div className="w-16 h-6 bg-gray-700 rounded mb-2"></div>
          <div className="w-20 h-4 bg-gray-700 rounded"></div>
        </div>
      </div>

      {/* 项目名称和Symbol */}
      <div className="mb-4">
        <div className="w-3/4 h-6 bg-gray-700 rounded mb-2"></div>
        <div className="w-1/2 h-4 bg-gray-700 rounded"></div>
      </div>

      {/* 描述 */}
      <div className="space-y-2 mb-4">
        <div className="w-full h-4 bg-gray-700 rounded"></div>
        <div className="w-5/6 h-4 bg-gray-700 rounded"></div>
      </div>

      {/* 标签 */}
      <div className="flex gap-2 mb-4">
        <div className="w-16 h-6 bg-gray-700 rounded-full"></div>
        <div className="w-20 h-6 bg-gray-700 rounded-full"></div>
      </div>

      {/* 指标 */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <div className="w-16 h-3 bg-gray-700 rounded mb-1"></div>
          <div className="w-20 h-5 bg-gray-700 rounded"></div>
        </div>
        <div>
          <div className="w-16 h-3 bg-gray-700 rounded mb-1"></div>
          <div className="w-20 h-5 bg-gray-700 rounded"></div>
        </div>
      </div>

      {/* 按钮 */}
      <div className="w-full h-10 bg-gray-700 rounded"></div>
    </div>
  )
}
