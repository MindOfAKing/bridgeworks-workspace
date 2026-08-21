#!/usr/bin/env python3
"""Build the canonical first-batch receipt and verifiable lifecycle receipts.

This is a reconciliation utility. It reads historical artifacts, writes only
internal GTM receipts/snapshots, and never calls an external connector.
"""

from __future__ import annotations

import json
from pathlib import Path

from transitions import append_receipt, load_receipts, receipt, reconstruct

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
SOURCE_REL = "operations/internal-gtm/runs/qualification-batches/internal-gtm-qualification-2026-08-11-01.json"
CLAUDE_REL = "operations/internal-gtm/runs/batches/gtm-batch-2026-08-11.json"
GEO_REL = "operations/internal-gtm/runs/geo/premier-fm-2026-08-11.json"
OUT_DIR = GTM_ROOT / "runs" / "canonical-batches"
SNAP_DIR = OUT_DIR / "evidence"
OUT_FILE = OUT_DIR / "first-real-gtm-batch-2026-08-11.json"
RUNTIME = "canonical-reconciliation"


def read(rel: str) -> dict:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def qualification_model(q: dict) -> dict:
    coverage = q.get("qualification_coverage") or {}
    return {
        **q,
        "model": q.get("model") or q.get("qualification_version") or "qualification-v1",
        "qualification_coverage": {
            **coverage,
            "exhausted_unknown_dimensions": coverage.get("exhausted_unknown_dimensions", []),
        },
    }


def evidence_ledger(q: dict) -> dict:
    entries = []
    for name, component in q.get("components", {}).items():
        sources = component.get("source_provenance") or [SOURCE_REL]
        for index, evidence_id in enumerate(component.get("approved_evidence_ids") or component.get("evidence_ids") or []):
            entries.append({
                "id": evidence_id,
                "status": "verified" if component.get("confidence") == "high" else "observed",
                "value": {"dimension": name, "component_score": component.get("score")},
                "source": sources[min(index, len(sources) - 1)],
                "observed_at": q.get("as_of", "2026-08-11"),
            })
    if not entries:
        entries.append({"id": "reconciliation-source", "status": "observed",
                        "value": "historical qualification snapshot", "source": SOURCE_REL,
                        "observed_at": "2026-08-11"})
    return {"ledger": entries}


def ensure_chain(prospect_id: str, q: dict, ledger: dict, snapshot_rel: str,
                 target: str, diagnostic: dict) -> list[dict]:
    sequence = [
        ("account_discovered", "evidence_collected", "evidence-auditor"),
        ("evidence_collected", "qualified", "bridgeworks-lead-qualifier"),
        ("qualified", "routed", "bridgeworks-prospect-router"),
    ]
    if target == "diagnostic_selected":
        sequence.append(("routed", "diagnostic_selected", diagnostic["capability"]))

    history = load_receipts(prospect_id)
    completed = {item["to_stage"] for item in history}
    for from_stage, to_stage, capability in sequence:
        if to_stage in completed:
            continue
        entry = receipt(
            prospect_id, from_stage, to_stage,
            triggering_capability=capability,
            ledger=ledger,
            qualification=q,
            diagnostic={"diagnostic_id": diagnostic.get("diagnostic_id"),
                        "status": diagnostic.get("status", "not_run")},
            approval_id=None,
            runtime=RUNTIME,
            history=history,
            evidence_snapshot_path=snapshot_rel,
        )
        append_receipt(entry)
        history.append({**entry, "kind": "transition_receipt"})
        completed.add(to_stage)
    return history


def prospect_receipt(p: dict) -> dict:
    pid = p["prospect_id"]
    q = qualification_model(p["qualification_v1"])
    coverage = q["qualification_coverage"]
    diagnostic = p.get("diagnostic") or {}
    target = "routed"
    status = "not_run"
    objective = "complete_qualification_coverage"
    next_action = p.get("next_action") or "complete_stage_2_coverage"
    superseded = []

    if pid == "arc-solutions-limited":
        next_action = "Evidence Auditor reviews the completed Stage 2 receipt, then qualification-v1 reruns"
    elif pid == "tilz-prosperitas":
        target = "diagnostic_selected"
        status = "blocked_partial"
        objective = "resolve_blocking_evidence"
        next_action = "complete the bounded missing GEO specialists and aggregate; otherwise return to research"
    elif pid == "bv-integrated-ltd":
        target = "diagnostic_selected"
        status = "selected_pending_workflow_owner_validation"
        objective = "resolve_blocking_evidence"
        next_action = "validate the workflow hypothesis with an approved owner before accepting the diagnostic"

    diagnostic_record = {
        "capability": p.get("selected_diagnostic_capability") or diagnostic.get("capability"),
        "diagnostic_id": (diagnostic.get("detail") or {}).get("run_id") or
                         ("tilz-prosperitas-geo-audit-2026-08-11" if pid == "tilz-prosperitas" else
                          "bv-integrated-ai-workflow-scan-2026-08-11" if pid == "bv-integrated-ltd" else None),
        "status": status,
    }
    snapshot = {
        "prospect_id": pid, "company": p["company"], "as_of": "2026-08-11",
        "existing_trigger": p.get("existing_trigger"),
        "problem_evidence": p.get("problem_evidence"),
        "qualification_v1": q,
        "commercial_intelligence": p.get("commercial_intelligence"),
        "buyer_intelligence": p.get("buyer_intelligence"),
        "selected_service_route": p.get("selected_service_route"),
        "diagnostic": diagnostic,
        "source_batch": SOURCE_REL,
    }
    snapshot_path = SNAP_DIR / f"{pid}-2026-08-11.json"
    write_json(snapshot_path, snapshot)
    snapshot_rel = snapshot_path.relative_to(REPO_ROOT).as_posix()
    ledger = evidence_ledger(q)
    history = ensure_chain(pid, q, ledger, snapshot_rel, target, diagnostic_record)
    state = reconstruct(pid, history)

    return {
        "prospect_id": pid,
        "company": p["company"],
        "qualification_score": q["score"],
        "tier": q["tier"],
        "actionability": q.get("actionability"),
        "qualification_coverage": coverage.get("percentage"),
        "missing_dimensions": coverage.get("missing_dimensions", []),
        "partial_dimensions": coverage.get("partial_dimensions", []),
        "exhausted_unknown_dimensions": coverage.get("exhausted_unknown_dimensions", []),
        "current_lifecycle_stage": state["canonical_lifecycle_stage"],
        "diagnostic_id": diagnostic_record["diagnostic_id"],
        "diagnostic_status": diagnostic_record["status"],
        "current_objective": objective,
        "valid_approval_packet_id": None,
        "superseded_artifacts": superseded,
        "exact_next_action": next_action,
        "transition_receipt_path": f"operations/internal-gtm/runs/transition-receipts/{pid}.jsonl",
    }


def premier_reconciliation() -> dict:
    claude = read(CLAUDE_REL)
    geo = read(GEO_REL)
    p = next(item for item in claude["batch"] if item["prospect_id"] == "premier-fm")
    qraw = p["qualification"]
    q = {
        "model": "qualification-v1",
        "score": qraw["score"], "tier": qraw["tier"],
        "qualification_coverage": {
            "percentage": qraw["coverage_percent"],
            "sufficiently_researched_dimensions": 6,
            "missing_dimensions": qraw.get("missing_dimensions", []),
            "exhausted_unknown_dimensions": [],
        },
    }
    ledger = geo.get("evidence") or {"ledger": geo.get("approved_claims", [])}
    diagnostic = {"capability": "client-audit", "diagnostic_id": None,
                  "status": "not_run"}
    history = ensure_chain("premier-fm", q, ledger, GEO_REL, "diagnostic_selected", diagnostic)
    artifacts = [
        {"kind": "artifact", "type": "approval_packet", "lifecycle_stage": "awaiting_approval",
         "artifact_id": p["stage_4"]["packet"]["approval_payload_digest"]},
        {"kind": "artifact", "type": "approval_packet", "lifecycle_stage": "awaiting_approval",
         "artifact_id": geo["packet"]["approval_payload_digest"]},
    ]
    state = reconstruct("premier-fm", history + artifacts)
    return {
        "prospect_id": "premier-fm", "company": "Premier FM",
        "qualification_score": 70, "tier": "STRONG", "qualification_coverage": 100.0,
        "canonical_lifecycle_stage": state["canonical_lifecycle_stage"],
        "diagnostic_capability": "client-audit",
        "diagnostic_status": "not_run",
        "canonical_approval_packet_id": state["canonical_approval_packet_id"],
        "superseded_artifacts": state["superseded_artifacts"],
        "evidence": {
            "route_requires": "client-audit",
            "newer_batch_diagnostic_result": p["stage_3"]["diagnostic_result"],
            "older_adapted_run_score": (geo.get("diagnostic") or {}).get("score"),
            "older_adapted_run_status": (geo.get("diagnostic") or {}).get("status"),
            "required_success_receipt_present": False,
        },
        "exact_next_action": "run and successfully complete registered client-audit; only then receipt diagnostic_complete",
        "transition_receipt_path": "operations/internal-gtm/runs/transition-receipts/premier-fm.jsonl",
    }


def main() -> int:
    source = read(SOURCE_REL)
    prospects = [prospect_receipt(item) for item in source["prospects"]]
    result = {
        "receipt_id": "first-real-gtm-batch-2026-08-11-canonical-v1",
        "contract_version": 1,
        "as_of": "2026-08-11",
        "authority_rule": "evidence plus prerequisite receipts; runtime recency is not authority",
        "source_batch": SOURCE_REL,
        "prospect_count": len(prospects),
        "prospects": prospects,
        "premier_fm_reconciliation": premier_reconciliation(),
        "tilz_objective_rule": "advance_active_revenue requires an evidenced commercial event; qualification alone is insufficient",
        "commercial_event_types": ["reply", "active_conversation", "booked_meeting", "discovery", "proposal", "negotiation", "explicit_buying_signal"],
        "stage_2_resume": {
            "prospect_id": "arc-solutions-limited",
            "priority_rank": 1,
            "status": "research_complete_evidence_audit_pending",
            "receipt": "operations/internal-gtm/runs/intelligence/arc-solutions-limited-stage-2-2026-08-11.json",
            "next_action": "Evidence Auditor review, then qualification-v1 rerun",
        },
        "external_action_authorized": False,
        "engine_touched": False,
    }
    write_json(OUT_FILE, result)
    print(json.dumps({"written": OUT_FILE.relative_to(REPO_ROOT).as_posix(),
                      "prospects": len(prospects),
                      "premier_stage": result["premier_fm_reconciliation"]["canonical_lifecycle_stage"],
                      "tilz_objective": next(x for x in prospects if x["prospect_id"] == "tilz-prosperitas")["current_objective"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
