# BridgeWorks Prospecting Automation Map

Version: 1.0  
Created: 2026-05-17

## Automation Priority

Build automation in this order:

1. Market triage
2. Prospect tracker in Google Sheets
3. Daily outreach queue
4. Prospect enrichment
5. Message drafting
6. Gmail draft creation
7. Audit preview PDF generation
8. Follow-up email with PDF attachment
9. Follow-up reminders
10. Weekly scorecard

## Recommended Stack

Use:

- Google Sheets as the prospect database
- Gmail as draft and send layer
- Google Drive as file storage
- Apollo as the main prospecting database if one must be kept
- Hunter or Tomba only for email enrichment
- Google Maps or Places API for local company discovery
- Perplexity or Google Custom Search for research
- YouTube API plus `youtube-channel-scout` for market and operator intelligence
- n8n as the automation runner
- Telegram as instant alert channel
- Codex or Claude as drafting and analysis layer

Geography rule:

- Hungary is the first proof-adjacent lane, not the ceiling.
- Add prospects daily across CEE, UK/EU, Nigeria/Africa, and other English-speaking markets where the pain is visible.
- Segment by buyer type and pain, not by country alone.

Avoid:

- Running Apollo, Hunter, and Tomba as three separate CRMs
- Creating a custom dashboard before the spreadsheet works
- Automating sending before message quality is proven

## Plugin And MCP Usage

## Skill Layer

Use skills as the operating layer above plugins and APIs.

### agent-market-strategy

Use before choosing a campaign.

Answers:

- Is this market worth selling into now?
- What is the likely revenue opportunity?
- What offer should BridgeWorks lead with?
- Is the market better for audit, website build, automation, retainer, or advisory?
- What is the single biggest growth lever?

Output feeds:

- Campaign choice
- Offer choice
- Estimated value
- Priority score

### agent-market-competitive

Use before writing outreach for a new niche.

Answers:

- Who are the visible competitors?
- How do prospects in this niche currently position themselves?
- What language is common in the market?
- What gaps are competitors leaving open?
- What angle can BridgeWorks own?

Output feeds:

- Outreach angle
- Positioning gap
- Teardown hook
- Content ideas

### agent-market-conversion

Use on individual prospect websites before outreach.

Answers:

- What is the primary conversion path?
- Where is the lead capture friction?
- Is the CTA weak, hidden, generic, or missing?
- What quick fix would improve enquiries?

Output feeds:

- Signal found
- Growth leak
- Message 1
- Audit recommendation

### agent-market-technical

Use on individual prospect websites when SEO, tracking, schema, speed, or AI visibility may be the hook.

Answers:

- Is the technical marketing foundation weak?
- Are metadata, sitemap, robots, schema, and tracking present?
- Is the site ready for search and AI discovery?
- What technical fix has revenue impact?

Output feeds:

- AI visibility angle
- Technical audit note
- GEO/SEO offer fit

### prospecting-department

Use for:

- Campaign choice
- Market choice
- Prospect source logic
- Sales process discipline
- CEE versus Nigeria channel choice

This is the default owner of the whole prospecting workflow.

### lead-qualifier

Use for:

- Scoring HOT, WARM, or COLD prospects
- Recommending a BridgeWorks service
- Estimating value
- Drafting reply or first message
- Deciding whether to enrich with Apollo, Hunter, or Tomba

Rule:

Do not burn enrichment credits on COLD leads.

### competitive-research

Use for:

- Market landscape scans
- Competitor positioning
- Prospect niche research
- Finding gaps BridgeWorks can use in outreach

Best first research target:

```text
facility management and property service companies in Budapest and Central Europe
```

This skill is useful for broad market scans. The `agent-market-*` skills are useful when the scan needs structured market scoring.

### geo-audit / geo-citability / geo-technical

Use when the outreach angle is AI visibility, Google visibility, schema, or search proof.

### ads-audit / ads-landing

Use when the prospect appears to run paid ads or sends traffic to a weak landing page.

### content-department

Use after each good teardown or client insight.

Output:

- LinkedIn post draft
- Case-study note
- Proof asset for future prospecting

### youtube-channel-scout

Use for:

- Finding videos worth extracting from AI agency, sales, automation, GEO, SEO, and service-business marketing channels.
- Spotting offer, pricing, client delivery, sales, and automation ideas.
- Feeding better prospecting angles and content proof.

Rule:

Scout channels first. Extract videos only when they are likely to change a BridgeWorks action.

Source files:

- `pipeline/youtube-scout/channels.csv`
- `pipeline/youtube-scout/scout-results.md`
- `pipeline/youtube-scout/extraction-queue.csv`
- `pipeline/youtube-scout/actions-from-youtube.md`

### Google Drive / Sheets

Use for:

- Creating the live prospect tracker
- Updating statuses
- Searching rows
- Weekly reporting

First action:

Import `prospect-tracker.csv` into Google Sheets.

### Gmail

Use for:

- Creating outreach drafts
- Creating follow-up drafts
- Attaching branded audit preview PDFs to follow-up drafts
- Reviewing sent replies later

Rule:

Create drafts first. Do not auto-send until the first 50 messages prove the angle.

### PDF Skill

Use for:

- Generating branded audit preview reports
- Attaching the right PDF to follow-up 1
- Keeping report format consistent across GEO, market, conversion, technical, and speed-to-lead audits

Rule:

Free audit PDFs are preview reports. They show the problem and next step. They do not give away the full implementation plan.

### Google Calendar

Use later for:

- Discovery call reminders
- Follow-up review blocks
- Weekly prospecting sprint review

### Supabase

Use later only if:

- Google Sheets becomes too slow
- A custom dashboard needs real-time filtering
- Multiple tools need a structured backend

Do not start with Supabase.

### Vercel

Use later for:

- A private command center
- Form-to-pipeline integration
- Website lead capture

Do not build the dashboard until prospecting motion exists.

## API Usage

### Google Maps / Places

Use to collect:

- Company name
- Website
- Phone
- Address
- Rating
- Review count
- Business category

Best first searches:

```text
facility management Budapest
property management Budapest
office cleaning Budapest
apartment management Budapest
serviced apartment operator Budapest
facility management Lagos
commercial cleaning Lagos
property management Nigeria
serviced apartment operator London
property management Warsaw
facility management Prague
```

### Hunter Or Tomba

Use to enrich:

- Domain email patterns
- Company emails
- Contact emails

Rule:

One enrichment tool should win. Default decision: keep Apollo as main source, use Hunter or Tomba only if it clearly improves email discovery.

### Perplexity / Google CSE

Use to research:

- Company proof
- Services
- Recent news
- Leadership names
- Specific pain signals

### Gmail API

Use to create:

- Message 1 draft
- Follow-up 1 draft with audit preview PDF attachment
- Follow-up 2 draft

Do not auto-send at first.

## n8n Workflow 1: Daily Prospect Builder

Trigger:

- Manual button or weekday schedule

Steps:

1. Read target niche and location.
2. Fetch companies from Google Maps or search.
3. Add raw companies to Google Sheet.
4. Remove duplicates by website or company name.
5. Mark status as `New`.

Output:

- 20 new raw prospects per run.

## n8n Workflow 0: Market Triage

Trigger:

- Manual button before starting a new 7-day sprint.

Input:

- Market
- Niche
- Location
- BridgeWorks offer hypothesis

Steps:

1. Run `agent-market-strategy` on the niche.
2. Run `agent-market-competitive` on the niche.
3. Pick the top 3 pain angles.
4. Pick the best BridgeWorks entry offer.
5. Decide whether to proceed, park, or reject the niche.

Output:

- Market score from 0 to 10.
- Recommended offer.
- Best outreach angle.
- Search terms for prospect collection.
- Decision: Proceed, Park, or Reject.

## n8n Workflow 2: Qualification Assistant

Trigger:

- New row with status `New`.

Steps:

1. Visit website or fetch page text.
2. Check contact path.
3. Check service pages.
4. Check visible proof.
5. Generate signal found.
6. Generate growth leak.
7. Score prospect.
8. Set priority.

Output:

- Status becomes `Qualified` or `Rejected`.

## n8n Workflow 3: Outreach Draft Builder

Trigger:

- Row status becomes `Qualified`.

Steps:

1. Pick outreach angle.
2. Draft message 1.
3. Draft follow-up 1.
4. Draft follow-up 2.
5. Check that each draft includes pain versus outcome.
6. Update tracker.
7. Add A priority prospects to daily queue.

Output:

- Status becomes `Message drafted`.

## n8n Workflow 4: Gmail Draft Creator

Trigger:

- Row status becomes `Message drafted` and email exists.

Steps:

1. Create Gmail draft.
2. Write Gmail draft ID back to tracker.
3. Set status to `Draft ready`.
4. Send Telegram alert.

Output:

- Manual review in Gmail.

## n8n Workflow 5: Follow-Up Scheduler

Trigger:

- Row status becomes `Contacted`.

Steps:

1. Set follow-up 1 date to 3 business days later.
2. Set follow-up 2 date to 7 business days later.
3. Add to daily outreach queue on due date.

Output:

- No contacted prospect is forgotten.

## n8n Workflow 5A: Audit Preview PDF Generator

Trigger:

- Row status becomes `Contacted`.
- `audit_preview_required` is true.

Steps:

1. Read prospect row.
2. Select report type from outreach angle.
3. Run the matching skill:
   - `geo-audit` for GEO and AI visibility.
   - `agent-market-strategy` and `agent-market-competitive` for market audit.
   - `agent-market-conversion` for conversion audit.
   - `agent-market-technical` for technical audit.
   - `lead-qualifier` plus `agent-market-conversion` for speed-to-lead preview.
4. Reduce output to three findings.
5. Generate branded PDF preview.
6. Save PDF to Drive.
7. Write PDF link and local path back to tracker.

Output:

- Status becomes `Audit preview ready`.

## n8n Workflow 5B: Follow-Up With Audit Preview

Trigger:

- Follow-up 1 date is due.
- `audit_preview_status` is `Ready`.

Steps:

1. Create Gmail follow-up draft.
2. Attach audit preview PDF.
3. Include one-sentence pain summary and one-sentence outcome summary in email body.
4. Write Gmail draft ID back to tracker.
5. Send Telegram alert for manual review.

Output:

- Status becomes `Follow-up 1 draft ready`.

Rule:

Do not auto-send until the report quality is proven.

## n8n Workflow 6: Weekly Prospecting Scorecard

Trigger:

- Friday afternoon.

Steps:

1. Count raw prospects added.
2. Count qualified prospects.
3. Count messages sent.
4. Count replies.
5. Count discovery calls.
6. Count proposals.
7. Draft weekly review.

Output:

- Weekly prospecting scorecard.

## First Build Decision

Build now:

- Google Sheets tracker
- Manual daily queue
- Gmail draft flow

Build next:

- Google Maps discovery
- Enrichment
- Scoring

Build later:

- Private dashboard
- Auto-send
- Supabase backend
