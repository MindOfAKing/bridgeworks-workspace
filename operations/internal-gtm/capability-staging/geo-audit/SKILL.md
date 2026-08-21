---
name: geo-audit
description: Orchestrate a full BridgeWorks GEO audit across AI citability, brand authority, content E-E-A-T, technical GEO, schema, and platform readiness. Use for a paid or deep GEO diagnostic that must delegate to the five governed GEO specialists and return one structured geo-audit result.
---

# GEO Audit

Preserve the canonical `geo-audit` methodology. This is the Codex runtime
adaptation of the fuller Claude orchestration contract, not a competing audit.

## Workflow

1. Confirm the URL, scope, page cap, and output date. Default to 50 pages maximum.
2. Read and respect `robots.txt`. Use read-only public research and wait between
   repeated page fetches.
3. Collect one shared reconnaissance packet: canonical URLs, raw HTML where
   required, page text, headers, sitemap, robots rules, and business type.
4. Invoke exactly these governed specialists with the same packet:
   `agent-geo-ai-visibility`, `agent-geo-platform-analysis`,
   `agent-geo-technical`, `agent-geo-content`, and `agent-geo-schema`.
5. Require each specialist to separate observed evidence from inference and return
   sources, findings, scores, confidence, gaps, and blocked checks.
6. Normalize the five hand-backs with `scripts/aggregate_geo.py`.
7. Return the structured result defined in `references/specialist-contract.md`.
   A narrative report may be derived from it, but never replaces it.

## Guardrails

- Do not send, publish, deploy, mutate a website, or write to CRM systems.
- Do not claim live answer-engine visibility when a platform could not be checked.
- Static Core Web Vitals observations are risk estimates, not field measurements.
- Preserve one capability identity and the existing six weighted GEO categories.
- Do not depend on Claude Code. Codex must be able to run the full chain itself.
- Do not create or invoke ungoverned specialists.

## Scoring

Aggregate six 0-100 categories:

- AI citability: 25%
- brand authority: 20%
- content E-E-A-T: 20%
- technical GEO: 15%
- schema and structured data: 10%
- platform optimization: 10%

Run:

`python scripts/aggregate_geo.py input.json`

Read `references/specialist-contract.md` before preparing specialist hand-offs.
