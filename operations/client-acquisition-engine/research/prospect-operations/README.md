# Prospect Research Operations

This folder is the durable handoff between the local Mission Control worker and the scheduled research agent.

## Weekday Flow

1. Mission Control prepares up to five active-lane prospects from the canonical 45-row tracker.
2. The scheduled research agent opens the JSON and Markdown batch in `batches/`.
3. The agent verifies public evidence and writes a structured JSON file to `results/`.
4. The agent runs the completion validator.
5. Mission Control prepares a review packet under `review/packets/`.
6. A verified identity without a specific, evidence-backed commercial gap returns to a bounded `gap_completion` research task.
7. Only an outreach-ready record creates an exact external-action task in `awaiting_approval`.
8. Mission Control reports the batch, evidence state, warnings, follow-up research, and approval queue.

## Outreach readiness

`verified` means the business identity and route were established. It does not by itself authorize outreach.

An outreach-ready result must also contain:

- one evidence-backed `commercial_gap`;
- a relevant `proof_to_use`, including an explicit decision to hold proof for follow-up;
- a supported channel and exact public destination;
- the exact proposed subject and 25-to-180-word body;
- the next internal action and any risk notes.

The valid readiness values are `ready`, `hold`, and `needs_more_evidence`. Ready items become approval tasks; they do not become sends.

## Boundaries

- Research and internal preparation may run unattended.
- Every current factual observation needs a source URL and access date.
- A Maps or directory omission is not proof that a business has no website.
- Paid enrichment is off by default.
- Gmail draft creation, sending, LinkedIn messaging, browser submission, publishing, proposal delivery, and mobile URL opening require explicit Emmanuel approval.
- Research results do not modify the canonical prospect CSV automatically. Reviewed findings are promoted separately.

## Commands

```powershell
python scripts/prospect_research_queue.py prepare --limit 5
python scripts/prospect_research_queue.py status
python scripts/prospect_research_queue.py complete --batch <batch.json> --results <results.json>
python scripts/prospect_review_queue.py validate-gap --results <results.json> --prospect-id <prospect-id>
python scripts/prospect_review_queue.py prepare --results <results.json> --summary-only
```

Repeated preparation on the same date reuses the open batch. A new batch is not created until the current one is completed or deliberately resolved.

Durable review state is stored in `review/prospect-review-state.json`; review events are appended to `review/prospect-review-events.jsonl`. External action approval remains in private Mission Control and is scoped to the exact destination and copy shown in the task.
