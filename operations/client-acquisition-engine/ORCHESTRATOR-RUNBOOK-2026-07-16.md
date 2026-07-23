# BridgeWorks Acquisition Orchestrator

Status: designed, approval-gated, not activated
Owner: Emmanuel Ehigbai
Timezone: Europe/Budapest
Scope: client acquisition, authority content, proof packaging, and operating reports

## Purpose

Run the BridgeWorks acquisition loop with two trigger types:

1. Scheduled runs keep research, content, pipeline hygiene, reporting, and review queues moving.
2. Event-driven runs react to new replies, approvals, source evidence, failures, and browser execution results.

The orchestrator is the coordinator. Specialist workers do the narrow work. HubSpot remains the commercial source of truth, ClickUp remains the execution source of truth, Google Drive remains the canonical file store, and the mobile outbox remains the reading surface.

## Operating boundary

The orchestrator may run unattended for:

- read-only research and connection checks
- deduplication and evidence classification
- draft creation and review packets
- local asset validation and manifest updates
- internal task, log, and report updates
- mobile summaries and health alerts

It must stop at an approval gate before:

- sending email or direct messages
- publishing or deleting social content
- uploading files to a public channel
- changing a live website, deployment, DNS, or client data
- consuming paid prospect-enrichment credits
- creating calendar events with other people

An approval authorizes one exact action or one explicitly named batch. It does not authorize a wider campaign.

## Run lifecycle

```text
triggered -> observed -> oriented -> validated -> drafted -> awaiting_approval -> approved -> executed -> verified
```

Any stage may become `blocked` with a reason and next safe action. A run may not skip validation or verification.

## OODA contract

### Observe

- Read only the sources needed for the trigger.
- Start from the last successful run memory.
- Check HubSpot before adding a prospect.
- Read reviewed proof from the canonical `01 Acquisition and Authority` Drive section.
- Treat named-client originals as private evidence only.

### Orient

- Separate `observed`, `inferred`, `drafted`, and `executed` facts.
- Map each prospect to a lane, commercial gap, proof module, route, and next action.
- Reject unsupported ratings, review counts, outcomes, testimonials, or automation claims.
- Apply the current offer ladder. Do not revive the retired free-digital-presence-audit wording.

### Decide

- Continue automatically when the work is internal, reversible, and evidence-backed.
- Create an approval item when an external action is ready.
- Create a blocker when a route, identity, source, or approval is missing.
- Do not broaden a batch because a similar item looks eligible.

### Act

- Write the smallest idempotent update to the canonical system.
- Save drafts and assets with stable IDs and source links.
- Write a run log and mobile summary even when no action is needed.
- After an approved browser action, record the URL, timestamp, account, asset hash, and result.

## Scheduled cadence

| Time | Run | Automatic result |
|---|---|---|
| Every weekday 09:10 | Prospect evidence pass | Verify public evidence, dedupe against HubSpot, score gaps, and create a review packet. No contact is sent. |
| Every weekday 12:30 | Reply and approval watcher | Check for new replies, approvals, expiring approvals, and failed runs. Create only the next safe queue items. |
| Every weekday 17:30 | Execution and health check | Reconcile completed internal work, browser results, stale queues, and exceptions. Write a mobile summary. |
| Sunday 17:00 | Weekly acquisition control run | Review pipeline, content, proof, Oliviks gates, scorecard, and next-week approval queue. |
| Monday 09:00 | Weekly dispatch preparation | Convert the approved weekly queue into exact channel bundles and ClickUp actions. Publishing remains gated. |

The weekday 09:10 research run preserves the existing operating cadence. The other times are the proposed orchestrator cadence and should be activated only after the runtime connection is confirmed.

## Event-driven triggers

| Event | Worker | Result |
|---|---|---|
| New Gmail reply | Reply triage | Classify reply, link to HubSpot, prepare a discovery-call or follow-up task, and alert mobile. |
| New HubSpot company/contact or deal change | Pipeline reconciler | Deduplicate, validate stage and next action, and surface stale or high-fit records. |
| New approved asset or proof source | Content/proof packager | Refresh relevant drafts, create variants, and queue only affected outputs. |
| Emmanuel approves an item | Approval executor | Execute only the named action, then verify and log it. |
| Chrome upload or publish result | Browser result ingester | Record account, post URL, asset hash, and failure details. |
| Connector or worker failure | Health sentinel | Retry once where safe, then create a blocker and mobile alert. |
| Oliviks completion gate changes | Delivery-to-proof worker | Refresh case-study eligibility and prevent premature public claims. |

Event triggers may be implemented as webhooks where available or as a short polling adapter. They must not become a second source of truth.

## Weekly acquisition loop

The orchestrator aims at the existing starting cadence:

- 25 researched prospects added or refreshed
- 15 highly relevant first-contact drafts
- 10 follow-up candidates
- 5 relationship touches
- 2 personalized mini-observations or scan excerpts
- 1 referral request candidate

These are queue targets, not permission to send. The system may report a shortfall instead of manufacturing activity.

## Mobile control surface

Every run writes a short item to `LLM Daily Outbox` and, when required, an item to `Approval Queue`. Each item includes an exact command.

Supported commands:

```text
brief me
show acquisition status
show approval queue
approve outreach [item_id]
approve publish [item_id]
approve batch [batch_id]
hold [item_id]
pause acquisition
resume acquisition
explain run [run_id]
```

`approve outreach`, `approve publish`, and `approve batch` are explicit external-action commands. `pause acquisition` prevents new external-action queue items while allowing health checks and logging to continue.

## Run log contract

Each run records:

| Field | Requirement |
|---|---|
| `run_id` | Stable ID, for example `BW-AO-20260716-0910-001`. |
| `trigger` | Schedule name or event name. |
| `scope` | Exact lanes, records, channels, and folders read. |
| `started_at`, `finished_at` | Europe/Budapest timestamps. |
| `observed` | Evidence read and source links. |
| `inferred` | Judgments clearly labeled as inference. |
| `drafted` | Files, tasks, and approval items created. |
| `executed` | External actions actually completed, or `none`. |
| `exceptions` | Missing data, failed checks, or stale configuration. |
| `status` | `verified`, `awaiting_approval`, `blocked`, or `failed`. |
| `next_run` | Expected next schedule or event condition. |

No run may report a draft as sent, a prepared browser action as published, or a local file as uploaded.

## Failure and recovery

- Search before create. Update by stable ID where one exists.
- Retry a transient read once. Do not loop on rate limits or auth failures.
- Preserve conflicting evidence and mark it `Needs check`.
- If a connector is unavailable, write the local run log and a mobile blocker.
- If an approval expires or its source hash changes, return it to review.
- If the same failure repeats across three runs, pause that worker and surface the blocker.

## Activation checklist

Before activation, confirm:

- one persistent scheduler or workflow host
- active Composio connections for the exact worker set
- a webhook or polling route for Gmail replies and approvals
- access to the canonical Drive folder and mobile outbox
- an idempotency store for run IDs and action IDs
- a dry run that produces logs without sending or publishing
- a successful mobile brief and approval-queue test

The existing n8n workflow remains inactive until its retired offer wording and write nodes are reconciled against this contract.
