# Claude Code handoff: native qualifier compatibility repair

## Objective

Repair the native Codex skill wrapper at:

`C:/Users/User/.codex/skills/bridgeworks-lead-qualifier/scripts/score_prospect.py`

It currently emits a complete canonical qualification-v1 result, then raises
`KeyError: 'valid'` because its exit path expects the former legacy field.

## Ownership and scope

Claude Code is the implementation writer. Acquire the Internal GTM
`implementation` lock before editing and release it when finished.

Allowed writes:

- the native wrapper above;
- its native regression test, colocated with the skill if appropriate;
- the exact mirrored staging wrapper/test only if the installed native skill's
  existing mirror contract requires parity.

Do not edit Arc operating state, canonical batches, evidence, qualification
records, transition receipts, entity receipts, shadow state, scheduler state,
CRM, or external systems.

## Required behavior

- Canonical qualification-v1 output is consumed directly and exits zero when
  scoring succeeds.
- Do not add a legacy `valid` field to qualification-v1 or its schema solely for
  wrapper compatibility.
- The historical compatibility path may translate at the wrapper boundary if it
  still needs a `valid` decision.
- Add a regression test reproducing the canonical result without `valid`.

## Acceptance

Run the wrapper regression test and one real invocation against:

`operations/internal-gtm/runs/qualification-inputs/arc-solutions-limited-qualification-v1-2026-08-11.json`

The invocation must exit zero. Return a concise changed-file and test manifest.
