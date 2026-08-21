# Superseded logic

Marked 2026-08-11. Nothing here is deleted, disabled, or unscheduled.

`SUPERSEDED_AFTER_MIGRATION` means: the new architecture covers this behaviour, the
old implementation still runs, and the switch happens in Phase 3 after the
replacement passes tests against real data.

Five files carry the marker in place. This file is the canonical record.

## 1. Sector-weighted prospect ranking

**File:** `operations/client-acquisition-engine/scripts/prospect_research_queue.py`, `rank_row`

The ranker adds 20 points for "property" or "facility" in the row text, 15 for
"cleaning", 10 for "dental" or "clinic". It subtracts for "benchmark only",
"watchlist only", "later lane" and "high-scale".

The 2026-08-01 qualifier repair explicitly removed geography scoring from
`bridgeworks-lead-qualifier` because it biased Budapest, CEE and Nigeria. The same
class of bias survived here, one layer up, as sector keywords. A prospect's sector
is not evidence about that prospect.

**Superseded by:** `gtm_core.score_qualification`. Its five inputs are route fit,
trigger freshness, evidence quality, reachability and gap severity. None of them
reads the sector or the country.

**Keep:** the negative filters. "benchmark only" and "watchlist only" are lane
decisions Emmanuel made, not bias.

## 2. Refill-first daily selection

**File:** `operations/client-acquisition-engine/scripts/prospect_research_queue.py`, `eligible_rows` and `prepare`

`eligible_rows` answers one question: which active-lane companies have not been
researched yet. Anything already `researched`, `in_research`, `held` or `rejected`
is skipped forever. So the 09:10 job can only ever move forward into new supply.
A prospect that is researched, verified, ready and never contacted is invisible to
it, because its research status is `researched`.

Today that describes nine prospects.

**Superseded by:** `operations/internal-gtm/scripts/daily_objective.py` plus
`operations/internal-gtm/adapters/engine_snapshot.py`. Generating new companies is
one of eight possible objectives and it is gated behind coverage, approval backlog,
unresolved research, and a validated market gap.

## 3. Qualification-rubric conflict — resolved

**File:** `operations/client-acquisition-engine/skill-repair-staging/bridgeworks-lead-qualifier/scripts/score_prospect.py`

Weights: fit 25, active_change 25, problem_evidence 20, capacity 15, buyer_access 15.
Gates at 65 points plus four verified signals plus a buyer path plus an evidenced
service route. It separates `nurture`, `research`, `audit-approved` and
`discovery-ready`.

The historical implementation remains useful source material, but no longer owns
qualification state.

**Resolved 2026-08-11:** `qualification-v1` in internal GTM is canonical. The native
Codex entry point delegates canonical inputs to `gtm_core.score_qualification` and
labels old inputs compatibility-only with `requires_qualification_v1_rescore: true`.
No legacy status is translated into a canonical tier.

## 4. Second route registry

**File:** `operations/client-acquisition-engine/skill-repair-staging/bridgeworks-prospect-router/scripts/validate_route.py`

`ROUTES` is a hardcoded set of the five service-route ids. It also revealed a real
naming split: this file and the live run artifacts use `digital-platforms-brand`,
and the internal-GTM package originally used `digital-platforms`.

**Resolved 2026-08-11:** internal-GTM was changed to `digital-platforms-brand` to
match the established id. The older name never reached a run record.

**Superseded by:** `operations/internal-gtm/service-routes.yaml`, which holds the
five routes, their gap-category mappings, wedges and proof assets in one place,
verified against the deployed site.

**Note the different job:** `validate_route.py` validates a route plan it is handed.
It does not choose a route. `gtm_core.select_service_route` chooses one from
evidence. The validator's production ceilings, four-pass limit and overproduction
check have no equivalent in internal-GTM yet and should be ported, not dropped.

## 5. Staged capability-registry copy

**File:** `operations/client-acquisition-engine/skill-repair-staging/bridgeworks-prospect-router/references/capability-registry.md`

A capability registry in prose. Its activation note is now stale: the five GEO
specialists are installed as native Codex skills under `~/.codex/skills/`, while
the aggregate `geo-audit` contract remains registered at the Claude path. Phase 2
used the registered aggregate contract and the five native subordinate skills;
it did not reproduce their logic in internal-GTM.

**Superseded after migration by:** `skill-governance/capability-registry.yaml`
read through `operations/internal-gtm/scripts/capability_loader.py`. Until the
canonical registry is regenerated and the Codex installations resolve there,
this is `BLOCKED_CANONICAL_DECISION`, not a safe deletion candidate.

**The real fix is upstream.** The canonical registry was generated 2026-07-25 and
holds 74 skills with only three Codex installations recorded. The live estate is 74
Claude skills and 63 Codex skills. Every skill authored on 2026-08-01, including
`bridgeworks-lead-qualifier`, `bridgeworks-prospect-router` and the three bounded
scans, is invisible to the canonical registry. That is why a second registry got
written. Regenerating the canonical registry is Phase 3 step 1.

## 6. Evidence readiness in prose

**File:** `operations/client-acquisition-engine/scripts/prospect_review_queue.py` and `research/prospect-operations/README.md`

The rule is written correctly: `verified` establishes identity and route but does
not authorize outreach; an outreach-ready record also needs a commercial gap, a
proof choice, a destination, exact copy, a next action and risk notes.

It is enforced by a validator over a result record, and the evidence itself carries
one flat `status` field per prospect.

**Superseded by:** the six-class evidence ledger in `gtm_core.build_evidence_ledger`,
which classifies each claim separately and downgrades but never upgrades. No source
becomes `unknown`. Over 180 days becomes `stale`. Two approved claims that disagree
on the same proposition both become `contradicted`. `build_outreach_packet` then
raises if a packet cites anything outside the approved set.

**Not superseded:** the review packet surface, `review/prospect-review-state.json`,
and the append-only event log stay canonical. Internal-GTM must feed them, not
replace them.

## 7. The 09:10 schedule entry

**File:** `operations/client-acquisition-engine/orchestrator-schedule.json`, schedule `prospect-evidence-weekday`

Cron `10 9 * * 1-5`. Purpose: "verify evidence, dedupe, score, and prepare prospect
review packets".

The schedule is correct. The purpose is the thing being replaced.

**Not changed.** The cron entry is untouched and still runs. See
`daily-objective-redesign.md` for the replacement behaviour and its cutover test.

## Explicitly not superseded

These are the engine's best assets and the new architecture depends on them.

| Component | Why it stays |
|---|---|
| The research result schema | Sourced URLs with access dates, owned domain, conversion route, decision maker, observations, gap, readiness. Nothing in internal-GTM produces this. |
| `research/prospect-operations/results/` | Seven files of real verified evidence. This is the corpus. |
| The approval packet surface | Fourteen packets and a durable review state with an event log. Internal-GTM stops at `awaiting_approval` and hands off here. |
| The three bounded scan skills | Initial-contact diagnostics sized for outreach. `geo-audit` is paid-delivery depth. Both have a place and the router should pick between them. |
| `scripts/outreach_engine.py` | Gmail evidence reconciliation and the canonical register. An adapter, and a good one. |
| The three live-test runs | `appinio`, `silver-lining`, `bridgeworks-dogfood`. The regression corpus for the new architecture. |
