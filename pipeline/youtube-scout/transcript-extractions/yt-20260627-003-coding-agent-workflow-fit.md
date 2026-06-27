# YouTube Extraction: Coding Agent Selection By Workflow Fit

Date: 2026-06-27
Sources:
- Jan, `Cursor vs Claude Code vs Codex (I Built the Same App 3 Times)`, https://www.youtube.com/watch?v=OnCep-HlMzI
- ColdIQ-style GTM setup video from web fallback, https://www.youtube.com/watch?v=b9tygqQiBS8
URL: https://www.youtube.com/watch?v=OnCep-HlMzI and https://www.youtube.com/watch?v=b9tygqQiBS8
Decision: Adapt
BridgeWorks area: AI delivery verification, website production system, cost governance

## Core idea
The model is only one part of delivery. The agent workflow, review surface, preview reliability, diff quality, model flexibility, and proof loop decide whether a solo operator can ship safely.

## Evidence
- OnCep, 00:20 to 00:52: the test asks which tool is least annoying, easiest to control, best for review, and best fit for daily work. The agent is the car, the model is the engine.
- OnCep, 02:38 to 03:19: every build started with a high-quality PRD so the agent had a shared source of truth.
- OnCep, 10:27 to 11:00: Claude Code produced strong results, but the surrounding product experience created friction.
- OnCep, 20:39 to 21:05: Codex was polished and reliable, but may not fit every model preference or workflow.
- OnCep, 21:21 to 22:05: Cursor's editor-native workflow matters when code review and manual inspection are required.
- OnCep, 24:31 to 26:29: visual PRD canvas and model flexibility help planning, handoff, and task routing.
- b9ty, 01:45 to 02:02: mini tools can become lead magnets when users exchange an email for a useful result.
- b9ty, 04:02 to 04:31: API documentation and action discovery can now be delegated to the coding agent, but keys and connections still need safeguards.

## BridgeWorks fit
High as an internal operating rule. Do not chase a new paid coding stack. Use the lesson to improve tool selection and proof standards.

## Adoption rule
Before using any coding agent for BridgeWorks delivery, define:
1. PRD or task brief.
2. Review surface.
3. Verification method.
4. Cost cap.
5. Rollback path.
6. Which model/tool is used for planning, execution, and review.

## Action created
Add a Coding Agent Workflow Fit row to the AI Delivery Verification Checklist and Model Routing Trial Sheet.
