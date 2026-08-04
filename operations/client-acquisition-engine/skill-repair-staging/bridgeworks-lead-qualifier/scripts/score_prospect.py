#!/usr/bin/env python3
"""Deterministically score a BridgeWorks prospect from evidence ratings."""

from __future__ import annotations

import json
import sys
from pathlib import Path


LIMITS = {
    "fit": 25,
    "active_change": 25,
    "problem_evidence": 20,
    "capacity": 15,
    "buyer_access": 15,
}


def score(data: dict) -> dict:
    ratings = data.get("ratings", {})
    errors: list[str] = []
    total = 0

    for field, maximum in LIMITS.items():
        value = ratings.get(field)
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{field} must be an integer from 0 to {maximum}")
            continue
        if not 0 <= value <= maximum:
            errors.append(f"{field} must be from 0 to {maximum}")
            continue
        total += value

    signals = data.get("verified_signal_count")
    if not isinstance(signals, int) or isinstance(signals, bool) or signals < 0:
        errors.append("verified_signal_count must be a non-negative integer")

    exclusions = data.get("exclusions", [])
    if not isinstance(exclusions, list) or not all(isinstance(item, str) for item in exclusions):
        errors.append("exclusions must be a list of strings")
        exclusions = []

    buyer_path = data.get("reachable_buyer_path")
    if not isinstance(buyer_path, bool):
        errors.append("reachable_buyer_path must be true or false")

    service_route = data.get("evidenced_service_route")
    if not isinstance(service_route, bool):
        errors.append("evidenced_service_route must be true or false")

    inbound_or_event = data.get("inbound_reply_referral_or_time_bound_event", False)
    if not isinstance(inbound_or_event, bool):
        errors.append("inbound_reply_referral_or_time_bound_event must be true or false")

    if errors:
        return {"valid": False, "errors": errors}

    if exclusions:
        status = "reject"
    elif total >= 65 and signals >= 4 and buyer_path and service_route:
        status = "discovery-ready" if inbound_or_event else "audit-approved"
    elif total >= 45 or signals >= 3:
        status = "research"
    else:
        status = "nurture"

    return {
        "valid": True,
        "score": total,
        "status": status,
        "verified_signal_count": signals,
        "gates": {
            "score_65": total >= 65,
            "four_signals": signals >= 4,
            "reachable_buyer_path": buyer_path,
            "evidenced_service_route": service_route,
            "inbound_reply_referral_or_time_bound_event": inbound_or_event,
        },
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: score_prospect.py <prospect.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 1

    result = score(data)
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
