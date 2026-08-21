#!/usr/bin/env python3
"""Vertical slice 2: sector hypothesis -> candidates -> dedupe -> qualify -> ranked queue.

HOW TO USE
    python operations/internal-gtm/scripts/run_market_discovery.py \
        --input operations/internal-gtm/examples/market-discovery-input.json \
        --as-of 2026-08-11 --out operations/internal-gtm/runs
Without a `candidates` list the run stops at market_hypothesis and prints the exact
Trigger Scout call to make. Dedupe and scoring are deterministic code, so the same
candidate list always produces the same queue in the same order.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import capability_loader as cl  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_v1 as qv1  # noqa: E402
from run_geo_slice import (  # noqa: E402
    _reachability, _trigger_age, _qualification_components, _proof_claim,
)


def run(payload: dict, as_of: str) -> dict:
    cl.assert_single_registry()
    service_routes = cl.load_service_routes()

    market = payload.get("market")
    hypothesis = payload.get("sector_hypothesis")
    stage = "market_hypothesis"
    steps = [{"stage": stage, "role": "market-icp-strategist", "market": market, "hypothesis": hypothesis}]

    candidates = payload.get("candidates")
    if not candidates:
        request = cl.capability_call_request(
            role_id="trigger-scout",
            capability_id="competitive-research",
            task="deep_research_synthesis",
            payload={"market": market, "sector_hypothesis": hypothesis,
                     "required_fields": ["company", "website_url", "trigger", "source"]},
        )
        return {"slice": "market_discovery", "as_of": as_of, "market": market,
                "lifecycle_stage": stage, "blocked_on": request, "steps": steps,
                "external_action_authorized": False}

    deduped = core.dedupe(candidates)
    stage = core.advance(stage, "account_discovered")
    steps.append({"stage": stage, "role": "data-steward",
                  "input_count": len(candidates), "unique_count": len(deduped.unique),
                  "merged": len(deduped.merges), "rejected": len(deduped.rejected),
                  "rule": "exact_key_match, deterministic_code"})

    queue: list[dict] = []
    for record in deduped.unique:
        evidence = core.build_evidence_ledger(record.get("claims", []), as_of=as_of)
        approved = set(evidence["approved_claim_ids"])
        gaps = sorted({c["subject"] for c in evidence["ledger"]
                       if c["id"] in approved and c["subject"]})
        declared = record.get("gap_categories") or []
        buyer = record.get("buyer") or {}
        route_findings = [
            {"category": entry["subject"], "status": entry["status"],
             "severity": record.get("gap_severity", "none")}
            for entry in evidence["ledger"] if entry["id"] in approved
        ]
        route = core.select_service_route(
            sorted(set(gaps) | set(declared)), service_routes,
            findings=route_findings, buyer=buyer,
            known_capabilities=set(cl.capability_index()),
        )
        signals = {
            "route_fit": route["fit"],
            "trigger_age_days": _trigger_age(record.get("trigger"), as_of),
            "evidence_quality": evidence["evidence_quality"],
            "reachability": _reachability(buyer),
            "gap_severity": record.get("gap_severity", "none"),
        }
        proof_claim = _proof_claim(route, service_routes, as_of)
        extra = [proof_claim] if proof_claim else []
        if buyer.get("email") or buyer.get("name"):
            extra.append({"id": "q-buyer", "subject": "buyer_accessibility",
                          "claim_key": "buyer_contact_route",
                          "value": buyer.get("email") or buyer.get("name"),
                          "status": "observed", "source": buyer.get("source"),
                          "observed_at": (record.get("trigger") or {}).get("observed_at")})
        trigger = record.get("trigger") or {}
        if trigger.get("type"):
            extra.append({"id": "q-trigger", "subject": "trigger_urgency",
                          "claim_key": "current_buyer_event", "value": trigger.get("type"),
                          "status": "observed", "source": trigger.get("source"),
                          "observed_at": trigger.get("observed_at")})
        full_ledger = core.build_evidence_ledger(
            (record.get("claims") or []) + extra, as_of=as_of)
        findings = [{"id": entry["id"], "category": entry["subject"],
                     "severity": record.get("gap_severity", "none")}
                    for entry in full_ledger["ledger"]]
        components = _qualification_components(
            findings, set(full_ledger["approved_claim_ids"]), buyer,
            signals["trigger_age_days"], route, service_routes)
        qualification = qv1.derive_and_score(components, full_ledger, {
            "canonical_domain": record.get("canonical_domain"),
            "normalized_company": record.get("normalized_company"),
            "contact_destination": buyer.get("email"),
            "service_route_exists": bool(route.get("route_id")),
            "contradicted_claim_ids": [e["id"] for e in full_ledger["ledger"]
                                       if e["status"] == "contradicted"],
        }, as_of=as_of)
        queue.append({
            "prospect_id": record.get("prospect_id") or record["entity_key"],
            "entity_key": record["entity_key"],
            "company": record.get("company"),
            "normalized_company": record.get("normalized_company"),
            "canonical_domain": record.get("canonical_domain"),
            "market": market,
            "service_route": route["route_id"],
            "route_fit": route["fit"],
            "matched_gaps": route["matched_gaps"],
            "evidence_quality": evidence["evidence_quality"],
            "approved_claim_count": len(approved),
            "qualification_score": qualification["score"],
            "qualification_tier": qualification["tier"],
            "qualification_model": qualification["model"],
            "actionability": qualification["actionability"],
            "component_scores": qualification["component_scores"],
            "signals": signals,
            "source_provenance": record.get("source_provenance", []),
            "lifecycle_stage": "qualified",
            "next_capability": route.get("diagnostic_capability"),
            "route_escalation": route.get("tied_routes"),
        })

    ranked = core.rank(queue)
    stage = core.advance(stage, "evidence_collected")
    stage = core.advance(stage, "qualified")
    steps.append({"stage": stage, "role": "lead-qualifier", "scored": len(ranked),
                  "rubric": "qualification-v1, evidence-attributed fixed arithmetic"})

    tiers = {name: sum(1 for item in ranked if item["qualification_tier"] == name)
             for name in ("HOT", "STRONG", "QUALIFIED", "WATCH", "DO_NOT_PURSUE")}
    return {
        "slice": "market_discovery",
        "as_of": as_of,
        "market": market,
        "sector_hypothesis": hypothesis,
        "lifecycle_stage": stage,
        "dedupe": {"merges": deduped.merges, "rejected": deduped.rejected},
        "tier_counts": tiers,
        "research_queue": ranked,
        "steps": steps,
        "external_action_authorized": False,
        "next_action": "run diagnostic capability on actionable HOT, STRONG and QUALIFIED rows, in rank order",
    }


def write_csv(path: Path, queue: list[dict]) -> None:
    columns = ["rank", "prospect_id", "company", "canonical_domain", "service_route",
               "qualification_score", "qualification_tier", "evidence_quality", "next_capability"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in queue:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    record = run(payload, args.as_of)
    text = json.dumps(record, indent=2, ensure_ascii=False)
    if args.out:
        target = args.out / "market-discovery"
        target.mkdir(parents=True, exist_ok=True)
        slug = (record.get("market") or "market").lower().replace(" ", "-")
        (target / f"{slug}-{args.as_of}.json").write_text(text + "\n", encoding="utf-8")
        if record.get("research_queue"):
            write_csv(target / f"{slug}-{args.as_of}-queue.csv", record["research_queue"])
        print(f"stage: {record['lifecycle_stage']}")
        print(f"written: {target}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
