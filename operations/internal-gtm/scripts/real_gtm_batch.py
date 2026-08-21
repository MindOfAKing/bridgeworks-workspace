#!/usr/bin/env python3
"""Build the first bounded no-send qualification batch from existing evidence only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
ENGINE_OPS = REPO_ROOT / "operations" / "client-acquisition-engine" / "research" / "prospect-operations"
sys.path.insert(0, str(GTM_ROOT / "adapters"))
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import engine_snapshot  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_v1 as qv1  # noqa: E402
from daily_objective import select_daily_objective  # noqa: E402


DIMENSIONS = ("problem_evidence", "commercial_fit", "buyer_accessibility",
              "trigger_urgency", "proof_fit", "execution_readiness")
SCALE_TERMS = ("employee", "customer", "countries", "cities", "locations", "years",
               "finance", "funding", "contract", "export", "markets", "clients")
TRIGGER_TERMS = ("expand", "new ", "launch", "finance", "growth", "transition", "hiring")


def _json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _sources() -> dict[str, dict]:
    path = ENGINE_OPS / "prospect-source-current.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["prospect_id"]: row for row in csv.DictReader(handle) if row.get("prospect_id")}


def _results() -> dict[str, dict]:
    found = {}
    for path in sorted((ENGINE_OPS / "results").glob("*.json")):
        for row in _json(path, {}).get("prospects", []):
            pid = row.get("prospect_id")
            if pid and str(row.get("checked_at", "")) >= str(found.get(pid, {}).get("checked_at", "")):
                found[pid] = row
    return found


def _named_buyer(text: str | None) -> bool:
    value = (text or "").strip().lower()
    return bool(value) and not value.startswith(("no ", "not verified", "the site does not"))


def _route_category(record: dict) -> str:
    text = " ".join(str(record.get(k) or "") for k in
                    ("commercial_gap", "recommended_angle", "proof_to_use")).lower()
    if any(word in text for word in ("ai visibility", "search", "discover", "citation", "demand-capture")):
        return "ai_visibility"
    if any(word in text for word in ("follow-up", "workflow", "routing", "reporting", "onboarding")):
        return "manual_followup"
    if any(word in text for word in ("quote", "website", "navigation", "page", "trust", "domain")):
        return "website_trust"
    return "positioning"


def _intelligence(pid: str, record: dict, source_row: dict, as_of: str) -> tuple[dict, dict, list[dict], dict]:
    sources = record.get("sources") or []
    observed_at = (record.get("checked_at") or as_of)[:10]
    commercial_findings, buyer_findings, claims = [], [], []

    for index, source in enumerate(sources, 1):
        url, text = source.get("url"), str(source.get("supports") or "")
        if not url:
            continue
        base = {"source": url, "observed_at": source.get("accessed_at") or observed_at,
                "status": "observed"}
        claim_id = f"{pid}-problem-{index}"
        claims.append({"id": claim_id, "subject": "problem_evidence",
                       "claim_key": f"public_problem_observation_{index}", "value": text, **base})
        hits = sorted(term for term in SCALE_TERMS if term in text.lower())
        if hits:
            finding = {"id": f"{pid}-ci-{index}", "category": "commercial_fit",
                       "claim_key": f"public_scale_or_growth_signal_{index}", "claim": text,
                       "value": {"matched_signals": hits}, "severity": "none", "tool": "existing_public_evidence", **base}
            commercial_findings.append(finding)
            claims.append({"id": finding["id"], "subject": "commercial_fit",
                           "claim_key": finding["claim_key"], "value": finding["value"], **base})

    destination = str(record.get("proposed_destination") or "").strip() or None
    decision_text = record.get("decision_maker")
    named = _named_buyer(decision_text)
    person = (source_row.get("contact_name") or "").strip() or (
        str(decision_text).split(" is publicly", 1)[0].split(" is listed", 1)[0] if named else None)
    buyer_source = next((s.get("url") for s in sources if s.get("url")), None)
    if named and buyer_source:
        buyer_findings.append({"id": f"{pid}-bi-person", "category": "buyer_accessibility",
            "claim_key": "decision_maker_identity", "claim": decision_text, "value": person,
            "severity": "none", "source": buyer_source, "observed_at": observed_at, "status": "observed"})
    if destination and buyer_source:
        buyer_findings.append({"id": f"{pid}-bi-route", "category": "buyer_accessibility",
            "claim_key": "public_business_contact_route", "claim": f"A public business route is recorded: {destination}",
            "value": destination, "severity": "none", "source": buyer_source,
            "observed_at": observed_at, "status": "observed"})
    for finding in buyer_findings:
        claims.append({k: finding[k] for k in ("id", "claim_key", "value", "status", "source", "observed_at")} |
                      {"subject": "buyer_accessibility"})

    trigger_text = source_row.get("trigger_observation") or record.get("recommended_angle") or ""
    trigger_url = (source_row.get("evidence_urls") or "").split(" | ")[0] or buyer_source
    trigger_hit = any(term in trigger_text.lower() for term in TRIGGER_TERMS)
    if trigger_text and trigger_url:
        claims.append({"id": f"{pid}-trigger", "subject": "trigger_urgency", "value": trigger_text,
                       "status": "observed", "source": trigger_url,
                       "observed_at": source_row.get("checked_at") or observed_at})

    category = _route_category(record)
    routes = _json(GTM_ROOT / "service-routes.yaml", {})
    route = core.select_service_route([category], routes,
        findings=[{"id": f"{pid}-route-signal", "category": category, "severity": "medium",
                   "status": "observed", "source": buyer_source, "observed_at": observed_at,
                   "claim": record.get("commercial_gap") or trigger_text}],
        buyer={"role": source_row.get("contact_role")}, known_capabilities=None)
    proof_id = route.get("proof_asset_id")
    proof = next((p for p in routes.get("proof_assets", []) if p["id"] == proof_id), None)
    proof_strength = (proof.get("route_strength") or {}).get(route.get("route_id")) if proof else None
    if proof:
        claims.append({"id": f"{pid}-proof", "subject": "proof_fit", "value": proof["claim"],
                       "status": proof.get("status", "verified"), "source": proof.get("source"),
                       "observed_at": as_of})

    if destination and buyer_source:
        claims.append({"id": f"{pid}-execution", "subject": "execution_readiness",
                       "value": "A public business contact route exists for a bounded next step.",
                       "status": "observed", "source": buyer_source, "observed_at": observed_at})

    scale_count = sum(len(f["value"]["matched_signals"]) for f in commercial_findings)
    problem_ids = [c["id"] for c in claims if c["subject"] == "problem_evidence"]
    components = {
        "problem_evidence": {"score": min(20, 8 + len(problem_ids) * 3) if record.get("commercial_gap") else min(10, len(problem_ids) * 2), "evidence_ids": problem_ids, "research_status": "complete" if record.get("commercial_gap") and sources else "partial" if sources else "required"},
        "commercial_fit": {"score": min(14, scale_count * 2), "evidence_ids": [f["id"] for f in commercial_findings], "research_status": "complete" if scale_count >= 3 else "partial" if scale_count else "required"},
        "buyer_accessibility": {"score": 15 if named and destination else 9 if named else 4 if destination else 0, "evidence_ids": [f["id"] for f in buyer_findings], "research_status": "complete" if named and destination else "partial" if buyer_findings else "required"},
        "trigger_urgency": {"score": 12 if trigger_hit else 5 if trigger_text else 0, "evidence_ids": [f"{pid}-trigger"] if trigger_text and trigger_url else [], "research_status": "complete" if trigger_hit else "partial" if trigger_text else "required"},
        "proof_fit": {"score": 15 if proof_strength == "strong" else 8 if proof_strength == "partial" else 0, "evidence_ids": [f"{pid}-proof"] if proof else [], "research_status": "complete" if proof_strength else "required"},
        "execution_readiness": {"score": 4 if destination else 0, "evidence_ids": [f"{pid}-execution"] if destination and buyer_source else [], "research_status": "partial" if destination else "required"},
    }
    commercial = {"capability": "bridgeworks-commercial-intelligence", "prospect_id": pid,
        "as_of": as_of, "stage": "targeted_enrichment_from_existing_public_evidence",
        "findings": commercial_findings, "commercial_value_band": {"low": None, "high": None,
        "currency": None, "basis": None, "confidence": "none"},
        "procurement_complexity": "unknown", "engagement_size_fit": "plausible" if scale_count >= 3 else "unknown",
        "unresolved_questions": [] if scale_count >= 3 else ["More public scale or budget-capacity evidence is required."],
        "external_action_authorized": False}
    buyer = {"capability": "bridgeworks-buyer-intelligence", "prospect_id": pid, "as_of": as_of,
        "stage": "targeted_enrichment_from_existing_public_evidence",
        "roles": {"decision_maker": {"person": person if named else None,
                   "title": source_row.get("contact_role") or None,
                   "evidence_id": f"{pid}-bi-person" if named else None,
                   "attribution_confidence": "medium" if named else "none"}},
        "contact_route": {"destination": destination, "destination_type": "general" if destination else "none",
                          "source": buyer_source if destination else None,
                          "lawful_basis_note": "public business contact route recorded in prior research"},
        "findings": buyer_findings,
        "unresolved_questions": [] if named and destination else ["Verify the exact budget owner and a lawful direct or role-specific destination."],
        "external_action_authorized": False}
    return commercial, buyer, claims, {"components": components, "route": route, "proof": proof}


def build(as_of: str) -> dict:
    # A real batch is an immutable decision snapshot. Once created, reruns read
    # it instead of reselecting against the state that the batch itself changed.
    existing = (GTM_ROOT / "runs" / "qualification-batches" /
                f"internal-gtm-qualification-{as_of}-01.json")
    persisted = _json(existing, {})
    if persisted.get("as_of") == as_of and persisted.get("prospects"):
        return persisted
    snapshot = engine_snapshot.build(as_of)
    objective = select_daily_objective(snapshot)
    raw_results, source_rows = _results(), _sources()
    by_id = {p["prospect_id"]: p for p in snapshot["prospects"]}
    rows = []
    for priority in objective.get("enrichment_cohort", []):
        pid = priority["prospect_id"]
        record, source_row, state = raw_results[pid], source_rows.get(pid, {}), by_id[pid]
        commercial, buyer, claims, intelligence = _intelligence(pid, record, source_row, as_of)
        ledger = core.build_evidence_ledger(claims, as_of=as_of)
        destination = buyer["contact_route"]["destination"]
        route = intelligence["route"]
        qualification = qv1.score(intelligence["components"], ledger, {
            "canonical_domain": source_row.get("canonical_domain") or record.get("owned_domain"),
            "normalized_company": record.get("company"),
            "contact_destination": destination,
            "service_route_exists": bool(route.get("route_id")),
            "contradicted_claim_ids": [], "communication_state_resolved": True,
            "prior_outreach": False, "legal_exclusion": False,
            "hold_reason": None,
        }, as_of)
        coverage = qualification["qualification_coverage"]
        warrants_diagnostic = (qualification["tier"] in {"HOT", "STRONG", "QUALIFIED"}
                               and qualification["actionability"] == "actionable"
                               and coverage["percentage"] >= 66.7)
        selected_diagnostic = ("geo-audit" if pid == "tilz-prosperitas" and warrants_diagnostic
                               else route.get("diagnostic_capability"))
        diagnostic = {"capability": selected_diagnostic,
                      "result": "not_justified_at_current_qualification_coverage"}
        if warrants_diagnostic:
            diagnostic["result"] = "justified_but_not_run_in_stage_2"
        if pid == "tilz-prosperitas" and warrants_diagnostic:
            partial = _json(GTM_ROOT / "migration" / "phase-2" / "acceptance" / "tilz-geo-audit-partial-2026-08-11.json", {})
            diagnostic = {"capability": "geo-audit", "result": "existing_partial_diagnostic",
                          "detail": partial, "gate": "partial result cannot support outreach preparation"}
        if pid == "bv-integrated-ltd" and warrants_diagnostic:
            diagnostic = {
                "capability": "bridgeworks-ai-workflow-scan",
                "result": "completed_internal_test_draft",
                "artifact": "operations/internal-gtm/runs/qualification-batches/AI-WORKFLOW-SCAN-BV-INTEGRATED-2026-08-11.md",
                "candidate_score": 5.0,
                "gate": "buyer-facing release blocked until the workflow owner validates the hypothesis",
            }
        reaches_commercial_prep = warrants_diagnostic and diagnostic["result"] not in {
            "justified_but_not_run_in_stage_2", "existing_partial_diagnostic",
            "completed_internal_test_draft"}
        rows.append({
            "prospect_id": pid, "company": record.get("company"), "priority": priority,
            "existing_trigger": source_row.get("trigger_observation") or state.get("existing_trigger"),
            "problem_evidence": record.get("commercial_gap") or state.get("problem_evidence"),
            "qualification_v1": qualification,
            "commercial_intelligence": commercial, "buyer_intelligence": buyer,
            "selected_service_route": route.get("route_id"),
            "selected_diagnostic_capability": selected_diagnostic,
            "diagnostic": diagnostic,
            "chosen_proof": intelligence["proof"],
            "offer_hypothesis": next((r.get("wedge") for r in _json(GTM_ROOT / "service-routes.yaml", {}).get("routes", [])
                                      if r.get("id") == route.get("route_id")), None),
            "next_action": ("complete_stage_2_coverage" if coverage["percentage"] < 66.7 else
                            "validate_workflow_hypothesis" if diagnostic["result"] == "completed_internal_test_draft" else
                            "complete_justified_diagnostic" if not reaches_commercial_prep else
                            "prepare_approval_packet"),
            "approval_packet": None,
            "external_action_authorized": False,
        })
    return {"batch_id": f"internal-gtm-qualification-{as_of}-01", "as_of": as_of,
            "objective": objective, "progressive_spend_stage": 2,
            "prospects": rows, "approval_packets_created": 0,
            "note": "No prospect completed a justified diagnostic, so none reached commercial preparation.",
            "external_action_authorized": False}


def render_md(batch: dict) -> str:
    lines = [f"# Internal GTM Qualification Batch, {batch['as_of']}", "",
             f"Priority class: `{batch['objective']['priority_class']}`", "",
             "This is a no-send Stage 1 and Stage 2 batch. Priority score is for enrichment order only. It is not qualification-v1.", ""]
    for row in batch["prospects"]:
        q, coverage = row["qualification_v1"], row["qualification_v1"]["qualification_coverage"]
        scores = q["component_scores"]
        lines += [f"## {row['company']}", "",
            f"- Existing trigger: {row['existing_trigger'] or 'No specific trigger verified.'}",
            f"- Problem evidence: {row['problem_evidence'] or 'Not established.'}",
            f"- Qualification-v1: `{q['score']}` / `{q['tier']}` / `{q['actionability']}`",
            f"- Components: " + ", ".join(f"{name} {scores[name]}" for name in DIMENSIONS),
            f"- Coverage: `{coverage['sufficiently_researched_dimensions']}/{coverage['total_dimensions']}` ({coverage['percentage']}%)",
            f"- Commercial Intelligence: {len(row['commercial_intelligence']['findings'])} approved-source candidate findings; fit `{row['commercial_intelligence']['engagement_size_fit']}`.",
            f"- Buyer Intelligence: decision maker `{row['buyer_intelligence']['roles']['decision_maker']['person']}`; destination `{row['buyer_intelligence']['contact_route']['destination']}`.",
            f"- Route: `{row['selected_service_route']}`",
            f"- Diagnostic: `{row['selected_diagnostic_capability']}`; result `{row['diagnostic']['result']}`",
            f"- Proof: `{(row['chosen_proof'] or {}).get('id')}`",
            f"- Offer hypothesis: {row['offer_hypothesis']}",
            f"- Next action: `{row['next_action']}`", ""]
    lines += ["## Approval packets", "", "None. No prospect completed Stage 3, so commercial preparation was not permitted.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default="2026-08-11")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    batch = build(args.as_of)
    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"{batch['batch_id']}"
    (args.out / f"{stem}.json").write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / f"{stem}.md").write_text(render_md(batch), encoding="utf-8")
    print(json.dumps({"batch_id": batch["batch_id"], "prospects": len(batch["prospects"]),
                      "approval_packets_created": batch["approval_packets_created"],
                      "objective": batch["objective"]["objective_type"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
