# Codex Handoff: Send CEEFM Handover Email

## What this is

The CEEFM digital growth engagement (16 weeks, client: Victor / CEEFM Kft, Budapest) is complete.
A full handover package has been prepared. Your task is to upload it to Google Drive and send the
handover email to Victor with the Drive link.

---

## What has already been done

1. **Handover package ZIP created** at:
   `C:\Users\User\Projects\bridgeworks-workspace\clients\ceefm\CEEFM-Handover-Package.zip`
   Size: ~38.76 MB, 86 files.
   
   Contents:
   - `1-Reports/` — Handover PDF, GEO audit PDF (78/100 final), Marketing audit PDF, 4 monthly report PDFs
   - `2-Outreach/` — Prospect list CSV (84 companies), outreach queue CSV, cold email sequence, full playbook
   - `3-Deliverables/` — GBP description, Google Ads plan, RSA copy, Aparthotel Standard draft, LinkedIn optimisation doc
   - `4-Content/` — April and May LinkedIn content calendars + 29 post images
   - `5-Website-Source/` — Full Astro source code for ceefm.eu (38 files)

2. **Gmail draft already created** (draft ID: `r-6528220436381025947`) in Emmanuel's Gmail account
   (emmanuelehigbai@gmail.com). The draft body is complete but has no attachment.

---

## Your task (in order)

### Step 1: Upload the ZIP to Google Drive

Use the Google Drive MCP (`mcp__claude_ai_Google_Drive__create_file` or equivalent) to upload
`CEEFM-Handover-Package.zip` from the path above.

- Upload to Emmanuel's personal Drive (root or a folder named "CEEFM Handover 2026")
- After upload, use the Drive MCP to get the file ID and set sharing permissions to "anyone with the link can view"
- Retrieve the shareable link

### Step 2: Delete the existing draft

The existing Gmail draft (ID: `r-6528220436381025947`) has no Drive link. Delete it (or find it 
and note it for reference), then create a new draft with the Drive link included.

Use `mcp__claude_ai_Gmail__create_draft` to create the new draft with the following content:

**To:** office@ceefm.eu  
**Subject:** CEEFM Digital Growth - Engagement Handover  
**Body** (insert the actual Drive share link where indicated):

---

Hi Victor,

The 16-week digital growth engagement is now complete. I have prepared a full handover package for you.

Download your files here: [INSERT GOOGLE DRIVE SHARE LINK]

The folder contains:

1-Reports
- Handover document (what was built, what is live, what to do next)
- GEO audit report (final score: 78/100, up from 16 at the start of the engagement)
- Marketing audit report
- Monthly performance reports from April and May

2-Outreach
- Full prospect list (84 companies remaining for cold outreach)
- Prioritised outreach queue
- Cold email sequence in English and Hungarian
- Full outreach playbook with step-by-step operating guide

3-Deliverables
- Ready-to-paste Google Business Profile description (EN and HU)
- Google Ads campaign plan and RSA copy
- Aparthotel Operating Standard draft (14 categories)
- LinkedIn company page optimisation document

4-Content
- April and May LinkedIn content calendars
- All 29 post images

5-Website-Source
- Complete source code for ceefm.eu (pass this to any developer you work with)

The single highest-impact action you can take right now is completing the Google Business
Profile verification. The postcard should have arrived. Go to business.google.com and confirm
it. That one step is estimated to push your GEO score from 78 to 81-82 and puts CEEFM on
Google Maps for facility management searches in Budapest.

All priority actions are listed and ranked in the handover document, Section 3.

It has been a pleasure working with you. I wish CEEFM continued growth.

Best regards,
Emmanuel Ehigbai
BridgeWorks
office@bridgeworks.agency
bridgeworks.agency

---

### Step 3: Send the draft

Once the draft is created and confirmed, use the Gmail MCP or available send tool to send it.

If no send tool is available, confirm to Emmanuel that the draft is ready in Gmail and he should
review and send it manually.

---

## Context if needed

- Emmanuel's email: emmanuelehigbai@gmail.com
- Victor's email: office@ceefm.eu
- BridgeWorks brand rules: no em dashes, no AI slop, short sentences
- The engagement ran from late March 2026 to June 2026
- GEO score at close: 78/100 (up from 16/100 at baseline — a 62-point gain)
- The handover document PDF is the primary deliverable; everything else supports it

---

## If Drive upload is blocked or unavailable

If you cannot upload to Drive programmatically, do one of the following:

**Option A:** Split the zip into parts under 25MB and attach directly to the Gmail draft:
```python
import zipfile, math, os

zip_path = r'C:\Users\User\Projects\bridgeworks-workspace\clients\ceefm\CEEFM-Handover-Package.zip'
chunk_size = 24 * 1024 * 1024  # 24MB chunks

with open(zip_path, 'rb') as f:
    data = f.read()

parts = math.ceil(len(data) / chunk_size)
for i in range(parts):
    chunk = data[i*chunk_size:(i+1)*chunk_size]
    part_path = zip_path.replace('.zip', f'.part{i+1}.zip')
    with open(part_path, 'wb') as out:
        out.write(chunk)
    print(f'Part {i+1}: {part_path} ({len(chunk)/1024/1024:.2f} MB)')
```
Then encode each part as base64 and pass to Gmail draft attachments field.

**Option B:** Tell Emmanuel to go to drive.google.com, upload the zip manually, get a share link,
then open the Gmail draft (ID: r-6528220436381025947) and add the link before sending.

---

*Prepared by Claude Code — 2026-06-11*
