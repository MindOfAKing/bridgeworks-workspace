#!/usr/bin/env python3
"""Validate a bounded Commercial Intelligence hand-back."""

import argparse, json
from pathlib import Path

STATUSES = {"complete", "partial", "required", "not_applicable"}
CONFIDENCE = {"unknown", "low", "medium", "high"}
BANDS = {"low", "medium", "high", "unknown"}

def validate(data):
    errors=[]
    if data.get("capability") != "commercial-intelligence": errors.append("wrong capability")
    if not data.get("prospect_id"): errors.append("missing prospect_id")
    if not isinstance(data.get("evidence"), list): errors.append("evidence must be a list")
    else:
        for i,row in enumerate(data["evidence"]):
            if not all(row.get(k) is not None for k in ("id","claim","status","source","observed_at")):
                errors.append(f"evidence[{i}] missing attribution")
    if data.get("confidence") not in CONFIDENCE: errors.append("invalid confidence")
    if data.get("commercial_value_band") not in BANDS: errors.append("invalid commercial_value_band")
    if data.get("research_status") not in STATUSES: errors.append("invalid research_status")
    if not isinstance(data.get("unresolved_questions"), list): errors.append("unresolved_questions must be a list")
    if data.get("external_action_authorized") is not False: errors.append("external action must be false")
    return errors

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
    errors=validate(json.loads(a.input.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not errors,"errors":errors},indent=2)); return 1 if errors else 0

if __name__ == "__main__": raise SystemExit(main())
