# YouTube Extraction - Draft-Only Design To Code Loop

Date: 2026-06-29  
Source: `Claude Design 2.0 Just Changed Everything...`  
URL: https://www.youtube.com/watch?v=58CQM6I6DZg  
Transcript: `pipeline/youtube-scout/runtime-transcripts/58CQM6I6DZg.txt`  
Decision: Adapt with constraints  
BridgeWorks area: Foundation website prototypes, brand assets, client review drafts, website production system

## Core extraction

Claude Design can be useful as a draft surface between brand context and code.

The practical pattern is:

1. Give the design tool a brand source, visual reference, repo, or website context.
2. Generate a rough deck, website direction, animation, or design concept.
3. Edit directly on the canvas to avoid wasting credits on tiny changes.
4. Export to PowerPoint, PDF, HTML, or zip depending on the next step.
5. Move the result into Claude Code / Codex only after the concept is good enough.
6. Use the downloaded zip when direct handoff is unreliable.

## Evidence

- 00:46 to 01:28: the update focuses on better credits, design systems, two-way design, and canvas edits.
- 02:21 to 02:56: projects can use a design system, templates, brand context, GitHub repos, Figma files, images, and exports to PowerPoint, PDF, Miro, or Figma.
- 05:20 to 05:46: direct canvas edits avoid sending tiny change requests through the whole context window.
- 05:56 to 06:09: exports include standalone HTML and PowerPoint.
- 06:58 to 08:17: connector use can extract a brand identity from a website, but this depends on tools such as Firecrawl.
- 09:16 to 10:35: a design can move back to code when it needs database work, a real webpage, or fuller implementation.
- 10:45 to 11:31: direct integration can be unreliable. Downloading the zip and using the actual files is the safer handoff.
- 12:02 to 13:47: Open Design can run locally and use different models, but that is a repo/tool adoption decision.

## BridgeWorks adaptation

Use this as a draft-only client-review pattern, not a platform switch.

Possible BridgeWorks use:

- Create quick visual directions for Foundation homepage sections.
- Turn an existing client site into a simple brand direction board.
- Produce a rough PDF or HTML mockup for internal review.
- Hand the approved direction to Codex / Claude Code for static-first Vercel work.
- Keep `design.md` as the source of truth before generation.

## Guardrails

- No paid Firecrawl, Higgsfield, OpenRouter, GLM, or other API spend without approval.
- No installing unknown repos without explicit task approval and review.
- No client-facing mockup without Emmanuel approval.
- No switch away from static-first Foundation delivery unless scope and budget justify it.
- Treat generated designs as draft assets, not approved client work.

## One BridgeWorks action

Add a `Draft-Only Design To Code Loop` note to the Website Production System backlog, linked to the existing `design.md` action.
