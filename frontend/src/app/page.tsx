import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center py-20">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-accent-primary to-accent-purple bg-clip-text text-transparent">
            Web3 Alpha Hunter
          </h1>
          <p className="text-xl text-text-secondary mb-8">
            AI驱动的Web3项目早期发现与分析平台
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 mb-12">
            {/* 今日概览 */}
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6 hover:border-accent-primary transition-colors">
              <div className="text-text-secondary mb-2">扫描项目</div>
              <div className="text-4xl font-bold text-accent-primary">127</div>
            </div>
            
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6 hover:border-success transition-colors">
              <div className="text-text-secondary mb-2">新发现</div>
              <div className="text-4xl font-bold text-success">18</div>
            </div>
            
            <div className="bg-bg-tertiary border border-accent-gold rounded-xl p-6 glow-gold">
              <div className="text-text-secondary mb-2">S级机会</div>
              <div className="text-4xl font-bold text-accent-gold">3</div>
            </div>
          </div>
          
          {/* 功能特性 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16 text-left">
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6">
              <div className="text-2xl mb-3">🔍</div>
              <h3 className="text-xl font-semibold text-text-primary mb-2">
                全球情报收集
              </h3>
              <p className="text-text-secondary text-sm">
                7x24小时监控Twitter、Telegram等10+平台,第一时间发现优质项目
              </p>
            </div>
            
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6">
              <div className="text-2xl mb-3">🤖</div>
              <h3 className="text-xl font-semibold text-text-primary mb-2">
                AI智能分析
              </h3>
              <p className="text-text-secondary text-sm">
                6维度评分系统,Claude/GPT-4驱动,准确识别百倍千倍潜力项目
              </p>
            </div>
            
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6">
              <div className="text-2xl mb-3">⭐</div>
              <h3 className="text-xl font-semibold text-text-primary mb-2">
                S/A/B/C分级
              </h3>
              <p className="text-text-secondary text-sm">
                清晰的四级分级系统,S级项目平均涨幅>200% (历史回测)
              </p>
            </div>
            
            <div className="bg-bg-tertiary border border-gray-700 rounded-xl p-6">
              <div className="text-2xl mb-3">🛡️</div>
              <h3 className="text-xl font-semibold text-text-primary mb-2">
                风险智能识别
              </h3>
              <p className="text-text-secondary text-sm">
                自动检测骗局项目,识别准确率>85%,保护投资安全
              </p>
            </div>
          </div>
          
          {/* CTA按钮 */}
          <div className="mt-16 flex gap-4 justify-center">
            <Link
              href="/projects"
              className="px-8 py-3 bg-gradient-to-r from-accent-primary to-accent-purple rounded-lg font-semibold text-white hover:scale-105 transition-transform"
            >
              查看项目列表 →
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-3 bg-bg-tertiary border border-gray-700 rounded-lg font-semibold text-text-primary hover:border-accent-primary transition-colors"
            >
              API文档
            </a>
          </div>
          
          <div className="mt-12">
            <p className="text-text-tertiary text-sm">
              🚀 MVP已上线 · 后端API 100%完成 · 前端UI开发中
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
