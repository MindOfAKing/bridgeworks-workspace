# Oliviks Kitchen Supabase activation

Current status: connected and serving the public preview from the active `oliviks-kitchen` project (`toltnysainnkpxfxibff`). Verified read-only on 2026-07-14.

Verified state:

- 5 active menu categories.
- 33 available menu items.
- 0 option groups and 0 menu options. Current menu uses item-level prices.
- 0 subscriber rows. The website signup path has not been proven end to end against Supabase.
- RLS is enabled on every public table.
- Supabase security advisor returned no warning or error findings. It returned one informational notice because `site_settings` has RLS with no public policy, which is the intended private posture.

## Files

- `schema.sql` creates the CMS tables, RLS, and public read policies.
- `seed-menu.sql` seeds the current approved menu from `src/data/menu.ts`.
- `scripts/generate-menu-seed.cjs` regenerates `seed-menu.sql` after the static menu changes.
- `activate.sql` is a historical combined snapshot and is not canonical. Do not run it. Its embedded 30-item seed is older than `seed-menu.sql` and the live 33-item menu.

## Current verification and future activation steps

For a fresh replacement project only:

1. Create the client-owned Supabase project.
2. Open the Supabase SQL editor and run `supabase/schema.sql`.
3. Run the current `supabase/seed-menu.sql`.
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

## Current open verification

- `/admin` reports Supabase connected and loads the current menu.
- Admin writes still use the temporary server secret. Owner login through Supabase Auth is not implemented.
- A real signup test would create client data in Supabase and MailerLite. It requires Emmanuel's explicit approval before execution.
