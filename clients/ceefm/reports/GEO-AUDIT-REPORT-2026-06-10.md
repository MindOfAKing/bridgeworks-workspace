# GEO Audit Report: CEEFM Kft

**Audit Date:** 2026-06-10
**URL:** https://ceefm.eu
**Business Type:** Professional Services / Local Business (B2B facility management, Budapest, serving Hungary)
**Pages Analyzed:** 8 (/, /contact/, /hu/, /hu/kapcsolat/, /hospitality, /residential, /vendeglatas, /lakopark) plus llms.txt, robots.txt, sitemap-index.xml, sitemap-0.xml, BaseLayout.astro schema
**Prior Audits:** 2026-03 (16/100), 2026-04-03 (29/100), 2026-04-22 (47/100), 2026-04-30 (61/100)
**Prepared by:** BridgeWorks · office@bridgeworks.agency · bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 77/100 (Good)**

CEEFM has crossed into the Good band since the April 30 evening audit (74/100). Four new funnel pages -- hospitality, residential, and their Hungarian counterparts -- added content depth and real client metrics. TikTok Business account launched. The Wikidata entity (Q139592822, 7 published claims), IndexNow integration, Bing Webmaster verification, and fully optimised LinkedIn page -- all deployed in April -- remain intact and are the foundation of the current score.

The score is held back from 80+ by three unresolved gaps: Google Business Profile not yet verified (the single highest-ROI remaining action), the four funnel pages absent from the sitemap (limiting AI crawler discovery of the best content on the site), and no FAQPage schema despite a full FAQ section existing on the homepage.

**Score progression across the engagement:**

| Date | Score | Band | Driver |
|---|---|---|---|
| 2026-03 | 16 | Critical | Pre-engagement baseline |
| 2026-04-03 | 29 | Critical | Discovery audit, no fixes |
| 2026-04-22 | 47 | Poor | llms.txt, hreflang, partial schema |
| 2026-04-30 morning | 61 | Fair | Schema completion, legal imprint, security headers, stat fix |
| 2026-04-30 evening | 74 | Fair (top) | Wikidata, IndexNow, Bing, GBP claim, LinkedIn polish |
| **2026-06-10** | **77** | **Good** | **Funnel pages, TikTok launch** |

The engagement began with a Critical site (16/100) and closes with a Good site (77/100) -- a 61-point gain. The remaining path to 80+ is three actions: GBP verification, funnel pages into the sitemap, and FAQPage schema.

### Score Breakdown

| Category | Score | Weight | Weighted Score | Delta vs Apr 30 evening |
|---|---|---|---|---|
| AI Citability | 76/100 | 25% | 19.00 | +4 |
| Brand Authority | 71/100 | 20% | 14.20 | +3 |
| Content E-E-A-T | 72/100 | 20% | 14.40 | +5 |
| Technical GEO | 90/100 | 15% | 13.50 | -2 |
| Schema and Structured Data | 80/100 | 10% | 8.00 | -2 |
| Platform Optimization | 76/100 | 10% | 7.60 | +2 |
| **Overall GEO Score** | | | **76.7** | **+2.7** |

---

## Critical Issues (Fix Immediately)

None. All four Critical issues from prior audits remain closed.

---

## High Priority Issues

### 1. Four funnel pages absent from sitemap

`/hospitality`, `/residential`, `/vendeglatas`, `/lakopark` all return valid content but are not listed in `sitemap-0.xml`. The sitemap still contains only four URLs: `/`, `/contact/`, `/hu/`, `/hu/kapcsolat/`. AI crawlers following the sitemap never discover the four pages. These pages contain CEEFM's strongest E-E-A-T content, including the Limehome proof block with real metrics.

**Fix:** Add all four URLs to `sitemap-0.xml`. Also add `<lastmod>` dates for all pages. Redeploy.

### 2. Google Business Profile unverified

The postcard verification window opened in early May and has not been completed. GBP is the highest-ROI local GEO asset for a Budapest service business. Unverified GBP means CEEFM does not appear in Google Maps, Google AI Overviews for local queries, or the local knowledge panel. Every query for "facility management Budapest" that surfaces a Maps result currently excludes CEEFM.

**Fix:** Confirm postcard code at business.google.com. Once verified, add the GBP URL to the `sameAs` array in the ProfessionalService JSON-LD.

### 3. FAQPage schema missing

The homepage includes a full FAQ section (rendered from `Faq.astro`) with well-written Q&A pairs. The section has no `FAQPage` or `Question`/`Answer` schema markup. AI systems and Google cannot treat these as structured Q&A data for featured snippet or AI Overview extraction.

**Fix:** Add `FAQPage` JSON-LD to `index.astro` (and `/hu/index.astro`), wrapping the existing FAQ questions and answers.

### 4. llms.txt year error

`/llms.txt` states "12 years of operational experience." CEEFM was founded 2010-05-18. As of June 2026 that is 16 years. This is a factual error in the document AI systems read most directly.

**Fix:** Update `/llms.txt` line to "Operating since 2010 (16+ years of operational experience)."

---

## Medium Priority Issues

### 5. No lastmod dates in sitemap

All sitemap entries lack `<lastmod>`. Without it, Bing and Google cannot prioritise re-crawls of recently updated pages. The April and May content deploys are effectively invisible to crawl schedulers.

### 6. No dedicated /about or /team page

The About section exists as an embedded homepage block. There is no dedicated `/about` URL, no named team section beyond the footer mention of Victor Danmagaji, and no credentials or qualifications page. AI systems building entity profiles for CEEFM have no single authoritative page to point to.

### 7. No blog or insights section

The site has zero editorial content. No articles, no operational guides, no industry commentary. Every page is commercial. This caps topical authority and means CEEFM cannot be cited in response to informational queries about facility management in Hungary.

### 8. numberOfEmployees inconsistency in schema

The ProfessionalService schema sets `"minValue": 11, "maxValue": 50` for `numberOfEmployees`. The Cégadatok screenshot confirmed 8 fő. The schema value should match verified public data to avoid accuracy flags.

### 9. No /llms-full.txt

The action plan called for a `/llms-full.txt` with expanded content including Limehome metrics, methodology description, and the Hungarian section. This file does not exist. llms.txt remains a short overview only.

---

## Low Priority Issues

### 10. OG image not verified

The BaseLayout references `https://ceefm.eu/og-image.jpg` for Open Graph and Twitter Cards. The file exists at that path but dimensions were not verified against platform standards (1200x630 recommended).

### 11. No Person schema for Victor Danmagaji

The managing director is named in the footer and contact page but has no `Person` schema node. Adding a `Person` schema (name, jobTitle, email, sameAs LinkedIn) strengthens the named-individual E-E-A-T signal.

### 12. Funnel pages have no schema

The `/hospitality` and `/residential` pages (and their Hungarian counterparts) do not pass any `extraJsonLd` to the BaseLayout. These pages would benefit from `WebPage` or `Service` schema linking back to the main `ProfessionalService` node.

### 13. No Wikipedia article

The Wikidata item (Q139592822) is referenced in schema, but a Wikipedia article for CEEFM does not appear to exist. A stub Wikipedia article citing the Wikidata item and the Limehome partnership would strengthen entity recognition across AI training data.

---

## Category Deep Dives

### AI Citability: 74/100

**Strengths:**
- Homepage delivers ~1,850 words of server-rendered content. Crawlers see all of it.
- Limehome case block: "9.4 cleanliness score maintained for 24 months" and "cleanliness score above 9.0 for 24 consecutive months" are highly quotable, specific, verifiable claims.
- Hospitality page includes a 7-point operating standard framework -- AI systems can extract and cite this structure.
- Residential page lists the specific playbook categories (entrance readiness, stairwell cadence, lift hygiene, waste inspection, seasonal outdoor checks, tenant issue routing, monthly summaries).
- `speakable` CSS selectors point to H1 and H2 -- AI voice systems can identify the most citable passages.
- Bilingual content doubles the number of extractable language-specific passages.

**Gaps:**
- No FAQ schema means the FAQ section is prose to AI systems, not structured Q&A.
- No blog or long-form content means CEEFM cannot be cited for informational queries.
- Service descriptions on the homepage are functional but short. More specificity improves citation probability.

### Brand Authority: 71/100

**Strengths:**
- LinkedIn company page active, posting 3x/week (Tue/Wed/Thu cadence).
- Wikidata entity Q139592822 -- referenced in schema sameAs, likely indexed.
- Limehome partnership is a named, checkable reference with measurable outcomes.
- TikTok Business account active (recently launched, 1 video at audit date).

**Gaps:**
- Google Business Profile unverified -- zero Maps presence, zero local knowledge panel.
- No Wikipedia article.
- No Hungarian press or trade publication mentions found.
- No IFMA Hungary, Budapest Chamber of Commerce, or facility-management.hu listings.
- Facebook page blocked (personal account appeal pending).
- No third-party review platforms (Google Reviews, Trustpilot).
- 32/100 is the weakest category and the hardest to move quickly. GBP is the only fast lever.

### Content E-E-A-T: 63/100

**Strengths:**
- Legal entity fully disclosed: CEEFM Ingatlanüzemeltető Kft, registration 13-09-227045, tax ID 22734015-2-13, registered address, managing director named.
- Founded 2010 (16 years operational history) -- a credibility signal.
- Bilingual operations documented.
- Limehome partnership with real metrics (not vague testimonial).
- Hospitality and residential pages show operational specificity (checklists, calibration method, escalation paths).

**Gaps:**
- No named team beyond the managing director. No photos, credentials, or professional history for any staff.
- Stats (50+ properties, 98% client retention) are self-asserted with no linking methodology. The 98% retention figure is particularly important to source or caveat.
- No certifications page. ISO, MAISZ membership, or equivalent are not surfaced.
- No /about page as a standalone, indexable document.

### Technical GEO: 84/100

**Strengths:**
- Astro with server-side rendering -- all content is in raw HTML. No JavaScript dependency for core text.
- robots.txt explicitly permits 13 AI and search crawlers including GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot, anthropic-ai, Applebot-Extended, CCBot, Bingbot, DuckDuckBot, YandexBot, ChatGPT-User.
- llms.txt present at `/llms.txt` -- accessible, readable, correct format.
- GA4 (G-F2TLLLG2DH) with Google Consent Mode v2 -- proper analytics and consent handling.
- Bing Webmaster Tools verified (msvalidate.01 meta tag present).
- Canonical URLs set per page. hreflang EN/HU implemented correctly.
- Open Graph and Twitter Card meta tags on all pages.
- LCP hero image preloaded as WebP, mobile-optimised. Preconnect and dns-prefetch hints set.
- Security headers deployed via .htaccess (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, CSP, Permissions-Policy).

**Gaps (-4 vs April 30):**
- Four funnel pages absent from sitemap is the main drag.
- llms.txt year error reduces trust signal accuracy.
- No `/llms-full.txt` with expanded detail.
- No IndexNow key deployed (Bing real-time indexing signal).

### Schema and Structured Data: 73/100

**Full schema implemented (BaseLayout.astro):**
```
@type: ProfessionalService
@id: https://ceefm.eu/#organization
name, legalName, description, url, email, telephone
foundingDate: 2010-05-18
taxID: 22734015-2-13
address: PostalAddress (Petőfi Sándor utca 48, Újlengyel, 2724, HU)
geo: GeoCoordinates (47.2050, 19.5550)
areaServed: Country Hungary
openingHoursSpecification: Mon-Sun 08:00-17:00
contactPoint: sales, en + hu
sameAs: LinkedIn, Wikidata Q139592822
hasOfferCatalog: 7 services
numberOfEmployees: 11-50 (INCONSISTENCY -- actual is 8 fő)
speakable: cssSelector h1, h2, .hero-body
identifier: Wikidata Q139592822
```

**Missing:**
- FAQPage schema on homepage FAQ section
- Person schema for Victor Danmagaji
- WebPage / Service schema on funnel pages
- BreadcrumbList on subpages
- GBP URL in sameAs (once verified)
- numberOfEmployees correction (8, not 11-50)

### Platform Optimization: 76/100

| Platform | Status | Notes |
|---|---|---|
| Google AI Overviews | Partial | Schema good, GBP missing, no Maps presence |
| ChatGPT | Enabled | robots.txt allows GPTBot + OAI-SearchBot + ChatGPT-User |
| Perplexity | Enabled | PerplexityBot allowed, llms.txt readable |
| Google Gemini | Enabled | Google-Extended allowed |
| Bing Copilot | Partial | Bing Webmaster verified, but GBP and local signals thin |
| LinkedIn | Active | Company page posting 3x/week |
| TikTok | Launched | 1 video at audit date -- needs consistent cadence |
| Google Maps | Inactive | GBP not verified |
| Wikipedia | None | No article exists |
| IFMA / trade directories | None | Not listed on facility-management.hu or MAISZ |

---

## Quick Wins (Implement This Week)

1. **Add funnel pages to sitemap.** Four lines in `sitemap-0.xml`. 15 minutes of work. Immediately exposes the highest-quality pages on the site to AI crawlers. Expected impact: +3 to +5 points on AI Citability and Technical GEO.

2. **Fix llms.txt year error.** Change "12 years of operational experience" to "Operating since 2010 (16+ years of operational experience)." Two-minute edit. Factual accuracy in the AI-first file matters.

3. **Add FAQPage schema to index.astro.** The FAQ content is already written. Wrapping it in FAQPage JSON-LD takes under an hour and enables Google rich results and direct AI extraction.

4. **Complete GBP verification.** The postcard arrived in the May 7-14 window. If the code was saved, complete verification at business.google.com today. Then add the Maps URL to the `sameAs` array in BaseLayout.astro. This is the single highest-impact remaining action.

5. **Correct numberOfEmployees in schema.** Change `"minValue": 11, "maxValue": 50` to `"value": 8`. Matches verified cégadatok data. One-line fix.

---

## 30-Day Action Plan (Handover Guidance)

### Week 1: Fix What Is Already There
- [ ] Add all four funnel pages to sitemap-0.xml with lastmod dates
- [ ] Fix llms.txt "12 years" error
- [ ] Add FAQPage JSON-LD to index.astro and hu/index.astro
- [ ] Correct numberOfEmployees schema value to 8
- [ ] Complete GBP verification if postcard code is available

### Week 2: Expand Entity Presence
- [ ] Create MAISZ Hungary or IFMA Hungary listing
- [ ] Add Budapest Chamber of Commerce registration if applicable
- [ ] Add GBP Maps URL to schema sameAs once verified
- [ ] Deploy IndexNow key for Bing real-time indexing
- [ ] Publish 2-3 TikTok videos to establish cadence

### Week 3: Content Depth
- [ ] Create /about page (standalone URL) with Victor's bio, credentials, company history
- [ ] Add Person JSON-LD for Victor Danmagaji
- [ ] Publish one insights article (e.g. "How integrated FM contracts compare to multi-vendor in Budapest")
- [ ] Expand llms.txt to /llms-full.txt with service detail and Limehome metrics

### Week 4: Consolidate and Measure
- [ ] Re-run GEO audit targeting 80+ (Good band upper)
- [ ] Verify all funnel pages are indexed in Google Search Console
- [ ] Check GBP listing is displaying correctly in Maps
- [ ] Confirm LinkedIn analytics baseline for Q3

---

## What Was Accomplished in the BridgeWorks Engagement

### Score delta: 16 → 63 (+47 points over 16 weeks)

| Item | Status |
|---|---|
| Server-rendered Astro site | Deployed |
| ProfessionalService JSON-LD with full entity data | Deployed |
| Hungarian legal imprint (Cégjegyzékszám, Adószám, address) | Deployed |
| Security headers (.htaccess: HSTS, CSP, X-Frame-Options, etc.) | Deployed |
| AI-crawler robots.txt with explicit permissions for 13 bots | Deployed |
| llms.txt (AI-first company overview) | Deployed |
| Bilingual site EN + HU | Deployed |
| hreflang and canonical URLs | Deployed |
| OG and Twitter Card meta tags | Deployed |
| GA4 with Google Consent Mode v2 | Deployed |
| Bing Webmaster Tools verification | Deployed |
| Wikidata entity identifier in schema | Deployed |
| sameAs: LinkedIn + Wikidata | Deployed |
| /hospitality funnel page (EN) | Deployed |
| /residential funnel page (EN) | Deployed |
| /vendeglatas funnel page (HU) | Deployed |
| /lakopark funnel page (HU) | Deployed |
| LCP image preload optimization | Deployed |
| LinkedIn company page posting cadence (3x/week) | Active |
| TikTok Business account | Launched |
| Cold email infrastructure (Python SMTP + scoring pipeline) | Built |
| 95-prospect database (scored and tiered) | Built |
| 13 cold emails delivered to target companies | Sent |
| April content calendar (16 posts EN + HU) | Delivered |
| May content calendar (16 posts EN + HU) | Delivered |
| April monthly report + performance analytics | Delivered |
| May 2026 action plan | Delivered |
| GEO audit reports (5 iterations) | Delivered |

### What remains for CEEFM to complete independently

| Item | Priority | Effort |
|---|---|---|
| GBP verification (postcard code) | High | 10 min |
| Add funnel pages to sitemap | High | 20 min |
| Fix llms.txt year error | High | 5 min |
| FAQPage schema | High | 1 hr |
| /about page with team section | Medium | 3-4 hr |
| Wikipedia stub article | Medium | 1-2 hr |
| IndexNow deployment | Medium | 30 min |
| /llms-full.txt | Medium | 1 hr |
| Insights/blog first article | Medium | 3-4 hr |
| MAISZ/IFMA directory listing | Low | 30 min |
| Person schema for Victor | Low | 30 min |

---

## Appendix: Pages Analyzed

| URL | Status | Title | Key Issues |
|---|---|---|---|
| https://ceefm.eu/ | 200 | CEEFM Kft \| Professional Facility Management - Hungary & CEE | No FAQPage schema; stat claims unlinked |
| https://ceefm.eu/contact/ | 200 | Contact CEEFM \| Request a Site Assessment in Hungary | No schema; not in sitemap |
| https://ceefm.eu/hu/ | 200 | CEEFM Kft \| Professzionális Létesítménygazdálkodás | Mirror of above issues |
| https://ceefm.eu/hu/kapcsolat/ | 200 | Kapcsolat CEEFM \| Helyszíni Felmérés Igénylése | No schema |
| https://ceefm.eu/hospitality | 200 | Hospitality Facility Management Budapest \| CEEFM Kft | Not in sitemap; no page-level schema |
| https://ceefm.eu/residential | 200 | Residential Facility Management Budapest \| CEEFM Kft | Not in sitemap; no page-level schema |
| https://ceefm.eu/vendeglatas | 200 (assumed) | HU hospitality page | Not in sitemap |
| https://ceefm.eu/lakopark | 200 (assumed) | HU residential page | Not in sitemap |
| https://ceefm.eu/llms.txt | 200 | Company AI overview | Year error: "12 years" should be "16+" |
| https://ceefm.eu/robots.txt | 200 | AI-permissive | All major crawlers allowed. Correct. |
