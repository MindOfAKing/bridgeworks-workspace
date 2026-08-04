---
name: bridgeworks-geo-prospect-scan
description: Use when a qualified BridgeWorks prospect needs a 15-20 minute, evidence-led snapshot showing how clearly public web and AI-search systems can understand, corroborate, and cite the business before initial outreach.
---

# BridgeWorks GEO Prospect Scan

Create one useful AI-search proof asset without pretending that a small public sample is a full GEO audit. Every observation must point to a reviewed page, search result, validator result, or captured AI response.

## Entry Gate

Require:

- `audit-approved` or `discovery-ready` qualification;
- `content-visibility-demand` as the primary service route;
- a clear commercial buyer question;
- a reachable buyer path.

Otherwise stop and return the record to `bridgeworks-prospect-router`.

For an explicitly requested internal test, continue only as `internal-test-draft`. Place that label at the top and state that the artifact is not approved for prospect delivery.

## Timebox

1. Two minutes: define offer, audience, geography, and buyer question.
2. Five minutes: inspect the homepage and at most three high-value pages.
3. Three minutes: inspect brand search and third-party entity evidence.
4. Five minutes: run one controlled AI-search demonstration when access exists.
5. Five minutes: select three actions and package the snapshot.

Stop at 20 minutes.

## Evidence Rules

Collect:

- title, H1, meta description, and opening offer statement;
- service pages that answer distinct buyer questions;
- crawlable proof such as cases, quantified outcomes, credentials, dates, or original research;
- consistent company identity, geography, and leadership details;
- direct-answer blocks, FAQs, and internal links joining services to proof;
- visible structured-data types, only when actually inspected;
- brand search and one category-plus-audience or category-plus-market query;
- selected credible third-party corroboration;
- exact AI prompt, product surface, date, result, and citations when tested.

Say "not found in the pages reviewed," never "does not exist." Do not infer traffic, conversions, complete index coverage, citation frequency, or causation.

Maintain an inspection ledger for homepage fields, service pages, proof, credentials, FAQs, internal links, schema, brand search, category search, and AI test. Mark each `inspected`, `not found in inspected scope`, or `not inspected`. Never convert an uninspected item into a negative finding.

## AI Demonstration

Use one commercially relevant, non-branded question:

`Which [service category] firms help [buyer] with [problem] [in market, when known]?`

Capture:

- exact prompt;
- product/platform and date;
- approximate market context;
- cited, mentioned, omitted, or not tested;
- sources selected instead;
- one observable content or corroboration difference.

Label an executed result a reproducible observation, not an overall visibility measure. If live testing is unavailable, provide the exact recommended test, mark it unexecuted, and do not use the executed-result disclaimer.

## Output

Follow [references/one-page-template.md](references/one-page-template.md). Produce:

- `GEO-PROSPECT-SCAN-[company]-[date].md`;
- a branded PDF only when it improves the delivery artifact.

Use the active `pdf` or document capability for rendering and visual inspection. Do not use the broken `market-report-pdf` generator. Inspect the final PDF before handoff.

## Recommendations

Return exactly three actions. Each must include:

1. `Change`: a concrete page or evidence improvement.
2. `Why`: the observed ambiguity or gap it addresses.
3. `Start here`: the exact URL or asset.

Include one future-state demonstration, such as a rewritten entity-and-offer block, a stronger answer block, or the outline of a crawlable case study.

## Stop Conditions

Stop when:

- 20 minutes elapse;
- three useful evidence/action pairs exist;
- more than four pages are required;
- access requires login, paid credits, CAPTCHA, or restricted systems;
- the brand or offer cannot be identified confidently;
- a result cannot be reproduced;
- the claim would require guessing about traffic, rankings, citations, conversion, causality, or internal implementation.

State the limitation and omit the claim.

## Paid-Audit Boundary

Reserve for an engaged prospect:

- full crawl and indexability analysis;
- analytics, Search Console, CRM, or conversion evidence;
- researched query universe and competitor corpus;
- repeated multi-platform prompt tests;
- citation-frequency and source-pattern analysis;
- complete schema/entity/content architecture;
- implementation specifications, roadmap, and monitoring.

Never include a proposal, price, invented score, ROI estimate, or visibility guarantee in the initial scan.
