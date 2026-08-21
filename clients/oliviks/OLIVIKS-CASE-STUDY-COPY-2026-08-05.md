# Oliviks Case Study — Deployable Copy

**Date:** 2026-08-05
**For:** bridgeworks.agency `/work`, second case study slot
**Structure:** mirrors the existing `work.ceefm` object in `src/messages/en.json`
**Status:** copy is final. **Publication is approval-gated.** See blockers at the end.

Every number below is traceable to a dated evidence file in `clients/oliviks/evidence/`. Nothing is estimated. Nothing is rounded up.

---

## Headline numbers

Captured 2026-07-14 with the same controlled Chrome trace method against the legacy production site and the new build, same day, same conditions.

| Metric | Legacy site | New site | Evidence |
|---|---:|---:|---|
| Mobile LCP | 23,280 ms | 2,840 ms | `metrics/oliviks-metric-sheet-2026-07-14.csv` |
| Mobile page weight | 5,556 KB | 390 KB | same |
| Mobile requests | 102 | 21 | same |
| Desktop LCP | 4,952 ms | 2,804 ms | same |
| Desktop page weight | 3,698 KB | 672 KB | same |

The strongest single line: **a customer on a phone waited 23 seconds to see the page. Now they wait under 3.**

Verified live on production 2026-08-05: `oliviks.com`, `/menu`, `/admin`, `/robots.txt`, `/sitemap.xml`, `/llms.txt`, and `shop.oliviks.com` all return 200.

---

## Proposed `work.oliviks` content

**Tag:** Order-Loop Build
**Badge:** Delivered and live
**Client:** Oliviks Kitchen
**Anchor:** How Oliviks cut its mobile load from 23 seconds to under 3

### Card proof tiles

| Value | Label |
|---|---|
| 23s -> 2.8s | Mobile load |
| 5,556 -> 390 KB | Page weight |
| 33 | Menu items live |
| 4 | Systems connected |

### Meta

| Field | Value |
|---|---|
| Industry | Restaurant and food service |
| Region | Budapest, Hungary. Nigerian-owned |
| Stage | Trading business, digital presence owned by a previous agency |
| Engagement | Foundation package, April to July 2026 |

### Context

Oliviks Kitchen serves Nigerian food from Rákóczi tér in Budapest. The food was working. The digital side was not.

The website was a generic WooCommerce theme. It still identified itself as "Organic Store" in the browser tab and carried another agency's credit in the footer. It made claims the business could not keep, including "Available all EUROPE" and "24/7 Support Team." On a phone it took over 23 seconds to render.

The people most likely to order were Nigerians in Budapest looking for food from home, and Hungarians curious enough to try it. Both were meeting a page that loaded slowly and did not say who the business was.

### The bottleneck

**A site that did not identify the business.** The browser tab said "Organic Store." The footer credited a different agency. Nothing on the page said Nigerian, Budapest, or Oliviks in a way a search engine or an AI assistant could read and repeat.

**23 seconds on mobile.** 5,556 KB and 102 requests to load a homepage. Most food ordering happens on a phone. Most people do not wait.

**A scattered order path.** The legacy homepage carried 86 links and 11 inline add-to-cart actions spread across separate shop, cart, account, and product routes. There was no single obvious way to order.

**No customer list.** Every order was a one-off. The business had no way to reach a customer who had already bought once, which is the cheapest sale in food service.

### Systems built

**1. A website that says what the business is**

A new site on Next.js, replacing the theme. Mobile load went from 23,280 ms to 2,840 ms and page weight from 5,556 KB to 390 KB. The menu runs on a database with 5 categories and 33 dishes, editable by the owners without touching code.

*Why:* A restaurant site has one job on a phone. Show the food, then take the order. Everything that did not serve that was removed.

**2. The shop, restyled and completed**

The existing WooCommerce shop was kept, restyled to match the new brand, secured, and extended to carry every dish on the menu rather than a partial list. Keeping it meant the owners did not lose their order history or have to learn a new system.

*Why:* Replacing a working payment path is a risk with no upside. The shop worked. It just did not look like the same business.

**3. A customer list the business owns**

Email capture into MailerLite with double opt-in and a five-step welcome automation, backed up to the business's own Supabase project. A WhatsApp broadcast route and a printable counter QR card for in-store signups.

*Why:* A restaurant that can message its regulars on Thursday about the weekend special does not depend on the algorithm. This is the loop the whole build points at.

**4. Findable, by people and by AI**

Restaurant schema with name, address, hours, phone, and menu. Working `robots.txt`, `sitemap.xml`, and `llms.txt`, all verified live. Google Business Profile optimised, review handling set up, and the Restaurant Guru 2026 award surfaced on the site.

*Why:* When someone asks an assistant where to eat Nigerian food in Budapest, the answer is assembled from structured, readable sources. The legacy site gave those systems nothing to work with.

### Outcome

The Foundation was delivered, paid in full at 272,611 HUF, and the domain cutover to `oliviks.com` was executed and verified on 2026-07-24.

Every account is in the owners' names: domain, hosting, shop, email tool, database, Google profile. BridgeWorks holds working access to support, nothing more. The handover document lists every system and how to run it, written for people with no technical background.

Everything runs on free tiers. The business pays nothing to keep it online.

---

## Blockers before this can be published

These are real. The copy is ready. Publishing is not.

**1. Client permission is not on file.**
`delivery/OLIVIKS-CLOSEOUT-PRIORITY-2026-08-01.md` states plainly: "Approval required: GBP replies, testimonial use, **or any public case study**." No written acceptance and no testimonial permission is recorded. CEEFM named use was approved on 2026-07-14. Oliviks has no equivalent.

**2. The owner-editing path is down in production.**
Checked live 2026-08-05: `oliviks.com/api/admin/menu` returns `source: static-fallback` with `fallback: "Supabase menu load failed."` The Supabase project `toltnysainnkpxfxibff` was paused after inactivity on 2026-07-31.

The site is serving its menu correctly from a static fallback, so customers see nothing wrong. But the case study above claims the owners can edit their own menu, and right now they cannot. Publish that claim while it is false and it is the one detail a prospect could check.

**3. The shop still carries the previous agency's branding.**
Checked live 2026-08-05: `shop.oliviks.com` still contains "Organic Store" twice and "Kreativewin" once. The case study opens by describing exactly those two things as the problem that was fixed. A prospect who clicks through to the shop sees them still there.

**4. The walkthrough email is drafted and unsent.**
Gmail draft `r-7795127371496586913`, in the existing Oliviks thread, prepared 2026-08-01. It is the email that would produce the acceptance, the feedback, and the permission. It has not been sent.

### The unblocking sequence

Every one of the four blockers resolves through the same short chain:

1. Unpause the Supabase project. Verify `/api/admin/menu` returns `source: supabase`.
2. Apply the shop CSS/title patch. The fix is already written in `delivery/SHOP-CSS-PATCH-2026-08-01.md`.
3. Send Gmail draft `r-7795127371496586913` to `olivikskitchen@gmail.com`, CC `agaigbeaese@gmail.com`.
4. On the walkthrough call, ask for three things: written acceptance, permission to publish this case study by name, and a Clutch reference.
5. Publish.

Steps 1, 2, and 3 all touch the client and all need your approval before I run them.

Step 3 is the one that matters. That draft has been sitting for four days, and it is the single dependency for the case study, the testimonial, and the Clutch review at the same time.
