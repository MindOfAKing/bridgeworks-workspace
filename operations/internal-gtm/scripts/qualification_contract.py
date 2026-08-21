#!/usr/bin/env python3
"""Historical qualification compatibility reader after qualification-v1 approval.

HOW TO USE
    from qualification_contract import codex_to_gtm, tier_to_codex_status, translate

Historical records may contain either of these superseded scales:

  bridgeworks-lead-qualifier   fit 25, active_change 25, problem_evidence 20,
                               capacity 15, buyer_access 15. Gate at 65 plus four
                               verified signals plus a buyer path plus a route.
  former gtm_core rubric       route fit 30, trigger 20, evidence 20,
                               reachability 15, gap severity 15. HOT at 75.

Neither scale owns current qualification state. `gtm_core.score_qualification`
implements canonical `qualification-v1`. This module only labels historical
numbers and shows their approximate old crosswalk. It never synthesizes the six
canonical components because that would invent evidence attribution.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtm_core as core  # noqa: E402

CONTRACT_VERSION = "qualification-v1-compatibility-2026-08-11"

# Codex rating maxima, from score_prospect.LIMITS.
CODEX_LIMITS = {"fit": 25, "active_change": 25, "problem_evidence": 20,
                "capacity": 15, "buyer_access": 15}

# Each band is (minimum rating, gtm value). Read top down, first match wins.
BANDS = {
    "fit": [(20, "exact"), (10, "adjacent"), (0, "none")],
    "problem_evidence": [(16, "verified"), (10, "observed"), (1, "inferred"), (0, "unknown")],
    "buyer_access": [(12, "named_buyer_with_email"), (7, "named_buyer"), (1, "generic_contact"), (0, "none")],
    "capacity": [(12, "high"), (7, "medium"), (1, "low"), (0, "none")],
}
# active_change is a rating, not a date. Map it to the freshness band it implies.
CHANGE_TO_TRIGGER_AGE = [(20, 15), (10, 60), (1, 150), (0, None)]

TIER_TO_STATUS = {
    "HOT": "audit-approved", "STRONG": "audit-approved",
    "QUALIFIED": "research", "WATCH": "research", "DO_NOT_PURSUE": "nurture",
}


class ContractError(ValueError):
    """Raised when a payload cannot be translated without guessing."""


def _band(name: str, value: int) -> str:
    for minimum, mapped in BANDS[name]:
        if value >= minimum:
            return mapped
    return BANDS[name][-1][1]


def codex_to_gtm(payload: dict) -> dict:
    """Codex qualifier ratings -> gtm_core.score_qualification signals."""
    ratings = payload.get("ratings")
    if not isinstance(ratings, dict):
        raise ContractError("payload needs a `ratings` object")
    missing = sorted(set(CODEX_LIMITS) - set(ratings))
    if missing:
        raise ContractError(f"missing ratings: {', '.join(missing)}")
    for name, maximum in CODEX_LIMITS.items():
        value = ratings[name]
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= maximum:
            raise ContractError(f"{name} must be an integer from 0 to {maximum}")

    trigger_age = next(age for minimum, age in CHANGE_TO_TRIGGER_AGE
                       if ratings["active_change"] >= minimum)
    return {
        "route_fit": _band("fit", ratings["fit"]),
        "trigger_age_days": trigger_age,
        "evidence_quality": _band("problem_evidence", ratings["problem_evidence"]),
        "reachability": _band("buyer_access", ratings["buyer_access"]),
        "gap_severity": _band("capacity", ratings["capacity"]),
    }


def tier_to_codex_status(tier: str, inbound_reply_referral_or_time_bound_event: bool = False) -> str:
    """Compatibility-only display mapping. It never changes canonical state."""
    if tier not in TIER_TO_STATUS:
        raise ContractError(f"unknown tier: {tier}")
    if tier == "HOT" and inbound_reply_referral_or_time_bound_event:
        return "discovery-ready"
    return TIER_TO_STATUS[tier]


def translate(payload: dict) -> dict:
    """Label a legacy payload without pretending it is qualification-v1."""
    if payload.get("exclusions"):
        return {
            "contract_version": CONTRACT_VERSION,
            "codex_score": sum(payload.get("ratings", {}).get(k, 0) for k in CODEX_LIMITS),
            "codex_status": "reject",
            "canonical_qualification": None,
            "requires_qualification_v1_rescore": True,
            "note": "legacy exclusion preserved; canonical gates must be evaluated separately",
        }
    signals = codex_to_gtm(payload)
    codex_score = sum(payload["ratings"][name] for name in CODEX_LIMITS)
    inbound = bool(payload.get("inbound_reply_referral_or_time_bound_event"))

    codex_gate = (
        codex_score >= 65
        and int(payload.get("verified_signal_count", 0)) >= 4
        and bool(payload.get("reachable_buyer_path"))
        and bool(payload.get("evidenced_service_route"))
    )
    codex_status = ("discovery-ready" if inbound else "audit-approved") if codex_gate else (
        "research" if (codex_score >= 45 or int(payload.get("verified_signal_count", 0)) >= 3) else "nurture")

    return {
        "contract_version": CONTRACT_VERSION,
        "historical_approximate_signals": signals,
        "codex_score": codex_score,
        "codex_status": codex_status,
        "canonical_qualification": None,
        "requires_qualification_v1_rescore": True,
        "state_ownership": "operations/internal-gtm qualification-v1 only",
        "note": "historical score retained for provenance; do not use it to advance lifecycle",
    }
