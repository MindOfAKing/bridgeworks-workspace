# Accounting receipt pointer

The single canonical reconciliation-accounting receipt is
`reconciliation-accounting-receipt.md` in this directory. This file is retained
only as a non-destructive pointer because two implementations landed concurrently;
it is not a second accounting result.

<!-- Superseded content retained below for provenance only. -->

Date: 2026-08-11  
Scope: explain, not force, the Claude/local-only and Codex/live-reconciled counts.
No source system was written.

## Count comparison

| Measure | Claude/local-only accounting | Codex/live-reconciled accounting | Explanation |
|---|---:|---:|---|
| Source records | 303 | 339 | The live view adds 10 Gmail domain receipts, 15 Mission Control approval records and 14 HubSpot company-ID records, then suppresses 3 lower-authority local Gmail rows already represented by the live receipt: `303 + 10 + 15 + 14 - 3 = 339`. These are source assertions, not unique prospects. |
| Canonical entity keys | 122 | 120 | Three company-only Gmail buckets now join their exact domains, reducing the count by 3. `ppmgt.hu` appears only in the live Gmail/HubSpot scope and adds 1: `122 - 3 + 1 = 120`. |
| Reported contacted count | 8 entity buckets | 12 domain-resolved companies | The old 8 was not eight unique companies. It counted three company-only Gmail buckets plus five generated-register domain rows, with Managerent, A+ and Craftex appearing in both sets. The live count is 10 Gmail-verified domains plus two register-only historical contacts, Pyramidon and Geiger Services. |
| Orphaned send buckets | 3 | 0 | A+ Real Estate, Craftex and Managerent now meet the deterministic rule below. Nothing was merged from name similarity alone. |

## Source scope

The local-only 303 rows were:

| Source | Rows |
|---|---:|
| Local Gmail send log | 3 |
| Acquisition-engine results | 49 |
| Acquisition-engine source CSV | 100 |
| Generated canonical register | 60 |
| Lead Engine v1 | 64 |
| Legacy pipeline/prospecting | 27 |

The live-reconciled 339 rows are:

| Source | Rows |
|---|---:|
| Live Gmail receipt | 10 |
| Mission Control awaiting-approval tasks | 15 |
| Live HubSpot exact-domain matches | 14 |
| Acquisition-engine results | 49 |
| Acquisition-engine source CSV | 100 |
| Generated canonical register | 60 |
| Lead Engine v1 | 64 |
| Legacy pipeline/prospecting | 27 |

The three local Gmail rows are deliberately suppressed when the same message ID
is present in the stronger live receipt. They remain preserved in their source
file and in the deterministic resolution receipt.

## Deterministic orphan rule

A legacy send becomes `confirmed_match` only when all of these agree:

1. normalized historical company name;
2. recipient email domain;
3. declared canonical domain;
4. historical website/domain;
5. legacy Gmail message ID found in the live Gmail result.

The receipt also stores Gmail thread IDs and the known destination/contact. A row
missing any part remains `possible_match`; it is not merged. Current result:
three `confirmed_match`, zero `possible_match`, zero orphaned send buckets.

Machine-readable evidence:

- `operations/internal-gtm/migration/phase-3/prospect-reconciliation.json`
- `operations/internal-gtm/migration/phase-3/gmail-contact-history-2026-08-11.json`
- `operations/internal-gtm/migration/phase-3/hubspot-company-evidence-2026-08-11.json`
