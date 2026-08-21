# Phase 3 completion report

2026-08-11. Steps 1 to 9 implemented and validated. Steps 10 and 11 are blocked by
design: cutover needs ten shadow days and Emmanuel's approval, decommission needs
cutover.

152 repository tests pass: 139 internal-GTM, 10 skill-governance and 3
acquisition-engine. The installed native qualifier and router also pass their 16
contract cases (8 qualifier, 8 router), and their installed files match the
staged migration sources by SHA-256.

---

## 1. Regenerated capability-registry diff

Tool: `skill-governance/scripts/registry_migrate.py`. `diff` writes nothing, it
generates into a temporary directory using the live generator and compares.

Full report: `registry-diff-2026-08-11.json`.

| Class | Count |
|---|---:|
| new capability | 29 |
| updated capability | 0 |
| duplicate installation | 2 |
| superseded implementation | 0 |
| metadata gap | 74 |
| runtime conflict | 32 |
| governance concern | 0 |

**Zero governance concerns.** No curated `security`, `status`, `notes` or
`known_weaknesses` value would be lost, and no provenance becomes less specific.
23 records gain a repository and commit they did not have.

**All five 2026-08-01 BridgeWorks capabilities present and active:**
`bridgeworks-lead-qualifier`, `bridgeworks-prospect-router`,
`bridgeworks-geo-prospect-scan`, `bridgeworks-revenue-system-scan`,
`bridgeworks-ai-workflow-scan`. All Codex-installed.

**The 32 runtime conflicts are the most important finding.** These are not
skills installed twice. They are skills whose Claude and Codex copies hold
*different* SKILL.md content. `client-audit` is 117 lines under Claude and 125
under Codex with a rewritten description. `market-audit` is 389 against 402. For
these 32, which version runs depends on which runtime you are in, and the registry
records one description for both. Each carries a `runtime_divergence` block naming
the scanned runtime and both digests, so the conflict lives on the record and not
only in a report.

The pre-write diff therefore reported `blocking: 32`. No force-apply selected a
winner. The final registry was produced through the preserving annotation path:
it added the discovered installations and attached both runtime digests while
retaining curated status and provenance. A post-write dry diff now raises 24
governance concerns if the plain live generator tries to auto-activate the 24
unknown records. That is the intended guardrail, not an unresolved write.

**Baseline recovery, worth flagging.** The first `apply` wrote a backup at
`capability-registry.yaml.pre-2026-08-11`, which a concurrent run then overwrote
with its own post-regeneration state. The true 25 July baseline was restored from
git to `capability-registry.yaml.baseline-2026-07-25` and is covered by a test.

---

## 2. Final capability counts by runtime

| Measure | Before | After |
|---|---:|---:|
| Unique capabilities | 74 | 103 |
| Claude installations | 73 | 74 |
| Codex installations | 3 | 63 |

| Distribution | Count |
|---|---:|
| Claude only | 40 |
| Codex only | 30 |
| Both runtimes | 34 |
| of which two live versions | 32 |
| of which byte-identical copies | 2 |

| Governance status | Count |
|---|---:|
| active | 79 |
| unknown, pending review | 24 |

Nothing was auto-approved because it was installed. The 24 `unknown` records are
the newly discovered `agent-*` specialists, `impeccable`, `claude-skill-creator`
and `bridgeworks-daily-operations`. `capability_loader.require_capability` raises
on a non-active capability, so an unreviewed skill cannot be called even though it
is registered. A test pins that.

---

## 3. Duplicate and superseded capability disposition

| Duplicate | Disposition | Evidence |
|---|---|---|
| Second capability registry in the router skill | Retired. Body replaced with a pointer to the canonical registry and the loader command. The unique work-pass routing table is kept. The original is preserved at `phase-3/preserved/staged-capability-registry-2026-08-01.md`. | `test_no_second_registry_in_the_acquisition_engine` |
| Duplicate qualification rubric (`score_prospect.py`) | Canonical `qualification-v1` inputs delegate to `gtm_core`. Historical inputs return compatibility provenance and `requires_qualification_v1_rescore: true`; they never create canonical qualification state. | `QualificationContractTests`, `test_legacy_readiness_cannot_create_qualification` |
| Duplicate route registry (`validate_route.py` `ROUTES`) | Now a compatibility CLI over `service-routes.yaml`. The hardcoded literal is gone and a test fails if it returns. | `test_the_router_no_longer_holds_its_own_route_list`, `test_the_router_cli_still_runs` |
| Production ceilings unique to `validate_route.py` | Preserved before removal and ported into `gtm_core`: four work passes, 20 minutes, and the overproduction check that rejects proposal, full audit, ROI estimate and CRM migration architecture at first contact. They now run on every packet, not only when someone hands the validator a plan. | `ProductionCeilingTests` |
| Sector-weighted ranking in `prospect_research_queue.rank_row` | Marked `SUPERSEDED_AFTER_MIGRATION`, still running. Replaced at cutover, not before. | `superseded-logic.md` |

**Resolved by Emmanuel on 2026-08-11:** `qualification-v1` is the sole owner of
qualification arithmetic, tier, actionability, and qualification lifecycle state.
The six dimensions and seven hard gates are implemented in `gtm_core`; evidence
freshness, confidence and provenance are derived by `qualification_v1.py`.
`qualification_contract.py` preserves historical records without translating
their statuses into canonical tiers. The acquisition snapshot likewise leaves 46
prospects unscored and queues `complete_qualification_v1` instead of inventing a
provisional tier.

---

## 4. Canonical prospect migration results

Tool: `adapters/prospect_reconcile.py`. Read-only. `writes_performed: 0`.

| Measure | Value |
|---|---:|
| Rows across all stores and live receipts | 339 |
| Unique entities | 120 |
| Entities present in more than one store | 97 |
| Rows with no usable key | 0 |
| Entities marked contacted by any evidence source | 12 |
| Gmail-verified contacted businesses | 10 |
| Gmail SENT messages | 19 |
| HubSpot-linked entities | 14 |
| Mission Control acquisition approvals waiting | 15 |
| Stale entities | 0 |
| Same-authority conflicts | 1 |
| Cross-key duplicate candidates | 3 |

Rows by source: live Gmail 10, Mission Control approvals 15, live HubSpot 14,
acquisition-engine results 49, acquisition-engine source 100, canonical register
60, Lead Engine v1 64 and pipeline/prospecting 27.

Authority order, enforced in code: live Gmail, Mission Control approval state,
live HubSpot object identity, local Gmail log, acquisition-engine results,
acquisition-engine source, canonical register, Lead Engine v1 and
pipeline/prospecting. Each operational system owns only its own facts. A
lower-authority value never overwrites a higher one, and same-authority
disagreement stays contradicted rather than being resolved.

The three previously orphaned Gmail sends are resolved by a deterministic receipt:
recipient domain equals canonical domain, that domain appears in historical
identity evidence, and the historical Gmail message ID is present in the live
mailbox result. This attaches A+ Real Estate, Craftex and Managerent. Ambiguity is
retained as `possible_match`; none remains for sends. The one canonical accounting
receipt, `reconciliation-accounting-receipt.md`, explains 303 versus 339 source
rows, 122 versus 120 entities, 8 versus 12 contacted companies, and 3 versus 0
orphaned sends without forcing the counts to match.

The live mailbox check found 19 SENT messages across Managerent, A+ Real Estate,
Craftex, Homever, Interház, Premier Property Management, Rentify, FirstClean,
Loffice and Budbed. Seven DRAFT messages were also present. No inbound reply was
observed in the exact-address results. HubSpot exact-domain searches found 14 of
25 checked companies and supplied their object IDs; 11 domains were recorded as
not found. Both connector receipts are immutable and explicitly `read_only`.

| HubSpot domain | Company ID |
|---|---:|
| homever.hu | 437186387147 |
| interhaz.hu | 437186689256 |
| ppmgt.hu | 440275030214 |
| rentify.hu | 437186128088 |
| firstclean.hu | 437177281724 |
| loffice.hu | 437184928983 |
| budbed.hu | 439947420864 |
| rideflow.org | 442342357193 |
| kunbase.com | 442178947293 |
| gbsafrica.co.uk | 442339765493 |
| daraja-africa.eu | 442351660280 |
| bvintegrated.co.uk | 442331804911 |
| logistics.bepelog.hu | 442274292944 |
| premierfm.hu | 442352746693 |

The one same-authority conflict is `domain:budapest.cylex.hu`, two research
results claiming `checked_at` 2026-07-23 and 2026-07-24. Left contradicted.

---

## 5. Routing-bias regression results

`route_priority` no longer selects anything. It is display order, labelled as such
in `service-routes.yaml`. Selection now runs a six-dimension comparison in the
order Emmanuel specified: evidence strength, commercial pain, buyer relevance,
proof fit, urgency, entry-offer credibility.

**Capability maturity is not in the comparison at all.** It is reported as
`confidence` on the result. A test asserts it never appears in any candidate's
ranking key.

**On a true tie, nothing is selected.** `fit: "tie"`, both routes named, and the
run escalates to `strategic_recommendation` instead of guessing. Code that cannot
choose says so.

| Test | Result |
|---|---|
| `test_geo_does_not_win_a_true_tie` | pass. Equal evidence on `ai_visibility` and `conversion_path` returns a tie with both routes and an escalation, not GEO |
| `test_maturity_is_never_in_the_ranking_key` | pass |
| `test_stronger_evidence_wins_not_display_order` | pass. Two verified `conversion_path` findings beat one observed `ai_visibility` finding, and `digital-platforms-brand` wins |
| `test_buyer_role_breaks_a_tie_before_maturity` | pass. A Head of Sales buyer moves the tie to `digital-platforms-brand` |

Both live prospects re-run under the corrected router and hold, now for stated reasons:

| Prospect | Route | Won on | Scores |
|---|---|---|---|
| GBS Africa | `content-visibility-demand` | evidence_strength | 32 against 9 for `digital-platforms-brand` |
| Premier FM | `digital-platforms-brand` | only_matching_route | GEO scored nothing, no visibility gap was evidenced |

---

## 6. Claim-key regression results

The invariant is now system-wide, and the fallback changed.

- `subject` is the routing and evidence category.
- `claim_key` is the exact proposition.
- A producer that declares no `claim_key` gets an implicit key of `(subject, source)`.
  It **never** falls back to `subject` alone. That fallback was the Phase 2 bug.

| Test | Covers |
|---|---|
| `test_distinct_findings_in_one_category_are_not_contradictions` | GEO, the original bug |
| `test_implicit_key_is_subject_and_source_never_subject_alone` | conversion path, non-GEO |
| `test_same_subject_same_page_disagreement_is_caught_without_a_declared_key` | ownership, non-GEO, undeclared conflict still caught |
| `test_declared_key_beats_page_coincidence` | process gaps, two propositions on one page |
| `test_invariant_holds_for_manual_workflow_claims` | AI-workflow, four findings under one subject |
| `test_shared_claim_key_still_detects_the_real_conflict` | search visibility, the GBS Africa title-tag conflict |
| `test_invariant_validator_warns_on_implicit_collisions` | `validate_claim_invariant` warns rather than failing |

Every producer was updated: the GEO slice, the market-discovery fixture and the
acquisition-engine adapter, which now stamps one proposition per source.

---

## 7. GTM telemetry schema and example records

Schema: `schemas/gtm-telemetry.schema.json`. Store:
`runs/telemetry/gtm-telemetry.jsonl`. Tool: `scripts/telemetry.py`.

Every dimension asked for is present. Decisions sit under `decision`, outcomes
under `outcome`, and the two are never mixed.

**A null outcome means unknown, never no.** A prospect with `sent_at: null` has not
been contacted, so it enters no conversion denominator. Every rate reports its
denominator, and a zero denominator gives `null`, not `0`. Rebuilding decisions
never clobbers a real outcome.

The store now contains 122 rows and covers all 120 canonical entity keys while
preserving separate attempts. Three current run records carry `qualification-v1`;
119 rows correctly retain null qualification values until scored. All six component
scores are persisted and are valid `compare --by` dimensions. Unknown decisions
remain null. Example, GBS Africa:

```json
{
  "record_id": "gbs-africa@2026-08-11",
  "decision": {
    "trigger_type": "diagnostic_run", "buyer_reachability": "generic_contact",
    "qualification_version": "qualification-v1",
    "qualification_score": 59, "qualification_tier": "QUALIFIED",
    "problem_evidence": 25, "commercial_fit": 0,
    "buyer_accessibility": 4, "trigger_urgency": 15,
    "proof_fit": 15, "execution_readiness": 0,
    "primary_service_route": "content-visibility-demand", "route_fit": "adjacent",
    "route_won_on": "evidence_strength", "secondary_routes": ["digital-platforms-brand"],
    "diagnostic_capability": "geo-audit", "diagnostic_score": 45,
    "diagnostic_result": "complete", "evidence_quality": "verified",
    "approved_claim_count": 14, "contradicted_claim_count": 2,
    "proof_asset_id": "ceefm-geo-16-to-77", "offer_hypothesis": "AI visibility snapshot",
    "channel": "email"
  },
  "outcome": { "approval_state": "pending_approval", "sent_at": null, "..." : null }
}
```

`compare --by <dimension>` gives the GTM Learning role funnel counts and rates
across 24 dimensions. Ten Gmail-verified businesses now carry exact latest-sent
timestamps. In the legacy/no-route group, 23 prospects reached preparation and
10 reached send; no reply was observed in the exact-address Gmail results.
Native service-route groups remain prepared but unsent. Later-stage rates are
`null` when their denominators are zero. A null means unknown or not yet reached,
never a negative outcome.

---

## 8. 09:10 shadow-test results to date

Harness: `scripts/shadow_log.py`. Log: `runs/shadow/09-10-shadow-log.jsonl`.
**Day 1 of 10.** The old job is imported and evaluated, never executed, and every
run verifies the engine is untouched by mtime comparison.

Day 1, 2026-08-11:

| Field | Value |
|---|---|
| Old workflow action | `no_eligible_rows`, 0 eligible rows |
| New workflow action | `reconcile_unsafe_state` on `gbs-africa` |
| Reason | `contradicted_evidence_or_contact_state` |
| Pipeline depth | 48 |
| Qualified untouched | 1 |
| Requires `qualification-v1` | 46 |
| Overdue research | 2 |
| Missing evidence | 0 |
| Approvals waiting | 15 |
| New supply justified | no |
| Observed difference | old would do nothing, new resolves a contradiction |
| Human correction | none recorded |
| Engine untouched | yes |

The new selector put the GBS Africa evidence contradiction at the top. Two claims
about the same page disagree, so every downstream decision about that prospect is
unsound until it is resolved. The old job had nothing to do that morning.

Readiness: `ready_for_cutover: false`. Two of the four criteria need Emmanuel and
the harness will not self-certify them.

A separate bounded heartbeat, `bridgeworks-gtm-shadow-validation`, is active at
09:12 on the next nine weekdays. It appends the read-only comparison and reports
back to this task. It neither invokes nor edits the live 09:10 workflow. The live
schedule remains unchanged.

---

## 9. Systems and readers repointed

| Reader | Was | Now |
|---|---|---|
| `bridgeworks-prospect-router` route list | hardcoded `ROUTES` set | `service-routes.yaml` through `capability_loader` |
| `bridgeworks-lead-qualifier` rubric | own 25/25/20/15/15 scale | canonical `qualification-v1`; legacy inputs compatibility-only |
| Acquisition snapshot | readiness mapped to WARM/COLD | readiness retained as evidence; tier/score null until `qualification-v1` |
| Router capability reference | own prose registry | pointer to `skill-governance/capability-registry.yaml` |
| `role-registry.yaml` | 18 capabilities | 22, including the five 2026-08-01 capabilities and no generic qualifier duplicate |
| Internal-GTM slices | `route_priority` | six-dimension tie-break with escalation |
| All evidence producers | `subject` as contradiction key | `claim_key`, implicit `(subject, source)` |
| Contact-state reader | stale generated register only | Phase 3 canonical reconciliation, with register fallback |
| Approval backlog reader | historical review packets | live Mission Control acquisition tasks, with review-state fallback |

**Not repointed, deliberately:** the live 09:10 cron, the acquisition engine's
approval surface, Mission Control, and the Weekly Sales Review. Those move at
cutover, which is step 10.

---

## 10. Remaining blockers before cutover

| # | Blocker | Owner | Notes |
|---|---|---|---|
| 1 | Nine more shadow days | bounded heartbeat, Emmanuel reviews | Day 1 recorded. The remaining weekday runs are scheduled at 09:12. Two criteria need a human judgment the harness will not fake. |
| 2 | GTM-critical runtime reviews | Claude Code and Emmanuel | The named critical set is classified. Intentional Codex adaptations are recorded; GEO specialist distribution/status and revops runtime coverage still need review. Other divergent skills remain deliberately untouched. |
| 3 | 24 unknown-status capabilities | Emmanuel via the intake gate | They cannot be called until reviewed. Includes the five `agent-geo-*` specialists the geo-audit orchestrator delegates to. |
| 4 | Approval surface cutover | Claude Code after validation | Read-side reconciliation now uses Mission Control and sees 15 waiting acquisition tasks. Internal-GTM packets still stop in `runs/geo/`; write ownership moves only at cutover. |
| 5 | 46 prospects require `qualification-v1` | Lead Qualifier plus Emmanuel review | They have evidence/readiness history but no canonical score or tier. No provisional qualification is minted. |
| 6 | Capacity numbers | Emmanuel | Coverage target 4 and approval cap 3 are defaults in `engine_snapshot.CAPACITY`, not measurements of his week. |
| 7 | Eleven HubSpot absences | Data Steward at cutover | Exact-domain reads returned no company for 11 of 25 checked domains. No CRM objects were created because Phase 3 is read-only externally. |

**Nothing was sent, published, deleted, shut down, or revoked. No credential was
touched. The 09:10 schedule is unchanged and still runs the old job.**
