# GTM Migration / Decommission Manifest

Rule for every superseded GTM component:

`preserve -> migrate -> repoint -> test -> approve shutdown -> browser/API shutdown -> revoke obsolete credentials -> archive`

Nothing below has been migrated, repointed, shut down or archived. The current
state of every candidate is recorded in `receipts/2026-08-11-preserve-inventory.md`.
That receipt is read-only. Shutdown and credential revocation need Emmanuel's
approval and run through Codex.

## Candidates

### operations/lead-engine-v1/
Preserve Gmail IDs, send timestamps, hold reasons and next-action history. Migrate into canonical GTM state. Repoint all readers. Verify against Gmail. Archive.

### pipeline/prospecting/
Preserve legacy-only companies and provenance. Migrate valid records. Repoint scheduled reviews. Archive read-only.

### Duplicate prospect Sheets/registers
Preserve unique rows and provenance. Migrate. Repoint dashboards and reports. Archive historical.

### BridgeWorks Ops GTM portions
Preserve browser-local prospect/client state, inbound leads, Gmail links and useful webhook logic. Migrate and repoint inbound/contact workflows. Test end-to-end. Shutdown through Codex browser/API only after Emmanuel approval. Revoke Ops-only keys after verification.

### Hermes BridgeWorks GTM jobs
Preserve unique prompts/schedules/transport adapters only. Migrate useful logic to Codex/Cowork/internal agents. Test replacements. Disable GTM-specific Hermes jobs.

## Candidate added on merge: operations/client-acquisition-engine/

Not in the shipped manifest. It is the largest GTM surface in this repository and
it is live: 7,911 files, a scheduled 09:10 weekday research run, its own approval
packets, and prospect-operations state files modified today.

It is not obviously superseded by this package. It holds proof inventories,
approval packets, scorecards and a 100-row prospect source that the internal-GTM
roles have no equivalent for yet. Its README already records the same offer
conflict this package hit.

No decision is recorded here. Emmanuel decides one of:

1. `client-acquisition-engine` stays the operating layer and internal-gtm becomes
   its deterministic spine, with the engine repointed onto `gtm_core` for dedupe,
   evidence and scoring.
2. `client-acquisition-engine` becomes a migration candidate like the others.
3. The two run in parallel with an explicit boundary written down.

Until that call, do not migrate, repoint or archive anything inside it.
