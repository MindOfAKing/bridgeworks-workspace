#!/usr/bin/env python3
"""Self-contained tests for score_prospect.py."""

from score_prospect import score


def expect_status(payload: dict, expected: str) -> None:
    result = score(payload)
    assert result["valid"], result
    assert result["status"] == expected, result


BASE = {
    "ratings": {
        "fit": 18,
        "active_change": 20,
        "problem_evidence": 15,
        "capacity": 10,
        "buyer_access": 10,
    },
    "verified_signal_count": 5,
    "exclusions": [],
    "reachable_buyer_path": True,
    "evidenced_service_route": True,
    "inbound_reply_referral_or_time_bound_event": False,
}


def main() -> None:
    expect_status(BASE, "audit-approved")
    expect_status({**BASE, "inbound_reply_referral_or_time_bound_event": True}, "discovery-ready")
    expect_status({**BASE, "verified_signal_count": 2}, "research")
    expect_status({**BASE, "reachable_buyer_path": False}, "research")
    expect_status({**BASE, "exclusions": ["not a buyer"]}, "reject")

    weak = {
        "ratings": {
            "fit": 8,
            "active_change": 0,
            "problem_evidence": 7,
            "capacity": 5,
            "buyer_access": 5,
        },
        "verified_signal_count": 2,
        "exclusions": [],
        "reachable_buyer_path": True,
        "evidenced_service_route": True,
        "inbound_reply_referral_or_time_bound_event": False,
    }
    expect_status(weak, "nurture")

    invalid = score({**BASE, "ratings": {**BASE["ratings"], "fit": 30}})
    assert not invalid["valid"], invalid
    print("6 status cases and 1 validation case passed")


if __name__ == "__main__":
    main()
