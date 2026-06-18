# YouTube Intelligence Extraction: Turn 1 Blog Post Into 3 Posts Automatically

Channel: MLTut  
URL: https://www.youtube.com/watch?v=0mI42jCF9Mw  
Date extracted: 2026-06-18  
Transcript source: YouTube transcript  
BridgeWorks pillar: Content And Visibility Systems  
Extraction score: 17/20

## Core Thesis

Content repurposing works better when each platform gets its own prompt and draft destination. A single generic rewrite prompt makes every channel sound the same.

## Frameworks

| Framework | Adopt / Adapt / Reject | BridgeWorks Use |
|---|---|---|
| One URL to three draft formats | Adopt | Use for BridgeWorks and client content from long-form reports |
| Separate AI node per platform | Adopt | Create LinkedIn, X, and newsletter prompts separately |
| Text-length quality gate | Adopt | Do not repurpose weak/short source material |
| Human review layer before publishing | Adopt | Must stay draft-only without Emmanuel/client approval |
| Separate publishing workflow | Park | Useful later. Do not automate publishing yet |

## Tools Mentioned

| Tool | Use Case | BridgeWorks Decision |
|---|---|---|
| n8n | Workflow orchestration | Adapt |
| Form trigger | URL input | Adopt |
| HTTP request | Fetch article HTML | Adopt if source allows |
| HTML extract | Pull article body | Adopt with selector testing |
| IF node | Catch failed scrapes under 200 chars | Adopt |
| Gemini 2.5 Flash | Draft generation | Adapt |
| Notion | Review database | Adapt to Command Center or Notion |

## Systems And Processes

1. Form accepts blog URL.
2. HTTP node fetches raw HTML.
3. HTML extract pulls article body.
4. IF node checks whether extracted text exceeds 200 characters.
5. Three Gemini nodes create platform-native drafts.
6. Three Notion nodes save drafts with platform/content/status.
7. Human approves or edits.
8. Optional second workflow publishes only approved items.

## Service Fulfillment Lessons

This is a strong BridgeWorks fulfillment asset because it turns existing evidence into content. It avoids asking the client for new ideas every week.

## Sales / Positioning Angles

- "One source asset becomes three review-ready drafts."
- "No autopublishing. You approve before anything goes live."
- "Your audit/report/blog becomes a week of content."

## Audit Preview Improvements

When auditing a client content system, ask:

> Does every long-form asset become platform-native posts, or does it die after publication?

## SOP Updates Needed

Create an `Article-to-3-Drafts Pipeline` SOP with platform prompts, minimum source length, review statuses, and approval rules.

## Content Or Proof Angles

- LinkedIn proof post from CEEFM case study.
- BridgeWorks mini-demo: turn one marketing audit section into LinkedIn, X, and newsletter drafts.

## Evidence

- `[03:17] Most people add one AI note with a prompt like rewrite this for LinkedIn X and a newsletter`
- `[03:30] LinkedIn rewards insight and a little vulnerability`
- `[03:40] X rewards compression and a killer first line`
- `[03:48] A newsletter intro rewards warmth and a first person voice`
- `[04:03] So we are using three separate Gemini nodes each with its own system prompt`
- `[07:06] The right answer is a review layer`
- `[08:26] don't run this on short content`

## Final Decision

Adopt internally. Adapt for clients.

## Next Action

Draft the automation spec and prompt library entry. Do not build/publish until Emmanuel approves the exact workflow.
