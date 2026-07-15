# BridgeWorks AI Visibility Methodology v1

Date: 2026-07-14
Status: internal method for future audits and the 2026 report

## What the method measures

BridgeWorks uses `AI visibility` as shorthand for a business's readiness to be discovered, understood, corroborated, and cited across search and AI-assisted discovery surfaces.

It is not a score issued by Google, OpenAI, Microsoft, or any other platform. It does not guarantee that a business will appear in an answer. A BridgeWorks score is a diagnostic prioritisation tool that combines observable website, entity, content, discovery, and conversion signals.

## Primary-source guardrails

1. OpenAI documents `OAI-SearchBot` as the crawler used to surface sites in ChatGPT search. It is distinct from `GPTBot`, which is associated with model training. Audit reports must test and describe these separately. Source: https://developers.openai.com/api/docs/bots
2. Google states that normal Search fundamentals remain relevant for AI Overviews and AI Mode and that no special AI schema is required. Source: https://developers.google.com/search/docs/appearance/ai-features
3. Google says structured data can help it understand page meaning and can enable search features, but correct markup does not guarantee appearance. Source: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
4. Bing recommends crawlable links, XML sitemaps, and IndexNow to support discovery and freshness across Bing and Copilot. These signals improve eligibility and index accuracy but do not guarantee visibility. Source: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
5. `llms.txt` is an experimental proposal for a curated LLM-readable site overview. It is not a universal crawler-control standard and must not be described as a confirmed ranking factor. Source: https://llmstxt.org/

## Evidence classes

| Class | Meaning | Example |
|---|---|---|
| Observed | Directly fetched, inspected, or read from an authoritative account. | A 404 from `/sitemap.xml`; Search Console property status. |
| Reported | Supplied by a client, owner, or prior record but not directly reproduced in the current run. | A review count supplied from Maps. |
| Inferred | A cautious conclusion from observed facts. | Fragmented listings are likely to make entity reconciliation harder. |
| Not tested | The audit scope did not support a conclusion. | Schema status when no owned site was located. |

Audit outputs must not convert reported, inferred, or not-tested items into observed facts.

## Stable scoring model for new full audits

Historical BridgeWorks audits used evolving category weights. Do not average or rank their scores as if they came from one stable benchmark. Starting with methodology v1, new full audits use the following 100-point model.

| Domain | Weight | What is checked |
|---|---:|---|
| Crawl and index readiness | 20 | HTTP access, robots directives, canonical URLs, internal links, sitemap coverage, freshness signals, Search Console/Bing evidence where available. |
| Entity clarity | 15 | Clear legal/brand identity, location, named people, consistent business information, authoritative profiles, disambiguation. |
| Answer-ready content | 20 | Specific service pages, direct answers, original evidence, named expertise, dates, citations, buyer questions, content depth appropriate to the topic. |
| Structured information | 15 | Accurate JSON-LD or equivalent markup that matches visible content and uses relevant supported types. |
| Authority and corroboration | 15 | Reviews, profiles, press, memberships, references, and third-party evidence that can corroborate first-party claims. |
| Conversion and measurement | 15 | Clear enquiry/booking path, working forms and links, analytics, search measurement, source tracking, and handoff readiness. |

### Scoring bands

| Score | Band | Interpretation |
|---|---|---|
| 0 to 24 | Critical | Major access, identity, or evidence gaps prevent reliable discovery and evaluation. |
| 25 to 49 | Weak | Some useful content or authority exists, but important signals are fragmented or missing. |
| 50 to 69 | Developing | The foundation works, but consistency, authority, content, or measurement limits performance. |
| 70 to 84 | Good | Strong, coherent foundation with a smaller number of material gaps. |
| 85 to 100 | Advanced | Comprehensive, maintained, measured, and well-corroborated system. This still does not guarantee inclusion. |

## Required checks

### Crawl and index

- Test representative URLs with normal and relevant crawler user agents where permitted.
- Inspect status codes, redirect chains, canonical tags, robots directives, sitemap coverage, and internal discovery.
- Separate crawler access from index presence. A 200 response does not prove indexing.
- Separate index presence from answer inclusion. An indexed URL is only eligible, not guaranteed to appear.

### Entity clarity

- Record the exact business name, location, category, legal identity where public, and named decision makers or experts.
- Compare owned-site details with Google Business Profile, major directories, social profiles, and authoritative registries.
- Treat Wikidata, Wikipedia, and knowledge panels as possible corroboration, not mandatory checkboxes.

### Answer-ready content

- Evaluate whether pages answer real buyer questions with specific, attributable information.
- Prefer first-hand examples, methods, dates, qualifications, policies, case evidence, and limitations over generic marketing copy.
- Do not apply arbitrary word-count thresholds as universal rules. The necessary depth depends on the query and subject.

### Structured information

- Validate syntax and confirm markup matches user-visible content.
- Use the most specific relevant type supported by the target platform and context.
- Never add self-serving review markup, invented credentials, or invisible claims.

### Authority and local corroboration

- Verify review counts and profile status directly before using them externally.
- Record whether third-party evidence supports the same entity, location, services, and people.
- Distinguish an absent profile from a profile that was not located in the audit.

### Conversion and measurement

- Test forms, phone links, WhatsApp links, booking paths, and ordering routes without submitting live data unless approved.
- Record Search Console, Bing Webmaster, analytics, and CRM status when access exists.
- Do not claim commercial improvement without enquiry, conversion, or revenue evidence.

## Platform query tests

Prompt tests in ChatGPT, Gemini, Perplexity, Copilot, or Google AI features are snapshots, not deterministic rankings. Every test record must include:

- platform and product;
- account/location context where relevant;
- exact prompt;
- date and time;
- whether web search was active;
- cited URLs;
- result classification: cited, mentioned without citation, absent, or ambiguous.

One prompt result must not be presented as proof that a business is globally visible or invisible.

## Claim language

Use:

- `eligible for discovery`;
- `machine-readable business information`;
- `crawl and index readiness`;
- `observed in this dated test`;
- `diagnostic score`;
- `structured data can help platforms understand the page`.

Avoid:

- `guarantees AI rankings`;
- `invisible to every AI engine` without dated platform tests;
- `llms.txt tells all AI crawlers what to cite`;
- `schema makes a page appear in AI answers`;
- `indexed by every major platform` without platform evidence.

## Historical-audit handling

Historical audits remain useful evidence of what was observed at the time. Their causal or platform claims must be rechecked against this methodology before external reuse. The 2026 report may count recurring observed gaps from those audits, but it must not reuse unsupported statements about platform behaviour.

