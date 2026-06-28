# YouTube Extraction — Context Ownership For Agent Work

Date: 2026-06-28  
Sources:  
- Vaibhav Sisinty, `Claude's New Update Is Scarier Than You Think (+18 AI Updates)`  
- Patrick Debois, `Context Is the New Code for AI Agents`  
URLs:  
- https://www.youtube.com/watch?v=65RvB3Xta0E  
- https://www.youtube.com/watch?v=Pz-vVV0Jmfc  
Transcript files:  
- `pipeline/youtube-scout/runtime-transcripts/65RvB3Xta0E.txt`  
- `pipeline/youtube-scout/runtime-transcripts/Pz-vVV0Jmfc.txt`  
Decision: Adapt  
BridgeWorks area: Agency Operations, AI Growth Systems, Delivery Verification, Knowledge Map

## Why it matters

Two separate videos point to the same operating rule: rent model intelligence, but own the context. This fits Emmanuel's solo AI build method and BridgeWorks' need for durable source-of-truth files.

## Evidence from transcript

Vaibhav roundup:

- 05:16 to 05:30: Claude in Slack can pull files, break jobs into steps, update docs, and post completion checklists.
- 05:45 to 06:31: access is channel-scoped, memory respects boundaries, and credential use is logged.
- 06:45 to 07:09: AI is shifting from app to coworker inside company memory and tools.
- 07:21 to 07:53: model swapping is easy, but company memory, workflows, and lessons are hard to move. Rent intelligence, own context.
- 18:07 to 18:49: Excel Copilot Skills show the same pattern for recurring monthly reports, but paid plan and rollout limits apply.

Patrick Debois talk:

- 02:46 to 03:16: if context is like code, it needs testing, linting, and evals.
- 05:35 to 06:19: context should be packaged, versioned, and distributed like libraries, not only copied around.
- 06:48 to 07:01: skills and context packages need security scanning before publishing.
- 07:20 to 08:05: agent logs reveal missing context and repeated manual additions.
- 11:48 to 12:12: retry count or agent hops can become a context-quality metric.
- 12:16 to 13:20: context drifts like technical debt and needs retrospectives.
- 13:52 to 14:16: context is the fuel for coding agents.

## BridgeWorks adaptation

Add a `Context Ownership Gate` before adopting AI coworker, skill, agent, or connector workflows:

1. Source-of-truth location: where the context lives locally.
2. Exportability: how to move it if a vendor changes.
3. Access boundary: what files, clients, and credentials it can see.
4. Verification: lint, checklist, or proof task before trusting it.
5. Drift control: monthly review of repeated agent mistakes.
6. Cost gate: free first, low-cost second, paid only after proof.
7. No client data in new tools unless explicitly approved.

## Reject or guardrail

- Do not move BridgeWorks memory into one vendor as the only copy.
- Do not install paid coworker or Copilot workflows from a roundup.
- Do not connect private client data to a new agent without approval.
- Do not treat AI-generated context as accurate without proof.

## Action

Fold `Context Ownership Gate` into the BridgeWorks Knowledge Map spec and Skill Adoption Gate.

Status: Needs SOP row.
