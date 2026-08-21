# Internal GTM shadow objective refinement

Date: 2026-08-11  
Status: implemented, tested, shadow only  
Live 09:10 workflow: unchanged

## Decision result

The refined selector now uses the seven approved priority classes. GBS Africa is
`unsafe_contained`, not `unsafe_active`. It remains a class 4 reconciliation task,
`resolve_blocking_evidence`, because its qualification gate blocks advancement,
it has no executable approval, and no shared rule is contaminated.

At the recorded 09:10 shadow state, classes 1 and 2 were empty. The selector chose
class 3, `complete_qualification_coverage`, with an explainable cohort of eight.
New supply stayed closed.

After the batch was persisted, the current next-objective calculation changed to
class 2, `advance_active_revenue`, for Tilz Prosperitas. This is expected state
progression, not a change to the recorded shadow observation.

## Enrichment ranking

`scripts/enrichment_priority.py` ranks only existing prospects. Its factors are:

- problem evidence, 0 to 20;
- trigger strength, 0 to 20;
- buyer evidence, 0 to 15;
- proof fit, 0 to 15;
- company attractiveness, 0 to 15;
- evidence freshness, 0 to 10;
- explicit blocker penalties.

The output prints every factor and penalty. Stable prospect ID breaks exact ties.
Route maturity and implementation maturity are not inputs. Cohorts are clamped to
five through ten, with eight as the current operating default.

## First real no-send batch

Canonical artifacts:

- `runs/qualification-batches/internal-gtm-qualification-2026-08-11-01.json`
- `runs/qualification-batches/internal-gtm-qualification-2026-08-11-01.md`
- `runs/qualification-batches/AI-WORKFLOW-SCAN-BV-INTEGRATED-2026-08-11.md`

| Prospect | Score and tier | Coverage | Route | Diagnostic result | Next action |
|---|---|---:|---|---|---|
| Arc Solutions Limited | 46 WATCH, actionable | 33.3% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |
| DARAJA Africa-EU | 53 WATCH, actionable | 50.0% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |
| Geneto Facility Management Company | 44 WATCH, actionable | 33.3% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |
| Tilz Prosperitas | 72 STRONG, actionable | 83.3% | content-visibility-demand | existing GEO result is partial | complete the justified GEO diagnostic |
| BEPELOG Kft | 42 WATCH, actionable | 33.3% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |
| BV Integrated Ltd | 56 QUALIFIED, actionable | 66.7% | ai-workflow-automation | bounded internal test draft completed | validate workflow hypothesis |
| Greenleaf Engineering | 42 WATCH, actionable | 33.3% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |
| Kunbase Kft | 42 WATCH, actionable | 33.3% | digital-platforms-brand | client-audit not justified | complete Stage 2 coverage |

Every row includes the existing trigger, problem evidence, all six component
scores, qualification coverage, Commercial Intelligence, Buyer Intelligence,
tier, actionability, route, diagnostic, proof, offer hypothesis, and next action.

## Progressive intelligence spend

Stage 1 used existing records and deterministic free checks. Stage 2 used only
evidence already captured from public sources and marked unresolved commercial or
buyer questions explicitly. Two prospects warranted Stage 3 consideration.

Tilz cannot advance because three GEO specialist areas remain unverified and the
existing diagnostic has no aggregate score. BV Integrated received one bounded
workflow scan. It is an internal test draft because the real enquiry process and
owner have not been validated. It cannot be released.

No prospect completed a Stage 3 diagnostic. Therefore no prospect reached Stage 4
and no approval-ready packet was created.

## Conflicting pre-gate artifact

`runs/batches/gtm-batch-2026-08-11.json` appeared concurrently and assembled a
Premier FM approval packet while its client-audit result still said
`eligible, not yet run`. That violates the progressive spend gate. The artifact
is retained for provenance but marked `superseded_pre_gate_artifact`. Its nested
packet must not be approved or executed.

## Shadow day 1

| Field | Recorded result |
|---|---|
| Old workflow | `no_eligible_rows` |
| Refined workflow | `complete_qualification_coverage` |
| Priority rank | 3 of 7 |
| Higher classes | no unsafe active state; no active qualified revenue work at observation time |
| Deferred contained state | GBS Africa under `resolve_blocking_evidence` |
| Approval backlog | 15 |
| New supply | not justified |
| Engine untouched | yes |
| Emmanuel decision | accepted after containment refinement |
| Shadow days | 1 of 10 |

The log keeps both old and refined actions, priority class, higher-class reasons,
unsafe classification, cohort, supply decision, backlog, and engine-mtime proof.
Cutover remains prohibited until all ten original shadow days and human acceptance
conditions are complete.

## Verification

- 190 internal-GTM tests passed.
- 10 skill-governance tests passed.
- 3 acquisition outreach-engine tests passed.
- The shadow harness reports one day, no engine write, and no cutover readiness.

## Safety result

No outreach, Gmail write, HubSpot write, Mission Control write, acquisition-engine
write, scheduler cutover, shutdown, credential change, paid research, deletion,
commit, or push occurred.
