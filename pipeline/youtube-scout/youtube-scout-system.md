# BridgeWorks YouTube Intelligence And Adoption System

Version: 2.0  
Created: 2026-05-17  
Updated: 2026-06-05  
Owner: Emmanuel Ehigbai

## Purpose

Use YouTube as a daily business-intelligence radar and weekly adoption engine
for BridgeWorks.

The goal is not to watch more videos.

The goal is to find what BridgeWorks should adopt, adapt, reject, park, or
review to improve:

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

## Operating Principle

Metadata can discover candidates.

Transcript-read extraction is required before any adoption or adaptation
recommendation.

Do not recommend that BridgeWorks adopt or adapt content from a video unless a
transcript or captions were fetched and read. If transcript fetching fails, keep
the item in the queue as `Needs transcript` or `Needs review`.

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

## Daily And Weekly Rhythm

The system has three operating layers.

### Daily Radar

Use channel metadata, recent uploads, titles, and descriptions.

Output:

- Videos worth extracting
- Why they matter
- BridgeWorks pillar affected
- Extraction score
- Approval needed

Daily radar may queue videos, but it does not create adoption decisions unless
the transcript has already been read.

### Transcript Extraction

Use transcript or captions where available.

If transcript is unavailable, use:

- Description
- Chapters
- Public article/show notes
- Manual summary from available video metadata

Do not pretend a transcript was read if it was not.

Metadata-only extraction can support a `Review` or `Park` decision. It cannot
support `Adopt` or `Adapt`.

### Weekly Adoption Brief

On Mondays, summarize the latest transcript-read intelligence into:

- Top 3 adopt now
- Top 3 adapt next
- Items to reject or park
- Items needing transcript or Emmanuel review
- Service areas affected
- Single-command options for Emmanuel

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

## Adopt / Adapt / Reject / Park / Review Rule

Every extracted idea must be labeled:

- `Adopt`: Use as-is because it fits BridgeWorks now.
- `Adapt`: Modify for BridgeWorks context, market, or solo-founder capacity.
- `Reject`: Interesting but not useful, too complex, too expensive, off-brand, or wrong timing.
- `Park`: Useful later, but not relevant this week or this month.
- `Review`: Emmanuel should inspect before deciding.

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

## Daily Workflow

Every weekday:

1. Scout a bounded set of active and A-priority channels or topic searches.
2. Add only high-value candidates to `extraction-queue.csv`.
3. Use statuses: `Needs approval`, `Needs transcript`, `Approved`,
   `Extracted`, `Rejected`, `Parked`, `Edited`.
4. Keep output short: new candidates, why they matter, and the next approval
   command.

## Weekly Workflow

Every week:

1. Review the last 7 days of candidates and extracted videos.
2. Extract only approved videos with transcript access.
3. Produce the weekly adoption brief.
4. Convert approved extracted insights into one BridgeWorks action each.
5. Route decisions into `adoption-decisions.md`, `actions-from-youtube.md`, and
   the Daily Approval Brief.

## Command Grammar

Emmanuel should be able to respond with one short command:

```text
approve youtube [item_id]
reject youtube [item_id]
review youtube [item_id]
park youtube [item_id]
edit youtube [item_id] into SOP
edit youtube [item_id] into skill draft
edit youtube [item_id] into script proposal
edit youtube [item_id] into client checklist
edit youtube [item_id] into offer update
handoff youtube [item_id] to codex
handoff youtube [item_id] to claude code
handoff youtube [item_id] to cowork
handoff youtube [item_id] to claude project
handoff youtube [item_id] to gemini
```

Meanings:

- `approve`: extraction or implementation may proceed within the stated scope.
- `reject`: mark rejected and do not resurface unless Emmanuel asks.
- `review`: summarize source, transcript status, score, and proposed action.
- `park`: keep for later and do not action this week.
- `edit`: convert a transcript-read idea into the requested operational
  artifact, then mark it `Needs final approval`.
- `handoff`: convert the item into a tool-specific handoff for the named tool.

## Cross-Tool Routing

Every weekly adoption brief should include the best owner for each item.

Use this routing:

| Tool | Use for |
|---|---|
| Codex | Durable system updates, Command Center writes, automation updates, local docs, repo state checks, source registry updates |
| Claude Code | Repo-local builds, skills, scripts, tests, frontend/backend code, implementation in `bridgeworks-workspace`, `bridgeworks-ops`, DGE, or site repos |
| Cowork | Gmail, Calendar, Drive, Canva, connected data triage, Gmail drafts, file creation, browser/connector operations |
| Claude Project | Strategy, synthesis, long-form writing, offer thinking, positioning, narrative, decision framing |
| Gemini | Multimodal research across text, video, images, Drive/Docs/Sheets, NotebookLM-style source grounding, fact-checking, second-pass analysis, and long-context comparison |

Output handoffs in this shape:

```text
YOUTUBE HANDOFF
Item ID:
Source video:
Transcript status:
Decision: Adopt / Adapt / Reject / Park / Review
Target tool: Codex / Claude Code / Cowork / Claude Project / Gemini
Why this tool:
BridgeWorks area:
Operational output:
Files or systems involved:
Approval needed:
Do not do:
```

Rules:

- Claude Code handoffs must include exact repo/folder and expected files.
- Cowork handoffs must state connector actions and approval gates.
- Codex handoffs must state what durable registry, doc, automation, or Command
  Center location changes.
- Claude Project handoffs must preserve uncertainty and request synthesis, not
  external actions.
- Gemini handoffs must name the source set to inspect: Google files, folders,
  tabs, videos, images, screenshots, PDFs, or research questions. Ask for
  evidence-backed findings, source-grounded synthesis, comparison, or
  NotebookLM-style briefing, not implementation.

## Emmanuel OS Feed

The YouTube Intelligence And Adoption Engine feeds the Emmanuel OS Command
Center first. Local files are working memory and evidence, not the cockpit.

Primary Command Center destinations:

| Command Center tab | Purpose |
|---|---|
| `LLM Daily Outbox` | Mobile-readable daily radar and Monday weekly adoption brief |
| `Approval Queue` | Items Emmanuel can approve, reject, review, park, or edit from mobile |
| `Today` | Highest-priority YouTube action if it affects today's work |
| `Daily Brief` | Short summary when the daily/weekly brief is composed |
| `LLM Intake Log` | Source/handoff record for meaningful video intelligence |
| `Agent Registry` | New or changed agent/routine ideas that need tracking |
| `Agent Runbooks` | Adopted SOP/runbook changes or proposed routine cards |
| `Brand Assets` | Brand rules, visual standards, and reusable asset references affected by extracted intelligence |
| `Context Packets` | Portable knowledge packets for important source docs, SOPs, and cross-tool context |
| `Prompt Library` | Reusable prompts or command patterns created from extracted workflows |
| `Asset Factory` | Tangible asset requests created from YouTube intelligence |

Local working destinations:

| Destination | Purpose |
|---|---|
| `extraction-queue.csv` | Candidate videos and approval state |
| `transcript-extractions/` | Transcript-read intelligence files |
| `adoption-decisions.md` | Adopt/adapt/reject/park/review decisions that change BridgeWorks |
| `actions-from-youtube.md` | Operational actions created from YouTube intelligence |

Command Center row shape:

```text
YOUTUBE INTELLIGENCE ITEM
Item ID:
Date:
Source video:
Transcript status:
Decision state: Needs approval / Approved / Rejected / Parked / Review / Edited
Recommended action:
Owner tool:
BridgeWorks area:
Mobile command:
Evidence link/path:
Approval needed:
```

Portable knowledge rule:

If an extraction changes an SOP, brand rule, reusable prompt, service standard,
or source document, the local file is not enough. Create or update the matching
Command Center surface so Emmanuel can carry the knowledge on mobile:

- SOP or routine -> `Agent Runbooks`
- agent/routine identity -> `Agent Registry`
- brand/visual/copy rule -> `Brand Assets`
- reusable prompt/command -> `Prompt Library`
- source-doc summary or portable context -> `Context Packets`
- tangible output request -> `Asset Factory`
- approval/action needed -> `Approval Queue`
- mobile brief -> `LLM Daily Outbox`

Asset commands:

```text
create asset from [item_id]
create SOP from [item_id]
create checklist from [item_id]
create prompt from [item_id]
create canva brief from [item_id]
create client worksheet from [item_id]
create proposal section from [item_id]
create report section from [item_id]
create script proposal from [item_id]
create dashboard spec from [item_id]
create automation spec from [item_id]
create website brief from [item_id]
```

Mobile rule:

Every item that needs Emmanuel should include one exact mobile command, such as:

```text
approve youtube YT-20260605-001
review youtube YT-20260605-001
handoff youtube YT-20260605-001 to claude code
```

The weekly brief should also produce cross-tool handoffs when useful:

- Codex handoff for durable system updates.
- Claude Code handoff for implementation.
- Cowork handoff for connected-tool execution.
- Claude Project handoff for strategy and writing.
- Gemini handoff for multimodal research, source-grounded synthesis, and
  NotebookLM-style briefings.

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
