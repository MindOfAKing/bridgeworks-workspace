# Weekly-Plan Failure Safeguards

Documentation only. The live Cowork Weekly Content Plan routine
(trigger `trig_01JeovUEsbtcnGyNmRijfCry`) is a Cowork cloud routine, not
a file in this repository. Nothing here edits that routine, its
schedule, or its prompt. Per `automation-source-map.md`, Claude Code
"must not create, edit, pause, or delete Cowork schedules." This file
records what a fix needs to cover, for whoever (Emmanuel, or Claude
Code with explicit authorization) next edits that routine's prompt.

## Why this file exists

The 2026-07-22 Cowork audit (`receipts/2026-07-22-cowork-cross-model-content-audit.md`,
Section 6) found a real, live failure: the routine's July 9 and July 19
runs each scheduled a different Personal LinkedIn post for 2026-07-20
(10:00 and 09:00 respectively). Both are confirmed live on the Google
Calendar. Root cause: the routine's only duplicate check is the
Historical Planner Sheet's Queue tab, which had not been updated since
2026-06-30 when the second run checked it. It found no conflict because
it was checking a stale source, not because there wasn't one.

## Required safeguards for the next revision of the routine's prompt

1. **Calendar deduplication before drafting dates.** Check the actual
   Google Calendar for the target week before proposing new post dates
   and times, not only the Historical Planner Sheet. The Sheet can be
   (and was) stale for weeks while the Calendar kept accumulating real
   events.
2. **Check existing CONTENT-WEEK files and canonical Drive packs too.**
   Dedup must also look at the most recent `CONTENT-WEEK-*.md` files
   already on disk and, once the Mobile Publishing Pack pipeline exists,
   any `YYYY-MM-DD Weekly Pack` folders already in the canonical Drive
   Content Studio. One source is not enough; the July 20 collision is
   what "one stale source" produces.
3. **Verify a Git or Drive write before reporting success.** The July 19
   run's session log reported a successful commit and push to
   `personal-brand-workspace` (`31070fc`) that does not exist in that
   repository (`git cat-file -t 31070fc` returns "Not a valid object
   name"; independently, the Cowork audit found the Drive mirror of that
   repo has no `07-20` file either). A write step must read back what it
   just wrote (file exists, or commit SHA resolves) before the routine
   is allowed to report success anywhere (session log, Gmail draft,
   chat).
4. **Report a stale planner as a source gap, not a clean check.** If the
   Historical Planner Sheet (or any dedup source) has not been updated
   in longer than one cycle (a week), the routine should say so
   explicitly ("dedup source last updated N days ago, treat this check
   as incomplete") instead of silently reporting "no duplicates found."
5. **No Calendar event until the plan is approved.** Per the runbook's
   approval-gated pipeline, Calendar events are a form of publishing
   commitment. Creating them before Emmanuel has approved the week's
   plan pre-empts the approval step the whole system is built around.
6. **Canonical weekly output must land in Drive Content Studio.**
   Today the routine's only durable outputs are a git repo
   (`personal-brand-workspace`, write-path unverified per item 3) and an
   incidental personal Drive sync mirror of that repo. Neither is the
   canonical Drive Content Studio folder
   (`1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY`) governance names as the source
   of truth. At minimum, a copy of the week's `CONTENT-WEEK-*.md` needs
   to reach that folder (or its future weekly-pack structure) so the
   canonical source of truth actually receives something.
7. **Must not create a competing plan.** This applies to any other
   system too (the client-acquisition Authority Queue feeder, any
   Hermes duplicate). There is exactly one primary weekly editorial
   trigger; everything else feeds it or reads from it, never runs an
   independent parallel version.

## CEEFM status (ratified, not open)

The Cowork audit (Section 8) found the CEEFM closure date stated
inconsistently across sources and left it open. That has since been
ratified. Current-system status, source `clients/ceefm/VERIFIED-FACTS.md`:

- CEEFM closed: 2026-06-19.
- Public engagement wording: "engagement, March to June 2026". Do not
  state the engagement duration publicly (the contract was 16 weeks;
  the client terminated at week 9; neither number goes in public copy).
- Public GEO result: 16/100 to 77/100. 16 and 77 are GEO scores --
  never employee or user counts.
- Verified CEEFM headcount is 8. This is unrelated to the GEO figures
  above; do not let the two get confused in any content that mentions
  both a score and a headcount.

Any weekly-plan output, theme derivation, or reconciliation check that
touches CEEFM should treat the above as settled, not as a question to
re-derive.

## What this file does not do

- It does not change the live trigger, its cron schedule, or its prompt
  text. Only Emmanuel, or Cowork itself, can do that.
- It does not resolve which `content-week` SKILL.md file
  (`bridgeworks-codex/plugin/skills/content-week/SKILL.md` vs.
  `.claude/skills/content-week/SKILL.md`) is actually current -- the
  two give conflicting status and neither was reachable from the
  sessions that found this. That still needs a source-of-truth ruling.
- It does not decide whether the routine should expand to cover
  Instagram/Facebook/WhatsApp now or wait for the Mobile Publishing
  Pack pipeline. That is an open decision, not a safeguard.
