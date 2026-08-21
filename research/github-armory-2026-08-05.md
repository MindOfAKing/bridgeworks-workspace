> # ⚠ SOURCE RESEARCH — NOT OPERATING GUIDANCE
>
> **Marked 2026-08-05.** Superseded by `research/armory-decision-record-2026-08-05.md`.
> Retained as an input record. Three errors below are corrected there:
>
> 1. **"Clone the n8n libraries today"** (§What to actually do, item 1) is **withdrawn.**
>    `enescingoz/awesome-n8n-templates` is NOASSERTION — no declared licence grant. This
>    contradicted this document's own licence-warnings section. Correct action: review and
>    catalogue as references; do not vendor into a commercial operating repo.
> 2. **"AGPL is safe to self-host"** is **too broad.** AGPL-3.0 §13 attaches source-disclosure
>    obligations to *modified* network-accessible deployments. Per-deployment review required.
> 3. **The service-area sourcing line** — "Taken from live site copy,
>    `bridgeworks-agency/src/messages/en.json`" — conflated a working-tree file with the
>    deployed site. That file was dirty and the repo 6 commits behind. The five names happened
>    to be correct, confirmed later against the deployed page, but the method was not sound.
>
> Also: Relaticle's 30 MCP tools are a capability, not evidence of operational fitness.
> The marketplace-registration item is a Claude Code configuration choice, not an
> agency-capability decision, and is ranked too highly here.

---

# BridgeWorks GitHub Armory
Researched: 2026-08-05
Method: live `gh search repos` + `gh api` verification. Every repo below was checked for star count, last push date, and licence on 2026-08-05. Nothing here is recalled from memory.

---

## The five service areas (source of truth)

Taken from live site copy, `bridgeworks-agency/src/messages/en.json` → `routes.items`. Note this does **not** match the five services listed in `bridgeworks-workspace/CLAUDE.md` (Digital Growth Strategy / AI-Powered Marketing / Brand Identity / Web Design & Development / AI Business Automation). The site is newer. CLAUDE.md is stale and should be corrected.

1. Strategy & Transformation
2. Digital Platforms & Brand Systems
3. Content, Visibility & Demand
4. AI & Workflow Automation
5. Execution & Operating Systems

---

## Headline finding

The armory is not thin. It is unregistered.

`~/.claude/plugins/installed_plugins.json` shows **four** plugins installed at user level (superpowers, code-simplifier, context7, code-review) and **one** marketplace registered (`anthropics/claude-plugins-official`). The session exposes far more plugin skills than that, so the rest are app-managed rather than repo-pinned. Either way, no third-party marketplace is registered locally, which means none of the community skill collections below are reachable from a fresh Claude Code session.

Second finding: coverage is lopsided. Area 3 (Content, Visibility & Demand) is already over-served — 13 in-house `geo-*` skills, 15 `market-*` skills, the searchfit-seo plugin, brightdata, Ahrefs MCP. Area 1 (Strategy) and Area 5 (Execution) have almost no tooling behind them, in-house or third-party. That is the real gap, and it is the gap that costs money, because strategy and execution are where the retainer lives.

---

## Area 1 — Strategy & Transformation

Weakest OSS coverage of the five. Consulting frameworks do not package well as repos; searches for "consulting frameworks llm" and "business intelligence agent research" returned nothing usable.

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [dzhng/deep-research](https://github.com/dzhng/deep-research) | 19,480 | 2026-04-11 | MIT | Iterative depth+breadth research loop. The reference implementation everyone forked. Closest thing to a diligence engine for pre-pitch work. |
| [Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) | 19,786 | — | — | Heavier, model-side. Reference only unless self-hosting. |
| [SkyworkAI/DeepResearchAgent](https://github.com/SkyworkAI/DeepResearchAgent) | 3,506 | — | — | Hierarchical multi-agent. Architecture to borrow, not to run. |

**Verdict:** build, don't install. The `/client-audit` and `/discovery-call-prep` skills already exist; what is missing is a market/sector diligence skill that runs before a strategy engagement. Borrow the depth-then-breadth loop from `dzhng/deep-research` and wire it to the Ahrefs and Bright Data MCPs already connected.

---

## Area 2 — Digital Platforms & Brand Systems

Already well covered in-session (figma plugin, `design:*` skills, `frontend-design`, `impeccable`, base44). The gap is verification, not creation: nothing currently proves a delivered site is accessible and fast before handover.

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [addyosmani/a11y](https://github.com/addyosmani/a11y) | 1,721 | — | — | Accessibility audit tooling for the web. Turns "we built it well" into a number on a handover doc. |
| [amankumarrr/lighthouse-insights-action](https://github.com/amankumarrr/lighthouse-insights-action) | 0 | — | — | GitHub Action, Lighthouse CI with PR vs production comparison. Low stars, read the source before trusting it. |

**Verdict:** one gap worth closing. A pre-handover gate that runs Lighthouse + axe against the staging URL and emits a scorecard. This is a client-facing artefact, not just hygiene — Oliviks and CEEFM handovers would both have been stronger with it. Build it as a skill; the OSS here is thin enough that installing is not worth it.

---

## Area 3 — Content, Visibility & Demand

Best OSS availability of the five, and the area where BridgeWorks is already strongest. Recommend selectively — most of this duplicates existing `geo-*` skills.

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [onvoyage-ai/gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills) | 1,286 | 2026-06-07 | MIT | The most-starred AEO/GEO Claude Code skill. Direct peer to the in-house `geo-*` suite. Read it as a benchmark: what does a 1.2k-star GEO skill do that ours does not? |
| [Auriti-Labs/geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill) | 644 | 2026-07-20 | MIT | Active AEO/GEO toolkit. Second opinion on scoring methodology. |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | 110 | 2026-06-25 | MIT | Vendor-built (SE Ranking) production skills — content briefs etc. Useful as a structure reference even without their MCP. |
| [amplifying-ai/awesome-generative-engine-optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization) | 470 | 2026-04-14 | none | Curated GEO guides, tools, research. Reading list. |
| [mverab/eGEOagents](https://github.com/mverab/eGEOagents) | 148 | 2026-08-05 | MIT | Pushed today. GEO/AEO agent toolkit, actively moving. |
| [yaojingang/GEORank](https://github.com/yaojingang/GEORank) | 364 | 2026-07-30 | Apache-2.0 | GEO *ranking* platform — measurement, not optimisation. Fills a real hole: proving movement to a client. |
| [cxcscmu/AutoGEO](https://github.com/cxcscmu/AutoGEO) | 193 | — | — | ICLR'26 paper + framework. Cite it in proposals; the academic backing is a sales asset. |
| [ai-search-guru/getcito...](https://github.com/ai-search-guru/getcito-worlds-first-open-source-aio-aeo-or-geo-tool) | 154 | 2026-08-03 | MIT | Open-source AIO/AEO tool. Overclaimed name, active repo. |
| [AgriciDaniel/seo-os](https://github.com/AgriciDaniel/seo-os) | 97 | 2026-06-29 | AGPL-3.0 | Local-first SEO agency operating system. Closest published thing to what BridgeWorks runs. AGPL — do not embed in client deliverables. |

**Verdict:** do not install more GEO skills, you have thirteen. Take two things: `GEORank` for the measurement gap (the `/geo-compare` skill tracks deltas but there is no independent ranking signal), and `AutoGEO` as a citation in proposals.

---

## Area 4 — AI & Workflow Automation

Highest immediate leverage. n8n is already the stated automation stack, and there are large, current template libraries that map straight onto client work.

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [enescingoz/awesome-n8n-templates](https://github.com/enescingoz/awesome-n8n-templates) | 24,448 | 2026-07-23 | NOASSERTION | 280+ ready workflows: Gmail, Telegram, Slack, Discord. The single biggest time-saver on this list. Licence is non-standard — check before reselling a workflow to a client. |
| [lucaswalter/n8n-ai-automations](https://github.com/lucaswalter/n8n-ai-automations) | 1,580 | 2026-03-02 | none | AI-agent-flavoured n8n workflows from The Recap. No licence declared: treat as reference, not redistributable. |
| [Marvomatic/n8n-templates](https://github.com/Marvomatic/n8n-templates) | 1,532 | **2025-11-26** | none | SEO and content-optimisation workflows. **Stale by ~8 months** — n8n node APIs will have drifted. Mine for patterns, expect to repair. |
| [zengfr/n8n-workflow-all-templates](https://github.com/zengfr/n8n-workflow-all-templates) | 103 | — | — | Claims 10,258+ workflows, synchronised. Volume over curation. |
| [devlikeapro/waha-n8n-templates](https://github.com/devlikeapro/waha-n8n-templates) | 183 | — | — | WhatsApp HTTP API templates. Directly relevant — Oliviks already routes ordering through WhatsApp. |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 91,841 | 2026-08-03 | MIT | The canonical MCP directory. Use it to close connector gaps rather than building integrations. |

**Verdict:** clone `enescingoz/awesome-n8n-templates` and `devlikeapro/waha-n8n-templates` this week. The WAHA templates in particular are a shortcut for the WhatsApp infrastructure pattern already sold to Oliviks and reusable across every hospitality prospect.

---

## Area 5 — Execution & Operating Systems

Currently run on Google Sheets (Emmanuel OS) plus Notion. That works at one client. It does not work at five.

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [relaticle/relaticle](https://github.com/relaticle/relaticle) | 1,486 | 2026-08-04 | AGPL-3.0 | Open-source CRM with **native AI agent support — 30 MCP tools**, REST API, self-hosted, Laravel. The only CRM here built for agent operation. AGPL: fine self-hosted, a problem if resold. |
| [frappe/crm](https://github.com/frappe/crm) | 3,165 | 2026-08-05 | AGPL-3.0 | Fully featured, actively developed (pushed today). Safe, boring, complete. |
| [espocrm/espocrm](https://github.com/espocrm/espocrm) | 3,191 | 2026-08-04 | AGPL-3.0 | Mature, stable, well documented. |
| [SuiteCRM/SuiteCRM](https://github.com/SuiteCRM/SuiteCRM) | 5,626 | — | — | Most stars, heaviest, oldest architecture. |

**Verdict:** `relaticle` is the interesting one and the only one that fits how BridgeWorks actually works — an agent-operated CRM with MCP tools means Claude Code can read and write pipeline directly instead of going through the Sheets script. Worth a spike. Caveat: AGPL-3.0, and the "Hunter/Tomba/Apollo — pick one" loop is still open. Do not add a CRM before closing that loop.

---

## Cross-cutting: skill and agent collections

| Repo | Stars | Last push | Licence | Why it matters |
|---|---|---|---|---|
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 51,683 | 2026-08-05 | NOASSERTION | The main index. Updated today. |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 24,027 | 2026-07-31 | MIT | 100+ subagents, actively maintained, MIT. Best single source for agent patterns. |
| [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | 2,445 | 2026-05-12 | Apache-2.0 | 135 agents, 35 skills, 42 commands in one Apache-2.0 package. Cleanest licence for commercial adaptation. |
| [asgard-ai-platform/skills](https://github.com/asgard-ai-platform/skills) | 223 | 2026-06-06 | MIT | 301 skills across 22 domains, framed around methodology and judgment rather than code snippets. |
| [0xfurai/claude-code-subagents](https://github.com/0xfurai/claude-code-subagents) | 976 | **2025-10-15** | MIT | 100+ dev subagents. Stale by ~10 months. |
| [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) | 895 | **2025-10-14** | Apache-2.0 | Curated plugin list. Stale by ~10 months — the plugin ecosystem moved a lot since. |

These are dev-engineering biased. There is no mature *agency/consulting* skill marketplace on GitHub. The in-house `market-*` + `geo-*` suite is, as far as this search goes, ahead of what is public.

---

## What to actually do

Ordered by return, not by effort.

1. **Clone the n8n libraries.** `enescingoz/awesome-n8n-templates` and `devlikeapro/waha-n8n-templates`. Directly reusable in Area 4 client work. Today.
2. **Register a third-party marketplace.** Only `anthropics/claude-plugins-official` is known locally. Add `rohitg00/awesome-claude-code-toolkit` (Apache-2.0, commercially clean) and pull selectively.
3. **Fix the CLAUDE.md service list.** It contradicts the live site. Any agent reading it pitches the wrong five services.
4. **Build the handover gate (Area 2).** Lighthouse + axe scorecard before every site handover. Client-facing artefact, not just hygiene.
5. **Build a diligence skill (Area 1).** Borrow the loop from `dzhng/deep-research`, wire to Ahrefs + Bright Data MCPs already connected.
6. **Spike relaticle (Area 5).** Agent-native CRM. But close the Hunter/Tomba/Apollo loop first.
7. **Do not add GEO skills.** Thirteen is enough. Take `GEORank` for measurement and `AutoGEO` as a proposal citation, nothing else.

## Licence warnings

- AGPL-3.0 (`relaticle`, `frappe/crm`, `espocrm`, `seo-os`): safe to self-host, dangerous to embed in a client deliverable without legal review.
- NOASSERTION / none (`enescingoz`, `lucaswalter`, `Marvomatic`, `amplifying-ai`, `hesreallyhim`): no declared grant. Fine to learn from. Check before selling a derivative to a client.
- MIT / Apache-2.0 is the clean set: `gtm-engineer-skills`, `geo-optimizer-skill`, `seo-skills`, `eGEOagents`, `GEORank`, `getcito`, `punkpeye/awesome-mcp-servers`, `VoltAgent`, `rohitg00`, `asgard-ai-platform`, `dzhng/deep-research`.

## Stale — verify before relying on

`Marvomatic/n8n-templates` (2025-11-26) · `0xfurai/claude-code-subagents` (2025-10-15) · `ccplugins/awesome-claude-code-plugins` (2025-10-14)
