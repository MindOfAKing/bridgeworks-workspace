# Reconciliation accounting receipt

2026-08-11. Two reconciliation passes ran against the same repository on the same
day and produced different totals. The numbers are not forced to match. This is
the accounting that explains why they differ.

Both passes are read-only. `writes_performed: 0` in each.

## The two passes

| | Pass A | Pass B |
|---|---|---|
| Run by | Claude Code | Codex |
| Sources | six local file stores | eight sources, including three live systems |
| Live systems queried | none | Gmail, HubSpot, Mission Control |
| Report | first `prospect-reconciliation.json` | current `prospect-reconciliation.json` |

Pass B supersedes Pass A. Pass A is preserved here as accounting, not as a rival
answer.

## The four differences

### Source-record totals: 303 against 339

| Source | Pass A | Pass B |
|---|---:|---:|
| live Gmail receipt | not queried | 10 |
| Mission Control approvals | not queried | 15 |
| live HubSpot receipt | not queried | 14 |
| local Gmail send log | 3 | 3, suppressed where a live receipt exists |
| acquisition-engine results | 49 | 49 |
| acquisition-engine source CSV | 100 | 100 |
| canonical register | 60 | 60 |
| Lead Engine v1 | 64 | 64 |
| pipeline/prospecting | 27 | 27 |
| **total** | **303** | **339** |

The 36-row difference is exactly the three live systems Pass A could not read:
10 + 15 + 14 = 39, less the 3 local send-log rows that Pass B suppresses once the
stronger live receipt covers the same business.

**Counting rule:** a row is one assertion from one source about one business. The
same business appearing in six stores is six rows, not one. Row totals measure
source coverage, not prospects.

### Canonical entity totals: 122 against 120

Both passes key on domain first, normalized company name second.

Pass A produced 122 buckets. Three of them were company-name buckets holding only
a Gmail send with no domain: `company:a real estate`, `company:craftex`,
`company:managerent`.

Pass B read the live mailbox, which returns a recipient address and therefore a
domain. Those three sends joined their existing domain buckets. Three buckets
disappeared and one new entity appeared from a live source that Pass A never saw.
122 minus 3 plus 1 is 120.

**Counting rule:** an entity is one dedupe key. A key changes when better identity
evidence arrives. Entity counts fall when identity improves, and a falling count is
a good sign, not a loss.

### Contacted-company totals: 8 against 12

Pass A counted a business as contacted from two signals: a row in the local send
log, or a non-empty contact column in the canonical register. That gives 8.

Pass B added the live mailbox, which found sent messages to businesses whose
register rows were never filled in. That gives 12.

The four extra are not new activity. They are activity that happened and was never
written back to the CSV. The register is a generated view that fell behind the
mailbox.

**Counting rule:** contacted means Gmail holds a sent message to that business.
Gmail is communication ground truth. A CSV column is a claim about Gmail, and when
they disagree Gmail wins.

### Orphaned-send totals: 3 against 0

| | Pass A | Pass B |
|---|---:|---:|
| Gmail-verified businesses | 3 | 10 |
| Gmail SENT messages | 3 | 19 |
| Orphaned from a prospect record | 3 | 0 |
| Cross-key candidates without a send | 3 | 3 |

Pass A found three sends it could not attach to a business, because the local send
log stores a company name and no domain.

Pass B resolved all three from the live mailbox, which carries the recipient
address. It also found the local log was an undercount: 19 sent messages across 10
businesses, not 3 across 3. The local log recorded one outreach batch from
2026-06-23 and nothing since.

**Counting rule:** an orphaned send is a verified send that cannot be attached to a
canonical entity. Zero orphans does not mean zero ambiguity. Three cross-key
candidates remain, none of them holding a send, and they stay `possible_match`
because a similar company name is a lead, not identity proof.

## What this receipt is evidence of

The local files understated real activity by a factor of six on sent messages.
Pass A was not wrong about what the files said. The files were behind.

That is the argument for the reconciler reading live systems on every run rather
than trusting a generated register, and it is the reason the authority order puts
Gmail above every CSV in the repository.

## What neither pass can settle

- Reply state. Sends are counted, replies are not classified. Sixteen of the
  nineteen sent messages have no recorded outcome.
- Whether the four newly discovered contacted businesses should re-enter the
  pipeline or stay closed. That is Emmanuel's call.
- The three `possible_match` candidates. Each needs one manual domain check.
