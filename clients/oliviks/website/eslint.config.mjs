import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';

const eslintConfig = [
  {
    ignores: [
      '.next/**',
      '.vercel/**',
      '.hermes/**',
      'out/**',
      'build/**',
      'next-env.d.ts',
    ],
  },
  ...nextVitals,
  ...nextTypescript,
  {
    files: ['**/*.cjs'],
    rules: {
      '@typescript-eslint/no-require-imports': 'off',
    },
  },
];

export default eslintConfig;
