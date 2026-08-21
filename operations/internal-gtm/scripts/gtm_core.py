#!/usr/bin/env python3
"""Deterministic GTM core: identity, dedupe, evidence, scoring, lifecycle, packets.

HOW TO USE
    from gtm_core import dedupe, score_qualification, build_evidence_ledger
Every function here is pure. Same input gives the same output, in the same order,
with no clock, no randomness, and no model call. Anything that needs judgment is
returned as a capability call request by the slice runners, not guessed here.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import date

# --------------------------------------------------------------------------
# Lifecycle
# --------------------------------------------------------------------------

LIFECYCLE: tuple[str, ...] = (
    "market_hypothesis",
    "account_discovered",
    "evidence_collected",
    "qualified",
    "routed",
    "diagnostic_selected",
    "diagnostic_complete",
    "offer_selected",
    "outreach_prepared",
    "awaiting_approval",
    "sent",
    "replied",
    "opportunity",
    "discovery",
    "proposal",
    "won",
    "lost",
    "nurture",
)

TERMINAL = {"won", "lost", "nurture"}
# Stages this runtime may never set. Only an approved external action reaches them.
APPROVAL_GATED = {"sent", "replied", "opportunity", "discovery", "proposal", "won", "lost"}


class LifecycleError(ValueError):
    """Raised on an illegal stage transition."""


def advance(current: str, target: str) -> str:
    if current not in LIFECYCLE:
        raise LifecycleError(f"unknown current stage: {current}")
    if target not in LIFECYCLE:
        raise LifecycleError(f"unknown target stage: {target}")
    if target in APPROVAL_GATED:
        raise LifecycleError(f"stage {target} requires an approved external action")
    if current in TERMINAL:
        raise LifecycleError(f"{current} is terminal")
    current_index = LIFECYCLE.index(current)
    target_index = LIFECYCLE.index(target)
    if target_index <= current_index:
        raise LifecycleError(f"cannot move backwards: {current} -> {target}")
    if target_index != current_index + 1:
        missing = LIFECYCLE[current_index + 1:target_index]
        raise LifecycleError(
            f"cannot skip lifecycle prerequisites: {current} -> {target}; "
            f"missing={list(missing)}")
    return target


# --------------------------------------------------------------------------
# Identity normalization and exact dedupe
# --------------------------------------------------------------------------

LEGAL_SUFFIXES = (
    "kft", "bt", "zrt", "nyrt", "kkt", "ev", "kv",
    "ltd", "limited", "llc", "inc", "incorporated", "corp", "corporation",
    "gmbh", "ag", "bv", "nv", "sa", "srl", "sro", "spzoo", "oy", "ab", "as",
    "plc", "co", "company", "group", "holding", "holdings",
)


def normalize_company(name: str) -> str:
    """Lowercase, drop punctuation and trailing legal-form words, collapse spaces."""
    if not name:
        return ""
    text = name.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    words = text.split()
    while words and words[-1] in LEGAL_SUFFIXES:
        words.pop()
    return " ".join(words)


def normalize_domain(value: str) -> str:
    """Reduce a URL or host to a bare registrable host. Empty string if none."""
    if not value:
        return ""
    text = value.strip().lower()
    text = re.sub(r"^[a-z][a-z0-9+.-]*://", "", text)
    text = text.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    text = text.split("@")[-1].split(":", 1)[0].rstrip(".")
    if text.startswith("www."):
        text = text[4:]
    return text if re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", text or "") else ""


def entity_key(record: dict) -> str:
    """Canonical dedupe key. Domain wins, company name is the fallback."""
    domain = normalize_domain(record.get("canonical_domain") or record.get("website_url") or "")
    if domain:
        return f"domain:{domain}"
    company = normalize_company(record.get("company", ""))
    return f"company:{company}" if company else ""


@dataclass
class DedupeResult:
    unique: list[dict] = field(default_factory=list)
    merges: list[dict] = field(default_factory=list)
    rejected: list[dict] = field(default_factory=list)


def _completeness(record: dict) -> int:
    return sum(1 for value in record.values() if value not in (None, "", [], {}))


def _merge_group(group: list[dict]) -> dict:
    """Fold a duplicate group into one record, independent of input order.

    The most complete record wins, ties broken by content digest. Fields the
    winner leaves empty are filled from the rest. Claims are unioned by id.
    """
    ordered = sorted(group, key=lambda r: (-_completeness(r), digest(r)))
    primary = dict(ordered[0])
    claims: dict[str, dict] = {str(c.get("id")): c for c in primary.get("claims", []) or []}
    for member in ordered[1:]:
        for field_name, value in member.items():
            if value in (None, "", [], {}):
                continue
            if primary.get(field_name) in (None, "", [], {}):
                primary[field_name] = value
        for claim in member.get("claims", []) or []:
            claims.setdefault(str(claim.get("id")), claim)
    if claims:
        primary["claims"] = [claims[k] for k in sorted(claims)]
    return primary


def dedupe(records: list[dict]) -> DedupeResult:
    """Exact deterministic dedupe. No fuzzy matching, no model call.

    Records that produce no key are rejected, never silently merged. Output is in
    sorted key order and each merged record is order-independent, so a shuffled
    input list gives a byte-identical result.
    """
    buckets: dict[str, list[dict]] = {}
    result = DedupeResult()
    for record in records:
        key = entity_key(record)
        if not key:
            result.rejected.append({"record": record, "reason": "no_domain_or_company"})
            continue
        buckets.setdefault(key, []).append(record)
    for key in sorted(buckets):
        group = sorted(buckets[key], key=lambda r: (-_completeness(r), digest(r)))
        primary = _merge_group(group)
        primary["entity_key"] = key
        domains, provenance = [], []
        for member in group:
            for value in (member.get("canonical_domain"), member.get("website_url")):
                host = normalize_domain(value or "")
                if host and host not in domains:
                    domains.append(host)
            for source in member.get("source_provenance", []) or ([member["source"]] if member.get("source") else []):
                if source not in provenance:
                    provenance.append(source)
        primary["canonical_domain"] = domains[0] if domains else None
        primary["alternate_domains"] = sorted(domains[1:])
        primary["normalized_company"] = normalize_company(primary.get("company", "")) or None
        primary["source_provenance"] = sorted(provenance)
        result.unique.append(primary)
        if len(group) > 1:
            result.merges.append({
                "entity_key": key,
                "kept": primary.get("company"),
                "merged_count": len(group),
                "merged": [m.get("company") for m in group[1:]],
                "rule": "exact_key_match",
            })
    return result


# --------------------------------------------------------------------------
# Evidence ledger
# --------------------------------------------------------------------------

EVIDENCE_CLASSES = ("verified", "observed", "inferred", "stale", "contradicted", "unknown")
APPROVED_CLASSES = ("verified", "observed")
DEFAULT_STALENESS_DAYS = 180

# ---- The claim_key invariant, system-wide ----
#
# `subject` is the broad routing and evidence category. One subject holds many
# distinct findings and those are NOT contradictions.
#
# `claim_key` is the exact proposition that may be confirmed or contradicted.
#
# Contradiction fires on claim_key. A producer that does not declare one gets an
# implicit key of (subject, source): the same topic observed on the same page. That
# catches an undeclared conflict without collapsing distinct findings from
# different pages into a false one. It never falls back to `subject` alone, which
# is the bug that made every geo-audit finding in a category look contradictory.


def claim_contradiction_key(claim: dict) -> tuple:
    explicit = claim.get("claim_key")
    if explicit:
        return ("declared", str(explicit))
    return ("implicit", str(claim.get("subject") or ""), str(claim.get("source") or ""))


def validate_claim_invariant(claims: list[dict]) -> list[str]:
    """Report producers that let `subject` stand in for `claim_key`.

    Not an error. A warning that two claims are only being compared because they
    happen to share a page, and the producer should say what it means.
    """
    warnings: list[str] = []
    implicit: dict[tuple, list[str]] = {}
    for claim in claims:
        key = claim_contradiction_key(claim)
        if key[0] == "implicit":
            implicit.setdefault(key, []).append(str(claim.get("id")))
    for key, ids in sorted(implicit.items()):
        if len(ids) > 1:
            warnings.append(
                f"claims {', '.join(sorted(ids))} share subject {key[1]!r} and source {key[2]!r} "
                "with no declared claim_key; declare one if they are competing assertions"
            )
    return warnings


def _days_between(observed_at: str, as_of: str) -> int | None:
    try:
        return (date.fromisoformat(as_of) - date.fromisoformat(observed_at)).days
    except (TypeError, ValueError):
        return None


def build_evidence_ledger(
    claims: list[dict],
    as_of: str,
    staleness_days: int = DEFAULT_STALENESS_DAYS,
) -> dict:
    """Classify claims. A claim without a source is never approved.

    Each claim needs id, subject, value, status, source, observed_at. A declared
    status is downgraded, never upgraded: no source means unknown, an old
    observation means stale, and two approved claims that disagree are both
    marked contradicted.

    Contradiction is checked on `claim_key`, which names the proposition, not on
    `subject`, which names the routing category. A category holds many distinct
    findings and those are not contradictions. A claim with no explicit claim_key
    falls back to its subject.
    """
    ledger: list[dict] = []
    for claim in claims:
        entry = {
            "id": claim.get("id"),
            "subject": claim.get("subject"),
            "claim_key": claim.get("claim_key"),
            "contradiction_key": claim_contradiction_key(claim),
            "value": claim.get("value"),
            "source": claim.get("source"),
            "observed_at": claim.get("observed_at"),
            "declared_status": claim.get("status", "unknown"),
        }
        status = entry["declared_status"] if entry["declared_status"] in EVIDENCE_CLASSES else "unknown"
        reason = "declared"
        if not entry["source"]:
            status, reason = "unknown", "no_source"
        elif status in APPROVED_CLASSES:
            age = _days_between(entry["observed_at"], as_of)
            if age is None:
                status, reason = "unknown", "no_observation_date"
            elif age < 0:
                status, reason = "unknown", "observation_in_the_future"
            elif age > staleness_days:
                status, reason = "stale", f"observed_{age}_days_ago"
        entry["status"] = status
        entry["reason"] = reason
        ledger.append(entry)

    by_key: dict[tuple, list[dict]] = {}
    for entry in ledger:
        if entry["status"] in APPROVED_CLASSES:
            by_key.setdefault(entry["contradiction_key"], []).append(entry)
    for key, entries in by_key.items():
        values = {json.dumps(e["value"], sort_keys=True, default=str) for e in entries}
        if len(values) > 1:
            label = key[1] if key[0] == "declared" else f"{key[1]}@{key[2]}"
            for entry in entries:
                entry["status"] = "contradicted"
                entry["reason"] = f"conflicting_values_for_{label}"

    ledger.sort(key=lambda e: (str(e["id"]), str(e["subject"])))
    approved = [e for e in ledger if e["status"] in APPROVED_CLASSES]
    rejected = [e for e in ledger if e["status"] not in APPROVED_CLASSES]
    if any(e["status"] == "verified" for e in approved):
        quality = "verified"
    elif approved:
        quality = "observed"
    elif any(e["status"] == "inferred" for e in ledger):
        quality = "inferred"
    else:
        quality = "unknown"
    return {
        "as_of": as_of,
        "staleness_days": staleness_days,
        "ledger": ledger,
        "approved_claim_ids": [e["id"] for e in approved],
        "rejected_claim_ids": [e["id"] for e in rejected],
        "evidence_quality": quality,
        "counts": {name: sum(1 for e in ledger if e["status"] == name) for name in EVIDENCE_CLASSES},
    }


# --------------------------------------------------------------------------
# qualification-v1 (canonical fixed arithmetic, evidence-backed components)
# --------------------------------------------------------------------------

QUALIFICATION_VERSION = "qualification-v1"
QUALIFICATION_COMPONENT_LIMITS = {
    "problem_evidence": 25,
    "commercial_fit": 20,
    "buyer_accessibility": 15,
    "trigger_urgency": 15,
    "proof_fit": 15,
    "execution_readiness": 10,
}
QUALIFICATION_TIERS = (
    (85, "HOT"),
    (70, "STRONG"),
    (55, "QUALIFIED"),
    (40, "WATCH"),
    (0, "DO_NOT_PURSUE"),
)
MAX_SCORE = sum(QUALIFICATION_COMPONENT_LIMITS.values())
CONFIDENCE_LEVELS = ("unknown", "low", "medium", "high")
FRESHNESS_LEVELS = ("current", "stale", "unknown")
RESEARCH_STATUSES = ("complete", "partial", "required", "exhausted_unknown",
                     "not_applicable")
# exhausted_unknown: the right capability ran against every approved source and the
# fact is still unknowable. It scores zero like `required`, but the scheduler must
# not reopen it. Only fresh evidence reopens an exhausted dimension.
RESEARCH_EXHAUSTED = "exhausted_unknown"

GATE_PRIORITY = (
    ("unresolved_identity_domain", "blocked_unresolved_identity_domain"),
    ("missing_viable_contact_destination", "blocked_missing_destination"),
    ("materially_contradicted_evidence", "blocked_contradicted_evidence"),
    ("unresolved_previous_outreach", "blocked_unresolved_communication_state"),
    ("legal_compliance_exclusion", "blocked_legal_compliance"),
    ("no_credible_service_route", "blocked_no_service_route"),
    ("explicit_defer_hold", "blocked_defer_hold"),
    ("unverified_gate_state", "blocked_unverified_gate_state"),
)

# Compatibility profile retained from the native BridgeWorks Lead Qualifier.
# It is centralized here so the skill wrapper no longer owns a second rubric.
LEGACY_READINESS_LIMITS = {
    "fit": 25,
    "active_change": 25,
    "problem_evidence": 20,
    "capacity": 15,
    "buyer_access": 15,
}


class QualificationError(ValueError):
    """Raised when qualification-v1 input cannot be scored without guessing."""


def _downgrade_confidence(confidence: str) -> str:
    index = CONFIDENCE_LEVELS.index(confidence)
    return CONFIDENCE_LEVELS[max(0, index - 1)]


def _qualification_gates(gates: dict, contradicted_referenced: bool) -> list[str]:
    blocking: list[str] = []
    required_truth = ("identity_domain_resolved", "viable_contact_destination",
                      "credible_service_route")
    if any(name not in gates for name in required_truth):
        blocking.append("unverified_gate_state")
    if gates.get("identity_domain_resolved") is not True:
        blocking.append("unresolved_identity_domain")
    if gates.get("viable_contact_destination") is not True:
        blocking.append("missing_viable_contact_destination")
    if gates.get("materially_contradicted_evidence") is True or contradicted_referenced:
        blocking.append("materially_contradicted_evidence")
    if gates.get("previous_outreach_exists") is True and gates.get("communication_state_resolved") is not True:
        blocking.append("unresolved_previous_outreach")
    if gates.get("legal_compliance_exclusion") is True:
        blocking.append("legal_compliance_exclusion")
    if gates.get("credible_service_route") is not True:
        blocking.append("no_credible_service_route")
    if gates.get("explicit_defer_hold") is True:
        blocking.append("explicit_defer_hold")
    return [name for name, _ in GATE_PRIORITY if name in set(blocking)]


def score_qualification(payload: dict) -> dict:
    """Score qualification-v1 and return actionability as a separate field.

    Every positive component needs at least one verified or observed evidence ID
    and explicit source provenance. Unknown, missing, stale-only or contradicted-
    only evidence contributes zero. Referenced contradictions are preserved and
    activate the contradiction hard gate; they are never silently selected.
    """
    components = payload.get("components")
    if not isinstance(components, dict):
        raise QualificationError("qualification-v1 requires a components object")
    missing = sorted(set(QUALIFICATION_COMPONENT_LIMITS) - set(components))
    extra = sorted(set(components) - set(QUALIFICATION_COMPONENT_LIMITS))
    if missing or extra:
        raise QualificationError(f"component mismatch; missing={missing}, extra={extra}")

    evidence_rows = payload.get("evidence") or []
    if not isinstance(evidence_rows, list):
        raise QualificationError("evidence must be a list")
    evidence_by_id = {str(row.get("id")): row for row in evidence_rows if row.get("id") is not None}

    scored: dict[str, dict] = {}
    adjustments: list[dict] = []
    contradicted_referenced = False
    for name, maximum in QUALIFICATION_COMPONENT_LIMITS.items():
        component = components[name]
        if not isinstance(component, dict):
            raise QualificationError(f"{name} must be an object")
        requested = component.get("score")
        if not isinstance(requested, int) or isinstance(requested, bool) or not 0 <= requested <= maximum:
            raise QualificationError(f"{name}.score must be an integer from 0 to {maximum}")
        ids = component.get("evidence_ids")
        provenance = component.get("source_provenance")
        freshness = component.get("evidence_freshness")
        confidence = component.get("confidence")
        if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
            raise QualificationError(f"{name}.evidence_ids must be a list of strings")
        if not isinstance(provenance, list) or not all(isinstance(item, str) for item in provenance):
            raise QualificationError(f"{name}.source_provenance must be a list of strings")
        if freshness not in FRESHNESS_LEVELS:
            raise QualificationError(f"{name}.evidence_freshness must be one of {FRESHNESS_LEVELS}")
        if confidence not in CONFIDENCE_LEVELS:
            raise QualificationError(f"{name}.confidence must be one of {CONFIDENCE_LEVELS}")

        statuses = {evidence_id: (evidence_by_id.get(evidence_id) or {}).get("status", "unknown")
                    for evidence_id in ids}
        unresolved = sorted(evidence_id for evidence_id in ids if evidence_id not in evidence_by_id)
        usable = sorted(evidence_id for evidence_id, status in statuses.items()
                        if status in APPROVED_CLASSES)
        contradicted = sorted(evidence_id for evidence_id, status in statuses.items()
                              if status == "contradicted")
        contradicted_referenced = contradicted_referenced or bool(contradicted)
        declared_research = component.get("research_status")
        if declared_research is not None and declared_research not in RESEARCH_STATUSES:
            raise QualificationError(
                f"{name}.research_status must be one of {RESEARCH_STATUSES}")
        if declared_research is None:
            research_status = "complete" if usable and not unresolved and not contradicted else "required"
        elif declared_research == "complete" and (unresolved or contradicted):
            research_status = "partial"
        elif declared_research == "complete" and not usable:
            research_status = "required"
        else:
            research_status = declared_research
        if research_status == "not_applicable":
            evidence_state = "not_applicable"
        elif contradicted:
            evidence_state = "contradicted"
        elif unresolved:
            evidence_state = "unknown"
        elif usable:
            evidence_state = "approved"
        elif "stale" in statuses.values():
            evidence_state = "stale"
        else:
            evidence_state = "unknown"
        effective = requested
        reason = None
        if requested > 0 and (not ids or not provenance or not usable or unresolved or contradicted):
            effective = 0
            if contradicted:
                reason = "contradicted_evidence_not_silently_resolved"
            elif unresolved:
                reason = "cites_evidence_ids_that_are_not_in_the_ledger"
            else:
                reason = "no_approved_evidence_attributable_to_this_component"
            adjustments.append({"component": name, "requested_score": requested,
                                "effective_score": 0, "reason": reason})
        effective_confidence = _downgrade_confidence(confidence) if freshness == "stale" else confidence
        scored[name] = {
            "score": effective,
            "requested_score": requested,
            "max_score": maximum,
            "evidence_ids": ids,
            "usable_evidence_ids": usable,
            "approved_evidence_ids": usable,
            "unresolvable_evidence_ids": unresolved,
            "contradicted_evidence_ids": contradicted,
            "contradicted": bool(contradicted),
            "evidence_classes": sorted(set(statuses.values())),
            "evidence_freshness": freshness,
            "evidence_age_days": component.get("evidence_age_days"),
            "confidence": effective_confidence,
            "source_provenance": provenance,
            "adjustment_reason": reason,
            "reason": reason or "scored",
            "rationale": component.get("rationale"),
            "evidence_state": evidence_state,
            "research_status": research_status,
        }

    score = sum(component["score"] for component in scored.values())
    tier = next(name for threshold, name in QUALIFICATION_TIERS if score >= threshold)
    gates = payload.get("gates") or {}
    if not isinstance(gates, dict):
        raise QualificationError("gates must be an object")
    blocking_reasons = _qualification_gates(gates, contradicted_referenced)
    actionability = "actionable" if not blocking_reasons else next(
        action for gate, action in GATE_PRIORITY if gate == blocking_reasons[0])
    sufficient = sum(
        item["research_status"] in {"complete", RESEARCH_EXHAUSTED, "not_applicable"}
        for item in scored.values())
    return {
        "qualification_version": QUALIFICATION_VERSION,
        "score": score,
        "max_score": MAX_SCORE,
        "tier": tier,
        "actionability": actionability,
        "blocking_reasons": blocking_reasons,
        "components": scored,
        "adjustments": adjustments,
        "thresholds": {name: threshold for threshold, name in QUALIFICATION_TIERS},
        "qualification_coverage": {
            "sufficiently_researched_dimensions": sufficient,
            "total_dimensions": len(QUALIFICATION_COMPONENT_LIMITS),
            "percentage": round(sufficient / len(QUALIFICATION_COMPONENT_LIMITS) * 100, 1),
            "by_dimension": {
                name: {
                    "score": item["score"],
                    "evidence_state": item["evidence_state"],
                    "evidence_ids": item["evidence_ids"],
                    "confidence": item["confidence"],
                    "research_status": item["research_status"],
                }
                for name, item in scored.items()
            },
        },
    }


def score_legacy_readiness(data: dict) -> dict:
    """Compatibility adapter for the former skill-local rubric.

    New architecture code uses `score_qualification`. Existing native skill calls
    keep their input/output contract while delegating all arithmetic and gates to
    this canonical module. The profile is labelled so it cannot be mistaken for
    the canonical HOT/WARM/COLD score.
    """
    ratings = data.get("ratings", {})
    errors: list[str] = []
    total = 0
    for field, maximum in LEGACY_READINESS_LIMITS.items():
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
        return {"valid": False, "errors": errors, "profile": "legacy_native_compatibility"}
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
        "profile": "legacy_native_compatibility",
        "canonical_successor": QUALIFICATION_VERSION,
        "gates": {
            "score_65": total >= 65,
            "four_signals": signals >= 4,
            "reachable_buyer_path": buyer_path,
            "evidenced_service_route": service_route,
            "inbound_reply_referral_or_time_bound_event": inbound_or_event,
        },
    }


def rank(prospects: list[dict]) -> list[dict]:
    """Stable ranking: score descending, then entity key ascending."""
    ordered = sorted(
        prospects,
        key=lambda p: (-int(p.get("qualification_score") or 0), str(p.get("entity_key") or ""), str(p.get("company") or "")),
    )
    for position, prospect in enumerate(ordered, start=1):
        prospect["rank"] = position
    return ordered


# --------------------------------------------------------------------------
# Routing and offer selection
# --------------------------------------------------------------------------

EVIDENCE_WEIGHT = {"verified": 3, "observed": 2}
SEVERITY_WEIGHT = {"high": 3, "medium": 2, "low": 1, "none": 0}
PROOF_STRENGTH = {"strong": 2, "partial": 1}


def _route_scores(
    route: dict,
    hits: list[str],
    findings: list[dict],
    buyer: dict | None,
    proof_assets: dict,
    known_capabilities: set[str] | None,
) -> dict:
    """Six commercial dimensions, in the order they break a tie. Integers only.

    Capability maturity is deliberately absent. It is reported as confidence on the
    result and never enters the comparison, so the most mature capability family
    cannot win a commercial tie on maturity alone.
    """
    mine = [f for f in findings if f.get("category") in set(hits)]
    proof = proof_assets.get(route["proof_asset_id"], {})
    proof_word = (proof.get("route_strength") or {}).get(route["id"])
    proof_fit = PROOF_STRENGTH.get(proof_word, 0)

    role_text = " ".join(str(v) for v in (buyer or {}).values() if v).lower()
    buyer_relevance = 2 if any(token in role_text for token in route.get("buyer_roles", [])) else 0

    capability = route["diagnostic_capability"]
    resolvable = known_capabilities is None or capability in known_capabilities
    credibility = (2 if resolvable and proof_fit else 1 if resolvable else 0)

    return {
        "evidence_strength": sum(EVIDENCE_WEIGHT.get(f.get("status"), 0) for f in mine),
        "commercial_pain": sum(SEVERITY_WEIGHT.get(f.get("severity"), 0) for f in mine),
        "buyer_relevance": buyer_relevance,
        "proof_fit": proof_fit,
        "urgency": sum(1 for f in mine if f.get("severity") == "high"),
        "entry_offer_credibility": credibility,
    }


def select_service_route(
    gap_categories: list[str],
    service_routes: dict,
    findings: list[dict] | None = None,
    buyer: dict | None = None,
    known_capabilities: set[str] | None = None,
) -> dict:
    """Pick one route from observed gaps, broken by commercial signal, not maturity.

    Tie-break order comes from `service-routes.yaml` -> `tie_break.order`:
    evidence strength, commercial pain, buyer relevance, proof fit, urgency,
    entry-offer credibility. If two routes tie on all six, no route is selected.
    The result is `fit: "tie"` and the decision escalates, because the evidence
    genuinely does not choose and code must not pretend it does.
    """
    observed = set(gap_categories)
    findings = findings or []
    proof_assets = {asset["id"]: asset for asset in service_routes.get("proof_assets", [])}
    order = service_routes["tie_break"]["order"]

    matches = {}
    for route in service_routes["routes"]:
        hits = sorted(observed & set(route["gap_categories"]))
        if hits:
            matches[route["id"]] = (route, hits)
    if not matches:
        return {"route_id": None, "route_name": None, "matched_gaps": [], "fit": "none",
                "unmatched_gaps": sorted(observed)}

    scored = []
    for route_id in sorted(matches):
        route, hits = matches[route_id]
        scores = _route_scores(route, hits, findings, buyer, proof_assets, known_capabilities)
        scored.append({
            "route_id": route_id,
            "route_name": route["name"],
            "matched_gaps": hits,
            "scores": scores,
            "ranking_key": [scores[name] for name in order],
            "capability_maturity": route.get("capability_maturity"),
            "diagnostic_capability": route["diagnostic_capability"],
            "proof_asset_id": route["proof_asset_id"],
        })
    scored.sort(key=lambda item: ([-value for value in item["ranking_key"]], item["route_id"]))

    best = scored[0]
    contenders = [item for item in scored if item["ranking_key"] == best["ranking_key"]]
    if len(contenders) > 1:
        return {
            "route_id": None,
            "route_name": None,
            "matched_gaps": sorted({gap for item in contenders for gap in item["matched_gaps"]}),
            "fit": "tie",
            "tied_routes": [item["route_id"] for item in contenders],
            "tie_break_order": order,
            "candidates": scored,
            "escalation": (
                "The evidence scores these routes identically on all six commercial dimensions. "
                "Capability maturity is not a selector. Route this to strategic_recommendation."
            ),
        }

    return {
        "route_id": best["route_id"],
        "route_name": best["route_name"],
        "matched_gaps": best["matched_gaps"],
        "fit": "exact" if len(matches) == 1 else "adjacent",
        "secondary_routes": [item["route_id"] for item in scored[1:]],
        "diagnostic_capability": best["diagnostic_capability"],
        "proof_asset_id": best["proof_asset_id"],
        "scores": best["scores"],
        "won_on": "only_matching_route" if len(scored) == 1 else next(
            (name for name in order if best["scores"][name] > scored[1]["scores"][name]),
            "route_id_ordering",
        ),
        "confidence": {"capability_maturity": best["capability_maturity"],
                       "note": "reported only, never used to select"},
        "candidates": scored,
    }


def select_offer_wedge(route_id: str, tier: str, service_routes: dict) -> dict:
    """Smallest credible wedge for the route. Price is never set here."""
    route = next((r for r in service_routes["routes"] if r["id"] == route_id), None)
    if route is None:
        raise ValueError(f"unknown service route: {route_id}")
    return {
        "route_id": route_id,
        "wedge": route["wedge"],
        "proof_asset_id": route["proof_asset_id"],
        "price": service_routes["price_policy"],
        "price_note": service_routes["price_policy_note"],
        "tier": tier,
    }


# --------------------------------------------------------------------------
# Outreach packet (approval gate)
# --------------------------------------------------------------------------

# Ported from bridgeworks-prospect-router/scripts/validate_route.py on 2026-08-11.
# These are the rules that stop a first touch becoming a free consulting project.
# In the router they only ran when someone handed the validator a plan. Here they
# run on every packet.
PROHIBITED_AT_FIRST_CONTACT = ("proposal", "full audit", "roi estimate", "crm migration architecture")
MAX_WORK_PASSES = 4
MAX_PRODUCTION_MINUTES = 20


class ApprovalError(RuntimeError):
    """Raised when a packet would carry an unapproved claim or an external action."""


def validate_initial_contact_plan(data: dict, service_routes: dict) -> dict:
    """Canonical production ceiling and approval-gate validation.

    This preserves the useful logic formerly owned by the prospect-router's
    hard-coded route validator while resolving route IDs from service-routes.yaml.
    """
    errors: list[str] = []
    route_ids = {route["id"] for route in service_routes["routes"]}
    if data.get("qualification_status") not in {"audit-approved", "discovery-ready"}:
        errors.append("qualification_status must be audit-approved or discovery-ready")
    if data.get("primary_service_route") not in route_ids:
        errors.append("primary_service_route must resolve in canonical service-routes.yaml")
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
    planned = " ".join([
        json.dumps(asset, ensure_ascii=True).lower() if isinstance(asset, dict) else "",
        " ".join(str(item).lower() for item in data.get("planned_outputs", [])),
    ])
    found = sorted(term for term in prohibited if term in planned)
    if found:
        errors.append("initial-contact overproduction detected: " + ", ".join(found))
    if not data.get("stop_conditions"):
        errors.append("at least one stop condition is required")
    if not data.get("approval_gates"):
        errors.append("at least one approval gate is required")
    return {"valid": not errors, "errors": errors}


def digest(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def build_outreach_packet(
    prospect: dict,
    evidence: dict,
    route: dict,
    offer: dict,
    cited_claim_ids: list[str],
    as_of: str,
) -> dict:
    """Assemble an approval packet. It stops at awaiting_approval and never sends.

    Every cited claim must be in the ledger's approved list. A citation that is
    rejected, stale, contradicted or unknown raises instead of being dropped.
    """
    approved = set(evidence["approved_claim_ids"])
    unapproved = [claim_id for claim_id in cited_claim_ids if claim_id not in approved]
    if unapproved:
        raise ApprovalError(f"packet cites unapproved evidence: {', '.join(map(str, unapproved))}")

    planned = " ".join(str(v) for v in offer.values() if v).lower()
    overproduction = sorted(term for term in PROHIBITED_AT_FIRST_CONTACT if term in planned)
    if overproduction:
        raise ApprovalError(
            "first-contact overproduction detected: " + ", ".join(overproduction))
    passes = offer.get("work_passes")
    if passes is not None and not 1 <= int(passes) <= MAX_WORK_PASSES:
        raise ApprovalError(f"work_passes must be 1 to {MAX_WORK_PASSES}")
    minutes = offer.get("production_ceiling_minutes")
    if minutes is not None and not 1 <= int(minutes) <= MAX_PRODUCTION_MINUTES:
        raise ApprovalError(f"production ceiling must be 1 to {MAX_PRODUCTION_MINUTES} minutes")
    body = {
        "prospect_id": prospect["prospect_id"],
        "company": prospect["company"],
        "canonical_domain": prospect.get("canonical_domain"),
        "buyer_name": prospect.get("buyer_name"),
        "buyer_role": prospect.get("buyer_role"),
        "buyer_email": prospect.get("buyer_email"),
        "service_route": route.get("route_id"),
        "offer_wedge": offer["wedge"],
        "proof_asset_id": offer["proof_asset_id"],
        "price": offer["price"],
        "cited_claims": [e for e in evidence["ledger"] if e["id"] in set(cited_claim_ids)],
        "qualification_score": prospect.get("qualification_score"),
        "qualification_tier": prospect.get("qualification_tier"),
    }
    return {
        "kind": "outreach_approval_packet",
        "lifecycle_stage": "awaiting_approval",
        "approval_state": "pending_approval",
        "approval_payload_digest": digest(body),
        "external_action_authorized": False,
        "no_send": True,
        "copy_required_from": "outreach-personalizer",
        "copy_authority": "draft_only",
        "prepared_at": as_of,
        "body": body,
        "approval_instruction": (
            "Approval authorizes only the exact copy attached to this digest, "
            "sent to this exact address, by Emmanuel or an approved Codex run."
        ),
    }
