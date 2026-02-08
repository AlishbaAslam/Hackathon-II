import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        primary: {
          DEFAULT: 'rgb(99, 102, 241)',  // --color-primary: #6366f1
          dark: 'rgb(79, 70, 229)',      // --color-primary-dark: #4f46e5
          light: 'rgb(129, 140, 248)',   // --color-primary-light: #818cf8
        },
        secondary: 'rgb(59, 130, 246)',   // --color-secondary: #3b82f6
        accent: 'rgb(139, 92, 246)',      // --color-accent: #8b5cf6
        'accent-fuchsia': 'rgb(217, 70, 239)', // --color-accent-fuchsia: #d946ef
        success: 'rgb(16, 185, 129)',     // --color-success: #10b981
        error: 'rgb(244, 63, 94)',        // --color-error: #f43f5e
        warning: 'rgb(245, 158, 11)',     // --color-warning: #f59e0b
      },
    },
  },
  plugins: [],
}
export default config