# BridgeWorks Workspace - Consulting Operations

## Project Overview
BridgeWorks is an AI-Powered Digital Growth Studio serving small businesses across Africa and Central Europe. Services: Digital Growth Strategy, AI-Powered Marketing, Brand Identity, Web Design & Development, AI Business Automation. Operating model: solo founder + AI skills stack, with paid engagements tracked per client.

## Repository
GitHub: `MindOfAKing/bridgeworks-workspace`. Default branch: `main`. Do not assume or clone an unspecified default/feature branch — always target `main` unless a specific task explicitly names another branch.

## Operating model and ownership

The **Emmanuel OS Command Center** (Google Sheet) is the shared canonical operating system and source of truth. Several tools read and write to it in their assigned lanes. No single tool owns it.

- **Codex** is schema steward, automation manager, broad system updater, and final reconciler for the Command Center.
- **Claude Code** is the repository and local implementation worker (this repo, skills, specs, scripts, docs). It may make scoped, evidence-backed Command Center updates through the approved local Google Sheets workflow (`C:/Users/User/Projects/update_emmanuel_os.py`). It is used through two interfaces, Claude Code Desktop and Claude Code VS Code; both are the same role, not separate owners or schedulers.
- **ChatGPT** is the mobile cockpit and scheduled review layer. It writes only to explicitly assigned Command Center lanes when its connector supports the operation.
- **Claude Cowork** is the cloud operations and scheduled-routine layer. It writes to explicitly assigned Sheet lanes or Drive outputs when the routine prompt authorizes it.
- **Claude Projects** handle strategy, synthesis, writing, and project memory. Default output is a structured handoff or Drive memo; direct Sheet writes require an assigned lane.
- **Gemini Gems** handle Google Workspace research, document comparison, and fact-checking. Default output is a sourced handoff or Drive memo; direct Sheet writes require an assigned lane.
- **Hermes** is the local Windows automation runner. It is not mobile-safe and not cloud-independent.

Claude Code is not a persistent scheduler. It can inspect and implement scheduler-related code, but it does not own the live Cowork, ChatGPT, Codex, or Hermes scheduler surfaces. The persistent scheduler surfaces, shared-write safeguards, and the two-interface handoff rules are mapped in `operations/automation-source-map.md`.

## Active Clients
- **Oliviks**: Foundation engagement (Foundation-only scope per contract dated 29 April 2026). Website rebuild + Google Business Profile optimization + email/WhatsApp infrastructure. Total fee 272,611 HUF, paid in full (deposit invoice EO-2026-11 in June; balance invoice EO-2026-13 for 136,305 HUF). Foundation delivery is complete on the BridgeWorks side. The one remaining gate is client-side: cutover of `oliviks.com` to the new site is pending Aese's approval (cutover approval requested 2026-07-13). Contact: Aese Agaigbe, olivikskitchen@gmail.com (also agaigbeaese@gmail.com). Client folder: `clients/oliviks/`

## Past Clients
- **CEEFM Kft**: 16-week digital growth engagement, late March to June 2026. **Closed 2026-06-19.** Contract terminated June 2026. Final GEO score 77/100 at the 2026-06-10 audit (from 16); 78 on 2026-06-11 after post-handover fixes; source of truth: `clients/ceefm/VERIFIED-FACTS.md`. Contract was 16 weeks, terminated by client at week 9; public phrasing is "engagement, March to June 2026", never "16-week" or "completed". Case study: named use approved 2026-07-14 for bridgeworks.agency; client-sensitive internals stay private. **CEEFM must not appear as an active client in any routine, skill, or report unless newer dated evidence (after 2026-06-19) shows Emmanuel reactivated the engagement.**

## What Lives Here
- `clients/` - Client-specific folders with deliverables, trackers, case studies
- `pipeline/` - Sales pipeline and lead tracking
- `knowledge/` - Research and reference materials
- `documents/` - Proposals, agreements, reports
- `scripts/` - Automation scripts
- `sessions/` - Session logs
- `skills-drafts/` - Skills in development

## Brand Rules
- No em dashes. No AI slop. Short sentences. Specific over general.
- See business-brain for full brand system.

## Pricing Reference
- Full rate card and pricing rules: `C:/Users/User/Projects/business-brain/context/finances.md`
- Rule: Never discount without reducing scope. Lead with bundles. NGN rates are not discounts.

## Sibling Locations
| Location | Purpose |
|----------|---------|
| `C:/Users/User/Projects/business-brain/` | Central business context and orchestration |
| `C:/Users/User/Projects/bridgeworks-agency/` | Live website (React/Vercel) |
| `C:/Users/User/Projects/BridgeWorks-Content-Studio/` | Content studio: production mirror of the canonical Drive content library (currently on production HOLD) |
| `C:/Users/User/Projects/bridgeworks-codex/` | Codex operating setup, automation registry, and mobile-project sources |
| `C:/Users/User/Projects/personal-brand-workspace/` | Emmanuel personal brand |
| `C:/Users/User/Projects/mindofaking-workspace/` | MindOfAKing creative brand |
| `C:/Users/User/Projects/brand-assets/` | Original brand asset library |

## Key References
- Business brain: `C:/Users/User/Projects/business-brain/CLAUDE.md`
- Brand guide: `C:/Users/User/Projects/business-brain/context/brand/bridgeworks/`
- Playbooks: `C:/Users/User/Projects/business-brain/context/playbooks/`
- Global instructions: `C:/Users/User/.claude/CLAUDE.md`

## Working agreement

Behavioral rules for this workspace come from the global Working Agreement at `C:/Users/User/.claude/CLAUDE.md`. This file only holds BridgeWorks-specific context.

---

## Live operating state

This section is the single source of truth for what's active and what this week needs to produce. I update it at end of day in under 5 minutes. Any chat that contradicts this section is working from stale context — say so, do not work around it.

**Last updated:** 2026-07-22

### Ventures — active this month

| Venture | Status | This month's work |
|---|---|---|
| Bridgeworks (agency) | Active — primary focus | Backend buildout to run as a fully-formed agency; lead generation |
| Oliviks (paid client) | Active — paid in full; Foundation delivery complete on the BridgeWorks side | One remaining gate: client-side cutover of `oliviks.com` to the new site, pending Aese's approval (requested 2026-07-13) |
| CEEFM (closed client) | Terminated June 2026 | Finalize and send handover doc, then archive |
| Street Kitchen (EV income, not Bridgeworks) | Active — recurring | Monthly cleaning contract; no new effort needed |
| emmanuelehigbai.com | Active — priority build | Build and launch this month; feeds Bridgeworks credibility |
| Build Brief (multilayer prompt builder) | Active — lives on Claude for now | Positioning question deferred (personal tool vs service offering) |

### Ventures — parked (revisit when Bridgeworks is stable)

DanubeGold Agri · VeriCrop · MindOfAKing build work · JHU Agentic AI program · the older "AI competitive intelligence platform" positioning in `bridgeworks-workspace/CLAUDE.md`.

Nothing is killed. No work happens on these until Bridgeworks is stable. If a chat tries to revive any of them before then, point it at this file.

### Open loops — decisions this week

| Loop | Decision | By |
|---|---|---|
| Stripe | Finish live setup OR archive until a signed proposal needs it | Friday |
| Hunter + Tomba + Apollo (three overlapping prospecting tools) | Pick one; kill the other two. Default: keep Apollo | Friday |
| Blotato | Continue or cancel — nothing publishing through it yet | End of month |
| CEEFM React dashboard artifact (1,158-line JSX) | Archive as sales demo, absorb into bridgeworks-workspace, or delete | End of week |
| Old BridgeWorks repo CLAUDE.md positioning | Rewrite to match agency positioning | Before next Claude Code session on that repo |
| CEEFM handover doc | Review draft, fix internal score inconsistency, send to Victor | This week |
| Oliviks cutover | Foundation build complete and balance paid. Only gate left is client-side: Aese approves the `oliviks.com` domain cutover to the new site (requested 2026-07-13). No BridgeWorks-side blockers remain | Pending Aese |
| CEEFM stale references | CEEFM is closed (2026-06-19) but still appears in stale artifacts: the 2026-05-21 `bridgeworks-codex` codex-automations.md registry lists a CEEFM Client Delivery Brief (no such automation exists in live `.codex/automations`), and `bridgeworks-codex/plugin/skills/content-week/SKILL.md` still plans CEEFM posts. Purge both. Archived CEEFM content must never re-enter active publishing queues | Separate task |
| Oliviks launch.json stale path | `clients/oliviks/.claude/launch.json` still points the bridgeworks-agency dev target at `C:/Users/User/bridgeworks-agency` (stale clone; canonical is `C:/Users/User/Projects/bridgeworks-agency`). Executable/config path migration, needs targeted testing; do not edit inline | Separate migration |
| Codex paused duplicates | `.codex/automations` has two paused duplicate folders (`bridgeworks-automation-health-check-660627399970`, `mailbox-control-tower-660627399970`). Confirm active twin is keeper, retire duplicates from the Codex dashboard | Codex |

### This week — single best close

**Backend setup to launch Bridgeworks as a running agency.** Definition of done (all four true):

1. A contact form submission on bridgeworks.agency arrives somewhere I see within 5 minutes
2. I can go from signed proposal to invoice in under 10 minutes
3. One screen shows: inbound pipeline, active client status, today's work
4. emmanuelehigbai.com is live OR has a confirmed build start date within 7 days

Nothing gets built this week that doesn't serve one of those four.

### Daily catcher (5 min, end of day)

Append to the log below. Never delete history.

```
### YYYY-MM-DD
- Closed: [what got done today]
- Opened: [what got started that now belongs to a loop, or is a new loop]
- Tomorrow's one: [the single most important move for tomorrow]
```

Friday review: revisit "This week's single best close" — did the four items move?

### Daily log

<!-- Append entries here. Most recent at top. -->

### 2026-07-22
- Closed: Corrected operating-model docs. Fixed ownership model (Command Center is shared canonical, not Codex-exclusive; Claude Code writes via approved local script). Rewrote `operations/automation-source-map.md` to map the four real scheduler surfaces (Cowork, ChatGPT, Codex, Hermes) plus a Claude Code implementation-role section. Refreshed Oliviks status (paid in full, Foundation complete, cutover pending Aese). Live-website path corrected to `Projects/bridgeworks-agency`.
- Opened: Active-script ELITEX21012G2 path migration (separate task, needs targeted testing). Hermes health degraded: 2 jobs are paused with an explicit revoked-Google-OAuth blocker. Eight active jobs last errored for mixed or unverified reasons and require per-job diagnosis. Do not assume one OAuth repair fixes all Hermes jobs. Cowork dashboard cleanup: old Sunday Refresh + four fired one-offs may still be visible.
- Tomorrow's one: Re-authorize Google OAuth for the two explicitly blocked Hermes jobs, diagnose the eight active errored jobs individually, then run the ELITEX path migration with tests.

### 2026-06-10
- Closed: New machine migration audit (9 connectors, plugins, Vercel, Notion all verified working); CEEFM closed out in CLAUDE.md and Notion Pipeline CRM
- Opened: CEEFM handover doc, finalize and send to Victor. Oliviks engagement live, half deposit paid, scope and deal value need recording. Scheduled tasks and artifacts wiped by migration, rebuild list needed.
- Tomorrow's one: review and send CEEFM handover doc

### 2026-04-23
- Closed: CLAUDE.md rollout across 5 repos + global + Drive reference; Bridgeworks Financial Tracker uploaded to 05 - Finance & Admin; BridgeWorks repo positioning aligned with live site
- Opened: (none)
- Tomorrow's one: backend setup work — pick one of the four DoD items and close it
