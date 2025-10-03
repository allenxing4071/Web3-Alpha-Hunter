import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // 背景色
        'bg-primary': '#0A0E27',
        'bg-secondary': '#141B34',
        'bg-tertiary': '#1E2847',
        
        // 强调色
        'accent-primary': '#00D4FF',
        'accent-gold': '#FFD700',
        'accent-purple': '#A855F7',
        
        // 功能色
        success: '#10B981',
        danger: '#EF4444',
        warning: '#F59E0B',
        info: '#3B82F6',
        
        // 文字色
        'text-primary': '#F9FAFB',
        'text-secondary': '#9CA3AF',
        'text-tertiary': '#6B7280',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}
export default config

