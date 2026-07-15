# Oliviks Delivery Verification

Date: 2026-07-14
Run type: read-only external audit plus local build verification
Status labels: observed / inferred / drafted / executed

## Decision

Oliviks is preview-ready, but the Foundation engagement is not yet production-complete.

The new site is healthy at `https://oliviks-kitchen.vercel.app`, connected to its current menu data, and visually verified on desktop and mobile. The approved root domain still serves the legacy WordPress site. Client cutover approval, public technical checks, end-to-end retention testing, final GBP evidence, and handover acceptance remain open.

## Observed External State

### Client and commercial correspondence

- Gmail message `19f5cb7a0b6b35ac`, thread `19f5cb446db99b5c`, was sent on 2026-07-13 with subject `Oliviks Foundation - complete, and your next steps`.
- The message gave the client the Vercel preview, asked for approval before pointing `oliviks.com` to it, attached invoice EO-2026-13, and identified WhatsApp printing/list work and the handover walkthrough as next steps.
- No reply to that exact thread was found on 2026-07-14. Production approval is therefore not evidenced.
- Invoice EO-2026-13 is for 136,305 HUF and is due 2026-07-19. Payment was not verified. Do not issue a duplicate invoice.
- Gmail warning message `19f42551b9d5163b` reported that `oliviks.com` and `www.oliviks.com` were misconfigured for the `oliviks-kitchen` Vercel project on 2026-07-08.

### Public web surface

| Surface | Result | Meaning |
|---|---|---|
| `https://oliviks.com/` | 200, legacy WordPress/WooCommerce site | Root cutover is not complete. |
| `https://oliviks-kitchen.vercel.app/` | 200, new Next.js site | Preview is available for review. |
| `https://oliviks-kitchen.vercel.app/menu` | 200 | Current public preview menu is available. |
| `https://oliviks-kitchen.vercel.app/admin` | 200, Supabase reported as menu source | CMS foundation is connected; owner login/authentication is not implemented. |
| `https://oliviks-kitchen.vercel.app/llms.txt` | 200 | AI-readable business file is present on the current deployment. |
| Preview `/robots.txt` | 404 | New local file is not deployed yet. |
| Preview `/sitemap.xml` | 404 | New local file is not deployed yet. |
| `https://shop.oliviks.com/` | 200, title `Oliviks` | Ordering subdomain is reachable in the latest check. |

The connected Google Search Console account contains only `https://bridgeworks.agency/`. No Oliviks property was present, so Oliviks indexing and search performance are not yet observable there.

### Supabase

Project `toltnysainnkpxfxibff` (`oliviks-kitchen`) was `ACTIVE_HEALTHY` on Postgres 17.6.

| Table | Rows | RLS |
|---|---:|---|
| `menu_categories` | 5 | enabled |
| `menu_items` | 33 | enabled |
| `menu_option_groups` | 0 | enabled |
| `menu_options` | 0 | enabled |
| `site_settings` | 2 | enabled |
| `subscribers` | 0 | enabled |

Public-read policies exist for menu data and an insert policy exists for subscribers. `site_settings` has RLS with no policy, which keeps it private. The performance advisor reported informational unindexed foreign keys on three menu relationships; no blocking security finding was observed.

### MailerLite

- Group `Oliviks subscribers`: 0 active, 1 unconfirmed, 0 unsubscribed.
- Automation `Oliviks welcome sequence`: enabled, valid, 5 steps, 0 qualified subscribers.
- Backup `500 HUF` automation: inactive, valid, 5 steps.
- Supabase has 0 subscriber rows, so the website form to Supabase to MailerLite to double opt-in to welcome-sequence path is not proven end to end.

No test subscriber was submitted because that would mutate live client data and requires Emmanuel approval.

## Local Technical Verification

Executed in `clients/oliviks/website` on 2026-07-14:

- `npm run lint`: passed with 0 errors and one pre-existing anonymous default-export warning in `postcss.config.mjs`.
- `npm run build`: passed on Next.js 15.5.19 and generated 15 static routes.
- Generated routes include `/robots.txt` and `/sitemap.xml`.
- Generated robots rules allow public pages, disallow `/admin` and `/api/`, and reference `https://oliviks.com/sitemap.xml`.
- Generated sitemap contains the production URLs for home, menu, about, contact, catering, and privacy.

Local fixes in this run:

- Centralized review rating/count metadata through `site.ts` to remove copy drift.
- Added Next.js metadata routes for robots and sitemap.
- Corrected Supabase documentation to reflect the connected project and current 33-item seed.
- Deprecated the stale combined `activate.sql` snapshot.
- Corrected retention and handover wording so configured systems are not described as end-to-end proven.

These local changes were not deployed.

## Visual Evidence

Exact viewports were 1440x1200 for desktop and 390x844 for mobile. Home, menu, and contact measured `innerWidth: 390` and `scrollWidth: 390` on mobile, so no horizontal overflow was detected.

| Evidence | File |
|---|---|
| Legacy desktop home | `../before/legacy-home-desktop-2026-07-14.png` |
| Legacy mobile home | `../before/legacy-home-mobile-2026-07-14.png` |
| Preview desktop home | `../after/preview-home-desktop-2026-07-14.png` |
| Preview mobile home | `../after/preview-home-mobile-2026-07-14.png` |
| Preview desktop menu | `../after/preview-menu-desktop-2026-07-14.png` |
| Preview mobile menu | `../after/preview-menu-mobile-2026-07-14.png` |
| Preview desktop contact | `../after/preview-contact-desktop-2026-07-14.png` |
| Preview mobile contact | `../after/preview-contact-mobile-2026-07-14.png` |
| Preview desktop admin | `../after/preview-admin-desktop-2026-07-14.png` |
| Preview mobile about | `../after/preview-about-mobile-2026-07-14.png` |
| Preview mobile catering | `../after/preview-catering-mobile-2026-07-14.png` |
| Preview mobile privacy | `../after/preview-privacy-mobile-2026-07-14.png` |
| Preview mobile admin | `../after/preview-admin-mobile-2026-07-14.png` |

The admin screenshot contains no credentials or secret values.

## Extended Functional and Performance Evidence

`OLIVIKS-FUNCTIONAL-PERFORMANCE-AUDIT-2026-07-14.md` records a scroll-aware production-build audit across seven routes in desktop and mobile profiles. All 14 route/profile combinations returned 200 with zero horizontal-overflow failures, broken images, console errors, page errors, or internal-link failures.

The same audit captured a controlled public legacy-versus-preview performance comparison. The preview reduced mobile LCP from 23,280 ms to 2,840 ms and desktop LCP from 4,952 ms to 2,804 ms in the single-run synthetic trace. Treat these as comparative evidence, not PageSpeed scores or production guarantees. The official PageSpeed endpoint returned 429 during the run.

The local JSON-LD parsed as Restaurant with the expected core fields. Approximate coordinates and the current review count still need factual confirmation, and public validation remains a post-launch gate.

## Exceptions

- The connected Vercel app returned 403 for project, deployment, fetch, and runtime-error reads because it is authenticated against the wrong account scope. Public HTTP checks were used instead.
- No deployment, DNS change, Google Business Profile mutation, MailerLite mutation, Gmail send, CRM write, invoice action, or client contact was performed.

## Closure Gates

### Done

- Preview build, current menu data, responsive evidence, safe admin evidence, and local build verification.
- Invoice state and client correspondence reconciled.
- Supabase and MailerLite configuration state documented.

### Needs Emmanuel approval

- Deploy the local metadata-route fixes.
- Run one controlled signup/double-opt-in/welcome-email test.
- Make any domain or DNS cutover after written client approval.
- Correct or reconnect the Vercel integration scope if connector-level evidence is required.

### Blocked

- Root-domain launch is blocked by client approval and domain configuration.
- Final Search Console evidence is blocked until an Oliviks property is connected.
- Final GBP completion evidence, WhatsApp list/QR proof, owner walkthrough, acceptance, testimonial request, and payment confirmation remain open.
