#!/usr/bin/env python3
"""Count current prospect qualification research gaps from the read-only snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapters"))
import engine_snapshot  # noqa: E402

DIMENSIONS = ("problem_evidence", "commercial_fit", "buyer_accessibility",
              "trigger_urgency", "proof_fit", "execution_readiness")


def build(as_of: str) -> dict:
    snapshot = engine_snapshot.build(as_of)
    missing = Counter()
    statuses = {name: Counter() for name in DIMENSIONS}
    for prospect in snapshot["prospects"]:
        by_dimension = (prospect.get("qualification_coverage") or {}).get("by_dimension") or {}
        for name in DIMENSIONS:
            status = (by_dimension.get(name) or {}).get("research_status", "required")
            statuses[name][status] += 1
            if status in {"required", "partial"}:
                missing[name] += 1
    return {
        "as_of": as_of,
        "prospects": len(snapshot["prospects"]),
        "missing_by_dimension": {name: missing[name] for name in DIMENSIONS},
        "research_status_by_dimension": {
            name: {status: statuses[name][status]
                   for status in ("complete", "partial", "required", "not_applicable")}
            for name in DIMENSIONS
        },
        "definition": "missing means research_status is required or partial",
        "external_action_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = build(args.as_of)
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
