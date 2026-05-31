# GEO Audit Report: Misi's Gin

**Audit Date:** 2026-05-31
**URL:** https://www.misisgin.com/
**Business Type:** Hybrid, Artisanal Distillery (Local, Budapest) + Direct-order Product Brand
**Pages Analyzed:** 2 primary pages (HU home, EN home) across a 6-language single-page WordPress site, plus robots.txt, sitemap, and llms.txt probes

---

## Executive Summary

**Overall GEO Score: 44/100 (Poor)**

Misi's Gin has a real, authentic brand with genuine off-site credibility: international award wins, a TasteAtlas entry, and eight-plus Hungarian retailers all listing consistent product facts. The problem is that the brand's own site gives AI systems almost nothing to work with. There is no structured data, the story content is thin (~280 words), and most hard facts (ABV, botanicals, price) live only on retailers' sites. Worst of all, the server actively returns 404 to GPTBot and ClaudeBot, so ChatGPT and Claude cannot read this site at all even though robots.txt invites them in.

Fix three cheap things first: unblock the AI crawlers, add JSON-LD schema, and rewrite the page answer-first with an FAQ. Those alone would move the score meaningfully within days.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 38/100 | 25% | 9.5 |
| Brand Authority | 58/100 | 20% | 11.6 |
| Content E-E-A-T | 52/100 | 20% | 10.4 |
| Technical GEO | 58/100 | 15% | 8.7 |
| Schema & Structured Data | 8/100 | 10% | 0.8 |
| Platform Optimization | 31/100 | 10% | 3.1 |
| **Overall GEO Score** | | | **44/100** |

---

## Critical Issues (Fix Immediately)

1. **GPTBot and ClaudeBot are served HTTP 404.** Verified directly: requests with `User-agent: GPTBot/1.0` and `ClaudeBot` return 404 on both `/` and `/en/`, while a normal browser returns 200. This is a user-agent block, almost certainly from Wordfence or the Aruba proxy, and it overrides the permissive robots.txt. OpenAI/ChatGPT and Anthropic/Claude cannot crawl or cite this site. Note the inconsistency: `anthropic-ai`, `PerplexityBot`, `CCBot`, `Google-Extended`, and `Googlebot` all get 200. Fix: whitelist GPTBot and ClaudeBot in Wordfence and re-test with `curl -A "GPTBot/1.0" https://www.misisgin.com/` until it returns 200.

2. **No business schema of any kind.** Zero JSON-LD on the site. The only structured data is auto-generated image-gallery microdata from the Envira plugin, which carries no business value. To an AI model this page is an entity with no machine-readable identity, no address, no product, no awards.

3. **No Wikipedia or Wikidata entity.** There is no canonical entity node for the brand anywhere. For AI entity recognition this is the single highest-leverage long-term gap. The brand likely meets notability through its international award wins, TasteAtlas listing, and Hungarian press.

4. **No age-verification gate.** An alcohol site selling across six markets (HU, DE, ES, RO, IT plus EN) loads all content with no age check. This is a legal/compliance and trust failure for a regulated product.

## High Priority Issues

1. **No privacy policy or impressum.** Only a cookie/ÁSZF reference is present. GDPR requires a privacy policy and Hungarian law expects an impressum. This is the biggest trust drag, and it is odd because the business-identity data is otherwise excellent (tax ID, excise license, NÉBIH license all shown).

2. **On-page content is anecdotal, thin, and answer-last.** The ~280-word founder story never states plainly what the product is. There is no ABV, no botanical list, no bottle size, no price on the brand's own pages. The brand has surrendered control of its own factual record to retailers.

3. **No structured product facts and no FAQ.** Nothing on the page answers the literal questions people ask AI: "What is Misi's Gin?", "What's the ABV?", "Where can I buy it?", "What botanicals?". FAQ blocks are disproportionately favored by AI extraction.

4. **Sitemap is broken for GEO.** `/sitemap.xml` lists only three URLs: `/blog/` (lastmod 2015), `/home/` (2023), and `/` (2026-04). The English page and the other five language versions are not in the sitemap at all. The 2015 date is a strong staleness signal. There is also no `Sitemap:` directive in robots.txt.

5. **Awards are stated but not evidenced and incomplete.** The 2021 Silver (Las Vegas Global Spirit Awards) and Gold (World Gin Awards) appear as plain text with no links, no medal images, no category. The strongest award, World Gin Awards 2022 Country Winner for Hungary (Contemporary Style), is not even mentioned on the brand's own site.

6. **No founder credential page.** "Misi" is Mihály Kenyeres, and his story is the entire E-E-A-T spine of the brand, yet there is no named byline, bio, photo with context, or Person schema tying the person to the expertise claim.

7. **No meta description, no Open Graph, no Twitter Card tags.** Verified absent on the EN page. AI and social previews fall back to scraped guesses, so the brand loses snippet control on every surface. The title is a duplicate, `Misi's Gin – Misi's Gin`.

## Medium Priority Issues

1. **Zero security headers.** No HSTS, CSP, X-Frame-Options, X-Content-Type-Options, or Referrer-Policy. HTTPS and redirects are clean, but the header gap is a quality/trust signal.

2. **Cocktail recipes are ingredient lists only, no method.** Negroni, "Thyme is up," and Gin & Tonic list quantities but give no preparation steps. Recipe content with steps is highly extractable by AI and maps to high-volume cocktail queries.

3. **No sitemap hreflang and no x-default.** Hreflang is correctly implemented in the page `<head>` for all six languages, but the sitemap carries no hreflang annotations and there is no `x-default`.

4. **Core Web Vitals risk is moderate.** The page is heavy: ~233 KB HTML, 30 stylesheets, 59 script tags with only one async/defer, jQuery loaded synchronously in `<head>`. Images are PNG/JPG with no WebP/AVIF (932 references, zero webp/avif), which matters for an image-heavy gin site.

5. **No Reddit footprint.** Absent from r/gin, r/spirits, and r/cocktails. Reddit is a recommendation surface that Perplexity in particular samples heavily.

6. **Dormant content layer.** Blog lastmod is 2015 against a 2026 footer, signaling abandonment. No publication or update dates on the live narrative.

## Low Priority Issues

1. **No llms.txt** (confirmed 404). Cheap future-proofing win.
2. **Crawl-Delay 5 plus 6 requests/minute daytime cap** slows full crawls of a six-language site.
3. **Typo "occured"** in the English story. Minor trust signal.
4. **No brand LinkedIn company page.** Weakens Bing Copilot and Microsoft-ecosystem signals.
5. **No WebSite+SearchAction or BreadcrumbList schema.**
6. **Social links present but not declared via `sameAs`,** so AI cannot resolve them to the entity.

---

## Category Deep Dives

### AI Citability (38/100)

The page reads like a charming personal anecdote, not an extractable knowledge source. It is narrative-heavy, fact-light, and structurally bare. The cocktail recipes and the award claims are the only genuinely quotable assets.

**Weak passage (origin story):** "The founder first consumed gin in November 2020 at age 44... the recipe also occurred to me in the bathtub." It is anecdotal, has a typo, and never states what the product is.

**Rewrite (answer-first):** "Misi's Gin is a handcrafted modern dry gin produced in Budapest by Mihály Kenyeres. Bottled at 40% ABV in 0.5L format, it is distilled in small weekend batches using a copper still, with hand-ground botanicals and a Japanese citrus character. Kenyeres founded the brand in 2020."

**Awards rewrite (structured fact block):** "Awards: Gold, World Gin Awards England (2021); Silver, Las Vegas Global Spirit Awards (2021); Country Winner, Hungary, World Gin Awards 2022 (Contemporary Style). Official tasting note: 'A pleasant nose leads to a classical, well-balanced palate with pine and floral notes. Clean, with a light mouthfeel.' ABV 40.5%."

### Brand Authority (58/100)

Off-site authority is genuinely solid for a micro-brand, which is what keeps this score from being low. The brand benefits from trustworthy, mutually consistent citations, exactly what AI uses to verify an entity.

| Platform | Status | Detail |
|---|---|---|
| Wikipedia / Wikidata | Absent | No article, no item. Biggest entity-recognition gap. |
| Awards databases | Strong | World Gin Awards live listing: Country Winner Hungary 2022, 40.5% ABV, official tasting note. |
| Food/spirits DB | Present | TasteAtlas entry ("Misi's Modern Dry Gin"). High-trust structured source. |
| Retailers | Strong | 8+ Hungarian webshops plus Árukereső, consistent 0.5L / 40% / ~13-16k HUF. |
| Press / editorial | Minimal | Niche Hungarian and Romanian coverage. |
| YouTube | Minimal | Brand story video exists, no channel scale. |
| Reddit | Absent | Zero discussion footprint. |
| LinkedIn (brand) | Absent | No company page. |
| Instagram / Facebook / TikTok | Present | Active official accounts. |

### Content E-E-A-T (52/100)

A genuine founder-led brand with strong authenticity and excellent business-identity transparency, undercut by thin depth, missing legal pages, and unverified awards.

| Dimension | Score | Evidence |
|---|---|---|
| Experience | 17/25 | Strong first-person founder narrative and a real recipe-development journey. Lacks process documentation. |
| Expertise | 13/25 | Claimed alcohol-making education and expert analysis, but no named credentials, no author page, no technical depth. |
| Authoritativeness | 11/25 | Two real awards, but no press links, no external citations, no links to award bodies. |
| Trustworthiness | 11/25 | Excellent identity data (tax ID, excise and NÉBIH licenses, address, phone). Severely undercut by missing privacy policy, impressum, and age gate. |

AI-content likelihood: highly likely human. The specific voice, concrete dates, and personal arc are the brand's strongest content asset.

### Technical GEO (58/100)

A strong server-side-rendered WordPress foundation wasted by a UA-level block on the two biggest AI crawlers and a skeletal, stale sitemap.

| Area | Status |
|---|---|
| Server-side rendering | Good. Body copy present in raw HTML, no JS execution needed. |
| GPTBot / ClaudeBot access | Critical. Served 404. |
| Sitemap | Critical. 3 URLs, 2015 lastmod, missing all language versions. |
| Security headers | Critical. None present. |
| Meta / OG / Twitter | Poor. All absent on EN. |
| Hreflang in head | Good. All six languages, self-referencing. No x-default. |
| Canonical, viewport, lang | Correct. Robots meta indexable. |
| Redirects | Clean. Single 301 hops for http and non-www. |
| Core Web Vitals | Fair. Render-blocking CSS/JS, no WebP/AVIF. |

### Schema & Structured Data (8/100)

The lowest-scoring category. The only markup is plugin-generated `ImageGallery` microdata (1 gallery, 30 `ImageObject`), which has no business value. No SEO plugin is installed, which is why nothing is auto-generated. Installing Rank Math or Yoast would deliver baseline Organization and WebSite schema almost for free. All GEO-critical types are missing: Organization/LocalBusiness, Person, Product, award properties, Recipe, sameAs, FAQPage, BreadcrumbList. Ready-to-use JSON-LD for the top three types is in the Appendix.

### Platform Optimization (31/100)

| Platform | Score | Status |
|---|---|---|
| Google Gemini | 38/100 | Best positioned. Google Business Profile potential, multilingual reach, recipe content. |
| Google AI Overviews | 34/100 | Recipes are extractable, but broken heading hierarchy and no schema. |
| ChatGPT Web Search | 33/100 | Blocked by the GPTBot 404 and no entity record. |
| Perplexity | 28/100 | No Reddit/community validation, no freshness dates. |
| Bing Copilot | 24/100 | Critical. No IndexNow, no LinkedIn, weak Bing footprint. |

Note: ChatGPT's effective score is dragged down further by the live GPTBot 404, which blocks crawling outright.

---

## Quick Wins (Implement This Week)

1. **Unblock GPTBot and ClaudeBot** in Wordfence and confirm with `curl -A "GPTBot/1.0"` returning 200. Highest-leverage fix on the whole site.
2. **Install an SEO plugin** (Rank Math or Yoast) and add the Organization/LocalBusiness, Person, and Recipe JSON-LD from the Appendix. Fixes schema, meta description, and Open Graph in one move.
3. **Rewrite the EN and HU page answer-first:** one definitional sentence, then a spec block (ABV, volume, botanicals, distillation), then awards as a list, then the story. Fix the "occured" typo.
4. **Add an FAQ section:** what it is, ABV, botanicals, price, where to buy, who makes it. One to three sentences each.
5. **Add a `Sitemap:` line to robots.txt** and regenerate a complete, language-aware sitemap with correct lastmod dates.

## 30-Day Action Plan

### Week 1: Access and Identity
- [ ] Whitelist GPTBot and ClaudeBot, verify 200 responses
- [ ] Install SEO plugin and publish Organization/LocalBusiness + Person + Recipe JSON-LD
- [ ] Add per-language meta descriptions and Open Graph tags
- [ ] Add `Sitemap:` directive to robots.txt and regenerate the sitemap

### Week 2: Content and Compliance
- [ ] Rewrite EN/HU pages answer-first with a product spec block
- [ ] Add an FAQ section covering the core gin questions
- [ ] Add an age-verification gate (localized per market)
- [ ] Publish privacy policy and impressum, link ÁSZF in the footer

### Week 3: Authority and Evidence
- [ ] Add the World Gin Awards 2022 Country Winner award and the official tasting note to the site
- [ ] Link awards to the awarding bodies and add medal imagery
- [ ] Create a founder bio/credentials block with a named byline and photo
- [ ] Add preparation steps to each cocktail recipe

### Week 4: Off-site and Hardening
- [ ] Create a Wikidata item for the brand and founder, citing award notability; begin Hungarian Wikipedia stub
- [ ] Create/claim Google Business Profile (Distillery) with full NAP
- [ ] Add security headers (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, basic CSP)
- [ ] Seed authentic Reddit/forum mentions; publish llms.txt; verify Bing Webmaster Tools and enable IndexNow

---

## Appendix A: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| https://www.misisgin.com/ | Misi's Gin – Misi's Gin | No schema, thin content, no meta description, GPTBot/ClaudeBot 404 |
| https://www.misisgin.com/en/ | Misi's Gin – Misi's Gin | No schema, no OG/Twitter, no meta description, ~280-word body, GPTBot/ClaudeBot 404 |
| /robots.txt | n/a | Allow-all but no Sitemap directive; restrictive rate limits |
| /sitemap.xml | n/a | 3 URLs only, 2015 lastmod, missing language versions |
| /llms.txt | n/a | 404 (absent) |

## Appendix B: Ready-to-Use JSON-LD

Add each inside a `<script type="application/ld+json">` tag in the site `<head>`, server-rendered (via the SEO plugin's custom-schema field or the theme header), not injected by JavaScript.

### 1. LocalBusiness / Distillery

```json
{
  "@context": "https://schema.org",
  "@type": ["Distillery", "LocalBusiness"],
  "@id": "https://www.misisgin.com/#organization",
  "name": "Misi's Gin",
  "url": "https://www.misisgin.com/",
  "logo": "https://www.misisgin.com/wp-content/uploads/logo-fc.png",
  "description": "Misi's Gin is an artisanal small-batch gin handcrafted in Budapest, Hungary by founder Mihaly Kenyeres.",
  "telephone": "+36 30 206 4320",
  "email": "misi@misisgin.com",
  "founder": { "@id": "https://www.misisgin.com/#founder" },
  "foundingDate": "2020",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Paskal-malom utca 3",
    "addressLocality": "Budapest",
    "postalCode": "1141",
    "addressCountry": "HU"
  },
  "sameAs": [
    "https://www.facebook.com/people/Misis-Gin/100083190165909/",
    "https://www.instagram.com/misisgin/",
    "https://www.tiktok.com/@misis.gin"
  ],
  "award": [
    "Las Vegas Global Spirit Awards 2021 - Silver Medal",
    "World Gin Awards 2021 - Gold",
    "World Gin Awards 2022 - Country Winner Hungary, Contemporary Style"
  ]
}
```

### 2. Person (founder)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://www.misisgin.com/#founder",
  "name": "Mihaly Kenyeres",
  "jobTitle": "Founder & Distiller",
  "worksFor": { "@id": "https://www.misisgin.com/#organization" },
  "url": "https://www.misisgin.com/",
  "knowsAbout": ["Gin distillation", "Artisanal spirits", "Craft cocktails"],
  "description": "[REPLACE: 1-2 sentence bio of Mihaly Kenyeres, the maker behind Misi's Gin]",
  "image": "[REPLACE: URL of founder headshot]"
}
```

### 3. Recipe (Negroni)

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Misi's Gin Negroni",
  "image": "[REPLACE: URL of the Negroni photo on the site]",
  "author": { "@id": "https://www.misisgin.com/#organization" },
  "description": "A classic Negroni made with Misi's Gin, a small-batch artisanal gin from Budapest.",
  "recipeCategory": "Cocktail",
  "recipeCuisine": "Cocktail",
  "keywords": "negroni, gin cocktail, Misi's Gin",
  "recipeYield": "1 cocktail",
  "recipeIngredient": [
    "30 ml Misi's Gin",
    "30 ml sweet vermouth",
    "30 ml Campari",
    "Orange peel, to garnish"
  ],
  "recipeInstructions": [
    { "@type": "HowToStep", "text": "Fill a rocks glass with ice." },
    { "@type": "HowToStep", "text": "Pour the gin, vermouth and Campari over the ice and stir for 20-30 seconds." },
    { "@type": "HowToStep", "text": "Garnish with an orange peel and serve." }
  ]
}
```

---

*office@bridgeworks.agency · bridgeworks.agency*
