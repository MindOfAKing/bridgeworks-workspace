# GTM-critical runtime divergence classification

2026-08-11. Only the GTM-critical capabilities named in the decision were examined.
The other divergent skills were deliberately left alone: resolving them to reduce
a count is not a reason to touch a working skill.

Three classes are used:

- **canonical shared implementation** — one implementation of the logic, whatever
  the surface. Nothing to merge.
- **intentional runtime adaptation** — the copies differ for a stated runtime
  reason. Converging them would break the reason.
- **needs review** — a real gap or an unexplained difference. Emmanuel decides.

## Result

| Capability | Runtimes | Divergence | Class |
|---|---|---|---|
| `bridgeworks-lead-qualifier` | codex | none | canonical shared implementation |
| `bridgeworks-prospect-router` | codex | none | canonical shared implementation |
| `bridgeworks-geo-prospect-scan` | codex | none | canonical shared implementation |
| `bridgeworks-revenue-system-scan` | codex | none | canonical shared implementation |
| `bridgeworks-ai-workflow-scan` | codex | none | canonical shared implementation |
| `client-audit` | claude, codex | two live versions | intentional runtime adaptation |
| `market-emails` | claude, codex | two live versions | intentional runtime adaptation |
| `post-call-followup` | claude, codex | two live versions | intentional runtime adaptation |
| `discovery-call-prep` | claude, codex | two live versions | intentional runtime adaptation |
| `engagement-architect` | claude, codex | two live versions | intentional runtime adaptation |
| `geo-audit` | claude only | none | needs review |
| `agent-geo-ai-visibility` | codex only, status unknown | none | needs review |
| `agent-geo-content` | codex only, status unknown | none | needs review |
| `agent-geo-platform-analysis` | codex only, status unknown | none | needs review |
| `agent-geo-schema` | codex only, status unknown | none | needs review |
| `agent-geo-technical` | codex only, status unknown | none | needs review |
| `revops` | claude only | none | needs review |

## Canonical shared implementation

The qualifier, the router and the three bounded scans are installed in Codex only,
and that is correct. Their arithmetic and gates now live in
`operations/internal-gtm/scripts/gtm_core.py`. The Codex files are compatibility
CLIs that delegate. Claude Code calls `gtm_core` directly and needs no copy.

One implementation, two surfaces. Installing a second copy under Claude would
recreate the duplication Phase 3 removed.

## Intentional runtime adaptation

All five divergent capabilities differ in exactly the same way. Similarity ranges
from 0.92 to 0.98 and every difference is one of two things:

1. A `## Codex operating rule` block the Claude copy does not have. It is identical
   boilerplate across all five: follow Codex tool, safety and approval policy;
   resolve bundled paths relative to the skill folder; drafting and previews may
   proceed, but sending, publishing, scheduling with other people, changing live
   customer handling, spending credits and modifying production systems require
   Emmanuel's explicit approval. `engagement-architect` adds one line naming the
   Codex Python interpreter.
2. A shorter, quoted `description:` line in the Codex copy.

Neither is drift. The approval block encodes the Codex runtime's safety contract
and must not be removed. The description difference is a frontmatter convention.

**Recommendation: do not merge.** Instead, extract the shared approval block into
one reference and have each Codex skill include it, so a change to the safety
policy is one edit rather than five. That is a maintenance improvement, not a
correctness fix, and it can wait.

**Verify before it becomes drift:** these five need a test that the *body* below
the operating rule stays in step. Today the only differences are the two above. If
a third appears, it is real drift and should be caught by the test rather than by
someone reading a diff.

## Needs review

Three findings here, and they are the ones worth Emmanuel's time.

**The GEO orchestrator and its specialists are in different runtimes.**
`geo-audit` is installed under Claude only. The five `agent-geo-*` specialists it
delegates to are installed under Codex only. Neither runtime holds the whole
capability. The 2026-08-11 GBS Africa run worked because Claude Code could reach
both the orchestrator and equivalent subagents in-session. A Codex run could not
reproduce it, and a Claude run cannot call the Codex specialists.

This is not a divergence to merge. It is a distribution gap to decide:

1. install `geo-audit` under Codex so the family is whole in both runtimes; or
2. state that full GEO is a Claude Code capability and Codex uses
   `bridgeworks-geo-prospect-scan` for bounded initial contact, which is what the
   2026-08-01 audit already concluded.

Option 2 matches the current design. It just is not written down as a decision.

**The five GEO specialists are `unknown` status.** They cannot be called through
`capability_loader.require_capability` until reviewed. The GEO family is the most
mature capability BridgeWorks has and its specialists are currently ungoverned.
They should go through intake before the next GEO run, not after.

**`revops` is Claude only and four roles reference it.** `gtm-director`,
`market-icp-strategist`, `data-steward`, `reply-intelligence` and
`pipeline-manager` all list it. Any Codex-side run of those roles has no `revops`.
Either install it under Codex or replace those references with
`bridgeworks-revenue-system-scan`, which is Codex-installed and bounded.

## What was deliberately not touched

27 other capabilities carry `two_live_versions`. They were not examined and not
changed. Reducing a count is not a reason to edit a working skill. They stay on the
governance queue until a GTM decision actually depends on one of them.
