# Claude Code implementation handoff: Internal GTM writer lock

## Objective

Implement the lightweight repo-local control-plane lock requested by Emmanuel on
2026-08-11. Claude Code is the designated implementation writer. Codex is currently
the operating-state writer and will separately reconcile Arc Solutions.

## Ownership boundary

Claude Code may write only implementation-owned surfaces for this handoff:

- a small lock implementation under `operations/internal-gtm/scripts/`;
- its schema under `operations/internal-gtm/schemas/`;
- tests under `operations/internal-gtm/tests/`;
- concise implementation documentation if required.

Do not rewrite canonical prospects, migration state, execution receipts, shadow-run
state, scheduler state, browser records, or external execution records. In
particular, do not edit anything under:

- `operations/internal-gtm/runs/canonical-batches/`;
- `operations/internal-gtm/runs/transition-receipts/`;
- `operations/internal-gtm/runs/intelligence/`;
- `operations/internal-gtm/runs/shadow/`.

## Required lock contract

Use a lightweight repo-local file mechanism. No service or database.

Every lock must record:

- owner runtime;
- scope/files;
- task;
- acquired timestamp;
- expiry;
- release state.

Required behavior:

1. An active overlapping lock owned by another runtime fails closed.
2. An expired lock does not block forever.
3. The same owner can continue an existing compatible lock.
4. Releasing a lock restores write access.
5. Scope overlap is deterministic and path aware.
6. Writes are atomic enough for a local single-repo workflow.

Expose a small CLI suitable for Claude Code and Codex to check/acquire/release a
scope before writing. Keep current live schedulers and external systems untouched.

## Acceptance

- Add tests for all four required behaviors.
- Run the Internal GTM test suite.
- Return a manifest of changed implementation files, commands/tests, and any
  unresolved limitation.
- Do not edit unrelated dirty files.
- Do not send, publish, mutate CRM, alter the live 09:10 workflow, cut over a
  scheduler, or change credentials.
