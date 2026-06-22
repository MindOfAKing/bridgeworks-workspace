# Oliviks Kitchen Supabase activation

Current status: local app is Supabase-ready, but no Supabase cloud project is connected yet.

## Files

- `schema.sql` creates the CMS tables, RLS, and public read policies.
- `seed-menu.sql` seeds the current approved menu from `src/data/menu.ts`.
- `scripts/generate-menu-seed.cjs` regenerates `seed-menu.sql` after the static menu changes.

## Activation steps

1. Create a Supabase project on the free tier.
2. Open the Supabase SQL editor and run `supabase/schema.sql`.
3. Then run `supabase/seed-menu.sql`.
4. Add these Vercel environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `ADMIN_API_SECRET`
   - `ADMIN_ALLOWED_EMAILS=olivikskitchen@gmail.com`
5. Redeploy Vercel production.
6. Verify:
   - `/api/admin/menu` returns `source: "supabase"`
   - `/admin` shows database status connected
   - `/menu` still shows the approved menu

## Local checks

```bash
node scripts/generate-menu-seed.cjs
npm run build
```

## Current blocker

The Supabase CLI is installed via `npx`, but this machine is not authenticated with Supabase yet. Run:

```bash
npx supabase login
```

Then provide the access token from Supabase if you want the agent to create/link the project through CLI instead of you creating it manually in the dashboard.
