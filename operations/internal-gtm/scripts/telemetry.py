#!/usr/bin/env python3
"""GTM outcome telemetry: one record per prospect per attempt, and the comparisons.

HOW TO USE
    python operations/internal-gtm/scripts/telemetry.py build --runs operations/internal-gtm/runs/geo
    python operations/internal-gtm/scripts/telemetry.py compare --by primary_service_route

`build` turns internal-GTM run records into telemetry rows and writes them to
`runs/telemetry/gtm-telemetry.jsonl`, keyed so a re-run updates rather than
duplicates. `compare` is what the GTM Learning role reads: counts and rates by any
decision dimension.

The rule that makes this worth keeping: a null outcome means unknown, never no. A
prospect with `sent_at: null` has not been contacted, so it belongs in no
conversion denominator. Rates are computed over prospects that actually reached
the stage, and every rate reports its denominator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qualification_v1 as qv1  # noqa: E402

GTM_ROOT = Path(__file__).resolve().parents[1]
STORE = GTM_ROOT / "runs" / "telemetry" / "gtm-telemetry.jsonl"
SCHEMA = GTM_ROOT / "schemas" / "gtm-telemetry.schema.json"
RECONCILIATION = GTM_ROOT / "migration" / "phase-3" / "prospect-reconciliation.json"

DECISION_DIMENSIONS = (
    "market", "segment", "trigger_type", "buyer_role", "buyer_reachability",
    "qualification_score", "qualification_tier", "problem_evidence",
    "commercial_fit", "buyer_accessibility", "trigger_urgency", "proof_fit",
    "execution_readiness", "qualification_coverage_dimensions",
    "qualification_coverage_percentage", "primary_service_route",
    "route_fit", "route_won_on", "diagnostic_capability", "diagnostic_score",
    "diagnostic_result", "evidence_quality", "proof_asset_id", "offer_hypothesis",
    "outreach_angle", "channel",
)

# Each funnel step and the field that proves it happened. Order matters.
FUNNEL = (
    ("prepared", "approval_state"),
    ("sent", "sent_at"),
    ("replied", "reply_classification"),
    ("positive", "positive_reply"),
    ("meeting", "meeting_booked_at"),
    ("proposal", "proposal_sent_at"),
    ("won", "final_state"),
)


def _repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(GTM_ROOT.parents[1])).replace("\\", "/")
    except ValueError:
        return str(resolved).replace("\\", "/")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def from_run_record(record: dict, run_path: Path) -> dict:
    """Build a telemetry row from an internal-GTM run record. Decisions only."""
    prospect = record.get("prospect") or {}
    route = record.get("route") or {}
    qualification = record.get("qualification") or {}
    evidence = record.get("evidence") or {}
    offer = record.get("offer") or {}
    packet = record.get("packet") or {}
    trigger = record.get("trigger") or {}
    signals = next((s.get("signals") for s in record.get("steps", []) if s.get("signals")), {}) or {}
    diagnostic_step = next((s for s in record.get("steps", []) if s.get("capability")), {})
    component_scores = qualification.get("component_scores") or {}
    coverage = (qualification.get("qualification_coverage") or
                qv1.coverage_from_scored_components(qualification.get("components") or {}))

    if record.get("blocked_on"):
        diagnostic_result = "blocked"
    elif diagnostic_step:
        diagnostic_result = "complete"
    else:
        diagnostic_result = "not_run"

    prospect_id = prospect.get("prospect_id") or "unknown"
    return {
        "record_id": f"{prospect_id}@{record.get('as_of')}",
        "prospect_id": prospect_id,
        "entity_key": prospect.get("entity_key"),
        "as_of": record.get("as_of"),
        "decision": {
            "market": record.get("market"),
            "segment": record.get("segment"),
            "trigger_type": trigger.get("type"),
            "trigger_age_days": signals.get("trigger_age_days"),
            "buyer_role": prospect.get("buyer_role"),
            "buyer_reachability": signals.get("reachability"),
            "qualification_score": qualification.get("score"),
            "qualification_tier": qualification.get("tier"),
            "qualification_version": qualification.get("model") or qualification.get("qualification_version"),
            "actionability": qualification.get("actionability"),
            **{name: (qualification.get("component_scores") or {}).get(name)
               for name in ("problem_evidence", "commercial_fit", "buyer_accessibility",
                            "trigger_urgency", "proof_fit", "execution_readiness")},
            "qualification_version": qualification.get("qualification_version") or qualification.get("model"),
            "problem_evidence": component_scores.get("problem_evidence"),
            "commercial_fit": component_scores.get("commercial_fit"),
            "buyer_accessibility": component_scores.get("buyer_accessibility"),
            "trigger_urgency": component_scores.get("trigger_urgency"),
            "proof_fit": component_scores.get("proof_fit"),
            "execution_readiness": component_scores.get("execution_readiness"),
            "qualification_coverage_dimensions": coverage.get("sufficiently_researched_dimensions"),
            "qualification_coverage_percentage": coverage.get("percentage"),
            "primary_service_route": route.get("route_id"),
            "route_fit": route.get("fit"),
            "route_won_on": route.get("won_on"),
            "secondary_routes": route.get("secondary_routes", []) or [],
            "diagnostic_capability": route.get("diagnostic_capability"),
            "diagnostic_score": diagnostic_step.get("score"),
            "diagnostic_result": diagnostic_result,
            "evidence_quality": evidence.get("evidence_quality"),
            "approved_claim_count": len(evidence.get("approved_claim_ids", []) or []),
            "contradicted_claim_count": (evidence.get("counts") or {}).get("contradicted"),
            "proof_asset_id": offer.get("proof_asset_id"),
            "offer_hypothesis": offer.get("wedge"),
            "outreach_angle": (trigger.get("summary") or None),
            "channel": "email" if prospect.get("buyer_email") else None,
        },
        "outcome": {
            "approval_state": packet.get("approval_state"),
            "approval_payload_digest": packet.get("approval_payload_digest"),
            "sent_at": None,
            "sent_message_id": None,
            "reply_classification": None,
            "positive_reply": None,
            "meeting_booked_at": None,
            "proposal_sent_at": None,
            "final_state": None,
            "revenue_if_won": None,
            "revenue_currency": None,
        },
        "provenance": {
            "run_record": _repo_relative(run_path),
            "written_by": "operations/internal-gtm/scripts/telemetry.py",
            "outcome_sources": [
                "sent_at and sent_message_id come from Gmail only, which is communication ground truth",
                "reply_classification comes from the reply-intelligence role, never from a timer",
                "revenue_if_won comes from an issued szamlazz.hu invoice, never from a proposal",
            ],
            "external_action_authorized": False,
        },
    }


def _field(entity: dict, name: str):
    return ((entity.get("fields") or {}).get(name) or {}).get("value")


def from_reconciled_entity(entity: dict, as_of: str, source_path: Path) -> dict:
    """Create a truthful telemetry baseline for a prospect without a GTM run.

    Unknown decisions and outcomes remain null. Communication and approval facts
    are copied only from their provenance-bearing canonical fields.
    """
    entity_key = entity.get("entity_key")
    entity_digest = hashlib.sha256(str(entity_key).encode("utf-8")).hexdigest()[:8]
    prospect_id = _field(entity, "prospect_id")
    if not prospect_id:
        prospect_id = "entity-" + entity_digest
    return {
        "record_id": f"{prospect_id}@canonical-{as_of}-{entity_digest}",
        "prospect_id": prospect_id,
        "entity_key": entity_key,
        "as_of": as_of,
        "decision": {
            "market": None,
            "segment": _field(entity, "lane"),
            "trigger_type": None,
            "trigger_age_days": None,
            "buyer_role": None,
            "buyer_reachability": "generic_contact" if _field(entity, "buyer_email") else "none",
            "qualification_score": None,
            "qualification_tier": None,
            "qualification_version": None,
            "problem_evidence": None,
            "commercial_fit": None,
            "buyer_accessibility": None,
            "trigger_urgency": None,
            "proof_fit": None,
            "execution_readiness": None,
            "qualification_coverage_dimensions": None,
            "qualification_coverage_percentage": None,
            "primary_service_route": None,
            "route_fit": None,
            "route_won_on": None,
            "secondary_routes": [],
            "diagnostic_capability": None,
            "diagnostic_score": None,
            "diagnostic_result": "not_run",
            "evidence_quality": None,
            "approved_claim_count": None,
            "contradicted_claim_count": None,
            "proof_asset_id": None,
            "offer_hypothesis": None,
            "outreach_angle": None,
            "channel": "email" if _field(entity, "buyer_email") else None,
        },
        "outcome": {
            "approval_state": _field(entity, "approval_state"),
            "approval_payload_digest": _field(entity, "approval_payload_digest"),
            "sent_at": _field(entity, "sent_at"),
            "sent_message_id": _field(entity, "sent_message_id"),
            "reply_classification": None,
            "positive_reply": None,
            "meeting_booked_at": None,
            "proposal_sent_at": None,
            "final_state": None,
            "revenue_if_won": None,
            "revenue_currency": None,
        },
        "provenance": {
            "run_record": _repo_relative(source_path),
            "written_by": "operations/internal-gtm/scripts/telemetry.py",
            "outcome_sources": [
                "sent_message_id and sent_at come only from the reconciled Gmail evidence",
                "approval_state and digest come only from the reconciled Mission Control task",
                "all absent decisions and outcomes remain null",
            ],
            "external_action_authorized": False,
        },
    }


def build(runs_dir: Path, store: Path = STORE, reconciliation_path: Path = RECONCILIATION) -> dict:
    existing: dict[str, dict] = {}
    if store.is_file():
        for line in store.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["record_id"]] = row

    added, updated, skipped = 0, 0, 0
    rows_to_write: list[dict] = []
    represented_entity_keys: set[str] = set()
    for path in sorted(runs_dir.glob("*.json")):
        record = _read_json(path)
        if not record.get("prospect"):
            skipped += 1
            continue
        row = from_run_record(record, path)
        rows_to_write.append(row)
        if row.get("entity_key"):
            represented_entity_keys.add(row["entity_key"])

    reconciliation = _read_json(reconciliation_path) if reconciliation_path.is_file() else {}
    for entity in reconciliation.get("entities", []):
        if entity.get("entity_key") in represented_entity_keys:
            continue
        rows_to_write.append(from_reconciled_entity(
            entity, reconciliation.get("as_of") or "unknown", reconciliation_path))

    for row in rows_to_write:
        previous = existing.get(row["record_id"])
        if previous:
            # Never clobber a real outcome with a null from a decision-only rebuild.
            row["outcome"] = {k: (previous["outcome"].get(k) if previous["outcome"].get(k) is not None else v)
                              for k, v in row["outcome"].items()}
            updated += 1
        else:
            added += 1
        existing[row["record_id"]] = row

    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(
        "\n".join(json.dumps(existing[k], ensure_ascii=False) for k in sorted(existing)) + "\n",
        encoding="utf-8")
    return {"added": added, "updated": updated, "skipped": skipped, "total": len(existing),
            "canonical_entities_considered": len(reconciliation.get("entities", []))}


def load(store: Path = STORE) -> list[dict]:
    if not store.is_file():
        return []
    return [json.loads(line) for line in store.read_text(encoding="utf-8").splitlines() if line.strip()]


def _reached(row: dict, field: str) -> bool:
    outcome = row["outcome"]
    value = outcome.get(field)
    # Funnel stages are cumulative. A verified send proves preparation happened
    # even when a legacy approval receipt is unavailable; a reply proves send,
    # and so on. This prevents disjoint historical sources from producing an
    # invalid numerator that is not a subset of its denominator.
    later_fields = {
        "approval_state": ("sent_at", "reply_classification", "positive_reply",
                           "meeting_booked_at", "proposal_sent_at", "final_state"),
        "sent_at": ("reply_classification", "positive_reply", "meeting_booked_at",
                    "proposal_sent_at", "final_state"),
        "reply_classification": ("positive_reply", "meeting_booked_at",
                                 "proposal_sent_at", "final_state"),
        "positive_reply": ("meeting_booked_at", "proposal_sent_at", "final_state"),
        "meeting_booked_at": ("proposal_sent_at", "final_state"),
        "proposal_sent_at": ("final_state",),
    }
    if any(outcome.get(name) not in (None, False) for name in later_fields.get(field, ())):
        return True
    if field == "positive_reply":
        return value is True
    if field == "final_state":
        return value == "won"
    return value is not None


def compare(rows: list[dict], dimension: str) -> dict:
    """Funnel counts and rates by one decision dimension, with denominators."""
    if dimension not in DECISION_DIMENSIONS:
        raise ValueError(f"unknown dimension: {dimension}. Known: {', '.join(DECISION_DIMENSIONS)}")
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[str(row["decision"].get(dimension))].append(row)

    result = {}
    for key in sorted(groups):
        group = groups[key]
        counts = {name: sum(1 for r in group if _reached(r, field)) for name, field in FUNNEL}
        rates = {}
        for index in range(1, len(FUNNEL)):
            name, _ = FUNNEL[index]
            previous_name, _ = FUNNEL[index - 1]
            denominator = counts[previous_name]
            rates[f"{previous_name}_to_{name}"] = {
                "numerator": counts[name],
                "denominator": denominator,
                "rate": round(counts[name] / denominator, 3) if denominator else None,
            }
        result[key] = {"prospects": len(group), "counts": counts, "rates": rates}
    return {
        "dimension": dimension,
        "groups": result,
        "note": ("A null outcome means unknown, not no. A rate with a zero denominator is null, "
                 "not zero, because nothing reached that stage yet."),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "compare", "dimensions"))
    parser.add_argument("--runs", type=Path, default=GTM_ROOT / "runs" / "geo")
    parser.add_argument("--by", default="primary_service_route")
    parser.add_argument("--store", type=Path, default=STORE)
    args = parser.parse_args()

    if args.command == "dimensions":
        print("\n".join(DECISION_DIMENSIONS))
        return 0
    if args.command == "build":
        stats = build(args.runs, args.store)
        print(f"telemetry: {stats}")
        print(f"store: {args.store}")
        return 0
    rows = load(args.store)
    if not rows:
        print("no telemetry rows yet", file=sys.stderr)
        return 1
    print(json.dumps(compare(rows, args.by), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
