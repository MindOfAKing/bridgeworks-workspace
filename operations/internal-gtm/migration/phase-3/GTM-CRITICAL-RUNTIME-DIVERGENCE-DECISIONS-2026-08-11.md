# Runtime-divergence decision pointer

The canonical classification is `gtm-critical-divergence-classification.md` in
this directory. This file is retained only as a non-destructive pointer because
two implementations landed concurrently; it is not a competing classification.

<!-- Superseded content retained below for provenance only. -->

Date: 2026-08-11  
Scope: only the capabilities named in the qualification decision. The other
runtime conflicts remain untouched.

Classification vocabulary:

- `canonical shared implementation`: one business contract owns behavior.
- `intentional runtime adaptation`: business workflow is shared; runtime safety,
  paths or invocation text differ deliberately.
- `needs review`: parity or governance is not strong enough to authorize use.

## Decisions

| Capability | Runtime state | Classification | Decision |
|---|---|---|---|
| BridgeWorks Lead Qualifier | Codex native plus repository control plane | canonical shared implementation | `qualification-v1` under `operations/internal-gtm/` owns arithmetic, gates and state. The installed native CLI calls it. Legacy ratings return compatibility-only metadata and require rescore. |
| BridgeWorks Prospect Router | Codex native plus repository control plane | canonical shared implementation | `service-routes.yaml`, `capability_loader.py` and `gtm_core.select_service_route` own routing. The native validator is a compatibility CLI over those files. |
| `client-audit` | Claude and Codex, different SKILL.md digests | intentional runtime adaptation | Diff is limited to a shorter Codex description, Codex approval policy and a runtime-relative brand reference. The audit workflow is otherwise identical. Recorded on the registry divergence block. |
| `geo-audit` | Claude only, active | canonical shared implementation | The capability remains the registered diagnostic interface and must return the canonical GEO schema. No competing same-ID Codex implementation exists. |
| `agent-geo-ai-visibility`, `agent-geo-content`, `agent-geo-platform-analysis`, `agent-geo-schema`, `agent-geo-technical` | Codex only, status `unknown` | needs review | They remain blocked by `capability_loader`. They may not become executable merely because Tilz testing used one specialist read-only. Review provenance and output contracts before activation. |
| Three bounded scans | Codex only, active | canonical shared implementation | `bridgeworks-geo-prospect-scan`, `bridgeworks-revenue-system-scan` and `bridgeworks-ai-workflow-scan` are the registered bounded diagnostic interfaces. Their outputs feed the Internal GTM evidence and routing contracts. |
| `revops` | Claude only, active | canonical shared implementation | One registered implementation serves the strategy/escalation capability. There is no same-ID runtime conflict. |
| Outreach preparation, `market-emails` | Claude and Codex, different SKILL.md digests | intentional runtime adaptation | Codex adds approval policy and drafting-scope clarification. The email workflow is shared and neither runtime gains send authority. Recorded on the registry divergence block. |
| `discovery-call-prep` | Claude and Codex, different SKILL.md digests | intentional runtime adaptation | Codex adds approval policy and a runtime-relative brand reference. The preparation workflow is shared. Recorded on the registry divergence block. |
| `engagement-architect` | Claude and Codex, different SKILL.md digests | intentional runtime adaptation | Codex adds approval policy and a runtime-specific Python path. The evidence-controlled engagement workflow and schema are shared. Recorded on the registry divergence block. |

## Exact reviewed conflict scope

| Capability | SKILL.md diff size | Business-logic difference found |
|---|---:|---|
| client-audit | 12 changed lines | none |
| market-emails | 13 changed lines | none |
| discovery-call-prep | 12 changed lines | none |
| engagement-architect | 11 changed lines | none |

These four remain byte-different by design, but are no longer unclassified. The
registry preserves both digests plus `resolution_classification`, scope and
review date. No other runtime conflict was altered merely to reduce the count.

## Remaining review gate

The five `agent-geo-*` specialists remain non-active. Promoting them requires an
explicit governance review; this decision does not auto-approve them.
