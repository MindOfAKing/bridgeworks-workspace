# GEO Audit Report: CEE FM (CEEFM Kft)

**Audit Date:** April 3, 2026
**URL:** https://ceefm.eu
**Business Type:** Local B2B Services (Facility Management)
**Pages Analyzed:** 2 (English homepage, Hungarian homepage)

---

## Executive Summary

**Overall GEO Score: 29/100 (Poor)**

CEE FM's website is largely invisible to AI search engines. The site has one genuine technical strength: it uses Astro (a static site generator) that delivers fully server-rendered HTML, meaning AI crawlers can read the content. However, the content itself is thin (1,200 words across one page), the brand has near-zero presence on platforms AI models cite (no LinkedIn, no YouTube, no Reddit, no Wikipedia), and the structured data contains fabricated ratings and incorrect geographic claims that risk penalties. The site allows all major AI crawlers in robots.txt and has llms.txt and hreflang implemented, but these technical positives cannot compensate for the fundamental lack of citable content and off-site authority signals.

The three highest-impact actions: (1) expand from a 2-URL site to 15+ pages with deep, data-rich content AI systems can quote, (2) build third-party brand signals on LinkedIn, Google Business Profile, and industry directories, and (3) fix the inaccurate schema data before it triggers a Google manual action.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 28/100 | 25% | 7.0 |
| Brand Authority | 10/100 | 20% | 2.0 |
| Content E-E-A-T | 20/100 | 20% | 4.0 |
| Technical GEO | 62/100 | 15% | 9.3 |
| Schema & Structured Data | 32/100 | 10% | 3.2 |
| Platform Optimization | 30/100 | 10% | 3.0 |
| **Overall GEO Score** | | | **29/100** |

---

## Important Technical Correction

The earlier marketing audit stated that ceefm.eu is a "client-side rendered React SPA" where crawlers see an empty `<div id="root"></div>`. Live technical analysis during this GEO audit found this is **incorrect**.

The site is built with **Astro** (static site generator) and serves **fully server-rendered HTML**. All text content, meta tags, JSON-LD structured data, headings, FAQ answers, and service descriptions are present in the initial HTML response without JavaScript execution. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) receive the full content.

This is a significant positive. The rendering problem identified in the marketing audit does not exist. The low GEO score is driven by content thinness, absent brand signals, and schema inaccuracies, not by a rendering blocker.

---

## Critical Issues (Fix Immediately)

### 1. Fabricated aggregateRating in Schema (Risk: Google Manual Action)

**Severity:** Critical
**Location:** JSON-LD in HTML head

The structured data claims 200 ratings with a 9.5/10 score. CEE FM has approximately 50 projects. No third-party review platform (Google Business, Trustpilot) backs this number. Google's guidelines explicitly prohibit fake or misleading review markup.

**Fix:** Remove the `aggregateRating` property entirely. Only re-add it when backed by a verifiable review source (such as Google Business reviews). A fabricated rating is worse than no rating.

### 2. Incorrect areaServed in Schema

**Severity:** Critical
**Location:** JSON-LD in HTML head

The schema lists Hungary, Romania, and Slovakia as service areas. CEE FM operates only in Budapest, Hungary. This creates a false entity profile that AI models will use when building knowledge graphs.

**Fix:** Replace with Budapest-specific area:
```json
"areaServed": {
  "@type": "City",
  "name": "Budapest",
  "containedInPlace": {
    "@type": "Country",
    "name": "Hungary"
  }
}
```

### 3. Missing Security Headers

**Severity:** Critical
**Location:** Hostinger server configuration

No HSTS, no X-Frame-Options, no X-Content-Type-Options, no Referrer-Policy, no Permissions-Policy. The only CSP directive is `upgrade-insecure-requests`. Security headers are trust signals for both search engines and AI systems evaluating source credibility.

**Fix:** Add via `.htaccess` or Hostinger hosting panel. 30-minute fix.

---

## High Priority Issues

### 4. Zero Third-Party Brand Presence

**Severity:** High

CEE FM has no LinkedIn company page, no YouTube channel, no Google Business Profile (found), no Reddit mentions, no Wikipedia article, no Wikidata entry, and no listing in Hungarian FM industry directories. AI models cannot verify this entity exists beyond the website itself. The Limehome partnership, CEE FM's strongest credibility signal, exists only on the CEE FM website and is not confirmed by any third-party source.

### 5. Only 2 URLs in Entire Site

**Severity:** High

The sitemap contains only `ceefm.eu/` and `ceefm.eu/hu/`. A 2-URL site cannot establish topical authority. AI systems cannot cite specific service pages because they do not exist. There is no `/services/deep-cleaning`, no `/industries/hotels`, no `/about`, no `/blog`.

### 6. No llms.txt File

**Severity:** High

**Note:** The Technical subagent reported llms.txt as present, but direct fetch attempts returned the homepage instead of a dedicated file. Status is uncertain. If the file exists, it may be malformed or redirecting. If it does not exist, this is a missed opportunity for a low-effort, high-impact action.

### 7. Content Too Thin for AI Citation

**Severity:** High

The entire site contains approximately 1,200-1,400 words. A single blog post should have this much. The homepage has no statistics, no case study details, no specific client outcomes, and no original data. The FAQ section has only 3 questions with brief answers. No content block scores above 40/100 on citability assessment. AI systems have nothing worth quoting.

### 8. Zero sameAs Entity Links in Schema

**Severity:** High

The LocalBusiness schema has no `sameAs` property. AI models use `sameAs` to cross-reference entities across platforms. Without it, Google, ChatGPT, and Perplexity cannot connect CEE FM to any external knowledge source.

### 9. Missing Service Schema

**Severity:** High

Six services are described on the page but have zero structured data representation. The `serviceType` property used in the current schema is not a recognized Schema.org property for LocalBusiness and is silently ignored by parsers.

---

## Medium Priority Issues

### 10. No Responsive Images

**Severity:** Medium

All images serve a single fixed size. No `srcset`, no `<picture>` elements, no WebP format. Unsplash images could use URL parameters (`w=400`, `fm=webp`) for responsive delivery. Hero image lacks `fetchpriority="high"` and `<link rel="preload">`.

### 11. Speakable Specification Targets Only Metadata

**Severity:** Medium

The speakable property targets only the `<title>` tag and meta description. It should target actual page content sections (hero text, service descriptions, company overview).

### 12. Sitemap Missing lastmod Dates

**Severity:** Medium

Neither URL in the sitemap has a `<lastmod>` timestamp. Crawlers cannot determine content freshness. Astro can generate these automatically at build time.

### 13. No ARIA Attributes

**Severity:** Medium

Zero ARIA landmarks, labels, or roles detected. This affects accessibility scoring and screen reader navigation.

### 14. No Publication or Update Dates on Content

**Severity:** Medium

No visible dates anywhere on the site. AI models use content freshness as a ranking signal. No "Last updated" indicators mean AI systems cannot determine if content is current.

---

## Low Priority Issues

### 15. Missing FAQPage Schema

**Severity:** Low

Three FAQ questions exist on the page but have no FAQPage structured data. While Google restricted FAQ rich results in August 2023, the schema still provides semantic value for AI models.

### 16. Stock Photography Instead of Original Images

**Severity:** Low

All images are from Unsplash, hosted externally. AI systems may devalue stock imagery. Self-hosted original photos of completed work, team members, and properties would strengthen trust signals.

### 17. Title Tag Slightly Over Optimal Length

**Severity:** Low

"CEEFM Kft | Professional Facility Management - Hungary & CEE" is 63 characters (recommended: under 60). Also references "CEE" which overstates geographic scope.

---

## Category Deep Dives

### AI Citability (28/100)

The homepage content is accessible to AI crawlers (confirmed: Astro SSG serves rendered HTML). However, content quality is the bottleneck.

**Content Block Citability Scores:**

| Content Block | Score | Issue |
|---|---|---|
| Hero headline | 10/100 | Pure marketing language, no factual content |
| 6 Services list | 22/100 | Generic labels without process details, pricing, or outcomes |
| 3 Industries served | 25/100 | Names segments but does not explain approach differences |
| 4 Differentiators | 27/100 | Claims without evidence (e.g., "Compliance & Safety" with no specifics) |
| FAQ: Hungary service area | 38/100 | Best content on site but too brief (2-3 sentences) |
| FAQ: Apartment hotels | 35/100 | Mentions Limehome but lacks specifics |
| FAQ: EU compliance | 33/100 | Declares compliance without naming standards |
| About section | 24/100 | Mentions Limehome but no metrics or timeline |

**Zero content blocks score above 40/100.** An AI model answering "What facility management companies operate in Budapest?" has no compelling reason to cite CEE FM over competitors who publish case studies, pricing guides, and methodology pages.

**What makes content citable for AI:**
- Specific numbers ("reduced common area complaints by 40% in Q1 2025")
- Named clients with permission ("Official FM partner for Limehome's 12 Budapest properties")
- Process descriptions with enough detail to be useful ("Our 7-step deep cleaning protocol uses...")
- Original data not available elsewhere ("Average facility management costs for Budapest apartment complexes range from...")
- Direct answers to specific questions in 40-60 word blocks

CEE FM has none of these.

---

### Brand Authority (10/100)

| Platform | Status | Impact |
|---|---|---|
| Wikipedia | Absent | No article in any language |
| Wikidata | Absent | No structured entity entry |
| LinkedIn | Absent | No company page found |
| YouTube | Absent | No channel or videos |
| Reddit | Absent | Zero mentions |
| Google Business Profile | Not found | May exist but not appearing in search |
| Trustpilot | Absent | Not listed |
| Industry Directories | Absent | Not on ensun.io "Top 37 FM Companies in Hungary" |
| Hungarian Business Registries | Present | Listed on ceginformacio.hu, nemzeticegtar.hu (legal filings only) |
| Limehome Co-mention | Absent externally | Partnership exists only on CEE FM website |

The brand is effectively a ghost online. The only external signals are mandatory Hungarian corporate filings. AI models have zero corroborating evidence to cite when answering queries about facility management in Budapest.

The Limehome partnership is the single most valuable brand signal CEE FM has, but it is invisible to AI systems because no third-party source confirms it. Pursuing a mention on Limehome's website, a joint press release, or a co-authored case study would immediately change the brand authority equation.

---

### Content E-E-A-T (20/100)

| Dimension | Score | Key Evidence |
|---|---|---|
| Experience | 4/25 | Limehome mention is the only experience signal. No case studies, no project details, no before/after evidence. |
| Expertise | 5/25 | Surface-level service descriptions. No methodology, no technical depth, no named experts. |
| Authoritativeness | 6/25 | Founded 2012 and Limehome partnership. Zero certifications displayed. Competitors show ISO 9001, 14001, 27001. |
| Trustworthiness | 7/25 | HTTPS present, contact form exists. But broken stats counter ("0+"), no testimonials, no team transparency. |

**Critical content gaps:**
- No case studies (for a 14-year company with 50+ employees)
- No testimonials (zero named client quotes)
- No team page (no founder story, no employee bios)
- No certifications displayed (competitors display multiple ISO certifications)
- No blog or thought leadership content
- No pricing information or guidance
- Broken stats counter showing "0+" for every metric actively damages credibility
- Total content: approximately 1,200 words (a single blog post should have more)

For a B2B facility management company where property managers hand over building keys, the absence of verifiable experience, named experts, and third-party validation is a primary conversion and citability blocker.

---

### Technical GEO (62/100)

**Strongest category.** The Astro SSG framework is an excellent foundation for AI discoverability.

**What works well:**
- Full server-rendered HTML (all content visible to crawlers)
- robots.txt allows all major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, ChatGPT-User)
- Complete meta tag set (title, description, viewport, robots, OG, Twitter Card)
- Hreflang properly implemented (en, hu, x-default)
- Canonical tags correctly configured
- JSON-LD structured data in HTML head (visible even without JS)
- HTTP-to-HTTPS redirect working
- Speakable specification present

**What needs fixing:**
- Security headers almost entirely absent (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy)
- Only 2 URLs in sitemap (no content depth for crawlers to discover)
- No `<link rel="preload">` for hero image or fonts
- No responsive images (no srcset, no WebP)
- No ARIA attributes for accessibility
- Sitemap missing lastmod dates
- External image hosting on Unsplash (no cache control)
- Multiple inline synchronous scripts

---

### Schema & Structured Data (32/100)

**What exists:**
- LocalBusiness JSON-LD with name, description, URL, telephone, email, foundingDate, logo, priceRange, numberOfEmployees, knowsLanguage
- Speakable specification (targets metadata only)

**What is wrong:**
- `aggregateRating`: Claims 200 ratings (actual: approximately 50 projects). Risk of Google manual action.
- `areaServed`: Lists Romania and Slovakia (actual: Budapest/Hungary only)
- `description`: Says "Central & Eastern Europe" (actual: Budapest/Hungary only)
- `serviceType`: Not a recognized Schema.org property for LocalBusiness. Silently ignored.
- `image`: Points to logo instead of a business photo
- `address`: Missing entirely (required for LocalBusiness rich results)
- `geo`: Missing (recommended for local businesses)
- `openingHoursSpecification`: Missing
- `sameAs`: Missing completely (zero external entity links)

**What is missing:**
- Service schema for 6 services (use OfferCatalog)
- FAQPage schema for 3 FAQ questions
- WebSite schema for basic site identity
- BreadcrumbList schema
- Person schema (when team page is created)

---

### Platform Optimization (30/100)

| Platform | Score | Key Blocker |
|---|---|---|
| Google AI Overviews | 25/100 | Content too thin for citation. No question-based headings. Only 3 FAQ questions. |
| ChatGPT Web Search | 32/100 | No entity verification possible (no LinkedIn, no Wikidata). Content lacks dates and attribution. |
| Perplexity AI | 22/100 | Near-zero community validation (no Reddit, no forums). No original data to cite as primary source. |
| Google Gemini | 30/100 | Invisible across Google ecosystem (no YouTube, no GBP, no Knowledge Graph). |
| Bing Copilot | 30/100 | No IndexNow, no Bing Webmaster Tools, no LinkedIn, minimal Microsoft ecosystem presence. |

**Cross-platform blockers:**
1. Content thinness (all platforms penalize)
2. No entity signals (all platforms need third-party verification)
3. 2-URL site structure (no deep content for specific queries)
4. No community discussion (Perplexity and Gemini weight this heavily)

---

## Quick Wins (Implement This Week)

1. **Fix the broken stats counter.** The hero section shows "0+" for Properties Managed, Client Retention, and Years Experience. Replace with hardcoded real numbers (e.g., "50+ Properties," "95% Retention," "14 Years"). A broken counter on a facility management site communicates carelessness to both humans and AI evaluation systems. *Impact: Medium. Effort: 30 minutes.*

2. **Remove or correct aggregateRating in schema.** Delete the fabricated 200-rating claim. Only re-add when backed by a real review platform. This is a compliance risk, not an optimization. *Impact: High (risk mitigation). Effort: 15 minutes.*

3. **Correct areaServed and description in schema.** Change to Budapest/Hungary only. Remove Romania and Slovakia. *Impact: High. Effort: 15 minutes.*

4. **Add security headers.** Configure HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy via Hostinger panel or .htaccess. *Impact: Medium. Effort: 30 minutes.*

5. **Create or verify llms.txt file.** Deploy a plain-text file at ceefm.eu/llms.txt with company name, services, industries, location, and contact info. If it already exists, verify it returns correct content and not a redirect. *Impact: Medium. Effort: 15 minutes.*

6. **Add lastmod dates to sitemap.** Configure Astro to include `<lastmod>` timestamps when building the sitemap. *Impact: Low-Medium. Effort: 30 minutes.*

7. **Add `<link rel="preload">` for hero image.** Add `fetchpriority="high"` to the hero image and a preload hint in the head. *Impact: Low-Medium. Effort: 15 minutes.*

---

## 30-Day Action Plan

### Week 1: Fix Accuracy and Security

- [ ] Remove fabricated aggregateRating from schema
- [ ] Correct areaServed to Budapest/Hungary only
- [ ] Correct schema description to Budapest/Hungary only
- [ ] Fix broken stats counter with real numbers
- [ ] Add security headers (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy)
- [ ] Create or verify llms.txt
- [ ] Add sameAs property to schema (even if only ceefm.eu for now)
- [ ] Add PostalAddress to LocalBusiness schema
- [ ] Add lastmod dates to sitemap

### Week 2: Build External Brand Signals

- [ ] Create LinkedIn company page for CEEFM Kft with full profile
- [ ] Claim and fully optimize Google Business Profile
- [ ] Add LinkedIn and GBP URLs to schema sameAs
- [ ] Request 3-5 Google Business reviews from current clients
- [ ] Contact Limehome about co-mention (partner page, case study, or press release)
- [ ] Submit site to Hungarian FM industry directories (ensun.io, etc.)

### Week 3: Expand Content Depth

- [ ] Create dedicated service pages (6 pages, 800+ words each)
- [ ] Create dedicated industry pages (apartments, hotels, student housing)
- [ ] Create about/team page with founder bio and key team members
- [ ] Add FAQPage schema wrapping existing FAQ content
- [ ] Add Service schemas via OfferCatalog structure
- [ ] Expand FAQ from 3 to 8-10 questions

### Week 4: Content Authority

- [ ] Write and publish Limehome case study with measurable outcomes
- [ ] Collect and publish 3-5 named client testimonials
- [ ] Create a Budapest facility management pricing guide (original data)
- [ ] Add publication dates and "Last updated" indicators to all pages
- [ ] Update sitemap with all new URLs and lastmod dates
- [ ] Register CEEFM on Wikidata as a Hungarian FM entity

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| https://ceefm.eu/ | CEEFM Kft \| Professional Facility Management - Hungary & CEE | Schema inaccuracies, thin content, no sameAs, missing security headers, broken stats counter |
| https://ceefm.eu/hu/ | (Hungarian version) | Same issues as English version |

---

## Appendix: Recommended Schema Replacements

### Corrected LocalBusiness (replace existing)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "CEE FM",
  "legalName": "CEEFM Kft",
  "description": "Professional facility management and hygiene services for apartment complexes, hotels, and student housing in Budapest, Hungary.",
  "url": "https://ceefm.eu",
  "telephone": "+36306005400",
  "email": "office@ceefm.eu",
  "foundingDate": "2012",
  "logo": {
    "@type": "ImageObject",
    "url": "https://ceefm.eu/logo.png"
  },
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Budapest",
    "addressCountry": "HU"
  },
  "areaServed": {
    "@type": "City",
    "name": "Budapest",
    "containedInPlace": {
      "@type": "Country",
      "name": "Hungary"
    }
  },
  "numberOfEmployees": {
    "@type": "QuantitativeValue",
    "minValue": 50
  },
  "knowsLanguage": ["hu", "en"],
  "sameAs": [
    "[Google Business Profile URL]",
    "[LinkedIn company page URL]"
  ],
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "08:00",
    "closes": "17:00"
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".hero-description", ".about-section"]
  }
}
```

### New: FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What areas in Hungary do you serve?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "CEEFM provides facility management and commercial cleaning services exclusively across Hungary, with a strong operational presence in Budapest."
      }
    },
    {
      "@type": "Question",
      "name": "Do you work with apartment hotels and short-term rentals?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. CEEFM specializes in high-turnover hospitality environments and is the official service partner for Limehome aparthotels in Budapest."
      }
    },
    {
      "@type": "Question",
      "name": "Are your cleaning protocols compliant with EU standards?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "All CEEFM hygiene and waste management programs strictly adhere to EU directives and Hungarian regulatory safety requirements."
      }
    }
  ]
}
```

### New: OfferCatalog with Services

```json
{
  "@context": "https://schema.org",
  "@type": "OfferCatalog",
  "name": "CEE FM Facility Management Services",
  "itemListElement": [
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Deep Cleaning & Sanitization",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    },
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Common Area Maintenance",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    },
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Waste & Hygiene Management",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    },
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Preventive Disinfection",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    },
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Eco Cleaning",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    },
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "Tailored Facility Solutions",
        "provider": {"@type": "LocalBusiness", "name": "CEE FM"},
        "areaServed": {"@type": "City", "name": "Budapest"}
      }
    }
  ]
}
```

---

*Generated by AI Marketing Suite -- `/geo-audit`*

office@bridgeworks.agency . bridgeworks.agency
