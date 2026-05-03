/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light theme colors
        'coral': {
          DEFAULT: '#FF6B6B',
          light: '#FF8787',
        },
        'peach': '#FFA94D',
        'amber': {
          DEFAULT: '#FFA94D',
          dark: '#FFB84D',
        },
        'cream': '#FFF8F3',
        'warm-white': '#FFFBF7',
        'warm-gray': '#2D3436',
        // Dark theme colors
        'charcoal': '#1A1A1D',
        'dark-gray': '#2D2D30',
        'warm-white-text': '#FAF3E0',
      },
      fontFamily: {
        'outfit': ['Outfit', 'sans-serif'],
        'space': ['Space Grotesk', 'sans-serif'],
        'clash': ['Clash Display', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(255, 107, 107, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(255, 107, 107, 0.8)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}

