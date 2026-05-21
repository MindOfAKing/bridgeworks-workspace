# BridgeWorks Inbound Lead Intake System

Version: 1.0  
Created: 2026-05-17  
Owner: Emmanuel Ehigbai

## Purpose

Every inbound lead from bridgeworks.agency should become visible, qualified, and ready for reply fast.

Target:

```text
Website form
→ email notification
→ pipeline record
→ HOT/WARM/COLD qualification
→ Gmail reply draft
→ approval brief
```

## Current Website State

The website contact API already supports an ops webhook:

```text
BRIDGEWORKS_OPS_INBOUND_URL
BRIDGEWORKS_OPS_WEBHOOK_SECRET
```

But these variables are not currently set in `bridgeworks-agency/.env.local`.

Until an ops webhook or n8n endpoint is connected, Web3Forms remains the primary delivery path.

## Required Fields

Track:

- Date received
- Name
- Email
- Company
- Website
- Country
- Service interest
- Message
- Source page
- Status
- Priority
- Lead score
- Recommended service
- Next follow-up date
- Draft reply
- Gmail draft ID
- Notes

## Statuses

Use these statuses:

- New
- Qualified
- Reply drafted
- Needs approval
- Sent
- Follow-up due
- Discovery booked
- Proposal needed
- Won
- Lost
- Dormant
- Spam

## Priority Rules

Use `lead-qualifier`.

HOT:

- Real business
- Specific need
- Clear timeline
- Budget signal
- CEE or Nigeria market
- Asks for call, quote, audit, proposal, or website help

WARM:

- Real business
- Vague need
- No budget or timeline yet
- Needs education

COLD:

- No clear business
- Free-work request
- Spam
- Outside BridgeWorks scope

## Reply Rule

Never auto-send first replies.

Create Gmail drafts and mark the lead as `Needs approval`.

## First Reply Template

```text
Hi [Name],

Thanks for reaching out.

I looked at what you shared. The main thing I would want to understand is [specific issue].

Best next step is a short discovery call. We can use it to confirm the goal, current setup, timeline, and whether BridgeWorks is the right fit.

Are you free [two specific options]?

Emmanuel
BridgeWorks.agency
office@bridgeworks.agency
```

## Implementation Options

### Option 1: n8n Webhook

Best for the 5-minute target.

```text
bridgeworks.agency contact form
→ BRIDGEWORKS_OPS_INBOUND_URL
→ n8n webhook
→ Google Sheet row
→ Telegram alert
→ Gmail draft
→ approval brief
```

### Option 2: Make/Zapier

Fastest no-code setup.

```text
Web3Forms email
→ parser
→ Google Sheet
→ Gmail draft
→ Telegram/email alert
```

### Option 3: Codex Scheduled Watcher

Good for local control, but not true 5-minute realtime.

Use this as backup:

```text
scheduled intake automation
→ check inbound tracker / email context
→ qualify new leads
→ draft replies
→ approval brief
```

## Recommended Setup

Use n8n as the real intake endpoint.

Set these on Vercel and local `.env.local`:

```text
BRIDGEWORKS_OPS_INBOUND_URL=https://[your-n8n-domain]/webhook/bridgeworks-inbound
BRIDGEWORKS_OPS_WEBHOOK_SECRET=[long-random-secret]
```

Then the website route already forwards form submissions to ops.

## Approval Flow

```text
New lead
→ lead-qualifier
→ draft reply
→ approval brief
→ Emmanuel approves
→ send
→ follow-up scheduled
```

