# GTM Preserve Inventory — 2026-08-11

Step 1 of `preserve -> migrate -> repoint -> test -> approve shutdown -> browser/API shutdown -> revoke obsolete credentials -> archive`.

This is a read-only count of what exists today. Nothing was moved, edited,
repointed or deleted. Counts come from the working tree on 2026-08-11 and will
drift, so re-count before any migration run.

## File counts

| Candidate | Files |
|---|---|
| `operations/lead-engine-v1/` | 50 |
| `pipeline/prospecting/` | 16 |
| `pipeline/inbound/` | 7 |
| `pipeline/lead-qualification/` | 4 |
| `operations/client-acquisition-engine/` | 7,911 |
| `operations-dashboard/` | 2 |
| `automation-reports-dashboard/` | 4 |

## Record counts

| File | Data rows |
|---|---|
| `operations/lead-engine-v1/01-prospects/prospect-batch-2026-07-14.csv` | 45 |
| `operations/lead-engine-v1/01-prospects/prospect-tracker.csv` | 12 |
| `operations/lead-engine-v1/01-prospects/adjacent-lane-watchlist.csv` | 7 |
| `pipeline/prospecting/prospect-tracker.csv` | 27 |
| `pipeline/prospecting/daily-outreach-queue.csv` | 12 |
| `pipeline/prospecting/audit-preview-tracker.csv` | 12 |
| `pipeline/prospecting/market-triage.csv` | 1 |
| `pipeline/inbound/inbound-leads.csv` | 4 |
| `operations/client-acquisition-engine/SERVICE-LINE-PROSPECT-LIST-2026-08-01.csv` | 26 |
| `operations/client-acquisition-engine/research/prospect-operations/prospect-source-current.csv` | 100 |

## Irreplaceable state

`operations/lead-engine-v1/03-outreach-drafts/outreach-send-log-2026-06-23.json`
holds the only local record of three real sent messages, with Gmail message ID,
thread ID and timestamp:

| Company | Sent message | Thread | Sent at |
|---|---|---|---|
| Managerent | `19ef5dd74e105f4e` | `19ef5cb9348d5278` | 2026-06-23 21:03 +0200 |
| Craftex | `19ef5dbdaedfb5bf` | `19ef5cb93d25d150` | 2026-06-23 21:01 +0200 |
| A+ Real Estate | `19ef5daed0f1afc1` | `19ef5cb9419fabdb` | 2026-06-23 21:00 +0200 |

These IDs cannot be reconstructed from anything else in the repository. Verify
them against Gmail before any archive step touches `lead-engine-v1/`.

`operations/lead-engine-v1/03-outreach-drafts/gmail-draft-manifest.json` and the
ten lead-leak reviews under `02-lead-leak-reviews/` are the evidence behind those
sends. They travel with the send log.

## Duplicate registers

Two prospect trackers exist with the same filename and different content:
`operations/lead-engine-v1/01-prospects/prospect-tracker.csv` (12 rows) and
`pipeline/prospecting/prospect-tracker.csv` (27 rows). A third, larger list lives
at `operations/client-acquisition-engine/research/prospect-operations/prospect-source-current.csv`
(100 rows). Overlap has not been measured. `gtm_core.dedupe` is the tool for that
measurement when the migration is approved, because it merges on exact domain or
normalized company name and reports every merge with a reason.

## Not counted

Hermes GTM jobs and the browser-local BridgeWorks Ops state are not in this
repository. They need a Codex inspection pass before they can be inventoried.

## Blocked on

- Emmanuel's decision on `operations/client-acquisition-engine/`, per
  `MIGRATION-DECOMMISSION.md`. It is live, scheduled and modified today. Nothing
  else should move until that call is made.
- Emmanuel's approval before any shutdown, credential revocation or archive step.
