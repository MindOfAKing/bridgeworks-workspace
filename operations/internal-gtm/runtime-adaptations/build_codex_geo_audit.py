#!/usr/bin/env python3
"""Generate the Codex runtime adaptation of `geo-audit` from the Claude source.

HOW TO USE
    python operations/internal-gtm/runtime-adaptations/build_codex_geo_audit.py --check
    python operations/internal-gtm/runtime-adaptations/build_codex_geo_audit.py --install

`geo-audit` is one canonical capability. There is one methodology, and it lives in
the Claude implementation, which carries the fuller orchestration contract. This
script derives the Codex copy from it rather than authoring a second one, so the
scoring weights, severity classes and quality gates cannot drift apart.

What the adaptation changes, and nothing else:

1. Frontmatter description rewritten in the Codex quoted style.
2. A `## Codex operating rule` block inserted, identical to the block every other
   Codex runtime adaptation carries.
3. Subagent names rewritten to the installed Codex specialist ids.
4. A machine-readable result contract appended, pinned to the shared schema, so
   both runtimes hand internal-GTM the same structure.

`--check` fails if the Claude source changed since the Codex copy was built. That
is the drift alarm: the copy is derived, so it is rebuilt, never hand-edited.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUDE_SOURCE = Path.home() / ".claude" / "skills" / "geo-audit" / "SKILL.md"
CODEX_TARGET = Path.home() / ".codex" / "skills" / "geo-audit" / "SKILL.md"
MANIFEST = HERE / "geo-audit-codex-adaptation.json"

# The five installed Codex specialists the orchestrator delegates to.
SPECIALIST_MAP = {
    "geo-ai-visibility": "agent-geo-ai-visibility",
    "geo-platform-analysis": "agent-geo-platform-analysis",
    "geo-technical": "agent-geo-technical",
    "geo-content": "agent-geo-content",
    "geo-schema": "agent-geo-schema",
}

CODEX_OPERATING_RULE = """## Codex operating rule

Follow current Codex tool, safety, and approval policy. Resolve bundled paths relative to this
skill folder. Drafting, analysis, and previews may proceed without external publication.
Require Emmanuel's explicit approval before sending, publishing, scheduling with other people,
changing live customer handling, spending credits, or modifying production systems.

This is a runtime adaptation of one canonical capability, not a second GEO methodology.
The scoring model, category weights, severity classes and quality gates below are derived
from the Claude implementation and must not be edited here. Rebuild with
`operations/internal-gtm/runtime-adaptations/build_codex_geo_audit.py --install`.

"""

RESULT_CONTRACT = """
---

## Structured result contract

Both runtimes hand internal-GTM the same structure. Wording may differ; shape may not.

Emit the audit result as JSON validating against
`operations/internal-gtm/schemas/geo-diagnostic.schema.json`:

```json
{
  "capability": "geo-audit",
  "run_id": "geo-audit:<host>-<YYYY-MM-DD>",
  "completed_at": "<YYYY-MM-DD>",
  "score": 0,
  "subagent_scores": {
    "ai_citability": 0, "brand_authority": 0, "content_eeat": 0,
    "technical_geo": 0, "schema": 0, "platform_optimization": 0
  },
  "findings": [
    {
      "id": "<short-id>",
      "category": "ai_visibility | schema | crawlability | content_depth | search_visibility | local_presence | website_trust",
      "severity": "high | medium | low | none",
      "claim": "<one factual sentence>",
      "value": "<machine-readable value>",
      "source": "<exact URL fetched>",
      "observed_at": "<YYYY-MM-DD>",
      "status": "verified | observed | inferred",
      "claim_key": "<optional, only when two findings assert the same proposition>"
    }
  ]
}
```

Rules that override any default behaviour:

- Every finding needs a source URL that was actually fetched. No source means
  `status: "inferred"`, and it will not score.
- `claim_key` is the exact proposition. `category` is the routing category. One
  category holds many distinct findings and those are not contradictions.
- Do not report a measurement that was not taken. An unavailable check is a gap,
  never a zero.
- The markdown report above is the human deliverable. The JSON is the machine
  deliverable. Produce both.
"""


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def adapt(source_text: str) -> str:
    parts = source_text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit("unexpected Claude source: no frontmatter block")
    body = parts[2]

    for claude_name, codex_name in SPECIALIST_MAP.items():
        body = re.sub(rf"\b{re.escape(claude_name)}\b", codex_name, body)

    description = (
        "Run the full BridgeWorks GEO audit: orchestrate five GEO specialists across "
        "AI citability, platform readiness, technical infrastructure, content E-E-A-T and "
        "schema, then produce a composite 0-100 GEO score with a prioritized action plan. "
        "Use for paid GEO delivery and full diagnostic runs."
    )
    frontmatter = f'---\nname: geo-audit\ndescription: "{description}"\n---\n\n'
    return frontmatter + CODEX_OPERATING_RULE + body.lstrip("\n") + RESULT_CONTRACT


# Parity assertions. Both runtimes must agree on every one of these.
PARITY_CHECKS = {
    "categories": ["AI Citability", "Brand Authority", "Content E-E-A-T",
                   "Technical GEO", "Schema & Structured Data", "Platform Optimization"],
    "weights": ["25%", "20%", "15%", "10%"],
    "formula": ["(Citability * 0.25)", "(Brand * 0.20)", "(EEAT * 0.20)",
                "(Technical * 0.15)", "(Schema * 0.10)", "(Platform * 0.10)"],
    "severity_classes": ["Critical (Fix Immediately)", "High (Fix Within 1 Week)",
                         "Medium (Fix Within 1 Month)", "Low (Optimize When Possible)"],
    "quality_gates": ["Never crawl more than 50 pages", "30-second maximum per page fetch"],
    "score_bands": ["90-100", "75-89", "60-74", "40-59", "0-39"],
}


def parity(claude_text: str, codex_text: str) -> dict:
    results = {}
    for name, needles in PARITY_CHECKS.items():
        results[name] = {"claude": all(n in claude_text for n in needles),
                         "codex": all(n in codex_text for n in needles)}
    results["specialists"] = {
        "claude": all(n in claude_text for n in SPECIALIST_MAP),
        "codex": all(n in codex_text for n in SPECIALIST_MAP.values()),
    }
    # The result contract is the Codex addition. Claude gets it via internal-GTM.
    results["result_contract"] = {"claude": True,
                                  "codex": "geo-diagnostic.schema.json" in codex_text}
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not CLAUDE_SOURCE.is_file():
        print(f"ERROR: Claude source missing: {CLAUDE_SOURCE}", file=sys.stderr)
        return 1
    claude_text = CLAUDE_SOURCE.read_text(encoding="utf-8")
    expected = adapt(claude_text)

    if args.install:
        CODEX_TARGET.parent.mkdir(parents=True, exist_ok=True)
        CODEX_TARGET.write_text(expected, encoding="utf-8")
        MANIFEST.write_text(json.dumps({
            "capability": "geo-audit",
            "canonical_source": str(CLAUDE_SOURCE),
            "runtime_adaptation": str(CODEX_TARGET),
            "source_sha256": digest(claude_text),
            "adaptation_sha256": digest(expected),
            "built_at": "2026-08-11",
            "specialist_map": SPECIALIST_MAP,
            "rule": "derived, never hand-edited. rebuild on source change.",
        }, indent=2) + "\n", encoding="utf-8")
        print(f"installed: {CODEX_TARGET}")

    if not CODEX_TARGET.is_file():
        print("ERROR: Codex adaptation not installed", file=sys.stderr)
        return 1
    actual = CODEX_TARGET.read_text(encoding="utf-8")
    drift = actual != expected
    report = parity(claude_text, actual)
    failures = [name for name, r in report.items() if not (r["claude"] and r["codex"])]

    print(f"claude source sha256 : {digest(claude_text)[:16]}")
    print(f"codex copy   sha256  : {digest(actual)[:16]}")
    print(f"drift from source    : {'YES, rebuild required' if drift else 'none'}")
    for name, r in report.items():
        print(f"  parity {name:18s} claude={r['claude']} codex={r['codex']}")
    if drift or failures:
        print(f"FAILED: {failures or ['drift']}", file=sys.stderr)
        return 1
    print("geo-audit runtime parity: contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
