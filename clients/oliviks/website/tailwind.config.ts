import type { Config } from 'tailwindcss';

// Oliviks brand system — Pomelli brandbook.
// Barn Red #761212 · Papaya Orange #FAB73A · Chalk White #F7F9F4 · Jet Black.
const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        palm: {
          DEFAULT: '#761212',
          50: '#faecec',
          100: '#f3dcdc',
          300: '#d99090',
          500: '#a83030',
          600: '#8f1c1c',
          700: '#761212',
          800: '#5a0e0e',
          900: '#3d0808',
        },
        gold: {
          DEFAULT: '#FAB73A',
          50: '#fff9ec',
          100: '#fef2d8',
          200: '#fde3ad',
          400: '#fcc865',
          500: '#fab73a',
          600: '#e6a328',
          700: '#c98a16',
        },
        leaf: '#761212',
        cream: '#F7F9F4',
        cocoa: '#111111',
        ink: '#121210',
        stone: {
          100: '#eef0ea',
          200: '#e1e3db',
          300: '#cdcfc7',
          400: '#a3a59d',
          500: '#74766e',
        },
      },
      fontFamily: {
        display: ['var(--font-rubik)', 'system-ui', 'sans-serif'],
        sans: ['var(--font-manrope)', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'pop-gold': '10px 10px 0 0 #FAB73A',
        'pop-palm': '10px 10px 0 0 #761212',
        'pop-sm': '6px 6px 0 0 #FAB73A',
      },
    },
  },
  plugins: [],
};

export default config;
