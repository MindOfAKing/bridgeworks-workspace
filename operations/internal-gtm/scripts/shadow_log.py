#!/usr/bin/env python3
"""Step 9 shadow harness: run both 09:10 workflows side by side, write nothing.

HOW TO USE
    python operations/internal-gtm/scripts/shadow_log.py --as-of 2026-08-11
    python operations/internal-gtm/scripts/shadow_log.py --as-of 2026-08-11 --append
    python operations/internal-gtm/scripts/shadow_log.py --report

`--append` adds one row to `runs/shadow/09-10-shadow-log.jsonl`, keyed by date so
re-running a day updates rather than duplicates. `--report` prints the ten-day
readiness check.

The old job is never called. Its selection logic is imported and evaluated
read-only, so this harness cannot prepare a batch, write engine state, or take an
external action. A run is verified against file mtimes.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
ENGINE = REPO_ROOT / "operations" / "client-acquisition-engine"
OLD_JOB = ENGINE / "scripts" / "prospect_research_queue.py"
LOG = GTM_ROOT / "runs" / "shadow" / "09-10-shadow-log.jsonl"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
sys.path.insert(0, str(GTM_ROOT / "adapters"))

from daily_objective import select_daily_objective  # noqa: E402
import objective_hierarchy as oh  # noqa: E402
import engine_snapshot  # noqa: E402

READINESS_DAYS = 10


def _engine_mtimes() -> dict[str, float]:
    return {str(p): p.stat().st_mtime for p in ENGINE.rglob("*")
            if p.is_file() and "outputs" not in p.parts and "__pycache__" not in p.parts}


def old_workflow_action() -> dict:
    """What the live 09:10 job would do today. Evaluated, never executed."""
    if not OLD_JOB.is_file():
        return {"action": "unavailable", "reason": "prospect_research_queue.py not found"}
    spec = importlib.util.spec_from_file_location("prospect_research_queue", OLD_JOB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    rows = module.load_rows()
    state = module.load_state()
    eligible = module.eligible_rows(rows, state)
    limit = 8
    return {
        "action": "prepare_research_batch" if eligible else "no_eligible_rows",
        "eligible_rows": len(eligible),
        "would_prepare": [row.get("company") for row in eligible[:limit]],
        "selection_rule": "unresearched active-lane rows, ranked by sector keywords",
    }


def build_row(as_of: str) -> dict:
    before = _engine_mtimes()
    snapshot = engine_snapshot.build(as_of)
    new = select_daily_objective(snapshot)
    refined = oh.select(snapshot, cohort_size=8)
    old = old_workflow_action()
    after = _engine_mtimes()

    metrics = new.get("metrics", {})
    supply_justified = bool(new.get("supply", {}).get("allowed"))
    difference = (
        "identical" if old["action"] == "prepare_research_batch" and new["objective_type"] == "generate_new_companies"
        else f"old would {old['action']}, new selects {new['objective_type']}"
    )

    return {
        "as_of": as_of,
        "old_workflow_action": old,
        "new_workflow_action": {
            "objective_type": new["objective_type"],
            "prospect_ids": new.get("prospect_ids", []),
            "batch_id": new.get("batch_id"),
            "reason_codes": new.get("reason_codes", []),
        },
        "pipeline_depth": len(snapshot["prospects"]),
        "qualified_untouched": metrics.get("qualified_untouched"),
        "overdue_research": metrics.get("overdue_research"),
        "missing_evidence": metrics.get("missing_evidence"),
        "missing_buyers": metrics.get("missing_buyers"),
        "approvals_waiting": metrics.get("approvals_waiting"),
        "new_supply_justified": supply_justified,
        "supply_blockers": new.get("supply", {}).get("blockers", []),
        "priority_class": refined["priority_class"],
        "priority_class_rank": refined.get("priority_class_rank"),
        "higher_classes_not_selected": [
            {"priority_class": c["priority_class"], "candidates": c["candidates"],
             "why_not": c.get("why_not")}
            for c in refined["considered_classes"]
            if not c["selected"]
            and oh.PRIORITY_CLASSES.index(c["priority_class"])
            < oh.PRIORITY_CLASSES.index(refined["priority_class"])
        ],
        "lower_classes_deferred": [
            {"priority_class": c["priority_class"], "candidates": c["candidates"],
             "why_not": c.get("why_not")}
            for c in refined["considered_classes"]
            if not c["selected"] and c["candidates"]
            and oh.PRIORITY_CLASSES.index(c["priority_class"])
            > oh.PRIORITY_CLASSES.index(refined["priority_class"])
        ],
        "unsafe_classification": refined["unsafe_classification"],
        "refined_cohort": refined["prospect_ids"],
        "observed_difference": difference,
        "human_correction": None,
        "engine_untouched": before == after,
        "snapshot_digest": new.get("source_snapshot_digest"),
        "requires_qualification_v1": snapshot["_provenance"]["prospects_requiring_qualification_v1"],
        "external_action_authorized": False,
    }


def append(row: dict, log: Path = LOG) -> dict:
    existing: dict[str, dict] = {}
    if log.is_file():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                previous = json.loads(line)
                existing[previous["as_of"]] = previous
    previous = existing.get(row["as_of"])
    if previous and previous.get("human_correction") is not None:
        row["human_correction"] = previous["human_correction"]
    existing[row["as_of"]] = row
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(json.dumps(existing[k], ensure_ascii=False) for k in sorted(existing)) + "\n",
                   encoding="utf-8")
    return {"days_recorded": len(existing)}


def report(log: Path = LOG) -> dict:
    rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()] \
        if log.is_file() else []
    bad_supply = [r["as_of"] for r in rows
                  if r["new_supply_justified"] and (r.get("qualified_untouched") or 0) > 0]
    blocked = [r["as_of"] for r in rows if r["new_workflow_action"]["objective_type"] == "blocked_unverified"]
    wrote = [r["as_of"] for r in rows if not r["engine_untouched"]]
    corrected = [r["as_of"] for r in rows if r.get("human_correction")]
    accepted = [r["as_of"] for r in rows
                if isinstance(r.get("human_correction"), dict)
                and str(r["human_correction"].get("decision", "")).startswith("accepted")]
    diverged = [r["as_of"] for r in rows if r["observed_difference"] != "identical"]
    return {
        "days_recorded": len(rows),
        "days_required": READINESS_DAYS,
        "criteria": {
            "never_generated_supply_while_ready_work_waited": {"pass": not bad_supply, "days": bad_supply},
            "blocked_days_matched_a_real_failure": {"pass": None, "days": blocked,
                                                    "note": "needs a human to confirm each blocked day"},
            "objectives_agreed_by_emmanuel": {
                # The harness records Emmanuel's decisions but never self-certifies
                # the acceptance criterion. Final acceptance remains human-owned.
                "pass": None,
                "corrections": corrected,
                "accepted_days": accepted,
                "note": "each shadow day needs an explicit human decision"},
            "no_run_wrote_to_the_engine": {"pass": not wrote, "days": wrote},
        },
        "days_the_two_workflows_disagreed": len(diverged),
        "ready_for_cutover": len(rows) >= READINESS_DAYS and not bad_supply and not wrote,
        "note": "Two criteria need a human. This harness cannot mark them passed.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--append", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--log", type=Path, default=LOG)
    parser.add_argument("--human-correction")
    args = parser.parse_args()

    if args.report:
        print(json.dumps(report(args.log), indent=2, ensure_ascii=False))
        return 0

    row = build_row(args.as_of)
    if args.human_correction:
        row["human_correction"] = {
            "decision": "accepted_after_refinement",
            "note": args.human_correction,
            "recorded_at": args.as_of,
        }
    if args.append:
        print(f"shadow log: {append(row, args.log)}")
        print(f"log: {args.log}")
    print(json.dumps(row, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
