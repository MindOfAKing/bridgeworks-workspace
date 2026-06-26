import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        palm: '#761212',
        gold: '#FAB73A',
        leaf: '#761212',
        cream: '#F7F9F4',
        cocoa: '#111111',
      },
      fontFamily: {
        display: ['var(--font-rubik)', 'system-ui', 'sans-serif'],
        sans: ['var(--font-manrope)', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
