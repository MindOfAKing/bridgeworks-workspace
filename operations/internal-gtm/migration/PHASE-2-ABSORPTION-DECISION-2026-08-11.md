# Internal GTM Phase 2 — acquisition-engine absorption decision

Completed 2026-08-11 for Emmanuel review.

## Decision

`operations/client-acquisition-engine/` remains the active GTM migration source.
Absorb its useful data, evidence, workflows, and history into the internal-GTM
architecture through verified adapters. Retire only duplicated control or state
surfaces after parity, shadow operation, rollback verification, and Emmanuel's
explicit approval. No bulk move was performed.

## 1. Functional inventory

The initial physical observation contained 204 regular files, including five
`.pyc` cache files. The stable meaningful-component inventory excludes ephemeral
`__pycache__` churn and contains 199 files totalling 8,829,368 bytes. The external
`node_modules` junction under generated output is also excluded and was not
traversed.

| Function | Files |
|---|---:|
| canonical prospect data | 5 |
| research evidence | 17 |
| market/ICP logic | 4 |
| trigger discovery | 8 |
| proof inventory | 11 |
| qualification | 4 |
| routing | 6 |
| diagnostic selection | 4 |
| outreach preparation | 18 |
| approval packet | 14 |
| automation/scheduling | 8 |
| reporting | 13 |
| historical artifact | 25 |
| duplicate | 19 |
| generated/transient output | 43 |
| **Total** | **199** |

Exact meaningful source paths, hashes, target areas, dispositions, and provenance labels are
in `phase-2/acquisition-engine-file-inventory-2026-08-11.csv`. The measured summary
is `phase-2/acquisition-engine-inventory-summary-2026-08-11.json`. Cache files are
excluded by rule because verification creates new ones and would otherwise make
the dated inventory non-deterministic.

Important reconciliation findings:

- the source queue has 100 rows, the generated canonical register 60, research
  state 50, and review state 41;
- the generated register says `source_reconciled: false` and is stale;
- the research state's stored source hash does not match the current source CSV;
- the service-line list has 26 accounts while its README says 25;
- 19 files in `skill-repair-staging/` are byte-identical to installed native Codex
  skills;
- 22 non-binary files embed machine-specific absolute paths;
- source Markdown remains canonical over derivative PDF/PNG renderings.

## 2. Source-to-target migration map

The 34-component map is in `acquisition-engine-map.json`; the exact per-file map
is the Phase 2 CSV. Target ownership is:

| Target | Source responsibilities absorbed |
|---|---|
| control | schedules, objectives, operating policy, state reconciliation |
| acquisition | source queue, market/ICP logic, trigger imports and discovery |
| evidence | research results, source dates, claim status, proof inventories |
| opportunities | identity, qualification, route, diagnostic, offer and lifecycle |
| approvals | immutable packet snapshots, exact destination/copy digest, event log |
| learning | reports, scorecards, historical runs, event lineage and migration receipts |
| adapters | queue scripts, browser/search, CRM/mail bridges, renderers and staging tools |

Historical artifacts are retained as read-only learning/provenance. Generated
artifacts are regenerated or referenced by hash unless the source is unavailable.

## 3. Superseded logic

The detailed disposition is in `superseded-logic.md`. Safe eventual replacements
include sector-weighted prospect ranking, refill-first daily selection, flat
evidence readiness, and the staged registry copy. The schedule itself, research
corpus, approval state/event log, bounded scans, outreach reconciliation adapter,
and live-test regression corpus are explicitly retained.

Three conflicts are not marked superseded because they need a canonical decision:

- native Lead Qualifier versus migration-slice scoring;
- callable `bridgeworks-revenue-system-scan` versus its absence from the canonical
  capability registry;
- registered aggregate `geo-audit` at the Claude path versus five native Codex GEO
  subordinate skills and a stale staged activation note.

## 4. Revised 09:10 workflow

The live weekday schedule remains unchanged. The replacement selector evaluates,
in order: unsafe contradictions/contact state, overdue prepared research, missing
evidence, missing buyer, stale qualified state, the strongest qualified untouched
prospect, approvals, validated market need, and finally new supply.

New-company discovery is allowed only when qualified untouched coverage is below
target, no unresolved batch can restore it, approvals are under their cap, and a
priority-market gap has been validated. Missing connector/state reads return
`blocked_unverified`, never zero.

The real 2026-08-11 shadow snapshot selected
`recover_overdue_research` for `2026-07-26-batch-01` and blocked new supply. The
source held two overdue batches and nine waiting approvals while the old workflow
still saw eight eligible new rows. Design and cutover gates are in
`daily-objective-redesign.md`; the machine-readable shadow result is under
`phase-2/workflow/`.

## 5. Real-prospect comparison

Appinio was refreshed and compared end to end. The new result normalizes the
domain, reuses only current cited evidence, preserves the old 90/95 score conflict,
routes to Execution & Operating Systems, applies the native revenue-system rubric,
and blocks approval because no exact destination exists. It does not reuse old
drafts as approved copy.

## 6. GEO test

Tilz Prosperitas is a legitimate GEO hypothesis because it is expanding across
international markets. The registered `geo-audit` contract and all five native
Codex subordinate skills were used. Technical GEO scored 86/100; content/E-E-A-T
was provisionally weak; the answer-engine and platform passes were incomplete.
The aggregate therefore remained unscored and the lifecycle stopped at
`diagnostic_selected`. No GEO defect, proof claim, offer, or packet was fabricated.

## 7. Non-GEO test

Appinio routed to `execution-operating-systems` with a bounded operating-cadence /
revenue-system hypothesis. It did not route to GEO. This passes the architectural
test while exposing the registry gap for the native revenue-system scan and the
weak-fit proof currently selected for that route.

Full old/new and GEO results are in `phase-2-test-results.md`.

## 8. Phase 3 plan

The exact sequenced plan, owners, verification, dependencies, rollback points, and
non-actions are in `PHASE-3-PLAN.md`. The first gates are registry regeneration and
diff review, one qualification contract, ten-weekday daily-objective shadowing,
backlog scoring, a single approval-surface adapter, a five-list dedupe report,
production-ceiling porting, then an explicitly approved 09:10 cutover.

## Tool routing

`adapters/tool-adapters.yaml` keeps public web, browser, search, Places,
Firecrawl, SerpAPI, and ODS local search independent from capabilities and business
truth. An adapter is configured only for a demonstrated role need; every result
must enter the evidence ledger with source and observation date.

## Phase 2 stop condition

Met. No deletion, shutdown, schedule replacement, outreach, CRM mutation,
credential revocation, commit, or push occurred. Phase 3 has not started.
