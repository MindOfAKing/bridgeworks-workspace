# BridgeWorks Inbound Automation Map

Version: 1.0  
Created: 2026-05-17

## Target Workflow

```text
bridgeworks.agency contact form
→ direct Google Sheets append
→ inbound lead tracker
→ lead qualification
→ Gmail draft
→ approval brief
→ approved send
→ follow-up
```

## Existing Website Hook

The website contact route now supports direct Google Sheets append using:

```text
BRIDGEWORKS_INBOUND_SHEET_ID
BRIDGEWORKS_INBOUND_SHEET_RANGE
GOOGLE_SERVICE_ACCOUNT_JSON
```

It also still supports the future ops webhook:

```text
BRIDGEWORKS_OPS_INBOUND_URL
BRIDGEWORKS_OPS_WEBHOOK_SECRET
```

This means the website can run without n8n or Make now, then add n8n later.

## Direct Google Sheets Workflow

Current path:

1. Website receives contact form submission.
2. API validates and sanitizes the lead.
3. API authenticates with Google using the service account JSON.
4. API appends the lead to BridgeWorks Inbound Leads.
5. API sends Web3Forms notification email.
6. Codex Inbound Lead Intake Engine qualifies the row and drafts a reply.

Required manual permission:

Share the Google Sheet with the service account email as Editor.

The service account email is in:

```text
C:/Users/User/Projects/bridgeworks-service-account.json
```

Field:

```text
client_email
```

## n8n Workflow

Future path:

Trigger:

- Webhook: `/webhook/bridgeworks-inbound`

Steps:

1. Verify `x-bridgeworks-secret`.
2. Normalize payload:
   - name
   - email
   - company
   - businessStage
   - challenge
   - additionalContext
   - message
   - source
   - timestamp
3. Append row to Google Sheet.
4. Run lead qualification prompt or pass to Codex approval system.
5. Send Telegram alert:

```text
New BridgeWorks lead: [Name], [Company], [Challenge], [Priority]
```

6. Create Gmail draft reply.
7. Mark status `Needs approval`.

## Codex Automation Backup

The Codex automation should:

1. Read `inbound-leads.csv`.
2. Find rows with status `New`.
3. Apply `lead-qualifier`.
4. Draft a reply.
5. Create Gmail draft when email exists.
6. Update status to `Needs approval`.
7. Include item in Daily Approval Brief.

## Tools And Skills

Use:

- `lead-qualifier`
- Gmail drafts
- Google Sheets
- Telegram alert through n8n when available
- Daily Approval Brief

## Hard Rules

- Never auto-send inbound replies.
- Respond to HOT leads first.
- Inbound beats cold prospecting when both are waiting.
- Keep data minimal and GDPR-aware.
- Do not store unnecessary personal data.
