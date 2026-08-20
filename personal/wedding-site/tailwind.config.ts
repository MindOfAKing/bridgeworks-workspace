import type { Config } from 'tailwindcss';

// Wedding palette. These are the couple's colours, not BridgeWorks tokens.
// Off-white ground, burgundy for emphasis, green for accents.
// Provisional shades: change them here and the whole site follows.
const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: '#F7F4EF',
          deep: '#EFE9E0',
          card: '#FDFBF8',
        },
        burgundy: {
          DEFAULT: '#6B1F32',
          dark: '#4E1524',
          light: '#8C3049',
        },
        sage: {
          DEFAULT: '#3F5B45',
          dark: '#2E4433',
          light: '#5C7B62',
        },
        ink: '#2A2422',
        muted: '#6E635C',
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        body: ['var(--font-body)', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        prose: '68ch',
      },
    },
  },
  plugins: [],
};

export default config;
