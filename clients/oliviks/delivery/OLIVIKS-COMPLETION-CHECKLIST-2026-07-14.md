# Oliviks Completion Checklist

Date created: 2026-07-14
Client: Oliviks Kitchen
Purpose: define when Oliviks is commercially complete enough to hand over, invoice, and convert into a BridgeWorks proof package.

This checklist sits beside `FOUNDATION-DELIVERY-MATRIX-2026-07-09.md`. The matrix tracks contractual scope. This file tracks the final completion gate and evidence needed for future case-study use.

## Latest verification

On 2026-07-14, `https://oliviks.com/` still served the legacy WordPress/WooCommerce storefront. The new Next.js preview returned 200 and passed focused desktop/mobile review. `https://shop.oliviks.com/` returned 200 in the latest check.

Supabase is healthy with 5 menu categories and 33 menu items. MailerLite is configured, but has 0 active subscribers, 1 unconfirmed subscriber, and 0 subscribers qualified for the enabled welcome automation. The full retention path has not been proven. The connected Search Console account has no Oliviks property.

Client cutover approval was requested on 2026-07-13 and no reply was found. Invoice EO-2026-13 was already sent for 136,305 HUF and must not be duplicated. Local robots and sitemap routes now pass the build, but they have not been deployed and still return 404 on the current preview.

Evidence: `clients/oliviks/evidence/metrics/OLIVIKS-DELIVERY-VERIFICATION-2026-07-14.md`.

Status legend: `[x]` evidenced complete, `[~]` partial, `[!]` blocked or needs approval, `[ ]` not evidenced.

## Completion definition

Oliviks is done only when every required item below is checked or explicitly marked as out of scope with Emmanuel approval.

| Status | Area | Completion item | Evidence needed | Owner |
|---|---|---|---|---|
| [!] | Website | New site is live on the approved public domain. | Screenshot of `oliviks.com`, DNS/cutover note, final URL. | BridgeWorks |
| [~] | Website | Forms, menu links, WhatsApp links, ordering routes, and key CTAs work on live domain. | Full local runtime pass: 14 route/profile checks, 0 internal-link failures, 37 menu shop links, and 4 menu WhatsApp links. Production submissions and handoff still need testing. | BridgeWorks |
| [~] | Website | Mobile QA complete across home, menu, about, contact, catering if live, and admin if handed over. | All seven app routes passed at 390px with no overflow, broken images, console errors, or page errors. Production-domain repeat remains. | BridgeWorks |
| [!] | Website | Old site cleanup or redirect decision is documented. | Root still serves legacy site; cutover/redirect decision pending. | BridgeWorks |
| [~] | Website | Final client-approved menu, prices, photos, address, and platform wording captured. | Current 33-item menu verified; final written approval not found. | Client / BridgeWorks |
| [!] | Analytics | Analytics and search tools connected or deliberately deferred. | Connected Search Console account has no Oliviks property. | BridgeWorks |
| [~] | SEO/GEO | Technical SEO, schema, sitemap, robots, and AI-crawler checks complete. | `llms.txt` is public; robots/sitemap pass locally but are not deployed. | BridgeWorks |
| [~] | Performance | Before-and-after page speed or Lighthouse/PageSpeed pass captured. | Controlled public legacy-versus-preview Chrome trace captured for mobile and desktop. Official PageSpeed returned 429; production-domain repeat remains. | BridgeWorks |
| [~] | GBP | GBP changes are published or remaining access blockers are documented. | Access and partial description evidence exist; final publication pack is incomplete. | BridgeWorks / Client |
| [~] | Retention | Email provider, popup, double opt-in, welcome sequence, and test subscriber are live or clearly deferred. | MailerLite automation is enabled; end-to-end test is not proven. | BridgeWorks / Client |
| [!] | WhatsApp | WhatsApp opt-in route, QR card, and broadcast-list handoff are complete or client-owned blockers documented. | Owner printing/list action and scan proof remain open. | Client / BridgeWorks |
| [~] | Handover | Website handover is delivered. | Handover document exists; owner walkthrough/acceptance not evidenced. | BridgeWorks |
| [~] | Handover | GBP handover is delivered. | Handover content exists; final live evidence/acceptance not evidenced. | BridgeWorks |
| [~] | Handover | Email/WhatsApp handover is delivered. | Handover document exists; operational acceptance not evidenced. | BridgeWorks |
| [~] | Commercial | Final balance invoice/payment request sent after handover gates close. | EO-2026-13 sent before all closure gates; payment unverified. | Emmanuel |
| [!] | Feedback | Testimonial or structured feedback request sent. | No request evidence found. | Emmanuel |
| [~] | Evidence | Before-and-after evidence folder exists and contains the minimum case-study capture. | Thirteen screenshots plus functional, performance, ordering, technical, timeline, scope, and pre-close learning records exist. Final launch metrics remain open. | BridgeWorks |
| [~] | Retrospective | Final project retrospective written. | `../evidence/decisions/OLIVIKS-PRE-CLOSE-RETROSPECTIVE-2026-07-14.md` records delivery learning; launch and acceptance addendum remains. | Emmanuel / Agent |

## Minimum evidence before case-study drafting

- Original website screenshots.
- New website screenshots.
- Mobile and desktop views.
- Original versus revised messaging.
- Original versus revised ordering journey.
- Performance, SEO, and AI-visibility baselines.
- Search Console and analytics configuration status.
- Schema, sitemap, robots.txt, and structured-data notes.
- Before-and-after page speed results.
- Major business decisions and why they were made.
- Scope changes and deliberate exclusions.
- Delivery timeline.
- Client comments, approvals, and testimonial request.
- Final URLs and launch date.
- Lessons, mistakes, and unresolved limitations.
