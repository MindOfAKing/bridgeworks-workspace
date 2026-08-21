# Shadow objective refinement

> SUPERSEDED RESULT NOTE, 2026-08-11: The selector and GBS classification in
> this report remain valid. Its `runs/batches/gtm-batch-2026-08-11.json` batch is
> not canonical because it assembled a Premier FM approval packet while the
> client-audit result still said `eligible, not yet run`. The canonical no-send
> batch is `runs/qualification-batches/internal-gtm-qualification-2026-08-11-01.json`.
> No packet from the superseded artifact may be approved or executed.

2026-08-11. Implemented and validated. The live 09:10 workflow is unchanged.

198 tests pass: 185 internal-GTM, 10 skill-governance, 3 acquisition-engine.

---

## Unsafe-state severity, and the GBS Africa reclassification

`objective_hierarchy.classify_unsafe` returns `unsafe_active` when any of these
hold, and `unsafe_contained` otherwise:

- the lifecycle stage can reach an external action (`awaiting_approval` or later);
- an executable approval task is attached;
- contact state conflicts, so a send could repeat or be missed;
- the contradiction sits on shared or canonical state;
- the same contradiction appears on another prospect.

**GBS Africa is `unsafe_contained`.** The classifier's own reasons:

```
stage qualified cannot reach an external action
no approval exists that could execute against it
isolated to this prospect, no shared rule contaminated
```

It moves from priority class 1 to class 4, `resolve_blocking_evidence`. It is still
a reconciliation task. It no longer outranks revenue-producing work, because the
gates already hold it and nothing can escape while they do.

Six tests cover the boundary in both directions: an identical contradiction at
`awaiting_approval`, or with an approval task attached, or affecting two prospects,
or touching shared state, classifies as `unsafe_active` and does outrank revenue.

---

## Canonical objective hierarchy

Seven classes, implemented in order. Within a class, ranking uses expected
commercial value, urgency, evidence confidence and effort.

**Route maturity and implementation maturity are not ranking factors.** They appear
in the output only as `factors_deliberately_excluded`, and a test asserts no factor
name contains "maturity". How good BridgeWorks is at a capability is not a fact
about the prospect.

Day 1, against real state:

| Rank | Class | Candidates | Outcome |
|---:|---|---:|---|
| 1 | `stop_unsafe_external_action` | 0 | nothing in this class today |
| 2 | `advance_active_revenue` | 0 | nothing in this class today |
| 3 | `complete_qualification_coverage` | 48 | **selected** |
| 4 | `resolve_blocking_evidence` | 1 | deferred, a higher class was selected |
| 5 | `execute_due_followup_or_nurture` | 0 | nothing in this class today |
| 6 | `recover_overdue_research` | 2 | deferred, a higher class was selected |
| 7 | `generate_new_supply` | 0 | blocked by every higher class |

`advance_active_revenue` is empty for a reason worth stating: no prospect is both
qualified and unblocked yet, because the coverage work has not been done. That is
the argument for class 3 winning, not an argument against class 2 existing.

---

## Qualification coverage as a primary objective

The selector chose `complete_qualification_coverage` over creating supply, with 48
candidates. That is the behaviour the decision asked for and it is now the observed
behaviour, not a stated intention.

---

## Enrichment prioritisation

`enrichment_priority` ranks on evidence already held, before any spend. Seven
factors, integers, each traceable to an engine field: problem evidence, trigger
strength, buyer evidence, proof fit, company attractiveness, evidence freshness,
minus blockers.

Across 48 prospects the scores spread from 100 down to 0. **34 of 48 carry at least
one blocker.** Nothing was enriched wholesale.

Cohort of 8, inside the preferred 5 to 10:

| Priority | Company | Why |
|---:|---|---|
| 95 | BV Integrated Ltd | 3 sourced URLs, verified 2 days ago, named CEO with an exact destination |
| 95 | DARAJA Africa-EU | 2 sourced URLs, two named co-founders, exact destination |
| 95 | Eloria Consult | recent verification, exact destination |
| 95 | Green Facilities Limited | two named directors, client proof, exact destination |
| 95 | Premier FM | named sales director with a direct address, recent verification |
| 92 | Vendorcredit | partnership trigger, exact destination |
| 90 | Arc Solutions Limited | 3 sourced URLs, no named buyer, generic destination |
| 90 | BEPELOG Kft | live quote route, generic destination |

Below the line, and why: PERCOSO Nigeria scores 88 raw and drops to 38 after a 20
point penalty for no exact contact route and a 30 point penalty for its historical
hold. The ranking is reviewable line by line; every score prints the arithmetic and
the evidence that produced it.

---

## Progressive intelligence spend

Four stages, each a gate rather than a step.

The first build of this batch had **all eight prospects reaching Stage 4** on Stage 1
evidence alone, which is exactly the waste the staging is supposed to prevent. The
Stage 3 gate was too loose. It now requires that **no dimension is still
unresearched**, which in practice means Stage 2 has run.

Result after tightening:

| Stage | Prospects |
|---|---:|
| Stage 1, cheap | 8 of 8 |
| Stage 2, targeted enrichment | **1** |
| Stage 3, diagnostic eligible | **1** |
| Stage 4, approval packet | **1** |

Seven of eight are held at `stage_2_targeted_enrichment` with the exact reason
recorded: `dimensions still unresearched: commercial_fit, execution_readiness`. No
diagnostic was run on any of them, and no diagnostic will be until the cheap
research says the prospect is worth it.

---

## The first real GTM batch

`runs/batches/gtm-batch-2026-08-11.json`. Nothing was sent.

Stage 2 was genuinely performed on Premier FM using free public sources only. It
produced real findings, including two that matter:

**Commercial Intelligence, Premier FM.** The trading name is operated by
Otthonbiztonsagban.hu Kft., tax number 26381183-2-07, registered in Szekesfehervar
rather than Budapest. The homepage publishes counter labels for years of experience,
operated area, assignments, satisfied clients and subcontractors, and **every one
appears with no numeric value**. No headcount and no client count is published
anywhere.

`commercial_value_band: null`, confidence `none`, with the reason recorded: there is
no published quantity to multiply, so a band would be a fabrication with a number
attached. Procurement complexity low. Engagement size fit plausible, on the basis
that a Kft with two published staff and one location is the size BridgeWorks has
actually delivered for.

**Buyer Intelligence, Premier FM.** Problem owner and champion established with a
role-specific published business address. Budget owner and decision maker left
**null**, because no managing director or signing authority is published anywhere on
the site. The unresolved question is recorded: the managing director is on the
Hungarian register under that tax number, which was not queried in this pass.

### Premier FM, the one prospect that reached an approval packet

| Field | Value |
|---|---|
| Trigger | facility-management credibility-proof and quote-route review, missing KPI-number rendering |
| Problem evidence | quote route and named contacts reachable, proof-counter section shows KPI labels with no numbers |
| Component scores | problem 25, commercial 0, buyer 15, trigger 15, proof 15, execution 0 |
| Coverage | **100%**, missing dimensions **none** |
| Commercial Intelligence | value band null with reason, procurement low, size fit plausible |
| Buyer Intelligence | problem owner and champion established, budget owner and decision maker null |
| Tier | STRONG, 70 of 100 |
| Actionability | `actionable` |
| Service route | `digital-platforms-brand` |
| Diagnostic capability | `client-audit` |
| Diagnostic result | eligible, not yet run |
| Chosen proof | `oliviks-foundation-2026-07-24` |
| Offer hypothesis | Lead path and trust review |
| Approval packet | `awaiting_approval`, digest `8820ab98…`, 2 cited claims |
| Next action | `emmanuel_approval` |

**The distinction now visible on the record.** Premier FM scores 0 on
`commercial_fit` and 0 on `execution_readiness`, and both appear in
`verified_negative_dimensions`, with `missing_dimensions` empty. BV Integrated
scores 0 on the same two dimensions and both appear in `missing_dimensions`.

Identical zeros, opposite meanings. One has been researched and the answer was no.
The other has not been researched. Only coverage can tell them apart, and it does.

**A finding worth your attention.** Companies House shows BV INTEGRATED LTD,
company number 16768029, incorporated **7 October 2025**, registered at 20 Wenlock
Road, London N1 7GU. That is a company roughly ten months old at an address widely
used as a registered-office service. It is the highest-priority prospect in the
cohort on evidence already held. That is a commercial-fit question, not a
disqualification, and it is exactly the question Stage 2 exists to ask before
anyone spends a diagnostic on it.

---

## Shadow comparison

The log now records, per day, both workflows plus the class decision:

| Field | Day 1 |
|---|---|
| Old 09:10 workflow | `no_eligible_rows` |
| Refined selector | `complete_qualification_coverage`, rank 3 of 7 |
| Cohort | 8 prospects |
| Higher classes not selected | `stop_unsafe_external_action` 0 candidates; `advance_active_revenue` 0 candidates |
| Lower classes deferred | `resolve_blocking_evidence` 1; `recover_overdue_research` 2 |
| Unsafe classification | `gbs-africa` → `unsafe_contained` |
| New supply justified | no |
| Engine untouched | yes |

Every earlier field is still written, so rows from before and after this refinement
remain directly comparable. Day 1 of 10. The acceptance period is unchanged.

---

## Not done

No outreach, no CRM mutation, no scheduler cutover, no shutdown, no credential
change, no deletion. The 09:10 cron still runs the old job.

Stage 2 has been performed on one prospect. The other seven in the cohort are
queued for it, and nothing downstream of them has been spent.
