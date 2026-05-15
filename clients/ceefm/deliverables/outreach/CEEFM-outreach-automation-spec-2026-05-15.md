# CEEFM Outreach Automation Spec

Built: 2026-05-15

## Operating Reality

- Outreach can be bilingual: English plus Hungarian in the same written message.
- Phone calls are not the default. Use phone only after English capability is confirmed or a Hungarian speaker can help.
- LinkedIn actions stay manual. Do not automate connection requests or DMs.
- Email automation is allowed only after sender-domain setup is fixed.

## Sender Setup

Planned sender:

- Gmail account: `office.ceefm@gmail.com`
- Visible sender: `office@ceefm.eu`

DNS check result:

- `ceefm.eu` SPF exists, but currently authorizes Hostinger only: `v=spf1 include:_spf.mail.hostinger.com ~all`
- `_dmarc.ceefm.eu` exists: `v=DMARC1; p=none`
- `google._domainkey.ceefm.eu` does not exist

Required before automated sending:

1. Add Google mail SPF authorization if Gmail will send directly as `office@ceefm.eu`.
2. Configure Gmail Send As for `office@ceefm.eu`.
3. Add Google DKIM for `ceefm.eu`.
4. Send a test email to Gmail, Outlook, and a mail-tester address.
5. Only then approve rows for automated email.

## Workbook Tabs

- `Client Queue`: full 95-client database with verification and automation fields.
- `Text Ready Queue`: rows with enough data for written outreach.
- `Send Control`: the execution tab for email or manual LinkedIn work.
- `Missing Fields`: rows needing verified decision maker, LinkedIn, email, or research.
- `Referral Queue`: partner/referral source queue.
- `Automation Plan`: rules for automation gates.
- `Scripts`: reusable phone, LinkedIn, reply, and QA scripts.

## Send-Control Rules

Only send or draft if all are true:

- `Send Approved` = `Yes`
- `Automation Stage` = `Auto-email eligible`
- `Email Verification` = `Direct - confirmed` or `Direct - website confirmed`
- `Sender Readiness` no longer says blocked
- `Sent At` is blank

Manual approval required:

- Generic inboxes
- LinkedIn rows
- Rows marked `Research before outreach`
- Rows with missing direct email
- Rows where the only next step is phone

## Recommended Workflow

### Daily 20-minute execution

1. Open `Send Control`.
2. Filter `Send Batch` to `Batch 1 - manual LinkedIn`.
3. Send 5 to 10 LinkedIn messages manually.
4. Filter `Send Batch` to `Batch 1 - direct verified email`.
5. Review bilingual copy.
6. Set `Send Approved` to `Yes` only for clean rows.
7. Run the Apps Script in draft mode.
8. Review drafts in Gmail.
9. Send manually until sender DNS is proven clean.

### Missing-field enrichment

1. Filter `Missing Fields` by `Automation Blocker`.
2. Work in this order:
   - missing verified decision maker
   - missing LinkedIn
   - email missing
   - email generic only
   - research first
3. Use Apollo/Hunter/Tomba only after a decision maker name is found.
4. Never spend enrichment credits on generic company rows without a named person.

## Automation Build Options

### Simple option: Google Sheets + Apps Script

Best for current stage. Low setup. Good human approval.

Artifacts:

- `CEEFM-gmail-send-control-apps-script-2026-05-15.js`
- `Send Control` tab

### Heavier option: n8n

Use later when sender setup and reply tracking are stable.

Nodes:

1. Google Sheets trigger or scheduled read.
2. Filter rows where `Send Approved = Yes`.
3. Filter rows where `Automation Stage = Auto-email eligible`.
4. Gmail create draft.
5. Update `Sent At`, `Thread ID`, `Follow-up Due`.
6. Wait 3 business days.
7. Check thread for replies.
8. If no reply, create follow-up draft.

## Safety Rules

- Start with drafts, not auto-send.
- Limit to 20 drafted emails per day.
- Do not automate LinkedIn.
- Do not phone Hungarian-only prospects.
- Stop all follow-up when there is any reply.
- Keep every sent message tied to a row ID.
