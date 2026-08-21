# Codex / Claude Code Implementation Directive

Merge this package into `MindOfAKing/bridgeworks-workspace/operations/internal-gtm/`.

Do not create a second capability registry.

Before editing:
1. Read root `AGENTS.md` and `CLAUDE.md`.
2. Read `skill-governance/README.md`.
3. Validate `skill-governance/capability-registry.yaml`.
4. Diff every capability referenced by `role-registry.yaml` against the live registry.
5. Do not invent missing IDs. Map them correctly or use governed intake.

Implementation order:
1. Add this package.
2. Add a loader/adapter for `skill-governance/capability-registry.yaml`.
3. Add tests for no dangling capability references.
4. Implement GEO vertical slice:
   website URL -> geo-audit -> structured result -> Evidence Auditor -> Prospect Router -> Offer Strategist -> outreach packet.
5. Implement market-discovery vertical slice:
   sector hypothesis -> Trigger Scout -> candidates -> deterministic dedupe -> Lead Qualifier -> ranked research queue.
6. Exact dedupe and scoring arithmetic must be deterministic.
7. ODS/Qwen only for bounded validated preprocessing.
8. Claude/Codex for contradictions, strategy and final commercial reasoning.
9. Preserve all approval/no-send rules.
10. Produce GTM-only migration/decommission receipts.

Claude Code owns capability engineering, tests, schemas and skill/agent adaptation.
Codex owns orchestration, automation, migrations, browser operations and approved execution.
Cowork/Claude owns deep research, synthesis and editorial/commercial review.

Never build a separate standalone GTM app unless this architecture proves one necessary.
