# GEO Audit Report: University of Pattern Drafting

**Audit Date:** 11 June 2026
**URL:** https://www.universityofpatterndrafting.com/
**Business Type:** Online Education Platform — garment construction and pattern drafting school
**Founder:** Umo Anwana (15+ years fashion industry experience)
**Pages Analyzed:** 11
**Audited by:** BridgeWorks | office@bridgeworks.agency · bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 20/100 — Critical**

University of Pattern Drafting has real expertise at its core — a practitioner founder with 15+ years of industry experience, nine structured courses, and an active social presence. But none of that expertise reaches AI systems. The site is invisible to every major AI search engine (ChatGPT, Perplexity, Gemini, Bing Copilot, Google AI Overviews). There is no structured data, no citable content, no entity declaration, and no AI-readiness infrastructure of any kind. The domain also returned connection failures during the audit, which means crawlers are likely unable to reach the site at all. The gap between the quality of the knowledge being taught and the site's ability to communicate that knowledge to AI systems is large — but almost every issue has a direct, actionable fix.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 14/100 | 25% | 3.50 |
| Brand Authority | 12/100 | 20% | 2.40 |
| Content E-E-A-T | 34/100 | 20% | 6.80 |
| Technical GEO | 34/100 | 15% | 5.10 |
| Schema & Structured Data | 4/100 | 10% | 0.40 |
| Platform Optimization | 14/100 | 10% | 1.40 |
| **Overall GEO Score** | | | **20/100** |

---

## Critical Issues — Fix Immediately

### 1. Domain is unreachable by crawlers

The site returned ECONNREFUSED during this audit. Direct HTTP connections failed on both www and non-www versions. This means AI crawlers (GPTBot, ClaudeBot, PerplexityBot) and search bots cannot fetch any content. A site that does not respond cannot be indexed, cited, or featured — by any platform.

**Fix:** Diagnose whether this is a firewall rule, a server outage, or an IP-range block targeting cloud-hosted user agents. If a firewall is blocking non-browser requests, whitelist the major crawler user agents at the server or hosting level.

**Affects:** All six GEO categories.

---

### 2. No schema markup of any kind

The site is built on custom PHP with no CMS. No structured data has been implemented. Nine courses have no Course schema. The organization has no EducationalOrganization schema. The founder has no Person schema. There are no BreadcrumbList, FAQPage, Review, or sameAs declarations anywhere.

Without schema, AI models cannot build an entity graph for this brand. Google cannot show course rich results. No platform can verify who this school is or what it teaches.

**Fix:** Add four JSON-LD blocks as an immediate priority (see Schema section for templates):
1. EducationalOrganization on every page
2. Course on every course enrollment page
3. Person on the /about/ page
4. sameAs links connecting YouTube, Facebook, Instagram

**Affects:** Schema (primary), AI Citability, Platform Optimization, Brand Authority.

---

### 3. No llms.txt file

There is no llms.txt at the domain root. This file is the direct signal AI systems use to understand what a site is and which content they are permitted to index. Its absence does not block crawlers — but it forfeits a meaningful early-adoption advantage.

**Fix:** Create `/llms.txt` with the following content:

```
# University of Pattern Drafting

> Online school for professional pattern drafting and garment construction, founded by Umo Anwana.

## Courses

- Mastering Pattern Drafting for Beginners: https://www.universityofpatterndrafting.com/course/enrol/?cn=mastering-pattern-drafting-for-beginners
- Advanced Corsetry Class: https://www.universityofpatterndrafting.com/course/enrol/?cn=advanced-corsetry-class
- Advanced Pattern Drafting, Manipulation and Grading Masterclass: https://www.universityofpatterndrafting.com/course/enrol/?cn=advanced-pattern-drafting,-manipulation-and-grading-masterclass
- Evening Dress and Draping Masterclass: https://www.universityofpatterndrafting.com/course/enrol/?cn=evening-dress-and-draping-masterclass
- Waist Snatching Masterclass: https://www.universityofpatterndrafting.com/course/enrol/?cn=waist-snatching-masterclass
- Pricing Masterclass: https://www.universityofpatterndrafting.com/course/enrol/?cn=pricing-masterclass

## About

- About Umo Anwana: https://www.universityofpatterndrafting.com/about/
```

**Affects:** AI Citability, Technical GEO.

---

### 4. No informational or citable content

The entire site is a product catalog. Every page is a course enrollment page or a contact form. AI systems cite content that answers questions — not pages that sell products. Without blog posts, guides, tutorials, or free resources, there is no content for ChatGPT, Perplexity, or Google AI Overviews to surface in response to queries like "how do I draft a bodice block" or "best pattern drafting courses online."

**Fix:** Publish a minimum of five long-form educational articles. Start with:
- "How to Take Body Measurements for Pattern Drafting" (beginner, high search volume)
- "What Is Pattern Grading and Why Does It Matter?" (intermediate, FAQ target)
- "The Difference Between Flat Pattern Drafting and Draping" (comparative, citable)
- "Standard Body Measurement Chart for Pattern Makers" (reference, AI-citation magnet)
- "Beginner's Guide to Corset Construction" (taps into course content, builds authority)

Each article should carry Umo Anwana's byline with credentials, a publication date, and a last-updated date.

**Affects:** AI Citability, Content E-E-A-T, Platform Optimization, Brand Authority.

---

## High Priority Issues

### 5. No Wikipedia or Wikidata entity

There is no Wikipedia article for University of Pattern Drafting or for Umo Anwana. Wikipedia presence is the single strongest signal for entity recognition by LLMs. Without it, ChatGPT and Google Gemini cannot reliably identify this brand as a distinct entity.

**Fix:** Build a verifiable external record first. Get at least two third-party press citations (a blog interview, an industry feature, a course review on an external site). Then submit a Wikipedia stub article for Umo Anwana citing those sources. This takes 4-8 weeks but produces lasting impact across every AI platform.

---

### 6. No Reddit or forum presence

No mentions found on Reddit, Quora, or any fashion/sewing forum. Reddit is a primary source for Perplexity AI citations. Subreddits like r/sewing, r/patternmaking, and r/fashiondesign have active communities asking exactly the questions this school can answer.

**Fix:** Have Umo Anwana answer 2-3 questions per week in r/sewing and r/patternmaking using a personal Reddit account. Link to the free content on the site where relevant. Do not promote courses directly — participate genuinely. Over 60-90 days, this builds Reddit mention signals that Perplexity will begin citing.

---

### 7. No XML sitemap confirmed

No sitemap.xml was found at the standard location. Without a sitemap, search engines and AI crawlers rely on link discovery alone, which means suspended or unlinked course pages are invisible.

**Fix:** Generate a sitemap.xml covering all active (non-suspended) pages. Submit to Google Search Console and Bing Webmaster Tools. Reference it in robots.txt.

---

### 8. www vs. non-www canonical inconsistency

Both `www.universityofpatterndrafting.com` and `universityofpatterndrafting.com` appear in search results. No confirmed canonical tag or 301 redirect is enforcing a single preferred version. This creates duplicate content across all indexed pages.

**Fix:** Choose one version (www preferred). Add a `<link rel="canonical">` tag to every page pointing to the www version. Configure a server-level 301 redirect from the non-www version.

---

### 9. No trust infrastructure

The site has no public email address, no privacy policy, no terms of service, and no enrollment/refund policy. All contact is routed through WhatsApp. This is a significant trust signal gap for both Google's Quality Rater Guidelines and AI system trustworthiness scoring.

**Fix:** Add a public email address (office@ or hello@). Create a Privacy Policy page. Add a Refund/Enrollment Policy. Link all three from the footer of every page.

---

### 10. No LinkedIn Company Page

No LinkedIn presence was found. LinkedIn is Bing Copilot's primary source for professional entity validation. Its absence contributes to the brand being invisible to AI tools targeting professional/business audiences.

**Fix:** Create a LinkedIn Company Page for University of Pattern Drafting. Add the company URL and LinkedIn handle to the site footer and to the Organization schema's sameAs array.

---

## Medium Priority Issues

- Facebook page has only 536 likes — social proof is minimal. Run a structured growth campaign alongside content publishing.
- Some courses appear suspended — these pages likely return soft 404s (200 status with "unavailable" message), wasting crawl budget. Return proper 301 redirects to the course catalog or 410 Gone responses.
- TikTok educational content exists but is not ported to the website. Transcribing and embedding these videos creates free indexable content at zero production cost.
- No Open Graph or Twitter Card meta tags — AI tools generate their own previews for shared links, reducing brand control over how the site appears in citations.
- Content freshness is unknown. No visible publication or last-updated dates on any page. Add dates to all content immediately.

---

## Low Priority Issues

- PHP file extension URLs (`/contact.php`) expose server technology and provide no keyword signal. Rewrite to clean URLs using `.htaccess` when time permits.
- Security headers (HSTS, X-Frame-Options, X-Content-Type-Options) are likely absent. Configure at server or `.htaccess` level.
- No CDN detected — page speed for international visitors is likely slow. Consider Cloudflare free tier.
- BreadcrumbList schema missing on all course pages.

---

## Category Deep Dives

### AI Citability — 14/100

Content on the site is not structured to be cited by AI systems. Every indexed page is an enrollment page. Enrollment pages do not answer questions; they sell courses. AI models extract factual, answer-structured passages — short paragraphs that directly address a question, followed by supporting detail. None of that exists here.

The founder bio on the About page is the only semi-citable element. It names a real expert with a specific professional background. But it exists only on one page, with no byline carrying it into course pages, and no structured data surfacing it to AI systems.

The domain also returned ECONNREFUSED during the audit. If this is not an intermittent outage but a persistent configuration issue, AI crawlers are receiving zero content. A closed door is functionally identical to a blocked robots.txt.

**What good looks like for this site:** A "Pattern Drafting Glossary" page with 30+ defined terms, structured with definition-list HTML and Article schema, authored by Umo Anwana, with a publication date. That single page would be cited by AI systems within 60-90 days of indexing.

---

### Brand Authority — 12/100

Third-party presence is minimal. YouTube channel confirmed. Facebook at 536 likes. TikTok has videos. Instagram exists. No mentions found on Wikipedia, Reddit, Quora, or any editorial source. No press coverage. No industry organization affiliations.

AI models assess brand authority by triangulating mentions across platforms they have been trained on. For this school, that training data is essentially zero. The brand exists in its own channels only.

The Nigerian fashion market context is also worth noting. AI models have less training data on Nigerian fashion education than on US or European equivalents. This means the bar for getting cited is lower — but the existing signals need to exist first.

---

### Content E-E-A-T — 34/100

Umo Anwana's 15+ years of fashion industry experience is a genuine credential. Pattern maker, production manager, quality control officer — these are specific, verifiable roles. That experience earns points in the Experience and Expertise dimensions.

What pulls the score down is that none of this expertise is present in a form AI systems can read and assess. The About page has a summary. Individual course pages do not carry an author byline. No course pages cite the founder's credentials as the authority behind the curriculum. There are no outcome statistics ("X students have enrolled," "Y% launched a business after completing the course"). No student testimonials with specific, named results. No original research.

The TikTok presence is a positive signal — it shows on-camera demonstration of real technique, which is the definition of the E (Experience) in E-E-A-T. But that content needs to be on the website, not only on TikTok.

---

### Technical GEO — 34/100

PHP-based server-side rendering is the best-case scenario for AI crawler content access. The content is in the HTML on page load — no JavaScript execution required. This is a genuine advantage over React or Vue SPA frameworks.

But the site loses points on nearly every other technical dimension. ECONNREFUSED during the audit is the most severe issue. No sitemap, no confirmed robots.txt, no Open Graph tags, no canonical enforcement, no security headers, and no CDN. The URL structure exposes PHP extensions and uses query strings for course routing (`/course/enrol/?cn=`) rather than clean keyword slugs.

Seven pages are confirmed indexed by Google, which means the site is not globally blocked. But full crawl coverage is unlikely without a sitemap, and AI platform-specific crawlers may not be receiving the same access as Googlebot.

---

### Schema & Structured Data — 4/100

No schema exists. The four points are awarded as a baseline for the site being live with indexable content — nothing more.

The opportunity here is significant. Nine course pages, a founder with documented expertise, and a specific educational niche — all of this maps directly to high-impact schema types. Course schema with Google's course carousels, EducationalOrganization with sameAs linking, Person schema with knowsAbout — these are achievable in under a week of implementation work on a PHP site.

The custom PHP architecture is not a barrier. All schema should be implemented as inline JSON-LD in the `<head>` of the relevant page templates. One shared header template change covers the EducationalOrganization block across all pages.

**See the recommended templates in the Critical Issues section above. All six schema blocks are ready for implementation.**

---

### Platform Optimization — 14/100

The site is not featured on any AI platform. No Google AI Overview, no Perplexity citation, no ChatGPT entity recognition, no Bing Copilot results. All five major AI search platforms returned no evidence of awareness of this brand.

The YouTube channel is the one genuine asset. YouTube is indexed by Google and is one of the few existing signals that connects this brand to a Google-owned platform. If the YouTube channel content is high-quality and the channel description is keyword-rich, this alone could create some Gemini awareness. But the channel optimization level is unknown.

The school is not listed in any educational directory (Class Central, CourseReport, Alison). These directories are frequently cited by AI systems when users ask about online courses. A free listing on Class Central alone could generate AI citations within 90 days.

---

## Quick Wins — Implement This Week

1. **Resolve ECONNREFUSED.** Contact the hosting provider or check firewall rules. If cloud-hosted crawlers are being blocked, whitelist the major AI crawler user agents. Until the site responds to HTTP requests, nothing else matters.

2. **Create /llms.txt.** One text file at the domain root. Fifteen minutes of work. Direct signal to all AI crawlers. Use the template in the Critical Issues section above.

3. **Add EducationalOrganization JSON-LD to the site header.** One PHP file edit covers every page. Paste the schema into the shared header include. This is the foundation that every other schema improvement builds on.

4. **Submit to Class Central.** Free course directory submission at classcentral.com. One of the most-cited educational directories by AI systems. Directly generates third-party brand mentions.

5. **Create a LinkedIn Company Page.** Free to create, 30 minutes of setup. Add the URL to the site footer and to the Organization schema sameAs array. Immediately signals professional entity to Bing Copilot and ChatGPT.

---

## 30-Day Action Plan

### Week 1 — Fix the Foundation

- [ ] Diagnose and resolve ECONNREFUSED server/connectivity issue
- [ ] Create robots.txt with explicit allow directives for GPTBot, ClaudeBot, OAI-SearchBot, PerplexityBot, Bingbot
- [ ] Create /llms.txt using the template above
- [ ] Choose www vs. non-www canonical, implement 301 redirect and canonical tags
- [ ] Add EducationalOrganization JSON-LD to shared PHP header template
- [ ] Add Person JSON-LD to /about/ page
- [ ] Generate and submit sitemap.xml to Google Search Console and Bing Webmaster Tools

### Week 2 — Course Schema and Trust

- [ ] Add Course JSON-LD to all 9 active course enrollment pages
- [ ] Handle suspended courses with proper 301 redirects or 410 responses
- [ ] Add BreadcrumbList schema to all course pages
- [ ] Add public email address, Privacy Policy, and Refund Policy to site footer
- [ ] Create LinkedIn Company Page and link it in footer and Organization sameAs
- [ ] Add Open Graph meta tags to homepage and course pages

### Week 3 — Content That AI Can Cite

- [ ] Publish first two free educational articles with Umo Anwana byline and publication date
- [ ] Transcribe and embed 3 TikTok educational videos on the website with supporting text
- [ ] Add student testimonials page with 5-8 specific, named outcome stories
- [ ] Create Google Business Profile (Online Education category)
- [ ] Submit courses to Class Central and CourseReport

### Week 4 — Brand Authority Building

- [ ] Begin Reddit presence in r/sewing and r/patternmaking (2-3 genuine answers per week)
- [ ] Publish remaining three free educational articles
- [ ] Identify two-three fashion or sewing publications for press outreach (interviews, guest posts)
- [ ] Optimize YouTube channel description with keyword-rich bio and full video descriptions
- [ ] Begin documenting verifiable career facts for a future Wikipedia submission

---

## Appendix: Pages Analyzed

| URL | Title | Issues |
|---|---|---|
| https://www.universityofpatterndrafting.com/ | Homepage | ECONNREFUSED, no schema, no OG tags, no canonical |
| https://www.universityofpatterndrafting.com/about/ | About Us | No Person schema, no byline schema, no press citations |
| https://universityofpatterndrafting.com/contact.php | Contact | .php extension, WhatsApp only, no email, non-www |
| https://universityofpatterndrafting.com/course/enrol/?cn=mastering-pattern-drafting-for-beginners | Mastering Pattern Drafting for Beginners | No Course schema, no canonical, query string URL |
| https://universityofpatterndrafting.com/course/enrol/?cn=advanced-corsetry-class | Advanced Corsetry Class | No Course schema, no canonical, query string URL |
| https://universityofpatterndrafting.com/course/enrol/?cn=waist-snatching-masterclass | Waist Snatching Masterclass | No Course schema, no canonical, query string URL |
| https://www.universityofpatterndrafting.com/course/enrol/?cn=intensive-upgrade-class-for-beginners-and-intermediates | Intensive Upgrade Class | No Course schema, URL too long, query string |
| https://universityofpatterndrafting.com/course/enrol/?cn=evening-dress-and-draping-masterclass | Evening Dress and Draping Masterclass | No Course schema, no canonical, query string URL |
| https://universityofpatterndrafting.com/course/enrol/?cn=hip-and-butt-padding-masterclass | Hip and Butt Padding Masterclass | No Course schema, no canonical, query string URL |
| https://universityofpatterndrafting.com/course/enrol/?cn=advanced-pattern-drafting,-manipulation-and-grading-masterclass | Advanced Pattern Drafting Masterclass | No Course schema, comma in URL, query string |
| https://universityofpatterndrafting.com/course/enrol/?cn=pricing-masterclass | Pricing Masterclass | No Course schema, no canonical, query string URL |

---

*BridgeWorks GEO Audit · office@bridgeworks.agency · bridgeworks.agency*
*Audit methodology: parallel specialist analysis across AI citability, brand authority, content quality, technical infrastructure, schema markup, and platform optimization.*
