# Oliviks Evidence Index

Date created: 2026-07-14
Purpose: preserve proof while finishing delivery, so the case study is factual instead of reconstructed from memory.

## Folder map

| Folder | Use |
|---|---|
| `before/` | Original site screenshots, old ordering flow, old messaging, old speed/SEO scans. |
| `after/` | New site screenshots, live domain proof, mobile/desktop views, admin/client-editing proof. |
| `metrics/` | Baseline and final metrics, Lighthouse/PageSpeed, Search Console, analytics, schema validation. |
| `decisions/` | Decision log, scope exclusions, client comments, approval notes, retrospective material. |

## Capture queue

| Status | Evidence | Format | Notes |
|---|---|---|---|
| [x] | Original homepage desktop screenshot | PNG/JPG | `before/legacy-home-desktop-2026-07-14.png`. |
| [x] | Original homepage mobile screenshot | PNG/JPG | `before/legacy-home-mobile-2026-07-14.png`. |
| [x] | Original ordering journey | PNG/JPG + note | Legacy storefront captured and compared in `decisions/OLIVIKS-ORDERING-JOURNEY-COMPARISON-2026-07-14.md`; production repeat remains a launch task. |
| [~] | Original messaging excerpts | Markdown note | Key legacy claims recorded in the verification report; dedicated copy comparison remains. |
| [x] | New homepage desktop screenshot | PNG/JPG | Preview evidence captured; production recapture still required. |
| [x] | New homepage mobile screenshot | PNG/JPG | Preview at 390x844 with no horizontal overflow. |
| [x] | New menu and ordering route | PNG/JPG + note | Desktop/mobile menu captured; 37 shop and 4 WhatsApp links observed in preview HTML. |
| [x] | Contact/conversion route | PNG/JPG + note | Desktop/mobile contact route captured. |
| [x] | Admin/menu editing flow | PNG/JPG + note | Safe desktop capture shows 33 Supabase-backed items and no secret values. |
| [x] | Extended mobile route evidence | PNG/JPG + note | About, catering, privacy, and admin mobile captures added after scroll-aware verification. |
| [~] | Schema validation | Markdown/PDF/PNG | Local JSON-LD parses as Restaurant with core fields. Approximate coordinates, review count, and public post-launch validation remain open. |
| [~] | Sitemap and robots checks | Markdown/PNG | Local routes pass build; current preview returns 404 until deployment. |
| [x] | AI-crawler or llms.txt check | Markdown/PNG | Preview `llms.txt` returns 200. |
| [x] | Page speed baseline | Metric row + report | Controlled public legacy mobile/desktop Chrome trace captured. |
| [~] | Page speed final | Metric row + report | Preview trace captured and materially improved; repeat on production root after cutover. |
| [ ] | GBP baseline and final state | PNG + Markdown | Use already captured baseline plus final screenshots. |
| [~] | Email signup test | PNG + note | Provider state documented; controlled live signup requires approval. |
| [ ] | WhatsApp QR/opt-in proof | PNG + note | Counter card, QR target, client-owned list status. |
| [~] | Client approval comments | Markdown | 2026-07-13 approval request recorded; no reply found. |
| [ ] | Testimonial request | Markdown | Include copy and sent date. |
| [x] | Delivery timeline | Markdown | `decisions/OLIVIKS-DELIVERY-TIMELINE-2026-07-14.md`. |
| [x] | Scope exclusions | Markdown | `decisions/OLIVIKS-SCOPE-AND-DECISIONS-2026-07-14.md`. |
| [~] | Final retrospective | Markdown | Pre-close retrospective written; append launch, acceptance, payment, feedback, and first operating result. |

## Case-study angle hypotheses

1. A small restaurant website should not just look better. It should make the order loop clearer.
2. The valuable work was infrastructure: menu data, shop path, GBP, email/WhatsApp, schema, and handover.
3. BridgeWorks turned scattered food-business assets into a maintainable system the owners can keep using.
