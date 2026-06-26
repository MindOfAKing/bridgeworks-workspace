# Local Model Routing Economics

Date: 2026-06-24  
Source: Greg Isenberg - `GLM 5.2: Set Up Local AI with Cursor/Codex etc`  
URL: https://www.youtube.com/watch?v=xa-9O5cDm3c  
Status: Transcript fetched.  
Decision: Adopt as an internal cost-governance rule. Do not start paid OpenRouter, Z AI, or hardware experiments without Emmanuel approval.

## Source-grounded evidence

- `[01:23] kind of use compounding models or fusion models as as open router calls it to be able to do sequencing between a more extensive thinking model and a more execution-based model.`
- `[04:01] GLM 5.2 came out and essentially has a 1 million context window and it scores 81 points on the terminal bench 2.1.`
- `[06:01] if I feel like GLM 5.2 is strong in one part, but weak on the other, then I think about how do I actually use other tools or other models.`
- `[11:56] to get almost close to an Opus 4.8 level of output, it will cost us 44 cents. Whereas with Opus 4.8, it costs you $2.38.`
- `[15:19] GLM 5.2 doesn't support vision capabilities... I actually used Open 4.8 to import screenshots and explain back to me what it sees... then I switched to GLM 5.2.`
- `[18:53] can you help us figure out like how to build governance and proper education on how to actually use the right models?`
- `[20:04] no, you don't need a Mac Mini. You don't need this equipment. You can get started today.`
- `[21:43] You shouldn't be token maxing. You should be token minimizing as much as possible and output maxing instead.`

## Practical framework

**Model Routing Ladder:**

1. Define the task: vision, planning, coding, rewrite, QA, extraction, or formatting.
2. Use the cheapest competent route first.
3. Use premium models for ambiguity, visual reasoning, high-risk client deliverables, and final review.
4. Hand off execution to cheaper/local/open models only when the task is well-scoped.
5. Record cost, time, output quality, and failed retries.
6. Upgrade only when measured quality gain beats the extra cost.

## BridgeWorks fit

High fit for local AI ops and solo delivery economics. This extends the 2026-06-23 model-routing cost gate with a concrete pattern: premium model for seeing/planning, cheaper model for execution, premium or Codex review for verification.

It does not justify buying hardware now. The source explicitly says the starting point can be cloud routing through a credit-based provider, but BridgeWorks still needs approval before paid API usage.

## Next experiment

Create a no-spend `Model Routing Trial Sheet` using existing tools first:

- Task type
- Default model/tool
- Cheaper candidate
- Verification method
- Result quality
- Time saved or lost
- Cost if paid
- Decision: keep, reject, or retest

## Guardrails

- No paid OpenRouter/Z AI loop without approval.
- No hardware purchase recommendation from this video alone.
- Do not expose API keys in logs or screenshots.
- Do not route client/private data into new providers without explicit approval and privacy review.
