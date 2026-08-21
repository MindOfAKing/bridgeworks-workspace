#!/usr/bin/env python3
"""Vertical slice 1: website URL -> geo-audit -> evidence -> route -> offer -> packet.

HOW TO USE
    python operations/internal-gtm/scripts/run_geo_slice.py \
        --input operations/internal-gtm/examples/geo-slice-input.json \
        --as-of 2026-08-11 --out operations/internal-gtm/runs
Without a `diagnostic` block the run stops at diagnostic_selected and prints the
exact geo-audit capability call to make. It never invents a diagnostic result and
it never sends anything. The last stage it can reach is awaiting_approval.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import capability_loader as cl  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_v1 as qv1  # noqa: E402


def _reachability(buyer: dict | None) -> str:
    if not buyer:
        return "none"
    if buyer.get("email") and buyer.get("name"):
        return "named_buyer_with_email"
    if buyer.get("name"):
        return "named_buyer"
    if buyer.get("email") or buyer.get("contact_form"):
        return "generic_contact"
    return "none"


def _trigger_age(trigger: dict | None, as_of: str) -> int | None:
    if not trigger or not trigger.get("observed_at"):
        return None
    return core._days_between(trigger["observed_at"], as_of)


def _worst_severity(findings: list[dict], approved_ids: set[str]) -> str:
    order = ("high", "medium", "low")
    present = {f["severity"] for f in findings if f["id"] in approved_ids}
    for level in order:
        if level in present:
            return level
    return "none"



def _qualification_claims(payload: dict, diagnostic: dict, service_routes: dict) -> list[dict]:
    """Extra sourced claims so buyer, trigger and proof are attributable evidence.

    qualification-v1 requires every non-zero component to cite evidence. A buyer
    email and a trigger are evidence too, so they enter the ledger with their own
    source and date. Anything without a source becomes `unknown` and scores zero,
    which is the correct outcome, not a workaround.
    """
    claims: list[dict] = []
    buyer = payload.get("buyer") or {}
    buyer_source = buyer.get("source") or (payload.get("trigger") or {}).get("source")
    if buyer.get("email") or buyer.get("name"):
        claims.append({
            "id": "q-buyer", "subject": "buyer_accessibility", "claim_key": "buyer_contact_route",
            "value": {"name": buyer.get("name"), "email": buyer.get("email")},
            "status": "observed", "source": buyer_source,
            "observed_at": diagnostic.get("completed_at"),
        })
    trigger = payload.get("trigger") or {}
    if trigger.get("type"):
        claims.append({
            "id": "q-trigger", "subject": "trigger_urgency", "claim_key": "current_buyer_event",
            "value": trigger.get("type"), "status": "observed",
            "source": trigger.get("source"), "observed_at": trigger.get("observed_at"),
        })
    return claims


def _proof_claim(route: dict, service_routes: dict, as_of: str) -> dict | None:
    """The BridgeWorks proof asset is evidence about BridgeWorks, and it is sourced."""
    asset = next((a for a in service_routes.get("proof_assets", [])
                  if a["id"] == route.get("proof_asset_id")), None)
    if not asset:
        return None
    return {
        "id": f"q-proof-{asset['id']}", "subject": "proof_fit", "claim_key": "bridgeworks_proof_asset",
        "value": asset["id"], "status": asset.get("status", "unknown"),
        "source": asset.get("source"), "observed_at": as_of,
    }


PROOF_STRENGTH_POINTS = {"strong": 15, "partial": 8}
SEVERITY_POINTS = {"high": 8, "medium": 5, "low": 2}
BUYER_POINTS = {"named_buyer_with_email": 15, "named_buyer": 9, "generic_contact": 4, "none": 0}
TRIGGER_POINTS = ((30, 15), (90, 9), (180, 4))


def _qualification_components(findings, approved_ids, buyer, trigger_age, route, service_routes):
    """Derive what the diagnostic can evidence. Leave the rest at zero, explicitly."""
    mine = [f for f in findings if f["id"] in approved_ids]
    problem = min(25, sum(SEVERITY_POINTS.get(f.get("severity"), 0) for f in mine))

    buyer_points = BUYER_POINTS[_reachability(buyer)]
    trigger_points = 0
    if trigger_age is not None and trigger_age >= 0:
        trigger_points = next((points for limit, points in TRIGGER_POINTS if trigger_age <= limit), 0)

    asset = next((a for a in service_routes.get("proof_assets", [])
                  if a["id"] == route.get("proof_asset_id")), None)
    strength = (asset.get("route_strength") or {}).get(route.get("route_id")) if asset else None
    proof_points = PROOF_STRENGTH_POINTS.get(strength, 0)

    return {
        "problem_evidence": {"score": problem, "evidence_ids": sorted(f["id"] for f in mine),
                             "research_status": "complete" if mine else "required",
                             "rationale": "approved diagnostic findings weighted by severity"},
        "buyer_accessibility": {"score": buyer_points, "evidence_ids": ["q-buyer"],
                                "research_status": "complete" if _reachability(buyer) == "named_buyer_with_email" else "partial" if buyer_points else "required",
                                "rationale": "verified contact route"},
        "trigger_urgency": {"score": trigger_points, "evidence_ids": ["q-trigger"],
                            "research_status": "complete" if trigger_points else "required",
                            "rationale": "age of the observed buyer event"},
        "proof_fit": {"score": proof_points,
                      "evidence_ids": [f"q-proof-{asset['id']}"] if asset else [],
                      "research_status": "complete" if proof_points else "required",
                      "rationale": f"verified proof asset strength for this problem: {strength}"},
        # Not derivable from a website diagnostic. Zero with an explicit gap, never guessed.
        "commercial_fit": {"score": 0, "evidence_ids": [],
                           "research_status": "required",
                           "rationale": "no contract-value, budget or segment evidence collected"},
        "execution_readiness": {"score": 0, "evidence_ids": [],
                                "research_status": "required",
                                "rationale": "no delivery-capacity or decision-process evidence collected"},
    }


def run(payload: dict, as_of: str) -> dict:
    cl.assert_single_registry()
    service_routes = cl.load_service_routes()

    company = payload.get("company") or ""
    website = payload.get("website_url") or ""
    identity = core.dedupe([{
        "company": company,
        "website_url": website,
        "source": payload.get("source", "manual_input"),
    }])
    if not identity.unique:
        raise ValueError("input needs a company name or a website URL")
    prospect = identity.unique[0]
    prospect["prospect_id"] = payload.get("prospect_id") or prospect["entity_key"]
    buyer = payload.get("buyer") or {}
    prospect.update({
        "buyer_name": buyer.get("name"),
        "buyer_role": buyer.get("role"),
        "buyer_email": buyer.get("email"),
    })

    stage = "account_discovered"
    steps: list[dict] = [{"stage": stage, "role": "data-steward", "note": "identity normalized, exact dedupe applied"}]

    diagnostic = payload.get("diagnostic")
    if not diagnostic:
        # No evidence, no qualification, no route yet. The stage does not move.
        # A diagnostic capability call is requested; requesting it is not a transition.
        request = cl.capability_call_request(
            role_id="prospect-router",
            capability_id="geo-audit",
            task="diagnostic_capability_run",
            payload={"website_url": website, "company": company,
                     "expected_schema": "operations/internal-gtm/schemas/geo-diagnostic.schema.json"},
        )
        steps.append({"stage": stage, "role": "prospect-router",
                      "note": "geo-audit not yet run; stage stays at account_discovered"})
        return {
            "slice": "geo",
            "as_of": as_of,
            "prospect": prospect,
            "lifecycle_stage": stage,
            "blocked_on": request,
            "steps": steps,
            "external_action_authorized": False,
        }

    findings = diagnostic["findings"]
    claims = [{
        "id": f["id"],
        "subject": f["category"],
        # subject is the routing category; claim_key is the exact proposition.
        # See gtm_core.claim_contradiction_key for the system-wide invariant.
        "claim_key": f.get("claim_key"),
        "value": f.get("value", f["claim"]),
        "status": f["status"],
        "source": f.get("source"),
        "observed_at": f.get("observed_at") or diagnostic.get("completed_at"),
    } for f in findings]
    evidence = core.build_evidence_ledger(claims, as_of=as_of)
    stage = core.advance(stage, "evidence_collected")
    steps.append({"stage": stage, "role": "evidence-auditor",
                  "note": f"{len(evidence['approved_claim_ids'])} of {len(claims)} claims approved",
                  "counts": evidence["counts"]})

    approved_ids = set(evidence["approved_claim_ids"])
    gap_categories = sorted({f["category"] for f in findings if f["id"] in approved_ids})
    route = core.select_service_route(
        gap_categories, service_routes,
        findings=[f for f in findings if f["id"] in approved_ids],
        buyer=buyer,
        known_capabilities={
            item_id for item_id, item in cl.capability_index().items()
            if item.get("status") == "active"
        },
    )

    signals = {
        "route_fit": route["fit"],
        "trigger_age_days": _trigger_age(payload.get("trigger"), as_of),
        "evidence_quality": evidence["evidence_quality"],
        "reachability": _reachability(buyer),
        "gap_severity": _worst_severity(findings, approved_ids),
    }
    # qualification-v1 is canonical. It scores whether BridgeWorks should invest
    # further effort. It never sees the route id or the diagnostic score.
    extra = _qualification_claims(payload, diagnostic, service_routes)
    proof_claim = _proof_claim(route, service_routes, as_of)
    if proof_claim:
        extra.append(proof_claim)
    full_ledger = core.build_evidence_ledger(claims + extra, as_of=as_of)
    components = _qualification_components(
        findings, approved_ids, buyer, signals["trigger_age_days"], route, service_routes)
    qualification = qv1.score(components, full_ledger, {
        "canonical_domain": prospect.get("canonical_domain"),
        "normalized_company": prospect.get("normalized_company"),
        "contact_destination": prospect.get("buyer_email"),
        "service_route_exists": bool(route.get("route_id")),
        "prior_outreach": bool(payload.get("prior_outreach")),
        "communication_state_resolved": bool(payload.get("communication_state_resolved", True)),
        "contradicted_claim_ids": [e["id"] for e in full_ledger["ledger"]
                                   if e["status"] == "contradicted"],
        "legal_exclusion": payload.get("legal_exclusion"),
        "hold_reason": payload.get("hold_reason"),
    }, as_of=as_of)
    qualification["superseded_reference"] = {
        "model": "former-gtm-core-five-signal-rubric",
        "historical_signals": signals,
        "score": None,
        "tier": None,
        "note": "source material only. It cannot independently own qualification state.",
    }
    prospect["qualification_model"] = qualification["model"]
    prospect["qualification_score"] = qualification["score"]
    prospect["qualification_tier"] = qualification["tier"]
    prospect["actionability"] = qualification["actionability"]
    stage = core.advance(stage, "qualified")
    steps.append({"stage": stage, "role": "lead-qualifier", "signals": signals,
                  "result": {k: v for k, v in qualification.items() if k != "components"}})

    record = {
        "slice": "geo",
        "as_of": as_of,
        "prospect": prospect,
        "evidence": full_ledger,
        "route": route,
        "qualification": qualification,
        "steps": steps,
        "external_action_authorized": False,
    }

    if route["fit"] == "tie":
        record["lifecycle_stage"] = stage
        record["next_action"] = "strategic_route_decision"
        record["blocked_on"] = cl.capability_call_request(
            role_id="prospect-router",
            capability_id="revops",
            task="strategic_recommendation",
            payload={"tied_routes": route["tied_routes"],
                     "tie_break_order": route["tie_break_order"],
                     "candidates": route["candidates"],
                     "escalation": route["escalation"]},
        )
        steps.append({"stage": stage, "role": "prospect-router",
                      "note": "routes tied on all six commercial dimensions, escalated"})
        return record

    if qualification["tier"] == "DO_NOT_PURSUE":
        record["lifecycle_stage"] = stage
        record["next_action"] = "nurture"
        record["next_action_reason"] = [c["reason"] for c in qualification["components"]]
        return record

    if qualification["actionability"] != qv1.ACTIONABLE:
        record["lifecycle_stage"] = stage
        record["next_action"] = "resolve_blocking_condition"
        record["blocking_conditions"] = qualification["blocking_conditions"]
        steps.append({"stage": stage, "role": "lead-qualifier",
                      "note": f"score {qualification['score']} {qualification['tier']}, "
                              f"actionability {qualification['actionability']}"})
        return record

    stage = core.advance(stage, "routed")
    steps.append({"stage": stage, "role": "prospect-router", "route": route})
    stage = core.advance(stage, "diagnostic_selected")
    steps.append({"stage": stage, "role": "prospect-router",
                  "capability": diagnostic["capability"], "note": "diagnostic selected"})
    stage = core.advance(stage, "diagnostic_complete")
    steps.append({"stage": stage, "role": "prospect-router",
                  "capability": diagnostic["capability"], "score": diagnostic.get("score")})

    offer = core.select_offer_wedge(route["route_id"], qualification["tier"], service_routes)
    stage = core.advance(stage, "offer_selected")
    steps.append({"stage": stage, "role": "offer-strategist", "offer": offer})

    cited = [f["id"] for f in findings
             if f["id"] in approved_ids and f["category"] in set(route["matched_gaps"])]
    packet = core.build_outreach_packet(prospect, evidence, route, offer, cited, as_of)
    stage = core.advance(stage, "outreach_prepared")
    steps.append({"stage": stage, "role": "outreach-personalizer",
                  "note": "packet assembled from approved claims only", "cited_claims": cited})

    packet["copy_request"] = cl.capability_call_request(
        role_id="outreach-personalizer",
        capability_id="market-emails",
        task="client_facing_output",
        payload={"cited_claims": cited, "offer_wedge": offer["wedge"],
                 "proof_asset_id": offer["proof_asset_id"], "buyer": buyer},
    )
    if not prospect.get("buyer_email"):
        packet.update({
            "kind": "outreach_preparation_packet",
            "lifecycle_stage": "outreach_prepared",
            "approval_state": "blocked_missing_destination",
            "approval_payload_digest": None,
            "approval_instruction": "Verify an exact lawful destination before requesting approval.",
        })
        steps.append({"stage": stage, "role": "outreach-personalizer",
                      "note": "approval blocked because no exact destination is verified"})
        next_action = "verify_exact_destination"
    else:
        stage = core.advance(stage, "awaiting_approval")
        steps.append({"stage": stage, "role": "outreach-personalizer", "note": "stopped at approval gate"})
        next_action = "emmanuel_approval"
    record["offer"] = offer
    record["packet"] = packet
    record["lifecycle_stage"] = stage
    record["next_action"] = next_action
    return record


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
        target = args.out / "geo"
        target.mkdir(parents=True, exist_ok=True)
        name = f"{record['prospect']['prospect_id'].replace(':', '-').replace('.', '-')}-{args.as_of}.json"
        (target / name).write_text(text + "\n", encoding="utf-8")
        print(f"stage: {record['lifecycle_stage']}")
        print(f"written: {target / name}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
