# The weekday 09:10 run, redesigned

Designed and tested 2026-08-11. **The live schedule is unchanged.** Cron
`10 9 * * 1-5` still runs `prospect_research_queue.py prepare` exactly as before.

## What it does today

`prospect_research_queue.eligible_rows` asks one question: which active-lane
companies in `prospect-source-current.csv` have not been researched yet. Anything
with research status `researched`, `in_research`, `held` or `rejected` is skipped.
The survivors are ranked by sector keywords and the top eight become a batch.

The job is structurally incapable of noticing that work already done has not moved.
A prospect that is researched, verified, outreach-ready and never contacted has
status `researched`, so it is filtered out on line 153 every single morning.

Existing work already includes two unresolved prepared batches and nine
approval-gated acquisition actions, so the daily decision cannot be based on the
new-row count alone.

## What it should do

Ask what the pipeline needs, then decide whether new supply is one of the answers.

The replacement is two pieces:

- `adapters/engine_snapshot.py` reads the acquisition engine and builds a snapshot.
  It is the only thing that knows where engine state lives. It writes nothing.
- `scripts/daily_objective.py` is a pure function over that snapshot. It returns one
  objective, its reason codes, its metrics, and whether supply is allowed.

Splitting them matters: the selector can be tested against synthetic states with no
filesystem, and the adapter can be swapped when state moves without touching the
decision logic.

## The evaluation order

Each check runs against real state. The first one that fires wins.

| Order | Objective | Fires when |
|---|---|---|
| 1 | `reconcile_unsafe_state` | Evidence is contradicted or contact state conflicts |
| 2 | `recover_overdue_research` | A batch has sat prepared or in-research beyond 2 days |
| 3 | `complete_missing_evidence` | A qualified untouched prospect is one source short |
| 4 | `complete_missing_buyer` | A qualified untouched prospect has no named decision maker |
| 5 | `refresh_stale_prospect` | A qualified untouched prospect was verified over 14 days ago |
| 6 | `advance_qualified_prospect` | A clean qualified untouched prospect exists |
| 7 | `surface_approval_decision` | Approvals are waiting and nothing above fired |
| 8 | `investigate_new_market_need` | A validated market gap exists but coverage is already sufficient |
| 9 | `generate_new_companies` | Every gate below is clear |

Unsafe state is first on purpose. A contradiction is not a low-priority tidy-up. It
means the system currently believes two incompatible things about a real company,
and every downstream decision is unsound until it is resolved.

## The supply gate

`generate_new_companies` fires only when all four are true:

1. qualified untouched prospects are below the coverage target;
2. the approval backlog is at or under its cap;
3. no unresolved research batch exists;
4. a priority market gap has been validated, not assumed.

Point 4 is the one that matters most. `validated_new_market_gap` defaults to false
in the snapshot adapter, so the gate is closed until a market-discovery run
positively establishes that a service route has no qualified depth. The system
cannot talk itself into prospecting because prospecting feels productive.

## A missing read blocks. It does not become zero.

If `approvals_waiting`, `prospects` or `unresolved_batches` cannot be read, the
selector returns `blocked_unverified` rather than treating the gap as an empty
queue. An unread connector is not an empty one. This is the failure mode that
would otherwise cause the system to generate supply on a morning when HubSpot or
Gmail was simply down.

## Result against real state, 2026-08-11

Run: `python operations/internal-gtm/adapters/engine_snapshot.py --as-of 2026-08-11 --select`

```
objective        recover_overdue_research
batch            2026-07-26-batch-01
prospects        budbed, eliezer-facility-management-company-lagos, go2flats,
                 homerun, marvel-homes-property-management
reason           prepared_or_in_research_over_2_days
supply allowed   false
```

Metrics behind that decision:

| Metric | Value |
|---|---|
| qualified untouched | 0 in the conservative shadow snapshot (target 4) |
| overdue research batches | 2 |
| approvals waiting | 9 |
| missing evidence | 0 |
| missing buyers | 0 |
| stale states | 0 |

The old job, run on the same morning, reports eight eligible rows and would prepare
a new batch of eight companies.

The new one says: two old batches (26 July and 1 August) remain unresolved and
nine acquisition actions are already waiting on approval. Recover existing work
before adding another research batch.

## Honest limits of this design

**Provisional tiers.** 39 of the 41 researched prospects have no internal-GTM
qualification score yet, so the snapshot maps engine readiness onto a tier: `ready`
to WARM, `hold` and `needs_more_evidence` to COLD. It never maps anything to HOT.
Every provisional row is labelled in `_provenance`. Premier FM scored 94 HOT once
the real rubric ran, so the bridge is conservative, but it is still a bridge.

**Contradiction detection is partial.** `evidence_contradicted` is only true for
prospects that have an internal-GTM run record, because that is where the evidence
ledger lives. Two of 41 have one today.

**Capacity numbers are decisions, not measurements.** The coverage target of 4 and
the approval cap of 3 are set in `engine_snapshot.CAPACITY`. They should be set
from Emmanuel's actual weekly capacity, not from a default.

## Cutover test before the schedule changes

The replacement runs in shadow first. For ten weekdays:

1. The live 09:10 job runs unchanged.
2. `engine_snapshot.py --select` runs alongside it and writes to `runs/daily-objective/`.
3. Each morning, record which objective each system chose.

The replacement is ready when all four hold:

- it never selected `generate_new_companies` on a day when a ready-and-uncontacted
  prospect existed;
- every `blocked_unverified` result matched a real connector or file failure;
- the objectives it chose were ones Emmanuel agreed were the right call;
- no run wrote to the acquisition engine, confirmed by mtime comparison.

Only then does the cron entry change, and Codex makes that change, not Claude Code.
