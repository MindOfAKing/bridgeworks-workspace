#!/usr/bin/env python3
"""Deterministically rank existing prospects for bounded qualification enrichment."""

from __future__ import annotations

from datetime import date, datetime


DEFAULT_COHORT_SIZE = 8
MIN_COHORT_SIZE = 5
MAX_COHORT_SIZE = 10


def _day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def score_candidate(prospect: dict, as_of: date) -> dict:
    """Return a reviewable priority score. This is not qualification-v1."""
    problem = 20 if prospect.get("problem_evidence_present") else 0
    trigger = int(prospect.get("trigger_strength_signal") or 0)
    buyer = int(prospect.get("buyer_evidence_signal") or 0)
    proof = 15 if prospect.get("proof_fit_present") else 0
    attractiveness = int(prospect.get("company_attractiveness_signal") or 0)

    checked = _day(prospect.get("last_verified_at"))
    age = (as_of - checked).days if checked else 999
    freshness = 10 if age <= 7 else 7 if age <= 14 else 3 if age <= 30 else 0

    blocker_codes = []
    penalty = 0
    if prospect.get("contacted"):
        blocker_codes.append("already_contacted")
        penalty += 40
    if prospect.get("unsafe_state") == "unsafe_active":
        blocker_codes.append("unsafe_active")
        penalty += 40
    elif prospect.get("unsafe_state") == "unsafe_contained":
        blocker_codes.append("unsafe_contained")
        penalty += 12
    if prospect.get("missing_evidence"):
        blocker_codes.append("existing_research_incomplete")
        penalty += 8
    if prospect.get("engine_readiness") == "hold":
        blocker_codes.append("historical_hold")
        penalty += 5

    components = {
        "problem_evidence": _clamp(problem, 0, 20),
        "trigger_strength": _clamp(trigger, 0, 20),
        "buyer_evidence": _clamp(buyer, 0, 15),
        "proof_fit": _clamp(proof, 0, 15),
        "company_attractiveness": _clamp(attractiveness, 0, 15),
        "evidence_freshness": freshness,
        "blocker_penalty": -penalty,
    }
    total = sum(components.values())
    return {
        "prospect_id": prospect.get("prospect_id"),
        "company": prospect.get("company"),
        "priority_score": total,
        "components": components,
        "blocker_codes": blocker_codes,
        "why": [
            f"problem={components['problem_evidence']}/20",
            f"trigger={components['trigger_strength']}/20",
            f"buyer={components['buyer_evidence']}/15",
            f"proof={components['proof_fit']}/15",
            f"attractiveness={components['company_attractiveness']}/15",
            f"freshness={components['evidence_freshness']}/10",
            f"blockers={components['blocker_penalty']}",
        ],
    }


def rank(prospects: list[dict], as_of: date, cohort_size: int = DEFAULT_COHORT_SIZE) -> list[dict]:
    """Rank untouched existing prospects; stable prospect id breaks exact ties."""
    cohort_size = _clamp(int(cohort_size), MIN_COHORT_SIZE, MAX_COHORT_SIZE)
    eligible = [p for p in prospects if not p.get("contacted") and
                p.get("qualification_tier") != "DO_NOT_PURSUE" and
                (p.get("qualification_tier") is None or p.get("missing_qualification_dimensions"))]
    scored = [score_candidate(p, as_of) for p in eligible]
    scored.sort(key=lambda item: (-item["priority_score"], str(item["prospect_id"])))
    return scored[:cohort_size]
