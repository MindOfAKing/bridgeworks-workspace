# GEO Audit Report: CEEFM Kft

**Audit Date:** 2026-04-22
**URL:** https://ceefm.eu
**Business Type:** Professional Services / Local Business (B2B facility management, Budapest, serving Hungary and CEE)
**Pages Analyzed:** 2 (/, /hu/)
**Prepared by:** BridgeWorks · office@bridgeworks.agency · bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 47/100 (Poor)**

CEEFM has a strong technical foundation. Astro static rendering, open AI crawler policy, llms.txt, hreflang, and a present meta description put it ahead of most Hungarian SMEs for AI discoverability. But the site is invisible as an entity. Zero Wikipedia/Wikidata presence, minimal LinkedIn footprint, placeholder stat counters showing "0+ Properties / 0% Retention / 0+ Years" in the raw HTML, a single LocalBusiness schema block missing telephone, address, geo, and sameAs, and only one real case study (Limehome) means AI systems have almost nothing defensible to cite when asked about facility management in Budapest.

The fix is content breadth and entity building, not technical rework. Three weeks of focused work can move this from 47 to 70+.

**Progress since last audit (2026-04-03):** previous score 29/100. An 18-point lift in three weeks, driven by llms.txt, meta description, LocalBusiness schema, and hreflang additions. Remaining gains are content, entity, and schema completion.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 58/100 | 25% | 14.5 |
| Brand Authority | 18/100 | 20% | 3.6 |
| Content E-E-A-T | 34/100 | 20% | 6.8 |
| Technical GEO | 78/100 | 15% | 11.7 |
| Schema and Structured Data | 52/100 | 10% | 5.2 |
| Platform Optimization | 54/100 | 10% | 5.4 |
| **Overall GEO Score** | | | **47/100** |

### Score Interpretation

47 sits in the Poor band (40-59). AI systems can reach the site and parse some facts, but will not confidently recommend or cite CEEFM because entity signals and content depth are too thin.

---

## Critical Issues (Fix Immediately)

1. **Placeholder stat counters render as zeroes in raw HTML.** The homepage ships "0+ Properties Managed / 0% Client Retention / 0+ Years Experience" to every crawler because the real numbers are written by JavaScript after load. AI crawlers never see the actual figures (50+, 95%, 12+). Replace the JS counters with server-rendered text, then animate on top if the motion matters.

2. **Hungarian legal imprint is missing.** A Hungarian Kft is required by the Electronic Commerce Act (Ekertv.) to publish registered address, cégjegyzékszám (company registration number), and adószám (tax number) on its website. These are also primary trust signals for E-E-A-T. Without them, Google, Gemini, and Perplexity downgrade the authority of every claim on the page.

3. **LocalBusiness schema missing critical fields.** The single JSON-LD block has no `telephone`, no `address` as PostalAddress, no `geo`, no `openingHoursSpecification`, and no `sameAs`. Rich results will not trigger and entity linking across AI platforms has no anchor.

4. **No entity presence on Wikipedia, Wikidata, or major directories.** LLMs use these sources to confirm an organization exists and is real. A minimum viable entity scaffold (Wikidata item, LinkedIn company page completion, Budapest Chamber of Commerce listing) is mandatory before AI citation becomes realistic.

---

## High Priority Issues

5. **Only 2 URLs in the sitemap.** The entire site is one English and one Hungarian homepage. Every platform score is capped by this. Split into dedicated pages for the 6 services, 3 industries, an About/Leadership page, and a Case Studies index. Target 12-15 indexable URLs before the end of May.

6. **Only one case study on the site.** The Limehome partnership block is the single strongest proof asset (9.2 Booking, 9.4 Cleanliness, 24 months above 9.0) and it is buried mid-page. Turn it into a dedicated `/case-studies/limehome` page and add 3-4 more case studies from the 50+ projects.

7. **Self-declared aggregateRating without Review nodes.** The schema claims a 9.5/10 rating with no linked reviews. Google treats this as a manual action risk. Either add structured `Review` nodes tied to the rating or remove `aggregateRating`.

8. **EU Ecolabel certification not visible on-page.** It is mentioned in llms.txt but not shown prominently on the homepage with logo, certificate number, and scope. This is the single biggest expertise signal the business holds and it is hidden.

9. **No security headers (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy).** Not a direct GEO penalty, but Perplexity and Gemini use security posture as a trust proxy. Add via a `public/_headers` file in the Astro project.

10. **FAQ section exists on-page but no FAQPage schema wraps it.** Google has restricted FAQ rich results but AI systems still parse FAQPage JSON-LD as the cleanest question/answer signal.

---

## Medium Priority Issues

11. **Sitemap missing `<lastmod>` dates.** Crawl freshness is harder to signal. Configure `@astrojs/sitemap` with `lastmod: new Date()`.

12. **llms.txt lacks the Limehome metrics and a Hungarian section.** The single most citable proof point on the entire site is absent from the llms.txt. Also add a `## Optional` section with link references once case study pages exist, and publish a companion `/llms-full.txt` with the full homepage content as clean markdown.

13. **No Google Business Profile verified.** No address, geo, or hours data reaches Google's Knowledge Graph. Claim and complete the profile, then link its URL in the `sameAs` array.

14. **No Bing signals.** No `msvalidate.01` meta, no IndexNow key file, no sitemap submission to Bing Webmaster Tools. Bing Copilot has almost no signal to work with.

15. **No named leadership on the page.** Founder or managing director visibility is a primary E-E-A-T lever, especially for Hungarian B2B buyers. Add a short leadership section with photo, name, role, and credentials.

16. **Generic Unsplash stock images.** Undermines authenticity and makes the site look interchangeable with any competitor. Replace with photographs of CEEFM teams, equipment, and actual managed properties.

17. **No dated content, no blog, no news.** Every AI system reads "last updated" signals. Without any dated pages, freshness defaults to unknown.

---

## Low Priority Issues

18. **CSP header is minimal** (`upgrade-insecure-requests` only). Tighten once schema and headers are in place.
19. **No `/.well-known/security.txt`** with a security contact.
20. **CCBot, anthropic-ai, OAI-SearchBot, Bingbot not explicitly named in robots.txt.** They inherit the `User-agent: *` allow so access works, but explicit naming is clearer and future-proof.
21. **No Cache-Control header on HTML.** Relies on ETag only.
22. **CLS risk on hero and service images.** Verify explicit width/height attributes.

---

## Category Deep Dives

### AI Citability (58/100)

**Strongest citable assets:**
- Limehome partnership metrics: 9.2 Booking Score (from 8.9), 9.4 Cleanliness Score (from 8.9), 24 months above 9.0. Self-contained, specific, unique. Citability 82/100.
- llms.txt company facts: founded 2012, 50+ projects, 9.5/10 satisfaction, phone number. Citability 78/100.
- EU Ecolabel plus bilingual operations as a differentiator. Citability 68/100.
- FAQ entry "What areas do you serve?" in direct Q and A format. Citability 65/100.

**Citation-unlikely content:**
- Hero copy ("Elevating Property Standards. Precision hygiene...") is marketing language with no extractable fact. Citability 22/100.
- JavaScript-rendered stat counters showing "0+" in raw HTML. Citability 15/100.
- Six service tiles with single-sentence blurbs and no specifics. Citability 28/100.

**Rewrite pattern to apply site-wide:** Lead every section with one quotable fact, number, or distinct claim. A sentence that could be pasted into an AI answer without stripping context is the standard.

### Brand Authority (18/100)

| Platform | Status | Notes |
|---|---|---|
| Wikipedia (EN + HU) | Absent | Zero API results for "CEEFM" or "CEEFM Kft" |
| Wikidata | Absent | No Q-number entity |
| LinkedIn | Minimal | `/company/ceefm` returns 200 but page is thin |
| Reddit | Absent | No mentions |
| YouTube | Absent | No channel |
| Trustpilot | Absent | No review profile |
| Google Business Profile | Unverified | Needs to be claimed |
| IFMA Hungary / industry directories | Not found | Major gap |
| Hungarian business registries | Likely present as a Kft but not indexed to AI | |

This is the single largest pulled-down category and the best 90-day lever.

### Content E-E-A-T (34/100)

| Pillar | Score | Evidence |
|---|---|---|
| Experience | 10/25 | Only the Limehome mention; no project stories, no process docs, no named experience |
| Expertise | 8/25 | Generic service copy; EU Ecolabel not shown on-page despite being the headline credential; no methodology |
| Authoritativeness | 7/25 | No industry memberships, no press, no certifications visible, single-page site limits topical breadth |
| Trustworthiness | 11/25 | HTTPS and email present; missing address, cégjegyzékszám, adószám, third-party reviews, terms |

Word count is around 1,200 across the full homepage. Readability sits in the B2B-appropriate range (Flesch 50-55). The dominant AI-slop signal is parallel three-bullet service descriptions with matching cadence and generic benefit language. The Limehome block breaks the pattern with real numbers and reads human.

### Technical GEO (78/100)

The strongest category. Positives dominate:

- Astro static build ships 48KB of fully rendered HTML. AI crawlers see 100% of content without executing JavaScript.
- robots.txt explicitly allows GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended.
- Sitemap and sitemap-index present.
- Canonical, hreflang (en, hu, x-default), and meta robots correct.
- llms.txt present and spec-compliant.
- OG and Twitter Card meta complete.
- Brotli compression active.
- Hero image preloaded with `fetchpriority="high"`, DNS prefetch for third parties.

Weakness is entirely in security and freshness headers:

- HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy all missing.
- No Cache-Control for HTML.
- Sitemap has no `<lastmod>` dates.
- No `security.txt`.

### Schema and Structured Data (52/100)

One LocalBusiness JSON-LD block is present. It validates structurally but has critical gaps:

| Field | Status |
|---|---|
| @context, @type, name, url, email, foundingDate, logo, image, priceRange | Present |
| aggregateRating | Risky: self-declared without Review nodes, triggers Google manual action risk |
| telephone | Missing |
| address (PostalAddress) | Missing |
| geo (GeoCoordinates) | Missing |
| openingHoursSpecification | Missing |
| sameAs | Missing (critical for entity linking) |
| contactPoint | Missing |
| areaServed | Only "Hungary", brand includes "CEE" |
| serviceType | Flat strings; should be structured Service nodes |
| FAQPage | Missing (FAQ visible on page) |
| Organization (separate) | Missing |

Recommendation: upgrade type from `LocalBusiness` to `ProfessionalService` (a subclass) which retains local fields while fitting B2B service delivery across CEE. Full replacement JSON-LD is provided in Appendix A.

### Platform Optimization (54/100)

| Platform | Score | Rating | Primary Gap |
|---|---|---|---|
| Google AI Overviews | 62 | Moderate | FAQPage + Service schema, more URLs |
| Perplexity | 58 | Moderate | Source-linked claims, more case studies |
| Gemini | 55 | Moderate | Google Business Profile, sameAs |
| ChatGPT Web Search | 48 | Weak-Moderate | No Wikipedia entity, no sameAs |
| Bing Copilot | 45 | Weak | No Bing verification, no IndexNow, thin content |

---

## Quick Wins (Implement This Week)

1. **Replace JS stat counters with server-rendered text.** Ship "50+ Properties Managed / 95% Client Retention / 12+ Years Experience" as static HTML. Keep the animation on top if desired. Biggest single citability lift.

2. **Add the Hungarian legal imprint block to the footer.** Registered address, cégjegyzékszám, adószám, managing director name, phone +36 30 600 5400. Legal requirement and trust boost.

3. **Complete the LocalBusiness JSON-LD.** Add telephone, PostalAddress, geo, openingHoursSpecification, sameAs array (LinkedIn at minimum), and either add Review nodes or remove aggregateRating. Code block in Appendix A.

4. **Surface the EU Ecolabel certification** on the homepage with logo, certificate number, and scope. Add as a dedicated section near the top.

5. **Claim and complete Google Business Profile.** Address, hours, service categories, photos. Add the GBP URL to the schema sameAs array.

---

## 30-Day Action Plan

### Week 1: Truth and Trust Foundations
- [ ] Replace JS stat counters with static HTML values (50+, 95%, 12+)
- [ ] Add Hungarian legal imprint to footer (address, cégjegyzékszám, adószám, director)
- [ ] Surface EU Ecolabel certification block on homepage with logo and cert number
- [ ] Add complete LocalBusiness/ProfessionalService JSON-LD per Appendix A
- [ ] Add security headers via `public/_headers` (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy)

### Week 2: Entity and Platform Signals
- [ ] Claim Google Business Profile, upload 10+ photos, add services
- [ ] Complete LinkedIn company page (description, banner, services, 3 founding posts)
- [ ] Create Wikidata item for CEEFM Kft
- [ ] List on IFMA Hungary, Budapest Chamber of Commerce, facility-management.hu
- [ ] Verify Bing Webmaster Tools, submit sitemap, add IndexNow key file
- [ ] Update llms.txt: add Limehome metrics, add Hungarian section, link /hu/
- [ ] Publish /llms-full.txt with full homepage content as clean markdown

### Week 3: Content Breadth and Case Studies
- [ ] Publish /case-studies/limehome as a full dated page with metrics
- [ ] Draft and publish 3 additional case studies from existing 50+ projects
- [ ] Split homepage into 6 dedicated service pages (facility management, hygiene, maintenance, hotel housekeeping, student housing, apartment complex)
- [ ] Publish /about with named leadership, photos, credentials, and bios
- [ ] Add FAQPage JSON-LD to wrap the existing FAQ section
- [ ] Replace Unsplash stock with real CEEFM photography (teams, equipment, sites)

### Week 4: Topical Authority and Freshness
- [ ] Launch /insights with 4 pillar articles: Hungarian FM compliance, hotel turnover SOPs, apartment complex maintenance, green cleaning standards
- [ ] Add sitemap `<lastmod>` dates via `@astrojs/sitemap` config
- [ ] Mirror all new pages to `/hu/` with translations via scripts/translate.mjs
- [ ] Publish first monthly operations note on LinkedIn with a link back to a dedicated site page
- [ ] Re-run GEO audit to measure delta; target 70+/100

---

## Appendix A: Recommended LocalBusiness JSON-LD

Replace the existing `<script type="application/ld+json">` block in `src/layouts/BaseLayout.astro`. Fill the placeholder values before shipping.

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://ceefm.eu/#organization",
  "name": "CEEFM Kft",
  "legalName": "CEEFM Kft",
  "description": "Professional facility management and hygiene services for apartment complexes, hotels, and student housing in Budapest and across Hungary and CEE.",
  "url": "https://ceefm.eu",
  "logo": "https://ceefm.eu/logo.png",
  "image": "https://ceefm.eu/og-image.jpg",
  "email": "office@ceefm.eu",
  "telephone": "+36-30-600-5400",
  "foundingDate": "2012",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[REPLACE: street + number]",
    "addressLocality": "Budapest",
    "postalCode": "[REPLACE: 1xxx postcode]",
    "addressCountry": "HU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[REPLACE: e.g. 47.4979]",
    "longitude": "[REPLACE: e.g. 19.0402]"
  },
  "areaServed": [
    {"@type": "Country", "name": "Hungary"},
    {"@type": "Country", "name": "Austria"},
    {"@type": "Country", "name": "Romania"},
    {"@type": "Country", "name": "Slovakia"}
  ],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "17:00"
  }],
  "contactPoint": [{
    "@type": "ContactPoint",
    "telephone": "+36-30-600-5400",
    "email": "office@ceefm.eu",
    "contactType": "sales",
    "availableLanguage": ["en","hu"]
  }],
  "sameAs": [
    "[REPLACE: https://www.linkedin.com/company/ceefm]",
    "[REPLACE: https://www.facebook.com/ceefm if exists]",
    "[REPLACE: Google Business Profile URL once claimed]"
  ],
  "knowsLanguage": ["hu","en"],
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "name": "EU Ecolabel Certified"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Facility Management Services",
    "itemListElement": [
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Integrated Facility Management"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Professional Hygiene and Cleaning"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Technical Property Maintenance"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Hotel Housekeeping"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Student Housing Management"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Apartment Complex Services"}}
    ]
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1","h2",".hero-description",".services-intro"]
  }
}
```

Mirror the block on `/hu/` with the description translated to Hungarian.

---

## Appendix B: Security Headers File

Create `public/_headers` in the Astro project:

```
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: upgrade-insecure-requests

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable
```

Also create `public/.well-known/security.txt`:

```
Contact: mailto:office@ceefm.eu
Expires: 2027-04-22T00:00:00.000Z
Preferred-Languages: en, hu
```

---

## Appendix C: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| https://ceefm.eu/ | CEEFM Kft \| Professional Facility Management - Hungary & CEE | JS-rendered zero counters, incomplete schema, missing legal imprint, single case study, no FAQPage markup |
| https://ceefm.eu/hu/ | Hungarian mirror | Same issues mirrored; hreflang correct |

---

*office@bridgeworks.agency · bridgeworks.agency*
