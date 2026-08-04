#!/usr/bin/env python3
"""Tests for validate_route.py."""

from validate_route import validate


GOOD = {
    "qualification_status": "audit-approved",
    "primary_service_route": "execution-operating-systems",
    "asset": {"title": "Lead-to-owner map", "production_ceiling_minutes": 20},
    "work_passes": ["evidence", "specialist", "demonstration", "executive-qa"],
    "buyer": {"primary": "COO", "secondary": "Marketing Director"},
    "planned_outputs": ["one-page routing map"],
    "stop_conditions": ["Stop if shared routing is already verified."],
    "approval_gates": ["Approve before external send."],
}


def main() -> None:
    assert validate(GOOD)["valid"], validate(GOOD)
    cases = [
        {**GOOD, "qualification_status": "research"},
        {**GOOD, "asset": None},
        {**GOOD, "asset": {"title": "Too large", "production_ceiling_minutes": 25}},
        {**GOOD, "work_passes": GOOD["work_passes"] + ["extra"]},
        {**GOOD, "buyer": {"primary": ""}},
        {**GOOD, "planned_outputs": ["full audit and proposal"]},
        {**GOOD, "stop_conditions": []},
    ]
    for case in cases:
        assert not validate(case)["valid"], case
    print("1 valid route and 7 invalid route cases passed")


if __name__ == "__main__":
    main()
