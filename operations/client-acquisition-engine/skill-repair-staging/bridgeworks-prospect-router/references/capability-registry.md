# Prospecting Capability Registry

Verified for the BridgeWorks Codex environment on 2026-08-01. Recheck connector state before external execution.

## Active production capabilities

| Need | Capability | Use |
|---|---|---|
| Broad digital evidence | `client-audit` | Website, social, visibility, competitor, and marketing-gap evidence |
| Marketing diagnosis | `market-audit` and focused `market-*` skills | Use a focused specialist for initial contact; reserve the full audit for justified cases |
| Competitor context | `market-competitors` | Positioning and proof comparison |
| Conversion path | `market-funnel`, `market-landing`, `market-copy` | Annotated customer-journey or page recommendation |
| Search plan | `market-seo` | Bounded SEO evidence and priorities |
| Brand interpretation | `market-brand` | Positioning and voice evidence |
| Discovery prep | `discovery-call-prep` | Only after a conversation is scheduled |
| Scope control | `engagement-architect` | Only after discovery evidence exists |
| Branded document | `documents`, `docx`, `pdf` | Package verified findings using BridgeWorks brand constants |
| Prospect qualification | staged `bridgeworks-lead-qualifier` | Required before routing |
| Bounded GEO proof | `bridgeworks-geo-prospect-scan` | One public-evidence AI-search snapshot, three actions, one demonstration |
| Bounded revenue-system proof | `bridgeworks-revenue-system-scan` | One public-evidence lifecycle, ownership, CRM, or reporting hypothesis |
| Bounded AI-workflow proof | `bridgeworks-ai-workflow-scan` | One evidence-backed workflow candidate and synthetic human-reviewed demo |

## Capabilities found but not yet active

Do not invoke these until they are migrated, validated, and present in the active skill estate:

- Full GEO delivery: `geo-audit`, `geo-citability`, `geo-crawlers`, `geo-llmstxt`, `geo-schema`, `geo-technical`, `geo-content`, `geo-brand-mentions`, `geo-platform-optimizer`, `geo-compare`, `geo-report`, `geo-report-pdf`. Use the active bounded prospect scan for initial outreach; migrate the full suite only for paid delivery.
- Legacy revenue systems: `revops`. Use the active `bridgeworks-revenue-system-scan` for initial outreach.
- Demand-source programs: `referrals`, `lead-magnets`, `gsc-opportunity`.
- Department pointers: `prospecting-department`, `client-ops-department`, `content-department`, `design-department`.

Their presence under `.claude`, plugin source, or exports does not make them callable in the active Codex skill estate.

## Known broken or stale capabilities

- Active `market-report-pdf` points to a missing `scripts/generate_pdf_report.py`; use the verified shared Markdown-to-PDF renderer or the active PDF/document skills until repaired.
- Legacy `lead-qualifier` variants contain stale Budapest/CEE/Nigeria bias, hard-coded pricing, and default-free-audit logic. Do not use them.
- Legacy `geo-prospect` writes a separate JSON CRM. Do not use it as operational truth.
- Legacy `geo-proposal` contains hard-coded prices and unsupported market/ROI claims. Do not use it at initial contact.

## Connected tools

| Tool | Current safe use | Constraint |
|---|---|---|
| Web and browser | Public research and page verification | Cite evidence and date it |
| HubSpot | Read company/contact/deal context | Writes currently require reauthorization and approval |
| ClickUp | Read execution context | Confirm write capability before creating tasks |
| Gmail | Search context and prepare drafts | Sending requires explicit approval |
| LinkedIn through Composio | Read Emmanuel's profile and owned activity | No prospect DM, connection, or follow action is exposed |
| Controlled browser | Manual LinkedIn and website interaction | Use only with explicit approval for external actions |
| Apollo | Enrichment after qualification | Credits and plan limits; approval before spend |
| Google Maps toolkit | Potential local discovery | No active connection verified |

## Work-pass routing

Use sequential specialist passes by default. Use parallel agents only when Emmanuel explicitly requests agent or parallel work.

- `strategy-transformation`: market/competitor evidence, strategic synthesis, executive QA.
- `digital-platforms-brand`: client audit, conversion/brand specialist, visual concept, executive QA.
- `content-visibility-demand`: `bridgeworks-geo-prospect-scan` or focused SEO evidence, competitor evidence, opportunity synthesis, executive QA.
- `ai-workflow-automation`: `bridgeworks-ai-workflow-scan`, public journey evidence, synthetic future-state map, executive QA.
- `execution-operating-systems`: `bridgeworks-revenue-system-scan`, public process evidence, operating map, executive QA.
