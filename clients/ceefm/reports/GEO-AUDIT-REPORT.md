# GEO Audit Report: CEEFM Kft

**Audit Date:** March 29, 2026
**URL:** https://ceefm.eu
**Business Type:** Local Business / Facility Management
**Pages Analyzed:** 1 (single-page application)

---

## Executive Summary

**Overall GEO Score: 16/100 (Critical)**

CEEFM Kft is invisible to AI search systems. The website is a React single-page application that delivers an empty `<div id="root"></div>` to every AI crawler. None of them execute JavaScript. The site has one indexable URL, zero blog posts, zero case studies, and zero Hungarian-language content. The brand has no Wikipedia page, no Reddit presence, no YouTube channel, and only 92 LinkedIn followers. When anyone asks ChatGPT, Claude, Perplexity, or Gemini about facility management in Budapest, CEEFM does not exist.

The strongest signal is the LocalBusiness schema in the HTML head, which crawlers can read. But it is missing address, geo coordinates, sameAs links, and opening hours. The meta tags are well-structured. Everything else is absent.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 8/100 | 25% | 2.0 |
| Brand Authority | 12/100 | 20% | 2.4 |
| Content E-E-A-T | 14/100 | 20% | 2.8 |
| Technical GEO | 33/100 | 15% | 5.0 |
| Schema & Structured Data | 15/100 | 10% | 1.5 |
| Platform Optimization | 24/100 | 10% | 2.4 |
| **Overall GEO Score** | | | **16/100** |

---

## Critical Issues (Fix Immediately)

### 1. SPA renders empty HTML to all AI crawlers
The page body is `<div id="root"></div>`. GPTBot, ClaudeBot, PerplexityBot, and Bingbot see nothing. Googlebot can render JavaScript but with delays. All content exists only in a 233KB JavaScript bundle that non-JS crawlers cannot execute.

**Fix:** Implement server-side rendering (Next.js, Astro) or static site generation. Alternatively, use a pre-rendering service. This is the prerequisite for every other GEO improvement.

### 2. Single URL with zero internal pages
The entire site is one URL: `https://ceefm.eu/`. No service pages, no about page, no blog, no FAQ page. AI models cannot cite specific content because there is no specific content to cite.

**Fix:** Create multi-page architecture with distinct URLs for each service, industry, about, FAQ, and contact.

### 3. No robots.txt or sitemap.xml
The SPA catch-all routing serves the React shell for every URL path, including `/robots.txt` and `/sitemap.xml`. Both return 200 with HTML instead of their expected formats. AI crawlers have no directives and no URL discovery mechanism.

**Fix:** Create proper robots.txt allowing all AI crawlers (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Bingbot) with Sitemap directive. Create sitemap.xml listing all pages.

### 4. Zero citation-ready content
No passage on either ceefm.eu or ceefm.com scores above 20/100 for citability. AI models need 70+ to reliably cite a passage. There are no FAQ answers, no how-to guides, no data-backed statements, no detailed service descriptions. The "200+ projects" and "9.5 rating" claims have no supporting context.

**Fix:** Write 5-10 passages that directly answer questions like "What does facility management cost in Budapest?", "How to choose a facility management company in Hungary?", "What services does a facility management company provide?"

---

## High Priority Issues

### 5. No llms.txt file
Neither ceefm.eu nor ceefm.com has an llms.txt file. AI systems have no structured guidance about what the business is or where to find key content.

**Fix:** Create llms.txt with company description, services, service areas, key facts, and links to important pages.

### 6. No Hungarian-language content
A Hungarian company (Kft) operating in Budapest for 12+ years has zero Hungarian content online. Hungarian queries to AI models about "letesitmenykezeles Budapest" will never surface CEEFM.

**Fix:** Create all pages in both Hungarian and English. Add hreflang tags.

### 7. Schema missing critical properties
LocalBusiness schema exists but lacks: address, geo coordinates, openingHours, sameAs (zero platform links), foundingDate, aggregateRating, and individual Service schemas. Without sameAs, AI models cannot connect CEEFM to any other mention of the business online.

**Fix:** Add full PostalAddress, GeoCoordinates, sameAs array (LinkedIn, Google Business Profile), and expand serviceType into proper Service schemas.

### 8. Zero third-party brand presence
No Wikipedia page. No Reddit mentions. No YouTube channel. No Trustpilot profile. No industry directory listings. LinkedIn has 92 followers with sparse activity. When AI models search their training data and retrieval indexes for "CEEFM," they find almost nothing.

**Fix:** Create Google Business Profile, build LinkedIn to 500+ followers, get listed on Hungarian business directories (ceginfo.hu, firmadat.hu), start YouTube channel.

### 9. No case studies from 200+ projects
AI models prioritize content with specific, verifiable claims. "200+ projects" with zero documentation is worse than 20 projects with 5 detailed case studies. The number without evidence raises questions rather than building trust.

**Fix:** Document 5-10 case studies with client industry, facility type, challenge, solution, and measurable outcome.

---

## Medium Priority Issues

### 10. Open Graph image returns 422
`og:image` points to `https://ceefm.eu/og-image.jpg` which does not exist (HTTP 422). Social shares and AI previews show broken images.

### 11. No Person schema for team members
No team page, no author bios, no Person structured data. AI models cannot evaluate expertise signals.

### 12. Missing security headers
No HSTS, no proper CSP, no X-Frame-Options, no X-Content-Type-Options. Only `upgrade-insecure-requests` in CSP.

### 13. SPA catch-all breaks standard files
`/favicon.ico`, `/robots.txt`, `/sitemap.xml`, and CSS files all return HTML with 200 status. No proper 404 responses for non-existent paths.

### 14. www vs non-www not redirected
`www.ceefm.eu` serves the same content without redirecting to the canonical `ceefm.eu`. Creates duplicate content signals.

---

## Low Priority Issues

### 15. No speakable schema property
AI voice assistants have no signal about which content to read aloud.

### 16. No BreadcrumbList schema
No breadcrumb navigation structure for search engines.

### 17. No WebSite schema with SearchAction
No site-level schema for sitelinks search box eligibility.

### 18. priceRange uses deprecated format
"$$" dollar-sign notation is deprecated by Google. Should use descriptive text or numeric format.

---

## Category Deep Dives

### AI Citability (8/100)

The primary domain ceefm.eu has one extractable content block: the schema description "Professional facility management and hygiene services for apartment complexes, hotels, and student housing in Central & Eastern Europe." That scores 8/100 for citability.

ceefm.com has slightly more: statistics (200+ projects, 9.5 rating), service one-liners, and three testimonials. The strongest block scores 20/100. None approach the 70+ threshold needed for reliable AI citation.

Zero citation-ready passages exist anywhere. No FAQ answers. No how-to content. No data-backed analysis. No process explanations. No comparison content. The site has nothing an AI model would want to quote as an authoritative answer.

### Brand Authority (12/100)

| Platform | Status |
|---|---|
| Wikipedia | Absent |
| Reddit | Absent |
| YouTube | Absent |
| LinkedIn | 92 followers, sparse activity |
| Trustpilot | Absent |
| Google Business Profile | Unconfirmed |
| Industry directories | Absent |
| News/press mentions | Absent |

The LinkedIn page at linkedin.com/company/cee-facility-management is the only confirmed third-party presence. It lists 11-50 employees and has some recent posts including a Limehome partnership announcement. This is the single strongest brand authority signal and it scores 5/10.

AI models build entity recognition from cross-platform presence. With near-zero presence, CEEFM is not recognized as an entity by any AI system.

### Content E-E-A-T (14/100)

| Dimension | Score | Evidence |
|---|---|---|
| Experience | 3/25 | Zero case studies. Zero project documentation. "200+ projects" claimed but none shown. |
| Expertise | 4/25 | No author bios. No team credentials. No certifications displayed. Thin service descriptions. |
| Authoritativeness | 5/25 | Three testimonials from named professionals. 14 service categories (breadth signal). No external validation. |
| Trustworthiness | 6/25 | Testimonials present. 9.5 rating claimed without source. No editorial standards. No Hungarian content for a Hungarian company. |

The "200+ projects" claim is a liability without documentation. It raises the question: if 200 projects exist, why can none be shown? The 9.5 rating has no attribution to any review platform.

Content word count on ceefm.eu is estimated under 300 words. No blog. No resources. No FAQ. No team page. Content freshness is unknown because no dates appear anywhere.

### Technical GEO (33/100)

| Component | Score |
|---|---|
| Server-Side Rendering | 5/100 |
| Meta Tags & Indexability | 75/100 |
| Crawlability | 10/100 |
| Security Headers | 25/100 |
| Core Web Vitals Risk | 40/100 |
| Mobile Optimization | 50/100 |
| URL Structure | 70/100 |

The meta tags are the bright spot. Title, description, canonical, Open Graph, and Twitter Card tags are all present and well-formed in the HTML head. This is the only content AI crawlers can read.

Everything else is poor. The React SPA delivers empty HTML. The catch-all routing breaks robots.txt, sitemap.xml, and favicon.ico. No preconnect hints. Font loading chain is deeply nested (HTML > JS > CSS > Font). 233KB JS bundle must fully execute before any content appears.

### Schema & Structured Data (15/100)

One schema block found: LocalBusiness in JSON-LD format. Valid syntax. But missing critical properties:

- **address** (required for rich results)
- **geo** (required for local search)
- **sameAs** (critical for AI entity linking, zero links)
- **openingHoursSpecification**
- **foundingDate**
- **aggregateRating**
- **Service schemas** (serviceType is a flat text array, not structured)
- **Person schemas** (no team members)
- **speakable** property
- **BreadcrumbList**
- **WebSite**
- **FAQPage**

The JSON-LD format and server-rendered placement are correct. The schema just needs significant expansion.

### Platform Optimization (24/100)

| Platform | Score | Key Issue |
|---|---|---|
| Google AI Overviews | 28/100 | Only 3 FAQ items. No distinct service URLs. SPA limits extraction. |
| ChatGPT Web Search | 18/100 | No entity recognition. No sameAs. SPA invisible to ChatGPT crawler. |
| Perplexity AI | 15/100 | Zero community validation. Zero original content. Cannot render JS. |
| Google Gemini | 22/100 | No Google ecosystem presence. No Knowledge Graph entry. No YouTube. |
| Bing Copilot | 19/100 | No Bing Webmaster Tools. No IndexNow. No LinkedIn linked. SPA invisible. |

Cross-platform root causes: (1) SPA architecture blocks 4 of 5 platforms, (2) no multi-page structure means nothing to index, (3) no external presence means no entity recognition.

---

## Quick Wins (Implement This Week)

1. **Create robots.txt** allowing all AI crawlers with Sitemap directive. Deploy as a static file that bypasses SPA routing.
2. **Create sitemap.xml** listing the homepage (and any future pages). Reference in robots.txt.
3. **Create llms.txt** with company name, description, services, service areas, and contact info.
4. **Expand LocalBusiness schema** with address, geo coordinates, sameAs (LinkedIn URL), openingHours, and foundingDate.
5. **Fix og-image.jpg** by uploading an actual 1200x630px image to the public directory.

## 30-Day Action Plan

### Week 1: Technical Foundation
- [ ] Create robots.txt, sitemap.xml, llms.txt
- [ ] Fix og-image, favicon, www redirect
- [ ] Expand LocalBusiness schema with all missing properties
- [ ] Add FAQPage schema for existing FAQ content
- [ ] Register with Bing Webmaster Tools, implement IndexNow

### Week 2: Architecture and Rendering
- [ ] Implement SSR/SSG or pre-rendering for the React SPA
- [ ] Create multi-page architecture: /services, /about, /contact, /faq
- [ ] Create individual service pages for top 5 services
- [ ] Add hreflang tags for English/Hungarian content
- [ ] Add security headers (HSTS, CSP, X-Frame-Options)

### Week 3: Content Creation
- [ ] Write 5 case studies from existing projects
- [ ] Create About page with team, credentials, company history
- [ ] Write detailed service descriptions (500+ words each)
- [ ] Build FAQ page with 10-15 questions and answers
- [ ] Create all content in Hungarian and English

### Week 4: External Presence
- [ ] Create/verify Google Business Profile with full information
- [ ] Optimize LinkedIn company page, begin weekly posting
- [ ] Get listed on 3-5 Hungarian business directories
- [ ] Start YouTube channel with 2-3 facility management videos
- [ ] Solicit Google reviews from 5-10 existing clients

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| https://ceefm.eu/ | CEEFM Kft - Professional Facility Management | 18 issues (4 critical, 5 high, 5 medium, 4 low) |

*Only 1 page exists on the domain. The SPA architecture means all content lives on a single URL.*

---

*Generated by GEO Audit Suite | /geo audit*
*Prepared by BridgeWorks for CEEFM Kft | March 2026*
