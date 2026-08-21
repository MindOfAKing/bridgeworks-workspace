---
name: commercial-intelligence
description: Research evidence for BridgeWorks qualification-v1 commercial_fit, including company scale, budget-capacity proxies, growth state, problem value, procurement complexity, and plausible engagement-size fit. Use when commercial-fit coverage is required or partial; never infer contract value without evidence.
---

# Commercial Intelligence

Produce bounded public-source research for the `commercial_fit` qualification
dimension. Do not score the prospect and do not choose a service route.

## Workflow

1. Accept canonical company identity, domain, problem evidence, market, and the
   existing Evidence Auditor ledger.
2. Skip fresh approved questions already answered.
3. Prefer owned company pages, filings and registries, official announcements,
   public job posts, public procurement records, and reputable business sources.
4. Research scale, budget-capacity proxies, locations, employees or customers
   where relevant, growth state, probable problem value, procurement complexity,
   and fit with BridgeWorks engagement size.
5. Label every claim `verified`, `observed`, `inferred`, or `unknown` with URL and
   observation date. State unresolved questions.
6. Validate the hand-back with `scripts/validate_result.py`.

## Output

Return `capability: commercial-intelligence`, prospect identity, evidence rows,
confidence, a supported commercial-value band or `unknown`, unresolved questions,
research status, and `external_action_authorized: false`.

## Guardrails

- Never fabricate revenue, budget, contract value, headcount, or procurement state.
- A proxy is not a fact about available budget. Label the inference.
- Use free public research first. Do not consume enrichment credits.
- Do not contact people, write CRM data, or mutate external systems.
