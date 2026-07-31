# YouTube Intelligence Digest - 2026-07-27 Cron Run

## Status

**Candidates checked:** New web search candidates from 2026-07-15 to today.  
**Transcripts fetched:** 0 (YouTube Transcript API AttributeError blocker, same as previous runs).  
**Last comprehensive digest:** 2026-07-15 evening, 12 days ago.  
**Actions backlog:** 28 actions from YouTube sources, 0 completed since June 25.

## Findings

### YouTube Landscape - New Candidates (2026-07-15 to 2026-07-27)

Three new high-fit candidates found via web search:

1. **Automate AI Consulting - "8 Claude Skills You Can Sell to Local Businesses (I Built All 8)"**  
   Channel: Automate AI Consulting  
   Published: 18 hours ago (2026-07-26)  
   URL: https://www.youtube.com/watch?v=0i_APvGWUA4  
   Fit: High for Foundation offer packaging and Claude skill bundling  
   Fit reason: Directly targets the skill-to-SME monetization angle BridgeWorks is building.
   Status: Transcript fetch unavailable due to API blocker.

2. **Ranking Academy - "5 AI Search Signals Winning Rankings in 2026"**  
   Channel: Ranking Academy  
   Published: 1 month ago (June 2026)  
   URL: https://www.youtube.com/watch?v=AF_p3QnDcNE  
   Duration: 8:12  
   Fit: Medium-high for AI Visibility Authority Signal Map methodology  
   Fit reason: Complements the July 15 extraction on GEO signals; adds local SME framing.  
   Status: Transcript fetch unavailable due to API blocker.

3. **AWeber - "How to Rank in AI Search in 2026 (For Small Business Owners)"**  
   Channel: AWeber  
   Published: 1 month ago (May 2026)  
   URL: https://www.youtube.com/watch?v=h1eK5vN6nX0  
   Duration: 4:04  
   Fit: Medium-high for AI Visibility beginner framing  
   Fit reason: Simple language for handyman/local SME persona; covers LLMs.txt and discovery basics.  
   Status: Transcript fetch unavailable due to API blocker.

### No Progress Since July 15

The previous digest identified 5 high-fit videos and created 5 extraction files:
- AI Tools Assessment Diagnostic (Greg Isenberg $1000/hr model)
- AI Human Work Queue Evals (Nick Saraev agentic workflow)
- Local AI Employee Scope Filter (Jason Wardrop risk guardrail)
- n8n Prospect Research Intake Guardrail (Tito Space intake gate)
- GEO Authority Signal Map (GEO Blueprint methodology)

None of these have been converted into BridgeWorks assets or adopted into adoption-decisions.md since the July 15 extraction.

### Blockers

**Transcript API:** YouTube Transcript API continues to return AttributeError when invoked via uv run Python environment. This has persisted for 12 days.
- Last successful transcript fetch: July 15, 2026.
- Root cause: Not diagnosticated; likely dependency version conflict or API credential issue.
- Workaround: Manual transcript extraction via YouTube's auto-generated captions is not automated in the current pipeline.

**No Asset Creation:** 0 of 28 YouTube-sourced actions have been converted into BridgeWorks templates, checklists, specs, or offer updates since June 25.

## Insight

The gap is not discovery. YouTube landscape for local SMEs, Claude Skills, and GEO is rich and aligned.

The gap is **decision execution**: Five high-fit extractions from July 15 remain actionable but unadopted. The next digest will repeat discovery if these five actions are not completed or explicitly rejected.

## Actions Created

1. **Fix or Replace Transcript Pipeline**  
   Owner: Emmanuel / Codex  
   Priority: Blocker for next digest run  
   Options:  
   - Debug uv Python environment vs. youtube-transcript-api version clash  
   - Fallback: Manual scraping of YouTube auto-captions where available  
   - Fallback: Use web-extract tool to fetch YouTube video pages and parse caption blocks  

2. **Move 5 July 15 Extractions Into Asset Creation**  
   Owner: Emmanuel  
   Priority: High  
   Actions:  
   - Pick one: AI Readiness Diagnostic or AI Work Queue Eval  
   - Create outline with templates and guardrails  
   - Validate against Foundation offer and Oliviks QA  
   - Decide: adopt, adapt, or reject, then close the action in adoption-decisions.md

## Files Created or Updated

- `pipeline/youtube-scout/latest-candidates-2026-07-27-web.json` (new, 3 candidates)
- `pipeline/youtube-scout/sessions/yt-digest-2026-07-27-cron.md` (this file, new)
- `03-automation-layer/codex-active-work.md` (appended July 27 entry)
- No transcript files (API blocker)
- No extraction files (no transcripts fetched)

## Next Actions

**Priority 1:** Fix or replace transcript pipeline (debug uv environment vs. youtube-transcript-api version clash, or use web-scrape fallback for YouTube captions).

**Priority 2:** Execute 1 of 5 July 15 actions into a live asset (e.g., AI Readiness Diagnostic outline or AI Work Queue Eval Card). Validate against Foundation offer and Oliviks QA, then close the action in adoption-decisions.md.

**Blocker note:** YouTube Data API HTTP 403 remains in place; no plans to purchase or escalate API access without Emmanuel approval.
