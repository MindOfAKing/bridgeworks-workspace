#!/usr/bin/env python3
"""Validate a BridgeWorks prospect routing plan."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROUTES = {
    "strategy-transformation",
    "digital-platforms-brand",
    "content-visibility-demand",
    "ai-workflow-automation",
    "execution-operating-systems",
}


def validate(data: dict) -> dict:
    errors: list[str] = []
    if data.get("qualification_status") not in {"audit-approved", "discovery-ready"}:
        errors.append("qualification_status must be audit-approved or discovery-ready")
    if data.get("primary_service_route") not in ROUTES:
        errors.append("primary_service_route must be one recognized route")

    asset = data.get("asset")
    if not isinstance(asset, dict):
        errors.append("asset must be one object")
    elif asset.get("production_ceiling_minutes") not in range(1, 21):
        errors.append("asset production ceiling must be from 1 to 20 minutes")

    work_passes = data.get("work_passes", [])
    if not isinstance(work_passes, list) or not 1 <= len(work_passes) <= 4:
        errors.append("work_passes must contain from 1 to 4 passes")

    buyer = data.get("buyer")
    if not isinstance(buyer, dict) or not isinstance(buyer.get("primary"), str) or not buyer["primary"].strip():
        errors.append("exactly one primary buyer is required")

    prohibited = {"proposal", "full audit", "roi estimate", "crm migration architecture"}
    planned = " ".join(
        [
            json.dumps(asset, ensure_ascii=True).lower() if isinstance(asset, dict) else "",
            " ".join(str(item).lower() for item in data.get("planned_outputs", [])),
        ]
    )
    found = sorted(term for term in prohibited if term in planned)
    if found:
        errors.append("initial-contact overproduction detected: " + ", ".join(found))

    if not data.get("stop_conditions"):
        errors.append("at least one stop condition is required")
    if not data.get("approval_gates"):
        errors.append("at least one approval gate is required")

    return {"valid": not errors, "errors": errors}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_route.py <route.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 1
    result = validate(data)
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
