#!/usr/bin/env python3
"""Self-contained tests for score_prospect.py."""

from score_prospect import score
import sys
from pathlib import Path


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
    assert score(BASE)["status_scope"] == "historical_compatibility_only"

    canonical = score({
        "qualification_version": "qualification-v1",
        "as_of": "2026-08-11",
        "components": {"problem_evidence": {"score": 25, "evidence_ids": ["e1"]}},
        "evidence": {"ledger": [{"id": "e1", "status": "verified",
                                    "source": "https://example.com", "observed_at": "2026-08-10"}]},
        "context": {"canonical_domain": "example.com", "contact_destination": "a@example.com",
                    "service_route_exists": True, "communication_state_resolved": True},
    })
    assert canonical["qualification_version"] == "qualification-v1", canonical
    assert canonical["component_scores"]["problem_evidence"] == 25, canonical
    print("6 legacy status cases, 1 validation case and 1 qualification-v1 case passed")


if __name__ == "__main__":
    main()
