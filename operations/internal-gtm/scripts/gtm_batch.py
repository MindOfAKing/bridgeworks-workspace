#!/usr/bin/env python3
"""Build one real internal-GTM batch through the four progressive-spend stages.

HOW TO USE
    python operations/internal-gtm/scripts/gtm_batch.py --as-of 2026-08-11 --cohort 8 \
        --out operations/internal-gtm/runs/batches

Progressive intelligence spend. Each stage is a gate, not a step. A prospect only
reaches the next stage when the previous one justifies the cost.

    Stage 1  cheap        existing records, deterministic checks, free public evidence
    Stage 2  targeted     Commercial and Buyer Intelligence, only where a dimension is
                          missing and the prospect ranked into the cohort
    Stage 3  diagnostic   geo-audit, client-audit or a bounded scan, only once
                          qualification warrants the cost
    Stage 4  commercial   Evidence Auditor -> Prospect Router -> Offer Strategist ->
                          Outreach Personalizer, ending at an approval packet

The point of the gates is to stop expensive capability runs landing on weak
prospects. Stage 3 is the expensive one, and nothing reaches it on Stage 1 evidence
alone.

Nothing here sends. The last stage any prospect can reach is `awaiting_approval`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
INTELLIGENCE = GTM_ROOT / "runs" / "intelligence"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
sys.path.insert(0, str(GTM_ROOT / "adapters"))

import capability_loader as cl  # noqa: E402
import enrichment_priority as ep  # noqa: E402
import engine_snapshot as es  # noqa: E402
import gtm_core as core  # noqa: E402
import objective_hierarchy as oh  # noqa: E402
import qualification_v1 as qv1  # noqa: E402
from run_geo_slice import (  # noqa: E402
    _proof_claim, _qualification_components, _reachability, _trigger_age,
)

# Stage 3 is the expensive gate. A prospect must clear all of these first.
STAGE_3_GATE = {
    "no_dimension_still_required": True,
    "min_score": 40,
    "requires_contact_destination": True,
    "requires_no_active_unsafe_state": True,
    "why": ("Stage 3 is the expensive gate. A diagnostic run on a prospect whose "
            "commercial fit and buyer authority are still unknown is exactly the spend "
            "this staging exists to prevent. Every applicable dimension must be "
            "researched first, which in practice means Stage 2 has run."),
}


def _read(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def stage_1_signals(pid: str, record: dict, as_of: str, snapshot_row: dict) -> dict:
    """Cheap stage. Everything here comes from records BridgeWorks already holds."""
    sources = record.get("sources") or []
    gap = (record.get("commercial_gap") or "").strip()
    named = bool((record.get("decision_maker") or "").strip()) and not \
        (record.get("decision_maker") or "").lower().startswith("no ")
    destination = (record.get("proposed_destination") or "").strip()
    destination = destination if "@" in destination and not destination.startswith("http") else ""
    checked = (record.get("checked_at") or "")[:10]
    age = core._days_between(checked, as_of) if checked else None
    angle = (record.get("recommended_angle") or "").lower()
    proof_words = ("visibility", "ai", "search", "trust", "quote", "conversion", "enquiry",
                   "credibility", "proof", "workflow", "ownership", "process")

    return {
        "prospect_id": pid,
        "company": record.get("company"),
        "problem_evidence_present": bool(sources) and bool(gap),
        "trigger_strength_signal": (20 if age is not None and age <= 14
                                    else 12 if age is not None and age <= 45
                                    else 5 if age is not None and age <= 120 else 0),
        "buyer_evidence_signal": (15 if named and destination else 10 if destination
                                  else 6 if named else 0),
        "proof_fit_present": any(word in angle for word in proof_words),
        "company_attractiveness_signal": min(15, (8 if record.get("owned_domain") else 0)
                                             + (4 if record.get("conversion_route") else 0)
                                             + (3 if len(record.get("observations") or []) >= 2 else 0)),
        "last_verified_at": checked or None,
        "contacted": bool(snapshot_row.get("contacted")),
        "engine_readiness": record.get("outreach_readiness"),
        "missing_evidence": record.get("outreach_readiness") == "needs_more_evidence",
        "unsafe_state": snapshot_row.get("unsafe_state"),
        "qualification_tier": snapshot_row.get("qualification_tier"),
        "missing_qualification_dimensions": snapshot_row.get("missing_qualification_dimensions") or ["all"],
        "_engine_record": record,
    }


def stage_2_result(pid: str) -> dict | None:
    """Targeted enrichment, if it has actually been run. Never assumed."""
    return _read(INTELLIGENCE / f"{pid}-2026-08-11.json", None)


def _intelligence_claims(intelligence: dict) -> list[dict]:
    claims = []
    for block in ("commercial_intelligence", "buyer_intelligence"):
        for finding in (intelligence.get(block) or {}).get("findings", []):
            claims.append({
                "id": finding["id"], "subject": finding["category"],
                "claim_key": finding.get("claim_key"), "value": finding.get("value"),
                "status": finding.get("status", "unknown"), "source": finding.get("source"),
                "observed_at": finding.get("observed_at"),
            })
    return claims


def qualify(signals: dict, intelligence: dict | None, as_of: str) -> dict:
    """Requalify under qualification-v1 using everything collected so far."""
    record = signals["_engine_record"]
    service_routes = cl.load_service_routes()

    claims = [{
        "id": f"src{i}", "subject": "website_trust",
        "claim_key": f"{signals['prospect_id']}:source-{i}",
        "value": source.get("supports"), "status": "verified",
        "source": source.get("url"), "observed_at": source.get("accessed_at"),
    } for i, source in enumerate(record.get("sources") or [])]

    destination = (record.get("proposed_destination") or "").strip()
    destination = destination if "@" in destination and not destination.startswith("http") else None
    if destination:
        claims.append({
            "id": "q-buyer", "subject": "buyer_accessibility", "claim_key": "buyer_contact_route",
            "value": destination, "status": "observed",
            "source": (record.get("sources") or [{}])[-1].get("url"),
            "observed_at": (record.get("checked_at") or "")[:10],
        })
    claims.append({
        "id": "q-trigger", "subject": "trigger_urgency", "claim_key": "current_buyer_event",
        "value": "research_verification", "status": "observed",
        "source": (record.get("sources") or [{}])[0].get("url"),
        "observed_at": (record.get("checked_at") or "")[:10],
    })

    if intelligence:
        claims.extend(_intelligence_claims(intelligence))

    ledger = core.build_evidence_ledger(claims, as_of=as_of)
    approved = set(ledger["approved_claim_ids"])
    gap_categories = sorted({entry["subject"] for entry in ledger["ledger"]
                             if entry["id"] in approved})
    buyer = {"email": destination,
             "name": record.get("decision_maker") if destination else None}
    route = core.select_service_route(
        gap_categories, service_routes,
        findings=[{"category": e["subject"], "status": e["status"], "severity": "medium"}
                  for e in ledger["ledger"] if e["id"] in approved],
        buyer=buyer, known_capabilities=set(cl.capability_index()))

    proof = _proof_claim(route, service_routes, as_of)
    if proof:
        claims.append(proof)
        ledger = core.build_evidence_ledger(claims, as_of=as_of)
        approved = set(ledger["approved_claim_ids"])

    findings = [{"id": e["id"], "category": e["subject"], "severity": "medium"}
                for e in ledger["ledger"]]
    components = _qualification_components(
        findings, approved, buyer,
        core._days_between((record.get("checked_at") or "")[:10], as_of),
        route, service_routes)

    # Anything the intelligence pass actually established is now researched.
    if intelligence:
        for dimension in ("commercial_fit", "execution_readiness", "buyer_accessibility"):
            cited = [c["id"] for c in _intelligence_claims(intelligence)
                     if c["subject"] == dimension and c["id"] in approved]
            if cited:
                components[dimension] = {
                    "score": components[dimension]["score"],
                    "evidence_ids": cited,
                    "research_status": "complete",
                    "rationale": "stage 2 targeted enrichment",
                }

    qualification = qv1.score(components, ledger, {
        "canonical_domain": core.normalize_domain(record.get("owned_domain") or ""),
        "normalized_company": core.normalize_company(record.get("company") or ""),
        "contact_destination": destination,
        "service_route_exists": bool(route.get("route_id")),
        "contradicted_claim_ids": [e["id"] for e in ledger["ledger"]
                                   if e["status"] == "contradicted"],
    }, as_of=as_of)
    return {"qualification": qualification, "route": route, "ledger": ledger,
            "buyer": buyer, "destination": destination}


def stage_3_allowed(qualification: dict, destination: str | None, unsafe: str | None) -> tuple[bool, list[str]]:
    reasons = []
    coverage = qualification["qualification_coverage"]
    still_required = coverage.get("missing_dimensions") or []
    if still_required:
        reasons.append("dimensions still unresearched: " + ", ".join(still_required))
    if qualification["score"] < STAGE_3_GATE["min_score"]:
        reasons.append(f"score {qualification['score']} below the {STAGE_3_GATE['min_score']} gate")
    if STAGE_3_GATE["requires_contact_destination"] and not destination:
        reasons.append("no verified contact destination")
    if unsafe == oh.UNSAFE_ACTIVE:
        reasons.append("an active unsafe state must be resolved first")
    return (not reasons), reasons


def build(as_of: str, cohort_size: int) -> dict:
    snapshot = es.build(as_of)
    rows = {row["prospect_id"]: row for row in snapshot["prospects"]}
    records = ep_engine_records()

    signals = [stage_1_signals(pid, record, as_of, rows.get(pid, {}))
               for pid, record in sorted(records.items())]
    ranked = ep.rank([{k: v for k, v in s.items() if k != "_engine_record"} for s in signals],
                     date.fromisoformat(as_of), cohort_size)
    by_id = {s["prospect_id"]: s for s in signals}

    decision = oh.select(snapshot, cohort_size=cohort_size)

    batch = []
    for entry in ranked:
        pid = entry["prospect_id"]
        signal = by_id[pid]
        intelligence = stage_2_result(pid)
        result = qualify(signal, intelligence, as_of)
        qualification = result["qualification"]
        allowed, blocked_by = stage_3_allowed(
            qualification, result["destination"], signal.get("unsafe_state"))

        row = {
            "prospect_id": pid,
            "company": signal["company"],
            "enrichment_priority": entry["priority_score"],
            "priority_explanation": entry["why"],
            "stage_1": {
                "existing_trigger": (signal["_engine_record"].get("recommended_angle") or "")[:160],
                "problem_evidence": (signal["_engine_record"].get("commercial_gap") or "")[:220],
                "sources": len(signal["_engine_record"].get("sources") or []),
                "last_verified_at": signal["last_verified_at"],
            },
            "stage_2": {
                "run": bool(intelligence),
                "commercial_intelligence": (
                    {"value_band": intelligence["commercial_intelligence"]["commercial_value_band"],
                     "procurement_complexity": intelligence["commercial_intelligence"]["procurement_complexity"],
                     "engagement_size_fit": intelligence["commercial_intelligence"]["engagement_size_fit"],
                     "findings": len(intelligence["commercial_intelligence"]["findings"]),
                     "unresolved": intelligence["commercial_intelligence"]["unresolved_questions"]}
                    if intelligence else "not run: pending targeted enrichment"),
                "buyer_intelligence": (
                    {"roles_established": [name for name, role in intelligence["buyer_intelligence"]["roles"].items()
                                           if role["attribution_confidence"] != "none"],
                     "contact_route": intelligence["buyer_intelligence"]["contact_route"]["destination_type"],
                     "unresolved": intelligence["buyer_intelligence"]["unresolved_questions"]}
                    if intelligence else "not run: pending targeted enrichment"),
            },
            "qualification": {
                "model": qualification["model"],
                "component_scores": qualification["component_scores"],
                "score": qualification["score"],
                "tier": qualification["tier"],
                "actionability": qualification["actionability"],
                "coverage_percent": qualification["qualification_coverage"]["percentage"],
                "missing_dimensions": qualification["qualification_coverage"]["missing_dimensions"],
                "verified_negative_dimensions": qualification["qualification_coverage"].get(
                    "verified_negative_dimensions", []),
            },
            "route": {
                "service_route": result["route"].get("route_id"),
                "fit": result["route"].get("fit"),
                "won_on": result["route"].get("won_on"),
                "diagnostic_capability": result["route"].get("diagnostic_capability"),
                "proof_asset_id": result["route"].get("proof_asset_id"),
            },
            "stage_3": {"allowed": allowed, "blocked_by": blocked_by,
                        "diagnostic_result": "not run: gate not cleared" if not allowed
                        else "eligible, not yet run"},
            "stage_4": {"reached": False, "packet": None},
            "next_action": None,
        }

        if allowed and qualification["actionability"] == "actionable":
            # Eligibility selects a diagnostic. It is not diagnostic completion.
            # Offer selection and packet creation remain blocked until a successful
            # diagnostic_complete transition receipt exists.
            row["next_action"] = "stage_3_diagnostic"
        elif not intelligence:
            row["next_action"] = "stage_2_targeted_enrichment"
        elif qualification["actionability"] != "actionable":
            row["next_action"] = f"resolve {qualification['actionability']}"
        else:
            row["next_action"] = "stage_3_diagnostic"
        batch.append(row)

    return {
        "as_of": as_of,
        "objective": {k: decision[k] for k in
                      ("priority_class", "priority_class_rank", "considered_classes",
                       "unsafe_classification")},
        "cohort_size": len(batch),
        "prospects_considered": len(signals),
        "stage_gates": STAGE_3_GATE,
        "batch": batch,
        "summary": {
            "stage_2_run": sum(1 for r in batch if r["stage_2"]["run"]),
            "stage_3_eligible": sum(1 for r in batch if r["stage_3"]["allowed"]),
            "stage_4_reached": sum(1 for r in batch if r["stage_4"]["reached"]),
            "tiers": {t: sum(1 for r in batch if r["qualification"]["tier"] == t)
                      for t in ("HOT", "STRONG", "QUALIFIED", "WATCH", "DO_NOT_PURSUE")},
        },
        "external_action_authorized": False,
        "note": ("Nothing was sent. This builder stops at diagnostic selection. "
                 "Offer and packet creation require receipted diagnostic completion."),
    }


def ep_engine_records() -> dict[str, dict]:
    """Newest engine research record per prospect."""
    ops = REPO_ROOT / "operations" / "client-acquisition-engine" / "research" / "prospect-operations"
    latest: dict[str, dict] = {}
    for path in sorted((ops / "results").glob("*.json")):
        for record in _read(path, {}).get("prospects", []):
            pid = record.get("prospect_id")
            if not pid:
                continue
            previous = latest.get(pid)
            if previous is None or str(record.get("checked_at", "")) >= str(previous.get("checked_at", "")):
                latest[pid] = record
    return latest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--cohort", type=int, default=8)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = build(args.as_of, args.cohort)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        path = args.out / f"gtm-batch-{args.as_of}.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"written: {path}")
    print(f"priority class: {report['objective']['priority_class']}")
    print(f"cohort {report['cohort_size']} of {report['prospects_considered']} considered")
    print(f"summary: {report['summary']}")
    for row in report["batch"]:
        q = row["qualification"]
        print(f"  {row['company'][:30]:30s} pri={row['enrichment_priority']:3d} "
              f"score={q['score']:3d} {q['tier']:14s} cov={q['coverage_percent']:5.1f}% "
              f"s2={'yes' if row['stage_2']['run'] else 'no ':3s} "
              f"s3={'yes' if row['stage_3']['allowed'] else 'no ':3s} "
              f"s4={'yes' if row['stage_4']['reached'] else 'no ':3s} -> {row['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
