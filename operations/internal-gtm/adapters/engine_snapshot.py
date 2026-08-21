#!/usr/bin/env python3
"""Read-only snapshot of the acquisition engine, shaped for the daily objective selector.

HOW TO USE
    python operations/internal-gtm/adapters/engine_snapshot.py --as-of 2026-08-11
    python operations/internal-gtm/adapters/engine_snapshot.py --as-of 2026-08-11 --select

`--select` pipes the snapshot straight into daily_objective.select_daily_objective
and prints the chosen objective. The selector is a pure function over a snapshot.
This module is the only thing that knows where the acquisition engine keeps state,
and it never writes to it.

A field this adapter cannot verify is emitted as null, not as zero. The selector
treats a null critical field as `blocked_unverified`, which is the correct answer:
an unread connector is not an empty one.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
ENGINE = REPO_ROOT / "operations" / "client-acquisition-engine"
OPS = ENGINE / "research" / "prospect-operations"
RUNS = GTM_ROOT / "runs" / "geo"
QUALIFICATION_BATCHES = GTM_ROOT / "runs" / "qualification-batches"
RECONCILIATION = GTM_ROOT / "migration" / "phase-3" / "prospect-reconciliation.json"
MISSION_QUEUE = (REPO_ROOT.parent / "emmanuel-os-context" / "00-command-center" /
                 "mission-control" / "orchestrator-queue.json")

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import qualification_v1 as qv1  # noqa: E402
import contacted_companies as canonical_contacts  # noqa: E402

CONTACT_COLUMNS = ("first_contact_sent", "follow_up_1_sent", "follow_up_2_sent", "linkedin_touch")
MAX_RESEARCH_ATTEMPTS = 2

# Capacity is a decision, not a measurement. These are the current settings.
CAPACITY = {"qualified_untouched_target": 4, "approval_backlog_cap": 3}


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _named_decision_maker(record: dict) -> bool:
    text = (record.get("decision_maker") or "").strip().lower()
    return bool(text) and not text.startswith("no current named")


def internal_gtm_qualifications() -> dict[str, dict]:
    """Real tiers from internal-GTM run records, keyed by prospect id."""
    found: dict[str, dict] = {}
    if not RUNS.is_dir():
        return found
    for path in sorted(RUNS.glob("*.json")):
        record = _read_json(path, {})
        pid = (record.get("prospect") or {}).get("prospect_id")
        qualification = record.get("qualification") or {}
        if not pid or not qualification:
            continue
        previous = found.get(pid)
        if previous is None or record.get("as_of", "") >= previous.get("as_of", ""):
            found[pid] = {
                "tier": qualification.get("tier"),
                "score": qualification.get("score"),
                "stage": record.get("lifecycle_stage"),
                "as_of": record.get("as_of"),
                "contradicted": bool((record.get("evidence") or {}).get("counts", {}).get("contradicted")),
                "coverage": (qualification.get("qualification_coverage") or
                             qv1.coverage_from_scored_components(qualification.get("components") or {})),
                "actionability": qualification.get("actionability"),
            }
    if QUALIFICATION_BATCHES.is_dir():
        for path in sorted(QUALIFICATION_BATCHES.glob("*.json")):
            batch = _read_json(path, {})
            as_of = batch.get("as_of", "")
            for item in batch.get("prospects", []):
                pid = item.get("prospect_id")
                qualification = item.get("qualification_v1") or {}
                if not pid or not qualification:
                    continue
                previous = found.get(pid)
                if previous is None or as_of >= previous.get("as_of", ""):
                    found[pid] = {
                        "tier": qualification.get("tier"),
                        "score": qualification.get("score"),
                        "stage": "qualified",
                        "as_of": as_of,
                        "contradicted": "materially_contradicted_evidence" in
                            (qualification.get("blocking_reasons") or []),
                        "coverage": qualification.get("qualification_coverage") or {},
                        "actionability": qualification.get("actionability"),
                    }
    return found


def latest_results() -> dict[str, dict]:
    results: dict[str, dict] = {}
    for path in sorted((OPS / "results").glob("*.json")):
        for record in _read_json(path, {}).get("prospects", []):
            pid = record.get("prospect_id")
            if not pid:
                continue
            previous = results.get(pid)
            if previous is None or str(record.get("checked_at", "")) >= str(previous.get("checked_at", "")):
                results[pid] = record
    return results


def contacted_ids() -> set[str] | None:
    """Resolve contact truth from the canonical read-only reconciliation.

    The generated register remains a fallback for pre-Phase-3 installations.
    """
    source = OPS / "prospect-source-current.csv"
    if RECONCILIATION.is_file() and source.is_file():
        report = canonical_contacts.accounting(date.today().isoformat())
        contacted_domains = {
            row["entity_key"].split(":", 1)[1]
            for row in report.get("contacted_companies", [])
            if str(row.get("entity_key", "")).startswith("domain:")
        }
        found: set[str] = set()
        with source.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                domain = (row.get("canonical_domain") or "").strip().lower()
                if domain in contacted_domains and row.get("prospect_id"):
                    found.add(row["prospect_id"])
        return found

    register = OPS / "operating-output" / "canonical-prospect-register.csv"
    if not register.is_file():
        return None
    found: set[str] = set()
    with register.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if any((row.get(column) or "").strip() for column in CONTACT_COLUMNS) and row.get("prospect_id"):
                found.add(row["prospect_id"])
    return found


def approvals_waiting() -> int | None:
    """Count current acquisition approvals in Mission Control.

    The review state is a historical preparation store and is only a fallback.
    """
    queue = _read_json(MISSION_QUEUE, None)
    if isinstance(queue, list):
        return sum(1 for task in queue
                   if task.get("lane") == "acquisition" and task.get("status") == "awaiting_approval")
    state = _read_json(OPS / "review" / "prospect-review-state.json", None)
    if not isinstance(state, dict):
        return None
    total = 0
    for batch in state.get("batches", {}).values():
        total += len(batch.get("external_tasks", []) or [])
    return total


def unresolved_batches(state: dict) -> list[dict]:
    open_batches = []
    for batch in state.get("batches", []) or []:
        if batch.get("status") in {"prepared", "in_research"}:
            payload = _read_json(Path(str(batch.get("json_path", ""))), {})
            ids = [item.get("prospect_id") for item in payload.get("prospects", []) if item.get("prospect_id")]
            open_batches.append({
                "batch_id": batch.get("batch_id") or batch.get("date"),
                "updated_at": batch.get("updated_at") or batch.get("date"),
                "prospect_ids": sorted(ids),
            })
    return sorted(open_batches, key=lambda item: (str(item["updated_at"]), str(item["batch_id"])))


def build(as_of: str) -> dict:
    research_state = _read_json(OPS / "prospect-research-state.json", {"prospects": {}, "batches": []})
    per_prospect = research_state.get("prospects", {})
    results = latest_results()
    contacted = contacted_ids()
    scored = internal_gtm_qualifications()

    prospects = []
    provisional = 0
    for pid in sorted(results):
        record = results[pid]
        engine_row = per_prospect.get(pid, {})
        readiness = record.get("outreach_readiness")
        attempts = int(engine_row.get("research_attempts", 0))
        qualification = scored.get(pid)
        if qualification:
            tier, score, stage = qualification["tier"], qualification["score"], qualification["stage"]
            source = "internal-gtm"
            contradicted = qualification["contradicted"]
            coverage = qualification.get("coverage") or {}
            actionability = qualification.get("actionability")
        else:
            # Engine readiness is compatibility evidence, not qualification.
            # Only qualification-v1 may own a score, tier, or qualified stage.
            tier, score, stage = None, None, "evidence_collected"
            source = "unscored_requires_qualification_v1"
            contradicted = False
            coverage = {
                "sufficiently_researched_dimensions": 0,
                "total_dimensions": 6,
                "percentage": 0.0,
                "by_dimension": {
                    name: {"research_status": "required", "evidence_state": "unknown",
                           "evidence_ids": [], "confidence": "unknown", "score": 0}
                    for name in ("problem_evidence", "commercial_fit", "buyer_accessibility",
                                 "trigger_urgency", "proof_fit", "execution_readiness")
                },
            }
            provisional += 1
            actionability = "research_required"
        is_contacted = None if contacted is None else pid in contacted
        source_text = " ".join(str(source.get("supports") or "") for source in record.get("sources", []))
        commercial_gap = str(record.get("commercial_gap") or "").strip()
        observations = record.get("observations") or []
        # Only a structured public destination counts. The historical contact_route
        # field often contains prose such as "no named buyer was found".
        destination = str(record.get("proposed_destination") or "").strip()
        named_buyer = _named_decision_maker(record)
        scale_terms = ("employees", "customers", "countries", "cities", "locations", "years",
                       "funding", "finance", "contract", "revenue", "export", "markets")
        scale_hits = sum(1 for term in scale_terms if term in source_text.lower())
        trigger_terms = ("new ", "launch", "expand", "growth", "hiring", "transition", "finance",
                         "current", "visible", "asks", "quote", "active")
        trigger_hits = sum(1 for term in trigger_terms
                           if term in (commercial_gap + " " + " ".join(observations)).lower())
        unsafe_state = "none"
        unsafe_reasons = []
        if contradicted or (bool(is_contacted) and readiness == "ready"):
            approval_executable = stage in {"outreach_prepared", "awaiting_approval"}
            shared_contamination = bool(record.get("shared_state_contamination"))
            multi_prospect = bool(record.get("multi_prospect_impact"))
            external_risk = approval_executable or bool(record.get("external_action_possible"))
            if external_risk or shared_contamination or multi_prospect:
                unsafe_state = "unsafe_active"
                unsafe_reasons = [name for name, value in {
                    "external_action_possible": external_risk,
                    "shared_state_contamination": shared_contamination,
                    "multi_prospect_impact": multi_prospect,
                    "executable_approval": approval_executable,
                }.items() if value]
            else:
                unsafe_state = "unsafe_contained"
                unsafe_reasons = ["isolated", "lifecycle_blocks_advancement", "no_executable_approval"]
        prospects.append({
            "prospect_id": pid,
            "company": record.get("company"),
            "qualification_tier": tier,
            "qualification_score": score,
            "qualification_source": source,
            "lifecycle_stage": stage,
            "contacted": bool(is_contacted),
            "missing_evidence": readiness == "needs_more_evidence" and attempts < MAX_RESEARCH_ATTEMPTS,
            "missing_buyer": not _named_decision_maker(record),
            "evidence_contradicted": contradicted,
            "contact_state_conflict": bool(is_contacted) and readiness == "ready",
            "unsafe_state": unsafe_state,
            "unsafe_reasons": unsafe_reasons,
            "actionability": actionability,
            "last_verified_at": (record.get("checked_at") or "")[:10] or None,
            "engine_readiness": readiness,
            "existing_trigger": record.get("recommended_angle") or commercial_gap or None,
            "problem_evidence": commercial_gap or (observations[0] if observations else None),
            "problem_evidence_present": bool(commercial_gap or observations),
            "trigger_strength_signal": min(20, 4 + trigger_hits * 3) if trigger_hits else 0,
            "buyer_evidence_signal": 15 if named_buyer and destination else 10 if named_buyer else 7 if destination else 0,
            "proof_fit_present": bool(record.get("proof_to_use")),
            "company_attractiveness_signal": min(15, scale_hits * 3),
            "decision_maker": record.get("decision_maker"),
            "contact_route": destination or None,
            "proof_to_use": record.get("proof_to_use"),
            "source_evidence": record.get("sources") or [],
            "qualification_coverage": coverage,
            "missing_qualification_dimensions": sorted(
                name for name, item in (coverage.get("by_dimension") or {}).items()
                if item.get("research_status") in {"required", "partial"}),
        })

    return {
        "as_of": as_of,
        "prospects": prospects,
        "approvals_waiting": approvals_waiting(),
        "unresolved_batches": unresolved_batches(research_state),
        "validated_new_market_gap": False,
        "capacity": CAPACITY,
        "_provenance": {
            "engine": "operations/client-acquisition-engine",
            "adapter": "operations/internal-gtm/adapters/engine_snapshot.py",
            "read_only": True,
            "prospects_scored_by_internal_gtm": len(scored),
            "prospects_requiring_qualification_v1": provisional,
            "qualification_ownership_rule": (
                "Acquisition-engine outreach_readiness is retained as compatibility evidence only. "
                "It never creates a qualification score, tier, or qualified lifecycle stage."
            ),
            "validated_new_market_gap_rule": (
                "false until a market-discovery slice run records a route with no qualified depth. "
                "It is not assumed, so the supply gate stays closed by default."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--select", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    snapshot = build(args.as_of)
    payload = snapshot
    if args.select:
        from daily_objective import select_daily_objective

        payload = {"snapshot_provenance": snapshot["_provenance"],
                   "objective": select_daily_objective(snapshot)}
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
