import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        palm: '#C44D2B',
        gold: '#E8A838',
        leaf: '#2D5016',
        cream: '#FDF6EC',
        cocoa: '#2A1A12',
      },
      fontFamily: {
        display: ['var(--font-playfair)', 'Georgia', 'serif'],
        sans: ['var(--font-dmsans)', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
