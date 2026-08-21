#!/usr/bin/env python3
"""Reconstruct canonical lifecycle state from evidence and receipts, not from reports.

HOW TO USE
    python operations/internal-gtm/scripts/reconcile_state.py --prospect premier-fm
    python operations/internal-gtm/scripts/reconcile_state.py --all --out <path>

Two runtimes produced different states for the same prospect. Neither is authority
because it reported later. This walks the artifacts each runtime left behind, checks
every claimed transition against `transitions.PREREQUISITES`, and returns the one
stage the evidence supports.

An artifact that claims a stage with no receipt for its prerequisite is
`superseded_pre_gate_artifact`: kept as history, never executable.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
RUNS = GTM_ROOT / "runs"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import gtm_core as core  # noqa: E402
import transitions as tr  # noqa: E402

# A diagnostic is complete only when a real run produced a terminal status. An
# adapter that reshapes existing research records into a diagnostic block has not
# run a diagnostic; it has reformatted evidence.
ADAPTER_RUN_PREFIXES = ("acquisition-engine:",)


def _read(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def diagnostic_state(record: dict, prospect_id: str | None = None) -> dict:
    """Was a diagnostic actually run to completion for this prospect?

    The run record does not persist the diagnostic block, so provenance is read
    from the slice input that produced it. That is where the run_id lives, and the
    run_id is what distinguishes a real capability execution from an adapter that
    reshaped existing research into the same shape.
    """
    diagnostic = record.get("diagnostic") or {}
    if not diagnostic and prospect_id:
        diagnostic = (_read(RUNS / "inputs" / f"{prospect_id}.json", {}) or {}).get("diagnostic") or {}
    run_id = diagnostic.get("run_id") or ""
    steps = record.get("steps") or []
    completed_step = next((s for s in steps if s.get("capability")), None)

    if not diagnostic and not completed_step:
        return {"diagnostic_id": None, "status": "not_run",
                "reason": "no diagnostic block and no completed diagnostic step"}
    if any(run_id.startswith(prefix) for prefix in ADAPTER_RUN_PREFIXES):
        return {"diagnostic_id": run_id, "status": "not_run",
                "reason": ("the diagnostic block was reshaped from existing engine research "
                           "by an adapter. No diagnostic capability was executed.")}
    if diagnostic.get("capability") and diagnostic.get("findings"):
        return {"diagnostic_id": run_id or diagnostic.get("capability"),
                "status": "complete",
                "reason": f"{diagnostic['capability']} returned {len(diagnostic['findings'])} findings"}
    return {"diagnostic_id": run_id or None, "status": "partial",
            "reason": "a diagnostic block exists but carries no findings"}


def artifacts_for(prospect_id: str) -> list[dict]:
    """Everything either runtime left behind that claims a lifecycle stage."""
    found: list[dict] = []

    for path in sorted((RUNS / "geo").glob("*.json")):
        record = _read(path, {}) or {}
        if (record.get("prospect") or {}).get("prospect_id") != prospect_id:
            continue
        found.append({
            "artifact_id": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "type": "slice_run", "lifecycle_stage": record.get("lifecycle_stage"),
            "_record": record,
        })
        packet = record.get("packet")
        if packet:
            found.append({
                "artifact_id": packet.get("approval_payload_digest") or f"{path.stem}:packet",
                "type": "approval_packet", "lifecycle_stage": packet.get("lifecycle_stage"),
                "_record": record,
            })

    for path in sorted((RUNS / "qualification-batches").glob("*.json")):
        batch = _read(path, {}) or {}
        for row in batch.get("prospects", []):
            if row.get("prospect_id") != prospect_id:
                continue
            found.append({
                "artifact_id": f"{batch.get('batch_id') or path.stem}:{prospect_id}",
                "type": "qualification_batch_row",
                "lifecycle_stage": row.get("lifecycle_stage"),
                "_qualification_row": row,
            })

    for path in sorted((RUNS / "batches").glob("*.json")):
        batch = _read(path, {}) or {}
        for row in batch.get("batch", []):
            if row.get("prospect_id") != prospect_id:
                continue
            packet = (row.get("stage_4") or {}).get("packet")
            if packet:
                found.append({
                    "artifact_id": packet.get("approval_payload_digest") or f"{path.stem}:packet",
                    "type": "approval_packet", "lifecycle_stage": packet.get("lifecycle_stage"),
                    "_batch_row": row,
                })
    return found


def reconcile(prospect_id: str) -> dict:
    artifacts = artifacts_for(prospect_id)
    receipts = tr.load_receipts(prospect_id)

    slice_runs = [a for a in artifacts if a["type"] == "slice_run"]
    diagnostic = (diagnostic_state(slice_runs[-1]["_record"], prospect_id) if slice_runs
                  else {"diagnostic_id": None, "status": "not_run",
                        "reason": "no slice run found"})

    # Which stages are justified, in order, from the evidence.
    justified: list[str] = ["account_discovered"]
    if slice_runs and (slice_runs[-1]["_record"].get("evidence") or {}).get("ledger"):
        justified.append("evidence_collected")
    if slice_runs and slice_runs[-1]["_record"].get("qualification"):
        justified.append("qualified")
    if slice_runs and (slice_runs[-1]["_record"].get("route") or {}).get("route_id"):
        justified += ["routed", "diagnostic_selected"]
    if diagnostic["status"] in tr.TERMINAL_DIAGNOSTIC_STATUSES:
        justified.append("diagnostic_complete")

    canonical = justified[-1]
    classified = []
    for artifact in artifacts:
        result = tr.classify_artifact(artifact, justified, canonical)
        if artifact["type"] == "approval_packet" and result["classification"] == tr.CANONICAL:
            # A packet is only canonical if awaiting_approval itself is justified.
            if "awaiting_approval" not in justified:
                result = {**result, "classification": tr.SUPERSEDED, "executable": False,
                          "reason": ("packet claims awaiting_approval, which the evidence "
                                     "does not justify")}
        classified.append(result)

    record = slice_runs[-1]["_record"] if slice_runs else {}
    qualification = record.get("qualification") or {}
    batch_rows = [a for a in artifacts if a["type"] == "qualification_batch_row"]
    if not qualification and batch_rows:
        qualification = batch_rows[-1]["_qualification_row"].get("qualification_v1") or {}
        if qualification:
            justified = ["account_discovered", "evidence_collected", "qualified"]
            canonical = justified[-1]
    coverage = qualification.get("qualification_coverage") or {}
    if batch_rows and not diagnostic.get("diagnostic_id"):
        declared = batch_rows[-1]["_qualification_row"].get("diagnostic") or {}
        if declared:
            diagnostic = {"diagnostic_id": declared.get("diagnostic_id") or declared.get("capability"),
                          "status": declared.get("status", "not_run"),
                          "reason": declared.get("reason", "declared in the qualification batch")}

    # Once canonical transition receipts exist they own lifecycle state. Artifacts
    # remain evidence, but neither their runtime nor their prose can override a
    # verified adjacent chain. This is what lets Claude Code and Codex converge.
    if receipts:
        claims = [{k: v for k, v in item.items() if not k.startswith("_")}
                  for item in artifacts]
        verified = tr.reconstruct(prospect_id, receipts + claims)
        canonical = verified["canonical_lifecycle_stage"]
        justified = ["account_discovered"] + [
            item["to"] for item in verified["verified_transition_chain"]]
        selected_receipts = [item for item in receipts
                             if item.get("to_stage") == "diagnostic_selected"]
        completed_receipts = [item for item in receipts
                              if item.get("to_stage") == "diagnostic_complete"]
        diagnostic_receipt = (completed_receipts or selected_receipts)
        if diagnostic_receipt:
            latest = diagnostic_receipt[-1]
            diagnostic = {
                "diagnostic_id": latest.get("diagnostic_id"),
                "status": latest.get("diagnostic_status", "not_run"),
                "reason": "verified from the canonical transition receipt chain",
            }
        # The receipt carries the qualification coverage that actually gated the
        # transition. Prefer it to an older slice's embedded coverage snapshot.
        receipt_coverage = receipts[-1].get("qualification_coverage") or {}
        if receipt_coverage:
            coverage = receipt_coverage
            qualification = {**qualification, "qualification_coverage": coverage}
        classified = verified["artifacts"]

    return {
        "prospect_id": prospect_id,
        "canonical_lifecycle_stage": canonical,
        "justified_stages": justified,
        "diagnostic": diagnostic,
        "qualification": {
            "version": qualification.get("model") or qualification.get("qualification_version"),
            "score": qualification.get("score"),
            "tier": qualification.get("tier"),
            "actionability": qualification.get("actionability"),
            "coverage_percent": coverage.get("percentage"),
            "missing_dimensions": coverage.get("missing_dimensions", []),
            "exhausted_unknown_dimensions": coverage.get("exhausted_unknown_dimensions", []),
        },
        "artifacts": classified,
        "canonical_approval_packet_id": next(
            (a["artifact_id"] for a in classified
             if a["type"] == "approval_packet" and a["classification"] == tr.CANONICAL), None),
        "superseded_artifacts": [a["artifact_id"] for a in classified
                                 if a["classification"] == tr.SUPERSEDED],
        "existing_receipts": len(receipts),
        "next_action": _next_action(canonical, diagnostic, qualification, coverage),
        "method": ("reconstructed from artifacts and prerequisite rules. No runtime was "
                   "treated as authority for reporting later."),
        "external_action_authorized": False,
    }


def _next_action(canonical: str, diagnostic: dict, qualification: dict,
                 coverage: dict | None = None) -> str:
    coverage = coverage or qualification.get("qualification_coverage") or {}
    if coverage.get("missing_dimensions"):
        return f"complete qualification coverage: {', '.join(coverage['missing_dimensions'])}"
    if diagnostic["status"] not in tr.TERMINAL_DIAGNOSTIC_STATUSES:
        return (f"run the selected diagnostic to completion. Current status "
                f"{diagnostic['status']}: {diagnostic['reason']}")
    if qualification.get("actionability") not in (None, "actionable"):
        return f"resolve {qualification['actionability']}"
    return "advance to offer_selected with a transition receipt"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prospect")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if args.all:
        ids = sorted({(_read(p, {}) or {}).get("prospect", {}).get("prospect_id")
                      for p in (RUNS / "geo").glob("*.json")} - {None})
    else:
        ids = [args.prospect]

    results = [reconcile(pid) for pid in ids if pid]
    payload = results[0] if len(results) == 1 else {"reconciled": results}
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    for result in results:
        print(f"{result['prospect_id']:16s} canonical={result['canonical_lifecycle_stage']:20s} "
              f"diagnostic={result['diagnostic']['status']:10s} "
              f"packet={result['canonical_approval_packet_id'] or 'null'}")
        print(f"    superseded: {result['superseded_artifacts'] or 'none'}")
        print(f"    next      : {result['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
