# Phase 2 acceptance results

Run 2026-08-11. No outreach was sent, no CRM record was changed, and no live
schedule was edited.

## Test A — real unsent prospect and non-GEO routing: Appinio

Appinio is the acceptance prospect because the acquisition engine already holds a
qualification, route plan, decision snapshot, outreach drafts, and handoff. The
canonical operating state and log explicitly say no outreach was sent and no exact
recipient was verified.

Current public evidence was refreshed on 2026-08-11. Appinio's CEO announcement
names Arne Wolter and an operating-excellence mandate. Its live Senior Revenue
Operations role owns cross-functional workflows, HubSpot ecosystem optimization,
data-quality controls, CRM-health reporting, and reporting to Business
Intelligence. These are operating-system signals, not a GEO defect.

| Dimension | Old acquisition-engine state | New internal-GTM result |
|---|---|---|
| Identity | Appinio record plus five run artifacts | Domain-first key `domain:appinio.com`; source lineage retained |
| Contact history | Handoff and operating log say no send | `contacted: false`; no exact destination |
| Evidence | Seven public signals observed 2026-08-01 | Four current claims, all verified 2026-08-11; 0 stale and 0 contradicted |
| Qualification | Top-level 90, CRM field 95; `discovery-ready` | 88/100 HOT under the migration rubric; the score conflict is preserved as a migration issue |
| Service route | Execution & Operating Systems | `execution-operating-systems`, exact fit on `ownership` and `process_gaps` |
| Diagnostic | Revenue-system decision snapshot | Native `bridgeworks-revenue-system-scan` rubric applied; governed runtime falls back to registered `client-audit` pending registry repair |
| Proof | Reusable one-page snapshot | Current registry selects `oliviks-foundation-2026-07-24`; weak-fit proof is flagged for Phase 3 |
| Offer hypothesis | Bounded revenue-system decision/ownership review | `Operating cadence review`; price remains `confirmed_at_booking` |
| Approval packet | Drafts exist, but no verified recipient | `outreach_prepared`, `blocked_missing_destination`, no approval digest |
| Next action | Verify recipient before any send | Verify a lawful exact destination; then re-run approval preparation |

This passes the non-GEO test: the evidence selects Execution & Operating Systems,
not Content, Visibility & Demand. It also exposed three canonical conflicts that
must not be hidden: two qualification scores in the old run, the callable native
revenue scan being absent from the canonical registry, and a proof asset whose fit
to revenue operations is weak.

Machine-readable inputs and result:

- `migration/phase-2/acceptance/appinio-input.json`
- `migration/phase-2/acceptance/geo/appinio-2026-08-11.json`

The `geo/` output directory is a legacy name in the generic slice runner; the
record itself routes to `client-audit` and is not a GEO run.

## Test B — GEO suitability and aggregate gate: Tilz Prosperitas

Tilz is genuinely suitable for a GEO question because UK Export Finance records
an active international-expansion trigger and the company sells products and
wholesale/corporate gifting offers to cross-border buyers. That makes international
discoverability commercially relevant; it does not prove a visibility defect.

The existing registered `geo-audit` aggregate contract was used with the five
native Codex subordinate skills:

- `agent-geo-ai-visibility`
- `agent-geo-content`
- `agent-geo-platform-analysis`
- `agent-geo-schema`
- `agent-geo-technical`

The technical specialist completed a bounded four-page pass and scored 86/100.
It verified server-rendered Shopify content, public indexability, permissive public
robots rules, a valid five-child sitemap with 86 entries, structured data, and a
sitemap-advertised `agents.md`. The main technical opportunities are metadata
lengths, social-image metadata, duplicate H1s, security-header completeness, and
field CWV measurement. Technical accessibility is a strength, not evidence of
crawler invisibility.

The content specialist produced a provisional 37/100 content score and 28/100
E-E-A-T score from cached public evidence. It observed conflicting free-delivery
thresholds, an unsupported "curated by experts" claim, duplicated About-page copy,
and thin authority signals, but the page cache was stale enough that these require
fresh-page confirmation before commercial use. The schema specialist could not
inspect raw HTML and correctly returned `blocked_unverified`; the technical pass
did inspect raw HTML and observed syntactically valid Organization, WebSite,
ProductGroup and Article JSON-LD on its four-page sample. These are complementary
scope results, not grounds for claiming either complete schema coverage or no
schema.

The AI-visibility and platform passes could not retrieve enough current answer-
engine/entity evidence to issue defensible scores. Their unknown checks were not
converted into failures. Because a complete aggregate score and a material GEO
gap were not established, the Evidence Auditor must not advance Tilz to
qualification, proof selection, offer selection, or an approval packet.

| Stage | Result |
|---|---|
| Identity/dedupe | `domain:tilzcollection.co.uk`; named buyer Tayo Adebisi; no buyer email |
| Trigger | Current international expansion, observed 2026-08-02 |
| Registered diagnostic | `geo-audit`, using all five native specialist contracts |
| Technical result | 86/100 Good; strong crawlability and machine access |
| Content result | 37/100 content and 28/100 E-E-A-T, provisional pending fresh-page confirmation |
| Schema result | Dedicated pass blocked; technical sample observed valid JSON-LD but did not validate full eligibility |
| Aggregate result | Blocked/partial; no honest composite score |
| Evidence Auditor | Keeps unknown specialist checks unapproved |
| Route | GEO is plausible but not proven; remains `diagnostic_selected` |
| Proof/offer | Not selected; CEEFM proof must not be attached before a material gap is verified |
| Approval packet | Not produced |
| Next action | Retry the bounded AI-visibility, content, schema, and platform retrieval; then aggregate or return to research |

Machine-readable request:

- `migration/phase-2/acceptance/tilz-input.json`
- `migration/phase-2/acceptance/geo/tilz-prosperitas-2026-08-11.json`

This is a useful negative acceptance result. The architecture did not turn a
commercially relevant GEO hypothesis into a fabricated diagnosis merely to reach
an approval packet.

## Safety defect fixed during acceptance

The slice previously allowed a named buyer without an email to reach
`awaiting_approval`. It now stops at `outreach_prepared` with
`blocked_missing_destination`, a null approval digest, and the next action
`verify_exact_destination`. A regression test covers the gate.
