# BridgeWorks Workspace - Consulting Operations

## Project Overview
BridgeWorks is an AI-Powered Digital Growth Studio serving small businesses across Africa and Central Europe. Services: Digital Growth Strategy, AI-Powered Marketing, Brand Identity, Web Design & Development, AI Business Automation. Operating model: solo founder + AI skills stack, with paid engagements tracked per client.

## Active Clients
- **Oliviks**: Foundation engagement (Foundation-only scope per contract dated 29 April 2026). Website rebuild + Google Business Profile optimization + email/WhatsApp infrastructure. Total fee 272,611 HUF. Deposit 136,306 HUF paid June 2026; balance 136,305 HUF due on handover (end of week 3 from kickoff). Deposit invoice EO-2026-11 sent 6 June. Photos received (Hanna Mühl shoot, Drive folders forwarded 7 June). Kickoff still blocked on: working WP admin account, GBP manager access, WhatsApp number, first-subscriber incentive. Contact: Aese Agaigbe, olivikskitchen@gmail.com (also agaigbeaese@gmail.com). Client folder: `clients/oliviks/`

## Past Clients
- **CEEFM Kft**: 16-week digital growth engagement, late March to June 2026. Contract terminated June 2026. Final GEO score 77/100 at the 2026-06-10 audit (from 16); 78 on 2026-06-11 after post-handover fixes; source of truth: `clients/ceefm/VERIFIED-FACTS.md`. Contract was 16 weeks, terminated by client at week 9; public phrasing is "engagement, March to June 2026", never "16-week" or "completed". Case study: named use approved 2026-07-14 for bridgeworks.agency; client-sensitive internals stay private.

## What Lives Here
- `clients/` - Client-specific folders with deliverables, trackers, case studies
- `pipeline/` - Sales pipeline and lead tracking
- `knowledge/` - Research and reference materials
- `documents/` - Proposals, agreements, reports
- `scripts/` - Automation scripts
- `sessions/` - Session logs
- `skills-drafts/` - Skills in development

## Brand Rules
- No em dashes. No AI slop. Short sentences. Specific over general.
- See business-brain for full brand system.

## Pricing Reference
- Full rate card and pricing rules: `C:/Users/ELITEX21012G2/Projects/business-brain/context/finances.md`
- Rule: Never discount without reducing scope. Lead with bundles. NGN rates are not discounts.

## Sibling Locations
| Location | Purpose |
|----------|---------|
| `C:/Users/ELITEX21012G2/Projects/business-brain/` | Central business context and orchestration |
| `C:/Users/ELITEX21012G2/bridgeworks-agency/` | Live website (React/Vercel) |
| `C:/Users/ELITEX21012G2/Projects/personal-brand-workspace/` | Emmanuel personal brand |
| `C:/Users/ELITEX21012G2/Projects/mindofaking-workspace/` | MindOfAKing creative brand |
| `C:/Users/ELITEX21012G2/Projects/brand-assets/` | Original brand asset library |

## Key References
- Business brain: `C:/Users/ELITEX21012G2/Projects/business-brain/CLAUDE.md`
- Brand guide: `C:/Users/ELITEX21012G2/Projects/business-brain/context/brand/bridgeworks/`
- Playbooks: `C:/Users/ELITEX21012G2/Projects/business-brain/context/playbooks/`
- Global instructions: `C:/Users/ELITEX21012G2/.claude/CLAUDE.md`

## Working agreement

Behavioral rules for this workspace come from the global Working Agreement at `C:/Users/ELITEX21012G2/.claude/CLAUDE.md`. This file only holds BridgeWorks-specific context.

---

## Live operating state

This section is the single source of truth for what's active and what this week needs to produce. I update it at end of day in under 5 minutes. Any chat that contradicts this section is working from stale context — say so, do not work around it.

**Last updated:** 2026-06-10

### Ventures — active this month

| Venture | Status | This month's work |
|---|---|---|
| Bridgeworks (agency) | Active — primary focus | Backend buildout to run as a fully-formed agency; lead generation |
| Oliviks (paid client) | Active — deposit paid, awaiting client access to start kickoff clock | Collect access pack, then 3-week Foundation delivery (GBP + email/WhatsApp wk 2, website wk 3) |
| CEEFM (closed client) | Terminated June 2026 | Finalize and send handover doc, then archive |
| Street Kitchen (EV income, not Bridgeworks) | Active — recurring | Monthly cleaning contract; no new effort needed |
| emmanuelehigbai.com | Active — priority build | Build and launch this month; feeds Bridgeworks credibility |
| Build Brief (multilayer prompt builder) | Active — lives on Claude for now | Positioning question deferred (personal tool vs service offering) |

### Ventures — parked (revisit when Bridgeworks is stable)

DanubeGold Agri · VeriCrop · MindOfAKing build work · JHU Agentic AI program · the older "AI competitive intelligence platform" positioning in `bridgeworks-workspace/CLAUDE.md`.

Nothing is killed. No work happens on these until Bridgeworks is stable. If a chat tries to revive any of them before then, point it at this file.

### Open loops — decisions this week

| Loop | Decision | By |
|---|---|---|
| Stripe | Finish live setup OR archive until a signed proposal needs it | Friday |
| Hunter + Tomba + Apollo (three overlapping prospecting tools) | Pick one; kill the other two. Default: keep Apollo | Friday |
| Blotato | Continue or cancel — nothing publishing through it yet | End of month |
| CEEFM React dashboard artifact (1,158-line JSX) | Archive as sales demo, absorb into bridgeworks-workspace, or delete | End of week |
| Old BridgeWorks repo CLAUDE.md positioning | Rewrite to match agency positioning | Before next Claude Code session on that repo |
| CEEFM handover doc | Review draft, fix internal score inconsistency, send to Victor | This week |
| Oliviks access pack | Photos received (Hanna Mühl shoot, Drive links forwarded 7 June). WP login link forwarded 30 May but expired; need real admin account. Still missing: GBP manager access, WhatsApp number, first-subscriber incentive | This week |

### This week — single best close

**Backend setup to launch Bridgeworks as a running agency.** Definition of done (all four true):

1. A contact form submission on bridgeworks.agency arrives somewhere I see within 5 minutes
2. I can go from signed proposal to invoice in under 10 minutes
3. One screen shows: inbound pipeline, active client status, today's work
4. emmanuelehigbai.com is live OR has a confirmed build start date within 7 days

Nothing gets built this week that doesn't serve one of those four.

### Daily catcher (5 min, end of day)

Append to the log below. Never delete history.

```
### YYYY-MM-DD
- Closed: [what got done today]
- Opened: [what got started that now belongs to a loop, or is a new loop]
- Tomorrow's one: [the single most important move for tomorrow]
```

Friday review: revisit "This week's single best close" — did the four items move?

### Daily log

<!-- Append entries here. Most recent at top. -->

### 2026-06-10
- Closed: New machine migration audit (9 connectors, plugins, Vercel, Notion all verified working); CEEFM closed out in CLAUDE.md and Notion Pipeline CRM
- Opened: CEEFM handover doc, finalize and send to Victor. Oliviks engagement live, half deposit paid, scope and deal value need recording. Scheduled tasks and artifacts wiped by migration, rebuild list needed.
- Tomorrow's one: review and send CEEFM handover doc

### 2026-04-23
- Closed: CLAUDE.md rollout across 5 repos + global + Drive reference; Bridgeworks Financial Tracker uploaded to 05 - Finance & Admin; BridgeWorks repo positioning aligned with live site
- Opened: (none)
- Tomorrow's one: backend setup work — pick one of the four DoD items and close it
