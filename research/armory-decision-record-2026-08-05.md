# BridgeWorks Armory — Decision Record
Date: 2026-08-05
Status: **Current.** Supersedes both source reports on every point of conflict.

Supersedes:
- `research/BRIDGEWORKS-GITHUB-AGENCY-ARMORY-2026-08-05.md` (Codex) — banner-marked superseded, author concurring
- `research/github-armory-2026-08-05.md` (Claude) — corrected on four points, see §6
- `research/armory-comparison-2026-08-05.md` — the adjudication that produced this record

---

## 1. Canonical service taxonomy

Verified against the deployed page at `https://bridgeworks.agency/en` on 2026-08-05: all five present once each, HTML-unescaped. Codex concurs after re-check.

1. Strategy & Transformation
2. Digital Platforms & Brand Systems
3. Content, Visibility & Demand
4. AI & Workflow Automation
5. Execution & Operating Systems

`bridgeworks-workspace/CLAUDE.md` has been corrected today. It previously carried a stale list that misled two independent research agents in the same session.

**Verification method, for reuse:**
```bash
curl -s "https://bridgeworks.agency/en?cb=$(date +%s)" \
  | python -c "import sys,html; print(html.unescape(sys.stdin.read()))" \
  | grep -o "Strategy & Transformation\|Digital Platforms & Brand Systems\|Content, Visibility & Demand\|AI & Workflow Automation\|Execution & Operating Systems"
```
Unescape before matching — the page carries `&amp;`, so a naive grep for `AI & Workflow` returns nothing. That escaping is the likely root of the original error.

**Separately:** a packaged-offer layer (outcome-framed names for selling) is a legitimate idea and Codex's five work well as candidates — Lead Response Engine, Search & Trust Sprint, Trust Website System, Qualified Intake System, Client-Owned Operations Stack. They are **not currently deployed**. Shipping them is a positioning decision, not a research finding.

### 1a. Correction — Codex's five were real, and this matters

**Issued 2026-08-05, after this record was first written.** A wider background search (all of `Projects/`, not just the two repos I originally grepped) returned a third file, and git history settled it.

Timeline, verified:

| Date | Event | Evidence |
|---|---|---|
| 2026-06-23 | Codex's five go **live** on the site | commit `1276109` "Reposition homepage: Lead Leak Review, outcome copy, Sprint tier" |
| 2026-07-14 | Replaced by the current five | commit `f1ee7ef` "Site v3: … four service routes …" — confirmed ancestor of `origin/main`, so it shipped |
| 2026-07-24 | `BridgeWorks-Content-Studio/07_Review_And_Approval/SERVICE-CONTENT-REWRITE-REVIEW-2026-07-24.md` states the five are "the customer-facing offers **currently visible** on the BridgeWorks website" | already 10 days stale when written |
| 2026-08-05 | Deployed site carries the current five, zero of Codex's | live `curl`, HTML-unescaped |

**I was wrong.** I wrote that Codex's five were "invented" and appeared "in no git ref, and in no file in this workspace other than its own output." Both claims are false. They were live for three weeks, they exist in git history, and they are written down in a real internal document. My grep covered `bridgeworks-workspace` and `bridgeworks-agency` and missed the sibling `BridgeWorks-Content-Studio` repo. I asserted absence from a search I had not scoped widely enough — the same class of error I criticised.

Codex's own explanation — "stale indexed content" — was closer to correct than my accusation. The substantive conclusion is unchanged: the five are not current, and every priority in §2 stands. But the attribution changes from fabrication to inherited staleness, and that is a materially different fault.

**New hazard identified.** The 2026-07-24 Content Studio file is an active stale-source trap: it asserts site-currency, is wrong, and sits in the content pipeline. It is marked "Do not publish or produce assets from this file" and the Studio is on production HOLD, so the immediate risk is contained — but it is exactly the kind of document a future agent will read and trust. It should carry a dated correction pointing at the current five.

---

## 2. Agreed priority order

Both agents converged on this after correction. Ordered by return, not effort.

| # | Action | Area | Why now |
|---|---|---|---|
| 1 | Build the Strategy & Transformation diligence method | 1 | The one gap both independent reviews found empty. Not a tooling problem. |
| 2 | Build the Lighthouse + accessibility handover gate | 2 | Client-facing artefact. Cheap. Start with Oliviks closeout. |
| 3 | Reconcile and stabilise existing automations | 4 | Blocks everything else. See §3. |
| 4 | Catalogue n8n libraries as references, licence review first | 4 | High value, real licence risk. Do not vendor. |
| 5 | Add GEO **measurement**, not more GEO generation | 3 | Thirteen generation skills already. GEORank fills the missing half. |
| 6 | Relaticle isolated spike — only after the prospecting-tool decision closes | 5 | Do not make an open 3-way decision a 4-way one. |
| 7 | Adopt the ownership and handoff pack immediately | 5 | Best single artefact from either report. Zero cost. |
| 8 | Keep Szamlazz.hu as the only invoicing path | — | Compliance, not preference. |

---

## 3. Blocking dependency

Item 3 gates items 4 and 6. Per `bridgeworks-workspace/CLAUDE.md` (2026-07-22): two Hermes jobs paused on revoked Google OAuth, eight active jobs erroring for mixed and unverified reasons, with an explicit note not to assume one OAuth repair fixes them all.

**Do not stand up new hosted services while existing automations are failing.** This is the substantive operational conclusion both agents reached independently, and it is the reason Codex's original 10-item Phase 1 was withdrawn.

---

## 4. Licence determinations

| Component | Licence | Determination |
|---|---|---|
| **n8n** | Sustainable Use License (not OSS) | **Internal use only.** Grant covers "your own internal business purposes"; providing to others commercially is barred. Running n8n to deliver client work is fine. Deploying it into client infrastructure as a paid deliverable needs a licensing determination or commercial agreement. Also: non-`master` branches unlicensed; `.ee.` files need an enterprise licence. |
| **Invoice Ninja** | — | **Removed.** Conflicts with Szamlazz.hu + NAV auto-submission (`Projects/MEMORY.md:94`, `Projects/HOW-I-WORK.md:13`, both verified). Compliance matter. |
| **AGPL-3.0** (Relaticle, Plane, Documenso, Firecrawl, ToolJet, APITable, Kimai, listmonk, Plausible) | AGPL-3.0 | Self-hosting unmodified is fine. **Modifying** and exposing over a network can trigger §13 source-disclosure. Per-deployment review. Blanket "safe self-hosted" was wrong. |
| **NOASSERTION** (21 of Codex's 51, incl. n8n, Twenty, Astro, Formbricks, Chatwoot, Directus, Metabase, Outline) | none detected | GitHub's `Other` label hides non-standard terms. Read the actual LICENSE file before any client-facing use. |
| **Clean** (MIT / Apache-2.0) | — | Crawl4AI, Lighthouse, shadcn/ui, Next.js, Payload, Gitea, Bruno, mermaid, GEORank, gtm-engineer-skills, geo-optimizer-skill, eGEOagents, VoltAgent, rohitg00 toolkit. |

`enescingoz/awesome-n8n-templates` (24.4k stars) is **NOASSERTION**. Read and extract patterns; do not clone into a commercial operating repo as reusable delivery IP.

---

## 5. Kept from the Codex report

Verified sound and carried forward:

- **The ten-item client ownership and handoff pack** — adopt as standard for every website delivery, starting with Oliviks closeout. Highest-value single item across both reports.
- **Astro as default** for brochure, local-service, editorial, and case-study sites. Next.js + Payload only when portals or application logic justify the operational load.
- **Crawl4AI** (Apache-2.0, 76k stars, active) for audit and competitor crawling.
- **Explicit agent guardrails** — deterministic rules for routing and deadlines; LLM for extraction, summarisation, drafting. Draft/approval mode until the client signs off copy. Never let an LLM silently reject a prospect. Separate provided facts from inferred facts.
- **The internal-agency vs client-owned distinction** — the structural idea worth keeping even though n8n cannot sit on the client-owned side.
- **Monitoring, backup, rollback, documentation, and exit procedures.**
- **The local-SEO negative finding** — no mature OSS replacement for BrightLocal, Whitespark, or Semrush. Build thin around official Google APIs, Search Console, and Lighthouse. Stop shopping.
- **The due-diligence rules**, adopted verbatim as a gate before any tool enters client work.

---

## 6. Kept from the Claude report, with corrections applied

Carried forward:
- n8n template libraries (`enescingoz/awesome-n8n-templates`, `devlikeapro/waha-n8n-templates`) — **as references, licence review first**
- `GEORank` (Apache-2.0) for GEO measurement; `AutoGEO` (ICLR'26) as a proposal citation
- The existing-coverage audit: 13 `geo-*` skills, 15 `market-*` skills — Area 3 is over-served, stop adding
- Public skill/subagent collections: `VoltAgent` (MIT), `rohitg00` toolkit (Apache-2.0)
- Repo-level licence warnings and the stale-repo flags

Corrections applied:
1. **"Clone the n8n libraries today" withdrawn.** Contradicted my own licence warning. Now: review and catalogue, do not vendor.
2. **"AGPL is safe self-hosted" was too broad.** §13 attaches to modified network-accessible versions. Corrected in §4.
3. **Relaticle's 30 MCP tools are a capability, not a verdict.** Not evidence of operational fitness against Twenty, HubSpot, or the current setup.
4. **Marketplace registration downgraded.** A Claude Code configuration choice, not an agency-capability decision. Retained at low priority.

Scope note: the Claude report was a Claude-ecosystem armory plus a repo scan, not the full agency armory requested. Codex's infrastructure breadth is the better half of this merge.

---

## 7. Process finding

Two independent research agents, working the same question the same day, both mapped their findings to a service taxonomy that does not exist on the deployed site. Both were misled in part by a stale `CLAUDE.md`. Both asserted verification they had not performed to the standard claimed.

Four rules from this:

1. **A stale context file is an active hazard, not passive debt.** One wrong line in `CLAUDE.md`, plus a 2026-07-24 Content Studio draft asserting stale site-currency, cost two full research cycles. `CLAUDE.md` is fixed, with the verification command inlined so the next agent can re-check in ten seconds. The Content Studio file still needs the same treatment.
2. **"Verified against X" is a claim to be tested, not a credential.** Stated twice for a list that was three weeks out of date. Only fetching the artefact caught it.
3. **Check the spine before trusting the body.** Codex's 51 repos were all real, none archived, with an accurate `minio` archive warning and correct `cal.diy` naming — strong research resting on a stale frame. Good bodies sit on bad spines more often than the reverse, because the spine is the part nobody re-checks.
4. **Absence claims require scoped searches, and the scope must be stated.** I claimed Codex's five existed "in no file" when I had searched two of at least four relevant repositories, and had not checked git history at all. A negative finding is only as strong as its search boundary. Say the boundary out loud, or do not make the claim — "I did not find X in A and B" is honest; "X does not exist" is a different and much larger assertion.

---

## 8. What is still open

- The Hunter / Tomba / Apollo decision (open since July). Gates item 6.
- Whether to ship the outcome-framed packaged-offer names to the site.
- Per-deployment AGPL review process — who does it, against what checklist.
- The n8n client-deployment licensing determination, if client-owned automation is to be sold at all.
