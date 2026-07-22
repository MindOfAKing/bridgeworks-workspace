# BridgeWorks Business Operating SOP

Version: 1.0  
Owner: Emmanuel Ehigbai  
Last updated: 2026-05-16  
Applies to: BridgeWorks agency operations, bridgeworks.agency, sales, delivery, finance, and client success.

## Purpose

This SOP exists so BridgeWorks can run as a real agency, even with a solo founder and an AI-assisted operating stack.

The business has one job:

Turn qualified business problems into paid digital growth systems, deliver them cleanly, collect money on time, and turn each engagement into proof for the next sale.

## Operating Principles

1. Systems first.
2. Paid client work second.
3. Content third.
4. Scope changes before price cuts.
5. Every lead gets a clear next step.
6. Every paid engagement gets a folder, a tracker, a delivery plan, and a payment record.
7. Every week ends with a simple scorecard.

## Business Model

BridgeWorks sells three pillars:

1. AI Growth Systems
   Lead response, qualification, routing, follow-up, reactivation, and business intelligence automation.

2. Content & Visibility Systems
   LinkedIn content systems, GEO and AI search visibility, technical SEO, schema, newsletter infrastructure, and content dashboards.

3. Digital Infrastructure
   Websites, landing pages, brand systems, AI chat, lead capture, hosting, and handover.

Primary engagement types:

- Done For You
- Done With You
- Advisory

Entry offer:

- AI Audit, from EUR 500, delivered in 7 to 10 days.

## Source Of Truth

Use these locations as the operating source of truth:

- Agency operations: `C:/Users/User/Projects/bridgeworks-workspace/`
- Business brain: `C:/Users/User/Projects/business-brain/`
- Live website: `C:/Users/User/Projects/bridgeworks-agency/`
- Content studio (production mirror of the canonical Drive content library; on production HOLD): `C:/Users/User/Projects/BridgeWorks-Content-Studio/`
- Clients: `C:/Users/User/Projects/bridgeworks-workspace/clients/`
- Pipeline: `C:/Users/User/Projects/bridgeworks-workspace/pipeline/`
- Proposals and agreements: `C:/Users/User/Projects/bridgeworks-workspace/documents/`
- Daily session logs: `C:/Users/User/Projects/bridgeworks-workspace/sessions/`

Do not run the business from scattered chat history. If a decision matters, write it into the workspace.

## Daily Operating Rhythm

### Start Of Day, 15 Minutes

1. Check inbound leads from bridgeworks.agency.
2. Check email, LinkedIn, and WhatsApp for client or prospect messages.
3. Check active client obligations.
4. Choose one main business move for the day.
5. Write the day plan in the session log or active work tracker.

Daily priority order:

1. System that unlocks revenue or saves time this week.
2. Paid client deliverable.
3. Sales follow-up.
4. Content that proves the thing BridgeWorks sells.

### Midday Check, 5 Minutes

Ask:

- Is today still pointed at revenue, delivery, or system stability?
- Is any client waiting on me?
- Is any hot prospect waiting on me?
- Is there one task I should kill because it does not move the business?

### End Of Day, 10 Minutes

Append this to the live operating log in `CLAUDE.md` or the relevant session file:

```text
### YYYY-MM-DD
- Closed:
- Opened:
- Money moved:
- Client risk:
- Tomorrow's one:
```

If nothing was closed, write why. No drama. Just data.

## Weekly Operating Rhythm

Run this every Friday.

1. Review pipeline.
2. Review active client delivery.
3. Review invoices sent, paid, and overdue.
4. Review content published.
5. Review systems improved.
6. Pick next week's single best close.

Weekly scorecard:

```text
Week of:

Revenue:
- New sales:
- Invoices sent:
- Payments received:
- Overdue:

Pipeline:
- New leads:
- Discovery calls booked:
- Proposals sent:
- Follow-ups due:

Delivery:
- Active clients:
- Deliverables shipped:
- Risks:
- Next commitments:

Systems:
- Fixed:
- Built:
- Still broken:

Content:
- Published:
- Repurposed:
- Best signal:

Next week's single best close:
```

## Lead Capture SOP

Goal:

A contact form submission on bridgeworks.agency must arrive somewhere visible within 5 minutes.

Required inbound destinations:

- Email inbox
- Pipeline tracker
- Optional: Telegram or WhatsApp alert through automation

When a lead arrives:

1. Create or update the lead record.
2. Check source, business type, country, stated problem, and urgency.
3. Reply within 24 hours. If the lead looks strong, reply within 2 hours.
4. Offer one clear next step.

Lead statuses:

- New
- Qualified
- Discovery booked
- Proposal needed
- Proposal sent
- Negotiation
- Won
- Lost
- Dormant

Qualification rules:

Strong fit if:

- The business has an active offer, team, customers, or serious launch timeline.
- The problem maps to one of the three BridgeWorks pillars.
- The owner understands that tools, implementation, and strategy cost money.
- The project can become a proof point.

Weak fit if:

- They want free strategy.
- They need a full business model before any digital system can help.
- They expect ad spend to be included in service fees.
- They ask for a discount without reducing scope.

First response structure:

```text
Hi [Name],

Thanks for reaching out. I looked at what you shared.

The main thing I would want to understand is [specific problem].

Best next step is a short discovery call. We will use it to confirm the goal, current setup, timeline, and whether BridgeWorks is the right fit.

Here are two times:
- [Option 1]
- [Option 2]

Emmanuel
BridgeWorks
```

## Sales SOP

### Discovery Call

Before the call:

1. Research the business.
2. Check website, LinkedIn, Google Business Profile, and public content.
3. Identify one likely revenue leak.
4. Prepare 5 questions.

During the call:

1. Confirm business model.
2. Confirm current goal.
3. Find cost of inaction.
4. Find decision maker.
5. Confirm budget range or buying reality.
6. Explain only the relevant BridgeWorks pillar.
7. End with a clear next step.

Discovery call close:

```text
Based on what you shared, I see two possible routes.

Quick Win: [smaller scope]
Growth System: [larger scope]

I will send a short proposal with both options by [date].
```

### Proposal

Every proposal must include:

- Current situation
- Business problem
- Desired outcome
- Scope
- Timeline
- Deliverables
- What the client provides
- Price
- Payment terms
- Next step

Default close:

- Two options: Quick Win and Growth System.
- 50% upfront, 50% on delivery.
- Retainers require 3-month minimum.
- Ad spend is separate.
- Client owns accounts, assets, and code unless agreed otherwise.

Pricing rules:

- Never discount without reducing scope.
- NGN pricing is not a discount.
- Lead with bundles.
- Price against business value, not hours.
- Retainer baseline is 20% of project fee per month.

### Follow-Up

Follow-up schedule after proposal:

- Day 1: confirm received.
- Day 3: answer questions.
- Day 7: ask if decision is still active.
- Day 14: final useful follow-up.
- Day 30: move to dormant or nurture.

Follow-up template:

```text
Hi [Name],

Quick check on the BridgeWorks proposal.

The decision point is really this:
[specific business tradeoff].

If this is still active, I can help you choose between the Quick Win and Growth System option.

Emmanuel
```

## Client Onboarding SOP

When a deal is won:

1. Create client folder in `clients/`.
2. Create delivery tracker.
3. Create finance record.
4. Send invoice through szamlazz.hu.
5. Confirm payment instructions.
6. Schedule kickoff.
7. Collect access and assets.
8. Confirm first milestone.

Client folder structure:

```text
clients/[client-name]/
- 00-admin/
- 01-discovery/
- 02-strategy/
- 03-delivery/
- 04-reports/
- 05-assets/
- 06-handover/
```

Kickoff agenda:

1. Confirm goal.
2. Confirm scope.
3. Confirm timeline.
4. Confirm communication channel.
5. Confirm decision maker.
6. Confirm access needed.
7. Confirm first delivery date.

Access checklist:

- Website admin
- Domain registrar
- Hosting
- Analytics
- Search Console
- Google Business Profile
- Social accounts
- CRM or contact form inbox
- Email platform
- Payment or booking tools, if relevant

## Delivery SOP

Every active client needs:

- One outcome statement.
- One active tracker.
- One next milestone.
- One weekly status update.
- One risk log.

Delivery stages:

1. Diagnose
2. Design
3. Build
4. Review
5. Launch
6. Measure
7. Handover

Weekly client update:

```text
Hi [Name],

Here is this week's BridgeWorks update.

Completed:
- 

In progress:
- 

Waiting on:
- 

Next:
- 

Risk or decision:
- 

Emmanuel
```

If a client delays feedback:

1. Send one clear reminder.
2. Name what is blocked.
3. Give a decision deadline.
4. Move timeline if needed.

Delay message:

```text
Hi [Name],

I need [specific item] before I can continue [specific work].

If I receive it by [date], we stay on the current timeline.
If it comes later, I will move the delivery date accordingly.

Emmanuel
```

## Finance SOP

Current payment reality:

- Quote in EUR where relevant.
- Invoice in HUF through szamlazz.hu using the correct exchange rate.
- Use OTP personal account until Wise Business is active.
- Stripe payment links only after live setup is complete.
- The szamlazz invoice is the legal payment trigger.

Invoice process:

1. Confirm accepted scope.
2. Create invoice in szamlazz.hu.
3. Add VAT exemption note where required.
4. Include payment reference.
5. Send invoice to client.
6. Log invoice in finance tracker.
7. Confirm payment received.
8. Move project to active delivery only after upfront payment, unless explicitly agreed.

Finance tracker fields:

- Client
- Project
- Currency quoted
- Invoice currency
- Invoice number
- Invoice date
- Due date
- Amount
- Paid amount
- Status
- Payment account
- Notes

Invoice statuses:

- Draft
- Sent
- Paid
- Part-paid
- Overdue
- Cancelled

Overdue process:

- Day 1 overdue: polite reminder.
- Day 3 overdue: direct reminder with invoice number.
- Day 7 overdue: pause non-critical work.
- Day 14 overdue: escalation message and new payment deadline.

## Content SOP

BridgeWorks content must prove the service.

Best content types:

- Before and after audits
- Systems built in public
- Lessons from client delivery
- AI visibility findings
- Website teardown clips
- Founder notes about building a solo AI-powered agency

Weekly minimum:

- 2 LinkedIn posts
- 1 proof-based post from current work
- 1 direct offer or case-study style post

Content rule:

Do not publish vague claims. Show the system, the signal, the result, or the decision.

Post structure:

```text
Problem:

What I found:

What I changed or would change:

Why it matters:

BridgeWorks helps [type of client] fix this by [specific offer].
```

## Website SOP For bridgeworks.agency

The website exists to create qualified conversations.

Monthly checks:

1. Contact form works.
2. Submission reaches inbox within 5 minutes.
3. Offer pages match current services.
4. Pricing signals are not misleading.
5. Calendar or call booking path works.
6. Analytics is active.
7. Mobile layout is clean.
8. Case studies and proof are current.

After each new proof point:

1. Add it to the relevant client folder.
2. Turn it into a short case note.
3. Add it to website, proposal, or LinkedIn content where useful.

## Tool Stack SOP

Use tools for specific jobs:

- Google Workspace: documents, email, calendar, shared files.
- LinkedIn: primary B2B channel.
- WhatsApp: client communication where appropriate.
- Vercel: website hosting.
- React, Next.js, Tailwind, TypeScript: web builds.
- Sanity: CMS where needed.
- szamlazz.hu: invoices.
- Wise Business: future primary business bank.
- Stripe: future online payments.
- Apollo or chosen prospecting tool: outbound list building.
- AI tools: research, drafting, analysis, code, automation, and review.

Tool rule:

If two tools do the same job, pick one and shut the other down.

## Prospecting SOP

Run prospecting in focused batches.

Batch process:

1. Pick one niche or signal.
2. Build a list of 20 prospects.
3. Check for a visible business problem.
4. Write a short diagnosis.
5. Send direct outreach.
6. Follow up twice.
7. Log status.

Good prospect signals:

- Website exists but does not convert.
- Strong offline business, weak digital system.
- Growing business with no lead follow-up process.
- Founder posts expertise but has no content system.
- Business targets CEE or Africa and needs better English-language positioning.
- Service business with slow speed-to-lead.

Outreach structure:

```text
Hi [Name],

I noticed [specific signal].

The likely issue is [business consequence].

I run BridgeWorks. We build digital growth systems for small businesses across Africa and Central Europe.

I can send over a short teardown if useful.

Emmanuel
```

## Decision SOP

When choosing what to do next, ask:

1. Does this help BridgeWorks sell, deliver, collect, or prove?
2. Does it support an active client?
3. Will it save time this week?
4. Can it be finished in one session?
5. Is this a parked idea pretending to be urgent?

If the answer is no to the first two, do not do it during business hours.

## Emergency SOP

### Client Complaint

1. Acknowledge within 24 hours.
2. Restate the issue in plain language.
3. Check the project scope and timeline.
4. Offer a fix, decision, or revised date.
5. Write the resolution in the client folder.

### Broken Website Or Automation

1. Confirm the issue.
2. Capture screenshot or error.
3. Check recent changes.
4. Fix the smallest confirmed cause.
5. Test.
6. Log what happened.

### Cash Pressure

1. Check invoices due.
2. Follow up overdue payments.
3. Push one paid audit offer.
4. Contact warm prospects.
5. Pause non-essential tools.
6. Do not start speculative builds.

## Monthly Review

Run on the last business day of the month.

Review:

- Revenue booked
- Revenue collected
- Active clients
- Leads by source
- Proposals sent
- Close rate
- Delivery quality
- Systems built
- Tools to cancel
- Proof points created
- Next month focus

Monthly decision:

Choose one main business constraint:

- Not enough leads
- Not enough calls
- Not enough proposals
- Not enough closes
- Delivery too slow
- Cash collection weak
- Proof not visible

Then pick one fix for the next month.

## Definition Of A Healthy Week

A healthy BridgeWorks week has:

- One system improved.
- One client commitment shipped.
- One sales conversation advanced.
- One invoice sent, paid, or followed up.
- Two proof-building content pieces published.
- One clean Friday review.

If the week has no sales motion, the business is drifting.

If the week has no delivery motion, the business is risking trust.

If the week has no systems motion, the founder is becoming the bottleneck.

