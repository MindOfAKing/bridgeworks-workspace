# Armory research: Claude vs Codex, adjudicated
Date: 2026-08-05
Revision 2: adds Codex's rebuttal, the deployed-site test that settles it, and corrections Codex was right about.
Purpose: reconcile two independent GitHub armory reports. Every factual claim below was re-verified with `gh api` and a live fetch of bridgeworks.agency/en on 2026-08-05.

Inputs:
- `research/github-armory-2026-08-05.md` (Claude)
- `research/BRIDGEWORKS-GITHUB-AGENCY-ARMORY-2026-08-05.md` (Codex)

---

## Verdict in one line

Codex's repo research is excellent and its licence discipline is better than mine. Its service mapping is invented, and it claimed to have verified it against the website. Use the stack, throw away the spine.

---

## 1. The service areas — Codex is wrong, and the error is a verification failure

Codex's report is built on these five:

1. Lead Follow-Up Systems
2. Google and AI Search Visibility
3. Trust-Building Websites
4. Client Intake and Qualification
5. Digital Infrastructure Clients Own

I fetched `https://bridgeworks.agency/en` live. The page returns, verbatim:

1. Strategy & Transformation
2. Digital Platforms & Brand Systems
3. Content, Visibility & Demand
4. AI & Workflow Automation
5. Execution & Operating Systems

This matches `bridgeworks-agency/src/messages/en.json` → `routes.items` exactly.

I then grepped both `bridgeworks-workspace` and `bridgeworks-agency` for Codex's five names. **The only file in either repo containing them is Codex's own output.** They are not from a stale doc, an ICP file, or an older site version. They were invented.

Codex's summary states: *"The service mapping was verified against the current BridgeWorks website."* That claim is false. This is worse than being wrong, because it is the specific claim that would stop a reader from checking.

### What the mismapping costs

| Live service area | Codex coverage |
|---|---|
| Strategy & Transformation | **None.** No tooling, no agents, no offer. Entirely absent. |
| Digital Platforms & Brand Systems | Good — Astro/Next/Payload/shadcn/Lighthouse |
| Content, Visibility & Demand | Good, narrowed to search visibility only. No content production or demand generation. |
| AI & Workflow Automation | Good — n8n plus the agent bench |
| Execution & Operating Systems | Partial — infrastructure and handoff covered, delivery management thin |

Codex invented "Client Intake and Qualification" as a standalone area and spent a full section on it. Intake is a component of Strategy and Execution, not a service line — it is not something BridgeWorks sells by name.

Both reports independently produced good coverage of the middle three and near-nothing for Strategy & Transformation. That agreement is the finding: **Strategy is the real hole, and no amount of GitHub will fill it.** It is a methodology and judgment gap, not a tooling gap.

---

## 2. Where Codex beat me

I verified all 51 repos Codex cited. **All 51 exist. None are archived. Zero hallucinations.** That is a better hit rate than I expected and better than most research of this kind.

Specific points where Codex was right and I would have been wrong:

- **`minio/minio` is archived.** Codex flagged it unprompted in its due-diligence rules. Confirmed: `archived=true`, last push 2026-04-24. Precise and correct.
- **`calcom/cal.diy` is the current canonical name.** I assumed this was a typo for `cal.com` and checked. `calcom/cal.com` redirects to `calcom/cal.diy`. Codex had the current name; my assumption was the error.
- **Proportionate caution on small repos.** Codex flagged `surendranb/google-search-console-mcp` and `FlorianBruniaux/google-search-console-mcp` as small and needing code review before receiving credentials. Verified: 37 and 8 stars respectively. `mshahiddigital/agentic-local-seo-audit` is 15 stars. Codex recommended none of them for production. Correct call, correctly hedged.
- **The negative finding on local SEO.** "No mature open-source replacement for BrightLocal, Whitespark, Semrush." I did not surface this because I did not search for it. It is true and it is commercially useful — it tells you to build thin around official Google APIs rather than shop.
- **The due-diligence section is better than mine.** Specifically *"GitHub's `Other` label often means source-available or a non-standard license."* That is exactly right, and it turned out to matter more than Codex realised. See below.
- **The 10-item handoff pack** is a real, sellable artefact. I had nothing equivalent.

---

## 3. The licence problem Codex pointed at but walked past

Codex's own rule says to check the licence at the deployed version, and warns that `Other` hides non-standard terms. It then made **n8n its number-one Phase 1 standardisation pick** and built Offer #5, "Client-Owned Operations Stack", around client ownership.

I read n8n's actual `LICENSE.md`. It is the **Sustainable Use License**, not an open-source licence. The limitation clause reads:

> "You may use or modify the software only for your own internal business purposes or for non-commercial or personal use. You may distribute the software or provide it to others only if you do so free of charge for non-commercial purposes."

Consequences for BridgeWorks:

- **Running n8n internally to serve your own clients: fine.** That is internal business purposes. This is what you already do, and nothing here changes it.
- **Deploying n8n into a client's infrastructure as a paid deliverable: not clearly permitted.** That is providing the software to others, not free of charge. This directly undercuts the "Digital Infrastructure Clients Own" framing for n8n specifically.
- Branches other than `master` are unlicensed, and `.ee.` files require an enterprise licence.

This is the single most important thing to come out of comparing the two reports, and neither of us caught it first time.

Wider licence picture across Codex's 51, as verified today: **21 are NOASSERTION** (no standard licence detected — includes n8n, Twenty, Astro, Formbricks, Chatwoot, Directus, Metabase, Outline, Dify, PostHog, Sentry, Budibase, Novu, Invoice Ninja, Mautic, Teable, LiteLLM, Flowise, Dokploy) and **8 are AGPL-3.0** (Plane, Documenso, Firecrawl, ToolJet, APITable, Kimai, listmonk, Plausible).

That means the majority of a stack pitched as "clients own it" carries either unreviewed non-standard terms or a copyleft licence with distribution obligations. The architecture is sound; the licence assumption underneath it is not.

---

## 4. The two reports answer different questions

This is why they barely overlap. Only n8n appears meaningfully in both.

| | Claude | Codex |
|---|---|---|
| Question answered | What is missing from the Claude Code skill/agent stack you already run? | What infrastructure should the agency self-host? |
| Unit of recommendation | Skills, subagents, workflow template libraries | Deployable products |
| Method | `gh search repos` + `gh api`, plus reading your local config and site messages | GitHub candidate review |
| Blind spot | Never looked at infrastructure or self-hosted products | Never looked at what you already have installed |
| Best contribution | Found the unregistered-marketplace problem and the 13-overlapping-GEO-skills redundancy | The stack architecture, the handoff pack, the local-SEO negative finding |

Codex's blind spot is the more expensive one. It recommends a stack without auditing what you run. Its own closing line concedes this — *"audit what BridgeWorks already has before installing anything"* — which is the right instinct, arriving one step too late to have shaped the report.

---

## 5. Where I disagree with Codex's recommendation

Codex says Phase 1 is *"sufficient for a solo agency without creating an unmanageable hosting burden."* I think that is wrong, on your specific evidence.

Phase 1 is n8n, Twenty, Formbricks, Cal.com, Astro, Umami, Lighthouse, OpenAI Agents SDK, Plane, Outline. Of those, **seven are services that must be hosted, patched, backed up, and kept online.** Phases 2 and 3 add twenty more.

Your own `CLAUDE.md`, dated 2026-07-22, records: two Hermes jobs paused on revoked Google OAuth, eight active jobs erroring for mixed and unverified reasons, and a note not to assume one OAuth repair fixes them. You are currently not able to keep the automations you already own green. Adding seven self-hosted services to that is how a solo operator acquires a second job as a sysadmin.

### Direct conflicts with standing rules and existing tools

- **Invoice Ninja vs szamlazz.hu.** Your global instructions say: *"Invoicing: szamlazz.hu (connected to NAV) — never bypass."* Codex recommends Invoice Ninja for proposals and invoices in both the core table and Phase 2. That is a direct conflict with a standing rule, and NAV connection is a legal-compliance matter, not a preference. **Drop Invoice Ninja.**
- **Plane vs Notion.** You already run Notion for pipeline CRM. Plane duplicates it and is AGPL.
- **Twenty vs Apollo.** The "Hunter + Tomba + Apollo, pick one, default Apollo" loop has been open since July. Adding a self-hosted CRM before closing that makes it a four-way problem.
- **Umami vs Vercel Analytics.** You are already on Vercel. Check what you are paying for before hosting another analytics service.

---

## 6. What to actually take

**Take from Codex:**
1. The **handoff pack** (its section 5, ten items). Adopt as standard for every website delivery, starting with the Oliviks closeout. This is the highest-value single item across both reports and it costs nothing to adopt.
2. The **due-diligence rules** (its section on licences and security). Adopt verbatim as a gate before any tool enters client work.
3. The **local-SEO negative finding**. Stop looking for a BrightLocal replacement. Build thin around Search Console and Lighthouse.
4. **Astro as the default for brochure and local-service sites**, reserving Next.js for portals and application logic. This is a sound, cost-reducing default and it fits the Oliviks class of work.
5. **Crawl4AI** (Apache-2.0, 76k stars, active) for audit and competitor crawling. Clean licence, real utility.

**Take from mine:**
6. The **n8n template libraries** — `enescingoz/awesome-n8n-templates` and `devlikeapro/waha-n8n-templates`. Still the fastest return on this list.
7. **Register a third-party marketplace.** Only `anthropics/claude-plugins-official` is known locally.
8. **Stop adding GEO skills.** Thirteen is enough.

**Reject from both:**
9. Do not stand up seven self-hosted services this quarter. Pick **one** — the CRM decision — and only after closing the Apollo loop.
10. Do not adopt Invoice Ninja. szamlazz.hu is a compliance requirement.

**Fix regardless:**
11. `bridgeworks-workspace/CLAUDE.md` still lists the old five services. Both reports were slowed by this and Codex may have been misled by it. Correct it to match the site. This is the cheapest fix on the list and it prevents the next agent making the same error.

---

## 7. On the process

Two independent looks agreed on one thing without coordinating: **Strategy & Transformation has no tooling behind it.** I found no OSS worth adopting; Codex did not even generate a section for it. When two different methods produce the same hole, the hole is real.

The disagreement was equally informative. Codex's service list was wrong in a way that was invisible from inside its own document — it read plausible, it was internally consistent, and it carried an explicit claim of verification. The only thing that caught it was fetching the site.

Rule worth keeping: **a research document that states it verified something is not evidence that it did.** Check the spine of any report before trusting the body. In this case the body was largely sound and the spine was fabricated, which is an unusual and easy-to-miss failure shape.

---

# Revision 2 — Codex's rebuttal, tested

Codex challenged the central finding. Its argument: I sourced the five areas from `src/messages/en.json`, that file is **locally modified**, and the *deployed* homepage shows Codex's five instead. If true, my whole adjudication inverts.

## The methodological catch is fair

Codex is right on the process point, and I should have checked this myself:

```
$ git status -sb                    →  main...origin/main [behind 6]
$ git status --porcelain src/messages/en.json  →  M src/messages/en.json
$ git diff --stat origin/main -- src/messages/en.json
   1 file changed, 138 insertions(+), 151 deletions(-)
```

`en.json` **is** modified locally, and the repo is **6 commits behind origin/main**. Citing a dirty working-tree file as "live site copy" — my exact phrasing in the original report — conflated a source file with a deployed artefact. That was sloppy wording and Codex was right to attack it.

## The factual claim is wrong

The catch does not survive contact with the deployed page. Two independent checks:

**1. `origin/main` (ahead of local, closest to deploy) has identical route names:**

```
$ git show origin/main:src/messages/en.json | jq '.routes.items[].name'
Strategy & Transformation
Digital Platforms & Brand Systems
Content, Visibility & Demand
AI & Workflow Automation
Execution & Operating Systems
```

The local modification touched other keys. It did **not** change the five route names. Local, `origin/main`, and my report all agree.

**2. The deployed page itself**, fetched with a cache-buster, HTML-unescaped, counted:

```
$ curl -s "https://bridgeworks.agency/en?cb=xyz99"        # HTTP 200, 104,863 bytes

--- MY FIVE (deployed) ---            --- CODEX FIVE (deployed) ---
1x  Strategy & Transformation         0x  Lead Follow-Up
1x  Digital Platforms & Brand Sys.    0x  Google and AI Search Visibility
1x  Content, Visibility & Demand      0x  Trust-Building Websites
1x  AI & Workflow Automation          0x  Client Intake
1x  Execution & Operating Systems     0x  Client-Owned Infrastructure

--- OLD CLAUDE.md FIVE (deployed) ---
0x  Digital Growth Strategy   0x  AI-Powered Marketing   0x  Brand Identity
```

All five of mine present, once each. **Zero** occurrences of any of Codex's five. Zero of the stale CLAUDE.md five.

The earlier ampersand confusion was HTML escaping: the deployed source carries `AI &amp; Workflow`, which is why a naive grep for `AI & Workflow` returns nothing. Unescape first.

**Conclusion: there are not three competing service lists. There are two — the deployed site's five, and the stale `CLAUDE.md` five.** Codex's five exist in no deployed page, no git ref, and no file in either repository except Codex's own output. Its rebuttal restated the invented list as "deployed homepage" without re-testing it.

Anyone can re-run the curl above in ten seconds. That is the whole argument.

## Where Codex is right about my report

Independent of the taxonomy, four of its criticisms land and I am correcting them.

**1. "Clone the n8n libraries today" was wrong. Conceded.**
`enescingoz/awesome-n8n-templates` is NOASSERTION — no declared licence grant. I flagged that in my own licence-warnings section and then still made "clone today" action item #1. That is an internal contradiction in my report. Codex's framing is correct: **review and catalogue first; do not clone into a commercial operating repo as reusable delivery IP.** Revised action: read and extract patterns, do not vendor the repo.

**2. "AGPL is safe self-hosted" was too broad. Conceded — this is a real legal correction.**
AGPL-3.0 §13 attaches source-disclosure obligations when a **modified** version is made available over a network. Self-hosting an unmodified copy is fine; modifying Relaticle or Plane and exposing it to clients over a network can trigger disclosure. My phrasing implied self-hosting was a blanket safe harbour. It is not. Per-deployment review required.

**3. Relaticle's 30 MCP tools are not a quality signal. Conceded.**
I hedged ("worth a spike") but led with the tool count as if it were evidence. It is a capability, not a verdict on operational fitness against Twenty, HubSpot, or the current Sheets-and-Notion setup.

**4. My report was mostly a Claude Code armory, not a full agency armory. Largely conceded.**
You asked for the full agency and consulting armory. I delivered an audit of your Claude-ecosystem tooling plus a repo scan. Codex covered CRM, intake, scheduling, chat, notifications, CMS, analytics, hosting, backups, monitoring, billing, and project control. That breadth is real and mine lacked it.

Partial: the **Oliviks WhatsApp** point. Oliviks is closeout, delivery complete, paid in full — Codex is right that nothing should reopen it. My intent was a forward-looking pattern for future hospitality prospects, but the phrasing invited the other reading. Restated: WAHA templates are a **pattern library for future work**, with no Oliviks implication.

Partial: **marketplace registration**. Codex calls it a Claude Code config choice, not an agency-capability decision. Fair — I over-ranked it. It still gates what tooling is reachable, so it stays on the list, lower down.

## The taxonomy proposal — right idea, wrong labels

Codex proposes splitting **five public offers shown to buyers** from **five internal delivery capabilities**. The underlying idea is sound and worth adopting; a packaging layer distinct from a capability layer is how agencies normally organise.

But the labels are inverted. The site's five *are* what buyers currently see — that is verified and deployed. Codex's five are not shown to any buyer anywhere. So:

- **Public taxonomy (deployed, canonical today):** Strategy & Transformation · Digital Platforms & Brand Systems · Content, Visibility & Demand · AI & Workflow Automation · Execution & Operating Systems
- **Proposed packaged offers (not yet public, needs your decision):** Codex's five, relabelled honestly as a proposal — Lead Response Engine, Search & Trust Sprint, Trust Website System, Qualified Intake System, Client-Owned Operations Stack

That resolves the conflict without pretending the second list is deployed. If you prefer the outcome-framed names for selling, that is a **positioning decision to make and then ship to the site** — not a fact to be discovered in a research report.

## Net position after revision 2

Codex's assessment — "Claude's is the better tactical discovery supplement, mine is the stronger operating architecture" — is fair and I accept it. Its stack architecture, handoff pack, and guardrails are more complete than anything in my report.

That does not extend to the service taxonomy, where its list is invented and now twice asserted as verified. Keep the architecture. Discard the spine. Relabel its five as proposed offers and the merge becomes clean.
