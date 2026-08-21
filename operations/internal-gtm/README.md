# BridgeWorks Internal GTM

Merge target: `MindOfAKing/bridgeworks-workspace/operations/internal-gtm/`

## Rule
Business roles are stable. Skills, agents, tools, models, and APIs are replaceable implementations.

The existing canonical capability registry remains:
`skill-governance/capability-registry.yaml`

Do not create another capability registry.

## Runtime ownership
- Codex: orchestration, scheduling, migrations, execution, browser-driven approved actions.
- Claude Code: capability engineering, code, schemas, tests, skill/agent creation and adaptation.
- Cowork/Claude: research, synthesis, editorial/commercial review.
- ODS/Qwen: bounded low-cost preprocessing only.
- Emmanuel: approval authority.

## GTM lifecycle
market_hypothesis -> account_discovered -> evidence_collected -> qualified -> routed -> diagnostic_selected -> diagnostic_complete -> offer_selected -> outreach_prepared -> awaiting_approval -> sent -> replied -> opportunity -> discovery -> proposal -> won|lost|nurture

## First vertical slice
website_url -> capability router -> geo-audit -> structured diagnostic -> Evidence Auditor -> Prospect Router -> Offer Strategist -> outreach-preparation packet

## Second vertical slice
market_or_sector_hypothesis -> Trigger Scout -> candidate companies -> deterministic dedupe -> Lead Qualifier -> capability router -> ranked research queue

## Existing capabilities to reuse
geo-audit, geo-*, client-audit, lead-qualifier, revops, market-*, competitive-research, discovery-call-prep, post-call-followup, engagement-architect, council, skill-creator, find-skills, writing-skills, bridgeworks-operating-system.

New capabilities must pass the existing quarantine/intake/security/overlap/pilot workflow.

## Verify and run

```powershell
python operations/internal-gtm/scripts/capability_loader.py
python -m unittest discover -s operations/internal-gtm/tests -p "test_*.py" -v
python operations/internal-gtm/scripts/run_geo_slice.py --input operations/internal-gtm/examples/geo-slice-input-no-diagnostic.json --as-of 2026-08-11
python operations/internal-gtm/scripts/run_geo_slice.py --input operations/internal-gtm/examples/geo-slice-input.json --as-of 2026-08-11 --out operations/internal-gtm/runs
python operations/internal-gtm/scripts/run_market_discovery.py --input operations/internal-gtm/examples/market-discovery-input.json --as-of 2026-08-11 --out operations/internal-gtm/runs
```

The fixtures are synthetic. Runners never send outreach or mutate external systems.

`capability_loader.py check` fails if any role points at a capability that does
not exist, or if a second capability registry appears under this folder. All 18
capabilities referenced by the 16 roles resolved against the live registry on
2026-08-11, so nothing had to be invented or sent through intake.

## What is deterministic and what is not

Deterministic code, no model call:

- company and domain normalization
- exact dedupe and merge, order-independent
- evidence classification and contradiction detection
- the qualification rubric arithmetic
- service-route selection and offer wedge selection
- lifecycle transitions and the approval digest

Model work, handed back as an explicit capability call request:

- running geo-audit or client-audit
- trigger and market research
- ambiguous entity resolution
- outreach copy

`sent` and every stage after it is approval-gated. `gtm_core.advance()` raises if
code tries to reach those stages, so no run can walk itself into a send.

## Evidence rules

Classes are `verified`, `observed`, `inferred`, `stale`, `contradicted`, `unknown`.
Only `verified` and `observed` are approved. A declared status is downgraded,
never upgraded:

- no source becomes `unknown`
- an observation older than 180 days becomes `stale`
- two approved claims that disagree on the same `claim_key` both become `contradicted`

`claim_key` names the proposition. `subject` names the routing category. They are
separate because one category holds many distinct findings, and those are not
contradictions. A finding with no explicit `claim_key` gets its own id.

A packet that cites anything outside the approved list raises. It does not quietly
drop the claim.

## Qualification rubric

`qualification-v1` is the sole qualification owner. Its six evidence-attributed
components total 100: problem evidence 25, commercial fit 20, buyer accessibility
15, trigger urgency 15, proof fit 15, and execution readiness 10. Tiers are HOT
85, STRONG 70, QUALIFIED 55, WATCH 40, and DO_NOT_PURSUE below 40.

Every positive component cites approved evidence with freshness, confidence, and
source provenance. Unknown evidence scores zero; stale evidence reduces confidence;
contradictions remain explicit. Numeric score and actionability are separate. The
hard gates cover unresolved identity/domain, missing destination, contradicted
evidence, unresolved previous outreach, legal/compliance exclusion, no credible
service route, and explicit hold/defer. Routing and diagnostics never contribute
points. Historical rubrics are compatibility references only. See
`migration/phase-3/QUALIFICATION-V1-DECISION-RECORD.md`.

## Prices

`service-routes.yaml` holds the five canonical service routes, gap mappings,
wedges and verified proof assets. It holds no price. Two live sources conflict:
the 2026-06 offer ladder in lead-engine-v1 and the 2026-07-14 single-offer
decision, and the deployed site publishes no audit price. Until Emmanuel settles
that, price stays `confirmed_at_booking` and the engine never asserts one.

## Additions to the shipped package

One routing task was added on 2026-08-11: `diagnostic_capability_run` routed to
`claude_code`. The shipped policy had no route for running a registered diagnostic
such as geo-audit or client-audit. The addition is marked inline in
`routing-policy.yaml` with its reason.

## Layout

| Path | Contents |
|---|---|
| `role-registry.yaml` | 16 business roles, their inputs, outputs, authority, KPIs, permitted capabilities |
| `routing-policy.yaml` | which runtime handles which class of task |
| `service-routes.yaml` | the five canonical service routes, gap mappings, wedges, verified proof assets |
| `roles/` | one readable brief per role |
| `schemas/` | GTM state, capability contract, GEO diagnostic result |
| `scripts/` | capability loader, deterministic core, two slice runners |
| `tests/` | architecture, capability references, core determinism and approval gates |
| `examples/` | synthetic fixtures, clearly labelled, used by the tests |
| `runs/` | run records written by the slice runners |
| `receipts/` | migration and decommission receipts |

## Phase 2: acquisition engine absorption

Decision, 2026-08-11: `operations/client-acquisition-engine/` is the active GTM
migration source. Keep it, absorb it, retire only duplicated control and state
surfaces after verified migration. No bulk move.

| Document | What it holds |
|---|---|
| `migration/PHASE-2-ABSORPTION-DECISION-2026-08-11.md` | The eight-deliverable decision record and Phase 2 stop condition. |
| `migration/acquisition-engine-map.json` | 34 components classified by function and target area. Judgment lives here. |
| `migration/verify_map.py` | Measures paths and counts. Fails if a mapped path vanishes or a real path is unclaimed. |
| `migration/acquisition-engine-inventory.md` | Generated component inventory. Do not hand-edit. |
| `migration/phase-2/acquisition-engine-file-inventory-2026-08-11.csv` | Exact 199-file meaningful-component inventory with hashes, target, disposition, and provenance labels; ephemeral caches are excluded. |
| `migration/superseded-logic.md` | Six behaviours marked `SUPERSEDED_AFTER_MIGRATION`, and the six that are explicitly not. |
| `migration/daily-objective-redesign.md` | The 09:10 replacement, its gates, and the shadow-run cutover test. |
| `migration/phase-2-test-results.md` | Two real prospects run end to end. Old state versus new result. |
| `migration/PHASE-3-PLAN.md` | Ten steps with owners, verification and rollback. |

```bash
python operations/internal-gtm/migration/verify_map.py --write
python operations/internal-gtm/adapters/engine_snapshot.py --as-of 2026-08-11 --select
python operations/internal-gtm/adapters/acquisition_engine.py --prospect premier-fm
```

Nothing in Phase 2 moved a file, changed a schedule, or authorized an action. The
five markers placed inside the engine are comments and a banner.
