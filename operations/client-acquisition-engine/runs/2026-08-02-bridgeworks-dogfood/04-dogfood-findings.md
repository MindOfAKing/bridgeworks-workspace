# BridgeWorks Dogfood Findings

## Verdict

The orchestration logic works as a decision system, but it is not yet the operating system.

It successfully prevented three bad moves:

1. running all five audits because BridgeWorks has five service routes;
2. treating more prospect volume as the answer;
3. automating outbound before a stable manual control loop exists.

It routed BridgeWorks to `execution-operating-systems`, selected Emmanuel as the consequence owner, and produced one bounded prospect-to-proof control loop.

## What the test exposed

| Layer | Observed state | Gap | Decision |
|---|---|---|---|
| Public promise | BridgeWorks sells qualification, follow-up, visibility, workflow, and owned systems | The public promise is broader than the currently governed acquisition loop | Make BridgeWorks itself the first implemented case |
| Intake | Website submissions can reach Sheets and HubSpot contacts | Storage does not equal qualification, routing, task ownership, or commercial progression | Insert qualifier and router after capture |
| Free value | Website decision offers a free GEO audit to inbound and outbound prospects | This conflicts with qualification-earned bespoke work and biases every need toward GEO | Gate the asset type after qualification |
| CRM | Latest internal snapshot shows many companies and contacts but zero deals and weak lead-status completeness | Paying-customer, stage, market, trigger, and discourse learning cannot be trusted from the CRM alone | Reauthorize, reconcile, then use HubSpot as commercial truth |
| Execution | ClickUp is healthy and contains five tasks | It contains tests and one live prospect, not a repeatable campaign operating queue | Add pilot tasks only after qualification |
| Channel execution | Gmail is draftable; LinkedIn direct actions are not exposed through the connector | Prepared outreach can be mistaken for executed outreach | Preserve exact approval and execution evidence |
| Measurement | Market radar and sales logic are documented | No closed loop yet feeds replies, objections, value cited, and revenue back into market choice | Run one weekly evidence review |

## Capability test results

| Capability | Result |
|---|---|
| Lead qualifier | Passed. BridgeWorks scored 100 and met `discovery-ready` through explicit founder demand and verified operating evidence. |
| Prospect router | Passed. One primary route, buyer, question, and asset were selected. |
| Revenue-system scan | Passed. The artifact uses one hypothesis, exactly three actions, one narrow future state, and explicit evidence limits. |
| GEO scan | Correctly not invoked. Visibility is not the primary operating constraint in this run. |
| AI workflow scan | Correctly not invoked. Automation is a secondary implementation hypothesis, not the first diagnosis. |
| HubSpot | Read object access exists, but the user identity request returned reauthorization guidance and writes remain blocked. No further HubSpot action was taken. |
| ClickUp | Passed live read. The canonical list is writable, has five tasks, and no BridgeWorks dogfood task existed at inspection time. |
| PDF | Passed. The 584-word source rendered to three branded pages; text extraction confirmed the label, scope boundary, three-action section, and footer; all pages passed visual inspection. |

## Execution created

Three ClickUp tasks were created in the canonical `Pipeline & Partnerships` list:

1. [Approve prospect-to-proof diagnosis](https://app.clickup.com/t/869ecpwux)
2. [Run five-account manual control-loop pilot](https://app.clickup.com/t/869ecpwuy)
3. [Review pilot evidence before automation](https://app.clickup.com/t/869ecpwuz)

The existing [HubSpot reauthorization task](https://app.clickup.com/t/869ecm61y) was reused. No duplicate task was created.

## Product correction

The sellable capability should not be “a 16-page audit.” It should be:

> We identify the buyer event, qualify the account, select the one commercial constraint worth solving, produce a useful proof artifact, and connect the next action to the client’s operating systems.

The audit is evidence. The product is the decision and implemented control loop.
