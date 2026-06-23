# BridgeWorks YouTube Adoption Decisions

This file records what BridgeWorks adopts, adapts, or rejects from YouTube intelligence.

Do not store passive notes here.

Only record decisions that change how BridgeWorks sells, fulfills, reports, automates, or creates proof.

## Decision Format

```text
### YYYY-MM-DD - [Idea / Framework / Tool]

Source:
Decision: Adopt / Adapt / Reject
BridgeWorks area:
Reason:
Action:
Owner:
Status:
```

### 2026-05-17 - Service Business Homepage Audit Checklist

Source: Wes McDowell - "Why is THIS the Perfect Homepage?"

Decision: Adapt

BridgeWorks area: Digital Infrastructure, conversion audit previews, website builds

Reason: The homepage-as-conversion-path framework is useful for service-business audits, but BridgeWorks should translate it into sober B2B language for CEE and African SMEs.

Action: Create a BridgeWorks Service Business Homepage Audit Checklist and use it in the first conversion-audit preview PDF.

Owner: Emmanuel / BridgeWorks

Status: Next action

### 2026-06-18 - BridgeWorks Hermes Operating Layer Maturity Checklist

Source: Jack Roberts - "Every Level of Hermes Agent Explained"

Decision: Adapt

BridgeWorks area: Agency Operations, AI Growth Systems

Reason: The transcript gives a useful maturity model for moving from one-shot prompts to memory, skills, connectors, subagents, scheduled work, and reporting. BridgeWorks already has parts of this through Command Center and scheduled routines, but needs a visible checklist and dashboard layer before productising it.

Action: Create a BridgeWorks Hermes Operating Layer Maturity Checklist and score current routines against it.

Owner: Codex / Emmanuel

Status: Needs asset creation

### 2026-06-18 - Article-to-3-Drafts Content Repurposing Pipeline

Source: MLTut - "Turn 1 Blog Post Into 3 Posts Automatically (n8n + AI, No Code)"

Decision: Adopt internally / Adapt for clients

BridgeWorks area: Content And Visibility Systems

Reason: The workflow has clear implementation logic: one source URL, scrape check, three platform-specific prompts, and a review layer. It fits BridgeWorks' no-autopublish approval rule.

Action: Draft an automation spec and prompt library item for LinkedIn, X, and newsletter draft generation from long-form assets.

Owner: Codex / Claude Code after approval

Status: Needs spec

### 2026-06-18 - Missed-call Speed-to-Lead Audit Module

Source: Jason Wardrop - "How I Built A 10K/mo Side Income Sharing Other People's Software Online"

Decision: Adapt

BridgeWorks area: Sales And Prospecting, AI Growth Systems

Reason: The affiliate model is not the right primary business model for BridgeWorks, but the missed-call pain is concrete and useful for local SME audits and offers.

Action: Add a vendor-neutral missed-call and speed-to-lead module to audit previews. Validate tools manually before any implementation offer.

Owner: Emmanuel / BridgeWorks

Status: Needs module draft

### 2026-06-19 - AI Delivery Verification Checklist

Source: Nate Herk - "How to Build Effective Claude Code Agents in 2026"

Decision: Adopt

BridgeWorks area: AI Growth Systems, Agency Operations, Client Delivery

Reason: The transcript gives a direct operating loop for agentic work: plan with context, build, verify, then evolve the system. This fits Emmanuel's no-manual-coding reality and reduces the risk of accepting agent claims without proof.

Action: Create a BridgeWorks AI Delivery Verification Checklist and require proof outputs for website, automation, PDF, and research deliverables.

Owner: Codex / Emmanuel

Status: Needs checklist asset

### 2026-06-19 - Prospect Micro-Audit Template

Source: Sandy Lee AI - "How I Got My First AI Client in 2 Weeks (No Portfolio)"

Decision: Adapt

BridgeWorks area: Sales And Prospecting, Proof And Authority

Reason: The beginner-client framework is useful, but BridgeWorks should not depend on Upwork as the main channel. The durable lesson is a small relevant proof asset plus a problem-specific micro-audit.

Action: Create a reusable micro-audit template for local SME websites and AI visibility prospects. Keep outreach approval-gated.

Owner: Emmanuel / BridgeWorks

Status: Needs template

### 2026-06-19 - design.md Website Production Source

Source: Build Great Products - "Framer 3.0 Just Changed Website Design Forever"

Decision: Adapt

BridgeWorks area: Digital Infrastructure, Website Production System

Reason: Framer's agent workflow is useful as a prototype pattern, but BridgeWorks should not replace its static-first Next.js/Vercel default without a client and scope reason. The strong adoption is `design.md` as the handoff between brand context, code, and visual prototypes.

Action: Create a `design.md` template and add it to the website production process before any Framer-style prototype experiment.

Owner: Codex / Claude Code after approval

Status: Needs template

### 2026-06-21 - AI Operating Layer Workflow Map

Source: Paul J Lipsky - "The Simple Claude Cowork OS That Automates My Work"

Decision: Adapt

BridgeWorks area: Agency Operations, AI Growth Systems, Client Delivery

Reason: The transcript gives a practical structure for turning local folders, memory files, workflow instructions, connectors, skills, and schedules into a repeatable operating layer. BridgeWorks already has scheduled routines and local context files, but they need a visible workflow map before this becomes a client-facing method.

Action: Create a BridgeWorks AI Operating Layer Workflow Map and score YouTube Digest, Inbound Prospect Triage, and Oliviks QA against it.

Owner: Codex / Emmanuel

Status: Needs SOP asset

### 2026-06-21 - Validation Landing Page Sprint

Source: Michia Rohrssen - "How to launch a startup on easy mode (with AI)"

Decision: Adapt

BridgeWorks area: Digital Infrastructure, Sales And Prospecting, Build Brief

Reason: The workflow is useful because it ends at a real buying signal, not just a generated product idea. BridgeWorks should keep the validation logic but apply stricter approval gates for publishing, tracking, ad spend, and claims.

Action: Draft a BridgeWorks Validation Landing Page Sprint spec for Build Brief and future SME campaigns. Ban fake proof and require Emmanuel approval before external publishing or paid ads.

Owner: Codex / Claude Code after approval

Status: Needs spec

### 2026-06-21 - Paired Metrics Reporting Card

Source: Alex Hormozi - "How to Measure Customer Happiness (Paired Metrics)"

Decision: Adopt

BridgeWorks area: Client Delivery, Reporting, Retention

Reason: Paired metrics prevent reports from rewarding output while hiding quality loss. This fits Foundation website delivery, Digital Growth Engine reporting, and future client retainers.

Action: Create a one-page paired metrics reporting card: progress metric, quality guardrail, interpretation, next action.

Owner: Emmanuel / BridgeWorks

Status: Needs template

### 2026-06-22 - Pricing Integrity Guardrail

Source: Alex Hormozi - "You're Ashamed of Not Having Integrity With Your Own Pricing"

Decision: Adopt

BridgeWorks area: Pricing, sales qualification, scope control

Reason: The transcript gives a useful guardrail for a solo operator: do not discount because of pressure, sympathy, or fear, then resent the client later. If BridgeWorks accepts a lower price, it must be a deliberate trade-off with scope boundaries.

Action: Add a pricing integrity check before offers, discounts, and scope expansions: normal price, concession, exchange received, scope removed, peace check, and one-time-vs-rule decision.

Owner: Emmanuel / BridgeWorks

Status: Needs template integration

### 2026-06-23 - AI UGC Ad Sprint Approval Checklist

Source: Sandy Lee AI - "I Used Claude MCP to Make AI UGC Ads and Make Money in 2026"

Decision: Adapt

BridgeWorks area: Content And Visibility Systems, Offer Testing, Client Delivery

Reason: The workflow is useful for creating proof assets and ad concepts from product pages, ICP notes, hook research, scripts, and actor / voice selection. BridgeWorks should keep it draft-only until assets, client approval, and ad spend limits exist.

Action: Create a draft-only AI UGC ad sprint checklist for BridgeWorks and possible Oliviks use after missing client assets are confirmed.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist. No publishing, client contact, or paid ads without approval.

### 2026-06-23 - Model-Routing Cost Gate

Source: Nate Herk - "I Battle Tested Sakana Fugu's Fable Killer"

Decision: Reject for now / Watch

BridgeWorks area: Local AI Ops, Agency Operations, Delivery Verification

Reason: The transcript reports 36 of 38 tasks tied, while Fugu was 4.5x slower and 5x more expensive for that test set. The durable lesson is model routing discipline, not buying another orchestration layer.

Action: Add a cost gate to AI delivery SOPs: use cheaper routing first, require measured quality gain, cap spend, and verify with real task output before any paid orchestration API.

Owner: Codex / Emmanuel

Status: Needs SOP note. No paid API loop.

### 2026-06-23 - Foundation Client Fit Filter

Source: Alex Hormozi - "Same Sales Velocity, But LTV Is 5-10x Higher"

Decision: Adapt

BridgeWorks area: Pricing, Sales Qualification, Foundation Offer

Reason: Higher-value selling requires the full chain to match the buyer: funnel message, case studies, lead magnets, and sales script. BridgeWorks should not pretend to be a large agency, but it should qualify better and say no earlier.

Action: Create a one-page Foundation Client Fit Filter for static-first website clients and scope boundaries.

Owner: Emmanuel / BridgeWorks

Status: Needs template
