---
name: bridgeworks-ai-workflow-scan
description: Use when a qualified BridgeWorks prospect needs a 15-20 minute public-evidence diagnostic of one defensible AI-assisted workflow opportunity with a synthetic future-state demonstration and human approval point.
---

# BridgeWorks AI Workflow Scan

Identify one supportable workflow opportunity. Lead with responsiveness, consistency, capacity, or control, not "AI transformation."

## Entry Gate

Require:

- `audit-approved` or `discovery-ready`;
- `ai-workflow-automation` as the primary route;
- a recurring motion tied to prospect-specific public evidence;
- a plausible process owner and human reviewer.

If the gate fails, return to `bridgeworks-prospect-router`. An explicitly requested forward test may continue only as `internal-test-draft`.

## Timebox

1. Three minutes: confirm trigger, owner, qualification, and evidence.
2. Five minutes: capture up to six recent high-signal facts.
3. Three minutes: reconstruct the smallest plausible current-state sequence.
4. Three minutes: score and choose one candidate.
5. Four minutes: build a five-frame synthetic demonstration.
6. Two minutes: add caveats and QA.

Stop at 20 minutes.

## Evidence and Wording

Prioritize company pages, intake forms, public job descriptions, product documentation, cases, webinars, and leadership statements. Use third-party reviews and technology clues only as corroboration.

Label every material statement:

- `verified`: current, directly observed, URL and date recorded;
- `hypothesis`: an interpretation to test;
- `unknown`: requires internal evidence.

A buyer-facing asset requires a URL and observation/publication date for each verified signal, plus a named buyer or verified route to the accountable role. Otherwise label it `internal-test-draft` and block release.

Prefer evidence observed within 90 days for jobs and active operating signals, and within 12 months for leadership or strategy changes. Older evidence needs a current corroborating signal.

Job language is evidence of a declared responsibility, not proof of the current process. Technology detection does not prove active use, configuration, integration, adoption, or performance.

## Candidate Test

Score each factor `yes` (1), `partial` (0.5), or `no` (0):

| Factor | Question |
|---|---|
| Repetition | Does the task plausibly recur? |
| Information burden | Does it require reading, extracting, matching, classifying, summarizing, or drafting? |
| Handoff | Does information move between roles, forms, inboxes, documents, or tools? |
| Error/rework exposure | Could inconsistency or delay matter? |
| Human reviewability | Can a named person inspect the output cheaply? |
| Evidence strength | Is the need supported by prospect-specific public evidence? |

Choose one candidate only when the total is at least 4, with human reviewability and evidence strength both `yes`. Prefer deterministic rules or form redesign when they solve the problem more safely than AI.

Phrase the opportunity:

`When [observable trigger] happens, [role] may spend time on [specific information task or handoff]. A bounded workflow could produce [reviewable output], while [human owner] retains approval.`

## Demonstration

Use only public or synthetic data:

1. representative trigger arrives;
2. AI extracts, classifies, summarizes, or drafts;
3. deterministic rules route or structure the result;
4. named human reviews and approves;
5. structured output is shown.

Display:

> Illustrative future state. Not connected to company systems.

Do not scrape private data, bypass controls, impersonate people, expose personal information, or connect production systems.

For emergency, safety, legal, financial, health, or other high-impact categories, use deterministic escalation rules. AI may flag for urgent human review but must not downgrade, close, dispatch, diagnose, price, or decide the case.

## Output

Follow [references/one-page-template.md](references/one-page-template.md). Produce:

- `AI-WORKFLOW-SCAN-[company]-[date].md`;
- one synthetic demonstration as an annotated diagram, HTML mockup, or compact PDF;
- a branded PDF only when it helps the buyer understand the workflow.

Use active document/PDF workflows and inspect the output. Never use the broken `market-report-pdf`.
Keep the executive brief under 650 words. The synthetic demonstration may be a second page when a single physical page would harm legibility.

## Three Actions

Return exactly:

1. `Validate`: a 30-minute interview with the process owner and one frontline participant.
2. `Measure`: 10-20 historical cases or one week of baseline volume, wait, rework, error, and exception evidence.
3. `Pilot`: synthetic or historical cases with acceptance criteria, human approval, no production write, and a rollback path.

Adapt the objects and measures to the prospect. Do not invent baselines.
Define acceptance categories before the pilot: extraction completeness, classification accuracy, false escalation and missed escalation, routing correctness, draft quality, reviewer effort, and exception handling. Set numeric thresholds only after risk and baseline evidence are available.

## Stop and Paid Boundary

Stop when:

- no recurring workflow is tied to prospect-specific evidence;
- the claim depends on generic industry behavior;
- sensitive hiring, lending, diagnosis, legal judgment, surveillance, or other high-impact decisions lack a clear governance path;
- volume, cost, conversion, time saved, or error data would have to be invented;
- no human reviewer exists;
- the idea is merely "add a chatbot";
- the demo cannot be meaningful with public or synthetic inputs.

The free scan provides one evidence-backed hypothesis, one inspectable simulation, and three next actions. A paid audit begins with interviews, internal-system/data access, security/privacy/model-risk assessment, integration discovery, build-versus-buy analysis, ROI, roadmap, or live-data prototyping.

Never provide multiple automation ideas, a production app, autonomous workflow claims, vendor architecture, ROI, pricing, or proposal at initial contact.
