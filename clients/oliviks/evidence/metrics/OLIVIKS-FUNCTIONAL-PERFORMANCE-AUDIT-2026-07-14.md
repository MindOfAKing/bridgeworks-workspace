# Oliviks Functional and Performance Audit

Date: 2026-07-14
Scope: Read-only public comparison plus local production-build runtime verification
Decision: Local application QA is complete. Production launch, live form submissions, and final factual approval remain open.

## Build Result

- `npm run lint`: passed with 0 errors and the known anonymous default-export warning in `postcss.config.mjs`.
- `npm run build`: passed on Next.js 15.5.19.
- The build generated 15 routes, including `/robots.txt` and `/sitemap.xml`.

## Runtime Coverage

The optimized production build was served locally and audited in installed Chrome at:

- Desktop: 1440 x 1200.
- Mobile: 390 x 844.

Routes checked in both profiles:

1. `/`
2. `/menu`
3. `/about`
4. `/contact`
5. `/catering`
6. `/privacy`
7. `/admin`

Result across 14 route/profile combinations:

| Check | Result |
|---|---:|
| Non-200 route responses | 0 |
| Horizontal-overflow failures | 0 |
| Broken images | 0 |
| Browser console errors | 0 |
| Page errors | 0 |
| Internal-link failures | 0 |

The browser scrolled through every page before final evaluation. Initial full-page captures of animated sections contained blank areas because the test had not triggered the in-view animations. After the scroll-aware rerun, all About and Catering sections rendered normally. This was a capture artifact, not missing content.

## Functional Checks

| Surface | Observed result |
|---|---|
| Homepage retention form | Email, optional WhatsApp, and consent fields present. No submission was made. |
| Homepage order routes | 4 shop links and 3 WhatsApp links present. |
| Menu order routes | 37 shop links, including 33 product routes, plus 4 WhatsApp links. |
| Contact route | Name, email, and message fields; one submit button; 4 WhatsApp, 4 phone, and 2 email links. No form submission was made. |
| Admin route | Supabase-backed 33-item state visible; secret input and save control present. No write was attempted. |
| `robots.txt` | 200 locally, references the production domain, and disallows `/admin`. |
| `sitemap.xml` | 200 locally with 6 production URLs. |
| `llms.txt` | 200 locally and references the production domain. |

## Structured Data

One JSON-LD block parsed successfully as `Restaurant` and contained:

- Oliviks Kitchen name and production URL.
- Public telephone and Budapest postal address.
- `GeoCoordinates`.
- Menu URL.
- Opening hours.
- Aggregate rating.
- Two corroborating `sameAs` URLs.

This proves syntax and local rendering, not final factual approval. The coordinates are marked approximate in source, and the 493 review count must be rechecked before production launch. Public schema validation remains a post-deployment gate.

## Before-and-After Performance

Method: one cold synthetic Chrome run per public URL and profile. Mobile used 150 ms latency, 1.6 Mbps download, 750 Kbps upload, and 4x CPU slowdown. Desktop used 40 ms latency, 10 Mbps download, 2 Mbps upload, and no CPU slowdown. Both URLs returned 200.

This is a controlled comparative trace, not a Google PageSpeed score. The official PageSpeed endpoint returned HTTP 429 for both strategies during this audit.

### Mobile

| Metric | Legacy `oliviks.com` | New Vercel preview | Reduction |
|---|---:|---:|---:|
| First Contentful Paint | 8,840 ms | 2,608 ms | 70.5% |
| Largest Contentful Paint | 23,280 ms | 2,840 ms | 87.8% |
| Load event | 35,834 ms | 6,867 ms | 80.8% |
| Transfer | 5,556 KB | 390 KB | 93.0% |
| Resources | 102 | 21 | 79.4% |
| Cumulative Layout Shift | 0.0011 | 0 | Stable in both; lower on preview |

### Desktop

| Metric | Legacy `oliviks.com` | New Vercel preview | Reduction |
|---|---:|---:|---:|
| First Contentful Paint | 3,228 ms | 1,500 ms | 53.5% |
| Largest Contentful Paint | 4,952 ms | 2,804 ms | 43.4% |
| Load event | 6,475 ms | 3,258 ms | 49.7% |
| Transfer | 3,698 KB | 672 KB | 81.8% |
| Resources | 108 | 31 | 71.3% |
| Cumulative Layout Shift | 0.0017 | 0 | Stable in both; lower on preview |

The comparison supports a material performance improvement. It does not replace a production-domain PageSpeed run after cutover, and single-run values should not be presented as guarantees.

## New Visual Evidence

- `../after/preview-about-mobile-2026-07-14.png`
- `../after/preview-catering-mobile-2026-07-14.png`
- `../after/preview-privacy-mobile-2026-07-14.png`
- `../after/preview-admin-mobile-2026-07-14.png`

Machine-readable audit result:

- `../../website/test-results/completion-audit-2026-07-14/completion-audit.json`

## Remaining Production Gates

- Deploy the current local build only after approval.
- Repeat the route, schema, robots, sitemap, and performance checks on `oliviks.com` after cutover.
- Confirm final coordinates, review count, menu, photos, address, and ordering wording.
- Run the contact and retention submissions only with an approved test identity.
- Test the live checkout handoff and WhatsApp route without placing an order or creating client data unless explicitly approved.

No deployment, DNS change, form submission, database write, email action, order, or client contact occurred in this audit.
