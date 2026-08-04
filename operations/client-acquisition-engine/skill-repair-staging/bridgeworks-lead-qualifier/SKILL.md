---
name: bridgeworks-lead-qualifier
description: Use when BridgeWorks must decide whether an inbound or outbound prospect merits research, a tailored 15-20 minute diagnostic, direct outreach, nurture, or rejection before spending bespoke delivery time.
---

# BridgeWorks Lead Qualifier

Qualify evidence, not enthusiasm. Separate company fit from current buying motion and never treat a weak website, a familiar geography, or a guessed budget as sufficient reason to produce free work.

## Workflow

1. Establish legitimacy and exclusions.
2. Gather only public or user-provided evidence.
3. Record evidence against the rubric in [references/qualification-rubric.md](references/qualification-rubric.md).
4. Run `scripts/score_prospect.py <input.json>` when a repeatable score is useful.
5. Apply the decision gates below.
6. Return a qualification record and the smallest justified next action.

## Evidence Rules

- Cite the URL, file, CRM record, or user statement behind every positive signal.
- Mark unknowns as unknown. Do not turn absence of evidence into a negative fact.
- Do not invent revenue, headcount, budget, technology, authority, or urgency.
- Geography supplies context and access. It does not add qualification points.
- A broken site is problem evidence, not buying intent.
- A named founder is accessible authority, not proof of budget.
- Funding, hiring, expansion, a technology migration, an active tender, or a public transformation initiative are change signals only when dated and relevant.
- Count independent signals. Multiple observations from one page count once unless they prove different categories.

## Decision Gates

Apply exclusions first.

| Status | Gate | Next action |
|---|---|---|
| `reject` | Illegitimate, prohibited, fundamentally outside the current ICP, or no plausible BridgeWorks outcome | Record reason; do not research further |
| `nurture` | Valid company but fewer than 3 verified signals or score below 45 | Add a dated watch trigger; no bespoke asset |
| `research` | 3 verified signals or score 45-64, with a material unknown that could change the decision | Spend at most 10 minutes resolving the named unknown |
| `audit-approved` | At least 4 verified signals, score 65+, a reachable buyer path, and one evidenced service route | Produce one 15-20 minute diagnostic or demo |
| `discovery-ready` | `audit-approved` plus explicit inbound interest, a reply, referral context, or a time-bound buying event | Invite a scoped discovery conversation |

The score informs the gate; it does not override exclusions, evidence count, buyer access, or service-route evidence.

## Free-Value Rule

Free value is earned by qualification. For `audit-approved` prospects:

- Diagnose one commercially meaningful problem.
- Show evidence specific to the company.
- Recommend three prioritized actions.
- Demonstrate one future-state artifact where useful.
- Leave enough implementation depth for a paid engagement.
- Do not default to a long generic audit, proposal, or price sheet.

The asset must be useful even if the prospect never buys, but it must also make BridgeWorks' relevant execution capability obvious.

## Output Contract

Return:

```yaml
company:
domain:
market:
source:
status:
score:
verified_signal_count:
confidence: low | medium | high
evidence:
  fit: []
  problem: []
  change: []
  capacity: []
  access: []
unknowns: []
exclusions_checked: []
primary_service_route:
secondary_service_route:
likely_buyer:
buyer_evidence:
recommended_asset:
asset_question:
next_action:
stop_condition:
crm_fields:
  qualification_status:
  qualification_score:
  qualification_evidence:
  service_route:
  next_action:
  next_action_date:
```

Use only one primary service route. If the evidence cannot support one, set the status to `research` or `nurture`.

## Handoff

For `audit-approved` and `discovery-ready`, pass this record to the BridgeWorks prospect router. For all other statuses, do not invoke audit, proposal, PDF, or outreach production skills.
