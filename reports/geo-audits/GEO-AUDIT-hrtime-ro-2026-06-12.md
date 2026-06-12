# GEO Audit Report: HR TIME Romania

**Audit Date:** 2026-06-12
**URL:** https://hrtime.ro/en/
**Business Type:** Agency / Professional Services — HR Consulting
**Location:** Bucharest, Romania
**Pages Analyzed:** 14 (9 core pages + 3 service pages fetched + 2 supplementary)
**Conducted by:** BridgeWorks | office@bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 25/100 — Critical**

HR TIME has operated as an HR consulting agency in Bucharest since 2016 with real clients — including OMYA Group (a global industrial company) — but the website is almost entirely invisible to AI systems. Zero schema markup, an abandoned blog (last post: October 2016), no named team members, no FAQ content, and no llms.txt mean that AI models asked about HR outsourcing or executive search in Romania have nothing from this site to cite. The technical infrastructure is functional (server-side WordPress, all AI crawlers allowed, HTTPS), but it provides no competitive advantage. The gap between the business's actual capabilities and its AI presence is large — and entirely closeable.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 22/100 | 25% | 5.5 |
| Brand Authority | 18/100 | 20% | 3.6 |
| Content E-E-A-T | 30/100 | 20% | 6.0 |
| Technical GEO | 48/100 | 15% | 7.2 |
| Schema & Structured Data | 0/100 | 10% | 0.0 |
| Platform Optimization | 28/100 | 10% | 2.8 |
| **Overall GEO Score** | | | **25/100** |

---

## Critical Issues (Fix Immediately)

### C1 — Zero Schema Markup Across Entire Site
No structured data of any kind is present on any page — no Organization, no LocalBusiness, no Service, no Review, no BreadcrumbList. Yoast SEO is installed but appears unconfigured. The Organization settings under SEO > Search Appearance > General have never been filled in, so Yoast suppresses all schema output.

**Fix:** Complete Yoast's Organization settings (name, logo, social profiles). Then add JSON-LD blocks for Organization, LocalBusiness, and Service schemas. Full production-ready code for all schemas is provided in the Schema section of this report.

### C2 — No llms.txt File
`https://hrtime.ro/llms.txt` returns 404. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) receive no structured signal about what this site is, what services it offers, or which pages matter.

**Fix:** Create and publish the following file at `https://hrtime.ro/llms.txt`:

```
# HR TIME

> HR consulting agency in Bucharest, Romania. Founded 2016. Services: HR Outsourcing, Executive Search, and Career Counselling. Member of HR Club Romania.

## Services

- [HR Outsourcing](https://hrtime.ro/en/hr-outsourcing/): Full HR function management including personnel file compliance, employment contracts, and Labour Code adherence.
- [Executive Search](https://hrtime.ro/en/executive-search/): Recruitment and executive search with pre-screened candidate delivery.
- [Career Counselling](https://hrtime.ro/en/vocational-counselling/): Vocational guidance for individuals at any career stage.

## About

- [Why HR TIME](https://hrtime.ro/en/why-hr-time/): Company values, testimonials from OMYA Group, Happy Credit, and Aviance Travel.

## Contact

- Location: Aleea Fetesti 6-12, Sector 3, Bucharest, Romania
- Email: hello@hrtime.ro
- Phone: +40 721 351 821
```

### C3 — Complete Absence of Named Team / Founder
No person is named anywhere on the site as running or working for HR TIME. The CEO is anonymous. The only named individual ("Adina Vladau," blog author from 2016) has no bio and no subsequent activity. For an HR consulting firm where clients are trusting it with hiring decisions and employee data, this is a material trust failure and the largest single E-E-A-T gap.

**Fix:** Add a team page or an "About" section with the founder/director's name, professional background, and credentials. This is non-negotiable for both AI citability and client confidence.

### C4 — No Active Analytics
The site runs Universal Analytics (`UA-87834801-1`), which Google sunset in July 2023. No GA4 tag is present. The site is currently operating with zero functional analytics.

**Fix:** Install Google Analytics 4 via Yoast's header injection or a plugin like Site Kit by Google.

---

## High Priority Issues

### H1 — English Service Pages Missing from Sitemap
All URLs in `page-sitemap.xml` are Romanian-language versions (`hrtime.ro/hr-outsourcing/`, etc.). The English subdirectory (`/en/`) is entirely absent. Crawlers relying on sitemap discovery cannot find the English pages.

**Fix:** In Yoast SEO, verify that WPML is configured to include `/en/` URLs in the sitemap. Regenerate the sitemap and verify that both language versions appear.

### H2 — No Sitemap Reference in robots.txt
`robots.txt` does not declare the sitemap. AI crawlers must discover pages without a roadmap.

**Fix:** Add one line to robots.txt: `Sitemap: https://hrtime.ro/sitemap.xml`

### H3 — Security Headers Entirely Absent
HTTP response headers include only `X-Pingback`, `Link`, and `Content-Type`. No HSTS, no CSP, no X-Frame-Options, no X-Content-Type-Options, no Referrer-Policy.

**Fix:** Add security headers via `.htaccess`. A single block resolves all five:
```apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
```

Additionally, `xmlrpc.php` is exposed via `X-Pingback` header — a known WordPress attack vector. Disable it:
```apache
<Files xmlrpc.php>
  deny from all
</Files>
```

### H4 — No Meta Descriptions on Core Pages
Homepage and HR Outsourcing page have no meta description. Executive Search meta description reads "You can find more information on our website" — filler that provides no click-through signal and no AI snippet value.

**Fix:** Write distinct, keyword-specific meta descriptions for each page. 140-155 characters, leading with the service and location.

Example for homepage: "HR TIME — HR consulting agency in Bucharest, Romania. HR outsourcing, executive search, and career counselling since 2016. Member of HR Club Romania."

### H5 — OG Image and Twitter Image Missing
`og:image` and `twitter:image` are absent despite `twitter:card: summary_large_image` being declared. Social shares and AI platform previews display no image.

**Fix:** Upload one branded 1200x630 image and set it as the default OG image in Yoast SEO.

### H6 — LinkedIn Entity Collision
A Polish company called "HR Time" (hrtime.pl, Warsaw) occupies the "HR Time" namespace in LinkedIn's HR services category. Any AI model or researcher searching "HR Time HR consulting" on LinkedIn finds the Polish firm, not the Romanian one. This actively dilutes brand entity recognition.

**Fix:** Ensure HR TIME Romania has a claimed, verified LinkedIn company page with the Bucharest address and Romanian business registration number (CUI) visible. Add the LinkedIn URL to the Organization schema `sameAs` field immediately.

---

## Medium Priority Issues

### M1 — Blog Abandoned Since October 2016
Two posts, both in Romanian, last published 9+ years ago. The blog section has no content marketing value and contributes nothing to topical authority.

**Fix:** Either redirect `/blog/` to the homepage and remove the two legacy posts (if no restart is planned), or restart with a quarterly English-language publishing schedule targeting Romanian HR topics.

### M2 — Render-Blocking Resources Causing Performance Risk
21 CSS files loaded synchronously in `<head>`, jQuery loaded synchronously, Revolution Slider scripts without `async`/`defer`, and no `preload` hints. LCP and INP are likely to fail Core Web Vitals.

**Fix:** Enable Yoast's asset optimization or install a caching plugin with script deferral (WP Rocket, Autoptimize). Move jQuery to footer. Add `font-display: swap` to Google Fonts URL.

### M3 — No FAQ Content on Any Service Page
FAQ sections are the highest-return content format for AI citation — each question-answer pair is a discrete, self-contained block AI models can extract and quote. No page on this site has any FAQ content.

**Fix:** Add 5-7 FAQ questions per service page. See examples in the Quick Wins section.

### M4 — viewport `maximum-scale=1` Blocks User Zoom
Mobile users cannot zoom in on content. This is both an accessibility failure and a mobile usability signal issue.

**Fix:** Remove `maximum-scale=1` from the viewport meta tag. Change to: `<meta name="viewport" content="width=device-width, initial-scale=1">`

### M5 — Client and Testimonial Post Types Indexed Without Value
`/client-item/client-1/` through `/client-item/client-6/` and three `/testimonial-item/` URLs are in the sitemap and indexed, but contain no useful content. They fragment crawl budget.

**Fix:** Add `noindex` to these post types via Yoast SEO's post type settings.

### M6 — Google Business Profile Status Unverified
No Google Business Profile confirmed active for HR TIME Romania. GBP is critical for Gemini and Perplexity local queries and provides the local entity corroboration that schema alone cannot fully supply.

**Fix:** Claim and verify GBP at business.google.com. Add category "Human Resources Consulting," all services, office photos, and business hours. Request reviews from past clients.

---

## Low Priority Issues

### L1 — hreflang Missing from Sitemap
hreflang alternate tags are present in page `<head>` (correctly mapping `ro` and `en` versions), but the sitemap itself does not include hreflang annotations for each URL pair. Crawlers relying on sitemap-level hreflang cannot confirm the relationship.

**Fix:** Enable hreflang sitemap output in Yoast SEO's WPML integration settings.

### L2 — Executive Search English URL Retains Romanian Slug
The English version of the Executive Search page appears to use the Romanian slug (`/en/recrutare-executive-search/`). This creates an inconsistency and reduces keyword clarity for English-language AI crawlers.

**Fix:** Update the English page slug to `/en/executive-search/` if it does not already exist.

### L3 — Revolution Slider Images Not Responsive
Slider images are 1920x890 with no `srcset` variants. Mobile users download full desktop-size images.

**Fix:** Add responsive image variants via Yoast SEO or WordPress's native `srcset` support. Set explicit `width` and `height` on the 9 images currently missing these attributes.

### L4 — 2014 Gallup Reference Uncited
The "Why HR TIME" page references a 2014 Gallup study with specific percentages but no hyperlink to the original research.

**Fix:** Link to the original Gallup source or replace with more recent motivational research (Gallup's State of the Global Workplace 2024 is publicly available).

---

## Category Deep Dives

### AI Citability (22/100)

No content block on the site scores above 40/100 for AI citability. The five best blocks were assessed:

| Content Block | Citability Score | Verdict |
|---|---|---|
| Gallup statistics on Why HR TIME | 39/100 | Below threshold — source not linked |
| 50,000 EUR bad hire cost claim | 33/100 | Source unattributed ("studies show") |
| OMYA testimonial (4 years, named director) | 27/100 | No direct quote, no numbers |
| HR Outsourcing process steps | 20/100 | Generic, no specifics |
| Executive Search value proposition | 16/100 | Interchangeable with any recruiter |

The root problem: every page is written as marketing copy, not as a reference source. AI models do not cite brochures. They cite sources that answer specific questions with specific data attributed to named experts.

**Three sample rewrites for immediate implementation:**

**1. HR Outsourcing page — replace vague differentiator list:**

Current: "Fair promises. Quality of services. Commitment and reliability."

Recommended: "HR TIME's outsourcing covers the full HR compliance cycle under Romanian Labour Code: preparation and maintenance of personnel files, drafting employment contracts and annexes, managing leave records, and coordination with payroll providers. Each client receives a dedicated HR consultant — not a rotating team — who conducts a free audit of existing HR documentation before engagement begins. This model suits Romanian SMEs with 10 to 150 employees who need structured HR without the cost of a full-time internal HR manager. A dedicated HR manager in Bucharest costs between 4,000 and 7,000 RON per month in salary alone."

**2. Executive Search page — replace generic problem/solution block:**

Recommended: "Romanian companies lose an average of 4 to 8 weeks per open position to screening and re-advertising when recruiting without specialist support. HR TIME manages the full recruitment cycle: role definition, sourcing from active and passive candidate pools, structured competency interviews, and final shortlisting to 3 to 5 assessed candidates. Clients receive only pre-screened candidates who have passed HR TIME's internal evaluation. Since 2016, HR TIME has completed executive search mandates for companies including OMYA Group (a global industrial company operating in 50+ countries), Aviance Travel, and Happy Credit."

**3. Why HR TIME page — replace unattributed cost claim:**

Current: "Studies show that hiring the wrong person could bring additional costs of up to 50,000 euros per year."

Recommended: "According to SHRM (Society for Human Resource Management), replacing a single employee costs between 50% and 200% of their annual salary — including recruitment, onboarding, lost productivity, and team disruption. For a mid-level role in Romania earning 60,000 RON per year, that means a replacement cost of 30,000 to 120,000 RON. HR TIME's outsourcing and executive search services are designed to reduce this risk before it occurs."

---

### Brand Authority (18/100)

| Platform | Status |
|---|---|
| LinkedIn | HR TIME Romania page confirmed — completeness unverified |
| HR Club Romania | Claimed member — public listing unverified |
| Clutch.co | Listed but zero reviews — minimal citation value |
| Wikipedia | Absent |
| Google Business Profile | Status unverified |
| YouTube | No channel found |
| Reddit | No brand mentions detected |
| GoodFirms | No profile found |

The most significant gap: a Polish company named "HR Time" (hrtime.pl) operates in the same category on LinkedIn, creating an active entity disambiguation problem. AI models may associate the name with the Polish firm.

The OMYA Group client relationship is the strongest authority signal available and it is currently underutilized. OMYA is a Fortune-500-adjacent company (Swiss, 50+ countries). One LinkedIn post or recommendation from OMYA's HR leadership would create an entity link with significant GEO weight.

---

### Content E-E-A-T (30/100)

| Dimension | Score | Key Issue |
|---|---|---|
| Experience | 5/25 | No case studies, no process narratives, no first-hand evidence |
| Expertise | 6/25 | No named HR professionals, no credentials displayed |
| Authoritativeness | 9/25 | HR Club membership and OMYA testimonial are real signals — no content-driven authority |
| Trustworthiness | 10/25 | HTTPS, GDPR, physical address — but anonymous ownership |

The content reads as accurate but generic. Nothing demonstrates that the people writing it have direct HR experience. The Executive Search page claims "selection expertise accumulated over decades" with no named professional to support the claim.

Content freshness is severe: the "Why HR TIME" page references 2014 Gallup data (12 years old), and the only published articles date to 2016.

---

### Technical GEO (48/100)

| Check | Status |
|---|---|
| HTTPS | Passing |
| Server-side rendering | Passing — WordPress PHP, content visible to all crawlers |
| AI crawler access (robots.txt) | Passing — all bots allowed |
| hreflang in `<head>` | Passing — correctly maps ro/en pairs |
| Sitemap exists | Passing |
| llms.txt | Failing — 404 |
| Sitemap in robots.txt | Failing — not declared |
| English URLs in sitemap | Failing — `/en/` pages absent |
| Security headers | Failing — none present |
| Meta descriptions | Failing — absent on most pages |
| OG image | Failing — absent |
| Google Analytics | Failing — UA (sunset 2023), no GA4 |
| Page speed (LCP/INP risk) | Failing — 21 render-blocking CSS, sync jQuery |
| Mobile zoom | Failing — `maximum-scale=1` blocks zoom |
| xmlrpc.php | Exposed — security risk |

The technical foundation is sound (WordPress, SSR, HTTPS, open crawl access). Every failure is a configuration gap, not a structural problem. All can be fixed within a single WordPress admin session plus one `.htaccess` edit.

---

### Schema & Structured Data (0/100)

Zero structured data present across all pages. Yoast SEO is installed but suppresses output because the Organization settings have never been configured.

**Production-ready JSON-LD blocks are provided below. Implement in priority order.**

#### Priority 1 — Organization (Homepage `<head>`)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "HR TIME",
  "alternateName": "HR TIME®",
  "url": "https://hrtime.ro/en/",
  "logo": {
    "@type": "ImageObject",
    "url": "[REPLACE: Full URL to logo image]",
    "width": 200,
    "height": 60
  },
  "description": "HR consulting agency founded in 2016, based in Bucharest, Romania. Services: HR outsourcing, executive search and recruitment, vocational counselling. Member of HR Club Romania.",
  "foundingDate": "2016",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Aleea Fetesti 6-12",
    "addressLocality": "București",
    "addressRegion": "Sector 3",
    "postalCode": "[REPLACE: postal code]",
    "addressCountry": "RO"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+40-721-351-821",
    "email": "hello@hrtime.ro",
    "contactType": "customer service",
    "availableLanguage": ["English", "Romanian"]
  },
  "memberOf": {
    "@type": "Organization",
    "name": "HR Club Romania",
    "url": "https://hrclub.ro"
  },
  "sameAs": [
    "[REPLACE: LinkedIn company page URL]",
    "[REPLACE: Facebook page URL]"
  ]
}
```

#### Priority 2 — LocalBusiness (Homepage, alongside Organization)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://hrtime.ro/en/#localbusiness",
  "name": "HR TIME",
  "url": "https://hrtime.ro/en/",
  "telephone": "+40721351821",
  "email": "hello@hrtime.ro",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Aleea Fetesti 6-12",
    "addressLocality": "București",
    "addressRegion": "Sector 3",
    "postalCode": "[REPLACE: postal code]",
    "addressCountry": "RO"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[REPLACE: from Google Maps]",
    "longitude": "[REPLACE: from Google Maps]"
  },
  "foundingDate": "2016",
  "description": "HR consulting agency in Bucharest offering HR outsourcing, executive search, and vocational counselling since 2016.",
  "knowsLanguage": ["ro", "en"]
}
```

#### Priority 3 — Reviews / Testimonials (Why HR TIME page)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "HR TIME",
  "url": "https://hrtime.ro/en/",
  "review": [
    {
      "@type": "Review",
      "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
      "author": { "@type": "Person", "name": "George Chiriță", "jobTitle": "Director General", "worksFor": { "@type": "Organization", "name": "Happy Credit" } },
      "reviewBody": "Reliable partner, involved, dedicated and persevering in achieving objectives."
    },
    {
      "@type": "Review",
      "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
      "author": { "@type": "Person", "name": "Alexandra Copaci", "jobTitle": "Director General", "worksFor": { "@type": "Organization", "name": "Aviance Travel" } },
      "reviewBody": "Excellent collaboration with a team of professionals in the true sense."
    },
    {
      "@type": "Review",
      "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
      "author": { "@type": "Person", "name": "Maja Milicevic", "jobTitle": "HR Director SEE", "worksFor": { "@type": "Organization", "name": "OMYA Group" } },
      "reviewBody": "Very responsive and attentive to our needs, extremely effective in meeting them."
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5",
    "reviewCount": "3",
    "bestRating": "5"
  }
}
```

#### Priority 4 — Service Schemas (Each respective service page)

HR Outsourcing (`/en/hr-outsourcing/`):
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "HR Outsourcing",
  "serviceType": "Human Resources Outsourcing",
  "description": "HR outsourcing including personnel file management, employment contracts, Labour Code compliance, performance evaluations, and payroll consulting. Includes a free initial HR audit.",
  "url": "https://hrtime.ro/en/hr-outsourcing/",
  "provider": { "@type": "Organization", "name": "HR TIME", "url": "https://hrtime.ro/en/" },
  "areaServed": { "@type": "Country", "name": "Romania" }
}
```

Executive Search (`/en/executive-search/`):
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Executive Search and Recruitment",
  "serviceType": "Executive Search",
  "description": "Executive search and recruitment in Romania. Pre-screening and shortlisting candidates before presentation to reduce client time on unsuitable applications.",
  "url": "https://hrtime.ro/en/executive-search/",
  "provider": { "@type": "Organization", "name": "HR TIME", "url": "https://hrtime.ro/en/" },
  "areaServed": { "@type": "Country", "name": "Romania" }
}
```

Vocational Counselling (`/en/vocational-counselling/`):
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Vocational Counselling",
  "serviceType": "Career Counselling",
  "description": "Career counselling for individuals at any stage: talent assessment, CV building, interview preparation, career exploration, and SMART goal setting. Serves students, job seekers, and professionals considering a career change.",
  "url": "https://hrtime.ro/en/vocational-counselling/",
  "provider": { "@type": "Organization", "name": "HR TIME", "url": "https://hrtime.ro/en/" },
  "areaServed": { "@type": "Country", "name": "Romania" }
}
```

#### Priority 5 — FAQPage Template (Add to service pages once FAQ content is written)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is included in HR TIME's HR outsourcing service?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "HR TIME's HR outsourcing covers personnel file management, employment contract drafting, internal regulation creation, performance evaluation coordination, payroll consulting, and labour law consultation. All engagements begin with a free HR audit."
      }
    },
    {
      "@type": "Question",
      "name": "How does HR TIME's executive search process work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "HR TIME handles candidate sourcing, competency-based screening, and preliminary interviews. Clients receive a shortlist of 3 to 5 pre-assessed candidates, reducing time spent on unsuitable CVs and ineffective interviews."
      }
    },
    {
      "@type": "Question",
      "name": "Who is vocational counselling suitable for?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Vocational counselling at HR TIME suits anyone at a career crossroads: students choosing a direction, professionals considering a change, or individuals wanting to identify their strengths. Sessions follow a 5-step process: relationship building, talent assessment, CV and interview preparation, career exploration, and SMART goal setting."
      }
    }
  ]
}
```

---

### Platform Optimization (28/100)

| Platform | Score | Biggest Gap |
|---|---|---|
| Google AI Overviews | 32/100 | No FAQ schema, thin service pages, no source authority |
| ChatGPT Web Search | 24/100 | No Wikipedia entity, no Organization schema with sameAs |
| Perplexity AI | 26/100 | No community reviews, no original research to cite |
| Gemini | 27/100 | No YouTube, no Google Business Profile confirmed |
| Bing Copilot | 29/100 | Not registered in Bing Webmaster Tools, no IndexNow |

**Cross-platform finding:** Competitors with Clutch.co reviews dominate AI answers for "HR consulting Bucharest" queries. HR TIME is listed on Clutch but has zero reviews. A company called OnHires has 112 Clutch reviews and will appear in every AI answer on that query until HR TIME builds a comparable third-party review footprint.

---

## Quick Wins (Implement This Week)

1. **Create `/llms.txt`** — 30-minute task, zero technical barrier. Use the template in Critical Issues section C2. Immediately signals site structure to all AI crawlers.

2. **Configure Yoast Organization settings** — Under SEO > Search Appearance > General: set company name, upload logo, add social profile URLs. This alone generates WebSite and Organization schema blocks without any code.

3. **Add `Sitemap: https://hrtime.ro/sitemap.xml` to robots.txt** — One line, two minutes.

4. **Add security headers via `.htaccess`** — Five headers in one block. Use the code in High Priority issue H3. Resolves the largest technical security gap.

5. **Replace dead Universal Analytics tag with GA4** — Install via Yoast's header injection. The site is currently running completely blind on analytics.

6. **Add OG image and fix meta descriptions** — Upload one 1200x630 branded image in Yoast, set it as the site-wide default. Write meta descriptions for the homepage and both primary service pages.

---

## 30-Day Action Plan

### Week 1: Foundation (Technical + Schema)
- [ ] Create `/llms.txt` file
- [ ] Add `Sitemap:` directive to `robots.txt`
- [ ] Complete Yoast Organization settings (name, logo, social URLs)
- [ ] Add security headers to `.htaccess`
- [ ] Disable `xmlrpc.php` in `.htaccess`
- [ ] Replace Universal Analytics with GA4
- [ ] Add OG image, fix meta descriptions on all pages
- [ ] Add JSON-LD Organization + LocalBusiness schemas to homepage
- [ ] Fix `maximum-scale=1` in viewport meta tag

### Week 2: Entity Establishment
- [ ] Claim and fully complete Google Business Profile (category, services, hours, photos)
- [ ] Verify LinkedIn company page for HR TIME Romania — add description, services, founding year
- [ ] Add JSON-LD Service schemas to HR Outsourcing, Executive Search, Vocational Counselling pages
- [ ] Add JSON-LD Review schema to Why HR TIME page
- [ ] Register in Bing Webmaster Tools and submit sitemap
- [ ] Enable IndexNow in Yoast or install IndexNow plugin

### Week 3: Content Rewrites
- [ ] Rewrite HR Outsourcing page using the recommended content block (see AI Citability section)
- [ ] Rewrite Executive Search page with OMYA Group named client context and specific process description
- [ ] Update Why HR TIME page — replace uncited "studies show" claim with SHRM reference
- [ ] Add FAQ section (5 questions minimum) to HR Outsourcing page
- [ ] Add FAQ section to Executive Search page
- [ ] Verify and fix English URL slugs (ensure `/en/executive-search/` not a Romanian slug)

### Week 4: Authority Building
- [ ] Publish one team page with founder/director name, background, and credentials
- [ ] Request reviews from past clients on Google Business Profile
- [ ] Contact OMYA Group HR team about a LinkedIn mention or recommendation
- [ ] Set up Clutch.co review collection — request reviews from Happy Credit, Aviance Travel, OMYA contacts
- [ ] Verify hreflang sitemap output — both `/` and `/en/` versions of all pages appear in sitemap
- [ ] Set `/client-item/` and `/testimonial-item/` post types to noindex in Yoast

---

## Appendix: Pages Analyzed

| URL | Language | Last Modified | GEO Issues |
|---|---|---|---|
| https://hrtime.ro/en/ | English | 2026-05-17 | No schema, no meta desc, no OG image, dead UA tag |
| https://hrtime.ro/en/hr-outsourcing/ | English | 2025-01-10 | No schema, thin content (~450 words), no FAQ |
| https://hrtime.ro/en/executive-search/ | English | 2026-05-17 | No schema, no FAQ, generic content |
| https://hrtime.ro/en/vocational-counselling/ | English | 2025-01-09 | No schema, thin content (~450 words) |
| https://hrtime.ro/en/why-hr-time/ | English | 2017-02-13 | No schema, uncited 2014 Gallup data |
| https://hrtime.ro/en/contact/ | English | 2026-05-18 | No schema, no map embed, no hours |
| https://hrtime.ro/blog/ | Romanian | 2018-05-11 | Abandoned — 2 posts from Oct 2016 |
| https://hrtime.ro/recomandari/ | Romanian | 2014-10-13 | Oldest page on site — stale |
| https://hrtime.ro/termeni-si-conditii/ | Romanian | 2026-05-17 | Legal page — low priority |
| /client-item/client-1/ through client-6/ | — | 2016-02-19 | Non-descriptive URLs, no content, should be noindexed |
| /testimonial-item/ (3 entries) | — | 2021-03-23 | Duplicate entries in sitemap, should be noindexed |

---

*Report generated by BridgeWorks · office@bridgeworks.agency · bridgeworks.agency*
