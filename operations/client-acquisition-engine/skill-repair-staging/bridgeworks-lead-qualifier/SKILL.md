---
name: bridgeworks-lead-qualifier
description: Use when BridgeWorks must decide whether further GTM investment in a prospect is justified under canonical qualification-v1.
---

# BridgeWorks Lead Qualifier

Qualification answers: should BridgeWorks invest further GTM effort in this
prospect? Routing answers which service route and capability should handle it.
Never use GEO, website quality or another diagnostic family as an implicit proxy.

## Canonical ownership

The canonical model is `qualification-v1` under `operations/internal-gtm/`.
This native skill calls that implementation. The historical skill rubric remains
readable only through a labelled compatibility path and cannot own lifecycle
state.

## Workflow

1. Normalize identity and communication state.
2. Build an Evidence Auditor ledger.
3. Score all six components with evidence IDs, freshness, confidence and source
   provenance.
4. Evaluate hard gates separately from the numeric score and tier.
5. Return the smallest justified next action. Do not route or prepare outreach
   when actionability is blocked.

Run `scripts/score_prospect.py <input.json>`. Canonical input contains
`qualification_version`, `components`, `evidence`, `context` and `as_of`.

See [qualification-rubric.md](references/qualification-rubric.md) for the
versioned dimensions and thresholds.
