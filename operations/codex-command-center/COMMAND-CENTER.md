# BridgeWorks Codex Command Center

Updated: 2026-07-31
Owner: Emmanuel Ehigbai
Operator: Codex

## Purpose

This is the local operating contract for running BridgeWorks from Codex.
It is not a task list and it is not a handoff inbox.

Codex uses it to:

- reconcile business state across repositories, Codex tasks, Mission Control,
  GitHub, and connected systems
- identify the operating constraint, not just the loudest individual task
- keep verified outcomes available across separate Codex tasks
- preserve approval gates for consequential external actions
- maintain one current state and one append-only operating history

The live Emmanuel OS Command Center Google Sheet remains the shared canonical
business dashboard. These local files are the durable Codex control layer and
offline evidence surface.

## Files

- `OPERATING-STATE.md`: replaceable snapshot of what is true now
- `OPERATING-LOG.md`: append-only record of daily outcomes and unresolved loops

## Codex Task Structure

Use one pinned Codex task named `BridgeWorks Command Center` for:

- morning operating review
- founder decisions
- approval pressure
- cross-project reconciliation
- end-of-day closeout

Use separate Codex tasks for distinct outcomes such as a client closeout,
website build, content restart, automation repair, or proposal. Keep detailed
implementation logs inside those tasks. Return only verified outcomes,
decisions, blockers, and durable source links to the Command Center.

Do not use one giant task for every implementation detail. Do not assume a
separate task's transcript is shared automatically. Write durable facts here or
in the relevant canonical system.

## Evidence Classes

Every operating run must separate:

- `Observed`: directly supported by a current file, connector result, task
  result, or system record
- `Inferred`: likely conclusion that still lacks direct confirmation
- `Drafted`: prepared but not executed
- `Executed`: confirmed change with a receipt or verifiable result

Newer, more direct evidence overrides older summaries. A draft, brief, task
title, or another model's statement is never proof by itself.

## Source Priority

Use the narrowest current source that owns the fact:

1. Live system that owns the record
2. Current Mission Control state and event log
3. Current repository artifact or verified session receipt
4. Recent Codex task result
5. Current operating snapshot
6. Imported brief or another model's summary
7. Historical files

Examples:

- commercial status: HubSpot or the current approved pipeline system
- execution status: ClickUp or the current approved execution system
- prospect approvals: Mission Control approval queue
- code and deployment: repository, deployment provider, and verification result
- payments: invoice, bank or payment evidence, then reconciliation record
- commitments: Google Calendar
- correspondence: Gmail

## Daily Operating Cycle

### Morning

1. Read `OPERATING-STATE.md` and the newest log entry.
2. Collect only changed or decision-relevant evidence.
3. Review recent BridgeWorks Codex tasks for verified outcomes.
4. Reconcile conflicts and stale records.
5. Name the current operating constraint.
6. Set no more than three operating priorities.
7. Surface exact approvals and decisions needed from Emmanuel.

### During the day

Run distinct outcomes in separate tasks. For difficult work, use `/plan`.
Ask for subagents explicitly when independent research or verification can run
in parallel. Keep write-heavy work on the same files in one task.

### End of day

1. Review completed Codex tasks and changed files.
2. Verify completion against evidence.
3. Update `OPERATING-STATE.md`.
4. Append one dated entry to `OPERATING-LOG.md`.
5. Carry forward only open loops with an owner and next action.

## Approval Boundary

Codex may inspect, reconcile, draft, organize local operating records, and
prepare exact actions.

Emmanuel must explicitly approve the exact action before Codex:

- sends email or direct messages
- publishes content
- changes another person's calendar
- starts outreach or consumes enrichment credits
- pays, purchases, or starts billable usage
- changes production systems, deployments, domains, or live client data
- commits or pushes unless that exact repository action was approved
- deletes files, records, tasks, or healthy integrations

## Commands Emmanuel Can Use

- `Run BridgeWorks daily operations.`
- `What is the operating constraint today?`
- `Reconcile my recent BridgeWorks Codex tasks.`
- `Show only decisions and approvals that need me.`
- `Execute priority one, but stop at external approval gates.`
- `Run end-of-day closeout and update the operating state.`
- `Use subagents to investigate these independent operating lanes.`

