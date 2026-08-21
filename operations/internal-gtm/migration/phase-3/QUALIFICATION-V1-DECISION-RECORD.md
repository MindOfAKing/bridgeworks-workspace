# qualification-v1 decision record

Approved by Emmanuel, 2026-08-11. Implemented and live in `operations/internal-gtm/`.

## What is canonical

| Concern | Owner |
|---|---|
| Qualification arithmetic and hard gates | `operations/internal-gtm/scripts/gtm_core.py`, `score_qualification` |
| Evidence derivation for qualification | `operations/internal-gtm/scripts/qualification_v1.py` |
| Routing | `gtm_core.select_service_route`, `service-routes.yaml` |
| Historical scales | `qualification_contract.py`, compatibility reading only |

There is one implementation of the arithmetic. `qualification_v1.py` contains none
of it. It derives `source_provenance`, `evidence_freshness` and `confidence` from
the evidence ledger and delegates, so a caller cannot assert freshness it does not
have.

## The model

| Dimension | Max |
|---|---:|
| `problem_evidence` | 25 |
| `commercial_fit` | 20 |
| `buyer_accessibility` | 15 |
| `trigger_urgency` | 15 |
| `proof_fit` | 15 |
| `execution_readiness` | 10 |

Tiers: HOT 85, STRONG 70, QUALIFIED 55, WATCH 40, DO_NOT_PURSUE below 40.
Versioned operating defaults. Recalibrate from telemetry.

## Evidence rules, enforced in code

- A non-zero component with no approved evidence is zeroed and the reason recorded.
- Unknown evidence never scores positively.
- Stale evidence downgrades confidence, and beyond the ledger's staleness window it
  is no longer approved so it stops scoring.
- Contradicted evidence is never silently resolved. The component is zeroed and the
  contradiction opens a hard gate.
- Every component stores score, evidence IDs, freshness, confidence and source
  provenance. A cited ID that is not in the ledger is reported, not ignored.

## Separation of concerns, enforced in code

`qualification_v1.FORBIDDEN_CONTEXT` refuses `route_id`, `primary_service_route`,
`diagnostic_score`, `diagnostic_capability`, `geo_score` and `gap_categories`. The
scorer raises rather than reading them, so no diagnostic family can become an
implicit qualification proxy. A test covers all six.

Whether a credible service route exists is a **gate**, not a score. Removing the
route changes actionability and leaves the score untouched. A test proves it.

## Score and actionability never merge

Seven blocking conditions are supported. The result carries `score`, `tier` and
`actionability` as separate fields. A perfect 100 HOT with no verified destination
returns `actionability: blocked_missing_destination` and builds no packet.

## What the model did to the two live prospects

| Prospect | Superseded rubric | qualification-v1 | Actionability |
|---|---|---|---|
| Premier FM | 94 HOT | **50 WATCH** | actionable |
| GBS Africa | 77 HOT | **59 QUALIFIED** | blocked_contradicted_evidence |

Both lose 30 points to the same two components:

```
commercial_fit        0 / 20   no contract-value, budget or segment evidence collected
execution_readiness   0 / 10   no delivery-capacity or decision-process evidence collected
```

**This is the headline finding.** Every prospect in the pipeline has been qualified
on website evidence alone. The old rubric could not see the gap because it had no
dimension for it. qualification-v1 makes it a visible, quantified 30-point hole on
every record.

Premier FM also drops on `problem_evidence`: one medium-severity finding scores 5
of 25. The old rubric gave 30 points for route fit alone. GBS Africa scores the
full 25 because eleven approved findings back it.

Nothing about either prospect changed today. Only what we are willing to claim
about them changed.

## Consequences to expect

- Fewer HOT prospects. The 85 threshold is unreachable on website evidence alone.
- Two new research questions per prospect: what is the contract value, and who
  decides. Neither is answerable from a homepage.
- The `advance_qualified_prospect` objective will fire less often until commercial
  and execution evidence is collected. That is the model telling the truth about
  pipeline depth.
