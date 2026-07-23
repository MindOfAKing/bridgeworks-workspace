# BridgeWorks Client Acquisition Engine

Date started: 2026-07-14
Target period: 2026-07-14 to 2026-10-12
Owner: Emmanuel Ehigbai

## Goal

Turn completed BridgeWorks client work into a predictable client-acquisition engine.

By 2026-10-12, BridgeWorks should convert CEEFM and Oliviks proof into public authority, qualified conversations, proposals, and paid engagements without Emmanuel manually creating every asset from scratch.

## Orchestrator

The acquisition engine uses two trigger modes:

- scheduled weekday, weekly, and dispatch-preparation runs
- event-driven runs for replies, approvals, new proof, browser results, and failures

The canonical runbook is `ORCHESTRATOR-RUNBOOK-2026-07-16.md` and the machine-readable cadence is `orchestrator-schedule.json`. Both are designed but not activated. They write mobile-readable summaries, approval items, and run logs. External sending, publishing, uploads, deployments, and paid enrichment remain explicitly approval-gated.

## 90-day success criteria

| Area | Target by 2026-10-12 |
|---|---|
| Delivery | Oliviks completed, handed over, evidenced, and documented. |
| Proof | Oliviks and CEEFM packaged into sales-ready assets. |
| Authority | AI visibility becomes the repeated BridgeWorks public subject. |
| Content | Active social channels run from one central content queue. |
| Prospecting | CEEFM and Oliviks proof used in weekly outbound. |
| Conversations | 12 qualified sales conversations. |
| Proposals | 3 proposals issued. |
| Revenue | 1 to 2 new paid engagements closed. |
| Delegation | Agents draft; Emmanuel approves and improves. |

## Active workstreams

1. Finish and extract Oliviks.
2. Make AI visibility the authority category.
3. Build one content operating system.
4. Connect content to prospecting.

## Phase sequence

| Phase | Dates | Operating focus |
|---|---|---|
| Phase 1 | 2026-07-14 to 2026-07-27 | Finish Oliviks, preserve evidence, establish proof and prospecting base. |
| Phase 2 | 2026-07-28 to 2026-08-10 | Package Oliviks and CEEFM proof, prepare authority content, prep four-week queue. |
| Phase 3 | 2026-08-11 to 2026-09-07 | Publish, prospect weekly, release AI Visibility Report, record replies and objections. |
| Phase 4 | 2026-09-08 to 2026-10-12 | Follow up, run calls, issue proposals, optimize the highest-performing proof and channels. |

## Week-one control files

| File | Role |
|---|---|
| `clients/oliviks/delivery/OLIVIKS-COMPLETION-CHECKLIST-2026-07-14.md` | Definition of done before Oliviks becomes a case-study package. |
| `clients/oliviks/evidence/OLIVIKS-EVIDENCE-INDEX-2026-07-14.md` | Evidence capture map for screenshots, decisions, metrics, approvals, and launch proof. |
| `clients/oliviks/evidence/metrics/oliviks-metric-sheet-2026-07-14.csv` | Baseline and final metric tracker. |
| `operations/client-acquisition-engine/CEEFM-PROOF-INVENTORY-2026-07-14.md` | Existing proof assets and how to use them in sales. |
| `operations/client-acquisition-engine/CEEFM-PROOF-MODULES-2026-07-14.md` | Reusable outreach, proposal, and sales-call proof blocks. |
| `operations/client-acquisition-engine/CONTENT-PIPELINE-2026-07-14.md` | Central queue structure for Emmanuel, BridgeWorks, Instagram/Facebook, video, and journal. |
| `operations/client-acquisition-engine/CONTENT-CHANNEL-INVENTORY-2026-07-14.md` | Verified public channels, unverified account routes, roles, and activation gates. |
| `operations/client-acquisition-engine/AI-VISIBILITY-REPORT-OUTLINE-2026.md` | Report structure and evidence requirements. |
| `operations/client-acquisition-engine/AI-VISIBILITY-REPORT-DRAFT-2026.md` | 3,900-plus-word evidence-led report manuscript. |
| `operations/client-acquisition-engine/research/AI-VISIBILITY-METHODOLOGY-V1-2026-07-14.md` | Stable scoring model, evidence classes, and platform claim guardrails. |
| `operations/client-acquisition-engine/research/ai-visibility-evidence-dataset-2026-07-14.csv` | Ten-record substantiated evidence corpus: six scored audits, three mini-scans, one implementation verification. |
| `operations/client-acquisition-engine/research/LANE-A-OBSERVATION-BANK-2026-07-14.md` | Three private response observations for each of the 15 Lane A first-contact drafts. |
| `operations/client-acquisition-engine/research/prospect-operations/README.md` | Weekday research-to-review contract, evidence threshold, gap-completion loop, and explicit external-action boundary. |
| `operations/client-acquisition-engine/research/prospect-operations/review/packets/2026-07-23-batch-01-approval-review.md` | First generated five-prospect review packet; one exact email is awaiting approval and no external action has run. |
| `operations/client-acquisition-engine/research/BRIDGEWORKS-WEBSITE-SOURCE-MAP-2026-07-14.md` | Production GitHub/Vercel identity, deployed commit, exact multilingual claim paths, offer drift, and local user-change preservation boundary. |
| `operations/client-acquisition-engine/sales/REPLY-TO-PROPOSAL-PLAYBOOK-2026-07-14.md` | Manual operating path from a genuine reply through qualification, proof selection, proposal, and follow-up. |
| `operations/client-acquisition-engine/sales/DISCOVERY-CALL-BRIEF-TEMPLATE-2026.md` | Reusable 20-to-25-minute discovery-call agenda, qualification record, and next-step gate. |
| `operations/client-acquisition-engine/templates/SME-DIGITAL-FOUNDATION-PROPOSAL-TEMPLATE-2026.md` | Prospect-specific proposal source with CEEFM proof, scope, exclusions, measures, investment, and pre-send checks. |
| `operations/client-acquisition-engine/content/WEEK-01-AUTHORITY-QUEUE-2026-07-20.md` | Twelve approval-ready authority drafts across LinkedIn, social, video, journal, and conversion use. |
| `operations/client-acquisition-engine/output/pdf/BridgeWorks-Small-Business-AI-Visibility-Report-2026-DRAFT.pdf` | Fourteen-page report review PDF; not approved or published. |
| `operations/client-acquisition-engine/output/pdf/BridgeWorks-CEEFM-Case-Study-2026-DRAFT.pdf` | Corrected four-page CEEFM review PDF using the verified 16-to-77 claim. |
| `operations/lead-engine-v1/01-prospects/prospect-batch-2026-07-14.csv` | Central 45-prospect queue with active-lane and deferred-lane states reconciled. |
| `operations/client-acquisition-engine/EXPANDED-PROSPECT-VERIFICATION-2026-07-14.md` | Top-five public verification and corrected offer angles for the expanded search. |
| `operations/client-acquisition-engine/scans/AI-VISIBILITY-MINI-SCAN-TEMPLATE.md` | Evidence-first format for small prospect scans without invented scores. |
| `operations/client-acquisition-engine/scans/dental-de-classique-mini-scan-2026-07-14.md` | Dental De Classique controlled-presence and booking-path scan. |
| `operations/client-acquisition-engine/scans/nimaz-aesthetic-mini-scan-2026-07-14.md` | Nimaz Aesthetic controlled-presence and patient-path scan. |
| `operations/client-acquisition-engine/scans/moso-agency-mini-scan-2026-07-14.md` | MOSO AGENCY controlled-presence and direct-enquiry scan. |
| `operations/client-acquisition-engine/CURRENT-STATE-AUDIT-2026-07-14.md` | Reconciliation of local work, HubSpot, Gmail, ClickUp connection state, and the Command Center. |
| `operations/client-acquisition-engine/approvals/OUTREACH-APPROVAL-PACKET-2026-07-14.md` | Three final follow-ups and three new first touches for Emmanuel's approval. |
| `operations/client-acquisition-engine/approvals/LANE-A-FIRST-CONTACT-APPROVAL-PACKET-2026-07-14.md` | Consolidated 15-contact Lane A wave: 12 priority drafts and 3 separately labeled tests. |
| `operations/client-acquisition-engine/approvals/BRIDGEWORKS-WEBSITE-CLAIM-CORRECTION-PACKET-2026-07-14.md` | Approval brief for stale or unsubstantiated website proof, scan, and automation claims. |
| `operations/client-acquisition-engine/approvals/WEEK-ONE-CONSOLIDATED-REVIEW-2026-07-14.md` | One prioritized 30-to-40-minute decision sheet across revenue, proof, authority, Oliviks, channels, and automation. |
| `operations/client-acquisition-engine/approvals/WEEK-ONE-RELATIONSHIP-AND-REFERRAL-PACKET-2026-07-14.md` | Five approval-only LinkedIn comments and one CEEFM referral request, with source and action gates. |
| `operations/client-acquisition-engine/approvals/WEEK-ONE-LINKEDIN-PUBLISH-BUNDLES-2026-07-14.md` | Three exact Chrome publish bundles with account, canonical copy, asset path, dimensions, hash, and approval state. |
| `operations/client-acquisition-engine/output/social/week-01/` | Two visually verified review PNGs for the first LinkedIn release; neither is approved or uploaded. |
| `operations/client-acquisition-engine/TWO-WEEK-EXECUTION-RUN-SHEET-2026-07-14.md` | Calendar-derived three-day and four-day kitchen modes, realistic execution blocks, collision decisions, and approval-aware stop rules. |
| `operations/client-acquisition-engine/approvals/NO-OWNED-SITE-OUTREACH-PACKET-2026-07-14.md` | Two clinic routing messages and one MOSO OLX first touch for Emmanuel's approval. |
| `operations/client-acquisition-engine/scorecards/WEEKLY-SCORECARD-2026-07-14.md` | Week-one baseline from verified current state. |
| `operations/client-acquisition-engine/offers/PAID-AI-READINESS-DIAGNOSTIC-OUTLINE-2026-07-15.md` | Internal diagnostic-first AI offer outline with interview, pain extraction, process-before-automation rules, effort/impact matrix, 4-day quick-start plan, pricing guardrail, and implementation upsell boundaries. |

All draft, PDF, outreach, content, and conversion assets require Emmanuel approval before sending, scheduling, publishing, or attaching to a prospect message.

Weekday research is scheduled for 09:10. The agent may verify public evidence and prepare exact outreach for review without supervision. A verified company is not outreach-ready until a specific commercial gap, proof choice, exact destination, exact copy, next action, and risks pass the local validator. Mission Control then holds the resulting external task in `awaiting_approval`; approval authorizes only that exact action.

The local lead-scoring prompt now follows the current offer ladder, but the workflow JSON still embeds the retired free-audit wording. The production website also presents different homepage offers by locale. Do not import, activate, update, or promote either path until Emmanuel confirms the unified offer and approves a guarded reconciliation.

## Weekly scorecard

Every week, answer this before building more system:

> What produced evidence, reach, conversations, or revenue, and what only made the system more elaborate?
