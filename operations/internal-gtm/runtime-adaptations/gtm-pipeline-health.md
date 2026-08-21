---
name: bridgeworks-gtm-pipeline-health
description: "Bounded internal GTM pipeline analysis: lifecycle reasoning, pipeline movement, handoff logic, stage health, next-action logic and commercial process analysis over canonical internal-GTM state. Use for GTM Director, Market and ICP Strategist, Reply Intelligence and Pipeline Manager work. Not a prospect-facing diagnostic."
---

# BridgeWorks GTM Pipeline Health

A narrow capability, deliberately. It covers the six RevOps functions the GTM roles
actually consume and nothing else. The full `revops` skill stays available in Claude
Code for consulting work on a client's revenue system. This is BridgeWorks looking
at its own pipeline.

## What this replaces and why

Five roles referenced `revops`, which is a 345-line general RevOps consulting skill
installed in Claude only. Codex-side runs of those roles had no capability at all.

Copying the whole skill into Codex would have carried lead scoring, CRM automation
workflows, deal desk processes and data-hygiene enrichment that none of the five
roles use, and two of those sections restate logic that already lives in
`operations/internal-gtm` as deterministic code.

Six functions were actually needed. They are below.

## Canonical state, not a second store

Read from internal-GTM. Never build a parallel pipeline record.

| Input | Path |
|---|---|
| Prospect snapshot | `operations/internal-gtm/adapters/engine_snapshot.py` |
| Qualification | `qualification-v1`, `gtm_core.score_qualification` |
| Lifecycle stages | `gtm_core.LIFECYCLE` |
| Outcome telemetry | `operations/internal-gtm/runs/telemetry/gtm-telemetry.jsonl` |
| Contacted companies | `operations/internal-gtm/scripts/contacted_companies.py` |

Deterministic arithmetic is already implemented. Do not re-derive a score, a tier,
a dedupe decision or a contacted count in prose. Read them.

## The six functions

### 1. Lifecycle reasoning

Map each prospect to its stage in `gtm_core.LIFECYCLE` and say what evidence
justifies that stage. A stage without evidence is a stage claim, not a stage.

`sent` and everything after it is approval-gated. If a record sits at `sent` with no
Gmail message id, that is a state error, not a pipeline position.

### 2. Pipeline movement

Compare stage occupancy between two telemetry snapshots. Report what moved, what
did not, and how long each stalled record has been where it is.

Never report movement you cannot evidence from two dated snapshots.

### 3. Handoff logic

For each stage boundary, name the owner before and after, the artifact that carries
the handoff, and the gate that must pass. Report boundaries where the artifact does
not exist. Those are the leaks.

### 4. Stage health

Per stage: count, median age, oldest record, and the blocking condition breakdown
from `qualification-v1` actionability. A stage that is large and old is not
necessarily unhealthy; a stage that is large and old *and* blocked on one repeated
condition is.

### 5. Next-action logic

One next action per prospect, derived from stage plus actionability:

| Condition | Next action |
|---|---|
| blocked on a hard gate | resolve that exact gate |
| qualification coverage below threshold | run the missing-dimension research capability |
| actionable, not contacted | prepare an approval packet |
| contacted, no reply classified | classify the reply |
| stale evidence | reverify the named sources |

Never propose an external action. Propose the internal work that makes the external
action approvable.

### 6. Commercial process analysis

Read outcome telemetry and report conversion by qualification dimension, tier,
service route and trigger type, each with its denominator. A rate with a zero
denominator is null, not zero.

Say plainly when there is not enough outcome data to support a conclusion. Today
there is not: no prospect has reached `sent` through this architecture.

## Output

```json
{
  "capability": "bridgeworks-gtm-pipeline-health",
  "as_of": "<YYYY-MM-DD>",
  "lifecycle": [{"stage": "<stage>", "count": 0, "median_age_days": 0, "oldest": "<prospect_id>"}],
  "movement": {"since": "<YYYY-MM-DD>", "advanced": [], "stalled": [], "regressed": []},
  "handoff_gaps": [{"boundary": "<from> -> <to>", "missing_artifact": "<name>"}],
  "stage_health": [{"stage": "<stage>", "blocking_conditions": {"<condition>": 0}}],
  "next_actions": [{"prospect_id": "<id>", "action": "<action>", "because": "<evidence>"}],
  "commercial_process": {"by_dimension": {}, "by_tier": {}, "insufficient_data": true},
  "external_action_authorized": false
}
```

## Guardrails

- Never invent a stage, a date, a count or a rate.
- Never propose or take an external action. This capability is read-only.
- A missing read blocks. An unread connector is not an empty one.
- Do not duplicate `revops`. If a question is about a client's revenue system rather
  than the BridgeWorks pipeline, that is `revops` in Claude Code, not this.
