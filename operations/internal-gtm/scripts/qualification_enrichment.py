#!/usr/bin/env python3
"""The qualification enrichment loop: detect missing dimensions, route research, requalify.

HOW TO USE
    from qualification_enrichment import detect, plan
    requests = plan(qualification_result, prospect_context)

    python operations/internal-gtm/scripts/qualification_enrichment.py --runs operations/internal-gtm/runs/geo

The loop:

    qualification-v1 -> missing-dimension detector -> research capability
                     -> Evidence Auditor -> requalification

The detector never guesses a score. It names which of the six dimensions has no
usable evidence, maps each to the capability that can collect it, and emits a
capability call request. Nothing runs itself.

The rule that keeps this cheap: a dimension already supported by fresh approved
evidence is never re-researched. `research_status` and `evidence_freshness` come
from the qualification result, so the check is free and cannot drift from scoring.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import capability_loader as cl  # noqa: E402
import qualification_v1 as qv1  # noqa: E402

# The dimension-to-capability map lives in `daily_objective.ENRICHMENT_CAPABILITIES`
# so the scheduler and this planner cannot disagree about who researches what.
# This adds the role and the routing task, which the scheduler does not need.
from daily_objective import ENRICHMENT_CAPABILITIES  # noqa: E402

DIMENSION_ROLE_TASK = {
    "commercial_fit": ("commercial-intelligence", "deep_research_synthesis"),
    "execution_readiness": ("commercial-intelligence", "deep_research_synthesis"),
    "buyer_accessibility": ("buyer-intelligence", "deep_research_synthesis"),
    "problem_evidence": ("prospect-router", "diagnostic_capability_run"),
    "trigger_urgency": ("trigger-scout", "deep_research_synthesis"),
    # proof_fit is answered from the BridgeWorks proof inventory, not from research
    # about the prospect. The router owns it; there is nothing to send an agent to find.
    "proof_fit": ("prospect-router", "strategic_recommendation"),
}


def research_route(dimension: str) -> dict | None:
    capability = ENRICHMENT_CAPABILITIES.get(dimension)
    entry = DIMENSION_ROLE_TASK.get(dimension)
    if not capability or not entry:
        return None
    role, task = entry
    return {"role": role, "capability": capability, "task": task}


# Statuses that mean the dimension still needs work.
# `exhausted_unknown` is deliberately absent. The capability already ran against
# every approved source and the fact stayed unknowable. Reopening it would spend
# the same research to reach the same answer. Only fresh evidence reopens it.
NEEDS_RESEARCH = ("required", "partial")
NEVER_REOPEN = ("exhausted_unknown", "not_applicable")


def detect(qualification: dict) -> dict:
    """Which dimensions need research, which are already covered, and why."""
    coverage = qualification["qualification_coverage"]
    by_dimension = coverage["by_dimension"]

    needed, covered, unowned = [], [], []
    for name, item in sorted(by_dimension.items()):
        status = item["research_status"]
        if status in NEVER_REOPEN:
            covered.append({
                "dimension": name,
                "reason": ("research exhausted against every approved source; only fresh "
                           "evidence reopens it" if status == "exhausted_unknown"
                           else "declared not applicable"),
                "score": item["score"],
                "research_status": status,
                "zero_because": item.get("zero_because"),
                "confidence": item["confidence"],
            })
            continue
        if status not in NEEDS_RESEARCH:
            covered.append({
                "dimension": name,
                "reason": "fresh approved evidence already supports this dimension",
                "score": item["score"],
                "zero_because": item.get("zero_because"),
                "confidence": item["confidence"],
            })
            continue
        route = research_route(name)
        entry = {
            "dimension": name,
            "research_status": status,
            "score": item["score"],
            "zero_because": item.get("zero_because"),
            "existing_evidence_ids": item["evidence_ids"],
            "confidence": item["confidence"],
            "evidence_freshness": item.get("evidence_freshness"),
        }
        (needed if route else unowned).append({**entry, **(route or {})})

    return {
        "model": qualification.get("model", qv1.MODEL_ID),
        "score": qualification["score"],
        "tier": qualification["tier"],
        "actionability": qualification["actionability"],
        "coverage_percent": coverage["percentage"],
        "researched_dimensions": coverage["sufficiently_researched_dimensions"],
        "total_dimensions": coverage["total_dimensions"],
        "needs_research": needed,
        "already_covered": covered,
        "no_owning_capability": unowned,
        "skipped_reresearch": [item["dimension"] for item in covered],
    }


def plan(qualification: dict, prospect: dict) -> dict:
    """Turn the detection into exact capability call requests. Runs nothing."""
    detection = detect(qualification)
    requests = []
    for item in detection["needs_research"]:
        requests.append(cl.capability_call_request(
            role_id=item["role"],
            capability_id=item["capability"],
            task=item["task"],
            payload={
                "prospect_id": prospect.get("prospect_id"),
                "company": prospect.get("company"),
                "canonical_domain": prospect.get("canonical_domain"),
                "dimension": item["dimension"],
                "current_status": item["research_status"],
                "existing_evidence_ids": item["existing_evidence_ids"],
                "instruction": (
                    f"Collect public evidence for the {item['dimension']} dimension only. "
                    "Every finding needs a source URL and an access date. Do not score, "
                    "do not route, do not contact anyone. Free tools first."
                ),
            },
        ))
    return {
        **detection,
        "capability_calls": requests,
        "requalify_after": "Evidence Auditor approves the returned findings",
        "external_action_authorized": False,
    }


def survey(runs_dir: Path) -> dict:
    """How many prospects are missing each dimension, across all run records."""
    missing = Counter()
    partial = Counter()
    verified_negative = Counter()
    prospects, coverages = 0, []
    for path in sorted(runs_dir.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        qualification = record.get("qualification") or {}
        coverage = qualification.get("qualification_coverage")
        if not coverage:
            continue
        prospects += 1
        coverages.append(coverage["percentage"])
        for name, item in coverage["by_dimension"].items():
            if item["research_status"] == "required":
                missing[name] += 1
            elif item["research_status"] == "partial":
                partial[name] += 1
            if item.get("zero_because") == "verified_negative":
                verified_negative[name] += 1
    return {
        "prospects_with_qualification": prospects,
        "missing_by_dimension": {name: missing.get(name, 0) for name in qv1.DIMENSIONS},
        "partial_by_dimension": {name: partial.get(name, 0) for name in qv1.DIMENSIONS},
        "verified_negative_by_dimension": {name: verified_negative.get(name, 0) for name in qv1.DIMENSIONS},
        "mean_coverage_percent": round(sum(coverages) / len(coverages), 1) if coverages else None,
        "fully_covered_prospects": sum(1 for c in coverages if c == 100),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=GTM_ROOT / "runs" / "geo")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = survey(args.runs)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    print(f"prospects with a qualification: {report['prospects_with_qualification']}")
    print(f"mean coverage: {report['mean_coverage_percent']}%")
    for name, count in report["missing_by_dimension"].items():
        print(f"  missing {name:22s} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
