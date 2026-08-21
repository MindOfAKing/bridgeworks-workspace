# Canonical state reconciliation

Date: 2026-08-11. The live 09:10 workflow remains unchanged.

## Premier FM

Canonical lifecycle state: `diagnostic_selected`.

The richer qualification-v1 snapshot remains 70, STRONG, 100 percent coverage, but
qualification does not satisfy a diagnostic gate. The selected route requires
`client-audit`. The newer batch says `eligible, not yet run`. The older slice used
`acquisition-engine:2026-08-05-batch-01-results` as its diagnostic provenance and
has no score or terminal run status. That is adapted research, not a successful
registered `client-audit` completion.

The verified chain is:

```text
account_discovered -> evidence_collected -> qualified -> routed -> diagnostic_selected
```

There is no `diagnostic_complete` receipt. Therefore neither `offer_selected`,
`outreach_prepared`, nor `awaiting_approval` is valid. Packets `247d861e...` and
`8820ab98...` are `superseded_pre_gate_artifact`, non-executable, and retained as
history. The canonical approval packet id is null.

Next action: successfully complete the registered `client-audit`, then persist the
`diagnostic_complete` receipt.

## Tilz Prosperitas

Canonical objective: `resolve_blocking_evidence`.

Tilz remains 72, STRONG, at 83.3 percent coverage and `diagnostic_selected`. Its
GEO result is `blocked_partial`: the technical specialist completed, but the full
diagnostic did not aggregate successfully. No dated, sourced reply, active
conversation, booked meeting, discovery, proposal, negotiation, or explicit buying
signal exists. Qualification alone never creates `advance_active_revenue`.

## Transition contract

Every adjacent advancement now records prospect id, from and to stages, triggering
capability, required gate results, exact evidence snapshot path and file hash,
approved-ledger hash, qualification version and coverage, diagnostic id and status,
approval id, runtime, and timestamp.

The enforced prerequisites are:

```text
diagnostic_selected -> diagnostic_complete  successful diagnostic id and terminal status
diagnostic_complete -> offer_selected       diagnostic_complete receipt
offer_selected      -> outreach_prepared    offer_selected receipt
outreach_prepared   -> awaiting_approval    outreach_prepared receipt
```

`gtm_core.advance` also rejects non-adjacent transitions. Pre-gate artifacts are
retained but cannot execute.

## `exhausted_unknown`

Qualification research status now supports `complete`, `partial`, `required`,
`exhausted_unknown`, and `not_applicable`. `exhausted_unknown` remains zero-scored
but counts as researched coverage and is excluded from repeat enrichment scheduling
until fresh evidence appears. Current advancement thresholds are unchanged.

## Canonical first-batch receipt

The authoritative machine-readable receipt is:

`operations/internal-gtm/runs/canonical-batches/first-real-gtm-batch-2026-08-11.json`

Its eight prospects are Arc Solutions Limited, DARAJA Africa-EU, Geneto Facility
Management Company, Tilz Prosperitas, BEPELOG Kft, BV Integrated Ltd, Greenleaf
Engineering, and Kunbase Kft. It records qualification score and coverage, missing,
partial, and exhausted-unknown dimensions, lifecycle, diagnostic status, objective,
valid packet id, superseded artifacts, and exact next action. All valid packet ids
are null.

Lifecycle reconstruction places Arc, DARAJA, Geneto, BEPELOG, Greenleaf, and Kunbase
at `routed`; Tilz and BV Integrated are at `diagnostic_selected`. Tilz is blocked on
the incomplete GEO diagnostic. BV Integrated is blocked pending workflow-owner
validation of its internal scan draft.

## Stage 2 restart

Stage 2 resumed only for the deterministic first-ranked unresolved prospect, Arc
Solutions Limited. Public owned sources support 500+ completed projects, 20+
corporate clients, 100+ field professionals, multi-location coverage, and a March
2026 coverage expansion. No supportable contract-value band was found. A general
business email and quote route are published, but no named decision maker was
established. Commercial, execution, and buyer statuses remain `partial`, not
`exhausted_unknown`, because useful positive evidence exists.

The research receipt is
`operations/internal-gtm/runs/intelligence/arc-solutions-limited-stage-2-2026-08-11.json`.
Evidence Auditor review and a qualification-v1 rerun are next. No Stage 3 diagnostic
is justified before that decision.

## Verification and safety

All 215 internal-GTM tests pass. A direct receipt audit verified 35 transition
receipts contain the required fields and that every evidence snapshot file hash
matches. No outreach, CRM mutation, scheduler cutover, acquisition-engine write,
shutdown, credential change, or destructive action occurred.
