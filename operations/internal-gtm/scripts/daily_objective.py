#!/usr/bin/env python3
"""Select one highest-value daily GTM objective without mutating any system."""

from __future__ import annotations

import hashlib
import json
import argparse
from datetime import date, datetime
from pathlib import Path

from enrichment_priority import rank as rank_enrichment


TIER_PRIORITY = {"HOT": 0, "STRONG": 1, "QUALIFIED": 2, "WATCH": 3,
                 "DO_NOT_PURSUE": 5, None: 4}
STAGE_PRIORITY = {
    "qualified": 0,
    "routed": 1,
    "diagnostic_selected": 2,
    "diagnostic_complete": 3,
    "offer_selected": 4,
    "outreach_prepared": 5,
    "awaiting_approval": 6,
}
ENRICHMENT_CAPABILITIES = {
    "commercial_fit": "bridgeworks-commercial-intelligence",
    "buyer_accessibility": "bridgeworks-buyer-intelligence",
    "problem_evidence": "client-audit",
    "trigger_urgency": "competitive-research",
    "proof_fit": "bridgeworks-prospect-router",
    # execution_readiness is about the prospect's delivery capacity and decision
    # process. bridgeworks-gtm-pipeline-health analyses the BridgeWorks pipeline,
    # which is a different target. Commercial Intelligence covers this dimension.
    "execution_readiness": "bridgeworks-commercial-intelligence",
}
DIMENSION_PRIORITY = ("commercial_fit", "buyer_accessibility", "execution_readiness",
                      "problem_evidence", "trigger_urgency", "proof_fit")
PRIORITY_CLASSES = (
    "stop_unsafe_external_action",
    "advance_active_revenue",
    "complete_qualification_coverage",
    "resolve_blocking_evidence",
    "execute_due_followup_or_nurture",
    "recover_overdue_research",
    "generate_new_supply",
)


class ObjectiveInputError(ValueError):
    pass


def _parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def _age_days(value: str | None, as_of: date) -> int | None:
    parsed = _parse_day(value)
    return (as_of - parsed).days if parsed else None


def _prospect_order(item: dict, as_of: date) -> tuple:
    due = _parse_day(item.get("next_action_due_at"))
    overdue_days = (as_of - due).days if due and due < as_of else 0
    return (
        TIER_PRIORITY.get(item.get("qualification_tier"), 4),
        -int(item.get("qualification_score") or 0),
        -overdue_days,
        STAGE_PRIORITY.get(item.get("lifecycle_stage"), 99),
        str(item.get("prospect_id") or ""),
    )


def _pick(items: list[dict], as_of: date) -> dict:
    return sorted(items, key=lambda item: _prospect_order(item, as_of))[0]


def _digest(snapshot: dict) -> str:
    return hashlib.sha256(
        json.dumps(snapshot, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def select_daily_objective(snapshot: dict) -> dict:
    """Return one objective. Missing critical reads block instead of becoming zero."""
    as_of_text = snapshot.get("as_of")
    as_of = _parse_day(as_of_text)
    if as_of is None:
        raise ObjectiveInputError("as_of must be an ISO date or datetime")

    critical = ("prospects", "approvals_waiting", "unresolved_batches")
    missing = [field for field in critical if snapshot.get(field) is None]
    objective_id = f"gtm-objective:{as_of.isoformat()}"
    base = {
        "objective_id": objective_id,
        "dedupe_key": objective_id,
        "as_of": as_of.isoformat(),
        "timezone": "Europe/Budapest",
        "external_action_authorized": False,
        "shadow_safe": True,
        "source_snapshot_digest": _digest(snapshot),
    }
    if missing:
        return {
            **base,
            "objective_type": "blocked_unverified",
            "prospect_ids": [],
            "reason_codes": [f"missing_input:{field}" for field in missing],
            "supply": {"allowed": False, "blockers": ["critical_state_unverified"]},
        }

    prospects = sorted(snapshot["prospects"], key=lambda item: str(item.get("prospect_id") or ""))
    approvals = int(snapshot["approvals_waiting"])
    batches = snapshot["unresolved_batches"]
    capacity = snapshot.get("capacity", {})
    target = int(capacity.get("qualified_untouched_target") or 0)
    approval_cap = int(capacity.get("approval_backlog_cap") or 0)

    untouched = [p for p in prospects if not p.get("contacted") and
                 p.get("qualification_tier") in ("HOT", "STRONG", "QUALIFIED")]
    unscored = [p for p in prospects if not p.get("contacted") and
                p.get("qualification_tier") is None]
    coverage_gaps = [p for p in prospects if not p.get("contacted") and
                     p.get("qualification_tier") not in (None, "DO_NOT_PURSUE") and
                     p.get("missing_qualification_dimensions")]
    unsafe_active = [p for p in prospects if p.get("unsafe_state") == "unsafe_active"]
    unsafe_contained = [p for p in prospects if p.get("unsafe_state") == "unsafe_contained"]
    overdue_batches = [b for b in batches if (_age_days(b.get("updated_at"), as_of) or 0) > 2]
    missing_evidence = [p for p in untouched if p.get("missing_evidence")]
    missing_buyers = [p for p in untouched if p.get("missing_buyer")]
    stale = [p for p in untouched if (_age_days(p.get("last_verified_at"), as_of) or 0) > 14]
    actionable = [
        p for p in untouched
        if not p.get("missing_evidence") and not p.get("missing_buyer")
        and not p.get("evidence_contradicted") and not p.get("contact_state_conflict")
    ]
    from objective_hierarchy import commercial_event
    active_revenue = [p for p in actionable if commercial_event(p) is not None]
    cohort_size = int(capacity.get("qualification_enrichment_batch_size") or 8)
    enrichment_cohort = rank_enrichment(prospects, as_of, cohort_size)

    metrics = {
        "qualified_untouched": len(untouched),
        "overdue_research": len(overdue_batches),
        "missing_evidence": len(missing_evidence),
        "missing_buyers": len(missing_buyers),
        "stale_states": len(stale),
        "approvals_waiting": approvals,
        "requires_qualification_v1": len(unscored),
        "qualification_coverage_gaps": len(coverage_gaps),
        "unsafe_active": len(unsafe_active),
        "unsafe_contained": len(unsafe_contained),
    }

    selected: dict
    if unsafe_active:
        p = _pick(unsafe_active, as_of)
        selected = {"priority_class": "stop_unsafe_external_action", "objective_type": "reconcile_unsafe_active_state", "prospect_ids": [p["prospect_id"]], "reason_codes": ["unsafe_active", *p.get("unsafe_reasons", [])]}
    elif active_revenue:
        p = _pick(active_revenue, as_of)
        selected = {"priority_class": "advance_active_revenue", "objective_type": "advance_qualified_prospect", "prospect_ids": [p["prospect_id"]], "reason_codes": ["actionable_qualified_revenue_work"]}
    elif unscored or coverage_gaps:
        selected = {
            "priority_class": "complete_qualification_coverage",
            "objective_type": "complete_qualification_coverage",
            "prospect_ids": [item["prospect_id"] for item in enrichment_cohort],
            "enrichment_cohort": enrichment_cohort,
            "reason_codes": ["canonical_qualification_missing_or_partial", "bounded_existing_prospect_cohort"],
        }
    elif unsafe_contained:
        p = _pick(unsafe_contained, as_of)
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "reconcile_unsafe_contained_state", "prospect_ids": [p["prospect_id"]], "reason_codes": ["unsafe_contained", *p.get("unsafe_reasons", [])]}
    elif missing_evidence:
        p = _pick(missing_evidence, as_of)
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "complete_missing_evidence", "prospect_ids": [p["prospect_id"]], "reason_codes": ["high_quality_untouched_missing_evidence"]}
    elif missing_buyers:
        p = _pick(missing_buyers, as_of)
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "complete_missing_buyer", "prospect_ids": [p["prospect_id"]], "reason_codes": ["high_quality_untouched_missing_decision_maker"]}
    elif stale:
        p = _pick(stale, as_of)
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "refresh_stale_prospect", "prospect_ids": [p["prospect_id"]], "reason_codes": ["qualified_untouched_over_14_days_since_verification"]}
    elif actionable:
        # Qualification is an investment decision, not evidence of live revenue.
        # Without a reply, conversation, meeting, discovery, proposal,
        # negotiation, or explicit buying signal this cannot be active revenue.
        p = _pick(actionable, as_of)
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "advance_precommercial_evidence", "prospect_ids": [p["prospect_id"]], "reason_codes": ["qualified_but_no_real_commercial_event"]}
    elif approvals:
        selected = {"priority_class": "resolve_blocking_evidence", "objective_type": "surface_approval_decision", "prospect_ids": [], "reason_codes": ["approval_backlog_requires_emmanuel"], "approval_count": approvals}
    elif overdue_batches:
        batch = sorted(overdue_batches, key=lambda b: (str(b.get("updated_at") or ""), str(b.get("batch_id") or "")))[0]
        selected = {"priority_class": "recover_overdue_research", "objective_type": "recover_overdue_research", "prospect_ids": sorted(batch.get("prospect_ids", [])), "reason_codes": ["prepared_or_in_research_over_2_days"], "batch_id": batch.get("batch_id")}
    elif snapshot.get("validated_new_market_gap") and len(untouched) >= target:
        selected = {"priority_class": "generate_new_supply", "objective_type": "investigate_new_market_need", "prospect_ids": [], "reason_codes": ["validated_market_gap_but_existing_coverage_sufficient"]}
    else:
        supply_blockers = []
        if len(untouched) >= target:
            supply_blockers.append("qualified_untouched_coverage_sufficient")
        if approvals > approval_cap:
            supply_blockers.append("approval_backlog_above_cap")
        if batches:
            supply_blockers.append("unresolved_research_exists")
        if not snapshot.get("validated_new_market_gap"):
            supply_blockers.append("no_validated_priority_market_gap")
        allowed = not supply_blockers
        selected = {
            "priority_class": "generate_new_supply",
            "objective_type": "generate_new_companies" if allowed else "hold_supply",
            "prospect_ids": [],
            "reason_codes": ["supply_gate_passed"] if allowed else supply_blockers,
        }

    supply_allowed = selected["objective_type"] == "generate_new_companies"
    chosen_index = PRIORITY_CLASSES.index(selected.get("priority_class", "generate_new_supply"))
    selected["higher_classes_not_selected"] = [
        {"priority_class": name, "reason": {
            "stop_unsafe_external_action": "no unsafe_active state detected",
            "advance_active_revenue": "no evidenced reply, active conversation, meeting, discovery, proposal, negotiation, or explicit buying signal detected",
            "complete_qualification_coverage": "no missing or partial qualification-v1 coverage detected",
            "resolve_blocking_evidence": "no higher-value blocking evidence task detected",
            "execute_due_followup_or_nurture": "no verified due follow-up or nurture task detected",
            "recover_overdue_research": "no overdue prepared or in-research batch detected",
        }.get(name, "not selected")}
        for name in PRIORITY_CLASSES[:chosen_index]
    ]
    return {
        **base,
        **selected,
        "metrics": metrics,
        "supply": {
            "allowed": supply_allowed,
            "target": target,
            "current": len(untouched),
            "blockers": [] if supply_allowed else selected.get("reason_codes", []),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = select_daily_objective(json.loads(args.input.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"objective: {result['objective_type']}")
        print(f"written: {args.out}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
