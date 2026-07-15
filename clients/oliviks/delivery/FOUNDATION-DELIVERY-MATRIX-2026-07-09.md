# Oliviks Foundation Delivery Matrix

Date: 2026-07-09
Owner: BridgeWorks
Client: Oliviks Nigerian Kitchen / Oliviks KFT
Source proposal: `PROPOSAL-OLIVIKS-2026-04-28.md`
Source contract: `CONTRACT-OLIVIKS-2026-04-29.md`
Scope selected in contract: Foundation only, 272,611 HUF fixed one-time fee
Foundation Total: 272,611 HUF

## Status legend

| Status | Meaning |
|---|---|
| Done local | Built or drafted locally with file evidence. Still may need live/client proof. |
| Partial | Some work exists, but at least one proposal requirement is missing. |
| Draft ready | Copy, checklist, or content pack exists, but it is not confirmed as published or operational. |
| Blocked | Requires client access, approval, account ownership, or external platform action. |
| Unknown | No reliable local evidence found yet. |
| Not started | No local evidence found and no safe assumption should be made. |

## Hard gates before final handover

Final handover under contract section 4 requires all four conditions below.

| Gate | Contract source | Current status | Evidence | Blocker / next action |
|---|---|---|---|---|
| Website live on `oliviks.com` | Contract section 4 | Blocked | Local/live preview evidence exists for `https://oliviks-kitchen.vercel.app`; no evidence found that `oliviks.com` points to the new Vercel site. | Needs explicit production/domain approval and domain cutover evidence. |
| GBP changes published | Contract section 4, section 2.2 | Partial | `reports/gbp-evidence/GBP-BASELINE-2026-06-26.md` says description submitted and pending Google review. Action checkboxes remain unchecked. | Needs GBP access/evidence screenshots for categories, attributes, Q&A, posts, photos, menu, NAP cleanup. |
| Email and WhatsApp systems operational | Contract section 4, section 2.3 | Partial / blocked | MailerLite group and enabled valid 5-step automation verified; 0 active, 1 unconfirmed, 0 qualified. Supabase has 0 subscribers. | Needs approved end-to-end subscriber test, client WhatsApp list/QR action, and handoff proof. |
| One-page handover document for each workstream | Contract sections 2.2, 2.3, 4 | Partial | `OLIVIKS-HANDOVER-2026-07-14.md` and workstream handover material exist. | Deliver owner walkthrough and capture client acceptance after live systems are verified. |

## Kickoff and client responsibility gates

| Gate | Contract source | Current status | Evidence | Next action |
|---|---|---|---|---|
| First payment received, 136,306 HUF | Contract sections 4 and 5 | Recorded paid / not independently verified | `FOUNDATION-HANDOVER-INVOICE-NOTE-2026-07-12.md` records EO-2026-11 as paid in June. | Emmanuel retains bank/payment evidence if needed. |
| WordPress admin access | Contract section 6 | Unknown / possibly obsolete | Contract required WP access. Current path appears to be Next.js/Vercel replacement. | Decide whether WP access is still needed for redirects, backup, order receipt, old-site cleanup, or domain migration. |
| GBP manager access | Contract section 6 | Done | Gmail correspondence shows Emmanuel received manager access on 2026-06-11. | Use access only for approved publication and capture final evidence. |
| 30 to 50 photos or written permission to source existing assets | Contract section 6 | Partial | Design system assets and legacy media are present. QA says legacy WordPress photos improved credibility. | Confirm client-approved final photo set and rights. |
| Business WhatsApp number | Contract section 6 | Unknown | Retention pack has copy, but no operational proof. | Client confirms WhatsApp Business number and opt-in method. |
| First-subscriber incentive | Contract section 6 | Draft ready | Retention pack recommends free puff puff or 500 HUF off. | Client chooses final incentive. |
| Single authorized approver | Contract section 6 | Unknown | No approval record found. | Emmanuel confirms named approver. |
| Address confirmation: Rákóczi tér 9, 1084 Budapest | Proposal acceptance, contract section 6 | Partial | Site data and baseline files use Rákóczi tér 9. | Confirm client explicitly approved as public-facing address and use for NAP cleanup. |

## A1. Website Upgrade, 163,566 HUF

| # | Proposal deliverable | Current status | Local evidence | Missing / next action |
|---|---|---|---|---|
| A1.1 | Homepage rewritten and rebuilt with clear hero, 4.8 stars, platform badges, press bar | Done local / needs final review | `website/src/app/page.tsx`; `website/src/data/site.ts`; `website/.hermes/qa/report.md`; `website/.hermes/qa/live-visual-review/report.md` | Confirm final proof language. Note memory preference: mention Wolt/foodora neutrally, not anti-platform. |
| A1.2 | About page rebuilt around Cynthia and Aese's story, with founder photos | Done local / partial | `website/src/app/about/page.tsx`; `.hermes/qa/report.md` says approved copy applied, founder story included. | Confirm founder details and final photos are approved by client. |
| A1.3 | Fake testimonials removed and real Google reviews embedded/carousel added | Partial | Site data includes rating/proof markers. QA report references proof. | Need explicit review carousel or embedded real Google review evidence. Verify live page and screenshots. |
| A1.4 | Dish descriptions for all 23 menu products | Done local / needs approval | `website/src/data/menu.ts`; `.hermes/qa/report.md` says approved menu copy applied; script count found 33 dish names/priced entries. | Confirm exact dish list against owner-approved menu. Proposal says 23, current local menu has 33 name entries, likely options/categories included. |
| A1.5 | Cleanup: `/sample-page/`, `/cart-2`, `/checkout-2`, `/my-account-2` deleted or redirected | Blocked / unknown | No WordPress access or redirect evidence found. | Need old-site backup and redirect checks against production domain. If new Vercel site replaces WP, add Vercel redirects or domain-level 301 plan. |
| A1.6 | Contact page rebuilt, chef hotline renamed, Google Map embedded, address structured data | Done local / partial | `website/src/app/contact/page.tsx`; `website/src/lib/schema.ts`; `website/src/data/site.ts` contains Rákóczi tér 9. | Verify Google Map embed and schema on live URL. |
| A1.7 | Empty Shop page resolved, either populated or removed from navigation | Partial / needs live check | Next.js routes include `/menu`, no `/shop` route found. | Need verify old production `/shop` does not remain in nav or resolves appropriately after domain cutover. |
| A1.8 | Pricing visible on every menu item | Done preview / needs approval | Supabase read verified 33 current menu items with price labels; preview menu no longer shows the stale Banga, Abacha, or `Price TBC` entries. | Capture final owner approval and repeat on production domain. |
| A1.9 | SEO basics: meta descriptions, Open Graph tags, alt text, focus keyword per page | Partial | `website/src/lib/schema.ts`; app pages exist; README says meta/OG built. | Need focused SEO verification: metadata per page, OG image, alt text audit, focus keyword log. |
| A1.10 | Page speed pass, image compression, caching, Elementor bloat reduced where possible | Partial | Next.js build passes. Legacy photo QA exists. | Need live Lighthouse/PageSpeed or at least mobile performance pass. Elementor bloat reduction only applies if staying on WP; current path is Next.js replacement. |
| A1.11 | Mobile responsive QA across all pages on iOS and Android | Partial / strong local evidence | `.hermes/qa/live-visual-review/report.md` checked Home, Menu, About desktop/mobile. `.hermes/qa/report.md` mentions cart QA. | Need Contact, Catering, Admin if included, and live production domain/mobile screenshots. |
| A1.12 | Pre-handover backup of existing site | Unknown / blocked | No backup evidence found in inspected files. | If old WP is still live, create/record backup before domain cutover or live mutation. |
| A1.extra | Contact form via Resend | Partial / blocked | `website/src/app/api/contact/route.ts` includes Resend. README lists `RESEND_API_KEY`, `CONTACT_TO`, `CONTACT_FROM`. | Add Vercel env vars and run live form test after approval. |
| A1.extra | Supabase admin/CMS path for client-editable menu | Connected preview / handover partial | Project `toltnysainnkpxfxibff` is healthy; preview admin reports Supabase and shows 33 items. | Replace temporary shared-secret workflow with an approved owner-auth plan if ongoing editing is included, then complete walkthrough. |
| A1.extra | Local code health | Done local | Previous Projects sweep: `npx tsc --noEmit`, `npm run lint`, `npm run build`, `npm audit --audit-level=moderate` all green. | Keep as code evidence, not handover completion evidence. |

## A2. Google Business Profile Optimization, 65,427 HUF

| # | Proposal deliverable | Current status | Local evidence | Missing / next action |
|---|---|---|---|---|
| A2.1 | Secondary categories added: Nigerian Restaurant, Caterer, Takeaway, Delivery Restaurant | Draft ready / blocked | `execution/GBP-CONTENT-PACK-OLIVIKS-2026-06-05.md` lists suggested categories. Baseline file has unchecked action. | Needs GBP access and screenshot after category changes. |
| A2.2 | Full attributes audit and completion | Draft ready / blocked | GBP content pack lists attributes to audit. Baseline action unchecked. | Needs GBP UI audit and evidence screenshot. |
| A2.3 | Business description rewritten in 750 chars, EN and HU | Partial | GBP content pack has EN/HU drafts. Baseline says new description submitted and pending Google review on 2026-06-26. | Need verify final Google approval and exact live text. Hungarian draft needs native polish before publishing if not already polished. |
| A2.4 | Menu uploaded inside GBP: 23 dishes, photo, description, price | Not started / blocked | GBP content pack and website menu exist. No GBP menu upload evidence found. | Needs owner-approved final menu, photos, prices, GBP access, upload screenshots. |
| A2.5 | Photo audit and upload up to 50 photos | Partial / blocked | Baseline references photos uploaded checkbox but unchecked. Local assets and post images exist. | Need photo audit list, client photo approval, GBP upload screenshots. |
| A2.6 | Q&A pre-populated with 8 to 10 owner-answered questions | Draft ready / blocked | GBP content pack includes 8 Q&A entries in EN/HU. Baseline action unchecked. | Needs approval and GBP publication evidence. |
| A2.7 | Four launch posts published | Draft ready / blocked | GBP content pack includes 4 launch posts; post images present in `reports/gbp-evidence/posts/`. Baseline action unchecked. | Needs approval and published post screenshots. |
| A2.8 | Review response templates and backfill unresponded reviews | Draft ready / blocked | GBP content pack includes review response templates. | Need owner approval, access, backfill log, screenshots or exported evidence. |
| A2.9 | NAP cleanup across Wolt, Foodora, Facebook, TripAdvisor, Wanderlog | Draft ready / blocked | GBP content pack includes NAP cleanup log template. Proposal notes Wolt address conflict. | Need platform screenshots, access/claim status, updates or handoff instructions where BridgeWorks cannot edit. |
| A2.10 | Website-side schema markup added | Done local / needs live check | `website/src/lib/schema.ts`; `website/src/data/site.ts`; site build passed. | Validate schema on live production URL after domain cutover. |
| A2.11 | Baseline GBP Insights screenshot before optimization and 4-week follow-up screenshot | Partial | `reports/gbp-evidence/GBP-BASELINE-2026-06-26.md` has metrics and follow-up target 2026-07-24. | Save actual screenshot files if available. Schedule or perform follow-up capture when due. |
| A2.12 | One-page GBP handover document | Not started / unknown | No final handover doc found. | Draft after GBP changes are live and verified. |

## A3. Email and WhatsApp Infrastructure, 79,966 HUF

| # | Proposal deliverable | Current status | Local evidence | Missing / next action |
|---|---|---|---|---|
| A3.1 | Email provider account set up, MailerLite or Beehiiv free tier, owned by client | Connected / ownership not reverified | MailerLite group `Oliviks subscribers` and automation were verified read-only. | Confirm client ownership/access in the walkthrough. |
| A3.2 | Email capture popup with first-order incentive | Draft ready / blocked | Retention pack contains popup copy and incentive options. | Need final incentive approval, provider form, site integration, mobile test. |
| A3.3 | 3-email welcome sequence | Configured / untested | MailerLite automation is enabled, valid, has 5 steps, and has 0 qualified subscribers. | Run one approved double-opt-in and welcome-delivery test. |
| A3.4 | Weekly specials email template EN/HU | Partial / draft ready | Retention pack has English weekly template. GBP pack includes some HU drafts, but retention pack is not fully HU. | Add Hungarian weekly template or native polish pass if EN/HU is required. |
| A3.5 | Branded WooCommerce order receipt email | Draft ready / blocked | Retention pack includes receipt rebrand notes. | Needs WordPress/WooCommerce access or alternative if Next.js path replaces WP ordering. |
| A3.6 | GDPR compliance: consent, double opt-in, unsubscribe, privacy policy update | Draft ready / blocked | Retention pack contains consent text and privacy notes. | Needs provider implementation and privacy policy page/update. Verify double opt-in and unsubscribe. |
| A3.7 | WhatsApp Business broadcast list with website and counter QR opt-in | Draft ready / blocked | Retention pack has WhatsApp opt-in copy, consent line, welcome message, broadcast template. | Needs client WhatsApp Business number, QR generation, counter placement, test scan. |
| A3.8 | WooCommerce integration: customers added to list with double opt-in | Not started / blocked | No integration evidence found. | Needs WooCommerce access, chosen email provider, GDPR setup. If current ordering is not WooCommerce, define replacement integration. |
| A3.9 | One-page Email and WhatsApp handover document | Drafted / acceptance pending | `execution/email-whatsapp/HANDOVER.md` records current provider state and owner actions. | Deliver walkthrough after retention and WhatsApp tests are evidenced. |

## Proposal optional items and scope control

| Item | Proposal status | Current matrix decision |
|---|---|---|
| Optional Growth Retainer, 218,088 HUF/month | Optional, not required for Foundation handover | Do not include as owed unless separately accepted. |
| Photo Shoot, 90,870 HUF | Optional add-on | Not owed unless accepted. But Foundation still requires client-supplied 30 to 50 photos or written permission to source existing assets. |
| Catering Page, 79,966 HUF | Optional add-on | Current website has `/catering`, but the proposal treats dedicated catering page as optional. Do not bill/claim as Foundation unless Emmanuel decides it was included as goodwill or later approved. |
| Full Hungarian translation of every website page | Explicitly not included | Do not treat as Foundation owed. A2 description and A3 weekly template have specific EN/HU requirements. |
| Full e-commerce restructure / direct delivery checkout | Explicitly not included | Do not promise direct checkout as Foundation. |
| Ongoing operations, review management, weekly posts | Retainer scope | Foundation includes setup, templates, launch posts, and handover only. |

## Immediate next actions

1. Confirm commercial gate: signed contract, first payment, and current client-approved scope.
2. Confirm whether the active website path is Next.js/Vercel replacement or WordPress improvement.
3. Obtain written client approval for the Next.js preview before domain or DNS changes.
4. Get final client approval for menu list, prices, `Price TBC` items, photos, address, order flow, and platform wording.
5. Prepare A2 GBP publication batch from existing drafts, then publish only after explicit approval and access.
6. Approve and run one controlled MailerLite double-opt-in/welcome test; complete the client-owned WhatsApp number, QR, and list flow.
7. Deliver the existing handover material in an owner walkthrough and capture acceptance.
8. Before claiming final completion, collect handover proof:
   - production URL/domain evidence
   - live GBP screenshots
   - test email subscriber evidence
   - WhatsApp QR/list evidence
   - client handover docs

## Bottom line

The website preview and its Supabase menu are healthy and materially advanced. The Foundation engagement is not complete until the root-domain launch, Google Business Profile evidence, retention/WhatsApp tests, and handover acceptance are complete. The biggest current risks are client approval, domain configuration, final GBP proof, controlled retention testing, and acceptance evidence.
