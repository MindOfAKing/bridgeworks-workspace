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


### 2026-06-24 - Local Model Routing Economics

Source: Greg Isenberg - "GLM 5.2: Set Up Local AI with Cursor/Codex etc"

Decision: Adopt as internal cost governance

BridgeWorks area: Local AI Ops, Agency Operations, Delivery Verification

Reason: The transcript gives a practical model-routing rule: use stronger models for planning, vision, ambiguity, and review, then route well-scoped execution to cheaper/open models when quality holds. The cost example was 44 cents versus $2.38 for a large task, but the video also warns that hardware is not required to begin.

Action: Create a no-spend Model Routing Trial Sheet before any paid OpenRouter, Z AI, or hardware experiment. Track task type, default model, cheaper candidate, verification method, quality, time saved/lost, and paid cost if any.

Owner: Emmanuel / BridgeWorks

Status: Needs SOP row. No paid API loop or hardware purchase without approval.

### 2026-06-24 - One-Person AI Offer Sprint

Source: Patrick Dang - "How I'd Start a $10K/Month One-Person Business With Claude (Masterclass)"

Decision: Adapt

BridgeWorks area: Sales And Prospecting, Offer Design, Proof And Authority

Reason: The transcript gives a useful order of operations for Emmanuel's current solo reality: define the offer, identify the buyer, set result-based pricing, validate with buyer conversations, then build. The useful lesson is sell-before-build discipline, not the income claims.

Action: Create a BridgeWorks One-Person Offer Sprint checklist with offer triangle, visible pain evidence, proof asset, approval gate, and build-after-signal rule.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist. No outreach without approval.

### 2026-06-24 - Local Social Content Maintenance Guardrail

Source: Jason Wardrop - "How To Run Local Businesses' Social Media In 1 Hour A Week (Charge 497/mo Each)"

Decision: Adapt with constraints

BridgeWorks area: Content And Visibility Systems, Foundation Offer, Client Delivery

Reason: Local businesses do need consistent social presence, but generic AI posts and reused content can damage trust. BridgeWorks should only adapt the workflow as a draft-only maintenance add-on with client facts and approval.

Action: Draft a guarded social maintenance add-on spec: monthly source facts, AI draft generation, client approval, no autopublishing, and paired reporting.

Owner: Emmanuel / BridgeWorks

Status: Needs spec. No vendor commitment or client pitch.

### 2026-06-24 - UX Heuristics Before Visual Polish

Source: Build Great Products - "This skill actually fixes AI slop"

Decision: Adopt as principle / watch tool

BridgeWorks area: Website Production System, Digital Infrastructure, QA

Reason: The strong principle is that AI-generated interfaces should be judged by design heuristics and user decisions, not by pasted style presets. The video is too short to justify adopting an unknown skill.

Action: Add a UX heuristics row to Foundation website and Build Brief QA: hierarchy, next action, consistency, contrast, section purpose, and trust.

Owner: Codex / Emmanuel

Status: Needs QA checklist integration.

### 2026-06-25 - Solo Product Sprint Gate

Source: Build Great Products - "The Secret System I Use to Build & Launch Real Apps in 24 Hours (With Claude Code, Codex or Cursor)"

Decision: Adapt

BridgeWorks area: Build Brief, Digital Infrastructure, Agency Operations

Reason: The useful lesson is not the 24-hour claim. It is the handoff stack for AI builds: validated pain, AI-friendly PRD, roadmap with checkboxes, design.md, build loop, review, verification, and launch checklist.

Action: Create a Solo Product Sprint gate before new BridgeWorks apps, automations, or client-facing tools are built.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist. No external launch without approval.

### 2026-06-25 - BridgeWorks Knowledge Map

Source: Paul J Lipsky - "Build a Self Improving Claude Knowledge Base"

Decision: Adapt internally

BridgeWorks area: Emmanuel OS, Agency Operations, Client Delivery

Reason: BridgeWorks already has source files, YouTube decisions, client notes, and active-work logs. A maintained map would reduce repeated context discovery and connect old decisions to current tasks.

Action: Draft a BridgeWorks knowledge map spec with source-of-truth links, project files, open actions, decisions, client patterns, and guardrails.

Owner: Codex / Emmanuel

Status: Needs spec. No Gmail, Zapier MCP, or private connector expansion.

### 2026-06-25 - Skill Adoption Gate

Source: Matt Wolfe - "9 Free AI Skills That Feel Like Cheat Codes"

Decision: Adapt selectively / watch

BridgeWorks area: AI Growth Systems, Delivery Verification, Competitive Intelligence

Reason: Skills are valuable when they create repeatable behavior. Plugin bundles can also create tool sprawl and data exposure risk, so BridgeWorks needs a gate before installation.

Action: Add a Skill Adoption Gate covering use case, project affected, free/paid status, data risk, rollback path, proof task, and keep/reject decision.

Owner: Emmanuel / BridgeWorks

Status: Needs SOP row. No plugin install in client work without approval.

### 2026-06-27 - Demand-Signal Scout Loop

Source: Vaibhav Sisinty - "Forget Prompt Engineering. Loop Engineering Is the New AI Skill That Replaces It."

Decision: Adapt

BridgeWorks area: Outreach Infrastructure, Competitive Intelligence, AI Growth Systems

Reason: The video gives a useful loop pattern for finding demand signals before they reach the website. The safe BridgeWorks version must watch, score, remember, draft, and stop. It must not send outreach or trigger spend.

Action: Draft a BridgeWorks Demand-Signal Scout Loop spec with approved sources, scoring rules, source-failure reporting, and Emmanuel approval gates.

Owner: Codex / Emmanuel

Status: Needs spec. No outreach automation.

### 2026-06-27 - AI-Native Owner-Operator Positioning

Source: Y Combinator - "India Can Create The Largest AI Companies"

Decision: Adapt as strategic principle

BridgeWorks area: Emmanuel Ehigbai authority layer, BridgeWorks positioning, Build Brief

Reason: The durable lesson is that AI-native execution, learning speed, clarity, taste, agency, and customer insight can let non-Silicon-Valley operators compete. This fits Emmanuel's story only if it stays proof-led and avoids hype.

Action: Draft an AI-native owner-operator positioning note for Emmanuel / BridgeWorks.

Owner: Codex / Emmanuel

Status: Needs note

### 2026-06-27 - Coding Agent Workflow Fit

Source: Jan - "Cursor vs Claude Code vs Codex (I Built the Same App 3 Times)" and GTM coding-agent setup web fallback video

Decision: Adapt

BridgeWorks area: AI Delivery Verification, Website Production System, Cost Governance

Reason: Strong models are not enough. For a solo non-manual coder, the working loop needs PRD, review surface, preview reliability, diff review, model/tool routing, cost cap, and rollback path.

Action: Add a Coding Agent Workflow Fit row to the AI Delivery Verification Checklist and Model Routing Trial Sheet.

Owner: Codex / Emmanuel

Status: Needs checklist row

### 2026-06-28 - AI Visibility Foundation QA

Source: FutureProof / TryFocal - "The Ultimate AI Visibility Checklist (AEO/GEO for 2026)"

Decision: Adapt

BridgeWorks area: GEO / AEO, Foundation website QA, Digital Growth Engine, client reporting

Reason: The transcript maps directly to BridgeWorks' Foundation website and GEO work: crawler access, JavaScript visibility, structured data, direct answers, FAQs, comparison tables, outcome-specific reviews, and external source mentions. The safe BridgeWorks version should be no-spend and proof-based.

Action: Add an AI Visibility Foundation QA row to website production and DGE reporting backlog.

Owner: Codex / Emmanuel

Status: Needs checklist integration. No gray-hat tactics, fake reviews, or ranking guarantees.

### 2026-06-28 - Context Ownership Gate

Source: Vaibhav Sisinty - "Claude's New Update Is Scarier Than You Think (+18 AI Updates)" and Patrick Debois - "Context Is the New Code for AI Agents"

Decision: Adapt

BridgeWorks area: Agency Operations, AI Growth Systems, Delivery Verification, Knowledge Map

Reason: Both transcripts point to the same durable rule: models and tools can change, but BridgeWorks must own its context, source files, workflows, lessons, and verification loops.

Action: Fold a Context Ownership Gate into the BridgeWorks Knowledge Map spec and Skill Adoption Gate: source location, exportability, access boundary, verification, drift control, cost gate, and client-data approval.

Owner: Codex / Emmanuel

Status: Needs SOP row. No paid coworker, Copilot, or private-data connector adoption without approval.

### 2026-06-28 - Root Bottleneck Check

Source: Alex Hormozi - "You Step on the Tail, But You're Looking at the Mouth"

Decision: Adapt

BridgeWorks area: Sales qualification, Foundation offer, client audit previews, scope control

Reason: The transcript gives a useful warning for client diagnostics: visible chaos may be downstream of a commoditized offer, weak sales motion, or insufficient pricing power, not merely a website or automation problem.

Action: Add a Root Bottleneck Check to audit previews: acquisition, conversion, retention, value capture, delivery capacity, and visibility.

Owner: Emmanuel / BridgeWorks

Status: Needs template integration.

### 2026-06-28 - Foundation Mockup-First Sales Loop

Source: `How to Sell Websites to Local Businesses In 2026 (START HERE)`

Decision: Adapt

BridgeWorks area: Foundation offer, local SME prospecting, audit previews, recurring care packaging

Reason: The transcript gives a useful sales order: find visible website gaps, create a small proof asset, ask permission to show it, diagnose business outcomes, and only then discuss pricing or recurring care. The Base44 platform pitch should not override BridgeWorks' static-first Vercel default.

Action: Create a one-page Foundation Mockup-First Sales Loop checklist for approved prospecting and audit previews.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist. No outreach, free full build, or platform switch without approval.

### 2026-06-28 - Local SEO And AI Search Signal Stack

Source: `Local SEO Signals That Actually Get Better SEO Results in 2026!` and `How Ai Search Actually Works (2026) - Understanding Ai Local SEO`

Decision: Adapt

BridgeWorks area: Foundation website QA, GEO / AEO, local SEO, Digital Growth Engine reporting

Reason: The transcripts agree that local AI visibility still depends heavily on Google Business Profile clarity, Google Maps and organic rankings, targeted service/location content, reviews, backlinks, and authority. This keeps BridgeWorks from selling fear-based GEO before fundamentals are fixed.

Action: Add a Local SEO And AI Search Signal Stack row to Foundation Website QA and DGE reporting backlog.

Owner: Emmanuel / BridgeWorks

Status: Needs QA and reporting integration. No fake reviews, paid backlink/citation campaigns, or AI-ranking guarantees.

### 2026-06-28 - AI Subscription Router

Source: `ChatGPT Plus vs SuperGrok in 2026 (Don't Waste Your Money)`

Decision: Adopt as cost guardrail

BridgeWorks area: Finance discipline, AI tool routing, solo operator workflow

Reason: The comparison supports a router, not a new subscription. ChatGPT/Codex remains stronger for Emmanuel's current file, writing, code, knowledge-work, and memory needs. Grok is only a candidate if X trend monitoring or built-in video generation becomes a proven weekly need.

Action: Add an AI Subscription Router row to the Skill Adoption Gate / Model Routing Trial Sheet: job type, existing-tool capability, monthly cost, weekly frequency, data exposure risk, approval, and proof task.

Owner: Emmanuel / BridgeWorks

Status: Needs SOP row. No SuperGrok or paid AI upgrade from this run.

### 2026-06-29 - Core 30 GBP Page Map

Source: `The 30-Page Local SEO Hack Google's AI Is Already Rewarding`

Decision: Adapt

BridgeWorks area: Foundation website QA, local SEO, GEO / AEO, Digital Growth Engine reporting

Reason: The transcript gives a concrete local SEO structure: treat the Google Business Profile as the local money page, then make the website match GBP categories, services, internal links, and buyer intent. This is useful, but BridgeWorks should not turn it into a default 30-page Foundation scope.

Action: Add a proportional Core 30 GBP Page Map row to Foundation QA and DGE reporting backlog.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist integration. No fake local pages, no AI slop location pages, no AI-ranking guarantees.

### 2026-06-29 - AI Agent Worktree Isolation

Source: `Run Multiple AI Agents in Parallel (Claude Code Tutorial)`

Decision: Adopt as delivery guardrail

BridgeWorks area: AI Delivery Verification, Website Production System, Agency Operations

Reason: Parallel agents can speed up AI-assisted delivery only if each agent has isolated files and a separate branch. This reduces collision risk for Codex / Claude Code work and fits Emmanuel's AI-as-build-method reality.

Action: Add an AI Agent Worktree Isolation row to the AI Delivery Verification Checklist and Website Production System.

Owner: Codex / Claude Code after approval

Status: Needs SOP row. No commit, push, broad refactor, or client-work parallelism without approval and rollback.

### 2026-06-29 - Draft-Only Design To Code Loop

Source: `Claude Design 2.0 Just Changed Everything...`

Decision: Adapt with constraints

BridgeWorks area: Foundation website prototypes, brand assets, client review drafts, website production system

Reason: The workflow can shorten draft visual exploration by moving from brand context to editable mockup to code handoff. The risks are paid APIs, unknown repos, unreliable handoff, and over-polishing instead of shipping.

Action: Add a Draft-Only Design To Code Loop note to the Website Production System backlog, linked to the existing `design.md` action.

Owner: Emmanuel / BridgeWorks

Status: Watch / Needs backlog note. No paid API spend, repo install, public sharing, or client-facing mockup without approval.

### 2026-06-29 - Guarded CRM Reactivation Audit

Source: `How To Find 50K Hidden In Any Local Business's CRM (Charge 5K Per Job)`

Decision: Adapt with constraints

BridgeWorks area: Sales and prospecting, AI Growth Systems, audit previews, client delivery

Reason: The transcript gives a concrete local-business diagnostic: old leads, missed calls, and stale CRM contacts may hold recoverable demand. BridgeWorks should adapt this as an audit and approval-gated recovery sprint, not as unsupervised SMS outreach.

Action: Add a Guarded CRM Reactivation Audit checklist covering consent, opt-outs, data source, value per appointment, owner approval, stop-on-response, manual handoff, and paired reporting.

Owner: Emmanuel / BridgeWorks

Status: Needs checklist. No SMS, WhatsApp, email, client contact, CRM access, or campaign execution without approval.

### 2026-06-29 - Multi-Lens Research Brief

Source: `Stanford's Method Turns Claude Into a PHD Level Research Team`

Decision: Adapt

BridgeWorks area: Competitive intelligence, audit previews, offer validation, proof and authority

Reason: The transcript provides a practical research workflow: multiple lenses, contradiction mapping, synthesis, and source verification. This fits BridgeWorks where claims must be accurate before they become audit findings, case-study language, or client-facing strategy.

Action: Add a Multi-Lens Research Brief SOP row using operator, buyer, skeptic, finance, and market-context lenses, followed by confirmed / corrected / demoted source labels.

Owner: Emmanuel / BridgeWorks

Status: Needs SOP row. No external skill install or paid agent loop from this run.

### 2026-06-29 - Search Everywhere Visibility Map

Source: `SEO Is Bigger Than Google Now. Here's the New Playbook`

Decision: Adapt

BridgeWorks area: Foundation website QA, local SEO, GEO / AEO, Digital Growth Engine reporting

Reason: The transcript reframes SEO as search-everywhere optimization. Traditional search, GBP, local packs, third-party profiles, reviews, social platforms, and AI citations now interact. BridgeWorks should turn this into a clear visibility map, not AI-ranking hype.

Action: Add a Search Everywhere Visibility Map template covering website clarity, GBP fit, local pack, AI answer presence, citation sources, third-party profiles, reviews, and proof gaps.

Owner: Emmanuel / BridgeWorks

Status: Needs template. No fake reviews, spam profiles, paid citation campaigns, or AI-ranking guarantees.
