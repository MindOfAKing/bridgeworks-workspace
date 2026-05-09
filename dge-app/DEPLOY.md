# BridgeWorks Digital Growth Engine — Deployment Guide

## What this is
Full-stack Next.js app — BridgeWorks Digital Growth Engine.
Frontend + Anthropic API proxy. Deploys to Vercel in under 2 minutes.

---

## Claude Code — paste this prompt exactly

```
Deploy this Next.js app to Vercel as a new project.

1. Run: npm install
2. Run: vercel --yes
   When prompted:
   - Scope: Emmanuel Ehigbai
   - Link to existing project: No
   - Project name: bridgeworks-dge
   - Directory: ./
   - Override settings: No
3. After deployment, get the live URL
4. Add ANTHROPIC_API_KEY to Vercel — read the value from my .env file.
   Add it to Production, Preview, and Development environments using:
   vercel env add ANTHROPIC_API_KEY production
   vercel env add ANTHROPIC_API_KEY preview
   vercel env add ANTHROPIC_API_KEY development
5. Redeploy to production so the env variable is live: vercel --prod
6. Give me the final live URL

If Vercel CLI is not installed: npm install -g vercel
If not logged in: vercel login
```

---

## Environment variable required
`ANTHROPIC_API_KEY` — already in your .env file. Claude Code reads it from there.

## After deployment
- Live URL: https://bridgeworks-dge.vercel.app (or similar)
- Custom domain later: Vercel → Project → Settings → Domains → dge.bridgeworks.agency

## App structure
```
pages/index.jsx      Full Digital Growth Engine (6 stages)
pages/api/claude.js  Anthropic proxy — key stays server-side
styles/globals.css   Base styles
```

## Troubleshooting
- Yellow banner in app = API key not set. Run steps 4-5 above.
- Vercel login errors = run vercel login first
- Build errors = run npm install before vercel
