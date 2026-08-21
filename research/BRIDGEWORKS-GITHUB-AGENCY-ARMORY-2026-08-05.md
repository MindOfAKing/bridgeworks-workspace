> # ⚠ SUPERSEDED — DO NOT ACT ON THIS DOCUMENT AS WRITTEN
>
> **Marked 2026-08-05, at the author's own request, after review.**
>
> The service-area mapping in this document is **out of date** — but it was not invented.
> The five areas below (Lead Follow-Up Systems, Google and AI Search Visibility,
> Trust-Building Websites, Client Intake and Qualification, Digital Infrastructure
> Clients Own) **were genuinely live on bridgeworks.agency from 2026-06-23 to 2026-07-14**
> (added in commit `1276109`, replaced in commit `f1ee7ef`, "Site v3"). They are not
> live today. The "verified against the current website" claim was wrong about
> *currency*, not about *existence*.
>
> **The canonical five are:** Strategy & Transformation · Digital Platforms & Brand
> Systems · Content, Visibility & Demand · AI & Workflow Automation · Execution &
> Operating Systems. Verified against the deployed page 2026-08-05.
>
> **Three specific recommendations below are withdrawn:**
> 1. **n8n as the default client-owned deployment layer.** Its Sustainable Use License
>    permits use "only for your own internal business purposes" and bars providing it to
>    others commercially. Internal use to deliver services is fine; paid client deployment
>    needs a licensing determination.
> 2. **Invoice Ninja.** Conflicts with Szamlazz.hu + NAV auto-submission
>    (`Projects/MEMORY.md:94`, `Projects/HOW-I-WORK.md:13`). Removed entirely.
> 3. **The 10-item Phase 1.** Seven newly hosted services is operationally excessive
>    before existing automation failures are reconciled.
>
> **Still valid and worth keeping:** the ten-item ownership and handoff pack (§5), Astro
> as the default brochure/service-site framework, Crawl4AI, the agent guardrails, the
> internal-infrastructure vs client-owned distinction, and the monitoring/backup/rollback/
> exit procedures.
>
> **Current decision record:** `research/armory-decision-record-2026-08-05.md`

---

# BridgeWorks GitHub Agency Armory

**Date:** 2026-08-05  
**Prepared for:** BridgeWorks  
**Scope:** Repositories, tools, agents, and operating systems mapped to the five live BridgeWorks service areas.

## Executive decision

BridgeWorks does not need one giant platform. It needs a small, composable core that can be handed to clients.

### Recommended BridgeWorks core

| Function | Default | Why it belongs in the core |
|---|---|---|
| Workflow automation | [n8n](https://github.com/n8n-io/n8n) | Strong integration coverage, visual workflows, code escape hatch, self-hosting |
| CRM and pipeline | [Twenty](https://github.com/twentyhq/twenty) | Modern, client-friendly CRM with ownership options |
| Intake | [Formbricks](https://github.com/formbricks/formbricks) | Forms, surveys, and qualification without a closed form platform |
| Scheduling | [Cal.com](https://github.com/calcom/cal.diy) | Client-owned scheduling infrastructure |
| Shared inbox and live chat | [Chatwoot](https://github.com/chatwoot/chatwoot) | Captures website, email, and messaging conversations |
| Notifications | [Novu](https://github.com/novuhq/novu) | One notification layer for email, SMS, chat, and in-app events |
| Website framework | [Astro](https://github.com/withastro/astro) | Fast, content-led service websites with low client lock-in |
| Complex web applications | [Next.js](https://github.com/vercel/next.js) | Use when the project needs application logic or a client portal |
| CMS | [Payload](https://github.com/payloadcms/payload) | Code-owned TypeScript CMS that fits a Next.js delivery stack |
| UI system | [shadcn/ui](https://github.com/shadcn-ui/ui) | Accessible components copied into the client codebase |
| Analytics | [Umami](https://github.com/umami-software/umami) | Simple, privacy-focused, MIT-licensed analytics |
| Technical audit | [Lighthouse](https://github.com/GoogleChrome/lighthouse) | Repeatable performance, accessibility, SEO, and quality checks |
| Web research | [Crawl4AI](https://github.com/unclecode/crawl4ai) | Apache-licensed crawling for audits, competitor research, and AI visibility work |
| Agent runtime | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Lightweight multi-agent workflows with handoffs, tools, and tracing |
| Deployment | [Coolify](https://github.com/coollabsio/coolify) | Client-owned application deployment with less platform lock-in |
| Monitoring | [changedetection.io](https://github.com/dgtlmoon/changedetection.io) plus [Healthchecks](https://github.com/healthchecks/healthchecks) | Page-change and scheduled-job monitoring |
| Backup | [restic](https://github.com/restic/restic) | Encrypted, portable backups across storage providers |
| Delivery management | [Plane](https://github.com/makeplane/plane) | Projects, issues, cycles, and delivery documentation |
| Knowledge and handoff | [Outline](https://github.com/outline/outline) | Client runbooks, SOPs, and searchable operating knowledge |
| Time and profitability | [Kimai](https://github.com/kimai/kimai) | Time, project, and utilization records |
| Proposals and invoices | [Invoice Ninja](https://github.com/invoiceninja/invoiceninja) | Quotes, invoices, projects, and payment records |

This is the default architecture, not an instruction to install everything at once.

## 1. Lead Follow-Up Systems

### Delivery stack

- [n8n](https://github.com/n8n-io/n8n): workflow backbone for form submission, routing, reminders, CRM updates, and escalation.
- [Twenty](https://github.com/twentyhq/twenty): source of truth for contacts, companies, opportunities, stages, and owners.
- [Chatwoot](https://github.com/chatwoot/chatwoot): unified inbox for website chat, email, and supported messaging channels.
- [Novu](https://github.com/novuhq/novu): notification orchestration and templates.
- [Mautic](https://github.com/mautic/mautic): heavier marketing automation for clients that need campaigns, scoring, and nurture logic.
- [listmonk](https://github.com/knadh/listmonk): lean newsletter and bulk-email option when Mautic is excessive.

### Agents

- **Speed-to-Lead Agent:** receives a lead event, enriches it, applies qualification rules, creates or updates the CRM record, drafts the first response, and escalates high-value leads.
- **Follow-Up Watchdog:** checks unanswered leads, stale opportunities, missed appointments, and failed automations.
- **Conversation Summarizer:** converts inbox threads and call notes into structured CRM updates and next actions.

### Standard workflow

`Form or message → n8n → validation and qualification → Twenty → Chatwoot or email response → Cal.com booking → follow-up watchdog`

### Guardrails

- Keep outbound messages in draft or approval mode until the client approves the copy and automation.
- Log consent, source, and unsubscribe status.
- Use deterministic rules for routing and deadlines. Use an LLM for extraction, summarization, and drafting.

## 2. Google and AI Search Visibility

### Delivery stack

- [Lighthouse](https://github.com/GoogleChrome/lighthouse): technical site audits.
- [Crawl4AI](https://github.com/unclecode/crawl4ai): structured site and competitor crawling.
- [Firecrawl](https://github.com/firecrawl/firecrawl): stronger hosted or self-hosted crawl API when scale and extraction features justify AGPL obligations.
- [Google Search Console MCP](https://github.com/surendranb/google-search-console-mcp): lets an agent query Search Console through the official API. Small project. Review code before production use.
- [FlorianBruniaux/google-search-console-mcp](https://github.com/FlorianBruniaux/google-search-console-mcp): broader Search Console, GA4, CrUX, PageSpeed, schema, and IndexNow surface. Small project. Treat as an evaluation candidate.
- [agentic-local-seo-audit](https://github.com/mshahiddigital/agentic-local-seo-audit): useful reference implementation for local SEO audit coverage. Do not adopt without a security and quality review.
- [changedetection.io](https://github.com/dgtlmoon/changedetection.io): competitor-page, offer, schema, and content-change monitoring.
- [SerpApi awesome SEO tools](https://github.com/serpapi/awesome-seo-tools): discovery catalog, not a production component.

### Agents

- **Local Visibility Auditor:** checks Google Business Profile completeness, NAP consistency, review velocity, local schema, map landing pages, and citation gaps.
- **Search Console Analyst:** finds declining queries, pages with high impressions and weak click-through, indexing gaps, and cannibalization.
- **AI Visibility Probe:** runs a fixed prompt set across approved answer engines, records citations and brand mentions, and compares competitors over time.
- **Content Opportunity Agent:** combines Search Console data, competitor pages, customer language, and commercial intent into briefs.
- **Review Operations Agent:** detects new reviews and drafts replies for approval. Google Business Profile API access and client authorization are required.

### Important gap

There is no mature, widely adopted GitHub project that replaces BrightLocal, Whitespark, Semrush, or a properly configured Google Business Profile workflow. BridgeWorks should build its own thin audit layer around official Google APIs and proven crawlers instead of trusting a low-star local SEO repository with client credentials.

## 3. Trust-Building Websites

### Delivery stack

- [Astro](https://github.com/withastro/astro): default for fast service-business and content sites.
- [Next.js](https://github.com/vercel/next.js): use for portals, authenticated applications, personalization, or complex integrations.
- [Payload](https://github.com/payloadcms/payload): default code-owned CMS for the Next.js path.
- [Directus](https://github.com/directus/directus): alternative when the client already has a SQL database or needs a data-first admin system.
- [shadcn/ui](https://github.com/shadcn-ui/ui): owned component source, accessible primitives, and no black-box theme dependency.
- [Lighthouse](https://github.com/GoogleChrome/lighthouse): delivery gate for performance, accessibility, SEO, and best practices.
- [Umami](https://github.com/umami-software/umami): default simple analytics.
- [Plausible](https://github.com/plausible/analytics): privacy-first alternative with AGPL licensing.
- [PostHog](https://github.com/PostHog/posthog): use for session replay, funnels, experiments, and product analytics on complex builds.
- [Sentry](https://github.com/getsentry/sentry): error and performance monitoring where the build contains application logic.

### Agents

- **Website Evidence Agent:** collects testimonials, accreditations, team credentials, case-study evidence, FAQs, and risk-reversal material.
- **Conversion Review Agent:** inspects message clarity, CTA hierarchy, mobile contact paths, forms, trust signals, and analytics events.
- **QA Agent:** runs build, link, accessibility, schema, responsiveness, Lighthouse, and visual checks before handoff.
- **Content Migration Agent:** inventories URLs and assets, maps redirects, converts content, and produces a migration exception report.

### Default build decision

- Use Astro for a brochure, lead-generation, local-service, editorial, or case-study site.
- Use Next.js and Payload only when the functional requirements justify the extra operational load.

## 4. Client Intake and Qualification

### Delivery stack

- [Formbricks](https://github.com/formbricks/formbricks): structured forms, surveys, and branching intake.
- [Cal.com](https://github.com/calcom/cal.diy): qualification-aware scheduling and routing.
- [Twenty](https://github.com/twentyhq/twenty): qualification status and opportunity pipeline.
- [Documenso](https://github.com/documenso/documenso): agreements and signatures.
- [Teable](https://github.com/teableio/teable) or [APITable](https://github.com/apitable/apitable): spreadsheet-like operational records when a full CRM is unnecessary.
- [Budibase](https://github.com/Budibase/budibase) or [ToolJet](https://github.com/ToolJet/ToolJet): custom intake portals, review queues, and internal dashboards.

### Agents

- **Qualification Agent:** converts free-text answers into structured fields, applies an explicit fit score, detects missing answers, and recommends the next route.
- **Discovery Prep Agent:** combines intake, website evidence, CRM history, and market context into a call brief.
- **Proposal Scope Agent:** turns approved discovery facts into a draft scope, assumptions, exclusions, milestones, and open questions.
- **Onboarding Agent:** checks agreement, payment, access, assets, stakeholders, deadlines, and required approvals before delivery starts.

### Guardrails

- Keep the score explainable. Store the rules and the evidence behind every decision.
- Never let an LLM silently reject a prospect.
- Separate prospect-provided facts from inferred facts.

## 5. Digital Infrastructure Clients Own

### Delivery stack

- [Coolify](https://github.com/coollabsio/coolify): primary self-hosting control plane.
- [Dokploy](https://github.com/Dokploy/dokploy): alternative deployment platform to evaluate.
- [Gitea](https://github.com/go-gitea/gitea): client-owned Git, review, registry, and CI/CD when GitHub is not acceptable.
- [restic](https://github.com/restic/restic): encrypted backup policy and restore testing.
- [Healthchecks](https://github.com/healthchecks/healthchecks): cron and workflow heartbeat monitoring.
- [Sentry](https://github.com/getsentry/sentry): application error tracking.
- [Bruno](https://github.com/usebruno/bruno): API collections stored with the project rather than in a closed workspace.
- [Semaphore UI](https://github.com/semaphoreui/semaphore): repeatable infrastructure and maintenance jobs using Ansible or Terraform.
- [LiteLLM](https://github.com/BerriAI/litellm): AI model gateway, budget control, fallbacks, and logging when a client uses multiple model providers.

### Required handoff pack

Every delivery should include:

1. Repository ownership and administrator list.
2. Domain, DNS, email, hosting, database, storage, analytics, and API ownership map.
3. Environment-variable inventory with values kept in an approved secret store.
4. Architecture diagram and data-flow diagram.
5. Deployment and rollback runbook.
6. Backup schedule plus evidence of a restore test.
7. Monitoring, alert recipients, and incident procedure.
8. Vendor and license register.
9. Monthly operating-cost table.
10. Exit procedure that another supplier can follow.

## Agency and consulting operating armory

### Delivery operations

- [Plane](https://github.com/makeplane/plane): projects, tasks, cycles, triage, and delivery records.
- [Outline](https://github.com/outline/outline): SOPs, client knowledge, decision records, and handoff documentation.
- [Kimai](https://github.com/kimai/kimai): time and project-cost evidence.
- [Invoice Ninja](https://github.com/invoiceninja/invoiceninja): proposals, quotes, invoices, and payment records.
- [Metabase](https://github.com/metabase/metabase): internal and client reporting over operational databases.
- [Mermaid](https://github.com/mermaid-js/mermaid): diagrams stored as version-controlled text.

### Consulting agents

- **Prospect Research Agent:** verified company, decision-maker, market, and trigger research.
- **Digital Presence Audit Agent:** website, social proof, reviews, visibility, competitors, and lead-path inspection.
- **Discovery Prep Agent:** hypotheses, evidence, questions, risks, and call plan.
- **Engagement Architect:** converts verified needs into options, deliverables, dependencies, exclusions, and acceptance criteria.
- **Proposal Drafting Agent:** prepares a proposal from approved scope and pricing rules.
- **Project Control Agent:** checks milestones, blockers, approvals, risks, time, and budget.
- **Meeting Intelligence Agent:** produces decisions, owners, deadlines, and CRM or project updates.
- **Client Reporting Agent:** combines delivery evidence and outcome metrics into a concise monthly report.
- **Handoff Agent:** verifies documentation, access, training, backups, ownership, and unresolved risks.
- **Margin Watchdog:** compares scoped effort, actual time, tool costs, change requests, and invoiced value.

## Agent framework bench

| Framework | Best use for BridgeWorks | Decision |
|---|---|---|
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Lean production agents with tools, handoffs, guardrails, and tracing | Default |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Long-running, stateful workflows with checkpoints and human review | Use for complex cases |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Rapid role-based prototypes and research crews | Prototype bench |
| [Microsoft AutoGen](https://github.com/microsoft/autogen) | Multi-agent experimentation and event-driven systems | Research bench |
| [browser-use](https://github.com/browser-use/browser-use) | Browser tasks when no API or reliable connector exists | Controlled fallback |
| [Dify](https://github.com/langgenius/dify) | Visual AI workflow and RAG app delivery | Client-specific option |
| [Flowise](https://github.com/FlowiseAI/Flowise) | Visual agent and RAG prototyping | Prototype bench |
| [LiteLLM](https://github.com/BerriAI/litellm) | Provider abstraction, budgets, routing, and observability | Infrastructure layer |

Do not operate several agent frameworks in production without a client requirement. Standardize BridgeWorks on one default runtime and one workflow engine.

## Recommended packaged offers

### 1. Lead Response Engine

Formbricks, n8n, Twenty, Chatwoot, Cal.com, and a Speed-to-Lead Agent.

**Outcome:** every enquiry is captured, qualified, acknowledged, routed, and followed up.

### 2. Search and Trust Sprint

Crawl4AI, Lighthouse, Search Console integration, structured audit agents, website corrections, schema, evidence, and measurement.

**Outcome:** a prioritized repair plan plus implemented high-impact fixes.

### 3. Trust Website System

Astro or Next.js, Payload where needed, shadcn/ui, Umami, Lighthouse, monitoring, and a complete handoff pack.

**Outcome:** a fast, credible, measurable website the client owns.

### 4. Qualified Intake System

Formbricks, explicit scoring rules, Twenty, Cal.com, Documenso, and qualification and discovery agents.

**Outcome:** unsuitable enquiries are identified early and good prospects reach the right next step.

### 5. Client-Owned Operations Stack

Coolify, GitHub or Gitea, restic, Healthchecks, Outline, diagrams, runbooks, restore tests, and a cost register.

**Outcome:** the client can operate, inspect, transfer, and recover the system without BridgeWorks.

## Adoption sequence

### Phase 1: standardize now

1. n8n
2. Twenty
3. Formbricks
4. Cal.com
5. Astro
6. Umami
7. Lighthouse
8. OpenAI Agents SDK
9. Plane
10. Outline

### Phase 2: add after one paid use case

1. Chatwoot
2. Novu
3. Payload
4. Crawl4AI
5. Coolify
6. Healthchecks
7. restic
8. Documenso
9. Kimai
10. Invoice Ninja

### Phase 3: specialist bench

1. Mautic
2. PostHog
3. Sentry
4. Directus
5. Budibase or ToolJet
6. LangGraph
7. Dify or Flowise
8. LiteLLM
9. Metabase
10. Gitea

## Due-diligence rules

- Check the license at the exact version being deployed. GitHub's `Other` label often means source-available or a non-standard license.
- Review authentication, authorization, secrets handling, dependency health, backup and restore, export capability, audit logs, and upgrade path.
- Pin versions. Test upgrades in staging.
- Do not connect client Google, email, CRM, payment, or messaging credentials to an unreviewed repository.
- Prefer official APIs over browser automation.
- Avoid archived repositories. `minio/minio` was archived when checked and is not recommended for a new default deployment.
- Popularity is not a security review.
- Record recurring infrastructure, email, SMS, AI-model, and maintenance costs before quoting.

## GitHub verification snapshot

All primary candidates above were checked on GitHub on 2026-08-05. The core repositories were active and not archived at the time of review. The Search Console and local SEO candidates are smaller projects and require deeper code review before they receive client credentials.

---

*Prepared by BridgeWorks · office@bridgeworks.agency · bridgeworks.agency*
