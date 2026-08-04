# BridgeWorks Prospecting Capability and Orchestration Audit

**Date:** 1 August 2026  
**Scope:** Local BridgeWorks skills, specialist agents, connected sales tools, representative client outputs, and their use across the prospect-to-client lifecycle.  
**Status:** Internal operating audit. No prospect records, messages, connections, follows, tasks, or campaigns were created.

## Executive conclusion

BridgeWorks already possesses most of the components required to run sophisticated value-first prospecting. The problem is not a shortage of audit skills. The problem is the absence of a reliable routing layer that:

1. detects what is happening in the prospect's business;
2. determines whether the prospect is legitimate and commercially qualified;
3. selects the smallest relevant skill stack;
4. produces one tailored demonstration of value;
5. identifies the decision owner;
6. renders a client-ready artefact;
7. records the evidence and next action;
8. advances outreach through an actually supported channel.

The current system is strongest at diagnosis and client-facing recommendations. It is weaker at qualification, operational diagnosis, capability routing, LinkedIn execution, and moving artefacts into a controlled sales workflow.

The correct acquisition unit is therefore:

> **Observed lead condition -> qualification -> relevant diagnostic -> tailored demonstration -> decision owner -> permission-based contact -> CRM and task progression**

It is not:

> Country -> Google Maps list -> generic audit -> generic message

## Inventory summary

The active local BridgeWorks skill directory contains:

- **58 custom skills**
- **21 specialist-agent skills**
- **15 market-suite skills**
- **5 marketing-audit specialist agents**
- **5 GEO specialist agents**
- **5 advertising specialist agents**
- sales-lifecycle skills for client audit, discovery preparation, engagement architecture, proposal creation, and post-call follow-up

The specialist capacity is real. The orchestration and installation state is uneven.

## What the representative client work proves

### University of Pattern Drafting

Two different audits found different classes of opportunity.

The marketing audit scored the business **29/100** and exposed:

- no effective homepage value proposition;
- no email capture;
- WhatsApp-only conversion dependence;
- dead-end course pages;
- weak public proof;
- underdeveloped offer and pricing architecture;
- no reliable nurture, upsell, or retention path.

The GEO audit scored the business **20/100** and exposed:

- crawler reachability problems;
- no structured data;
- no `llms.txt`;
- no citable informational content;
- weak entity and authority signals;
- no confirmed sitemap or canonical consistency;
- weak AI-platform discoverability.

**What this proves:** one audit does not substitute for the other. A marketing audit diagnoses demand and conversion. A GEO audit diagnoses whether AI systems can understand, trust, and cite the business.

### CEEFM

The client record proves that GEO diagnosis can become implementation.

The GEO score progressed from **16/100 to 78/100**. The engagement implemented:

- ProfessionalService schema;
- FAQPage schema;
- explicit permissions for 13 AI crawlers;
- `llms.txt`;
- bilingual hreflang;
- canonical URLs;
- security headers;
- Open Graph and Twitter Card metadata;
- Bing Webmaster verification;
- GA4;
- Google Consent Mode v2;
- cookie consent;
- Wikidata entity work;
- IndexNow;
- an expanded sitemap;
- four service-funnel pages;
- LinkedIn company-page improvements;
- TikTok Business setup;
- a cold-email sequence and pipeline.

**What this proves:** an audit should not merely list deficiencies. It can serve as the diagnostic layer for a staged build programme, with a score progression and implementation evidence.

### Oliviks

The marketing audit scored the business **38/100** and exposed:

- unclear positioning;
- real-world proof missing from the website;
- empty and duplicate commerce pages;
- weak direct-order conversion;
- no owned retention system;
- underused catering demand;
- dependence on Wolt and Foodora.

The downstream engagement produced:

- a new marketing website;
- a restyled and secured WooCommerce shop;
- a customer-owned email and WhatsApp list;
- welcome automation;
- Google Business Profile work;
- review handling;
- a counter QR acquisition asset;
- a client-owned operational handover.

**What this proves:** the highest-value result is often the system built from the audit, not the audit itself.

## Capability map by prospecting stage

| Stage | Current capability | Skills or agents | Tools | Output | State |
|---|---|---|---|---|---|
| Market sensing | Track paid demand, deadlines, programme funding, buyer discourse, and hiring signals | `market`, `market-competitors` | Web research, job boards, official sources | Market and trigger radar | Available, newly structured |
| Prospect discovery | Find businesses by search, directories, listings, job posts, funding, and public signals | No dedicated BridgeWorks discovery skill | Web, browser, Apollo | Candidate account | Partly available |
| Legitimacy gate | Reject fictional, dormant, placeholder, or unverifiable businesses | No dedicated skill | Browser, registries, website, HubSpot duplicate search | Qualified or rejected candidate | Workflow exists only as a lesson |
| Commercial qualification | Determine budget signal, urgency, buyer moment, fit, and likely deal value | Missing `lead-qualifier-skill` | Public evidence, Apollo, HubSpot | Qualification record | Material gap |
| Quick digital scan | Website, social presence, search visibility, reviews, local signals, competitor context | `client-audit` | Browser, web, social search | `CLIENT-AUDIT-[name].md` | Available |
| Full marketing diagnosis | Content, conversion, SEO, competition, trust, and growth strategy | `market-audit` plus five `agent-market-*` specialists | Browser, web, performance evidence | `MARKETING-AUDIT.md` | Available |
| GEO diagnosis | Citability, authority, E-E-A-T, crawler access, schema, platform readiness | Stored `geo-audit` plus five `agent-geo-*` specialists | Browser, web, technical inspection | `GEO-AUDIT-REPORT.md` | Agents available; orchestrator not actively installed |
| Local visibility diagnosis | Google profile, reviews, NAP, local pages, schema, search presentation | `client-audit`, `market-seo`, GEO local-business adjustment | Browser, web, Google Maps when connected | Local visibility brief | Partly available |
| Funnel and lead-capture diagnosis | Journey, leakage, forms, nurture, offer sequence, sales handoff | `market-funnel`, `market-landing`, `market-emails` | Browser, website inspection | Funnel map and recovery actions | Available |
| Copy demonstration | Rewrite hero, offer, CTA, landing section, email, or campaign | `market-copy`, `market-emails`, `market-landing` | Local documents | Before-and-after demonstration | Available |
| Social-authority demonstration | Content pillars, post concepts, profile positioning, calendar | `market-social`, `market-brand` | LinkedIn public evidence, social pages | Authority mini-system | Available |
| Advertising diagnosis | Audience, budget, competition, creative, funnel | `market-ads` plus five `agent-ads-*` specialists | Ad libraries, website, public evidence | Campaign and funnel plan | Available |
| Operational/CRM diagnosis | Lifecycle, ownership, automation, handoffs, reporting, failure handling | No dedicated prospect audit | HubSpot evidence if provided, browser, process clues | Revenue-system or workflow audit | Major gap |
| AI-workflow diagnosis | Workflow opportunity, data readiness, controls, evaluation, ownership, handover | No dedicated prospect audit | Public evidence, process interview | AI readiness or workflow demo | Major gap |
| Decision-maker research | Identify founder, executive, functional owner, and public profile | No dedicated BridgeWorks skill | Apollo, public LinkedIn, company pages, registries | Named buying committee | Available with limits |
| Client-facing PDF | Designed audit or report | `market-report-pdf`, `pdf`, shared BridgeWorks renderer | Local runtime | Branded PDF | Available through fallback; installed market PDF skill is broken |
| CRM record | Company, contact, deal, evidence, source, stage, and next action | `bridgeworks-operating-system`, HubSpot skill | HubSpot | Commercial source of truth | Read works; writes currently require reauthorization |
| Follow-up task | Owner, due date, dependencies, approval state | `bridgeworks-operating-system` | ClickUp | Execution source of truth | Connected and read-verified |
| Email outreach | Tailored first contact, follow-up, attachment, or link | `market-emails`, `post-call-followup` | Gmail | Draft email | Connected; send requires approval |
| LinkedIn outreach | Decision-maker viewing, follow, connection, DM, engagement | Copy can be drafted by `market-social` or `market-emails` | LinkedIn API or controlled browser | Connection or conversation | API gap for follows, invitations, and DMs |
| Discovery preparation | Research, hypotheses, questions, positioning, red flags | `discovery-call-prep` | Website, public evidence, CRM context | `DISCOVERY-PREP-[name].md` | Available |
| Post-call progression | Client-language recap, commitments, next step, deal assessment | `post-call-followup` | Notes, Gmail draft, HubSpot/ClickUp | Follow-up and action list | Available |
| Scope control | Separate facts, assumptions, scope, acceptance, dependencies, risks, and approvals | `engagement-architect` | Notes, emails, intake evidence | Engagement specification and evidence ledger | Available |
| Proposal | Specific scope, timeline, price, and next step | `new-proposal`, `market-proposal` | Documents and PDF | Client proposal | Available after verified scope and supplied pricing |
| Delivery handoff | Client workspace, tasks, files, technical delivery, milestones | `bridgeworks-operating-system` and implementation skills | ClickUp, Drive, GitHub, HubSpot | Controlled delivery system | Available by service line |

## Diagnostic routing by observed lead condition

The system should not automatically run every audit. It should invoke the smallest combination capable of demonstrating the relevant outcome.

### Condition 1: The business is credible but its value is hard to understand or buy

**Primary stack**

- `market-audit`
- `agent-market-content`
- `agent-market-conversion`
- `agent-market-competitive`
- `agent-market-technical`
- `agent-market-strategy`

**Optional demonstrations**

- `market-copy` for a rewritten hero and offer section
- `market-funnel` for the buying path
- `market-landing` for a conversion page

**Prospect asset**

A demand-and-conversion brief with one implemented example, not a list of defects.

### Condition 2: The business has expertise but weak AI-search visibility

**Primary stack**

- GEO orchestrator after repair or installation
- five `agent-geo-*` specialists

**Optional demonstrations**

- a rewritten citable answer block;
- Organization, Service, Course, Person, FAQ, or LocalBusiness JSON-LD;
- a draft `llms.txt`;
- an entity and citation plan.

**Prospect asset**

A GEO opportunity brief showing what AI systems currently fail to understand and the exact content or schema needed to fix it.

### Condition 3: A local business has strong reviews or demand but weak owned conversion

**Primary stack**

- `client-audit`
- `market-funnel`
- `market-seo`

**Optional demonstrations**

- `market-copy` for homepage positioning;
- `market-emails` for retention;
- `market-social` for review and authority reuse.

**Tools**

- Google Search and rendered browser inspection;
- Google Maps only after the connector is configured or through controlled browser research;
- website enquiry-path testing.

**Prospect asset**

A local demand-capture map: find -> trust -> enquire/order -> join list -> repeat.

### Condition 4: Paid ads are visible but the destination or follow-up is weak

**Primary stack**

- `market-ads`
- `agent-ads-competitive`
- `agent-ads-funnel`
- `agent-ads-creative`
- `market-landing`
- `market-funnel`

**Prospect asset**

A lead-leak audit that ties observed advertising spend to landing friction, response handling, nurture, and CRM ownership.

### Condition 5: The founder is credible but the company has weak authority content

**Primary stack**

- `market-brand`
- `market-social`
- `market-copy`
- `market-competitors`

**Prospect asset**

A founder-to-company authority system containing profile positioning, three content pillars, one finished post, proof extraction, and a conversion route.

### Condition 6: The company is hiring RevOps, CRM, automation, or an operator

**Current workaround**

- public role research;
- `market-funnel`;
- `engagement-architect` concepts for ownership and acceptance;
- manual architecture reasoning.

**Needed skill**

`revenue-system-audit` or `pre-hire-operating-system-audit`

It should diagnose lifecycle stages, ownership, integrations, handoffs, reporting, failure handling, documentation, and the first 30 days of implementation.

### Condition 7: The company is experimenting with AI or automation

**Current workaround**

- public workflow evidence;
- technical and process reasoning;
- `engagement-architect` for controls and scope.

**Needed skill**

`ai-workflow-readiness-audit`

It should produce:

- workflow inventory;
- value and feasibility score;
- data and access requirements;
- human-control points;
- evaluation plan;
- error handling and rollback;
- client ownership and handover;
- one bounded demonstration.

### Condition 8: A funding programme, grant, or institution supports delivery

**Primary stack**

- `market-competitors` for programme and delivery landscape;
- `engagement-architect`;
- `market-proposal` or `new-proposal`;
- a future cohort-design skill.

**Prospect asset**

A funded cohort diagnostic and implementation-lab design, not an individual SME audit.

## Specialist agents

### Marketing audit agents

- `agent-market-content`
- `agent-market-conversion`
- `agent-market-competitive`
- `agent-market-technical`
- `agent-market-strategy`

These collectively produce the six scored sections used by `market-audit`.

### GEO agents

- `agent-geo-ai-visibility`
- `agent-geo-platform-analysis`
- `agent-geo-technical`
- `agent-geo-content`
- `agent-geo-schema`

These exist locally even though the GEO orchestrator is not installed in the active skill directory.

### Advertising agents

- `agent-ads-audience`
- `agent-ads-budget`
- `agent-ads-competitive`
- `agent-ads-creative`
- `agent-ads-funnel`

These support a full advertising opportunity, creative, budget, competitive, and conversion-path analysis.

Specialist agents should be used when the target opportunity justifies their research depth. They should not be invoked to inflate a document.

## Connected-tool capability audit

### HubSpot

**Connection:** active, EU-hosted BridgeWorks portal.

**Verified capability:**

- read contacts;
- read companies;
- read deals;
- perform duplicate and pipeline checks.

**Current limitation:**

The direct HubSpot capability check reports that writing contacts, companies, deals, notes, tasks, calls, meetings, and emails requires reauthorization. The acquisition system must not claim that it can currently write a fully qualified lead into HubSpot without first resolving those permissions.

### ClickUp

**Connection:** active and read-verified for Emmanuel Ehigbai.

**Role:**

- follow-up tasks;
- research and audit production tasks;
- approvals;
- proposal and delivery dependencies;
- due dates and owners.

ClickUp should receive execution work only after the commercial record is qualified.

### Apollo

**Connection:** active.

**Useful capability:**

- search people by company, title, seniority, and location;
- identify likely decision owners;
- enrich only after approval where credits or personal contact data are involved.

**Limitations:**

- organisation search consumes credits and may be unavailable on the current plan;
- personal enrichment can consume credits;
- Apollo should follow a HubSpot duplicate check.

### LinkedIn

**Connection:** active and read-verified.

**Available through the connected API:**

- authenticated profile lookup;
- personal or organisation posting where permissions permit;
- comments;
- reactions;
- post inspection where accessible.

**Not exposed by the current connected tools:**

- prospect direct messages;
- connection invitations;
- following a person;
- following a company;
- general prospect search.

Decision-maker search should use Apollo and public web evidence. LinkedIn invitations, follows, and direct messages require a controlled browser or manual execution after explicit approval. The system must not describe those actions as currently automatable through Composio.

### Gmail

**Connection:** active.

**Available:**

- search and review correspondence;
- create and update drafts;
- send an approved draft.

Initial prospecting should create reviewable drafts, not send automatically.

### Google Maps

**Toolkit capability exists, but there is no active connection.**

Potential supported research includes:

- text search;
- place matching;
- address and operational status;
- ratings and review counts;
- place details and reviews.

Until connected, Maps research must use the browser or normal web search. Maps should remain a validation and local-evidence surface, not the universal top-of-funnel source.

## Skill-health findings

### Working or substantially usable

- `client-audit`
- `market-audit`
- five marketing specialist agents
- five GEO specialist agents
- five advertising specialist agents
- `market-copy`
- `market-funnel`
- `market-landing`
- `market-seo`
- `market-social`
- `market-emails`
- `market-competitors`
- `discovery-call-prep`
- `post-call-followup`
- `engagement-architect`
- `new-proposal`
- `market-proposal`
- `pdf`, `docx`, and `pptx`
- `bridgeworks-operating-system`

### Broken or incomplete

#### 1. GEO orchestration is not active

The five GEO agents exist, but `C:\Users\User\.codex\skills\geo-audit\SKILL.md` does not.

The stored plugin copy exists under the BridgeWorks Codex project, but it refers to a missing Claude-era brand-constants path. The orchestrator should be migrated or installed into the active skill directory and its resource paths repaired.

#### 2. `market-report-pdf` references a missing generator

The skill expects:

`market-report-pdf\scripts\generate_pdf_report.py`

That file is absent from the installed skill directory.

The shared acquisition-engine Markdown renderer and the general PDF skill can still produce branded reports, but the specific market PDF skill is not self-contained and should not be considered healthy.

Its documented colour system also conflicts with current BridgeWorks navy, gold, and ivory standards.

#### 3. Lead qualification is missing

`engagement-architect` references `lead-qualifier-skill`, but that skill is absent.

This is a serious acquisition gap. Without it, diagnosis can begin before legitimacy, urgency, budget evidence, decision access, and service fit have been evaluated consistently.

#### 4. No need-to-capability router exists

There is no skill that accepts a candidate account and selects:

- qualification route;
- primary audit;
- specialist agents;
- tailored demonstration;
- decision-maker research;
- PDF format;
- outreach channel;
- CRM and ClickUp actions;
- approval gates.

This missing router is the central problem identified by this audit.

#### 5. No operational or AI workflow prospect audit exists

The current audit estate is marketing-heavy. BridgeWorks also sells direction-to-execution, automation, CRM, AI workflows, operating systems, and cross-functional implementation.

A business may have a strong website and still be an ideal BridgeWorks prospect because its enquiry routing, lifecycle ownership, CRM data, reporting, or AI workflow is fragmented. The current skills do not diagnose that need adequately.

#### 6. LinkedIn execution is overstated

LinkedIn account access does not mean direct-message, invitation, or follow automation exists. The current system can research public evidence and draft the actions, but execution requires controlled browser interaction or manual approval.

## Corrected end-to-end prospecting architecture

### Gate 1: Detect a buyer event

Sources:

- hiring;
- funding;
- launch;
- paid advertising;
- regulatory deadline;
- new location;
- platform migration;
- public complaint;
- review pattern;
- visible lead-routing or conversion failure;
- grant or procurement opportunity.

Output:

- observed event;
- source;
- date;
- likely business consequence.

### Gate 2: Verify legitimacy

Check:

- real operating website;
- real legal or professional identity where appropriate;
- real people;
- current activity;
- consistent address and contact evidence;
- no demo, placeholder, fictional, or copied-company warning;
- HubSpot duplicate.

Output:

- pass;
- reject;
- hold for verification.

### Gate 3: Qualify commercial fit

Score:

- observable budget;
- urgency;
- consequence;
- service fit;
- decision-owner accessibility;
- existing implementation spend;
- complexity BridgeWorks can credibly own;
- disqualifiers.

Output:

- audit approved;
- research only;
- partner-led;
- reject.

### Gate 4: Select one primary diagnostic

Choose one:

- quick client audit;
- full marketing audit;
- GEO audit;
- local demand-capture audit;
- paid-media lead-leak audit;
- founder-authority audit;
- future revenue-system audit;
- future AI-workflow-readiness audit.

Do not run multiple full audits merely because the skills exist.

### Gate 5: Produce one value demonstration

Examples:

- rewritten homepage hero;
- corrected conversion path;
- lifecycle map;
- CRM architecture;
- `llms.txt`;
- JSON-LD block;
- lead-response workflow;
- content proof module;
- email nurture sequence;
- AI workflow with evaluation and ownership controls;
- cohort implementation design.

The demonstration is the lure. The audit is the evidence supporting it.

### Gate 6: Identify the buying committee

Find:

- economic buyer;
- functional owner;
- likely champion;
- technical or compliance stakeholder;
- public profile and contact route.

Use Apollo, company evidence, public LinkedIn, and registries. Do not enrich merely to make the record look complete.

### Gate 7: Package the artefact

The prospect-facing document should contain:

1. why BridgeWorks selected the business now;
2. what BridgeWorks is;
3. observed evidence;
4. commercial or operational consequence;
5. the tailored demonstration;
6. recommended action sequence;
7. what BridgeWorks would implement;
8. evidence, limitations, and verification requests.

### Gate 8: Record and assign

HubSpot:

- company;
- contact;
- trigger;
- source;
- audit type;
- qualification;
- stage;
- evidence;
- next action.

ClickUp:

- approved production task;
- asset status;
- outreach approval;
- follow-up due date;
- dependencies.

HubSpot writes remain blocked until permissions are repaired.

### Gate 9: Contact through the supported route

Preferred:

- permission-based email draft;
- warm introduction;
- partner introduction;
- controlled LinkedIn browser action;
- public engagement followed by an approved connection or message.

Do not claim LinkedIn API automation for unsupported actions.

### Gate 10: Advance based on response

- positive response -> `discovery-call-prep`;
- completed call -> `post-call-followup`;
- defined opportunity -> `engagement-architect`;
- approved scope and supplied pricing -> `new-proposal` or `market-proposal`;
- won deal -> BridgeWorks client-delivery cycle.

## Recommended remediation order

### Priority 1: Build the need-to-capability router

Create `prospect-opportunity-router`.

It should accept a candidate and produce:

- evidence ledger;
- legitimacy result;
- qualification score;
- observed-need classification;
- recommended skill stack;
- agent plan;
- demonstration asset;
- research and tool plan;
- approval gates;
- CRM and ClickUp payloads;
- channel recommendation;
- disqualifiers.

### Priority 2: Restore qualification

Create or restore `lead-qualifier-skill`. It must run before expensive audit production.

### Priority 3: Repair GEO orchestration

Install the GEO orchestrator into the active Codex skill directory, correct its brand-resource path, and validate one known client result.

### Priority 4: Repair PDF production

Either:

- restore the missing `generate_pdf_report.py` and update it to current BridgeWorks branding; or
- retire that script reference and standardise on the verified shared renderer plus the general PDF inspection workflow.

### Priority 5: Add operational diagnostics

Create:

- `revenue-system-audit`;
- `ai-workflow-readiness-audit`;
- optionally `local-demand-capture-audit`.

These would allow prospecting to reflect all BridgeWorks service lines rather than marketing alone.

### Priority 6: Repair HubSpot write permissions

Reauthorize the HubSpot connector with the minimum required write scopes for:

- companies;
- contacts;
- deals;
- notes;
- tasks or equivalent next actions.

Do not create duplicate commercial structures.

### Priority 7: Decide the LinkedIn execution policy

Choose one:

- manual execution from approved drafts;
- controlled browser execution with explicit approval per action or batch;
- a compliant supported provider if one becomes available.

The policy should not assume that Composio exposes connection invitations or DMs when it does not.

### Priority 8: Connect Google Maps only if it improves the selected workflows

Google Maps should support local verification, reviews, place matching, and local audit evidence. It should not become the default prospect source again.

## Final operating rule

The system should spend 15 to 20 minutes only after a lead passes legitimacy and commercial qualification.

That time should buy:

- a relevant specialist diagnosis;
- a tangible demonstration;
- a named buyer;
- a credible entry route;
- a recorded next action.

If it produces only a longer audit, it has failed.

## Execution addendum: the hidden skill estate

The first inventory understated the available capability because it treated the active Codex skill directory as the complete estate. A wider filesystem audit found four distinct skill estates:

| Estate | Skill folders found | Operating meaning |
|---|---:|---|
| Active Codex skills | 58 at time of initial audit | Closest to callable production |
| Claude skills | 74 | Useful source material, not automatically active in Codex |
| BridgeWorks Codex plugin source | 129 | Broadest build source; contains inactive and duplicated capabilities |
| Full skills export | 62 | Migration/backup source, not an operating registry |

The missing prospecting capabilities were therefore mostly stranded, not absent.

### High-value capabilities found outside the active estate

| Capability family | Skills found | What they can produce | Finding |
|---|---|---|---|
| Qualification | `lead-qualifier-skill`, `lead-qualifier`, `bridgeworks-lead-qualification` | Scores, stages, and workflow handoffs | Legacy logic is geographically biased, price-stale, and too willing to default to a free audit |
| Prospecting orchestration | `prospecting-department` | Department-level workflow pointer | Thin pointer to older Budapest/CEE/Nigeria operating logic |
| GEO | `geo-audit` plus 13 specialist/report/prospect skills | Citability, crawler, schema, technical, content, platform, comparison, report, PDF, proposal, and prospect records | Substantive capability exists, but the orchestrator is inactive and some sales claims/prices are stale |
| Revenue operations | `revops` | Lifecycle, pipeline, ownership, handoff, reporting, and system diagnosis | Strong generic source, but not aligned to BridgeWorks truth systems or initial-contact evidence limits |
| Demand programs | `referrals`, `lead-magnets`, `gsc-opportunity`, `competitive-research` | Referral systems, capture assets, search-demand prioritization, and competitor evidence | Useful source and campaign capabilities; they are not substitutes for prospect qualification |
| Delivery departments | `client-ops-department`, `content-department`, `design-department` | Department routing | Thin pointers; production value depends on their referenced operating instructions |

### Corrected operating interpretation

- A skill present in `.claude`, plugin source, or an export is not active merely because its files exist.
- `geo-prospect` must not create a JSON shadow CRM. HubSpot remains commercial truth.
- Legacy GEO proposals must not import hard-coded prices, unsupported market statistics, or speculative ROI.
- `market-report-pdf` remains blocked because its declared generator script is missing.
- Referrals, GSC, Maps, LinkedIn, Apollo, and content programs are prospect sources or channels. They do not decide whether bespoke work is warranted.

### Repairs executed on 2026-08-01

Two new skills were authored with baseline tests, deterministic checks, forward tests, and structural validation:

1. `bridgeworks-lead-qualifier`
   - removes geography scoring and hard-coded price logic;
   - requires at least four verified signals, a 65+ score, a buyer path, and an evidenced service route before bespoke work;
   - separates `nurture`, `research`, `audit-approved`, and `discovery-ready`;
   - blocks a free asset for a merely imperfect site.
2. `bridgeworks-prospect-router`
   - requires the qualification gate;
   - chooses one commercial question, primary service route, asset, and buyer;
   - caps production at four work passes and 20 minutes;
   - checks active, deferred, blocked, and stale capabilities before naming them;
   - prepares HubSpot and ClickUp handoffs without creating a parallel CRM;
   - explicitly gates Gmail sending, LinkedIn action, Apollo credit spend, and connector writes.

Both skills are installed in the active Codex skill directory. The router's forward test exposed a singular/plural schema mismatch between its documented output and validator. That defect was corrected and the exact contract passed on re-test.

### Revised service-line production map

| Service route | Initial commercial question | Small proof asset | Current production route | Missing repair |
|---|---|---|---|---|
| Strategy & Transformation | Which dated choice or expansion decision is being blocked? | Decision brief or priority-to-execution map | Public research, competitor evidence, strategic synthesis | No new specialist required for the first proof |
| Digital Platforms & Brand Systems | Where does the visible buyer journey lose clarity or trust? | Annotated conversion path or before/after page concept | `client-audit` plus focused market and document skills | None for bounded initial proof |
| Content, Visibility & Demand | Where is real demand not being captured or cited? | Search/AI visibility gap and three-page opportunity | `market-seo` plus `bridgeworks-geo-prospect-scan` | Bounded initial-contact route active; full GEO suite remains a paid-delivery migration |
| AI & Workflow Automation | Which observable handoff is a credible automation candidate? | Workflow friction map or candidate matrix | `bridgeworks-ai-workflow-scan` plus public journey evidence and a synthetic demo | Bounded initial-contact route active |
| Execution & Operating Systems | Where are ownership, lifecycle, or reporting boundaries most exposed? | Lead-to-owner or reporting map | `bridgeworks-revenue-system-scan`; HubSpot reads when relevant | Bounded initial-contact route active |

The three missing initial-contact routes were subsequently restored and activated as:

- `bridgeworks-geo-prospect-scan`;
- `bridgeworks-revenue-system-scan`;
- `bridgeworks-ai-workflow-scan`.

Each was baseline-tested without the skill, authored, structurally validated, forward-tested with the skill, corrected from test feedback, revalidated, and installed. The older full GEO and generic RevOps sources remain available for deliberate paid-delivery migration; they are no longer mistaken for safe initial-contact capabilities.

## Dogfood validation: BridgeWorks as the prospect

On 2 August 2026, BridgeWorks was run through the repaired acquisition system as an internal prospect with no insider exemption.

- Deterministic qualification: `discovery-ready`, 100/100, eight verified signals.
- Primary route: `execution-operating-systems`.
- Primary buyer: Emmanuel Ehigbai, Founder and Principal.
- Commercial question: how BridgeWorks should turn a buyer event into one governed prospect-to-proof loop without duplicating commercial truth.
- Specialist invoked: `bridgeworks-revenue-system-scan`.
- Specialists correctly not invoked: GEO and AI workflow scans.
- Asset: a 584-word, three-page BridgeWorks Prospect-to-Proof Control Loop.
- Validation: qualifier and route scripts passed; PDF text and all pages were inspected.
- Execution: three internal ClickUp tasks were created and the existing HubSpot reauthorization task was reused.
- External action: none.

The test found that the repaired skills work as a decision layer, but the production intake does not yet operate as the same system. Website submissions can be stored and can create or update HubSpot contacts, while qualification, service routing, proof-asset release, ClickUp execution, and market learning remain separate. The universal free GEO audit decision also conflicts with the active rule that bespoke work is earned by qualification.

Canonical dogfood run:

`operations/client-acquisition-engine/runs/2026-08-02-bridgeworks-dogfood/`

The first implementation test is therefore a five-account manual control loop. Automation is deferred until the pilot shows which trigger, route, asset, and channel create verified stage movement.
