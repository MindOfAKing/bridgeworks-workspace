#!/usr/bin/env python3
"""Pure BridgeWorks lifecycle and next-action health analysis."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path

STAGES = ("market_hypothesis", "account_discovered", "evidence_collected", "qualified",
          "routed", "diagnostic_selected", "diagnostic_complete", "offer_selected",
          "outreach_prepared", "awaiting_approval", "sent", "replied", "opportunity",
          "discovery", "proposal", "won", "lost", "nurture")


def _day(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except ValueError:
        return None


def analyze(payload: dict) -> dict:
    as_of = date.fromisoformat(payload["as_of"][:10])
    rows = payload.get("records")
    if not isinstance(rows, list):
        raise ValueError("records must be a list")
    results = []
    for row in sorted(rows, key=lambda item: str(item.get("prospect_id") or "")):
        stage = row.get("lifecycle_stage")
        issues = []
        if stage not in STAGES:
            issues.append("unknown_lifecycle_stage")
        due = _day(row.get("next_action_due_at"))
        if due and due < as_of:
            issues.append("next_action_overdue")
        if stage in {"qualified", "routed", "diagnostic_selected", "diagnostic_complete",
                     "offer_selected", "outreach_prepared", "awaiting_approval"} and not row.get("next_action"):
            issues.append("missing_next_action")
        if stage in {"sent", "replied", "opportunity", "discovery", "proposal"} and not row.get("contact_verified"):
            issues.append("communication_state_unverified")
        if row.get("evidence_contradicted"):
            issues.append("contradicted_evidence")
        results.append({
            "prospect_id": row.get("prospect_id"),
            "lifecycle_stage": stage,
            "health": "needs_attention" if issues else "healthy",
            "issues": sorted(issues),
            "recommended_next_action": sorted(issues)[0] if issues else row.get("next_action"),
        })
    return {"as_of": as_of.isoformat(), "records": results,
            "needs_attention": sum(r["health"] == "needs_attention" for r in results),
            "external_action_authorized": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(json.loads(args.input.read_text(encoding="utf-8"))), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
