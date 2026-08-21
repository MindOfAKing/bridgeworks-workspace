---
name: revops
description: Analyze BridgeWorks GTM lifecycle state, pipeline movement, handoffs, stage health, next actions, data hygiene, and commercial-process performance. Use when an internal GTM role needs bounded RevOps reasoning without CRM mutation or a full generic revenue-operations engagement.
---

# BridgeWorks RevOps

Use the shared `revops` capability identity. This Codex adaptation intentionally
covers only the functions consumed by Internal GTM roles.

## Workflow

1. Read canonical lifecycle definitions and the supplied prospect or pipeline state.
2. Check identity, stage requirements, next-action date, handoff completeness,
   approval state, and evidence freshness.
3. Identify invalid transitions, stalled records, missing owners, and overdue actions.
4. Recommend the smallest next action. Never advance a lifecycle stage merely
   because a numeric score exists.
5. Return observations, inferences, unresolved questions, and source provenance.

Use `scripts/analyze_pipeline.py` for deterministic stage-health checks. Read
`references/bounded-contract.md` for the exact role consumption map.

## Guardrails

- HubSpot remains the commercial source of truth, but this capability is read-only.
- Do not create workflows, tasks, CRM records, sends, or stage mutations.
- Do not own qualification arithmetic or service-route choice.
- Treat unknown state as unknown, never as zero or healthy.
- Do not use generic SaaS MQL benchmarks as BridgeWorks facts.
