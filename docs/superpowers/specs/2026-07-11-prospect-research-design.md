# Prospect Research (NotebookLM) — Design

**Date:** 2026-07-11
**Status:** Approved, not yet implemented

## Problem

BridgeWorks has two prospect pipelines, and both have a manual research step:

- **Inbound** (`~/.claude/skills/lead-qualifier-skill/SKILL.md`): Step 3 enriches HOT/WARM leads via Apollo (firmographic data only — no market/competitor/pain-point research).
- **Outbound** (`pipeline/prospecting/prospecting-system.md`): Daily Workflow Step 2 ("Qualify") requires manually checking each raw prospect's website, Google Business Profile, LinkedIn, and contact page to write one specific signal per prospect.

Both steps currently rely on manual browsing/reading. NotebookLM's deep web research (`source add-research --mode deep`) can produce a structured briefing doc for a prospect in 15-30 minutes, in the background, without blocking either pipeline's existing timelines.

## Goals

- One reusable research step, callable from both pipelines, so the NotebookLM integration logic exists in exactly one place.
- Non-blocking: neither pipeline's existing response-time commitments (HOT lead reply within 2 hours; A-priority outbound message same day) change.
- Output lands as a file each pipeline already knows how to consume (research brief → feeds existing tracker columns / reply drafting), not a new UI or dashboard.
- No change to the existing free audit-preview PDF generation (`pipeline/prospecting/audit-previews/generate_geo_preview_pdf.py`) — this step only improves the raw research that feeds it.

## Non-goals

- Not building a trigger/automation layer (no Gmail/form watcher, no Composio). Both call sites remain manually invoked, matching how `lead-qualifier-skill` and the prospecting daily workflow are invoked today.
- Not replacing Apollo enrichment in `lead-qualifier-skill` — NotebookLM research runs alongside it, not instead of it.
- Not auto-chaining into `discovery-call-prep` or `client-audit` — the research brief is saved as a reference file; a human (or a future, separately-designed step) decides what to do with it next.
- Not changing prospect-tracker.csv or audit-preview-tracker.csv schemas.

## Design

### 1. New skill: `prospect-research`

Location: `~/.claude/skills/prospect-research/SKILL.md`

**Inputs:**
- `company` (required)
- `website` (required)
- `mode`: `inbound` | `outbound`
- `context`: the inbound lead message (inbound mode) or niche/market/city (outbound mode)

**Steps:**

1. **Find or create the notebook.** Run `notebooklm list --json` and look for a title match `Prospect: [Company]`. Reuse it if found (avoids duplicate notebooks when the same prospect is researched twice, e.g. re-qualified after a stale first pass). Otherwise `notebooklm create "Prospect: [Company]"`.
2. **Seed sources.** Add the prospect's website directly: `notebooklm source add "<website>" --notebook <id>`.
3. **Kick off deep research**, non-blocking: `notebooklm source add-research "<company> <city> <niche> competitors reviews" --mode deep --no-wait --notebook <id>`.
4. **Spawn a background agent** to:
   - `notebooklm research wait --import-all --timeout 1800 -n <id>`
   - `notebooklm source wait` on the seeded website source if not already ready
   - Generate the briefing doc with mode-specific instructions appended:
     - **inbound**: "Focus on: business overview, current digital presence gaps, likely pain points, and which BridgeWorks service fits best."
     - **outbound**: "Focus on: one specific visible signal, service value, decision-maker findability, and which outreach angle fits — website conversion leak, speed-to-lead risk, weak proof/trust signals, or AI visibility gap."
   - `notebooklm generate report --format briefing-doc --append "<mode instructions>" --notebook <id> --json`, then `artifact wait` and `download report`
   - Save the downloaded report to:
     - inbound: `pipeline/lead-qualification/research/[company-slug]-[date].md`
     - outbound: `pipeline/prospecting/runs/research/[company-slug]-[date].md`
   - Report completion back to the main conversation (standard Agent tool background notification) with a one-line summary and the file path.
5. **Return immediately** to the caller after step 3 — do not wait in the main conversation for steps 4's background agent.

**Error handling:** if any NotebookLM call in the background agent fails (rate limit, auth, generation failure), log it to the output file's expected path as a `.md` stub noting the failure and stop — do not retry automatically, do not block the caller. The caller pipelines already have manual fallback (this is what they do today).

### 2. `lead-qualifier-skill` change

Add **Step 3b** (after the existing Apollo Step 3), gated to HOT/WARM leads:

> Invoke `prospect-research` with `mode: inbound`, `context: <the lead's message>`. Do not wait for it. Continue immediately to Step 4 (Recommend a Service) and Step 5 (Draft Reply) using only what's already known from the lead + Apollo. When the background agent later reports the research file is ready, mention it as available follow-up context (e.g., for the actual call, not the first reply) and note the file path when appending to ACTION-LOG.

Apollo (Step 3) is unchanged — it still runs for firmographic data.

### 3. `prospecting-system.md` change

Amend **Daily Workflow → Step 2 (Qualify)**:

> For A and B priority raw prospects, instead of manually checking website/GBP/LinkedIn/contact page one by one, invoke `prospect-research` with `mode: outbound`, `context: <niche, city>`. Use the resulting research brief to write the `signal_found`, `growth_leak`, `offer_fit`, `recommended_service`, and `estimated_value` columns in `prospect-tracker.csv`, and as the source material for `preview_thesis` in `audit-preview-tracker.csv` and for drafting the outreach message (Step 4). Since research runs in the background (~15-30 min), continue qualifying other prospects in the same block rather than waiting — come back to write the tracker row once the file lands.

C priority and below: skip NotebookLM research, keep the existing lightweight manual pass (not worth the research cost for low-priority prospects).

## Data flow

```
Raw signal (inbound lead message, or outbound raw-list entry)
        │
        ▼
prospect-research skill
  - find/create "Prospect: [Company]" notebook
  - seed website source
  - deep web research (background)
  - briefing-doc report (background)
        │
        ▼
Saved .md file (pipeline/lead-qualification/research/... or pipeline/prospecting/runs/research/...)
        │
        ├── inbound  → referenced in ACTION-LOG + follow-up context (reply already sent using Apollo + message alone)
        └── outbound → prospect-tracker.csv columns + audit-preview-tracker.csv preview_thesis + outreach message draft
```

## Testing / validation

No automated tests — this is a skill/prompt design, not application code. Validation is a dry run against real data:

1. Pick one live A-priority prospect from `prospect-tracker.csv`, run `prospect-research` in outbound mode, confirm the file lands at the right path and its content is usable to fill the tracker row.
2. Pick one recent HOT or WARM lead (or a hypothetical one), run `prospect-research` in inbound mode alongside `lead-qualifier-skill`, confirm the draft reply still goes out without waiting on NotebookLM, and the research file arrives later with a completion notification.

## Open questions for implementation time

- Exact slug format for `[company-slug]` (lowercase, hyphenated, matching the existing `bridgeworks-audit-preview-[name]-[date].pdf` convention already used in `audit-previews/`).
- Whether `pipeline/lead-qualification/research/` and `pipeline/prospecting/runs/research/` directories need to be created (they don't exist yet).
