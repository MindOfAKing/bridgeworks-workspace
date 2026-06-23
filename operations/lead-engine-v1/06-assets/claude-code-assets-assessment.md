# Claude Code Assets Assessment for BridgeWorks Lead Engine v1

Date: 2026-06-23

## What was found

### Claude Code executable

Claude Code is installed through the Claude Desktop package:

```text
C:/Users/User/AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/claude-code/2.1.181/claude.exe
```

Version checked:

```text
2.1.181 (Claude Code)
```

It is not currently on the Git Bash PATH as `claude`, but it can be called by absolute path.

### Global Claude context

Global file found:

```text
C:/Users/User/.claude/CLAUDE.md
```

Useful parts:
- Emmanuel identity and BridgeWorks context
- brand voice rules
- no em dash rule
- brand colors and document standards
- BridgeWorks/Oliviks context

Risky/stale parts:
- says CEEFM is an active client, which conflicts with current Hermes memory and BridgeWorks AGENTS.md saying CEEFM is closed/past case study only
- has heavy session-start/session-end rituals like git pull, commit, push, and Google Sheet updates that should not be copied into the lean Lead Engine workflow

Verdict: keep as historical/context source, but do not treat as current source of truth without checking BridgeWorks AGENTS.md and current Command Center context.

### Claude agents found

Global agents found under:

```text
C:/Users/User/.claude/agents
```

Agent groups:

#### GEO agents
- geo-ai-visibility
- geo-content
- geo-platform-analysis
- geo-schema
- geo-technical

Utility for Lead Engine:
- useful later for client deliverables and AI-search/GEO audits
- useful for Oliviks or website upgrade proof
- too advanced for initial niche/location research

Verdict: park for now. Do not discard.

#### Market audit agents
- market-competitive
- market-content
- market-conversion
- market-strategy
- market-technical

Utility for Lead Engine:
- highly relevant to Lead Leak Reviews
- can be adapted into the audit stage after a prospect is selected
- not ideal for choosing the niche itself unless constrained to quick sampling

Verdict: keep and adapt. These are the strongest Claude assets for the current setup.

### Claude skills found

Useful BridgeWorks sales/delivery skills:

- client-audit
- lead-qualifier
- discovery-call-prep
- post-call-followup
- new-proposal
- monthly-report
- competitive-research
- market-audit
- market-competitors
- market-copy
- market-funnel
- market-landing
- market-report
- market-seo
- geo-prospect

High relevance to Lead Engine:

1. lead-qualifier
2. client-audit
3. discovery-call-prep
4. post-call-followup
5. competitive-research
6. market-competitive
7. market-conversion
8. market-technical
9. market-content
10. market-strategy

Lower immediate relevance:

- content-week
- ad-script
- generate-social-visual
- generate-thumbnail
- youtube analytics/intelligence pipeline
- full GEO report/PDF skills

Keep these for later once the pipeline proves where money is.

## How to use the Claude assets without overbuilding

### Keep the lean Lead Engine as the source of truth

The Lead Engine remains:

1. Prospect tracker
2. Lead scoring rubric
3. Lead Leak Review template
4. Outreach templates
5. Follow-up reminders
6. Weekly review checklist

### Use Claude assets as specialist modules only

Recommended mapping:

| Lead Engine stage | Claude asset to reuse | Role |
|---|---|---|
| Market research | competitive-research, market-competitive | compare niches/competitors |
| Prospect scoring | lead-qualifier | HOT/WARM/COLD logic |
| Lead Leak Review | client-audit + market-conversion + market-technical + market-content | inspect website/contact/trust gaps |
| Discovery call | discovery-call-prep | prepare questions and pain hypotheses |
| After call | post-call-followup | draft follow-up and internal actions |
| Proposal | new-proposal | create offer only after interest exists |
| Delivery | market-audit/GEO agents | use only for paid work or serious opportunities |

## What to discard or archive mentally

Do not use these as first system components:

- full GEO agency CRM
- full marketing audit suite as the default first touch
- automated content production
- YouTube intelligence pipeline for acquisition
- complex agent architecture
- auto-commit/push session rituals
- CEEFM active-client assumptions

## Recommended migration principle

Do not throw the Claude system away. Convert it from a main operating system into a specialist library.

The new hierarchy:

1. Hermes = orchestrator and current operating layer
2. BridgeWorks Lead Engine v1 = source of truth for acquisition pipeline
3. Claude Code assets = specialist templates/agents for audits, conversion analysis, call prep, proposals, and delivery
4. Codex = second opinion or implementation assistant

## Immediate recommendation before market sprint

Create a small `claude-reuse-map.md` or keep this file as the reuse map.

For the sprint, use:

- Hermes subagents for parallel research
- Claude market/competitive concepts as evaluation lenses
- Claude Lead Qualifier logic for scoring
- Claude client-audit/market-conversion logic only after a prospect passes basic fit

Do not run the full Claude marketing audit on every possible prospect. It is too expensive and too heavy for the first pass.
