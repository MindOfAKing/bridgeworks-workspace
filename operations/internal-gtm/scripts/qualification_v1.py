#!/usr/bin/env python3
"""qualification-v1 derivation layer. The scorer itself lives in gtm_core.

HOW TO USE
    from qualification_v1 import derive_and_score
    result = derive_and_score(components, evidence_ledger, context, as_of="2026-08-11")

`gtm_core.score_qualification` is the canonical qualification-v1 scorer. It
validates a payload in which the caller has already declared `source_provenance`,
`evidence_freshness` and `confidence` per component.

This module is the layer that *derives* those three fields from the evidence
ledger instead of trusting a caller to assert them. A caller cannot claim
`current` freshness for a six-month-old source, or provenance it does not have,
because it never supplies them.

There is one implementation of the arithmetic and the gates. This file has none.
It builds a payload and delegates.

Qualification answers: should BridgeWorks invest further GTM effort here.
Routing answers: which service route and capability handle it. They stay apart,
and `FORBIDDEN_CONTEXT` makes the separation enforceable rather than a convention.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtm_core as core  # noqa: E402

# One source of truth. These are re-exported, never redefined.
MODEL_ID = core.QUALIFICATION_VERSION
DIMENSIONS = core.QUALIFICATION_COMPONENT_LIMITS
TIERS = core.QUALIFICATION_TIERS
MAX_SCORE = core.MAX_SCORE
ACTIONABLE = "actionable"
QualificationError = core.QualificationError

MODEL_APPROVED = "2026-08-11"
RESEARCH_STATUSES = core.RESEARCH_STATUSES

# Freshness bands. `gtm_core` accepts current, stale or unknown, so anything
# inside the staleness window reports `current` and confidence carries the nuance.
CURRENT_DAYS = 90

# Fields that would make a diagnostic family an implicit qualification proxy.
FORBIDDEN_CONTEXT = ("route_id", "primary_service_route", "diagnostic_score",
                     "diagnostic_capability", "geo_score", "gap_categories")

# Context keys this layer understands, mapped to the canonical gate names.
GATE_MAP = {
    "identity_domain_resolved": lambda c: bool(c.get("canonical_domain") or c.get("normalized_company"))
    and not c.get("identity_ambiguous"),
    "viable_contact_destination": lambda c: bool(c.get("contact_destination")),
    "credible_service_route": lambda c: bool(c.get("service_route_exists")),
    "materially_contradicted_evidence": lambda c: bool(c.get("contradicted_claim_ids")),
    "previous_outreach_exists": lambda c: bool(c.get("prior_outreach")),
    "communication_state_resolved": lambda c: bool(c.get("communication_state_resolved", True)),
    "legal_compliance_exclusion": lambda c: bool(c.get("legal_exclusion")),
    "explicit_defer_hold": lambda c: bool(c.get("defer_until") or c.get("hold_reason")),
}


def coverage_from_scored_components(components: dict) -> dict:
    """Backfill coverage for pre-coverage qualification-v1 run records.

    This changes no score. It interprets the evidence fields already persisted in
    each component. Buyer evidence below a verified named destination is partial;
    an evidence-free dimension remains required.
    """
    by_dimension = {}
    for name in DIMENSIONS:
        item = components.get(name) or {}
        status = item.get("research_status")
        usable = item.get("usable_evidence_ids") or item.get("approved_evidence_ids") or []
        if status not in RESEARCH_STATUSES:
            if item.get("contradicted_evidence_ids"):
                status = "partial"
            elif usable:
                status = "partial" if name == "buyer_accessibility" and item.get("score", 0) < 15 else "complete"
            else:
                status = "required"
        evidence_state = item.get("evidence_state")
        if not evidence_state:
            evidence_state = ("contradicted" if item.get("contradicted_evidence_ids") else
                              "approved" if usable else
                              "stale" if item.get("evidence_freshness") == "stale" else "unknown")
        by_dimension[name] = {
            "score": int(item.get("score", 0) or 0),
            "evidence_state": evidence_state,
            "evidence_ids": list(item.get("evidence_ids") or []),
            "confidence": item.get("confidence", "unknown"),
            "research_status": status,
        }
    sufficient = sum(item["research_status"] in {"complete", core.RESEARCH_EXHAUSTED,
                                                   "not_applicable"}
                     for item in by_dimension.values())
    return {"sufficiently_researched_dimensions": sufficient,
            "total_dimensions": len(DIMENSIONS),
            "percentage": round(sufficient / len(DIMENSIONS) * 100, 1),
            "by_dimension": by_dimension}


def _derive(name: str, given: dict, ledger_index: dict, as_of: str) -> dict:
    """Attach provenance, freshness and confidence from the ledger, not from the caller."""
    ids = [str(i) for i in (given.get("evidence_ids") or [])]
    cited = [ledger_index[i] for i in ids if i in ledger_index]
    classes = {entry["status"] for entry in cited}
    ages = [core._days_between(entry.get("observed_at"), as_of) for entry in cited]
    ages = [age for age in ages if age is not None]

    if not cited or not ages:
        freshness = "unknown"
    elif min(ages) > CURRENT_DAYS or classes == {"stale"}:
        freshness = "stale"
    else:
        freshness = "current"

    if not cited:
        confidence = "unknown"
    elif "contradicted" in classes or not (classes & set(core.APPROVED_CLASSES)):
        confidence = "low"
    elif "verified" in classes and freshness == "current":
        confidence = "high"
    else:
        confidence = "medium"

    research_status = given.get("research_status")
    if research_status is not None and research_status not in RESEARCH_STATUSES:
        raise QualificationError(
            f"{name}.research_status must be one of {RESEARCH_STATUSES}")

    return {
        "score": int(given.get("score", 0) or 0),
        "evidence_ids": sorted(ids),
        "source_provenance": sorted({str(e["source"]) for e in cited if e.get("source")}),
        "evidence_freshness": freshness,
        "confidence": confidence,
        "rationale": given.get("rationale"),
        "evidence_age_days": min(ages) if ages else None,
        "evidence_classes": sorted(classes),
        # A cited id that is not in the ledger is reported, never silently ignored.
        "unresolvable_evidence_ids": sorted(i for i in ids if i not in ledger_index),
        "research_status": research_status,
    }


def build_payload(components: dict, evidence: dict, context: dict, as_of: str) -> dict:
    smuggled = sorted(set(FORBIDDEN_CONTEXT) & set(context))
    if smuggled:
        raise QualificationError(
            "qualification must not read routing or diagnostic fields: " + ", ".join(smuggled))
    unknown = sorted(set(components) - set(DIMENSIONS))
    if unknown:
        raise QualificationError(f"unknown components: {', '.join(unknown)}")

    ledger_index = {entry["id"]: entry for entry in evidence.get("ledger", [])}
    derived = {name: _derive(name, components.get(name, {}), ledger_index, as_of)
               for name in DIMENSIONS}
    gates = {gate: check(context) for gate, check in GATE_MAP.items()}
    return {"components": derived, "evidence": evidence.get("ledger", []),
            "gates": gates, "as_of": as_of}


def derive_and_score(components: dict, evidence: dict, context: dict, as_of: str) -> dict:
    """Derive the evidence fields, then score with the canonical gtm_core scorer."""
    payload = build_payload(components, evidence, context, as_of)
    result = core.score_qualification(payload)
    result["model"] = MODEL_ID
    result["model_approved"] = MODEL_APPROVED
    result["as_of"] = as_of
    result["derived_by"] = "operations/internal-gtm/scripts/qualification_v1.py"
    result["gates_evaluated"] = payload["gates"]
    result["component_scores"] = {name: item["score"] for name, item in result["components"].items()}
    result["unscored_components"] = sorted(
        name for name, item in result["components"].items() if item["score"] == 0)
    result["unresolvable_evidence_ids"] = sorted({
        evidence_id
        for item in result["components"].values()
        for evidence_id in item.get("unresolvable_evidence_ids", [])
    })
    result["evidence_gap"] = bool(result["unscored_components"])
    result["blocking_conditions"] = [{"condition": reason} for reason in result["blocking_reasons"]]
    enrich_coverage(result)
    for name, item in result["components"].items():
        item["unresolvable_evidence_ids"] = payload["components"][name]["unresolvable_evidence_ids"]
        item["evidence_classes"] = payload["components"][name]["evidence_classes"]
        item["rationale"] = payload["components"][name]["rationale"]
    result["unresolvable_evidence_ids"] = sorted(
        {i for item in result["components"].values() for i in item["unresolvable_evidence_ids"]})
    return result



# ---- Coverage enrichment ----
#
# `gtm_core.score_qualification` owns qualification_coverage: per-dimension score,
# evidence state, evidence IDs, confidence and research status, plus the count and
# percentage. This adds the one distinction the decision calls out and the canonical
# block does not carry: why a dimension scored zero.
#
# A zero because nobody researched the dimension is not the same as a zero because
# the research was done and came back negative. The score cannot tell them apart.

ZERO_MISSING_RESEARCH = "missing_research"
ZERO_VERIFIED_NEGATIVE = "verified_negative"
ZERO_UNUSABLE_EVIDENCE = "unusable_evidence"
ZERO_EXHAUSTED_UNKNOWN = "exhausted_unknown"
COVERAGE_SUFFICIENT = ("complete", core.RESEARCH_EXHAUSTED)


def enrich_coverage(result: dict) -> dict:
    """Add `zero_because` and the missing-dimension lists. Never touches the score."""
    block = result["qualification_coverage"]
    for name, item in block["by_dimension"].items():
        component = result["components"][name]
        status = item["research_status"]
        if item["score"] > 0:
            item["zero_because"] = None
        elif status == "required":
            item["zero_because"] = ZERO_MISSING_RESEARCH
        elif status == "complete" and component.get("usable_evidence_ids"):
            item["zero_because"] = ZERO_VERIFIED_NEGATIVE
        elif status == core.RESEARCH_EXHAUSTED:
            item["zero_because"] = ZERO_EXHAUSTED_UNKNOWN
        elif status == "not_applicable":
            item["zero_because"] = None
        else:
            item["zero_because"] = ZERO_UNUSABLE_EVIDENCE

    by_dimension = block["by_dimension"]
    block["missing_dimensions"] = sorted(
        name for name, item in by_dimension.items()
        if item.get("zero_because") == ZERO_MISSING_RESEARCH)
    block["partial_dimensions"] = sorted(
        name for name, item in by_dimension.items() if item["research_status"] == "partial")
    block["verified_negative_dimensions"] = sorted(
        name for name, item in by_dimension.items()
        if item.get("zero_because") == ZERO_VERIFIED_NEGATIVE)
    block["exhausted_unknown_dimensions"] = sorted(
        name for name, item in by_dimension.items()
        if item["research_status"] == core.RESEARCH_EXHAUSTED)
    block["reopenable_dimensions"] = sorted(
        name for name, item in by_dimension.items()
        if item["research_status"] in ("required", "partial"))
    block["not_applicable_dimensions"] = sorted(
        name for name, item in by_dimension.items() if item["research_status"] == "not_applicable")
    block["note"] = ("Coverage is not a score and is never added to one. A dimension can be "
                     "fully researched and score zero. That is a verified negative, not a gap.")
    return block


# Backwards-compatible alias used by the slice and the tests.
score = derive_and_score
