#!/usr/bin/env python3
"""The one canonical batch receipt contract. Both runtimes resolve to this shape.

HOW TO USE
    python operations/internal-gtm/scripts/batch_receipt.py \
        --batch internal-gtm-qualification-2026-08-11-01 \
        --out operations/internal-gtm/runs/batch-receipts

Two runtimes produced two batches for the same day with different cohorts. A batch
is a proposal. This receipt is the authoritative record, and it is built by
reconciling each prospect's state from artifacts and receipts rather than by
trusting whichever batch file was written last.

Every row carries exactly these fields, and a row that cannot supply one carries
null rather than an inference:

    qualification_score, coverage, missing_dimensions, exhausted_unknown_dimensions,
    lifecycle_stage, diagnostic_status, current_objective,
    approval_packet_id (or null), superseded_artifacts, next_action
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
RUNS = GTM_ROOT / "runs"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
sys.path.insert(0, str(GTM_ROOT / "adapters"))

import objective_hierarchy as oh  # noqa: E402
import reconcile_state as rs  # noqa: E402
import transitions as tr  # noqa: E402

RECEIPT_CONTRACT_VERSION = "gtm-batch-receipt-1"

ROW_FIELDS = (
    "prospect_id", "company", "qualification_score", "qualification_tier",
    "coverage_percent", "missing_dimensions", "exhausted_unknown_dimensions",
    "lifecycle_stage", "diagnostic_status", "current_objective",
    "approval_packet_id", "superseded_artifacts", "next_action",
)


def _read(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def find_batch(batch_id: str) -> tuple[dict, Path]:
    for folder in ("qualification-batches", "batches"):
        for path in sorted((RUNS / folder).glob("*.json")):
            data = _read(path, {}) or {}
            if data.get("batch_id") == batch_id or path.stem == batch_id:
                return data, path
    raise SystemExit(f"batch not found: {batch_id}")


def _company(pid: str, batch: dict) -> str | None:
    for row in batch.get("prospects", []) or batch.get("batch", []):
        if row.get("prospect_id") == pid:
            return row.get("company")
    for row in (batch.get("objective") or {}).get("enrichment_cohort", []):
        if row.get("prospect_id") == pid:
            return row.get("company")
    return None


def _missing_dimensions(qualification: dict, snapshot_coverage: dict) -> list[str]:
    """Prefer a stated list; otherwise derive it from the per-dimension block."""
    stated = qualification.get("missing_dimensions") or snapshot_coverage.get("missing_dimensions")
    if stated:
        return stated
    for block in (qualification.get("qualification_coverage") or {}, snapshot_coverage):
        by_dimension = block.get("by_dimension") or {}
        derived = sorted(name for name, item in by_dimension.items()
                         if item.get("research_status") == "required")
        if derived:
            return derived
    return []


def _exhausted_dimensions(qualification: dict, snapshot_coverage: dict) -> list[str]:
    stated = (qualification.get("exhausted_unknown_dimensions")
              or snapshot_coverage.get("exhausted_unknown_dimensions"))
    if stated:
        return stated
    for block in (qualification.get("qualification_coverage") or {}, snapshot_coverage):
        by_dimension = block.get("by_dimension") or {}
        derived = sorted(name for name, item in by_dimension.items()
                         if item.get("research_status") == "exhausted_unknown")
        if derived:
            return derived
    return []


def _row_next_action(state: dict, snapshot_coverage: dict) -> str:
    """Derived from the fields this row prints, so the two can never disagree."""
    qualification = state["qualification"]
    missing = _missing_dimensions(qualification, snapshot_coverage)
    if missing:
        return f"complete qualification coverage: {', '.join(missing)}"
    coverage_block = (qualification.get("qualification_coverage") or {}) or snapshot_coverage
    partial = sorted(name for name, item in (coverage_block.get("by_dimension") or {}).items()
                     if item.get("research_status") == "partial")
    if partial:
        return f"finish partial qualification research: {', '.join(partial)}"
    return state["next_action"]


def _objective_for(pid: str, snapshot_rows: dict, as_of: str) -> str:
    """Which priority class this prospect currently belongs to."""
    row = snapshot_rows.get(pid)
    if row is None:
        return "complete_qualification_coverage"
    decision = oh.select({"as_of": as_of, "prospects": [row], "approvals_waiting": 0,
                          "unresolved_batches": [], "validated_new_market_gap": False},
                         cohort_size=1)
    return decision.get("priority_class") or "nothing_to_do"


def build(batch_id: str, as_of: str) -> dict:
    batch, path = find_batch(batch_id)
    ids = (batch.get("objective") or {}).get("prospect_ids") \
        or [r.get("prospect_id") for r in batch.get("prospects", [])] \
        or [r.get("prospect_id") for r in batch.get("batch", [])]
    ids = [pid for pid in ids if pid]

    import engine_snapshot as es
    snapshot = es.build(as_of)
    snapshot_rows = {row["prospect_id"]: row for row in snapshot["prospects"]}

    rows = []
    for pid in ids:
        state = rs.reconcile(pid)
        qualification = state["qualification"]
        row_snapshot = snapshot_rows.get(pid, {})
        coverage = row_snapshot.get("qualification_coverage") or {}

        rows.append({
            "prospect_id": pid,
            "company": _company(pid, batch),
            "qualification_score": qualification.get("score"),
            "qualification_tier": qualification.get("tier"),
            "coverage_percent": (qualification.get("coverage_percent")
                                 if qualification.get("coverage_percent") is not None
                                 else coverage.get("percentage")),
            "missing_dimensions": _missing_dimensions(qualification, coverage),
            "exhausted_unknown_dimensions": _exhausted_dimensions(qualification, coverage),
            "lifecycle_stage": state["canonical_lifecycle_stage"],
            "diagnostic_status": state["diagnostic"]["status"],
            "diagnostic_reason": state["diagnostic"]["reason"],
            "current_objective": _objective_for(pid, snapshot_rows, as_of),
            "approval_packet_id": state["canonical_approval_packet_id"],
            "superseded_artifacts": state["superseded_artifacts"],
            "next_action": _row_next_action(state, coverage),
            "transition_receipts": len(tr.load_receipts(pid)),
        })

    missing_fields = [f"{row['prospect_id']}.{field}" for row in rows
                      for field in ROW_FIELDS if field not in row]

    return {
        "receipt_contract_version": RECEIPT_CONTRACT_VERSION,
        "batch_id": batch_id,
        "source_batch": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "as_of": as_of,
        "compiled_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "row_fields": list(ROW_FIELDS),
        "prospect_count": len(rows),
        "rows": rows,
        "totals": {
            "with_a_canonical_approval_packet": sum(1 for r in rows if r["approval_packet_id"]),
            "with_a_completed_diagnostic": sum(1 for r in rows if r["diagnostic_status"] == "complete"),
            "superseded_artifacts": sum(len(r["superseded_artifacts"]) for r in rows),
            "by_objective": {name: sum(1 for r in rows if r["current_objective"] == name)
                             for name in oh.PRIORITY_CLASSES},
            "by_lifecycle_stage": {stage: sum(1 for r in rows if r["lifecycle_stage"] == stage)
                                   for stage in sorted({r["lifecycle_stage"] for r in rows})},
        },
        "contract_complete": not missing_fields,
        "missing_fields": missing_fields,
        "method": ("each row reconciled from artifacts and transition receipts. No runtime was "
                   "treated as authority for producing a later report."),
        "external_action_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    receipt = build(args.batch, args.as_of)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        path = args.out / f"{args.batch}-receipt.json"
        path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"written: {path}")

    print(f"contract {receipt['receipt_contract_version']}, "
          f"{receipt['prospect_count']} prospects, complete={receipt['contract_complete']}")
    print(f"totals: {receipt['totals']['with_a_canonical_approval_packet']} canonical packets, "
          f"{receipt['totals']['with_a_completed_diagnostic']} completed diagnostics, "
          f"{receipt['totals']['superseded_artifacts']} superseded artifacts")
    for row in receipt["rows"]:
        print(f"  {(row['company'] or row['prospect_id'])[:28]:28s} "
              f"score={str(row['qualification_score']):>4s} cov={str(row['coverage_percent']):>5s} "
              f"stage={row['lifecycle_stage']:20s} diag={row['diagnostic_status']:9s} "
              f"packet={row['approval_packet_id'] or 'null'}")
        print(f"      objective={row['current_objective']}  next={row['next_action'][:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
