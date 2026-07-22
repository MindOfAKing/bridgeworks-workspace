# Automation and Scheduler Source Map

Version: 2.0
Updated: 2026-07-22
Owner: Emmanuel Ehigbai
Purpose: single reference for the persistent scheduler surfaces, who owns each one, where their source of truth lives, and the shared-write safeguards that keep them from colliding. Supersedes v1.0, which incorrectly listed Claude Code as a scheduler and described Codex as the only Command Center writer.

## Operating model

The **Emmanuel OS Command Center** (Google Sheet, ID `11HdcEaQqGW-TmdhOoJnfSXP4Mj0KxWLYUqFUYSMVwsc`) is the shared canonical operating system and source of truth. Several tools read and write to it in assigned lanes. No single tool owns it.

| Tool | Role | Command Center writes |
|---|---|---|
| Codex | Schema steward, automation manager, broad system updater, final reconciler | Primary writer and reconciler across tabs |
| Claude Code | Repository and local implementation worker | Scoped, evidence-backed updates via the approved local Google Sheets workflow |
| ChatGPT | Mobile cockpit and scheduled review layer | Explicitly assigned lanes when its connector supports the operation |
| Claude Cowork | Cloud operations and scheduled-routine layer | Assigned Sheet lanes or Drive outputs when the routine prompt authorizes it |
| Claude Projects | Strategy, synthesis, writing, project memory | Default output is a handoff or Drive memo; direct writes need an assigned lane |
| Gemini Gems | Google Workspace research, document comparison, fact-checking | Default output is a sourced handoff or Drive memo; direct writes need an assigned lane |
| Hermes | Local Windows automation runner | Through its jobs; not mobile-safe, not cloud-independent |

Hard rule: an output lane has one primary writer per workflow. Codex is the final reconciler when lanes overlap.

## Persistent scheduler surfaces

There are four systems that own live, recurring schedules. Claude Code is not one of them (see the implementation-role section below).

### 1. Claude Cowork cloud routines

Owned by Cowork. Run as claude.ai scheduled agents in the cloud. Not defined in this repository and not inspectable from Claude Code or Hermes. Confirm exact schedule, IDs, and live status inside claude.ai.

Confirmed routines:

- Daily Brief
- Inbound Prospect Triage
- YouTube Intelligence Digest
- Job Search OS
- Weekly Content Plan
- Weekly TODO Refresh
- Weekly Sales Review

Job Search OS, Weekly TODO Refresh, and Weekly Sales Review are confirmed Cowork-owned cloud routines.

Dashboard cleanup, informational: the old **Sunday Refresh** routine and **four fired one-off routines** may still be visible in the Cowork dashboard and require manual cleanup if so. Do not attempt to modify them from here; this is a note for Emmanuel to clear in claude.ai.

Claude Code must not create, edit, pause, or delete Cowork schedules. It may read their outputs.

### 2. ChatGPT Tasks, schedules, and Pulse-style monitoring

Owned by ChatGPT (OpenAI). ChatGPT is Emmanuel's mobile cockpit and scheduled review layer. IDs and exact cron expressions are not available locally. Live status requires verification in ChatGPT's task manager.

Separate functions acknowledged:

- Executive Brief
- Emmanuel Inbox Control
- Weekly Sales Review independent challenge (an independent second view, distinct from the Cowork Weekly Sales Review)
- Follow-up Monitor
- High-Value Job Watch
- Email Attention Watch
- Fitness and kitchen-related schedules
- Other personal routines shown in ChatGPT's task manager

Claude Code does not own or modify these. Verify live state in ChatGPT.

### 3. Codex automations

Owned by Codex. Source of truth is Codex's live local automation files at `C:/Users/User/.codex/automations`, one folder per automation, each holding `automation.toml` (definition and `status`) and `memory.md` (run history). This inventory was regenerated directly from those files on 2026-07-22. The older mirror `bridgeworks-codex/mobile-project-sources/codex-automations.md` (last mirrored 2026-05-21, the AUTO-001..AUTO-009 list) is STALE and does not match the live set; do not rely on it.

Live inventory: 14 automations, all cron-scheduled (exact expressions live in each `automation.toml`). 12 ACTIVE, 2 PAUSED. The two paused entries are duplicate folders (`-660627399970` suffix) of an active automation, carrying the same `created_at` as their active twin.

| Automation folder | Name | Status |
|---|---|---|
| `bridgeworks-automation-cockpit-router` | BridgeWorks Automation Cockpit Router | ACTIVE |
| `bridgeworks-automation-health-check` | BridgeWorks Automation Health Check | ACTIVE |
| `bridgeworks-automation-health-check-660627399970` | BridgeWorks Automation Health Check (duplicate) | PAUSED |
| `bridgeworks-founder-signal` | BridgeWorks Founder Signal | ACTIVE |
| `daily-brief-composer` | Daily Brief Composer | ACTIVE |
| `daily-knowledge-tutor` | Daily Knowledge Tutor | ACTIVE |
| `emmanuel-approved-application-pack-builder` | Emmanuel Approved Application Pack Builder | ACTIVE |
| `emmanuel-approved-application-sending-layer` | Emmanuel Approved Application Sending Layer | ACTIVE |
| `emmanuel-high-value-job-watch` | Emmanuel High-Value Job Watch | ACTIVE |
| `finance-signal-watch` | Finance Signal Watch | ACTIVE |
| `follow-up-monitor` | Follow-up Monitor | ACTIVE |
| `llm-intake-inbox-watcher` | LLM Intake Inbox Watcher | ACTIVE |
| `mailbox-control-tower` | Mailbox Control Tower | ACTIVE |
| `mailbox-control-tower-660627399970` | Mailbox Control Tower (duplicate) | PAUSED |

Paused duplicates to resolve: `bridgeworks-automation-health-check-660627399970` and `mailbox-control-tower-660627399970`. Confirm the active twin is the keeper, then retire the paused duplicate from the Codex dashboard (Codex owns that action; do not attempt it from Claude Code).

Codex safety rules (from `automation.toml` prompts): no send, reply, forward, archive, delete, mark-read, label, draft, pay, deploy, or external mutation without Emmanuel's explicit approval of that exact action. The application-sending-layer acts on at most one role and only with explicit submission approval, stopping on any CAPTCHA/MFA/assessment/ambiguity. Finance status needs evidence or user confirmation.

Note: none of the live Codex automations is a CEEFM client-delivery brief. The stale 2026-05-21 registry still lists one; that reference is obsolete and must not be revived. CEEFM is closed (2026-06-19).

### 4. Hermes local cron jobs

Owned by Hermes. Runs on this Windows machine only. Not mobile-safe and not cloud-independent. Live source of truth is `hermes cron list` and the per-job output under `C:/Users/User/AppData/Local/hermes/cron/output/<job_id>/`. The local private dashboard at `automation-reports-dashboard/` (gitignored) renders status; refresh with `python automation-reports-dashboard/refresh.py`.

A configured job is not a healthy job. Distinguish configured, enabled or paused state, last-run status, and blockers. As of the 2026-07-22 dashboard snapshot: 4 jobs are healthy (`ok`), 2 are paused with an explicit Google OAuth block (`invalid_grant` / `TOKEN_REVOKED`), and 8 are active but last ran with errors whose causes are mixed or unverified. Do not assume a single OAuth re-authorization fixes every Hermes job: it should clear the two OAuth-blocked paused jobs, but the eight active errors need per-job diagnosis (some captured no blocker text, one is a private-video error, one hit hard-blocked OS shortcuts). Gateway running/stopped state and any credit-related failures are not captured in the dashboard and need direct verification (`hermes gateway status`).

| Job | Schedule | State | Last-run status | Note |
|---|---|---|---|---|
| Daily Operating Brief | `0 6 * * *` | paused | ok (2026-07-15) | Blocker: OAuth `invalid_grant` |
| Inbox, Finance, Investments, and Lead Control Tower | `45 7,14 * * *` | paused | ok (2026-07-15) | Blocker: `TOKEN_REVOKED / invalid_grant` |
| Daily Knowledge Tutor | `25 8 * * *` | active | error (2026-07-22) | No blocker text captured |
| Automation Intake, Router, and Health | `0 */4 * * *` | active | error (2026-07-22) | No blocker text captured |
| YouTube Intelligence Digest | `0 7,19 * * *` | active | error (2026-07-22) | Private/unavailable video error; overlaps the Cowork YouTube Intelligence Digest. Codex YouTube work is on-demand, not a scheduled automation |
| Weekly Content Plan | `0 19 * * 0` | active | error (2026-07-19) | Overlaps Cowork Weekly Content Plan |
| BridgeWorks Opportunity Radar | `0 9 * * *` | active | error (2026-07-22) | No blocker text captured |
| BridgeWorks SYSTEMology Review | `0 16 * * 5` | active | error (2026-07-17) | No blocker text captured |
| Refresh Automation Reports Dashboard | every 30m | active | ok (2026-07-22) | Healthy |
| Daily Content Publishing Prep | `0 8 * * *` | active | error (2026-07-22) | Content pipeline; approval-gated |
| Daily Approved Browser Publisher | `45 8 * * *` | active | error (2026-07-22) | Publisher; some OS shortcuts hard-blocked |
| Life Ops Morning | `0 7 * * *` | active | ok (2026-07-22) | Healthy |
| Life Ops Midday | `0 12 * * *` | active | ok (2026-07-21) | Healthy |
| Life Ops Evening | `0 21 * * *` | active | ok (2026-07-21) | Healthy |

Not captured in the local dashboard and requiring direct verification: Hermes gateway running/stopped state (`hermes gateway status`), and whether any failures are credit-related rather than OAuth-related. Do not assume credit failures without evidence; the visible blockers here are OAuth-token revocation.

## Claude Code implementation role (not a scheduler)

Claude Code is the repository and local implementation worker. It owns this repo's code, skills, specs, scripts, and documentation. It can inspect and implement scheduler-related code, but it does not own or run any of the four persistent scheduler surfaces above and is not itself a persistent scheduler.

Claude Code is used through two interfaces:

1. Claude Code Desktop
2. Claude Code inside VS Code

These are two interfaces to the same Claude Code role, not separate automation owners or schedulers. Both may access the same local repositories, the global `C:/Users/User/.claude/` instructions, project `CLAUDE.md` files, local scripts, the Emmanuel OS update pathway, and the git working trees. Their conversation histories, current working directories, loaded project context, permissions, and active sessions may differ.

Two-interface safeguards:

- Inspect the current repository state at the start of every Claude Code session, regardless of interface.
- Read the same global and repository instructions in both interfaces.
- Do not assume work completed in Desktop is loaded into the VS Code conversation, or vice versa.
- Use session files, git status, git history, and Emmanuel OS receipts for handoff between interfaces.
- Never let Desktop and VS Code edit the same working tree concurrently.
- Before taking ownership of uncommitted changes, check whether another Claude Code process or session is actively editing that repository.
- Preserve uncommitted changes created through either interface.
- Record the interface used in receipts as "Claude Code Desktop" or "Claude Code VS Code".
- Ownership remains "Claude Code" unless the interface distinction is operationally relevant.
- Neither interface is a persistent scheduler.
- Do not confuse Claude Code Desktop with Claude Cowork cloud routines or Claude Chat Projects.

### Approved Command Center write pathway

Claude Code has previously written to the Command Center through `C:/Users/User/Projects/update_emmanuel_os.py`. This is not theoretical. A successful run updating the Projects, Finance, and Today tabs is recorded in the Claude Code transcript `C:/Users/User/.claude/projects/c--Users-User-Projects/9de79474-8a02-48c5-9d14-43dabf2f34a3.jsonl` (2026-06-12), and the global session-end protocol in `C:/Users/User/.claude/CLAUDE.md` makes this part of Claude Code's routine. Do not claim Claude Code has never written to the Command Center.

The script in its current form is a dated session update. It appends rows and is not safely idempotent. It is documented here as evidence of the approved Claude Code write pathway, not as a generic script to rerun unchanged. Do not run it as-is.

Before any future use it must:

- search by stable ID
- update existing rows
- refuse duplicate IDs
- preview planned changes
- limit writes to assigned tabs
- report every confirmed write
- avoid storing or printing credentials

## Five distinct systems (do not conflate)

These are different systems with different homes. Keep them separate in every report:

- **Cowork cloud Routines** — scheduled agents on claude.ai, identified by `trig_` IDs (e.g. the Weekly Content Plan trigger `trig_01JeovUEsbtcnGyNmRijfCry`). Cloud, not locally inspectable.
- **Codex automations** — cron definitions under `C:/Users/User/.codex/automations` (one folder each, `automation.toml` + `memory.md`). Local to this machine, run by Codex.
- **Claude Code Desktop and VS Code** — two interactive implementation interfaces of one Claude Code role. Not schedulers. They share files and the git worktree; never run competing write sessions at the same time.
- **Hermes** — a separate local Windows cron scheduler (`hermes cron`). Not the same as Codex automations, though both are local.
- **ChatGPT scheduled tasks** — a separate cloud scheduler (OpenAI), managed in ChatGPT's task manager. Not Cowork, not Codex.

## Shared-write safeguards

These apply to every tool that writes to a shared lane (Command Center tab or Drive output):

1. Every output lane has one primary writer per workflow.
2. Use stable record IDs.
3. Search for an existing record before appending.
4. Update existing records instead of creating duplicates.
5. Record the source, timestamp, writer tool, and evidence.
6. Never overwrite a confirmed fact with an inference.
7. Never change Sheet tabs, columns, formulas, IDs, or schema without Emmanuel's approval.
8. Finance status requires documentary evidence or explicit Emmanuel confirmation.
9. Email actions remain draft-only unless Emmanuel approves the exact send or mailbox mutation.
10. A successful run must produce a receipt stating: what was done, which sources were read, what changed, where the result was written, and what needs Emmanuel's approval.
11. If two systems write the same record or output lane, treat it as an ownership conflict to resolve.
12. Running the same business function in two systems is allowed when their roles and outputs are intentionally different. Do not classify all parallel coverage as duplication.

## Cross-system overlaps to resolve

These functions run in more than one scheduler. Each needs a decision on whether it is intentional independent coverage (different role/output) or harmful duplication (competing canonical output):

- YouTube intelligence: Cowork YouTube Intelligence Digest (scheduled cloud routine) + Hermes YouTube Intelligence Digest (local cron). Codex has no live scheduled YouTube automation among the 14 `.codex/automations`; its YouTube extraction and adoption work is run on demand inside Codex sessions (evidence: `pipeline/youtube-scout/`). The old "YouTube Intelligence And Adoption Engine" from the stale 2026-05-21 registry is not a live automation.
- Weekly content planning: Cowork Weekly Content Plan + Hermes Weekly Content Plan.
- Weekly Sales Review: Cowork Weekly Sales Review + ChatGPT Weekly Sales Review independent challenge (likely intentional independent review).
- Inbound/prospecting: Cowork Inbound Prospect Triage + Codex prospecting, inbound intake, and approval automations.

Resolution is deferred to the content and pipeline audits; do not silently retire any of them.
