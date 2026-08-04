# BridgeWorks To-Do List

*Last updated: 2026-07-10*

## Priority closeout - Oliviks Foundation

Foundation delivery is complete, paid in full at 272,611 HUF, and live after the
verified 2026-07-24 cutover. Do not reopen delivery scope. Current closeout
source: `clients/oliviks/delivery/OLIVIKS-CLOSEOUT-PRIORITY-2026-08-01.md`.

- [x] Shop catalog: 33/33 dishes deep-linked, WooCommerce API cleanup done — shipped 2026-07-09
- [x] Supabase CMS wired end-to-end, admin PATCH verified — 2026-07-09
- [x] GBP manual pass: award post, Foodora-vs-Wolt correction, Lili review reply — done 2026-07-10
- [x] Shop SSL fix - verified externally 2026-07-14
- [x] Confirm `oliviks.com` points at the new Vercel site - cutover executed and verified 2026-07-24
- [ ] P1: Unpause Supabase and verify the live menu API returns `source: supabase` - exact approval required
- [ ] P2: Send Gmail draft `r-7795127371496586913` and hold the owner walkthrough - exact recipient approval required
- [ ] P3: Record the client-owned WhatsApp broadcast list and QR placement
- [ ] Capture written acceptance and structured feedback, then archive
- [x] Full payment received: 272,611 HUF

## Active — BridgeWorks backend (systems, still open)

- [ ] Invoicing template via szamlazz.hu (NAV-compliant, EN+HU)
- [ ] VAT handling for EU clients (HU + reverse charge logic)
- [ ] Payment flow for NGN clients (avoid 4% card fee)
- [x] Contract template EN/HU + signing flow — shipped 2026-05-05
- [x] Onboarding doc / week-1 client handbook (EN) — shipped 2026-05-05, HU translation still pending

## Active — Content

- [ ] Content gap: no posts drafted or queued for the week of Jul 7-13, 2026
- [x] Content-week-bot pre-drafted Jul 14-20 (9 posts, calendar events, Gmail draft) — 2026-07-09
- [ ] Set up The Bridge Issue 002 in Beehiiv (overdue since launch week, April)
- [ ] Add client logo bar to BridgeWorks homepage (Limehome anchor + anonymized references)

## Archive — CEEFM (closed 2026-06-19, no active work unless reactivated)

CEEFM Kft engagement ended 2026-06-19. Do not schedule content, outreach, or reports against this client without Emmanuel explicitly reactivating it. Full context: `clients/ceefm/CLAUDE.md`.

**Outcome on record:** GEO score 16 (Mar baseline) → 77/100 at the 2026-06-10 final audit, verified (per `clients/ceefm/VERIFIED-FACTS.md`; an interim 82 reading on 2026-04-25 was never reproduced and is superseded). Payment collected in full per the same source.

**Delivered during engagement (kept for case-study reference only):**

- Hungarian legal imprint, ProfessionalService JSON-LD, security headers, SolaCare service tile, server-rendered stat counters — all deployed
- April content calendar: 12/12 posts published
- Brand visual design package — cancelled by client 2026-04-12 (declined, EUR 625)
- Solar add-on pitch — declined by Victor 2026-04-16 (EUR 550, do not re-pitch)
- Case study documented for BridgeWorks portfolio: named use approved 2026-07-14; client-sensitive internals stay private

**Left unresolved at close (historical, not owed):** May/June content calendars, GBP claim + Wikidata + directory listings, case-study pages, paid acquisition phase, cold outreach expansion. None of this converts to open work — engagement ended before these phases started.

## Backlog / parked

- [ ] Set up pipeline cron schedules (daily/weekly/monthly)
- [ ] Fix youtube-analytics script for v1.2.4 API compatibility
- [ ] Scope command center (Notion vs dashboard vs Sheets expansion)
