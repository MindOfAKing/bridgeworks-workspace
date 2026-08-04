# BridgeWorks Dogfood Execution Handoff

## Current state

- Qualification: `discovery-ready`, 100/100, eight verified signals.
- Primary route: `execution-operating-systems`.
- Buyer: Emmanuel Ehigbai, Founder and Principal.
- Asset: BridgeWorks Prospect-to-Proof Control Loop.
- External actions: none.

## HubSpot

The live capability check on 2 August 2026 shows Company, Contact, and Deal reads as available. The requested user identity could not be returned, and Company, Contact, Deal, Note, Task, Email, Call, and Meeting writes require reauthorization.

Under the HubSpot guidance, no further HubSpot search or write was attempted.

BridgeWorks should not be created as a prospect or deal in its own CRM. After reauthorization, the implementation task is to reconcile existing fields and records around:

- current buyer event;
- evidence date and source;
- qualification status and score;
- primary service route;
- proof asset and approval state;
- current commercial stage;
- touch and response evidence;
- disqualification reason;
- next action and date;
- market, trigger, offer, and channel learning.

## ClickUp

The canonical list is `Sales & Partnerships > Pipeline & Partnerships`.

Live inspection found five tasks, all open. Existing work includes three Appinio tasks, one internal route test, and one ICP-definition task. No BridgeWorks dogfood implementation task existed at inspection time.

The minimum internal tasks now exist:

1. [Approve or revise the dogfood diagnosis](https://app.clickup.com/t/869ecpwux)
2. [Reauthorize and reconcile HubSpot](https://app.clickup.com/t/869ecm61y), reused from the existing system task
3. [Run a five-account manual pilot](https://app.clickup.com/t/869ecpwuy)
4. [Review pilot evidence before automation](https://app.clickup.com/t/869ecpwuz)

## Production boundary

Do not yet:

- modify the production website intake;
- activate an n8n or Composio outbound workflow;
- replace or expand the HubSpot pipeline;
- create automated email or LinkedIn sequences;
- produce five audit assets per account;
- create another prospect database.

## Pilot acceptance record

For each of five accounts, record:

| Field | Required evidence |
|---|---|
| Buyer event | Public or user-provided source and date |
| Buyer | Accountable role and reachable route |
| Qualification | Status, score, signal count, unknowns |
| Route | One primary service route |
| Asset | One question, one proof, production minutes |
| Contact | Exact channel, approval, timestamp |
| Outcome | Reply, no reply, objection, permission, meeting, nurture, or reject |
| Learning | Market, trigger, offer, channel, and recommendation cited |

## Next decision

Approve or revise the diagnosis in ClickUp. HubSpot changes, production workflow implementation, and external outreach remain separate approval-gated actions.
