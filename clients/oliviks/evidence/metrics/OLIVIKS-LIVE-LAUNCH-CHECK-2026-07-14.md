# Oliviks Live Launch Check

Date: 2026-07-14
Method: Read-only public URL check plus local Vercel project inspection
Result: Root-domain launch gate failed; preview and shop are reachable

## Public Root Domain

Checked: https://oliviks.com/

The public root domain is still serving the legacy WordPress/WooCommerce storefront.

Observed legacy signals:

- The site identity is `Organic Store`.
- The navigation contains Home, Menu, Contact, and My account.
- The page contains a cart total and WooCommerce product-grid language.
- The footer says `Powered by Kreativewin`.
- The page contains old claims including `Available all EUROPE`, `24/7 Support Team`, and `Online Payment`.

This is not the new Next.js Oliviks site in `clients/oliviks/website`.

## Shop Subdomain

Checked: https://shop.oliviks.com/

The latest direct check returned 200 with page title `Oliviks`. The ordering subdomain is reachable. A complete cart/checkout transaction was not performed.

## New Site Preview

Checked: https://oliviks-kitchen.vercel.app/

The new Next.js preview returned 200 and passed focused desktop/mobile visual checks. Its menu and admin routes also returned 200, and the admin route reported Supabase as the menu source.

The preview's `llms.txt` returned 200. Its public `robots.txt` and `sitemap.xml` returned 404. Local metadata routes were added and pass the build, but they have not been deployed.

## Local Vercel Link

The local website directory is linked to:

- Project name: `oliviks-kitchen`
- Project ID: `prj_wzv73j6L2TgkMfM30x7tRttKUsQq`
- Framework: Next.js

The local project link proves the build is associated with Vercel. It does not prove that `oliviks.com` points to that project.

## Gate Decision

- New site live on approved public domain: not achieved.
- Public ordering subdomain reachable: achieved.
- End-to-end ordering transaction: not tested.
- Final after screenshots: blocked until cutover.
- Final PageSpeed, schema, sitemap, robots, and llms checks: partial; local/preview evidence exists, but production checks remain blocked until cutover.
- Website completion, final handover, commercial close, and case-study drafting: blocked by launch evidence.

## Required Next Check

1. Confirm the production deployment for `oliviks-kitchen` is healthy.
2. Point `oliviks.com` and the required `www` route to the approved Vercel project.
3. Re-run the complete shop checkout-path QA after root cutover.
4. Re-run desktop and mobile checks on the root site and ordering route.
5. Capture screenshots and final technical metrics.

No deployment, domain, DNS, WordPress, Vercel, or client-facing change was made in this check.
