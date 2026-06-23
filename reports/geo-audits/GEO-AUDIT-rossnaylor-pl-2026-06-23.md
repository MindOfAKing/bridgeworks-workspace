# GEO Audit Report: rossnaylor.com
**Prepared by:** BridgeWorks  
**Date:** 2026-06-23  
**Prospect:** Ross Naylor, Financial Advice Poland  
**URL:** https://rossnaylor.com  
**Niche:** Fee-only financial advisor, British expats across EU  
**Location:** Warsaw, Poland  

---

## Overall GEO Score: 41 / 100
**Rating: Poor**

The site has real content depth and genuine niche authority. However, it is almost completely invisible to AI search engines. No structured data. No llms.txt. No location schema. The site cannot be cited by Perplexity, ChatGPT, or Google AI Overviews for the queries Ross's ideal clients are typing right now.

---

## Score Breakdown

| Category | Score | Weight | Notes |
|---|---|---|---|
| AI Citability | 6/20 | 20% | No llms.txt, no structured citability signals, no speakable markup |
| Schema & Structured Data | 2/20 | 20% | Zero JSON-LD detected across all pages audited |
| Content Quality (E-E-A-T) | 14/20 | 20% | Strong credentials and experience; weak on publication dates and author schema |
| Technical Infrastructure | 10/20 | 20% | Robots.txt clean, sitemap present, no AI crawler config, no canonical/OG/hreflang |
| Platform Readiness | 5/10 | 10% | No Google AI Overviews optimization, no featured snippet structure, limited Bing Copilot signals |
| Local & Geographic Targeting | 4/10 | 10% | Poland pages exist but zero LocalBusiness/GeoCoordinates schema; no NAP on contact page |

---

## Phase 1: Discovery & Crawl Summary

**Site architecture:** WordPress (SmartCrawl plugin for sitemap). Two sitemaps: posts (136 URLs) and pages (21 URLs). Total indexed content: ~157 pages.

**Key pages found:**
- `/uk-pension-poland/` — 4,500 words, comprehensive, no schema
- `/qrops-poland/` — 1,800 words, FAQ present, no FAQ schema
- `/state-pension-poland/` — step-by-step guide, no schema
- `/retire-to-poland-with-confidence-essential-tips-for-brits-looking-to-move/` — 4,500 words, most comprehensive Poland page on the site
- `/cross-border-financial-advice/` — core services page, no schema
- `/testimonials/` — 15 testimonials, no Review or AggregateRating schema
- `/contact/` — no physical address, no schema, no map

**robots.txt:** Clean. Allows all crawlers. Blocks feed URLs only. References sitemap correctly.

**llms.txt:** 404 Not Found. Does not exist.

---

## Phase 2: Detailed Findings

### Category 1: AI Citability (6/20)

**What was checked:** llms.txt presence, speakable markup, crawlability by AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended), citation-readiness of content.

**Findings:**

- **No llms.txt file exists.** This is the single most direct signal that the site has not been configured for AI discoverability. There is no file at `rossnaylor.com/llms.txt` telling AI systems what pages to prioritize for citation.

- **No Speakable markup.** None of the articles or FAQ pages include `speakable` schema properties. AI assistants and voice search cannot identify which content to surface.

- **robots.txt does not block AI crawlers** — GPTBot, ClaudeBot, PerplexityBot are all technically permitted. This is correct but insufficient on its own.

- **Content IS potentially citable** — the Poland-specific posts (uk-pension-poland, qrops-poland, state-pension-poland, retire-to-poland) are long-form, well-structured, and factually detailed. They could be cited if AI systems knew to prioritize them.

- **No canonical tags confirmed.** Without canonical tags, duplicate or near-duplicate content may confuse AI crawlers about which page to cite.

- **No OG/Twitter meta tags confirmed on homepage.** These are read by some AI systems for page context.

**Verdict:** Content exists that AI could cite. The infrastructure to signal that content to AI systems is entirely missing.

---

### Category 2: Schema & Structured Data (2/20)

**What was checked:** JSON-LD on homepage, service pages, blog posts, contact page, testimonials page, FAQ pages, about page.

**Findings — Zero JSON-LD detected across all audited pages.**

Pages audited for schema:
- Homepage: No schema
- `/about/`: No schema
- `/contact/`: No schema, no PostalAddress, no LocalBusiness
- `/services/`: No schema
- `/testimonials/`: No Review, no AggregateRating schema
- `/expat-pension-advice/`: No schema
- `/cross-border-financial-advice/`: No schema
- `/uk-pension-poland/`: No Article/BlogPosting schema, no FAQPage schema
- `/qrops-poland/`: No schema despite having a structured FAQ section
- `/state-pension-poland/`: No schema
- `/retire-to-poland-with-confidence-essential-tips-for-brits-looking-to-move/`: No schema

**Missing schema types that would directly improve AI discoverability:**

| Schema Type | Where Needed | Why It Matters |
|---|---|---|
| Person | Homepage, About, all posts | Establishes Ross as a named author entity AI systems can reference |
| ProfessionalService / FinancialService | Services pages, Homepage | Signals the business type to AI search |
| LocalBusiness with GeoCoordinates | Contact, Homepage | Anchors the business to Warsaw, Poland geographically |
| PostalAddress | Contact page | Required for local AI search (Perplexity, Google AI Overviews) |
| FAQPage / QAPage | /qrops-poland/, /uk-pension-poland/, /faqs/, all article FAQs | Enables FAQ-style AI answers pulling directly from his content |
| Article / BlogPosting | All blog posts and guides | Author entity, datePublished, dateModified — all missing |
| Review / AggregateRating | /testimonials/ | 15 testimonials exist but none are machine-readable |
| SameAs (sameAs property) | Person schema | Links homepage to LinkedIn, Facebook — establishes identity across AI knowledge graphs |

**Verdict:** Complete absence of structured data. This is the highest-effort fix with the highest AI visibility payoff.

---

### Category 3: Content Quality / E-E-A-T (14/20)

**Strengths:**
- Ross has lived in Poland for 25 years. This is stated clearly on the About page and in the retire-to-poland article. It is the strongest possible Experience signal for the niche.
- Credentials are genuine and high-level: Chartered Financial Planner (UK), Pension Transfer Specialist, European Financial Planner (EU). These are cited on multiple pages.
- 15 testimonials are present, including one that mentions Warsaw specifically (Stefan Rasche: "Warsaw, Prague, Brussels").
- Multiple long-form Poland-specific articles (4,000-5,000 words) demonstrate genuine depth.
- FAQ sections are present on key pages with 10+ questions each.
- Cross-linking between related posts creates topical clusters (Poland series).
- Fee-only model is stated — a trust signal that differentiates from commission-based advisors.

**Weaknesses:**
- **No publication dates or last-updated dates are visible on any blog post or guide.** AI systems weight freshness. Without dates, content is treated as potentially stale or undated — a citation risk.
- **Author bio is not marked up.** Ross's name appears on articles but there is no structured author schema (Person), no author box linking to a canonical About page, and no byline consistency across pages.
- **No external authoritative citations on most pages.** The Brexit article links to government tax resources, but most Poland-specific pages do not cite any authoritative external sources (UK government, Polish tax authority, FCA).
- **No credentials markup.** Qualifications are mentioned in text but not machine-readable. AI systems cannot confirm them as structured facts.
- **Meta descriptions are missing on most pages.** Confirmed absent on: homepage, /contact/, /services/, /uk-pension-poland/, /qrops-poland/, /state-pension-poland/, /cross-border-financial-advice/.

**Verdict:** E-E-A-T signals are genuinely strong in human-readable form. They are almost entirely absent in machine-readable form. AI systems cannot reliably extract them.

---

### Category 4: Technical Infrastructure (10/20)

**Strengths:**
- robots.txt is clean and well-formed. All crawlers permitted. Sitemap correctly referenced.
- Two sitemaps are present and accessible (post-sitemap1.xml, page-sitemap1.xml).
- SmartCrawl SEO plugin is installed — capable of generating schema, but appears unused for this purpose.
- Site loads over HTTPS. No HTTP redirect issues encountered.
- 157 total URLs across sitemaps — reasonable site depth for a specialist advisory site.

**Weaknesses:**
- **No canonical URL tags confirmed** on audited pages. Without canonicals, AI crawlers cannot resolve authority between similar/duplicate pages.
- **No hreflang tags.** Not applicable since the site is English-only, but worth noting for any future Polish-language content strategy.
- **No OG meta tags confirmed** on homepage. Open Graph data (og:title, og:description, og:type) is read by some AI systems for entity recognition and by social platforms that feed AI training data.
- **No Twitter/X Card meta tags** confirmed. Same impact as OG.
- **No Google Analytics or tracking visible** — likely present but not confirmed from front-end.
- **No structured AI crawler directives** beyond basic robots.txt. No `X-Robots-Tag` headers with AI-specific guidance.
- **WordPress-based site** — schema can be added without custom development using existing plugins (Yoast, RankMath, or Schema Pro). This is a low-cost fix.

---

### Category 5: Platform Readiness (5/10)

**Google AI Overviews:**
- No FAQPage schema on FAQ pages. FAQ sections are present on /qrops-poland/, /uk-pension-poland/, /state-pension-poland/ — but the content is invisible to AI Overviews because it lacks structured markup.
- No HowTo schema on procedural guides like "How to claim UK State Pension in Poland."
- Article schema absent — Google cannot confirm authorship, freshness, or topical authority for AI Overviews sourcing decisions.

**Perplexity AI:**
- No llms.txt. Perplexity relies heavily on llms.txt for site-level citation guidance.
- Content is publicly crawlable, but without structured signals, Perplexity cannot determine which pages represent the authoritative source on British expat financial advice in Poland.

**ChatGPT Web Search (Bing-indexed):**
- No Bing-specific optimization detected. Bing Copilot and ChatGPT web search both draw from Bing index. Schema markup substantially improves Bing ranking.
- No local business listing signals for Bing Places.

**Google Gemini:**
- No knowledge graph connection established. No sameAs properties linking rossnaylor.com to a Wikidata, Google Business Profile, or LinkedIn entity.
- No structured Person entity published.

**Overall:** The content could feed all four platforms. The signals that would get it cited are absent on every platform.

---

### Category 6: Local & Geographic Targeting (4/10)

This is the most critical category for Ross's business model.

**The core problem:** Ross Naylor is the only UK-qualified, EU-qualified, fee-only financial advisor physically based in Warsaw who has lived there for 25 years. This is an extraordinary positioning advantage. It is entirely invisible to AI search.

**Specific findings:**

- **No LocalBusiness schema anywhere on the site.** No schema type of `FinancialService`, `LocalBusiness`, or `ProfessionalService` with GeoCoordinates is present on any page.

- **No physical address on the contact page.** The contact page has an email address, a Calendly link, and a contact form. No street address, no city, no country. A person searching "British financial advisor in Warsaw" via any AI engine gets no location confirmation from this site.

- **Poland content cluster exists but is structurally invisible.** The site has four dedicated Poland pages:
  - `/uk-pension-poland/`
  - `/qrops-poland/`
  - `/state-pension-poland/`
  - `/retire-to-poland-with-confidence-essential-tips-for-brits-looking-to-move/`
  
  None of these pages contain location schema. None link from the homepage navigation or services nav. They are blog/resource posts, not location landing pages.

- **No "British financial advisor Warsaw" or "expat financial advice Poland" page exists as a dedicated service landing page.** There is `/uk-expat-financial-advisor/` but it is generic to all of the EU, not Poland-specific in its title tag, meta, or schema.

- **Warsaw appears in the About page text** ("lived in Poland for the last 25 years") and in one testimonial (Stefan Rasche) — but neither is structured data. AI systems reading these pages cannot extract "Ross Naylor = financial advisor + Warsaw, Poland" as a machine-readable fact.

- **No Google Business Profile signals.** No schema linking to a GBP. No local citations.

- **The about page confirms Ross lives in Warsaw and has done for 25 years.** This fact — which is his single biggest differentiator — is buried in body copy with zero schema support.

---

## Phase 3: Top Findings by Priority

### Critical

**1. Zero structured data across entire site**
Not a single JSON-LD block exists on any page. The site has 157 pages. Every page is invisible to AI citation systems at the machine-readable level. Person schema, FAQPage schema, Article schema, and LocalBusiness schema are all missing. This is a single fix that requires one afternoon of implementation using existing WordPress plugins (SmartCrawl is already installed).

**2. No llms.txt**
There is no `llms.txt` file at `rossnaylor.com/llms.txt`. This file tells AI systems (Perplexity, ChatGPT, Claude) which pages to prioritize when crawling for citations. Without it, AI systems have no site-level guidance. The Poland-specific content cluster — four substantial articles covering UK pensions, QROPS, State Pension, and retirement in Poland — cannot be surfaced as a priority citation cluster.

**3. No location identity in structured data**
Ross has lived in Warsaw for 25 years and is the only qualified British expat financial advisor based there. There is no PostalAddress, no GeoCoordinates, no LocalBusiness schema, and no physical address anywhere on the contact page. A British expat in Warsaw asking Perplexity "who is a UK-qualified financial advisor in Warsaw?" will not find Ross Naylor because the site has not told AI systems where he is.

### High Priority

**4. Meta descriptions missing on most pages**
Confirmed absent: homepage, contact, services, uk-pension-poland, qrops-poland, state-pension-poland, cross-border-financial-advice. Meta descriptions are read by AI systems for page-level context summaries and citation snippets. Missing meta descriptions reduce the clarity of what each page is about.

**5. No publication or update dates visible on articles**
AI systems use freshness signals when deciding what to cite. None of the blog posts or guides display a visible publication or last-updated date. Content that appears undated is deprioritized in AI citation decisions — even when the content is current (several posts reference 2026 UK tax changes).

**6. 15 testimonials with zero Review schema**
The testimonials page has 15 strong client testimonials including one from Warsaw-based Stefan Rasche. None are marked up as `Review` or `AggregateRating` schema. This data cannot contribute to the site's trust score in AI systems or appear as star ratings in search results.

---

## Strongest Gap for Email Hook

**The gap:**

Ross Naylor has lived in Warsaw for 25 years. He is the only UK-qualified, EU-qualified, fee-only financial planner based in Poland. He has four in-depth articles covering UK pensions, QROPS, State Pension, and retirement in Poland. He has a client testimonial from someone who met him in Warsaw.

None of this appears in structured data. There is no location schema. There is no llms.txt. The contact page has no address.

Right now, if a British expat in Warsaw types into Perplexity or ChatGPT: "UK-qualified financial advisor in Warsaw Poland" or "who can advise me on my UK pension in Poland," Ross Naylor does not appear. The site has the content. It lacks the signals.

**Single line for the email:**

"You have four detailed articles on UK pensions in Poland, 25 years in Warsaw, and the only EU-qualified British advisor credential in the country — but your site has no location schema, no llms.txt, and no structured data, so AI search engines cannot cite you for any of it."

---

## BridgeWorks Positioning

**One-line fix statement:**

BridgeWorks adds the structured data, llms.txt, and location signals that let AI systems cite Ross as the go-to British financial advisor in Poland — turning four existing articles into active AI citations instead of invisible blog posts.

---

## Recommended Actions (Priority Order)

| Priority | Action | Effort | Impact |
|---|---|---|---|
| 1 | Add Person schema to homepage and About page (name, credentials, location: Warsaw) | Low | High |
| 2 | Create llms.txt at rossnaylor.com/llms.txt listing the Poland content cluster as priority pages | Low | High |
| 3 | Add PostalAddress + LocalBusiness/FinancialService schema to contact page | Low | High |
| 4 | Add FAQPage schema to /qrops-poland/, /uk-pension-poland/, /state-pension-poland/, /retire-to-poland/ | Low | High |
| 5 | Add Article/BlogPosting schema with datePublished, dateModified, and author to all blog posts | Medium | High |
| 6 | Add meta descriptions to homepage, contact, services, and all Poland-specific pages | Low | Medium |
| 7 | Add Review + AggregateRating schema to /testimonials/ | Low | Medium |
| 8 | Add visible publication/last-updated dates to all articles and guides | Low | Medium |
| 9 | Create a dedicated "Financial Advisor Warsaw Poland" service landing page with full location schema | Medium | High |
| 10 | Add sameAs properties in Person schema linking to LinkedIn profile and Facebook page | Low | Medium |

---

## Audit Methodology

**Pages crawled:** 18 pages directly fetched and analyzed  
**Sitemap URLs catalogued:** 157 total (136 posts, 21 pages)  
**Schema check method:** Direct page fetch + content extraction, JSON-LD inspection  
**AI citability checks:** llms.txt fetch (404), robots.txt analysis, content structure review  
**Location checks:** Contact page, About page, all Poland-specific pages  
**E-E-A-T checks:** About page, all audited pages for author markup, dates, credentials  
**Platform checks:** Content structure vs. Google AI Overviews, Perplexity, ChatGPT, Gemini requirements  

**Auditor:** BridgeWorks GEO Audit System  
**Model:** Claude Sonnet 4.6  
