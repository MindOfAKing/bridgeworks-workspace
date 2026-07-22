# BridgeWorks Content System (Claude Code implementation layer)

File-based infrastructure for the cross-model content cycle. Built by
Claude Code per its role in `operations/cross-model-content-cycle-runbook.md`:
"implements and maintains the file-based system; builds templates, schemas,
validation, and production tooling. Does not independently decide what is
approved for publication."

Read these first, in order:
- `operations/cross-model-content-cycle-runbook.md` (the collaboration cycle)
- `operations/content-channel-model.md` (channel roles)
- `operations/mobile-publishing-pack-spec.md` (weekly pack structure)
- `operations/content-90-day-rollout.md` (rollout plan)
- `operations/automation-source-map.md` (who owns which scheduler, Command Center write rules)
- `receipts/2026-07-22-cowork-cross-model-content-audit.md` (live verification of what the Weekly Content Plan routine actually does, and the July 20 double-booking it caused)

## What is here

| File | Purpose |
|---|---|
| `content_id.py` | Issues and validates Content IDs and Master Thesis IDs. Locked/atomic against concurrent Claude Code Desktop, VS Code, or Codex runs. Enforces the brand/channel matrix (EE has no X or TT) |
| `reconciliation_checks.py` | Mechanically-checkable reconciliation: stale-client mentions, ID format, duplicate *ledger* issuance vs. duplicate *canonical definitions* vs. legitimate downstream references vs. intentional Master Thesis ID reuse, duplicate files |
| `registry/content-id-ledger.csv` | Every Content ID issued, so sequence numbers never repeat |
| `registry/master-thesis-ledger.csv` | Every Master Thesis ID issued |
| `templates/content-item-template.md` | Per-item fields for one content unit |
| `templates/weekly-pack-overview-template.md` | 00 Weekly Overview + 01 Approval Sheet structure |
| `templates/approval-card-template.md` | What Emmanuel sees before publishing |
| `templates/publishing-receipt-template.md` | What to fill after something goes live |
| `templates/analytics-backfill-template.md` | Performance data attached to a Content ID |
| `templates/interface-handoff-receipt-template.md` | End-of-session record for either Claude Code interface |
| `templates/per-channel-notes.md` | Condensed voice/role notes per channel |
| `local-to-drive-reconciliation-manifest.md` | Drift check between the Drive Content Studio and its local mirror |
| `weekly-plan-failure-safeguards.md` | Required fixes for the live Weekly Content Plan routine (documentation only, does not edit the routine) |
| `templates/claim-evidence-template.md` | Per-claim evidence record; required before an unsupported quantitative claim can reach an approval card |
| `registry/claim-evidence-ledger.csv` | Running index of approved/rejected claims |
| `receipts/` | Filled interface handoff receipts and audit reports, one per session that touches this system |

## What this is not

- Not a weekly content plan. The Cowork Weekly Content Plan (trigger
  `trig_01JeovUEsbtcnGyNmRijfCry`) remains the single primary weekly
  editorial trigger. Nothing here schedules or writes actual posts.
- Not a publishing tool. Codex owns publishing execution and the
  approval queue.
- Not a Command Center writer. No script here writes to the Command
  Center. See "Command Center" below.
- Not a media tool. Nothing here touches Remotion, image, or video
  assets. The BridgeWorks-Content-Studio production hold is unaffected.

## Command Center

The Command Center (Google Sheet `11HdcEaQqGW-TmdhOoJnfSXP4Mj0KxWLYUqFUYSMVwsc`)
already has a working "Agent Runbooks" tab (created 2026-05-30, holds the
Daily Brief Composer and Finance Sentinel runbooks). The cross-model
content-cycle runbook is not registered there yet: its own status line
says "Register... after Emmanuel resolves the open decisions." Registering
it, and any future Content ID writes to the Command Center, must go
through `C:/Users/User/Projects/update_emmanuel_os.py` only after that
script is updated to search by ID, update instead of append, and refuse
duplicates, per `operations/automation-source-map.md`. Not done in this
pass.

## Known gaps this system does not close

- The actual live weekly content routine (content-week-bot / Cowork
  Weekly Content Plan, trigger `trig_01JeovUEsbtcnGyNmRijfCry`) writes
  to `personal-brand-workspace/content/` using a Date/Platform/Content
  Type/... schema with no Content ID column. **It does not push the
  historical planner Sheet itself.** It creates `temp-week-queue.json`
  and places a manual `append-to-planner.py` command in a Gmail draft
  for Emmanuel to run. It does not touch the Command Center or write
  anywhere inside the canonical Drive Content Studio. Confirmed by
  direct inspection of the live trigger prompt; see
  `receipts/2026-07-22-cowork-cross-model-content-audit.md`, Section 2.
  Wiring the live routine to issue Content IDs through `content_id.py`,
  and to land a copy of its output in the Drive Content Studio, is a
  follow-up, not done here (personal-brand-workspace is a separate
  repository outside this audit's scope, and the Cowork routine cannot
  be edited from this repo).
- The routine's only dedup check (the historical planner Sheet's Queue
  tab) was three weeks stale when it mattered: two consecutive runs
  (2026-07-09 and 2026-07-19) each scheduled a different Personal
  LinkedIn post for 2026-07-20, and both are confirmed live on the
  Calendar. See `weekly-plan-failure-safeguards.md` for what the
  routine's next prompt revision needs to fix.
- `reconciliation_checks.py` only catches what a deterministic script
  can catch. Semantic duplicates and claim contradictions still need a
  human or a model reading the content, not a regex.

## How to use content_id.py

    python content_id.py new --brand BW --channel LI --date 2026-07-22
    python content_id.py new-thesis --date 2026-07-22
    python content_id.py check CONTENT-2026-29-EE-IG-01
    python content_id.py list

## How to use reconciliation_checks.py

    python reconciliation_checks.py
    python reconciliation_checks.py --root "C:/Users/User/Projects/BridgeWorks-Content-Studio"
