# BridgeWorks Sales Tool Execution Map

Date: 2026-08-01  
Status: Proposed configuration; no external writes executed

## System ownership

| System | Owns | Must not own |
|---|---|---|
| HubSpot | Companies, contacts, lifecycle, lead status, activities, deals, next commercial action | Research drafts and project checklists |
| ClickUp | Research batches, approvals, follow-ups, discovery preparation, proposal production, weekly review tasks | Duplicate CRM lifecycle or contact master data |
| Composio | Cross-app orchestration, dedupe checks, approved record/task actions, reconciliation evidence | Independent business truth |
| Apollo | Approved account/contact enrichment and relationship research | Unapproved volume prospecting or premature CRM creation |
| Gmail | Exact communication evidence, replies, bounces, and opt-outs | Pipeline stage truth |
| Drive | Reviewed diagnostics, account briefs, proposals, case evidence, weekly reports | Live pipeline stage |
| Local acquisition engine | Governed intake, validators, staging, audit history, generated previews | Permanent commercial truth after HubSpot reconciliation |

## HubSpot target model

Required company properties:

- `bridgeworks_service_route`
- `bridgeworks_outcome_label`
- `bridgeworks_icp_lane`
- `bridgeworks_priority_tier`
- `bridgeworks_observable_trigger`
- `bridgeworks_trigger_source_url`
- `bridgeworks_trigger_checked_at`
- `bridgeworks_relationship_path`
- `bridgeworks_diagnostic_entry`
- `bridgeworks_outreach_authority`
- `bridgeworks_suppression_reason`
- `bridgeworks_next_action_date`

Required contact properties:

- buyer role;
- relationship strength;
- public/business contact source;
- consent or lawful-contact note where required;
- personalization evidence;
- objection/suppression status.

Recommended lead statuses:

1. New target.
2. Researching.
3. Warm-up.
4. Approach ready.
5. Attempted to contact.
6. Connected.
7. Qualified.
8. Nurture.
9. Unqualified.
10. Suppressed.

Deal creation gate:

Create a deal only when a human conversation establishes a real initiative, accountable buyer, next action, and plausible commercial value. A researched account or sent email is not a deal.

## ClickUp target model

Keep the existing `Sales & Partnerships / Pipeline & Partnerships` list.

Create tasks only for work that has:

- a HubSpot company or contact link;
- one accountable owner;
- a due date;
- one deliverable or decision;
- an explicit approval state when external action is involved.

Task types:

- Research account.
- Complete evidence gap.
- Review exact approach.
- Execute approved action.
- Prepare discovery brief.
- Prepare value case/proposal.
- Process reply/bounce/opt-out.
- Ask for referral.
- Run weekly pipeline review.

Task title standard:

`[SERVICE] [ACCOUNT] — [NEXT INTERNAL ACTION]`

Example:

`[CREDIBILITY] 607 Cleaning — Review exact three-observation approach`

## Composio orchestration

Read-only daily sequence:

1. Reconcile local prospect IDs against HubSpot domain and email.
2. Check Gmail for prior contact, reply, bounce, or opt-out.
3. Pull ClickUp tasks due or overdue.
4. Prepare exceptions: duplicates, stale evidence, missing buyer, missing next action.
5. Produce an internal approval queue.

Approved-write sequence:

1. Show the exact proposed HubSpot and ClickUp changes.
2. Receive Emmanuel's approval.
3. Upsert no more than the reviewed batch.
4. Create associations and work tasks.
5. Read records back.
6. Log IDs, URLs, timestamps, rejects, and duplicates.

## Apollo gate

Apollo remains after, not before, qualification.

Before using credits:

1. Exact company count is approved.
2. Exact credit budget is approved.
3. HubSpot domain and email dedupe is complete.
4. Gmail history and suppression checks are complete.
5. Public research has established service-route fit.
6. Only business contact data needed for the commercial purpose is requested.

Suggested first enrichment batch after approval:

- Ten Tier A accounts.
- Maximum two buyer roles per account.
- Business email and LinkedIn/company role evidence only.
- No personal phone or personal email by default.

## Current connector state

Observed 2026-08-01:

- ClickUp connection `bridgeworks-ops` is active.
- HubSpot connection `bridgeworks-crm` is active through Composio.
- The native HubSpot connector can read companies, contacts, deals, and tickets.
- Native HubSpot writes and several activity objects currently require reauthorization.
- HubSpot reads found 55 companies, 32 contacts, and zero deals.
- ClickUp contains the intended Sales & Partnerships hierarchy but only two tasks.

## Recommended implementation order

1. Review the 25-account service-line list.
2. Rebuild the 76-row local source into current generated outputs.
3. Approve HubSpot property model and data reconciliation.
4. Reauthorize HubSpot write access.
5. Import or update the approved company/contact batch.
6. Create ClickUp tasks for the approved Tier A accounts.
7. Run the first five-account, one-service pilot.
8. Measure reply, discovery, qualified-opportunity, proposal, win, referral, and time-to-next-action.

