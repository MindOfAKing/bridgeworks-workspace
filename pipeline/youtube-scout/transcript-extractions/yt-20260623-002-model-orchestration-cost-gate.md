# YouTube Extraction: Model Orchestration Cost Gate

Date: 2026-06-23
Source: Nate Herk - `I Battle Tested Sakana Fugu's Fable Killer`
URL: https://www.youtube.com/watch?v=GpSqBjW6hR4
Decision: Reject for now / Watch
BridgeWorks area: Local AI Ops, Agency Operations, Delivery Verification

## Source-grounded evidence

- `[01:13] It is a multi-agent system delivered as one model.`
- `[01:40] each AI does one thing really well, one very specific thing, and that is how you achieve great results by chaining those outputs into the next.`
- `[05:40] what is that at the cost of? Typically speed and actual money`
- `[07:04] 36 of the 38 tasks end in a tie.`
- `[07:07] Fugu being 4.5 times slower overall and five times more expensive.`
- `[10:03] Opus only cost us about 10 bucks, whereas Fugu costed me 50 bucks.`
- `[10:53] Not locking yourself into one provider`
- `[11:00] cheapest model that I can use for this task that doesn't sacrifice quality.`

## Practical framework

Use orchestration only when the task earns the cost:

1. Is the task high-stakes enough to need multiple model perspectives?
2. Can cheaper routing solve it first?
3. Does the orchestrator improve result quality, not just novelty?
4. Does it save operator time after slower response time is counted?
5. Is there a budget cap?
6. Is there proof from tests, not vendor claims?

## BridgeWorks fit

High as a decision guardrail. Low as a tool adoption. Emmanuel's stack already has Claude, Codex, Gemini, and Hermes. The value is deliberate routing, not another paid API layer.

## Adoption note

Do not buy or integrate Fugu / similar orchestration APIs yet. Use this as a model-routing cost gate for local AI ops and client delivery.

## Next experiment

Add a lightweight routing note to AI delivery SOPs:

- Claude / Codex for build work.
- Gemini or web extraction for broad fact checks.
- Second-model review only for client-facing or risky outputs.
- Paid orchestration only after a measured quality or time gain.
