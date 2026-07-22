# Agent Runbook: Cross-Model Content Cycle

Version: 1.1 (proposed)
Created: 2026-07-22
Owner: Emmanuel Ehigbai
Status: Proposed. Register in the Command Center `Agent Runbooks` tab through the approved write pathway after Emmanuel resolves the open decisions at the end of this file. Creating this runbook does not create a new schedule and does not replace any existing weekly plan.
Production HOLD: the BridgeWorks Content Studio is on a production hold (see `CREATIVE-DIRECTION-HOLD-2026-07-16.md`). Audit, strategy, copy drafting, scheduling proposals, and runbook work are allowed. Do not edit, replace, delete, or regenerate existing media. Do not publish.

Purpose: define how OpenAI, Anthropic, and Google tools collaborate on one content item without producing competing canonical outputs. One primary writer per item, deliberate handoffs, source links preserved, approval-gated publishing.

Related governance documents:
- `content-channel-model.md` — channel roles and amplification rules
- `content-90-day-rollout.md` — the proposed 90-day plan, service sequence, and content mix
- `mobile-publishing-pack-spec.md` — the cloud-first weekly pack structure and per-item fields
- `linkedin-audit-runbook.md` — the monthly LinkedIn measurement process and 2026-07-22 baseline
- `automation-source-map.md` — the four scheduler surfaces, Codex inventory, and shared-write safeguards

## Content source of truth

Use this hierarchy. Do not store canonical content in chat.

1. **Drive Content Studio** (Google Drive master folder `1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY`): the canonical portable content library. Cloud-first, phone-accessible, the source of truth for finished content and creative assets.
2. **Local Content Studio** (`C:/Users/User/Projects/BridgeWorks-Content-Studio/`): the production mirror and working structure. It reflects the Drive library; it is not a second canonical source.
3. **Emmanuel OS Command Center** (Google Sheet): content IDs, status, approval state, and evidence/source links. It stores status and links, not full long-form drafts.
4. **ChatGPT, Claude, and Gemini projects**: working environments and collaboration surfaces. They are not independent sources of truth. Nothing is final until written to the Drive/Local Content Studio or the assigned Drive document.

## Content ID

Every content item gets a stable ID: `CONTENT-YYYY-WW-BRAND-CHANNEL-NN`
(year, ISO week, brand code, channel code, sequence). Example: `CONTENT-2026-30-BW-LI-01`.

Each content record identifies: Content ID, brand, audience, channel, objective, campaign or weekly theme, primary writer, reviewing tools, factual sources, master-copy location, asset location, approval status, publishing status, publication URL, performance result, lesson to carry forward.

## Division of responsibility

**Gemini / Google** — research; search-trend and market-context discovery; source verification; question and objection discovery. No unsourced market claims. No canonical final-draft ownership.

**Claude Project / Cowork** — weekly editorial direction; master thesis and narrative; long-form reasoning; voice review; the weekly cloud-safe draft package. No direct publishing. No competing Content IDs.

**ChatGPT Project** — independent challenge; audience-clarity review; channel adaptation; hook and CTA alternatives; detect repetition, unsupported claims, and message mismatch. Do not independently rebuild the entire weekly plan.

**Codex** — the content operating system: Content ID registration, reconciliation, asset and format coordination, the Mobile Publishing Pack, the approval queue, publishing execution only after explicit approval, the measurement and learning loop, and cross-channel consistency. No auto-send or auto-publish without approval.

**Claude Code** — implements and maintains the file-based system; builds templates, schemas, validation, and production tooling. Does not independently decide what is approved for publication.

**Production tools** (Canva, HeyGen, HyperFrames, others) — create the approved visual or video asset; follow the Brand Assets record; return the final asset link and production receipt. Do not change approved factual claims or positioning.

## Collaborative content pipeline

1. **Research** — Gemini produces a source-backed research packet.
2. **Editorial direction** — Claude reviews the research and creates the weekly angle, narrative, audience promise, and master draft.
3. **Independent challenge** — ChatGPT checks: is the hook specific? is the claim supported? does it sound like Emmanuel? is it useful to the audience? is it different from recent posts? is the CTA appropriate? is anything overstated?
4. **Reconciliation** — the primary writer accepts or rejects each challenge with a short reason. Do not merge suggestions blindly.
5. **Channel adaptation** — ChatGPT or Claude creates the LinkedIn, X, newsletter, short-video, or other approved variants from the reconciled master.
6. **Production** — Codex, Claude Code, Canva, HeyGen, or HyperFrames creates the required files and assets.
7. **Approval** — Emmanuel receives one approval card: master copy, variants, source links, visual or video preview, proposed publishing date, and unresolved factual or brand questions.
8. **Publishing** — approval-gated. A preparation routine may create drafts. It must not publish automatically unless Emmanuel has explicitly authorized that exact publishing workflow.
9. **Learning** — performance data returns to the Command Center and Content Studio. Google analyzes evidence and trends. Claude extracts editorial lessons. OpenAI updates reusable prompts, runbooks, and production rules.

## Handoff responsibilities

- **Gemini research handoff**: sourced research pack to Drive or the assigned Context Packet, with links and publication dates.
- **Claude editorial handoff**: Claude prepares the editorial direction, master draft, and metadata, and writes them to the Content Studio. Claude does not write canonical Command Center rows directly; Codex registers the Content ID, status, and canonical links. (No verified Claude routine writes content rows to the Command Center today.)
- **ChatGPT challenge and channel-adaptation handoff**: challenge notes for reconciliation; approved variants back to the primary writer.
- **Codex reconciliation and system-update**: registers the Content ID, status, and canonical links; reconciles final state; validates cross-tool handoffs; assembles the Mobile Publishing Pack and the approval queue.
- **Claude Code Desktop and VS Code implementation**: content systems, scripts, templates, file structures, production tooling. Both interfaces are the same role; hand off through session files, git, and Command Center receipts. Never edit the same working tree concurrently.
- **Production-tool handoff**: approved asset link + production receipt against the Brand Assets record.
- **Emmanuel approval gate**: one approval card before publishing.
- **Publishing receipt**: what was published, where, the URL, and what remains.
- **Performance-learning loop**: results to Command Center + Content Studio; lessons to the Prompt Library and this runbook.

## Collaboration rules

- Do not ask all three model families to create full competing drafts by default. Assign one primary writer per content item; use the others for research, challenge, adaptation, or production.
- Preserve source links through every handoff. A reviewer must not silently replace the primary draft. Every accepted material change is reflected in the canonical master copy.
- Working chat output is not final content until written to the Content Studio or the assigned Drive document.
- The Command Center stores status and links, not full long-form drafts.
- No CEEFM content unless it is an approved, anonymized BridgeWorks case-study reference. CEEFM is not an active client.
- Content involving current clients, financial results, testimonials, or performance claims requires supporting evidence.
- Voice: no em dashes, no AI filler, no unsupported superlatives. Short sentences, specific examples, real numbers, real timelines.
- Publishing, client-facing sends, paid promotion, and public claims require approval.

## Schedule ownership (existing content routines)

Audit before proposing any new content schedule. Do not create a new content schedule during this cycle setup. Scheduler details and health are in `operations/automation-source-map.md`.

| Routine | Scheduler | Schedule | Primary output | Canonical destination | Approval | Recommendation |
|---|---|---|---|---|---|---|
| Weekly Content Plan (content-week-bot) | Cowork (primary) | Sun 19:00 | 9-post weekly plan | `personal-brand-workspace/content/` + Sheet Queue | Yes | Primary weekly editorial trigger. Any Hermes weekly-content duplicate is a pause candidate after direct verification |
| WEEK-NN Authority Queue | Codex (client-acquisition-engine) | Weekly, manual | Authority-angle inputs | `operations/client-acquisition-engine/content/` | Yes (drafts only) | Feeder into the Cowork weekly plan. Must not generate a competing weekly plan |
| Daily Content Publishing Prep | Hermes | `0 8 * * *` | Staged drafts | needs verification | Yes | Verify script + health (last run errored 2026-07-22) |
| Daily Approved Browser Publisher | Hermes | `45 8 * * *` | Published posts via logged-in Chrome | Live channels | Yes, explicit | Verify approval gate; last run errored |
| YouTube Intelligence Digest | Cowork (scheduled cloud discovery + digest); Codex extraction on demand (not scheduled) | Cowork: `0 7,19 * * *`; Codex: on demand | yt-digest-*.md + Gmail draft | Cowork digest cloud; Codex extractions to `pipeline/youtube-scout/sessions/` | Draft only | Cowork owns the scheduled discovery/digest. Codex handles deeper extraction/adoption/registration on demand in Codex sessions (no live scheduled Codex YouTube automation). Any Hermes duplicate is a pause candidate after verification |

## Resolved ownership (decided)

- **Weekly plan**: the Cowork Weekly Content Plan (trigger `trig_01JeovUEsbtcnGyNmRijfCry`) is the single primary weekly editorial trigger. The client-acquisition Authority Queue is a feeder and must not generate a competing weekly plan. Any Hermes weekly-content duplicate is a pause candidate after direct verification.
- **YouTube**: Cowork owns the scheduled cloud discovery and digest (the live YouTube Intelligence Digest routine). Codex handles deeper extraction, adoption decisions, and operational registration on demand inside Codex sessions; there is no live scheduled Codex YouTube automation among the 14 `.codex/automations` (evidence: `pipeline/youtube-scout/`). Any Hermes YouTube duplicate is a pause candidate after verification.

## Open decisions (require Emmanuel)

1. **Confirm the Hermes pauses**: after verifying `hermes cron list`, decide whether to pause the Hermes "Weekly Content Plan" and "YouTube Intelligence Digest" duplicates. Do not pause without verification.
2. **Stale Codex plugin skill**: `bridgeworks-codex/plugin/skills/content-week/SKILL.md` still plans 12 posts including CEEFM, contradicting the CLAUDE.md CEEFM rule and the current global skill. Correct or retire it (separate task).
3. **Content Studio HOLD**: production is on hold pending music direction; drafting/analysis allowed. Confirm when to release.

## Consistency and reconciliation

Detect and reconcile before anything is treated as canonical:

- One Content ID per platform-specific unit; one Master Thesis ID linking related units.
- Origin channel and amplification channel recorded per unit.
- Exact-duplicate detection (same copy in two records).
- Semantic-duplicate detection (same message reworded).
- Claim-contradiction detection (two units make incompatible claims).
- Stale-client detection (CEEFM or any closed client re-entering a queue).
- Old-date and old-launch-language detection (obsolete positioning, superseded prices, past dates).
- Simultaneous-writer detection (two systems or two Claude Code interfaces writing the same lane).
- Approval-state conflict detection (published while not approved, or approved twice differently).
- Published-URL reconciliation (record the live URL against the Content ID).
- Analytics backfill (attach performance to the Content ID after publishing).

The old BridgeWorks Content Planner (Google Sheet `1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew`) is historical evidence; its Analytics tab is currently empty. Do not silently treat that planner as the complete current system.
