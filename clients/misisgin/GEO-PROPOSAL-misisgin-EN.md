# GEO Optimization Proposal (English reference copy)
## Misi's Gin: AI Search Visibility

**Prepared by:** BridgeWorks
**Prepared for:** Mihály Kenyeres, Misi's Gin (Kenyeres Mihály E.V.)
**Date:** 2026-05-31
**Valid until:** 2026-06-30
**Reference:** GEO-PROP-260531-misisgin

> Internal note (not for the client): this is your English reference version. The Hungarian file `GEO-PROPOSAL-misisgin-HU.md` is the one to send. Pricing is scaled for a micro-brand sole proprietor: a one-time foundation fix plus an optional light retainer, not the standard agency monthly tiers. HUF figures use an approximate rate of ~390 HUF/EUR and should be confirmed before sending. All prices exclude VAT (ÁFA); invoice via szamlazz.hu / NAV.

---

## Executive Summary

Misi's Gin is an award-winning artisanal gin made in Budapest by Mihály Kenyeres. The brand has real credibility off-site: a Gold at the World Gin Awards, a Country Winner title for Hungary, a TasteAtlas entry, and a dozen Hungarian retailers carrying the product.

Our GEO audit on 2026-05-31 puts the website at **44/100 (Poor)**. The gap is not the brand. It is that the website gives AI assistants almost nothing to work with, and in two cases actively shuts them out.

The three most urgent issues:

1. **ChatGPT and Claude are blocked at the server.** The site returns a "not found" error to OpenAI's and Anthropic's crawlers. The two most-used AI assistants literally cannot read the page, so they cannot recommend Misi's Gin when someone asks for a Hungarian craft gin.
2. **The site has no structured data.** AI has no machine-readable record of the brand, the product, the awards, or the maker. When AI describes the gin, it relies on retailers' pages, not yours.
3. **No age gate, privacy policy, or impressum.** For an alcohol site selling across six markets this is a legal and trust gap, and AI models read missing trust signals as lower quality.

Recommendation: a one-time **GEO Foundation Fix** that clears every critical and high issue, with an optional light monthly retainer for the off-site authority work that pays off over time.

---

## Why this matters for Misi's Gin

People increasingly ask ChatGPT, Google's AI answers, and Perplexity questions like "best Hungarian craft gin," "gin gift Budapest," or "award-winning small-batch gin." A Gold-medal gin should win those answers. Right now Misi's is close to invisible in them, while retailers who stock the gin show up instead. That means the discovery, and often the sale, goes through a middleman or a competitor.

The fix is mostly technical and one-time. Once the AI assistants can read the site and the brand's facts are machine-readable, the award wins start working for the brand inside AI answers.

---

## Audit findings summary

| Category | Score | Priority |
|---|---|---|
| AI Citability & Visibility | 38/100 | High |
| Brand Authority Signals | 58/100 | Medium |
| Content Quality & E-E-A-T | 52/100 | Medium |
| Technical Foundations | 58/100 | High |
| Structured Data | 8/100 | High |
| Platform Optimization | 31/100 | High |
| **Overall GEO Score** | **44/100** | **Poor** |

### Critical issues

**1. ChatGPT and Claude crawlers are served an error**
What we found: GPTBot and ClaudeBot receive a 404 while normal visitors get the page. A firewall rule is blocking them.
Business impact: the two biggest AI assistants cannot see or cite the site at all.
Our fix: whitelist both crawlers and verify they receive the page.

**2. No structured data anywhere**
What we found: zero business schema. AI has no machine-readable identity for the brand, product, awards, or maker.
Business impact: AI describes the gin from third-party pages, not from the brand.
Our fix: add full JSON-LD (Distillery, Product, Person, Recipe, awards, social links).

**3. Missing legal and compliance pages**
What we found: no age-verification gate, no privacy policy, no impressum on a six-market alcohol site.
Business impact: legal exposure plus a trust penalty in AI quality signals.
Our fix: add an age gate, privacy policy, and impressum, and surface the existing business identity data properly.

### High-priority issues
- Thin, story-only content with no product facts (ABV, botanicals, size, price) on the brand's own pages
- No FAQ answering the questions buyers actually ask AI
- Broken sitemap (3 URLs, a 2015 date, missing all six language versions)
- Awards stated but not evidenced, and the strongest 2022 award not mentioned at all
- No meta descriptions, no social preview tags

---

## Our solution

### GEO Foundation Fix (one-time)
**~550,000 HUF (~€1,400) + VAT**

A single defined project, roughly 4 to 6 weeks, that clears every critical and high issue:

- Unblock GPTBot and ClaudeBot, verify access for all major AI crawlers
- Full JSON-LD schema: Distillery/LocalBusiness, Product, Person (founder), Recipe for the cocktails, awards, and social links
- Rewrite the EN and HU homepage answer-first, with a clear product spec block (ABV, botanicals, size, origin)
- Add an FAQ section covering the core gin questions
- Rebuild the sitemap with all six languages and correct dates, add the robots.txt sitemap line
- Add the missing 2022 award and link awards to the awarding bodies
- Add age-verification gate, privacy policy, and impressum
- Add meta descriptions and social preview tags per language
- Publish llms.txt

Expected outcome: a substantially higher GEO score, with the site readable and citable by every major AI assistant. We commit to the work and the methodology, not to a specific score number.

### Visibility Care (optional retainer)
**~135,000 HUF/month (~€350) + VAT, 3-month minimum**

For the off-site authority work that compounds over time:

- Prepare and submit a Wikidata entry for the brand and founder (acceptance is at the platform's discretion)
- Set up and optimize the Google Business Profile (Distillery, Budapest)
- One to two pieces of content or cocktail recipes per month with proper schema
- Authentic participation in relevant Reddit and Hungarian spirits communities, within each platform's rules
- Monthly check on AI visibility and a short progress note

---

## Investment summary

| Item | HUF | EUR (approx.) |
|---|---|---|
| GEO Foundation Fix (one-time) | 550,000 | €1,400 |
| Visibility Care (per month, optional) | 135,000 | €350 |
| Foundation + 3 months Care | 955,000 | €2,450 |

All prices exclude VAT (ÁFA). Invoiced via szamlazz.hu.

---

## Next steps

1. Review the findings and the Hungarian proposal
2. A short call to walk through the audit together
3. Agree scope and start date for the Foundation Fix
4. Read access to Google Search Console if available (helpful, not required)

This proposal is valid until 2026-06-30.

---

*office@bridgeworks.agency · bridgeworks.agency*
