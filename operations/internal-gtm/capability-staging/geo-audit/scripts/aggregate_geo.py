#!/usr/bin/env python3
"""Aggregate five governed GEO specialist hand-backs deterministically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SPECIALISTS = {
    "agent-geo-ai-visibility": ("ai_citability", "brand_authority"),
    "agent-geo-content": ("content_eeat",),
    "agent-geo-technical": ("technical_geo",),
    "agent-geo-schema": ("schema_structured_data",),
    "agent-geo-platform-analysis": ("platform_optimization",),
}
WEIGHTS = {
    "ai_citability": 0.25,
    "brand_authority": 0.20,
    "content_eeat": 0.20,
    "technical_geo": 0.15,
    "schema_structured_data": 0.10,
    "platform_optimization": 0.10,
}
CONFIDENCE = {"low", "medium", "high"}


def aggregate(payload: dict) -> dict:
    records = payload.get("specialists")
    if not isinstance(records, dict) or set(records) != set(SPECIALISTS):
        raise ValueError("specialists must contain exactly the five governed GEO specialists")
    category_scores: dict[str, int] = {}
    findings: list[dict] = []
    blocked: list[str] = []
    manifest: dict[str, dict] = {}
    confidences: list[str] = []
    for specialist in sorted(SPECIALISTS):
        record = records[specialist]
        scores = record.get("scores") or {}
        for category in SPECIALISTS[specialist]:
            value = scores.get(category)
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
                raise ValueError(f"{specialist}.{category} must be an integer from 0 to 100")
            category_scores[category] = value
        confidence = record.get("confidence")
        if confidence not in CONFIDENCE:
            raise ValueError(f"{specialist}.confidence must be low, medium, or high")
        confidences.append(confidence)
        rows = record.get("findings")
        if not isinstance(rows, list):
            raise ValueError(f"{specialist}.findings must be a list")
        for row in rows:
            if not all(key in row for key in ("id", "category", "severity", "claim", "status")):
                raise ValueError(f"{specialist} finding is missing a required field")
            findings.append({**row, "specialist": specialist})
        specialist_blocked = sorted(str(item) for item in record.get("blocked_checks", []))
        blocked.extend(f"{specialist}:{item}" for item in specialist_blocked)
        manifest[specialist] = {
            "confidence": confidence,
            "sources_checked": sorted(str(item) for item in record.get("sources_checked", [])),
            "finding_count": len(rows),
            "blocked_checks": specialist_blocked,
        }
    score = round(sum(category_scores[name] * weight for name, weight in WEIGHTS.items()))
    overall_confidence = "low" if "low" in confidences else "medium" if "medium" in confidences else "high"
    return {
        "capability": "geo-audit",
        "run_id": payload.get("run_id"),
        "completed_at": payload.get("completed_at"),
        "score": score,
        "category_scores": {name: category_scores[name] for name in WEIGHTS},
        "findings": sorted(findings, key=lambda row: (str(row["id"]), str(row["specialist"]))),
        "specialist_manifest": manifest,
        "confidence": overall_confidence,
        "blocked_checks": sorted(blocked),
        "external_action_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = aggregate(json.loads(args.input.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
