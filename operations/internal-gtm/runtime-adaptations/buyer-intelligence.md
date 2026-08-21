---
name: bridgeworks-buyer-intelligence
description: "Collect public evidence for the buyer_accessibility qualification dimension: problem owner, budget owner, decision maker, champion and blocker, with an exact person, role, contact route and the evidence behind each attribution. Use when qualification-v1 reports buyer_accessibility as missing research. Outputs uncertainty explicitly and never chooses a service route."
---

# Buyer Intelligence

A bounded research capability. It answers one question: who inside this company can
say yes, and can we reach them lawfully.

It collects evidence about people. It does not qualify, does not route, and does not
contact anyone.

## When it runs

`qualification-v1` reports `buyer_accessibility` with `research_status: required` or
`partial`, or the daily objective selects `complete_missing_buyer`.

It does not run when `buyer_accessibility` already has fresh approved evidence.

## Roles to establish

Five distinct roles. One person can hold more than one. Often nobody is findable
for some of them, and saying so is the correct answer.

| Role | What it means | Typical evidence |
|---|---|---|
| Problem owner | lives with the problem daily | a job posting naming the responsibility, a team page, a published process owner |
| Budget owner | can release money | title with commercial authority, registry directorship, published signing authority |
| Decision maker | signs | founder, managing director, or a named function head where the spend is small |
| Champion | would argue for it internally | someone publicly writing or speaking about the exact problem |
| Blocker | can stop it | incumbent supplier, in-house team doing the same work, procurement or compliance function |

## Evidence rules

Every attribution needs a source URL and an access date, the same as any other
evidence. A name from a directory with no date is `inferred`, and inferred does not
score.

**Say what you do not know.** A record with a named decision maker and no budget
owner is a better record than one that guesses the budget owner. Use
`attribution_confidence` per role and leave the ones you cannot support as null.

Do not compile a personal profile. Collect the role, the public professional
identity and the public contact route for the business. Nothing else.

## Contact route

Prefer, in this order:

1. A published role-specific business address on the company's own site.
2. A published general business address on the company's own site.
3. A published contact form on the company's own site.
4. A public professional profile, for research only, never for a message.

A personal address found anywhere else is not a contact route. Record `null`.

## Output

```json
{
  "capability": "bridgeworks-buyer-intelligence",
  "prospect_id": "<id>",
  "as_of": "<YYYY-MM-DD>",
  "roles": {
    "problem_owner": {"person": null, "title": null, "evidence_id": null, "attribution_confidence": "none"},
    "budget_owner": {"person": null, "title": null, "evidence_id": null, "attribution_confidence": "none"},
    "decision_maker": {"person": null, "title": null, "evidence_id": null, "attribution_confidence": "none"},
    "champion": {"person": null, "title": null, "evidence_id": null, "attribution_confidence": "none"},
    "blocker": {"person": null, "title": null, "evidence_id": null, "attribution_confidence": "none"}
  },
  "contact_route": {
    "destination": null,
    "destination_type": "role_specific | general | form | none",
    "source": null,
    "lawful_basis_note": "public business contact route published by the company"
  },
  "findings": [
    {
      "id": "bi-<n>",
      "category": "buyer_accessibility",
      "claim_key": "<exact proposition, e.g. decision_maker_identity>",
      "claim": "<one factual sentence>",
      "value": "<machine-readable value>",
      "severity": "none",
      "source": "<exact URL fetched>",
      "observed_at": "<YYYY-MM-DD>",
      "status": "verified | observed | inferred"
    }
  ],
  "unresolved_questions": ["<which role could not be established and what would settle it>"],
  "external_action_authorized": false
}
```

## Guardrails

- Never message, connect with, follow or otherwise contact anyone.
- Never infer a personal email address from a naming pattern. A guessed address is
  a fabrication, and sending to one is a deliverability and legal risk.
- Two sources naming different decision makers is a contradiction. Declare a shared
  `claim_key` so the Evidence Auditor catches it. Do not pick one.
- **Do not choose the service route.** The Prospect Router consumes this evidence
  and decides. Buyer Intelligence supplies who, not what to sell them.
