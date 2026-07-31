# BridgeWorks Prospecting and Outreach Operating System

Date: 2026-07-26
Owner: Emmanuel Ehigbai
Run class: Sales audit and draft-only implementation
External actions executed: None

## Outcome

BridgeWorks now has one measurable operating path from prospect intake to conversion reporting.

HubSpot is the intended commercial source of truth. Until Emmanuel approves the prepared import and reconciliation, `research/prospect-operations/prospect-source-current.csv` is the governed staging source. The old live Google Sheets are evidence inputs only and must not drive outreach.

Sending authority remains `none`. A campaign row may be researched, qualified, personalized, and approved for Gmail draft creation without being approved for sending.

## Headline Gaps

1. The named live Prospect Tracker has 17 rows, while the current staging source has 60.
2. The first 10 rows in the live Prospect Tracker are column-shifted. Dates appear under `status`. It is unsafe as a source of truth.
3. The live outreach and audit-preview Sheets still expose rejected Geiger and Kavezo follow-ups as ready. Two PDF paths point to another Windows user profile.
4. Gmail proves seven outbound messages to five companies. The current source previously marked Pyramidon and Geiger as research candidates, creating repeat-contact risk. This is now reconciled locally.
5. Gmail contains no Kavezo message despite the old Sheet claiming an initial contact and ready follow-up.
6. HubSpot contains 37 companies, 11 contacts, and zero deals. Every sampled `hs_lead_status` is blank. Sample and integration-test records are mixed with commercial records.
7. The 60-row staging source has no duplicate domain or company-country keys, but it is incomplete: 21 missing websites, 35 missing emails, 41 missing contact names, 49 missing roles, and 45 missing dated evidence sets.
8. ClickUp has only two sales-list tasks. There are no live execution tasks for batch production, approvals, follow-ups, reply handling, suppression, or weekly reporting.
9. The operating dashboard says the commercial pipeline is empty and prospecting feeds are not behaviorally visible.
10. The Command Center contains old source-of-truth approval items and a stale May automation registry. It cannot prove that the historical prospecting routines are healthy.
11. HubSpot is hosted in EU and uses Europe/Budapest, but company currency remains USD.
12. The local research-state file pointed to the retired 45-row CSV. Queue state now writes the 60-row source.

## Canonical Data Path

| Layer | System | Role |
|---|---|---|
| Prospect intake | `prospect-source-current.csv` | Governed staging, evidence collection, and pre-CRM dedupe |
| Commercial truth | HubSpot | Companies, contacts, lifecycle, lead status, activities, deals, next action |
| Execution truth | ClickUp | Batch, approval, follow-up, research, and reporting tasks |
| Communication evidence | Gmail | Exact drafts, sent events, replies, bounces, opt-outs |
| Files and reporting | Drive | Reviewed assets and weekly reports |
| Enrichment | Apollo | Approved research only, after HubSpot dedupe |

The staging CSV stops being operationally authoritative after the approved HubSpot import. It remains an append-only intake and audit export.

## Canonical Prospect Record

Required fields before research:

- stable `prospect_id`;
- company;
- canonical domain or company-country dedupe key;
- ICP lane and sector;
- source;
- one next internal action;
- `outreach_authority=draft-only`.

Required before qualification:

- current owned domain or a careful `not located` result;
- dated evidence URL;
- observable commercial gap;
- buyer or responsible role;
- usable public contact route;
- offer fit and selected proof boundary;
- exclusion and risk notes.

Required before campaign-ready:

- exact destination;
- exact subject and body;
- 25 to 180 words;
- evidence link;
- no prior-contact conflict;
- no suppression, bounce, objection, or active customer conflict;
- `approval_state=awaiting_explicit_approval`;
- `sending_authority=none`.

## Deduplication

Run in this order:

1. Exact normalized domain.
2. Exact email.
3. Normalized company plus country.
4. HubSpot company-domain and contact-email search.
5. Gmail destination and company search.
6. Manual review for subsidiaries, trading names, and shared domains.

Never merge records only because names look similar. Preserve parent-subsidiary distinctions and record the decision.

## ICP Segments

### Active

1. Lane A: Budapest credibility-first SMEs.
2. Lane B: African-owned businesses in Europe.
3. Lane D: Nigeria growth businesses.

### Deferred

- wider CEE expansion;
- wider West Africa expansion;
- hospitality until Oliviks proof is complete;
- high-scale firms with long procurement cycles;
- businesses with weak evidence, unclear buyer authority, or no safe contact route.

### Qualification Score

Score 0 to 20:

- service value: 0 to 4;
- visible commercial gap: 0 to 4;
- response or conversion risk: 0 to 3;
- decision-maker findability: 0 to 3;
- BridgeWorks proof fit: 0 to 3;
- active-lane fit: 0 to 2;
- urgency: 0 to 1.

Priority A is 16 to 20. Priority B is 11 to 15. Below 11 does not enter a campaign batch.

## Enrichment Gate

Apollo is authenticated and its observed daily search limit is 600 with zero consumed in the audit.

Enrichment remains off by default.

Before any credit-consuming action:

1. Confirm the prospect passes ICP and evidence review.
2. Search HubSpot by domain and email.
3. Search Gmail for prior contact, objection, or bounce.
4. State the exact approved prospect count and credit budget.
5. Use business data only. Do not request personal phone numbers or personal emails by default.
6. Log source, access date, and result.

## HubSpot Import

Prepared files:

- `research/prospect-operations/operating-output/hubspot-companies-import-preview.csv`
- `research/prospect-operations/operating-output/hubspot-contacts-import-preview.csv`

Current previews contain 11 companies and 18 contacts after live domain and email dedupe.

Before import approval:

1. Remove HubSpot sample and BridgeWorks integration-test records from commercial reporting. Do not delete them without approval.
2. Confirm whether USD is intentional.
3. Confirm HubSpot lead-status values and mapping.
4. Review generic inbox contacts. A generic inbox may be a company route, not a named person.
5. Import companies before contacts.
6. Spot-check five associations.
7. Record import ID, timestamp, row counts, rejects, and duplicates.

No import was run.

## Campaign Batches

`research/prospect-operations/operating-output/campaign-ready-batch.csv` contains:

- 12 priority records;
- 3 test-segment records;
- exact destinations, subjects, bodies, and evidence;
- canonical staging IDs;
- `awaiting_explicit_approval`;
- `sending_authority=none`.

Campaign policy:

- one ICP, one offer, one pain angle per batch;
- five to ten priority records per send decision;
- test-segment records require separate approval;
- never convert approval for draft creation into approval to send;
- recheck the webpage, contact route, suppression state, and Gmail history immediately before any approved send.

## Personalization Standard

Every draft must:

- name one current observable issue;
- connect it to a plausible business outcome without pretending to know internal results;
- avoid generic compliments;
- avoid invented metrics;
- use only reviewed BridgeWorks proof;
- make a low-pressure next-step request;
- identify BridgeWorks and Emmanuel;
- provide a simple way to object to further contact when email outreach is legally permitted.

## Approval and Sending Authority

| State | Internal work allowed | External work allowed |
|---|---|---|
| `research` | Evidence collection | None |
| `qualified` | Scoring and angle selection | None |
| `drafted` | Exact copy and destination | None |
| `awaiting_explicit_approval` | Approval packet | None |
| `draft_creation_approved` | Create exact Gmail draft | No send |
| `send_approved` | Send exact approved copy after live recheck | Exact message only |
| `sent` | Record evidence and schedule follow-ups | Approved follow-ups only |
| `suppressed` | Retain minimum suppression evidence | No outreach |

Approval expires when the destination, subject, body, evidence, or material webpage state changes.

## Follow-Up

- Follow-up 1: three business days after a verified send.
- Follow-up 2: seven business days after a verified send.
- Stop after two follow-ups unless the prospect replies.
- Move to dormant after 14 days with no reply.
- A follow-up date is never created from a draft or planned send.
- Prior contacts such as Pyramidon and Geiger require a new reactivation decision, not automatic follow-up.

## Bounce, Reply, and Objection Handling

### Bounce

- hard bounce: suppress immediately;
- soft bounce: hold, verify once, and do not retry more than once without approval;
- record bounce reason and last attempted address;
- never enrich a replacement address automatically.

### Reply

- positive: classify, prepare a discovery brief, and create a deal only after the commercial opportunity is real;
- neutral or referral: update role and next action;
- negative: close the sequence;
- objection or opt-out: suppress immediately across Gmail, staging, and HubSpot;
- auto-reply: do not count as a human reply.

The right to object to direct marketing must be honored without charge, and the person must be informed of that right by the first communication. Email marketing also has separate ePrivacy rules. BridgeWorks should not treat a GDPR legitimate-interest assessment as permission to send unsolicited email. For Hungary and other EU markets, use a conservative consent or existing-customer rule unless qualified legal advice confirms the exact B2B route.

## Daily Execution Mode

Normal weekday target:

| Work | Target |
|---|---:|
| Raw companies added | 20 |
| HubSpot/Gmail dedupe checks | 20 |
| Qualified prospects | 10 |
| Contact routes verified | 8 |
| Evidence-complete personalized drafts | 5 |
| Approval-ready records | 5 |
| Follow-up/reply/bounce exceptions cleared | 100% due |

Draft-only days may reach the targets without sending anything.

## Weekly Execution Mode

| Work | Target |
|---|---:|
| Raw prospects | 100 |
| Qualified | 50 |
| Campaign-ready priority drafts | 25 |
| Approved sends | 0 until Emmanuel widens the gate |
| Follow-ups scheduled from verified sends | 100% |
| Discovery conversations | 5 target after sending is approved |
| Proposal opportunities | 1 target after conversations exist |

Every Friday report:

- raw, qualified, drafted, approved, sent;
- delivered, bounced, replied, positive replied;
- discovery calls, proposals, wins;
- stage-to-stage conversion;
- ICP, source, channel, angle, and batch performance;
- stale and suppressed records;
- next experiment and stop decision.

## Current Operating Output

- Staging prospects: 60.
- Duplicate domains: 0.
- Duplicate company-country keys: 0.
- Verified contacted companies: 5.
- Verified outbound messages: 7.
- Replies: 0.
- Bounces: 0.
- HubSpot deals: 0.
- Priority campaign-ready drafts: 12.
- Test-segment drafts: 3.
- New research batch: 5 prospects.

## Prioritized Next Actions

### Done

1. Reconciled Pyramidon and Geiger as `sent-no-reply`.
2. Preserved Managerent, A+ Real Estate, and Craftex send evidence.
3. Produced a deduplicated canonical register.
4. Produced HubSpot company and contact import previews.
5. Produced a 15-record approval-gated campaign batch.
6. Produced a weekly conversion report.
7. Prepared a five-prospect research batch from the current source.
8. Tested the local tooling and verified idempotent reconciliation.

### Needs Approval

1. Approve or reject HubSpot import preparation after reviewing the 11 companies and 18 contacts.
2. Decide whether the 12 priority drafts should move to Gmail draft creation. This does not approve sending.
3. Separately decide whether to keep or reject the three test-segment drafts.
4. Decide whether USD is the intended HubSpot currency.
5. Approve ClickUp task creation for the execution cadence.
6. Approve any exact sending batch only after legal-route and live-evidence recheck.

### Blocked

1. Sending remains unauthorized.
2. Apollo enrichment remains unauthorized.
3. The live Google Sheets cannot be promoted until their schemas and stale rows are repaired or archived.
4. Reply and conversion rates cannot improve until an approved, compliant sending test exists.
5. HubSpot cannot be the complete commercial source of truth until import and lead-status mapping are approved.

