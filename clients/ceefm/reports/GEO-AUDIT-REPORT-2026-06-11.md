# GEO Audit Report: CEEFM Kft

**Audit Date:** 2026-06-11
**URL:** https://ceefm.eu
**Business Type:** Professional Services / Local Business (B2B facility management, Budapest, Hungary)
**Pages Analyzed:** 8 (/, /contact/, /hu/, /hu/kapcsolat/, /hospitality/, /residential/, /vendeglatas/, /lakopark/)
**Prior Audit:** 2026-06-10 (77/100)
**Prepared by:** BridgeWorks · office@bridgeworks.agency · bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 78/100 (Good)**

Three of the four High-priority issues from the June 10 audit were resolved before this audit: FAQPage schema is now live on the homepage, all eight pages are in the sitemap including the four funnel pages, and the llms.txt year error ("12 years") has been corrected to "16 years." These changes push the score from 77 to 78.

The site remains in the Good band. The one High-priority item that did not change is the Google Business Profile — not yet verified. That remains the highest single-action gain available. Once verified and linked in the schema, the score is expected to reach 81-82.

**Score progression across the engagement:**

| Date | Score | Band | Driver |
|---|---|---|---|
| 2026-03 | 16 | Critical | Pre-engagement baseline |
| 2026-04-03 | 29 | Critical | Discovery audit, no fixes yet |
| 2026-04-22 | 47 | Poor | llms.txt, hreflang, partial schema |
| 2026-04-30 morning | 61 | Fair | Schema completion, legal imprint, security headers |
| 2026-04-30 evening | 74 | Fair (top) | Wikidata, IndexNow, Bing, GBP claim, LinkedIn polish |
| 2026-06-10 | 77 | Good | Funnel pages launched, TikTok |
| **2026-06-11** | **78** | **Good** | **FAQPage schema, sitemap complete, llms.txt corrected** |

The engagement closes with a 62-point gain from baseline.

### Score Breakdown

| Category | Score | Weight | Weighted Score | Delta vs Jun 10 |
|---|---|---|---|---|
| AI Citability | 78/100 | 25% | 19.50 | +2 |
| Brand Authority | 71/100 | 20% | 14.20 | 0 |
| Content E-E-A-T | 72/100 | 20% | 14.40 | 0 |
| Technical GEO | 92/100 | 15% | 13.80 | +2 |
| Schema and Structured Data | 83/100 | 10% | 8.30 | +3 |
| Platform Optimization | 76/100 | 10% | 7.60 | 0 |
| **Overall GEO Score** | | | **77.8 → 78** | **+1** |

---

## Issues Resolved Since June 10

| Issue | Status |
|---|---|
| Funnel pages absent from sitemap | Fixed — all 8 URLs now in sitemap-0.xml |
| FAQPage schema missing on homepage | Fixed — FAQPage JSON-LD live in page source |
| llms.txt "12 years" error | Fixed — now reads "16 years of operational experience" |

---

## Remaining Issues for Victor to Action

### High Priority

**1. Google Business Profile — not yet verified**

The GBP was claimed but the postcard verification was not completed during the engagement. This is the highest single-action improvement available to the site. Every local "facility management Budapest" query that surfaces a Maps result currently excludes CEEFM. GBP verification also feeds the knowledge panel on Gemini, the Perplexity local results, and enables Google Reviews.

**Action:** Go to business.google.com, complete the postcard verification, then add the GBP URL to the `sameAs` array in BaseLayout.astro.

**Expected impact:** +3 to +4 points overall. Score would reach 81-82.

**2. Privacy policy page returns 404**

The contact form links to a privacy policy ("By submitting this form you agree to our Privacy Policy") but the page does not exist. This is a GDPR compliance issue for a Hungarian company collecting personal data via web form.

**Action:** Create `/privacy-policy/` (English) and `/adatvedelem/` (Hungarian) pages with the required GDPR privacy notice. A solicitor or GDPR template service can provide the text.

**3. Homepage reads "10+ Years Experience"**

The company was founded in 2010. As of 2026 that is 16 years. The llms.txt correctly says "16 years." The homepage hero stat still says "10+." AI crawlers quoting this stat will cite an inaccurate figure.

**Action:** Edit the hero component and change to "16 Years" or "Since 2010."

---

### Medium Priority

**4. Meta descriptions missing on four funnel pages**

`/hospitality/`, `/residential/`, `/lakopark/`, `/vendeglatas/` have no meta description. Search engines and AI crawlers generate their own snippet text for these pages.

**Action:** Add a `description` prop to each of the four page files in `src/pages/`. 130-155 characters each, with location and a specific service claim.

**5. Funnel pages are thin**

Hospitality page is approximately 370 words. Residential page is approximately 670 words. These are the primary service pages. For AI models to extract substantive answers from them, each page needs to be 800 words minimum with structured proof points.

**Action:** Expand both pages with process documentation, client outcome data, and a 3-5 question FAQ section per page with FAQPage schema.

**6. No About page**

`/about/` returns 404. A dedicated company history page with named leadership, founding date, client count, and service scope is a core E-E-A-T signal for both AI systems and human visitors.

**Action:** Create `/about/` with company history, Victor's bio and LinkedIn profile, and verifiable company facts.

**7. llms.txt missing Limehome case study and page links**

The strongest third-party proof point (Limehome Budapest, 9.4 cleanliness score, 24 months above 9.0) is not referenced in llms.txt. AI crawlers reading this file first cannot discover the funnel pages.

**Action:** Add a `## Case Study` section with the Limehome data. Add a `## Pages` section with absolute URLs for all service pages.

---

### Lower Priority

**8. Sitemap has no lastmod dates**

All 8 sitemap entries have no `<lastmod>` value. Crawlers cannot determine freshness.

**Action:** Add `lastmod: true` to `@astrojs/sitemap` in `astro.config.mjs` and redeploy.

**9. speakable property on wrong schema type**

`speakable` is attached to the ProfessionalService schema block. Schema.org only supports it on Article and WebPage types. It has no effect in its current placement — the validator flags it as a warning.

**Action:** Remove `speakable` from the ProfessionalService block. Add a separate WebPage schema block per page that includes `speakable` with the same CSS selectors.

**10. No blog or topical content**

The site has no blog, guides, or resource pages. For AI models to cite ceefm.eu as an authority on facility management topics, the site needs content beyond service descriptions and one case study.

**Recommended topics:** "Facility management for aparthotels in Budapest," "EU hygiene compliance for residential buildings," "How to evaluate a facility management contract in Hungary."

---

## What Was Built During the Engagement

For reference, this section records what GEO infrastructure was added during the 16-week engagement that is now live and operational on the site.

| Item | Status |
|---|---|
| ProfessionalService JSON-LD schema (comprehensive) | Live |
| FAQPage JSON-LD schema (homepage) | Live |
| robots.txt with explicit AI crawler permissions (13 crawlers) | Live |
| llms.txt (AI-first company summary) | Live |
| Bilingual hreflang tags (en/hu) | Live |
| Canonical URLs on all pages | Live |
| Security headers (HSTS, CSP, X-Frame-Options) | Live |
| Open Graph and Twitter Card meta tags | Live |
| Bing Webmaster verification | Live |
| GA4 analytics | Live |
| Google Consent Mode v2 | Live |
| Cookie consent banner | Live |
| Wikidata entity (Q139592822) | Live |
| IndexNow integration | Live |
| Sitemap including all 8 pages | Live |
| 4 service funnel pages (EN and HU) | Live |
| LinkedIn company page polished | Done |
| TikTok Business account created | Done |
| Cold email sequence (11 delivered, pipeline built) | Done |

---

## Appendix: Pages Analyzed

| URL | Language | Title | Status |
|---|---|---|---|
| https://ceefm.eu/ | EN | CEEFM Kft \| Professional Facility Management - Hungary & CEE | Live |
| https://ceefm.eu/contact/ | EN | Contact CEEFM \| Request a Site Assessment in Hungary | Live |
| https://ceefm.eu/hospitality/ | EN | Hospitality Facility Management Budapest \| CEEFM Kft | Live |
| https://ceefm.eu/residential/ | EN | Residential Facility Management Budapest \| CEEFM Kft | Live |
| https://ceefm.eu/hu/ | HU | Hungarian homepage | Live |
| https://ceefm.eu/hu/kapcsolat/ | HU | Hungarian contact | Live |
| https://ceefm.eu/lakopark/ | HU | Lakopark es tarsashaz takaritas Budapest | Live |
| https://ceefm.eu/vendeglatas/ | HU | Vendeglatas es apartmanhotel uzemeltetes Budapest | Live |

---

*BridgeWorks · office@bridgeworks.agency · bridgeworks.agency*
