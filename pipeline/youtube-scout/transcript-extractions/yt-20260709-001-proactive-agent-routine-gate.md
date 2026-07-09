# YouTube Extraction: Proactive Agent Routine Gate

Source: `Build a proactive agent workflow with Claude Code`  
URL: https://www.youtube.com/watch?v=eSP7PLTXNy8  
Video ID: `eSP7PLTXNy8`  
Date extracted: 2026-07-09  
BridgeWorks pillar: Agency Operations, AI Growth Systems, Delivery Verification

## Useful Ideas

- Proactive agents should not depend on a laptop staying open.
- A routine is defined by prompt, repo, connectors, and trigger.
- Triggers can be time-based, GitHub event-based, or custom webhook-based.
- The session should be watchable, steerable, resumable, and bounded.
- A useful internal example is a weekly docs update routine that checks merged changes against documentation and opens a PR.

## Evidence

- 00:49 to 01:00: the topic is building a proactive agent workflow with Claude Code routines.
- 03:07 to 04:25: current proactive agents require hosting, persistence, auth, triggers, and human-in-loop management.
- 04:27 to 04:47: routines need a prompt, repos, connectors, and a trigger.
- 05:01 to 06:17: routines run on managed infrastructure, can be scheduled or event-triggered, and remain watchable and steerable.
- 07:48 to 08:07: weekly docs review can compare merged changes with documentation and create a PR.

## What This Changes For BridgeWorks

BridgeWorks already runs scheduled jobs. The useful adoption is not a new tool purchase. It is a routine design card for every scheduled or event-triggered AI job.

Each routine should state:

1. Trigger.
2. Source files.
3. Allowed tools.
4. Output file.
5. Human approval gate.
6. Verification proof.
7. Stop conditions.
8. What it must not do.

## Action To Take

Create a `Scheduled Routine Design Card` template for YouTube Digest, Inbound Prospect Triage, Oliviks QA, and future BridgeWorks automation jobs.

## SOP / Template Update

Add to Automation Layer backlog. Do not enable Claude Code routines, webhooks, GitHub PR creation, or connected-account actions without Emmanuel approval.

## Decision

Adapt.
