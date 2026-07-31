# Marketing Skills capability diff

Date: 2026-07-25  
Repository: `coreyhaines31/marketingskills`  
Pinned commit: `c21a984a56da10fb6085e6334f6f60929220a4da`  
Licence: MIT  
Installation decision: do not install the repository or any component in this batch

Each selected component contains Markdown instructions, evaluation data, and references. No executable script was present in the five component folders. Static scans were run on each component, not only the full bundle.

| Candidate | Static scan | Existing internal evidence | Gap assessment | Decision |
|---|---|---|---|---|
| Revenue operations | LOW, score 8, one autonomous-decision warning | `lead-qualifier-skill`, `new-proposal`, daily/weekly operations, pipeline and BridgeWorks Ops workflows | Partial gap. Lifecycle definitions, routing, and handoff rules are useful. A full SaaS revenue framework would duplicate current operations | Reference only. Cherry-pick lifecycle and handoff checks into existing pipeline documentation after a real backend use case |
| Churn prevention | LOW, score 0 | Client follow-up and client-success documentation exist, but no dedicated subscription churn skill was found | Genuine procedure gap, but the skill is SaaS and subscription focused. BridgeWorks does not have a current qualifying use case | Reject for now. Reassess only for a retained or subscription client |
| Marketing loops | LOW, score 0 | Hermes, YouTube Intelligence, daily brief, weekly review, content workflows, and existing automation source mapping | Conflicting orchestration framework. The bounded trigger, self-check, and stopping-condition pattern is useful | Reference only. Cherry-pick the stopping-condition pattern, not the framework |
| Programmatic SEO | LOW, score 0 | `market-seo`, `market-landing`, `geo-content`, `geo-schema`, `geo-technical`, `gsc-opportunity` | Improvement candidate. Templated page systems and thin-content controls are not a complete internal procedure, but most supporting capabilities exist | Reference only. Consider a bounded isolated pilot after a real client use case exists |
| App-store optimisation | LOW, score 8, three context-size warnings | No dedicated ASO equivalent | Genuine capability gap with no realistic BridgeWorks use case | Reject for now. Do not install speculatively |

## Programmatic SEO evidence

The generated capability diff classifies the component as an improvement candidate and cites:

- `C:\Users\User\.claude\skills\market-seo\SKILL.md`
- `C:\Users\User\.claude\skills\market-landing\SKILL.md`
- `C:\Users\User\.claude\skills\geo-content\SKILL.md`
- `C:\Users\User\.claude\skills\geo-schema\SKILL.md`
- `C:\Users\User\.claude\skills\geo-technical\SKILL.md`
- `C:\Users\User\.claude\skills\gsc-opportunity\SKILL.md`

The genuine missing layer is not generic SEO. It is a controlled template-plus-data production procedure with page-level usefulness, duplication, citation, schema, indexation, and rollback gates.

## Permission and workflow differences

The five reviewed component folders do not require credentials or executable helpers by themselves. Real implementation would require filesystem writes and usually web research. Programmatic publishing would also require production access, which is outside this batch and needs explicit approval.

The external repository assumes a shared product-marketing context file and its own family of related skills. BridgeWorks already has brand, market, GEO, proposal, automation, and memory systems. Installing the bundle would create a competing framework and duplicate triggers.

## Final recommendation

Do not install any selected Marketing Skills component now.

The next justified action is a reference-only RevOps review against the current proposal-to-invoice and lead-handoff backend. Success means one documented lifecycle and handoff map reduces an actual missed step without adding a second operations framework.
