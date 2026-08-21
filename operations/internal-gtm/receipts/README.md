# GTM migration receipts

One dated file per step of the migration rule:

`preserve -> migrate -> repoint -> test -> approve shutdown -> browser/API shutdown -> revoke obsolete credentials -> archive`

Rules for every receipt here:

1. Record what existed, with counts, before anything changed.
2. Name the exact files and IDs that cannot be reconstructed.
3. Separate observed from inferred. Never write a count you did not run.
4. A receipt records a step that happened. It does not authorize the next one.

Shutdown, credential revocation and archiving need Emmanuel's approval and run
through Codex. Claude Code writes receipts and migration code. It does not
execute shutdowns.

| Receipt | Step | State |
|---|---|---|
| `2026-08-11-preserve-inventory.md` | preserve | complete, read-only |
