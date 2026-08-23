/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.rs",
    "./index.html",
  ],
  theme: {
    extend: {
      colors: {
        'voltec-white': '#FFFFFF',
        'voltec-black': '#0A0A0A',
        'voltec-blue': '#00BFFF',
        'voltec-blue-dark': '#0099CC',
        'voltec-blue-light': '#66D9FF',
        'voltec-gray': '#1A1A1A',
        'voltec-gray-light': '#F5F5F5',
        /* Layered dark surfaces: depth instead of one flat black */
        'voltec-ink': '#06080C',
        'voltec-surface': '#0F141B',
        'voltec-elevated': '#161C25',
        'voltec-line': '#1F2733',
        /* Warm counterweight to the xenon blue, used sparingly */
        'voltec-amber': '#F2C14E',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
        brand: ['Orbitron', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      letterSpacing: {
        'tightest': '-0.045em',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'scan-line': 'scan-line 8s linear infinite',
        'particle-drift': 'particle-drift 20s linear infinite',
        'grow-bar': 'grow-bar 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 5px #00BFFF, 0 0 10px #00BFFF' },
          '50%': { boxShadow: '0 0 20px #00BFFF, 0 0 40px #00BFFF' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'scan-line': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        'particle-drift': {
          '0%': { transform: 'translateX(0) translateY(0)' },
          '100%': { transform: 'translateX(100px) translateY(-100px)' },
        },
        'grow-bar': {
          '0%': { transform: 'scaleX(0)' },
          '100%': { transform: 'scaleX(1)' },
        },
      },
      backgroundImage: {
        'grid-pattern': 'linear-gradient(to right, rgba(0, 191, 255, 0.1) 1px, transparent 1px), linear-gradient(to bottom, rgba(0, 191, 255, 0.1) 1px, transparent 1px)',
        'grid-fine': 'linear-gradient(to right, rgba(0, 191, 255, 0.055) 1px, transparent 1px), linear-gradient(to bottom, rgba(0, 191, 255, 0.055) 1px, transparent 1px)',
        'radial-glow': 'radial-gradient(ellipse at center, rgba(0, 191, 255, 0.15) 0%, transparent 70%)',
        'bar-blue': 'linear-gradient(90deg, #0099CC 0%, #00BFFF 55%, #66D9FF 100%)',
        'hairline': 'linear-gradient(90deg, transparent, rgba(0,191,255,0.35), transparent)',
      },
      backgroundSize: {
        'grid': '50px 50px',
        'grid-sm': '28px 28px',
      },
    },
  },
  plugins: [],
};
