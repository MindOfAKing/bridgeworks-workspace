# BridgeWorks YouTube Scout System

Version: 1.0  
Created: 2026-05-17  
Owner: Emmanuel Ehigbai

## Purpose

Use YouTube as a business intelligence and service-fulfillment source for BridgeWorks.

The goal is not to watch more videos.

The goal is to find videos that improve:

- Service offers
- Pricing models
- Client delivery
- Service fulfillment
- Delivery SOPs
- Client onboarding
- Client reporting
- Retention and account growth
- AI agency operations
- Sales processes
- Automation systems
- Content systems
- Market positioning
- Prospecting angles
- Technical implementation standards
- Website design and conversion quality
- GEO, SEO, schema, and AI visibility practice
- Proposal quality
- Founder operating rhythm

## Skill Used

Use these skills:

- `youtube-channel-scout` to decide which videos are worth extracting.
- `youtube-intelligence` for transcript-based business intelligence.
- `youtube-learning-pipeline` to turn approved videos into structured learning.
- `youtube-offer-extraction` when a video explains offer, pricing, packaging, or sales positioning.

The skill reviews recent channel titles and descriptions from the last 6 months and returns only videos worth extracting.

## API

Use `YOUTUBE_API_KEY` from:

```text
C:/Users/ELITEX21012G2/Projects/.env
```

Use the YouTube Data API first for:

- Channel lookup
- Recent uploads
- Video titles
- Video descriptions
- Published dates
- Video URLs

Use transcripts for:

- Frameworks
- Tools
- Systems
- Processes
- Angles
- Offer structures
- Pricing logic
- Delivery methods
- Client success ideas
- SOP updates
- Adopt/adapt/reject decisions

Fallback to web search only if the API fails or a channel cannot be resolved.

Do not print or expose the API key in logs or reports.

## Transcript Layer

The YouTube Scout Engine has two stages.

### Stage 1: Scout

Use channel metadata, recent uploads, titles, and descriptions.

Output:

- Videos worth extracting
- Why they matter
- BridgeWorks pillar affected
- Extraction score

### Stage 2: Extract

Use transcript or captions where available.

If transcript is unavailable, use:

- Description
- Chapters
- Public article/show notes
- Manual summary from available video metadata

Do not pretend a transcript was read if it was not.

## Extraction Targets

Every approved extraction must identify:

- Frameworks to adopt
- Frameworks to adapt
- Tools mentioned
- Systems mentioned
- Delivery methods
- Sales angles
- Pricing or packaging ideas
- Client communication patterns
- Risks or bad advice to reject
- One BridgeWorks action

## Adopt / Adapt / Reject Rule

Every extracted idea must be labeled:

- `Adopt`: Use as-is because it fits BridgeWorks now.
- `Adapt`: Modify for BridgeWorks context, market, or solo-founder capacity.
- `Reject`: Interesting but not useful, too complex, too expensive, off-brand, or wrong timing.

Default to `Adapt`.

## Operating Rule

Scout first. Extract later.

Do not summarize every video from a channel.

Only extract videos that can change a BridgeWorks offer, workflow, pitch, audit, automation, or content asset.

## Channel Categories

Track channels in five groups:

1. AI agency operators
2. B2B sales and outbound operators
3. Automation and no-code builders
4. SEO, GEO, and AI visibility practitioners
5. Service business marketing channels
6. Website design, CRO, and landing-page practitioners
7. Client delivery, project management, and agency operations
8. Reporting, analytics, and dashboard builders
9. Proposal, pricing, and packaging experts
10. Founder productivity and solo-operator systems

## Scout Output

Every channel scout must produce:

```text
## Channel: [Channel Name]

What this creator covers:
- [1-2 sentences]

Videos worth extracting:
1. [Video title] - [URL] - [Why BridgeWorks should extract it]

Videos to skip:
- [Category and why]

Channel-level insight:
- [1-2 sentences]
```

## Extraction Decision

Move a video to the extraction queue only if it can produce one of these:

- New BridgeWorks offer angle
- Better outreach message
- Better audit preview structure
- Better client delivery process
- Better pricing or packaging idea
- Better automation workflow
- Better fulfillment method for a BridgeWorks service
- Better onboarding or handover process
- Better weekly/monthly client report
- Better website build standard
- Better GEO/SEO/schema workflow
- Better AI automation architecture
- Better proposal or sales asset
- Better client communication pattern
- Better internal SOP
- LinkedIn post or proof content
- Prospecting niche insight

## Weekly Workflow

Every week:

1. Scout 5 channels.
2. Select up to 10 videos worth extracting.
3. Pick the top 3.
4. Extract only those top 3.
5. Convert each extraction into one BridgeWorks action.

## Output Destination

Use these files:

- `channels.csv`: channels to scout.
- `scout-results.md`: channel scout outputs.
- `extraction-queue.csv`: videos approved for deeper extraction.
- `actions-from-youtube.md`: decisions, offers, content, or workflows created from YouTube intelligence.
- `service-learning-map.md`: what BridgeWorks needs to learn to fulfill each service better.
- `transcript-extractions/`: extracted transcript intelligence.
- `adoption-decisions.md`: what BridgeWorks will adopt, adapt, or reject.

## Approval Rule

The automation can scout and queue videos.

It should not spend time extracting long videos unless Emmanuel approves the extraction queue or the video is already marked `Approved`.

## Learning Pillars

BridgeWorks should use YouTube scouting to improve these operating areas:

### 1. Sales And Prospecting

- Outbound systems
- Cold email quality
- Follow-up systems
- Sales calls
- Objection handling
- Proposal strategy

### 2. AI Growth Systems

- Lead capture
- Lead scoring
- Speed-to-lead
- CRM routing
- Follow-up automation
- n8n and Make workflows
- AI agent workflows

### 3. Content And Visibility Systems

- LinkedIn systems
- Newsletter systems
- Content repurposing
- GEO and AI search
- SEO foundations
- Schema and structured proof

### 4. Digital Infrastructure

- Website strategy
- Landing pages
- CRO
- Analytics and tracking
- Technical SEO
- Hosting and handover

### 5. Client Delivery

- Onboarding
- Discovery
- Weekly reporting
- Monthly reporting
- Client communication
- Risk management
- Handover

### 6. Agency Operations

- Solo founder systems
- SOPs
- Dashboards
- Financial operations
- Capacity planning
- Tool stack decisions

### 7. Proof And Authority

- Case studies
- Before and after assets
- Audit previews
- LinkedIn proof posts
- Website proof sections

## Extraction Output Rule

Every extracted video must become at least one of:

- SOP update
- Outreach update
- Offer update
- Audit-preview update
- Client-delivery checklist
- Website/landing-page standard
- Automation workflow idea
- Content draft
- Proposal improvement
- Tool decision

If it only produces "interesting notes", it should not be extracted.

## Transcript Extraction Format

Save each approved extraction as:

```text
pipeline/youtube-scout/transcript-extractions/[channel-slug]-[video-slug]-[YYYY-MM-DD].md
```

Use this format:

```text
# YouTube Intelligence Extraction: [Video Title]

Channel:
URL:
Date extracted:
Transcript source: YouTube transcript / captions / show notes / metadata only
BridgeWorks pillar:
Extraction score:

## Core Thesis

## Frameworks

| Framework | Adopt / Adapt / Reject | BridgeWorks Use |
|---|---|---|

## Tools Mentioned

| Tool | Use Case | BridgeWorks Decision |
|---|---|---|

## Systems And Processes

## Service Fulfillment Lessons

## Sales / Positioning Angles

## Audit Preview Improvements

## SOP Updates Needed

## Content Or Proof Angles

## Final Decision
Adopt / Adapt / Reject

## Next Action
```
