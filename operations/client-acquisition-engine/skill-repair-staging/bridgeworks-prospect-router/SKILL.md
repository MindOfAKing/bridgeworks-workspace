---
name: bridgeworks-prospect-router
description: Use when a BridgeWorks prospect has passed qualification and must be routed to one evidence-backed diagnostic or demo, the correct service line and work passes, a likely buyer, an outreach path, and CRM/task handoffs without overproducing.
---

# BridgeWorks Prospect Router

Turn an `audit-approved` or `discovery-ready` qualification record into the smallest valuable proof of work. The router chooses one commercial question and one primary route. It does not turn every visible weakness into a deliverable.

## Entry Gate

Require a record from `bridgeworks-lead-qualifier`.

- Continue only for `audit-approved` or `discovery-ready`.
- Send `research`, `nurture`, and `reject` records back unchanged.
- If the evidence cannot support one primary route, downgrade to `research`.

Read [references/capability-registry.md](references/capability-registry.md) before naming skills, agents, connectors, or channels. Do not invoke a capability marked `stranded`, `blocked`, or `unverified`.

## Routing Method

1. State the commercial question in one sentence.
2. Compare the five service routes using source-backed evidence.
3. Choose the route attached to the strongest combination of urgency, consequence, buyer ownership, and demonstrability.
4. Treat other routes as secondary hypotheses. Do not produce assets for them.
5. Choose one asset from the route table.
6. Limit production to the minimum work passes required for credible evidence.
7. Define buyer, channel sequence, system handoffs, approval gates, and stop conditions.
8. Run `scripts/validate_route.py <route.json>` for structured routing plans.

## Route Table

| Primary route | Lead with | Useful 15-20 minute asset | Avoid at initial contact |
|---|---|---|---|
| `strategy-transformation` | A dated strategic choice, expansion, acquisition, or execution conflict | Decision brief, expansion assumption map, priority-to-execution map | Full strategy, market-entry plan, proposal |
| `digital-platforms-brand` | A customer-journey or credibility problem with commercial consequence | Annotated conversion path, credibility review, before/after page concept | Full redesign, broad brand audit |
| `content-visibility-demand` | Demonstrable demand, discoverability, citability, or channel gap | Search/AI visibility gap, demand-capture map, three-page content opportunity | Generic content calendar, full SEO/GEO audit |
| `ai-workflow-automation` | Observable routing, repetitive work, tool fragmentation, or AI-readiness question | Workflow friction map, automation candidate matrix, bounded future-state demo | Claims about internal waste, production automation |
| `execution-operating-systems` | Ownership, CRM, reporting, handoff, integration, or governance signal | Lead-to-owner map, lifecycle/reporting gap scan, operating cadence diagram | Portal audit without access, migration architecture |

The best asset makes the prospect think, "They understood the consequence and showed the next state," not merely, "They found errors on my website."

## Work-Pass Budget

Use no more than four passes:

1. `evidence`: verify company, trigger, page or process observations, and buyer.
2. `specialist`: apply only the relevant service-line rubric.
3. `demonstration`: create one annotated map, mockup, comparison, or prioritized action view.
4. `executive-qa`: remove unsupported claims and connect evidence to outcome.

PDF rendering is packaging, not a fifth analytical pass. A polished PDF is justified only when the visual hierarchy improves comprehension.

## Buyer and Channel Logic

- Route to the executive who owns the consequence, not the person whose profile is easiest to find.
- A vacancy is evidence of intent; the unfilled role is not a contact.
- Use a warm introduction or relevant referral first when available.
- Email can carry the artifact. LinkedIn can establish familiarity and provide a second route.
- Do not automate LinkedIn DMs, connection requests, follows, or engagement unless the active capability registry confirms a compliant tool and Emmanuel approves execution.
- Do not send, publish, spend credits, create external records, or mutate production systems without the applicable approval.

## System Handoff

Prepare payloads, but preserve system ownership:

- HubSpot: account, contacts, qualification, service route, evidence summary, stage, touch history, next action.
- ClickUp: research, asset production, QA, approval, and follow-up tasks.
- Gmail: draft artifact email and follow-ups; sending remains approval-gated.
- LinkedIn: profile URLs, observation, engagement plan, connection note, and DM draft.
- Apollo: decision-maker enrichment only after qualification and credit approval.
- Google Maps: local discovery and evidence only when connected; never use locality as a quality proxy.

HubSpot is commercial truth. ClickUp is execution truth. Do not create a parallel CRM file as the operating source of truth.

## Output Contract

Return:

```yaml
company:
qualification_status:
primary_commercial_question:
primary_service_route:
secondary_hypotheses: []
route_evidence: []
asset:
  title:
  format:
  audience:
  content:
    - company-specific evidence
    - consequence or risk framed as a hypothesis
    - three prioritized recommended actions
    - one future-state demonstration
  production_ceiling_minutes: 20
work_passes: []
capabilities:
  active: []
  unavailable_or_deferred: []
buyer:
  primary:
  evidence:
  secondary:
channel_sequence: []
hubspot_payload: {}
clickup_tasks: []
approval_gates: []
stop_conditions: []
do_not_produce: []
next_action:
```

## Hard Stops

- One primary route, one asset, one primary buyer.
- No pricing, ROI claim, internal-system claim, or proposal without evidence.
- No full multi-discipline audit for first contact.
- No asset when the qualification gate failed.
- No connector named as active when the registry says otherwise.
- No external action disguised as preparation.
