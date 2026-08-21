# Pre-cutover capability and qualification completion

2026-08-11. All nine items implemented. The live 09:10 workflow is unchanged.

175 tests pass: 162 internal-GTM, 10 skill-governance, 3 acquisition-engine.

---

## 1. GEO runtime parity result

`geo-audit` is now installed in both runtimes. Codex GTM automation no longer
depends on Claude Code at runtime.

**One capability identity, one methodology.** The Codex copy is *derived* from the
Claude source by
`operations/internal-gtm/runtime-adaptations/build_codex_geo_audit.py`, not authored
separately. That is the whole point: a second GEO methodology cannot appear if the
second file is generated from the first.

What the adaptation changes, and nothing else:

1. Frontmatter description in the Codex quoted style.
2. A `## Codex operating rule` block, identical to the one every other Codex runtime
   adaptation carries.
3. Subagent names rewritten to the installed Codex specialist ids.
4. An appended structured-result contract pinned to
   `operations/internal-gtm/schemas/geo-diagnostic.schema.json`.

**Parity, eight checks, all passing:**

| Check | Claude | Codex |
|---|---|---|
| six weighted categories | pass | pass |
| category weights 25/20/20/15/10/10 | pass | pass |
| composite formula, term by term | pass | pass |
| four severity classes | pass | pass |
| quality gates, 50 pages and 30 seconds | pass | pass |
| five score bands | pass | pass |
| five specialists resolvable | pass | pass |
| structured result contract | pass | pass |

`--check` compares the installed Codex file against a freshly derived one and fails
on any difference. The copy is rebuilt, never hand-edited.

**Honest limit.** This is contract parity, verified by comparing both files and
their declared behaviour. It is not execution parity: I cannot run a Codex session
from here, so no side-by-side fixture *execution* was performed. The first real
Codex `geo-audit` run should be compared against
`runs/geo/gbs-africa-2026-08-11.json` before the capability is relied on for paid
delivery.

---

## 2. GEO specialist governance disposition

All five passed the pathway and were promoted to `active`. Registry status is now
84 active, 19 unknown.

| Specialist | Provenance | Source | Security | Permissions | Overlap | Isolated test | Pilot | Success criterion | Decision |
|---|---|---|---|---|---|---|---|---|---|
| `agent-geo-ai-visibility` | pass | pass | pass | pass | pass | pass | pass | pass | approve |
| `agent-geo-content` | pass | pass | pass | pass | pass | pass | pass | pass | approve |
| `agent-geo-platform-analysis` | pass | pass | pass | pass | pass | pass | pass | pass | approve |
| `agent-geo-schema` | pass | pass | pass | pass | pass | pass | pass | pass | approve |
| `agent-geo-technical` | pass | pass | pass | pass | pass | pass | pass | pass | approve |

One intake record each, at `skill-governance/intake/intake-agent-geo-*.yaml`.

**Pilot evidence, counted as evidence and not as approval.** The 2026-08-11 GBS
Africa run is recorded per specialist with what it actually produced, including the
gaps each one declared about itself:

| Specialist | Findings | Score | Self-declared gap |
|---|---:|---:|---|
| ai-visibility | 22 | 55 | Reddit and YouTube presence marked observed, not verified |
| content | 22 | 51 | freshness unverifiable, stated as such |
| platform-analysis | 28 | 34 | no live citation test run, stated as untested |
| schema | 17 | 0 | none |
| technical | 24 | 57 | Core Web Vitals field data not measured, stated as inferred |

The success criterion was that every finding carries a fetched source URL and no
measurement is reported that was not taken. All five met it, and four of the five
labelled their own limits without being asked. That is the behaviour worth
approving.

Security scanning is a static pattern check over the skill text. The standing
notice applies: a scan identifies known suspicious patterns; it does not prove a
skill is safe, necessary, correct or appropriate.

A test asserts each promoted specialist has an intake record with all eight
requirements marked pass. Promotion cannot happen without one.

---

## 3. RevOps runtime disposition

**Shared bounded capability, not a copy.** New capability
`bridgeworks-gtm-pipeline-health`, installed in both runtimes and registered.

The five roles consumed six functions from a 345-line general RevOps consulting
skill: lifecycle reasoning, pipeline movement, handoff logic, stage health,
next-action logic and commercial process analysis. Copying the whole skill would
have carried lead scoring, CRM automation workflows, deal desk processes and data
hygiene that none of them use, and two of those sections restate logic that already
exists as deterministic code in `gtm_core`.

| Role | Was | Now |
|---|---|---|
| `gtm-director` | revops | `bridgeworks-gtm-pipeline-health` |
| `market-icp-strategist` | revops | `bridgeworks-gtm-pipeline-health` |
| `reply-intelligence` | revops | `bridgeworks-gtm-pipeline-health` |
| `pipeline-manager` | revops | `bridgeworks-gtm-pipeline-health` |
| `gtm-learning` | revops | `bridgeworks-gtm-pipeline-health` |
| `prospect-router` | revops | `bridgeworks-gtm-pipeline-health` |
| `data-steward` | revops | **removed** |

`data-steward` never needed it. Its job is entity normalization, which
`gtm_core.dedupe` does deterministically. That reference was scope creep, not a
requirement.

`revops` stays installed in Claude Code for client revenue-system consulting, which
is a different job from analysing the BridgeWorks pipeline. The new capability's
guardrails say so explicitly. A test asserts no role points at `revops` any more,
and another asserts the bounded capability declares all six functions.

---

## 4. Commercial Intelligence

Role `commercial-intelligence`, capability
`bridgeworks-commercial-intelligence`, installed in both runtimes, `read_only`.

Establishes: plausible company scale, budget-capacity proxies, published locations
and headcount, growth or expansion state, probable value of the identified problem,
procurement complexity, and fit against engagement sizes BridgeWorks has actually
delivered.

**Free tools first, in a stated order:** public web and browser, public registries,
free search including SerpApi and Firecrawl free tiers, public directory pages.
Paid enrichment only after Emmanuel approves the spend, and Apollo credits are
spend. Each fact records the tool that produced it.

**The hard rule on value.** A published price times a published volume is a
supportable band, and the arithmetic is shown. Anything times an assumption is a
fabrication with a number attached, which is worse than silence. When the evidence
does not support a band, the output is `commercial_value_band: null` plus the list
of what would establish one.

It does not qualify and does not route. It returns sourced findings to the Evidence
Auditor.

---

## 5. Buyer Intelligence

Role `buyer-intelligence`, capability `bridgeworks-buyer-intelligence`, installed in
both runtimes, `read_only`.

Establishes five distinct roles where publicly supportable: problem owner, budget
owner, decision maker, champion, blocker. Each carries a person, a title, an
evidence id and an `attribution_confidence`. Roles that cannot be supported stay
null, because a record with one named decision maker and an honest gap is better
than one with five guesses.

Contact route preference: role-specific published business address, then general
published business address, then a published form, then a public professional
profile for research only and never for a message. A personal address found
elsewhere is not a contact route.

Explicit prohibitions in the contract: never message, connect, follow or contact;
never infer a personal address from a naming pattern; two sources naming different
decision makers declare a shared `claim_key` so the Evidence Auditor catches the
contradiction rather than one being picked.

**It does not choose the service route.** The contract says so in bold. The Prospect
Router consumes this evidence and decides.

---

## 6. Qualification-coverage schema

Coverage is a separate measure. It is never added to the score.

Per dimension:

```json
{
  "score": 0,
  "evidence_state": "verified | observed | inferred | stale | contradicted | unknown | none",
  "evidence_ids": ["..."],
  "confidence": "high | medium | low | unknown",
  "research_status": "complete | partial | required | not_applicable",
  "zero_because": "missing_research | verified_negative | unusable_evidence | null"
}
```

Plus, per prospect:

```json
{
  "sufficiently_researched_dimensions": 3,
  "total_dimensions": 6,
  "percentage": 50.0,
  "missing_dimensions": ["..."],
  "partial_dimensions": ["..."],
  "verified_negative_dimensions": ["..."],
  "not_applicable_dimensions": ["..."]
}
```

**The distinction the decision asked for, working.** A dimension scoring zero
because the research was done and came back negative reports
`zero_because: "verified_negative"` and `research_status: "complete"`. A dimension
scoring zero because nobody looked reports `zero_because: "missing_research"` and
`research_status: "required"`. Same zero in the score, opposite meaning in coverage.

Unknown evidence still scores zero. That rule is unchanged.

A test proves coverage never moves the score: two prospects with identical evidence
and different declared coverage produce the same score and different percentages.

---

## 7. Prospects missing each qualification dimension

Two populations, and the difference matters.

**Scored under qualification-v1: 2 prospects.**

| Dimension | Missing | Partial | Verified negative |
|---|---:|---:|---:|
| problem_evidence | 0 | 0 | 0 |
| commercial_fit | **2** | 0 | 0 |
| buyer_accessibility | 0 | 1 | 0 |
| trigger_urgency | 0 | 0 | 0 |
| proof_fit | 0 | 0 | 0 |
| execution_readiness | **2** | 0 | 0 |

Mean coverage 58.4 percent. Fully covered prospects: **0**.

**Awaiting a qualification-v1 score: 46 prospects.** The engine snapshot holds 48
prospects. Three carry an internal-GTM score. The other 46 carry no tier at all,
because the snapshot now queues `complete_qualification_v1` rather than inventing a
provisional tier.

So the honest statement is: `commercial_fit` and `execution_readiness` are missing
on 100 percent of everything scored so far, and 46 further prospects have not been
scored at all. Do not read "2 missing" as a small number. Read it as "every prospect
we have scored".

---

## 8. Canonical contacted-company accounting

One definition, one module, one computation:
`operations/internal-gtm/scripts/contacted_companies.py`.

> A `contacted_company` is a canonical prospect entity with at least one verified
> Gmail SENT message whose recipient email or recipient domain is deterministically
> linked to that entity.

Three link rules and nothing else: canonical domain match, alternate domain match,
recorded address match. A similar name is not a link.

| Measure | Value |
|---|---:|
| Contacted companies | **10** |
| Canonical sent messages | **19** |
| Ambiguous possible matches | **0** |
| Unmatched sent messages | **0** |

All ten linked by `canonical_domain_match`, the strongest rule:

A+ Real Estate 2, Budbed 1, Craftex 2, FirstClean 2, Homever 3, Interház 1,
Loffice 1, Managerent 2, Premier Property Management 3, Rentify 2.

Zero ambiguous is a result, not an assumption. The linker returns every matching
entity, and a send matching two entities stays unlinked. A test constructs that
case and asserts it is not resolved to one.

Claude, Codex, the dashboards and the Weekly Sales Review read this module. Nothing
recomputes the definition locally.

---

## 9. Effect on shadow objective selection

Shadow day 1 of 10, re-run after the changes. The comparison against earlier shadow
records is preserved: the log is keyed by date and every earlier field is still
written, so a row from before these changes and a row from after are directly
comparable.

| Field | Value |
|---|---|
| Old workflow action | `no_eligible_rows` |
| New workflow action | `reconcile_unsafe_state` on `gbs-africa` |
| Qualified untouched | 1 |
| Approvals waiting | 15 |
| New supply justified | no |
| Engine untouched | yes |

**What changed, and why it is correct.** Qualified untouched fell from 13 to 1.
That is not a regression. Under qualification-v1 only prospects with a real score
count, and 46 of 48 have not been scored yet. The old number counted provisional
tiers derived from engine readiness. The new number counts prospects BridgeWorks has
actually qualified.

Two new objectives now sit in the ladder: `complete_qualification_v1` for the 46
unscored prospects, and `enrich_qualification_coverage` for scored prospects with a
coverage gap. Neither fired today because `reconcile_unsafe_state` outranks them,
and there is still one unresolved evidence contradiction on GBS Africa.

The supply gate is unaffected and still closed. Nothing about these changes makes
new-company generation more likely; the coverage work makes it less likely, because
there is now visible internal work queued ahead of it.

---

## What was not done

- No outreach, no CRM mutation, no shutdown, no credential change, no deletion.
- The 09:10 cron is unchanged and still runs the old job.
- The ten-day shadow acceptance is unchanged. Day 1 of 10.
- No Codex session was executed, so GEO parity is contract-verified, not
  execution-verified.
- 19 capabilities remain `unknown` and uncallable, including `impeccable` and
  `claude-skill-creator`. They have not been through intake and were not touched.
