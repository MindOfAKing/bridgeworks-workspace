# Interface Handoff Receipt

Date: 2026-07-22
Interface: Claude Code Desktop
Session: correction and hardening pass on the uncommitted content-system
implementation, requested after a same-day Cowork audit landed in
`receipts/`

## Repository state at start

`bridgeworks-workspace` on `main`, HEAD `0d028912f7eec9d3bf39574167c4c9b205b3d78a`
(unchanged from the prior session). `git status --short` showed only
`?? operations/content-system/`. `receipts/` additionally contained a
naming collision: a complete Cowork audit saved as
`Cowork Audit - Cross-Model Content System - 2026-07-22 (1).md`
(25,231 bytes) and a 24-byte placeholder (`FILE_CONTENT_PLACEHOLDER`)
sitting on the clean filename.

## What was done

**A. Receipt cleanup.** Verified the "(1)" file byte-for-byte against a
freshly written copy before deleting anything. Retained one file:
`receipts/2026-07-22-cowork-cross-model-content-audit.md`. Removed the
placeholder and the "(1)" variant. Did not edit the Cowork audit's
content.

**B. Documentation accuracy.** Corrected `README.md`: the Weekly
Content Plan routine does not push the historical planner Sheet
directly (it writes `temp-week-queue.json` and puts a manual
`append-to-planner.py` command in a Gmail draft); it never touches the
Command Center or Drive Content Studio. Corrected the Claude Code
receipt: the routine is not "3.5 weeks dead" (the Cowork audit found it
fired on schedule on 2026-07-09 and 2026-07-19, confirmed via live
Gmail drafts and Calendar events) -- what's actually broken is its
write path to `personal-brand-workspace` and its dedup check, which
only reads the stale Sheet. That gap caused a real, live double-booking:
two different Personal LinkedIn posts scheduled for 2026-07-20. Also
corrected the receipt's "nine template files" claim to "seven," the
count actually built in that session.

**C. Content ID hardening (`content_id.py`).** Added a Windows-safe,
dependency-free mutex (atomic `O_CREAT | O_EXCL` file creation, stdlib
only) around the read-check-write sequence for both ledgers, with
stale-lock recovery (30s) and a bounded wait (10s) that fails loudly
rather than guessing. Added ISO week validation (`date.fromisocalendar`)
so `check` rejects out-of-range weeks like `00` or `60` even though
they match the regex shape. Added a sequence-overflow guard that
refuses to issue a 100th ID for one year/week/brand/channel combination
instead of silently emitting a 3-digit sequence that breaks the format.
Replaced the flat channel set with a per-brand matrix: EE is limited to
LI/IG/FB/WA; BW gets all six including X/TT. Enforced in both `new` and
`check`.

**D. Reconciliation logic (`reconciliation_checks.py`).** Replaced the
flat "same ID appears more than once anywhere" check with four
distinct signals: duplicate ledger issuance (parsed directly from the
registry CSVs, row-level), multiple canonical content-item definitions
(a "Content ID:" field declared in more than one file that isn't
recognizable as an approval card, publishing receipt, or analytics
record), legitimate downstream references (the same field inside a
file that is recognizable as one of those three, reported but never
flagged), and Master Thesis ID reuse (never flagged, by design).
Documented the file-level heuristic's limitation (one record per file)
directly in the script's docstring.

**E. Claim/evidence ledger.** Added `templates/claim-evidence-template.md`
(all 14 required fields) and `registry/claim-evidence-ledger.csv`. Both
were previously missing; nothing existing conflicted with them.

**F. Weekly-plan failure safeguards.** Added `weekly-plan-failure-safeguards.md`,
documentation only. Lists the 7 required fixes for the live routine's
next prompt revision, grounded in the Cowork audit's concrete finding
(the July 20 double-booking) rather than restating governance in the
abstract. Does not touch the live Cowork trigger.

## Bugs found

1. `datetime.utcnow()` deprecation (fixed in the prior session, carried
   forward correctly here).
2. The original reconciliation format-check flagged the runbook's own
   `CONTENT-YYYY-WW-BRAND-CHANNEL-NN` placeholder and unrelated
   filenames as malformed IDs (fixed in the prior session).
3. This session: the flat duplicate check would have flagged every
   normal approval-card/publishing-receipt/analytics-record reference
   to a Content ID as a "duplicate," which is exactly wrong and would
   have made the tool useless once real content existed. Fixed by the
   four-way classification in Correction D.
4. This session: `content_id.py` had no protection against two
   processes issuing at the same time. Two Claude Code interfaces (or
   Claude Code and Codex) calling `new` within the same second could
   have read the same "next sequence" and both written seq 01. Fixed
   with the lock in Correction C; verified under test (see below).
5. This session: sequence numbers could silently overflow past 99 and
   break the ID format with no error. Fixed with an explicit guard.
6. This session: README.md and the original receipt both stated or
   implied things about the live Weekly Content Plan routine that this
   session could not have verified on its own (the Sheet-push mechanism,
   whether the routine was "dead"). The same-day Cowork audit provided
   direct verification that contradicted both claims. Corrected in B.

## Tests run and results

All passed. Full output is in this session's transcript.

- Basic generation: sequential IDs issued correctly (01, 02); thesis ID
  issued correctly.
- Invalid brand: `new --brand ZZ` refused cleanly, exit 1.
- Invalid brand/channel combination: `new --brand EE --channel X` and
  `--channel TT` both refused with a clear message, exit 1. `new
  --brand BW --channel X` succeeded (positive control). `check
  CONTENT-2026-30-EE-X-01` also refused (enforcement on the check path,
  not just the issuance path).
- Invalid ISO weeks: `check` on week `00` and week `60` both refused,
  exit 1. Week `30` (today's real week) accepted.
- Sequence overflow: seeded the ledger with a synthetic `...-BW-TT-99`
  row, then `new --brand BW --channel TT` for the same year/week was
  refused with the overflow message, exit 1.
- Concurrent issuance: 6 simultaneous subprocess workers via a
  threaded driver script, all calling `new --brand BW --channel LI`
  for the same date. All 6 succeeded; all 6 issued IDs were unique
  (sequence 03 through 08, continuing from 2 already issued earlier in
  the same test run). No duplicates, no crashes, no orphaned lock file
  afterward.
- Reconciliation, against an isolated fixture directory in the
  scratchpad (not inside `operations/content-system`): a ledger CSV
  with an intentional duplicate row was correctly flagged under 3a; two
  files declaring the same Content ID with no lifecycle markers were
  correctly flagged under 3b as conflicting canonical definitions; an
  approval-card-shaped file and a publishing-receipt-shaped file
  referencing that same Content ID were correctly classified as
  downstream and NOT flagged; three files sharing one Master Thesis ID
  were correctly reported as informational reuse, not flagged. A
  malformed 3-digit-sequence ID planted in one fixture was correctly
  caught by the format check.
- `git status --short`: only `?? operations/content-system/`.
- `git diff --check`: clean.
- No `.lock` files left behind anywhere in `operations/content-system`
  after the concurrency test.

## Test artifacts removed

- Reset `registry/content-id-ledger.csv` and
  `registry/master-thesis-ledger.csv` to header-only after every test
  run that wrote to them (including the seeded overflow row).
- Deleted the scratchpad concurrency driver script and the scratchpad
  reconciliation fixture directory; neither was ever inside
  `operations/content-system`.

## Uncommitted changes left behind

Yes, by instruction: do not stage, commit, or push. `git status --short`
still shows only `?? operations/content-system/`.

## Handoff notes for the next session or interface

- The live Weekly Content Plan routine's July 20 double-booking
  (two different Personal LinkedIn posts on the Calendar for the same
  day) is still live and unresolved -- this pass only documented what
  the fix needs to cover (`weekly-plan-failure-safeguards.md`), it did
  not and cannot fix the routine itself from here.
- **Correction, per the 2026-07-22 final narrow-correction pass:** the
  CEEFM closure date is ratified, not open. Current-system status
  (source `clients/ceefm/VERIFIED-FACTS.md`): closed 2026-06-19; public
  wording is "engagement, March to June 2026" with no public statement
  of engagement duration; public GEO result is 16/100 to 77/100 (GEO
  scores, never headcount); verified headcount is 8. See
  `weekly-plan-failure-safeguards.md` for the full statement. Only the
  `content-week` SKILL.md status (two conflicting files) is still open.
- `content_id.py`'s lock files are named `<ledger>.lock` and
  self-clean on every run; if a run is ever killed mid-write, the next
  invocation will wait up to 10s, then break a lock older than 30s
  automatically. No manual cleanup should normally be needed, but if
  `content_id.py` ever hangs, check for a stray `.lock` file in
  `registry/` first.
