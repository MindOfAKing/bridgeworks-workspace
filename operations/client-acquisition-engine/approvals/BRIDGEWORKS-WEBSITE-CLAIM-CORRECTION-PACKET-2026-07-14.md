# BridgeWorks Website Claim Correction Packet

Date: 2026-07-14
Status: Source identified; correction approval still required. No source edit or deployment performed.
Live pages checked: https://bridgeworks.agency/en, https://bridgeworks.agency/hu, and https://bridgeworks.agency/en/about
Source map: `../research/BRIDGEWORKS-WEBSITE-SOURCE-MAP-2026-07-14.md`

## Decision

Approve one of these actions:

- `Approve the evidence-first replacements for implementation in the website source`
- `Provide missing evidence for selected claims and replace the rest`
- `Hold all website changes`

The production source is now identified as `MindOfAKing/bridgeworks-agency`, with a local clone at `C:\Users\User\Projects\bridgeworks-agency`. The audited `main` HEAD and latest GitHub production deployment both point to `f3e40e98480415b562c61a4eeb21ee9a1955b34e`. The local clone contains unrelated uncommitted contact-route and privacy-copy changes that must be preserved.

## Why This Is Urgent

The live site is the authority hub for the AI Visibility Report, outbound proof, and discovery-call funnel. Claims on that page must be at least as disciplined as the client-facing materials.

## Claim Review

### 1. CEEFM duration and result framing

Current production state:

- English says `Eight weeks later`.
- German, Hungarian, and Romanian source still says sixteen weeks in each language.
- The Hungarian live page directly confirms its sixteen-week version.

Evidence status: `REPLACE`

Reason:

- The verified engagement wording is March to June 2026.
- The public result guardrail is 16/100 to 77/100 at the June 10 engagement-close audit.
- BridgeWorks should not describe the engagement publicly as a completed 16-week engagement.
- Editing a client quotation without confirmation would be inappropriate.

Recommended replacement as a factual proof block, not an edited testimonial:

> CEEFM, Budapest facility management. BridgeWorks delivered a digital-growth foundation from March to June 2026. The verified engagement-close GEO and AI-visibility diagnostic improved from 16/100 to 77/100.

Optional boundary:

> Results are engagement-specific and do not guarantee the same score or commercial outcome for another business.

### 2. `30+ Scans delivered`

Current production state:

- English homepage: `30+ Reviews delivered`.
- Hungarian homepage: 30-plus delivered scans.
- All four locale files repeat `30+` on both the homepage offer and AI Visibility Scan route.

Evidence status: `VERIFY OR REPLACE`

Reason:

- The current evidence corpus substantiates six scored audits, three public mini scans, and one implementation verification.
- That corpus does not prove 30 or more delivered scans.
- Additional scans may exist, but no 30-plus source inventory is present in the current workspace.

Recommended replacement until a complete inventory exists:

> Evidence-led AI visibility diagnostics

Alternative after evidence is assembled:

> `<verified count>` documented audits and scans

### 3. `4 AI platforms scanned`

Current production state:

- English homepage: `4 platforms checked`.
- Hungarian homepage: four AI platforms scanned.
- All four locale files repeat the four-platform claim on both the homepage offer and AI Visibility Scan route.

Evidence status: `VERIFY SCOPE`

Reason:

- The public page does not name the four platforms or explain whether this is a repeatable scan scope.
- The current methodology evaluates owned-source accessibility, structure, entity clarity, citable content, trust, and commercial path. Platform observations must be labeled separately from owned-site evidence.

Recommended replacement:

> Owned-site, search, and AI-surface checks

If the four-platform product remains active, name the platforms and preserve dated evidence for each completed scan.

### 4. Free AI Visibility Scan

Current production state:

- English homepage: `48-Hour Lead Leak Review` plus a paid Lead Leak and Visibility Sprint.
- German, Hungarian, and Romanian homepages remain configured for the Free AI Visibility Scan.
- The non-English locale files also contain untranslated English positioning and sprint copy inside the same offer block.

Evidence status: `KEEP ONLY WITH A DEFINED SCOPE AND CAPACITY`

Reason:

- This is a public lead magnet and is distinct from the paid 48-Hour Lead Leak Review.
- The current lead-qualification workflow blurred it into a broader free digital-presence audit.
- The scan needs one controlled scope, output, owner, and capacity rule before it is promoted aggressively.

Recommended scope decision:

| Free AI Visibility Scan | Paid 48-Hour Lead Leak Review |
|---|---|
| Narrow AI-visibility snapshot using public evidence. | Wider trust, website, proof, and enquiry-path review. |
| Fixed limited output. | One-page review with five priority leaks and fixes. |
| No private access or implementation plan. | May lead directly to a scoped implementation offer. |
| Available only while capacity is explicitly open. | EUR 99 to EUR 250 unless strategically discounted. |

Do not promote the free scan as a complete audit.

### 5. Automated content publishing claim

Current live About-page text:

> The content engine publishing across multiple LinkedIn channels runs on automated workflows.

Evidence status: `VERIFY OR REPLACE`

Reason:

- The current scorecard confirms zero posts published in this run and twelve approval-ready content drafts.
- No current live publishing workflow was verified.

Recommended replacement until verified:

> BridgeWorks uses one evidence-led content queue to prepare channel-specific drafts for review.

### 6. Real-time lead qualification claim

Current live About-page text:

> The lead qualification system scores and routes every inbound enquiry in real time.

Evidence status: `VERIFY OR REPLACE`

Reason:

- A local n8n workflow template exists with lead scoring, Gmail-draft, alert, and Google-Sheets nodes.
- Its deployment and active status were not verified.
- Its embedded prompt still contains a retired free-audit rule.

Recommended replacement until a controlled live test passes:

> BridgeWorks has designed a guarded lead-qualification workflow for scoring, drafting, and routing inbound enquiries.

Do not claim real-time operation until webhook, Gmail, scoring, draft, alert, logging, and failure behavior are tested in the live environment.

## Implementation Checklist

1. Confirm the identified production source and hosting project from the source map. Completed in the read-only audit.
2. Locate every language and component that contains the reviewed claims.
3. Apply only Emmanuel-approved replacements.
4. Run the site build and tests.
5. Verify desktop and mobile rendering.
6. Deploy only with separate approval.
7. Recheck the live pages after deployment.
8. Update the authority report and outbound links only after the live hub is consistent.

## Approval Boundary

- The production source and local clone are identified, but no website source was edited because Emmanuel has not approved a correction direction.
- Existing uncommitted contact-route and privacy-copy changes in the website clone were preserved untouched.
- No deployment, CMS update, domain change, or production mutation was performed.
- The public offer is inconsistent by locale until Emmanuel chooses one homepage offer and capacity rule.
