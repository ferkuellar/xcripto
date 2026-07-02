/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#05070D',
        surface: {
          DEFAULT: '#0B1020',
          elevated: '#111827',
        },
        line: 'rgba(255,255,255,0.08)',
        ink: {
          DEFAULT: '#F8FAFC',
          secondary: '#94A3B8',
          muted: '#64748B',
        },
        accent: {
          cyan: '#00E5FF',
          green: '#22C55E',
          yellow: '#FACC15',
          red: '#EF4444',
          purple: '#8B5CF6',
          orange: '#FB923C',
          blue: '#38BDF8',
        },
        // Chart series palette — fixed order, validated for CVD separation
        // and 3:1 contrast on the #0B1020 surface. Never reorder or cycle.
        chart: {
          1: '#0891B2',
          2: '#DB2777',
          3: '#B45309',
          4: '#8B5CF6',
          5: '#059669',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Consolas', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.6875rem', { lineHeight: '1rem' }],
      },
      boxShadow: {
        glow: '0 0 24px rgba(0,229,255,0.08)',
        card: '0 1px 2px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.25)',
      },
      borderRadius: {
        xl: '0.875rem',
      },
    },
  },
  plugins: [],
}
