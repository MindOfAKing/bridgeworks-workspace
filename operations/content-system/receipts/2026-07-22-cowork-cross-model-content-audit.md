# Cowork Audit — Cross-Model Content System — 2026-07-22

Scope: live Cowork cloud routines, Drive Content Studio, historical planner, Command Center content lane. Read-only. No routine created, edited, paused, or deleted. No media touched. Nothing published. This audit runs in parallel with a same-day Claude Code Desktop audit found already in progress (see Section 0) — this report cross-checks that work rather than duplicating it, and adds direct verification Claude Code Desktop could not do from its position (live Cowork trigger inventory, Gmail, Calendar).

Confidence tags: [Certain] = directly observed primary evidence (trigger prompt text, live Sheet/Doc content, Gmail/Calendar API result, git log in the cloned repo). [Likely] = strong inference or a same-day independent source I could not personally re-verify. [Guessing] = filling a genuine gap.

## 0. Work already in progress — name it before adding anything new

A Claude Code Desktop session ran a nearly identical audit **today**, 2026-07-22, and left a receipt at `content-system/receipts/2026-07-22-claude-code-desktop-content-audit.md` in Drive (file ID `19kWpgXl9ot3p8C-_4Jaf_zmXN_d2xo3I`), which is why this doc sits in the same `receipts` folder. That session:

- Committed the six governance docs this audit reads (`operations/*.md`, commit `0d02891`, "docs: align automation ownership and cross-model content operations").
- Built (uncommitted, awaiting Emmanuel's approval) `bridgeworks-workspace/operations/content-system/`: `content_id.py`, `reconciliation_checks.py`, `registry/content-id-ledger.csv`, `registry/master-thesis-ledger.csv`, nine template files, and a reconciliation manifest.
- Found, independently of this audit: the Content ID scheme is used nowhere yet; the July 19 weekly-plan run's claimed git push to `personal-brand-workspace` does not check out; a messaging-core doc misquotes the ICP doc; four live site surfaces still carry the pre-2026-07-14 SME/CEE framing; three unreconciled service-taxonomy versions exist.
- Explicitly left the open governance decisions (end of `cross-model-content-cycle-runbook.md`) untouched, for Emmanuel.

Everything below either confirms, extends, or — in a few places — corrects that session's findings with evidence it didn't have access to (live trigger IDs, actual Gmail drafts, actual Calendar events).

## 1. Live routine inventory (Cowork, `list_triggers`, read 2026-07-22)

12 triggers total. Matches `automation-source-map.md`'s "Confirmed routines" list exactly — no undocumented routine exists.

| Routine | ID | Cadence (UTC) | State |
|---|---|---|---|
| Weekly Content Plan | `trig_01JeovUEsbtcnGyNmRijfCry` | `0 17 * * 0` (Sun 19:00 Budapest) | enabled |
| YouTube Intelligence Digest | `trig_017e3rRcK9w24cBTJ9xzA8o6` | `0 5,17 * * *` daily | enabled |
| Weekly TODO Refresh | `trig_01A7RhAi6AShBKnL8ajM1edR` | `0 16 * * 0` | enabled |
| Weekly Sales Review | `trig_017v9msaRXA52YawFXw27L8R` | `30 5 * * 1` | enabled |
| Inbound Prospect Triage | `trig_01GZoPVjfcH185jcsGBAMxwm` | `0 5,12 * * 1-5` | enabled |
| Daily Brief - Emmanuel | `trig_01SUPtcsyHqGHjDoYvUv62d6` | `0 4 * * 1-5` | enabled |
| Job Search OS — Discovery & Scoring | `trig_01HsideE4vf4iz3iHe5b9F8w` | `0 6 * * 2,5` | enabled |
| Sunday Refresh - TODO + Next Content Week | `trig_01HPBodf1RzMLpyWsmQXisze` | `0 16 * * 0` | **user-paused** (`enabled: null`, no `ended_reason` — matches `automation-source-map.md`'s "old Sunday Refresh routine... requires manual cleanup") |
| 4 one-off CEEFM/calendar-fix triggers | — | run-once | all `ended_reason: run_once_fired` |

[Certain] This is a clean match to governance's documented inventory. No pause/edit/delete performed.

## 2. Weekly Content Plan — assessment

**Trigger:** `trig_01JeovUEsbtcnGyNmRijfCry`, Sun 17:00 UTC / 19:00 Budapest, enabled. [Certain]

**Destinations (from the live prompt, verbatim):** `personal-brand-workspace/content/CONTENT-WEEK-[date].md` + `temp-week-queue.json` (git commit/push), 9 Google Calendar events on the primary calendar, one Gmail draft to emmanuelehigbai@gmail.com. It does **not** write to the Historical Planner Sheet directly — the Gmail draft body hands Emmanuel a manual command (`python append-to-planner.py --tab Queue --file temp-week-queue.json`) to push the Sheet Queue tab himself. It does **not** touch the Command Center (Sheet or Drive) at all. It does **not** write anywhere inside the canonical Drive Content Studio folder (`1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY`). [Certain, read from the live prompt text]

**Exactly one primary plan per run — yes, structurally.** One CONTENT-WEEK file, one Gmail draft, one calendar batch per firing. But see Section 6: two consecutive runs collided on the same date.

**Excludes CEEFM — yes**, by explicit instruction ("DO NOT generate CEEFM posts... CEEFM has its own separate Month-by-month content calendar"). One caveat: the prompt's own framing still reads "One active client: CEEFM Kft... 16-week engagement" — stale language contradicted by every other CEEFM-status source (see Section 8). It doesn't cause CEEFM content to be generated, but it's the wrong mental model going into theme derivation.

**Post count: nine, not twelve.** 4 Personal LinkedIn + 2 BridgeWorks LinkedIn + 3 Twitter/X = 9. [Certain, read from the live prompt, and confirmed against the actual July 19 session log and Gmail draft, which both list exactly 9.] A **separate, different system** — `bridgeworks-codex/plugin/skills/content-week/SKILL.md` — is flagged in `cross-model-content-cycle-runbook.md`'s open decisions as still defaulting to a 12-post plan that includes CEEFM. That file is not reachable from this session (it isn't in the `bridgeworks-workspace` repo). Claude Code Desktop's own `scheduler-source-map-2026-07-22.md` separately claims a **different** file, `.claude/skills/content-week/SKILL.md`, has already been corrected. These are two distinctly-pathed files with the same filename — one claimed fixed, one still flagged stale, in two documents written the same day. [Likely — I could not independently open either file to settle it. Flagging the disagreement rather than picking a side, per your rule.]

**Canonical sources it actually reads:** `bridgeworks-workspace/sessions/` (5-7 most recent), `bridgeworks-agency/sessions/` (3-5 most recent), `bridgeworks-workspace/TODO.md`, `bridgeworks-workspace/brand-constants.md`, `personal-brand-workspace/content/CONTENT-WEEK-*.md` (most recent, as voice reference), and the Historical Planner Sheet's Queue tab (`1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew`) for dedup only. It never reads the Drive Content Studio, never reads the Command Center. [Certain]

**Channel coverage vs. the newly-proposed channel model:** the live routine covers 3 of the 10 channels in `content-channel-model.md` (Personal LinkedIn, BridgeWorks LinkedIn, Twitter/X). It has no awareness of Personal/BridgeWorks Instagram, Personal/BridgeWorks Facebook, Nigerian WhatsApp Status, or Hungarian WhatsApp Business prep — because it was built 2026-04-21, three months before the channel model existed (`content-channel-model.md` is dated 2026-07-22, status "proposed"). It also treats Twitter/X as always-on every week, where the new channel model reserves X for "days 31-60" of a 90-day rollout that hasn't been approved or started. This isn't a bug in the routine — it predates the standard it's now being measured against. It is a real gap between what's live and what you're asking this audit to check it against.

## 3. Drive Content Studio — assessment

Folder `1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY` has the top-level structure its own `README.md` describes: `00_Project_Core` through `09_Performance_And_Learning`, plus `99_Superseded`. [Certain, listed directly]

- **Populated:** `00_Project_Core` (README, PROJECT-INSTRUCTIONS.md, PLATFORM-PROJECTS.md, CONTENT-CONSISTENCY-AND-ASSET-CONTRACT.md, START-HERE.md, a Platform_Upload_Pack with brand books/logos, a CONTEXT-MANIFEST.csv) and `02_Strategy_And_Messaging` (9 files: brand books, FOUNDER-MIND-OPERATING-SYSTEM.md, CREATIVE-DIRECTION-HOLD-2026-07-16.md, CONTENT-STRATEGY.md, bridgeworks-icp-v1.md, and more).
- **Effectively empty:** `04_Content_Briefs`, `06_Production`, `07_Review_And_Approval`, `08_Approved_Masters`, `09_Performance_And_Learning` each contain only their one-paragraph `README.md` stub. No actual briefs, no production files, no approved masters, no performance records.
- **No `YYYY-MM-DD Weekly Pack` folders exist anywhere** — the structure `mobile-publishing-pack-spec.md` defines. Expected: that spec is dated today and marked "Specification only... does not create the pack." Not a defect, just confirming zero implementation so far.

**Verdict on item 11:** the skeleton matches the committed structure. The skeleton is not populated. None of the actual weekly content the Weekly Content Plan routine produces lands here — it lands in a git repo and a separate personal Drive mirror (see Section 6), outside the folder governance calls the canonical source of truth. [Certain]

## 4. Historical Planner — assessment (Sheet `1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew`)

Five tables inside the one Sheet (tab names not independently confirmed — Drive's export flattens tab boundaries; inferred from column headers):

- **Queue** (`Date | Platform | Content Type | Topic | Hook | Copy (EN) | Copy (HU) | Status | Posted By | Notes`): 69 rows, dates 2026-04-03 → **2026-06-30**. Per-week counts are irregular (1 to 14 rows/week) — only one week actually has a clean 9-row batch. Nothing scheduled past 2026-06-30, meaning **the Sheet has no record of the July 14-20 or July 20-26 weeks at all**, despite both having Gmail drafts and Calendar events (Section 6). 11 CEEFM rows exist, all `Status = Archived` — correctly retired, not live. Copy (HU) is blank on 59 of 69 rows (85%). Only 2 of 69 rows are marked `Posted`.
- **Analytics tab: confirmed genuinely empty** — headers only (`Date | Platform | Post | Impressions | Comments | Clicks | Reach | Notes`), zero data rows. This matches the runbook's claim, and it's independently verified here, not just repeated.
- **Idea bank** (199 rows, `Date Added | Topic | Source | Priority | Used?`): every row blank except `Used? = FALSE`. Unused template.
- **CEEFM weekly calendar**: only 12 of 99 rows have real content (Weeks 1-4, April). Two of those weeks still show `Posted? = FALSE` despite being three months past.
- **Client schedule**: one row, still lists CEEFM Kft as an active 3-posts/week client with "Next Post Due" frozen at 2026-04-01 — never updated after closure.

**Verdict:** this Sheet is stale evidence, not a live system component. It confirms governance's own framing ("historical evidence... do not treat as the complete current system") rather than contradicting it. [Certain]

## 5. Command Center content-lane — assessment (Sheet `11HdcEaQqGW-TmdhOoJnfSXP4Mj0KxWLYUqFUYSMVwsc`)

30 tabs. **No Content ID lane exists anywhere.** Grepped the full sheet for `CONTENT-2026`, `-BW-LI-`, `-BW-IG-`, and "Content ID" — zero matches. No tab has an approval-status, publishing-status, or content-link column. This is a genuine structural gap, not a search miss — it directly confirms the runbook's own line: "No verified Claude routine writes content rows to the Command Center today." [Certain]

An **Agent Runbooks** tab does exist (`Runbook ID | Name | Status | Routine Type | Owner Tool | Trigger | Goal | Inputs | Process | Writes To | Approval Gate | Failure Behavior | Source Evidence | Mobile Command | Last Reviewed | Notes`), with exactly 3 rows registered (RUN-001 Daily Brief Composer, RUN-002 Finance Sentinel, RB-2026-06-08-KNOWLEDGE-TUTOR). The new cross-model runbook has not been registered there — expected, since its own status line says registration happens "after Emmanuel resolves the open decisions."

CEEFM closure date is **inconsistent across the Command Center's own rows**, not just across outside systems: a Projects-tab row says "Last Updated: 2026-06-19... no longer an active client"; a fuller, more detailed Projects row says "8-week engagement completed 2026-06-11"; the Finance row says "engagement ended 2026-06-11... after 16-week delivery" (which is internally contradictory: 8-week vs. 16-week in the same row). `bridgeworks-workspace/TODO.md` (in the repo) independently says "closed 2026-06-19." **I'm flagging this as an open disagreement rather than picking a date** — every source agrees CEEFM is closed and out of scope; they disagree by 8 days on exactly when, and by a factor of two on the stated engagement length.

The GEO-score figure also disagrees across sources: Command Center's detailed Projects row says 16→78; `TODO.md` and the Codex Authority Queue draft (which explicitly "corrects" this) both say 16→77, with 78 flagged as an unreproduced interim reading. [Certain — I read the actual correction language in `WEEK-01-AUTHORITY-QUEUE-2026-07-20.md`.] Treat 77 as the number with the paper trail behind it.

A Codex automation, `AUTO-002 "CEEFM Client Delivery Brief"`, still shows `Status: Active` as of 2026-05-21 — pre-dating closure by weeks. Outside this sheet, Codex's own live `.codex/automations` inventory (per `automation-source-map.md`) says no CEEFM automation exists among the current 14 — meaning this specific stale row may already be superseded, but the sheet itself still shows it active. Not resolved here; flagged for Codex.

## 6. Competing or duplicate outputs

**A real one, found by direct verification, not by reading governance:** the Weekly Content Plan routine collided with itself across two consecutive runs.

- Run on 2026-07-09 (session `2026-07-09-content-week-bot.md`) produced `CONTENT-WEEK-2026-07-14.md`, a Gmail draft (`r1094783331791917145`, confirmed live in Gmail), and calendar events for Jul 14–20 — including a Personal LinkedIn post "Month 3 of agency life" placed on **2026-07-20** (mislabeled "Sun" in that draft; 2026-07-20 is actually a Monday).
- Run on 2026-07-19 (session `2026-07-19-content-week-bot.md`) produced `CONTENT-WEEK-2026-07-20.md`, a Gmail draft (`r-394021362354165501`, confirmed live in Gmail), and calendar events for Jul 20–26 — including a **different** Personal LinkedIn post, "Six rounds in one day," also placed on **2026-07-20** at 09:00 (the July 9 run's post sits at 10:00 the same day).

Both calendar events are confirmed live via the Calendar API [Certain] — this is not a hypothetical. **Root cause:** the routine's only duplicate-check is the Historical Planner Sheet's Queue tab, and that tab hasn't been updated since 2026-06-30 (the manual `append-to-planner.py` step was never run for either week). So the July 19 run's dedup check ("Queue tab reviewed... nothing scheduled for July 20-26... no duplicates") was checking a source that was already three weeks stale and blind to the Calendar and to the un-pushed July 9 draft. Two Personal LinkedIn posts are now live on your calendar for the same day with different hooks. This is a direct, evidenced answer to audit items 3 and 10 — not a governance-doc citation, something I found by checking Gmail and Calendar directly.

**The claimed personal-brand-workspace push for the July 19 run is disputed, not confirmed.** The session log says "Committed and pushed to personal-brand-workspace main (commit: 31070fc)." Claude Code Desktop's same-day audit ran `git cat-file -t 31070fc` directly against that repo and got "Not a valid object name" — the commit does not exist there. [Likely — I could not reproduce this myself; `personal-brand-workspace` is a private repo I have no credentials for, and it isn't one of the canonical sources this audit was scoped to read.] What I *could* independently confirm: the Drive mirror of that repo's `content/` folder (folder `1xnwlDgESEwz-MzfvK0t17Df3PAujZa9q`) has files through `CONTENT-WEEK-2026-06-29.md` and nothing for 07-06, 07-13, or 07-20 — consistent with, though not proof of, the push having failed. Calendar and Gmail-draft creation for that run are independently confirmed real; the git write is the part in question.

**Not a competing plan (verified clean):** `WEEK-01-AUTHORITY-QUEUE-2026-07-20.md` (Codex's Authority Queue feeder, Drive file `1BgcuVYM77xC-sxhqN-WrdevGjjNWFTPR`) is drafts-only, explicitly "nothing approved, scheduled, or published," feeding proof-of-work LinkedIn/Instagram/video angles into review rather than generating an independent weekly plan. Matches governance's "feeder, must not compete" rule.

**Outside Cowork's reach, flagged not resolved:** `automation-source-map.md` records a Hermes-side "Weekly Content Plan" job at the same wall-clock time as the Cowork routine (`0 19 * * 0`, last run errored 2026-07-19) and a Hermes "YouTube Intelligence Digest" that overlaps the Cowork one (last run errored 2026-07-22). Governance already marks this as an open decision requiring Emmanuel ("do not pause without verification"). I cannot inspect Hermes from this session — noting it stays open, not resolving it.

## 7. YouTube Intelligence Digest — role and destination (audited only, not deep-assessed)

Trigger `trig_017e3rRcK9w24cBTJ9xzA8o6`, twice daily (`0 5,17 * * *` UTC = 07:00/19:00 Budapest). Role: pulls the 27-channel watchlist from `bridgeworks-workspace/youtube-watchlist.json`, fetches new videos via the YouTube Data API, classifies each (type + `[OFFER]`/`[SKILL]` flags + which brand it applies to), and drafts a Gmail summary. Destination: **Gmail draft only**, to office@bridgeworks.agency, never sent automatically. [Certain, read from the live prompt] Confirmed live: a matching draft, "YouTube Intelligence -- 2026-07-20 morning," exists in Gmail dated 2026-07-20T05:09:54Z. No git commit, no Drive write, no Command Center write in the live prompt — this resolves an "unconfirmed" item in Claude Code's own scheduler map (which flagged the write behavior as inconsistently described across sources).

## 8. Missing sources / conflicts with committed governance

- **CEEFM closure date**: 2026-06-19 (TODO.md, Inbound Prospect Triage prompt, one Command Center row) vs. 2026-06-11 (Command Center's more detailed Projects and Finance rows). Both agree it's closed; the date and even the engagement length (8-week vs. 16-week, same Finance row) disagree. Not resolved here.
- **CEEFM framing inside the live Weekly Content Plan prompt** is stale ("One active client: CEEFM Kft... 16-week engagement") relative to every other current source. It doesn't leak into output, but it's wrong context for theme derivation.
- **`content-week` SKILL.md**: two distinctly-pathed files with the same name — `bridgeworks-codex/plugin/skills/content-week/SKILL.md` (runbook says still stale, 12 posts + CEEFM) vs. `.claude/skills/content-week/SKILL.md` (Claude Code's scheduler map says already corrected). Neither is reachable from this session to settle directly.
- **Drive Content Studio vs. actual write target**: governance names the Drive folder as canonical; the live routine writes to a git repo and its content only reaches Drive via what looks like an incidental local sync mirror, not an intentional canonical write.
- **`TODO.md` currency**: "Last updated: 2026-07-10" — 12 days stale as of this audit, despite Weekly TODO Refresh (enabled, weekly) supposedly touching it every Sunday including 07-12 and 07-19. [Likely — inferred from the artifact's own header, not from execution logs I can't access.] Worth checking alongside the Weekly Content Plan's own dead-run question, since both point at the same failure shape: a routine shows "enabled" in the trigger list but its actual output hasn't moved in weeks.
- **Job Search OS and Weekly TODO Refresh** have no local documentation of inputs/outputs/approval boundary in Claude Code's own scheduler map — outside this audit's canonical source list, noted for completeness only.

## 9. Recommended changes to the existing Weekly Content Plan prompt (proposals only — none applied)

1. Replace the Queue-tab-only dedup check with a check against the Calendar (or, at minimum, against the most recent CONTENT-WEEK file's date range) before generating new dates — the July 20 collision happened because the Sheet was the only source checked and it was already stale.
2. Remove the stale "One active client: CEEFM Kft... 16-week engagement" framing; replace with a pointer to the closed-client note in TODO.md/CLAUDE.md so theme derivation doesn't start from a wrong premise.
3. Decide, and only then encode: does the routine start covering Instagram/Facebook/WhatsApp per `content-channel-model.md`, or does it stay 3-channel until Codex's Mobile Publishing Pack pipeline exists to receive the extra channel output? Right now it silently does neither — it wasn't updated to the new model at all.
4. Decide whether X stays always-on (current behavior) or moves to the new model's "reserved, day 31-60" gating.
5. Add a hard write step to the Content Studio (even a lightweight one — a copy of the CONTENT-WEEK file into `04_Content_Briefs` or a dedicated weekly-pack folder) so governance's stated source of truth actually receives something, instead of the content living only in a git repo plus an incidental Drive mirror.
6. Add a verification step after the `personal-brand-workspace` push (e.g., re-read the pushed file or commit SHA before writing the Gmail draft) so a failed push can't be reported as a success — this is exactly what happened on 2026-07-19.

## 10. Recommended routine changes (proposals only — none applied, none of this executed)

- Confirm with Hermes directly (`hermes cron list`) whether its Weekly Content Plan and YouTube Intelligence Digest jobs are still live duplicates before pausing anything — governance already flags this as open; this audit adds no new resolution, just re-confirms it's still unresolved as of today.
- Clear the dashboard clutter: the paused "Sunday Refresh - TODO + Next Content Week" trigger and the 4 fired one-offs are cosmetic only (already paused/fired, not executing) but governance already flagged them for manual cleanup in the claude.ai UI.
- Once Emmanuel decides the two disagreements in Section 8 (content-week SKILL.md status; CEEFM close date), have Codex or Claude Code correct whichever file is confirmed stale.

## 11. What requires Emmanuel's approval

- Whether to commit Claude Code Desktop's uncommitted `operations/content-system/` work (Content ID tooling, ledgers, templates) — already awaiting approval from that session, unrelated to this one.
- The 90-day rollout, channel model, and mobile publishing pack spec are all still "Proposed" — none of Section 9's prompt changes should be implemented until you've approved (or amended) that underlying model, since changing the Weekly Content Plan prompt to match a proposal that might still change would mean rewriting it twice.
- The two open date/version disagreements in Section 8 (CEEFM close date: 06-11 vs 06-19; `content-week` SKILL.md status) need a source-of-truth ruling, not an AI pick.
- The July 20 double-booked Personal LinkedIn slot (Section 6) needs a decision: which post runs, or do both, spaced out.
- Whether to verify/resolve the Hermes-side Weekly Content Plan and YouTube Digest duplicates (governance already flags this; still open).
- Whether the `personal-brand-workspace` git push actually failed on 2026-07-19 — worth a two-minute direct check by Emmanuel or Claude Code (which has credentialed access to that private repo) rather than relying on secondhand reports, including this one.

---

## Five-question receipt

**1. What am I doing?** One-time read-only audit of the live Cowork cross-model content system — routine inventory, Weekly Content Plan, Drive Content Studio, Historical Planner, Command Center content lane — against the governance docs committed today at `0d028912f7eec9d3bf39574167c4c9b205b3d78a`. No schedule created, edited, paused, or deleted. No media touched, nothing published.

**2. Which sources did I read?** Live Cowork trigger list (`list_triggers`, all 12); the 6 named `operations/*.md` governance docs at the pinned commit (cloned `bridgeworks-workspace` read-only, confirmed `main` HEAD = pinned commit); the Drive Content Studio folder and its subfolders; the Historical Planner Sheet (`1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew`); the Command Center Sheet (`11HdcEaQqGW-TmdhOoJnfSXP4Mj0KxWLYUqFUYSMVwsc`); today's Claude Code Desktop audit receipt and its companion `scheduler-source-map-2026-07-22.md`; the Codex `WEEK-01-AUTHORITY-QUEUE-2026-07-20.md` feeder draft; live Gmail drafts; live Google Calendar events for the week of 2026-07-20.

**3. What changed?** Nothing in any live system. This document is new.

**4. Where did I write the result?** This document, in the `content-system/receipts` Drive folder, alongside today's Claude Code Desktop audit receipt.

**5. What needs Emmanuel's approval?** See Section 11 in full — headline items: the July 20 double-booked LinkedIn slot, the CEEFM close-date disagreement (06-11 vs 06-19), whether the personal-brand-workspace push actually failed, and whether/how to update the Weekly Content Plan prompt once the proposed channel model and 90-day rollout are approved (not before).
