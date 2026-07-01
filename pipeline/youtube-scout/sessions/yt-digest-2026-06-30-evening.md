# YouTube Intelligence Digest - 2026-06-30 Evening

## Candidates checked

- YouTube Data API connector: configured script still blocked with HTTP 403 Forbidden.
- RSS fallback: 12 recent watchlist candidates, 0 RSS errors.
- Web fallback: checked current YouTube search results for AI automation, Claude Code / agent workflows, AI visibility / GEO, and local business website conversion.
- Transcripts fetched: 5.
- Extracted: 3 highest-fit videos.
- Parked after transcript: Jack Roberts Hermes + MiniMax clip because transcript was only 611 characters and duplicated model-routing guidance. Build Great Products AI-slop app clip because it reinforced the existing problem-before-polish gate but did not add a new system.

## Top insights

### 1. AI design should start with a reusable brand system

Source: `Claude Just Got An Insane Update, And This Is The Only Tutorial You Need (Free)`  
Fit: High for Foundation website production, BridgeWorks assets, client review drafts, and content repurposing.

Evidence:

- 10:17 to 10:36: design system means brand colors, fonts, spacing, buttons, cards, and components.
- 12:13 to 12:41: one prompt can convert a whole deck to the saved design system.
- 13:19 to 14:00: one source can become an infographic and carousel.
- 15:42 to 18:05: wireframe or prototype can be handed to code.
- 18:31 to 18:53: sending the design system to Claude Code avoids repeated brand explanation and token waste.
- 19:27 to 20:20: design systems can be exported to another tool, but fidelity may shift.

BridgeWorks fit: Add a `Design System Export Gate`. No Claude Design upgrade, Open Design install, GitHub setup, Higgsfield connector, client data upload, or publishing from this run.

### 2. "AI employee" is useful only as a scoped leak map

Source: `NEW AI → CLONE This Once → Sell AI Employees For 299/mo`  
Fit: High for AI Growth Systems, Foundation offer, audit previews, and local SME diagnostics.

Evidence:

- 01:49 to 02:58: target no-website local businesses, give a free site, then sell a $300/month AI upgrade.
- 04:49 to 05:03: auto-build a basic personalized demo website.
- 06:21 to 07:20: bundle includes website, chat widget, voice AI, missed-call text-back, booking, review automation, pipeline, follow-up, and inbox.
- 07:37 to 08:11: missed-call handling keeps leads from calling the next competitor.
- 08:12 to 08:24: review automation should prompt real customers, not create fake reviews.
- 08:57 to 09:25: unified inbox reduces lost messages across channels.

BridgeWorks fit: Adapt into a `Guarded AI Employee Scope Filter`. Reject default free-website outreach. No client contact, CRM access, SMS, WhatsApp, email, phone, review, payment, vendor setup, or SaaS commitment from this run.

### 3. Know what not to automate before building workflows

Source: `Don't Fall For This AI Trap`  
Fit: High for automation audits, client delivery, and avoiding tool-sprawl.

Evidence:

- 00:00 to 00:08: power users know what not to automate.
- 00:08 to 00:17: ask how the task should be automated, not merely whether AI can automate it.
- 00:19 to 00:31: check if the task is text/image based, nuanced, artistic, edge-case-heavy, or unclear.
- 00:34 to 00:55: AI thumbnails looked impressive but took trial and error and did not beat a human designer for that use case.

BridgeWorks fit: Add an `Automation Fit Filter` before n8n, AI agents, CRM, SMS, email, creative, or reporting automation recommendations.

## Actions created

1. Add `Design System Export Gate` to website production and Asset Factory backlog.
2. Add `Guarded AI Employee Scope Filter` to audit-preview backlog.
3. Add `Automation Fit Filter` to AI Growth Systems and delivery-verification backlog.

## Files created or updated

- Updated `pipeline/youtube-scout/latest-candidates-2026-06-30-rss.json` via RSS fallback.
- Created `pipeline/youtube-scout/latest-candidates-2026-06-30-evening-web.json`.
- Created runtime transcripts for `6jlYiUQc2eA`, `fUoG63VqCAA`, `9WY0mco6Vkc`, `qxb5jIPCAgE`, and `BF7ohr7OJcE`.
- Created `pipeline/youtube-scout/transcript-extractions/yt-20260630-004-design-system-export-gate.md`.
- Created `pipeline/youtube-scout/transcript-extractions/yt-20260630-005-guarded-ai-employee-scope-filter.md`.
- Created `pipeline/youtube-scout/transcript-extractions/yt-20260630-006-automation-fit-filter.md`.
- Updated `pipeline/youtube-scout/adoption-decisions.md`.
- Updated `pipeline/youtube-scout/actions-from-youtube.md`.
- Updated `03-automation-layer/codex-active-work.md`.

## Blockers

- The configured YouTube Data API script still returns HTTP 403 Forbidden. RSS and web fallback worked.
- No Command Center Google Sheet update was made from this run.
- No Gmail draft was created.
- No outreach, publishing, paid API usage, paid tool adoption, client contact, commit, or push was performed.

## Next action

Create the `Automation Fit Filter` first. It protects the Foundation offer, AI Growth Systems, and audit previews from recommending automation before the task is clear, repeated, safe, and measurable.
