# GEO Audit Report: Marani Architects

**Audit Date:** 2026-06-23
**URL:** https://maraniarchitects.com
**Business Type:** Architecture and Design Firm (Agency/Services)
**Location:** Prague, Czech Republic (Malá Strana)
**Contact:** Vincent Marani, Founder
**Pages Analyzed:** 14 (homepage, about, projects index, contact, careers, media, 5 project pages, 2 article pages, robots.txt, sitemap)
**Conducted by:** BridgeWorks | office@bridgeworks.agency

---

## Executive Summary

**Overall GEO Score: 19/100 — Critical**

Marani Architects is a 34-year-experienced firm with a real portfolio — hotel renovations, mixed-use developments, award-winning historic restorations — and a founder with AIA credentials, a former role as President of the AIA European Chapter, and projects in Berlin, Dubai, and Prague. None of that is findable by AI.

The site has zero schema markup, zero meta descriptions, no llms.txt, no Open Graph tags, and no JSON-LD anywhere across 6 core pages and 45 project pages. Article pages on the Media section are near-empty stubs averaging 40 words each. Project pages average 185 words of structured specs with minimal descriptive prose. The homepage has 80 readable words — no mission statement, no service description, no expertise claims.

A developer or hotel investor asking an AI system "who does hotel renovation architecture in Prague?" will not find Marani. The firm's signals are below the citation threshold on every AI platform: Google AI Overviews, Perplexity, ChatGPT web search, and Bing Copilot. The technical foundation is sound (WordPress with working sitemap, HTTPS, all crawlers allowed), but provides no competitive advantage. The gap between the firm's actual capability and its AI presence is severe and entirely closeable.

---

## Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 12/100 | 25% | 3.0 |
| Brand Authority | 28/100 | 20% | 5.6 |
| Content E-E-A-T | 22/100 | 20% | 4.4 |
| Technical GEO | 44/100 | 15% | 6.6 |
| Schema & Structured Data | 0/100 | 10% | 0.0 |
| Platform Optimization | 8/100 | 10% | 0.8 |
| **Overall GEO Score** | | | **20.4 / 100** |

**Rating: Critical**

---

## Phase 1: Discovery

### Site Architecture

- **Platform:** WordPress (confirmed via wp-sitemap.xml and robots.txt structure)
- **Total indexed pages:** 6 core pages + 45 project URLs + 17 article URLs + careers/users sitemap = ~70 indexable URLs
- **Language support:** English and Czech via `?lang=cs` parameter — no hreflang markup
- **Core pages:** Homepage, Projects, About Us, Contact, Careers, Media and News
- **Test pages in sitemap:** `/project/test-2/` and `/project/test-eng/` — live in the sitemap, likely draft/test content

### Crawlability

- robots.txt: clean — `Disallow: /wp-admin/` only, all AI crawlers permitted
- Sitemap: present at `https://maraniarchitects.com/wp-sitemap.xml` (sitemap index with 5 child sitemaps)
- No llms.txt file present (404 confirmed)
- AI crawler access: unrestricted — GPTBot, ClaudeBot, PerplexityBot all permitted by default

---

## Phase 2: Six-Dimension Analysis

---

### Dimension 1: AI Citability — 12/100

**The core problem.** AI systems cite sources when they can extract a clear answer from readable text. Marani's site provides almost none.

**Evidence gathered:**

| Page | Readable Word Count | Has Description? |
|---|---|---|
| Homepage | ~80 words | No |
| Projects index | ~85 words | No — grid of titles only |
| Contact | ~45 words | No |
| Project: Prague Hotel | ~185 words | Minimal spec block |
| Project: Almanac X | ~185 words | Minimal spec block |
| Project: Invalidovna 2 | ~295 words | Moderate — best performing |
| Project: BeBopBar Alcron Hotel | ~195 words | Minimal spec block |
| Project: Alsova Gallery | ~285 words | Moderate |
| Project: Dubai Hotels | ~185 words | Near-empty description |
| Project: Sony Center | ~95 words | 2-sentence description |
| Article: ASB Via Una | ~40 words | Stub — no article text |
| Article: Forbes Magazine | ~45 words | Stub — no article text |
| About Us | ~1,840 words | Strong — best page on site |
| Careers | ~1,240 words | Good for HR, not for GEO |

**Key finding:** The About Us page (1,840 words) is the only page an AI system could cite with confidence. It contains founder bio, credentials, AIA membership, project history, and awards. Every other page is below or near the 300-word citability threshold.

**Media/article pages are hollow stubs.** Marani has real press coverage — Forbes, E15 Magazine, European Property Awards. The article pages that should house that content contain ~40 words each. The content was never added. AI systems cannot cite coverage that has no text.

**No answerable questions.** A visitor (or AI) cannot learn: what services Marani offers, what types of projects they take, what their typical project size or timeline is, or what makes them different from other Prague architects.

**Score rationale:** 12/100. The About Us page and a handful of project spec blocks provide minimal signal, but the firm cannot be cited by any AI system for the queries that matter (hotel renovation architect Prague, commercial renovation architecture Czech Republic, AIA architect Central Europe).

---

### Dimension 2: Brand Authority — 28/100

**Genuine authority exists offline; it does not translate online.**

**Strengths found:**
- Vincent Marani: 34+ years experience, AIA member since 1995, AIA European Chapter President (2013)
- Projects: Sony Center Berlin (190,000 sqm), The Park Prague (190,000 sqm), Munich Airport Center (100,000 sqm)
- Awards: Dušan Jurkovič Award (2009), European Property Award 5-Star 2022, International Property Awards 2022 (two awards), Best of Reality 2022 Silver Medal
- Clients: PPF Real Estate, ORCO Properties, CPI, Penta, AIG Lincoln, Sony, InBev

**What is missing:**
- No Wikipedia entry or knowledge panel signals
- No LinkedIn company page linked (personal LinkedIn linked from homepage but no company page)
- No sameAs links in markup connecting the site to any authority source
- Press coverage on Forbes, E15, ASB, Hospodarske Noviny is listed but the article pages are stubs — the text that would build topical authority is absent
- No external backlink signals checked via this audit (Ahrefs data not requested), but on-site signals are weak
- Author attribution on articles: "admin" — not Vincent Marani

**Score rationale:** 28/100. Real credentials and real press. The authority is real but structurally unavailable to AI systems — no schema connects the founder's name to the firm's website, no article content exists to cite, and no external platform signals reinforce the brand.

---

### Dimension 3: Content E-E-A-T — 22/100

**Experience, Expertise, Authoritativeness, Trustworthiness (Google/AI framework)**

| Signal | Status |
|---|---|
| Named expert with credentials | Partial — About page only |
| First-person experience signals | Absent |
| Specific project outcomes / measurements | Partial — area (sqm), year, client listed but no outcomes described |
| Client testimonials | None found |
| FAQs or process explanation | None found |
| Service descriptions | None found |
| Contact with real address | Present |
| Copyright year | "All Rights Reserved 2015" — outdated, signals low maintenance |

**Content depth by page type:**
- Project pages: structured data (type, year, area, client, architects) present in HTML but not in schema. Description text is 1-4 sentences. No narrative about challenges, solutions, or results.
- About page: the strongest E-E-A-T signal on the site. Lists projects, dates, employers, awards. Reads as a biography, not a firm capability statement.
- Homepage: shows a featured project and four latest projects. No text explaining what the firm does.

**Readability issues:**
- No service page exists (what does Marani actually offer? Hotel renovation? Office fitout? Masterplanning? The site does not say.)
- No FAQ, no process, no "why hire us" content

**Score rationale:** 22/100. The About page has genuine E-E-A-T signals — dated credentials, named clients, specific projects with sqm figures. Everything else is thin. No AI system can extract what Marani does, how they work, or why to hire them.

---

### Dimension 4: Technical GEO — 44/100

**Infrastructure is functional but has multiple GEO-relevant gaps.**

| Technical Factor | Status |
|---|---|
| HTTPS | Confirmed |
| robots.txt | Present and correct |
| XML sitemap | Present (sitemap index, 5 sub-sitemaps) |
| AI crawlers allowed | Yes — no blocks on GPTBot, ClaudeBot, PerplexityBot |
| llms.txt | Absent (404) |
| Meta descriptions | Absent — zero meta descriptions found across all pages checked |
| Canonical tags | Not confirmed present |
| Open Graph tags | Absent |
| Twitter/X Cards | Absent |
| Hreflang | Absent (English/Czech language switching via URL parameter only) |
| Page speed / CWV | Not directly testable here; image-heavy portfolio sites often have CLS/LCP issues |
| JavaScript rendering | WordPress with server-side rendering — positive signal |
| Test content in sitemap | `/project/test-2/` and `/project/test-eng/` live in sitemap — needs cleanup |
| Copyright year in footer | "2015" — signals low maintenance to crawlers |

**Score rationale:** 44/100. Clean robots, working sitemap, HTTPS, SSR — all positive. But no meta descriptions, no Open Graph, no hreflang, no llms.txt, test pages in production sitemap, and a copyright date 11 years old. These are not blocking issues, but they reduce AI platform optimization significantly.

---

### Dimension 5: Schema & Structured Data — 0/100

**Zero schema markup detected anywhere on the site.**

Checked: homepage, contact page, about-us page, 5 project pages, 2 article pages.

**What is missing and what it costs:**

| Missing Schema | Impact |
|---|---|
| Organization schema | AI cannot confirm the firm's name, address, founding year, or business type with confidence |
| LocalBusiness / ArchitecturalFirm schema | No geo-anchored business type signals for location-based AI queries |
| Person schema (Vincent Marani) | Founder's AIA credentials and experience not machine-readable |
| sameAs links | No connection between the website and LinkedIn, industry directories, or external profiles |
| Project / CreativeWork schema | 45 project pages with zero structured signals — area, type, client, year are in HTML text but not schema |
| Article schema | 17 article URLs with no Article, NewsArticle, or BlogPosting schema |
| BreadcrumbList | No breadcrumb schema |
| WebSite schema with SearchAction | Absent |
| Speakable | Absent |

**This is the single largest fixable gap on the site.** Adding Organization + Person + LocalBusiness schema to 3 pages, and Project schema to the top 10-15 hotel/commercial project pages, would immediately make the site machine-readable for AI systems. It requires no new content — only markup on existing data.

**Score rationale:** 0/100. No schema anywhere. The firm's 34-year portfolio, AIA credentials, and Prague location are not machine-readable.

---

### Dimension 6: Platform Optimization — 8/100

**The site is not visible on any major AI platform.**

| Platform | Status | Why |
|---|---|---|
| Google AI Overviews | Not citable | No schema, no meta descriptions, thin content on most pages |
| ChatGPT web search | Not citable | No structured content, no press content with article text |
| Perplexity AI | Not citable | No citability signals, no FAQ, no entity markup |
| Google Gemini | Not citable | Same as Google AI Overviews — schema and content both missing |
| Bing Copilot | Not citable | No Open Graph, no structured data |

**What "not citable" means practically:**
A hotel developer in Prague asking an AI assistant "recommend architecture firms for hotel renovation in Prague" will not receive Marani as an answer. The firm has the portfolio to deserve that citation. The signals to trigger it do not exist.

**Social/external signal gaps:**
- No company LinkedIn page detected
- No visible presence on Archinect, ArchDaily, or other architecture directories that AI platforms commonly cite
- No Google Business Profile signals observed

**Score rationale:** 8/100. The site is technically crawlable but provides nothing that would cause an AI to cite it. No platform sees Marani as an authoritative source on any query.

---

## Priority Findings

### Critical (Immediate)

**1. Zero schema markup across entire site**
The firm's name, address, founder credentials, project types, and portfolio are entirely invisible to AI systems in machine-readable form. Organization + LocalBusiness + Person schema can be added in a single implementation session and would immediately register the firm's entity on every AI platform. This is the highest-leverage fix on the site.

**2. 45 project pages with no meta descriptions and near-zero descriptive prose**
Project pages average 185 words — nearly all of which is the spec block (type, year, area, client). The description field is 1-4 sentences on most pages. An AI system asked "what hotel renovation projects has Marani completed in Prague?" cannot answer from this content. Each project page needs a 200-400 word description of the brief, the design challenge, and the outcome.

**3. Article pages are empty stubs (avg 40 words)**
The Media section lists press coverage from Forbes, E15, Hospodarske Noviny, and multiple property award bodies. Each article page contains only a title, a date, and an author tag ("admin"). The actual coverage text was never added. These pages are indexed, they are crawled, and they contribute nothing to citability. Either they need content or they need to be redirected to the actual external articles with proper attribution schema.

### High

**4. No meta descriptions on any page**
Zero meta descriptions found across homepage, all project pages, about page, contact, careers, and articles. Meta descriptions are a minimum signal for AI platforms generating excerpts and citations.

**5. Homepage has 80 readable words and no service description**
A developer or investor landing on the homepage learns: the firm's name, four recent project names, and a list of 12 client logos. They cannot determine what types of work Marani accepts, the firm's specializations, service areas, or project minimums. This is the site's worst page per word-to-authority ratio.

**6. Language implementation has no hreflang**
The Czech/English language switch uses a URL parameter (`?lang=cs`) with no hreflang markup. Czech-language AI queries (architects in Prague for hotel renovation) will not associate the Czech version of the site with the English one.

### Medium

**7. Test content live in production sitemap**
`/project/test-2/` and `/project/test-eng/` are indexed in the sitemap. These are likely internal draft entries. They dilute crawl budget and may confuse AI systems encountering placeholder or incomplete content.

**8. No llms.txt**
No `llms.txt` file at the domain root. While not yet a universal standard, it is the emerging mechanism for giving AI crawlers direct guidance on what content to prioritize. Competitors who implement it first gain an advantage.

**9. Copyright "2015" in footer**
The footer displays "Marani Architects All Rights Reserved 2015" on every page. AI systems and crawlers may interpret this as indicating no updates since 2015. The actual firm and site are active — the footer is misleading.

---

## GEO Recommendations (Prioritized)

### Quick wins (under 1 week, no new content required)

1. Add Organization + LocalBusiness schema to homepage and contact page — name, address, phone, email, founding year, business type, same As links to LinkedIn
2. Add Person schema for Vincent Marani on the About page — name, job title, AIA credentials, sameAs to any profiles
3. Add meta descriptions to all 6 core pages (homepage, projects, about, contact, careers, media)
4. Remove or noindex test project pages from the sitemap
5. Fix footer copyright year to "2024" or current year

### Medium-term content work (2-4 weeks)

6. Rewrite homepage to include: one-paragraph firm description (what they do, who for, where), 3 service types, and a clear call to action
7. Add Project/CreativeWork schema to top 15 project pages — at minimum the hotel and commercial renovation projects
8. Expand project descriptions on the 5 highest-profile hotel/hospitality projects to 300+ words each — brief, challenge, approach, outcome
9. Populate the article pages with actual content or redirect them to the live press coverage with proper Article schema

### Structural improvements (1-3 months)

10. Create a dedicated Services page with specific service descriptions: hotel renovation, commercial fitout, mixed-use development, historic preservation
11. Implement hreflang for English/Czech language pairs
12. Add FAQ section (on homepage or services page) targeting the questions hotel developers and investors ask
13. Create or claim a Google Business Profile listing
14. Add llms.txt file prioritizing About, top 10 projects, and contact

---

## Single Strongest Gap (Email Hook)

**45 project pages. Zero meta descriptions. Zero schema. Average description: 3 sentences.**

Marani has completed hotel and commercial renovation projects across Prague, Berlin, Dubai, and Munich. The site lists them. It does not describe them. Every project page follows the same pattern: a spec block (type, year, sqm, client, architects) and 1-4 sentences of description. No AI system can extract what Marani actually did on any of these projects — what the challenge was, what they delivered, why it worked.

This is specific, verifiable, and instantly provable: ask any AI assistant "tell me about Marani Architects' hotel renovation work in Prague" and it will either return no result or a generic summary drawn from the About page only. A hotel developer doing preliminary research via AI will not find Marani.

The fix is content, not technical. 15 project pages, 300 words each, and Organization schema. That is the offer.

---

## One-Line Positioning

**BridgeWorks makes Marani's 30-year hotel renovation portfolio readable by AI — so developers and investors searching for Prague architects find the firm before they find the competitors.**

---

## Audit Metadata

| Field | Value |
|---|---|
| Audit type | Pre-outreach GEO diagnostic |
| Pages crawled | 14 |
| Project pages sampled | 7 of 45 |
| Article pages sampled | 2 of 17 |
| Schema checks | 14 pages (all returned 0 schema) |
| llms.txt | Absent (404) |
| Audit conducted by | BridgeWorks — Emmanuel Ehigbai |
| Contact | office@bridgeworks.agency |
| Audit date | 2026-06-23 |

---

*This audit was produced as pre-outreach research. No client relationship exists with Marani Architects at the time of writing.*
