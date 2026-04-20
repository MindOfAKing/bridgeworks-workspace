# Lead Qualification Automation

n8n workflow that scores inbound leads using Claude and routes them through a HOT/WARM/COLD pipeline.

## Files
| File | Purpose |
|------|---------|
| `lead-qualification-workflow.json` | Import into n8n at localhost:5678 |
| `test-payloads.json` | Test webhook with curl commands |
| `scoring-prompt.md` | The Claude prompt used for scoring (editable) |
| `SKILL.md` | This file |

## How to Set Up

### 1. Install n8n (if not already running)
```bash
npm install -g n8n
n8n start
```
Open http://localhost:5678

### 2. Import the workflow
- Go to Workflows > Import from File
- Select `lead-qualification-workflow.json`
- The workflow appears with all nodes connected

### 3. Configure credentials (5 total)

**a) Anthropic API Key**
- Settings > Credentials > Add Credential > Header Auth
- Name: `Anthropic API Key`
- Header Name: `x-api-key`
- Header Value: your Anthropic API key from `~/Projects/.env`
- Update the credential ID in the "Claude - Score Lead" node

**b) Gmail OAuth2**
- Settings > Credentials > Add Credential > Gmail OAuth2
- Name: `Gmail - emmanuelehigbai@gmail.com`
- Follow OAuth2 flow to authorize emmanuelehigbai@gmail.com
- Update credential ID in all Gmail nodes (4 nodes use this)

**c) Google Sheets**
- Settings > Credentials > Add Credential > Google Sheets OAuth2
- Or use Service Account with `~/Projects/bridgeworks-service-account.json`
- Update credential ID in all Sheet nodes (3 nodes use this)

**d) Create the Google Sheet**
- Create a new Google Sheet called "BridgeWorks Lead Pipeline"
- Sheet 1 name: "All Leads"
- Add these column headers in row 1:

```
Timestamp | Name | Email | Company | Source | Score | Reasoning | Recommended Service | Estimated Value | Market | Reply Draft | Status | Follow-up Date | Notes
```

- Copy the Sheet ID from the URL and replace `GOOGLE_SHEET_ID` in all 3 sheet nodes

### 4. Activate
- Toggle the workflow to Active
- The webhook URL will be: `http://localhost:5678/webhook/bridgeworks-lead`
- For production: use your n8n domain instead of localhost

## How It Works

```
Contact Form / WhatsApp / LinkedIn / Cold Email / Manual Entry
                          |
                    [Webhook POST]
                          |
              [Normalize Lead Data]
                          |
          [Claude Sonnet scores lead]
           HOT / WARM / COLD + reply draft
                    |
         +----------+----------+
         |          |          |
       [HOT]     [WARM]     [COLD]
         |          |          |
  - Email alert  - Email     - Log to
  - Draft reply    notice      sheet
  - Log to sheet - Draft      only
                   nurture
                 - Log to
                   sheet
```

## Entry Points

### Webhook (primary)
POST to `http://localhost:5678/webhook/bridgeworks-lead`

```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Corp",
  "source": "form",
  "message": "I need a website for my business"
}
```

Source values: `form`, `whatsapp`, `linkedin`, `cold-email`, `manual`

### Gmail Trigger (automatic)
Watches for Web3Forms submissions arriving at emmanuelehigbai@gmail.com.
Parses the email body and feeds into the same pipeline.
Checks every 5 minutes.

## Connecting bridgeworks.agency Contact Form

Your Web3Forms integration already sends form submissions to emmanuelehigbai@gmail.com. The Gmail trigger node picks these up automatically.

For direct webhook integration (faster, no 5-min delay):
1. In your contact form, add a second submission target
2. POST the form data to your n8n webhook URL
3. Map fields: name, email, company, source="form", message

## What Each Score Means

| Score | Action | Response Time |
|-------|--------|--------------|
| HOT | Immediate email alert + draft reply + sheet log | Reply within 2 hours |
| WARM | Email notice + nurture draft + sheet log | Follow up within 48 hours |
| COLD | Sheet log only | No action needed |

## Customizing the Scoring
Edit `scoring-prompt.md` to adjust:
- Service descriptions and pricing
- Ideal client criteria
- Red flags
- Reply tone and style

Then update the prompt in the "Claude - Score Lead" node.

## Monthly Cost Estimate
- Claude API: ~$0.01-0.03 per lead scored (Sonnet, ~1000 tokens per call)
- n8n: free (self-hosted)
- Gmail API: free
- Google Sheets API: free
- At 50 leads/month: ~$1.50/month total
