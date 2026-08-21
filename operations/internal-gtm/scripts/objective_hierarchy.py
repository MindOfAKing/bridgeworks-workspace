#!/usr/bin/env python3
"""The canonical GTM objective hierarchy: seven priority classes, ranked within.

HOW TO USE
    from objective_hierarchy import select
    decision = select(snapshot)

Approved 2026-08-11 after shadow day 1. Two things changed from the first ladder.

**Unsafe state is no longer automatically top priority.** It is top priority when it
is `unsafe_active`: when it can cause an external action, contaminate shared state,
affect several prospects, or sit behind an executable approval. When lifecycle and
approval gates already contain it, it is `unsafe_contained` and it is a
reconciliation task that does not outrank revenue-producing work.

**Qualification coverage is a primary objective, not a side quest.** With zero fully
covered prospects, the system must be able to choose to finish qualifying what it
already has instead of finding more.

Within a class, ranking uses expected commercial value, urgency, evidence
confidence and effort. **Route maturity and implementation maturity are not ranking
factors.** How good BridgeWorks is at a capability is not a fact about the prospect.
"""

from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrichment_priority import rank as rank_enrichment  # noqa: E402

# Priority classes, highest first. Position is the class rank.
PRIORITY_CLASSES = (
    "stop_unsafe_external_action",
    "advance_active_revenue",
    "complete_qualification_coverage",
    "resolve_blocking_evidence",
    "execute_due_followup_or_nurture",
    "recover_overdue_research",
    "generate_new_supply",
)

UNSAFE_ACTIVE = "unsafe_active"
UNSAFE_CONTAINED = "unsafe_contained"

# Lifecycle stages at or beyond which an unsafe state could reach an external action.
EXECUTABLE_STAGES = {"awaiting_approval", "sent"}

# Ranking factors, in the order they break a tie. Maturity is deliberately absent.
RANK_ORDER = ("expected_commercial_value", "urgency", "evidence_confidence", "low_effort")

CONFIDENCE_POINTS = {"high": 3, "medium": 2, "low": 1, "unknown": 0, None: 0}
TIER_VALUE = {"HOT": 5, "STRONG": 4, "QUALIFIED": 3, "WATCH": 2, "DO_NOT_PURSUE": 0, None: 1}


def _day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(str(value)[:10])
        except ValueError:
            return None


def _age(value: str | None, as_of: date) -> int | None:
    parsed = _day(value)
    return (as_of - parsed).days if parsed else None


def classify_unsafe(prospect: dict, snapshot: dict) -> dict:
    """Active or contained. The distinction is whether a gate already holds it."""
    reasons_active, reasons_contained = [], []

    stage = prospect.get("lifecycle_stage")
    actionability = prospect.get("actionability")
    approval_ids = prospect.get("approval_task_ids") or []
    contradicted_subjects = set(prospect.get("contradicted_subjects") or [])

    if stage in EXECUTABLE_STAGES:
        reasons_active.append(f"lifecycle stage {stage} can reach an external action")
    if approval_ids:
        reasons_active.append(f"attached to executable approval task {approval_ids}")
    if prospect.get("contact_state_conflict"):
        reasons_active.append("contact state conflicts, so a send could be repeated or missed")
    if prospect.get("shared_state_contaminated"):
        reasons_active.append("the contradiction sits on shared or canonical state")

    # Does the same contradiction appear on another prospect?
    if contradicted_subjects:
        others = [
            other["prospect_id"] for other in snapshot.get("prospects", [])
            if other.get("prospect_id") != prospect.get("prospect_id")
            and contradicted_subjects & set(other.get("contradicted_subjects") or [])
        ]
        if others:
            reasons_active.append(f"the same contradiction affects {len(others)} other prospects")

    if not reasons_active:
        if actionability and actionability != "actionable":
            reasons_contained.append(f"lifecycle gate already blocks advancement: {actionability}")
        if stage not in EXECUTABLE_STAGES:
            reasons_contained.append(f"stage {stage} cannot reach an external action")
        if not approval_ids:
            reasons_contained.append("no approval exists that could execute against it")
        reasons_contained.append("isolated to this prospect, no shared rule contaminated")

    severity = UNSAFE_ACTIVE if reasons_active else UNSAFE_CONTAINED
    return {
        "prospect_id": prospect.get("prospect_id"),
        "severity": severity,
        "reasons": reasons_active or reasons_contained,
        "may_cause_external_action": bool(reasons_active),
        "priority_class": ("stop_unsafe_external_action" if severity == UNSAFE_ACTIVE
                           else "resolve_blocking_evidence"),
    }


def rank_key(prospect: dict, as_of: date) -> tuple:
    """Expected commercial value, urgency, evidence confidence, effort. No maturity."""
    coverage = prospect.get("qualification_coverage") or {}
    by_dimension = coverage.get("by_dimension") or {}

    # Expected commercial value. Uses the qualification score and the commercial_fit
    # component where it exists. It never reads a route or a capability.
    commercial = (by_dimension.get("commercial_fit") or {}).get("score") or 0
    value = TIER_VALUE.get(prospect.get("qualification_tier"), 1) * 10 \
        + int(prospect.get("qualification_score") or 0) + commercial

    # Urgency. Fresher evidence and an overdue next action both raise it.
    age = _age(prospect.get("last_verified_at"), as_of)
    freshness = 0 if age is None else max(0, 30 - min(age, 30))
    due = _day(prospect.get("next_action_due_at"))
    overdue = (as_of - due).days if due and due < as_of else 0
    urgency = freshness + min(overdue, 30)

    # Evidence confidence, averaged over dimensions that actually cite evidence.
    scored = [CONFIDENCE_POINTS.get(item.get("confidence"), 0)
              for item in by_dimension.values() if item.get("evidence_ids")]
    confidence = round(sum(scored) / len(scored), 2) if scored else 0

    # Effort. Fewer missing dimensions means less work to make it actionable.
    missing = len([1 for item in by_dimension.values()
                   if item.get("research_status") == "required"])
    low_effort = len(by_dimension) - missing if by_dimension else 0

    return (-value, -urgency, -confidence, -low_effort, str(prospect.get("prospect_id") or ""))


def explain_rank(prospect: dict, as_of: date) -> dict:
    key = rank_key(prospect, as_of)
    return {
        "prospect_id": prospect.get("prospect_id"),
        "expected_commercial_value": -key[0],
        "urgency": -key[1],
        "evidence_confidence": -key[2],
        "low_effort": -key[3],
        "factors_used": list(RANK_ORDER),
        "factors_deliberately_excluded": ["route_maturity", "implementation_maturity"],
    }



# `advance_active_revenue` means a real commercial event has happened. Not a high
# score. Not a good prospect. An event, with a date and a source.
#
# A prospect that merely qualifies well and is blocked on evidence belongs in
# `resolve_blocking_evidence`. Treating a strong score as active revenue is how a
# pipeline reports momentum it does not have.
COMMERCIAL_EVENTS = (
    "reply_received",
    "active_conversation",
    "meeting_booked",
    "discovery_held",
    "proposal_sent",
    "in_negotiation",
    "explicit_buying_signal",
)


def commercial_event(prospect: dict) -> dict | None:
    """The real commercial event on this prospect, or None. Evidence required."""
    events = prospect.get("commercial_events") or []
    dated = [e for e in events
             if e.get("type") in COMMERCIAL_EVENTS and e.get("observed_at") and e.get("source")]
    if not dated:
        # Legacy shorthand fields, accepted only when they carry a date.
        for field, name in (("replied_at", "reply_received"),
                            ("meeting_booked_at", "meeting_booked"),
                            ("proposal_sent_at", "proposal_sent")):
            if prospect.get(field):
                return {"type": name, "observed_at": prospect[field], "source": field}
        return None
    dated.sort(key=lambda e: (COMMERCIAL_EVENTS.index(e["type"]), str(e["observed_at"])))
    return dated[-1]


def _class_members(snapshot: dict, as_of: date) -> dict[str, list]:
    prospects = snapshot.get("prospects", [])
    approvals = snapshot.get("approvals_waiting") or 0
    batches = snapshot.get("unresolved_batches") or []

    unsafe = [classify_unsafe(p, snapshot) for p in prospects
              if p.get("evidence_contradicted") or p.get("contact_state_conflict")]
    active = [u for u in unsafe if u["severity"] == UNSAFE_ACTIVE]
    contained = [u for u in unsafe if u["severity"] == UNSAFE_CONTAINED]
    contained_ids = {u["prospect_id"] for u in contained}

    def blocked(p):
        return (p.get("actionability") not in (None, "actionable")
                or bool(p.get("blocking_evidence")))

    # A real commercial event, not a high score. Qualification alone never qualifies
    # a prospect for this class.
    revenue = [p for p in prospects if commercial_event(p) is not None]

    # A blocked prospect is not a coverage problem. Enriching it cannot make it
    # advance while the block holds, so it belongs in resolve_blocking_evidence.
    # Tilz Prosperitas is the case that made this explicit: 83.3% coverage, but
    # blocked on an incomplete diagnostic, so more research is not the next move.
    coverage_gap = [p for p in prospects
                    if not p.get("contacted")
                    and p.get("qualification_tier") != "DO_NOT_PURSUE"
                    and not blocked(p)
                    and p["prospect_id"] not in contained_ids
                    and (p.get("qualification_tier") is None
                         or (p.get("qualification_coverage") or {}).get("percentage", 0) < 100)]

    followup = [p for p in prospects
                if p.get("contacted") and not p.get("reply_classified")]

    blocked_on_evidence = [
        {"prospect_id": p["prospect_id"], "severity": None,
         "reasons": [f"blocked by {p.get('actionability')}"],
         "priority_class": "resolve_blocking_evidence"}
        for p in prospects
        if blocked(p) and p["prospect_id"] not in contained_ids
        and commercial_event(p) is None
    ]

    return {
        "stop_unsafe_external_action": active,
        "advance_active_revenue": revenue,
        "complete_qualification_coverage": coverage_gap,
        "resolve_blocking_evidence": contained + blocked_on_evidence,
        "execute_due_followup_or_nurture": followup,
        "recover_overdue_research": [b for b in batches
                                     if (_age(b.get("updated_at"), as_of) or 0) > 2],
        "generate_new_supply": [],
    }


def select(snapshot: dict, cohort_size: int = 1) -> dict:
    """Choose one priority class, then rank inside it. Records why higher classes lost."""
    as_of = _day(snapshot.get("as_of"))
    if as_of is None:
        raise ValueError("snapshot needs an ISO `as_of`")

    members = _class_members(snapshot, as_of)
    supply_blocked = [name for name in PRIORITY_CLASSES[:-1] if members[name]]
    if not supply_blocked and snapshot.get("validated_new_market_gap"):
        members["generate_new_supply"] = [{"reason": "every higher class is empty and a market gap is validated"}]

    considered = []
    chosen = None
    for name in PRIORITY_CLASSES:
        entries = members[name]
        if entries and chosen is None:
            chosen = name
            considered.append({"priority_class": name, "selected": True, "candidates": len(entries)})
        else:
            considered.append({
                "priority_class": name,
                "selected": False,
                "candidates": len(entries),
                "why_not": ("nothing in this class today" if not entries
                            else f"a higher class, {chosen}, was selected first"),
            })

    if chosen is None:
        return {"priority_class": None, "objective_type": "nothing_to_do",
                "prospect_ids": [], "considered_classes": considered,
                "external_action_authorized": False}

    entries = members[chosen]
    if chosen in ("recover_overdue_research", "generate_new_supply"):
        ranked, ids = entries, []
        if chosen == "recover_overdue_research":
            batch = sorted(entries, key=lambda b: (str(b.get("updated_at") or ""),
                                                   str(b.get("batch_id") or "")))[0]
            ids = sorted(batch.get("prospect_ids", []))
            ranked = [batch]
    elif chosen in ("stop_unsafe_external_action", "resolve_blocking_evidence"):
        ranked = sorted(entries, key=lambda u: str(u["prospect_id"]))
        ids = [u["prospect_id"] for u in ranked[:cohort_size]]
    elif chosen == "complete_qualification_coverage":
        ranked_priority = rank_enrichment(entries, as_of, cohort_size)
        priority_by_id = {item["prospect_id"]: item for item in ranked_priority}
        ranked = sorted(entries, key=lambda p: (
            -priority_by_id.get(p.get("prospect_id"), {}).get("priority_score", -999),
            str(p.get("prospect_id") or "")))
        ids = [item["prospect_id"] for item in ranked_priority]
        if not ids:
            # The enrichment ranker has its own eligibility rules. A class with
            # candidates must still yield a cohort, so fall back to the standard
            # within-class ranking rather than returning an empty objective.
            ids = [p["prospect_id"] for p in ranked[:cohort_size]]
    else:
        ranked = sorted(entries, key=lambda p: rank_key(p, as_of))
        ids = [p["prospect_id"] for p in ranked[:cohort_size]]

    return {
        "priority_class": chosen,
        "priority_class_rank": PRIORITY_CLASSES.index(chosen) + 1,
        "objective_type": chosen,
        "prospect_ids": ids,
        "cohort_size": cohort_size,
        "candidates_in_class": len(entries),
        "considered_classes": considered,
        "ranking": (ranked_priority if chosen == "complete_qualification_coverage" else
                    [explain_rank(p, as_of) for p in ranked[:cohort_size]
                     if isinstance(p, dict) and p.get("qualification_coverage") is not None]),
        "unsafe_classification": [u for u in members["stop_unsafe_external_action"]]
                                 + [u for u in members["resolve_blocking_evidence"]],
        "supply_blocked_by": supply_blocked,
        "external_action_authorized": False,
    }
