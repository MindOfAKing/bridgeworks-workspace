---
name: buyer-intelligence
description: Research publicly supportable BridgeWorks buyer-accessibility evidence, including problem owner, budget owner, decision maker, champion, blocker, named people, titles, contact routes, and attribution confidence. Use when qualification-v1 buyer_accessibility coverage is required or partial; never choose the service route.
---

# Buyer Intelligence

Produce bounded public-source research for the `buyer_accessibility` qualification
dimension. Prospect Router consumes the evidence after qualification; this
capability never chooses the route itself.

## Workflow

1. Accept canonical company identity, domain, problem statement, and the existing
   Evidence Auditor ledger.
2. Skip fresh approved buyer questions already answered.
3. Prefer owned team/contact pages, public filings, official announcements,
   verified professional profiles, and reputable event or association pages.
4. Distinguish problem owner, likely budget owner, decision maker, champion, and
   blocker. A person may hold more than one role only when evidence supports it.
5. Record exact person, role/title, contact route, evidence, confidence, and
   uncertainty. A generic form is a route, not proof of decision authority.
6. Validate the hand-back with `scripts/validate_result.py`.

## Output

Return `capability: buyer-intelligence`, prospect identity, attributed actors,
contact routes, evidence rows, confidence, unresolved questions, research status,
and `external_action_authorized: false`.

## Guardrails

- Do not invent a person, title, email pattern, or authority relationship.
- Do not expose personal contact data that is not a public business route.
- Do not consume enrichment credits, contact anyone, or write CRM data.
- Do not qualify, route, draft outreach, or select an offer.
