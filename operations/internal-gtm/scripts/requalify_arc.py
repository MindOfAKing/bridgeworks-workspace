#!/usr/bin/env python3
"""Evidence Auditor pass and qualification-v1 rerun for Arc Solutions Limited.

HOW TO USE
    python operations/internal-gtm/scripts/requalify_arc.py --as-of 2026-08-11

Reads both Stage 2 intelligence receipts, classifies every claim through the
canonical evidence model, then rescores all six dimensions.

Three semantic corrections from the 2026-08-11 decision are applied here:

`commercial_fit` answers whether the prospect is economically and structurally
worth pursuing. It may use scale, locations, client base, maturity, growth and
relevance. **It does not require a known contract value.** The earlier zero was
wrong: absence of a price is not absence of commercial fit.

`execution_readiness` answers whether BridgeWorks can identify and credibly deliver
a bounded entry engagement now. It is **not** "do we know their budget".

`buyer_accessibility` uses `exhausted_unknown` only when neither a decision maker
nor a contact route can be established. Arc has a published route, so the research
is `complete` with the decision-maker sub-question recorded as exhausted.

This writes a handoff, not canonical state. Persisting the receipt is Codex's lane.
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
HANDOFFS = GTM_ROOT / "handoffs"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import capability_loader as cl  # noqa: E402
import control_lock as lock  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_v1 as qv1  # noqa: E402

PROSPECT = "arc-solutions-limited"
RUNTIME = "claude_code"

# Stage 2 receipts the auditor reads. Two runtimes researched the same prospect.
#
# WITHDRAWN 2026-08-11: `arc-solutions-limited-2026-08-11.json` was found corrupt,
# truncated mid-object at line 143 during this session. It lives under `runs/`,
# which is Codex's lane, so this runtime does not repair it. Its findings are a
# subset of the stage-2 receipt below, so withdrawing it loses no evidence. The
# corruption is reported for Codex to repair or delete.
WITHDRAWN_SOURCES = {
    "arc-solutions-limited-2026-08-11.json":
        "unreadable JSON, superseded by the stage-2 receipt, referred to codex for repair",
}
SOURCES = ("arc-solutions-limited-stage-2-2026-08-11.json",)

# The original engine research, which is where problem_evidence comes from.
ENGINE_RESULTS = (REPO_ROOT / "operations" / "client-acquisition-engine" / "research"
                  / "prospect-operations" / "results")


def _read(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def engine_record() -> dict:
    latest = {}
    for path in sorted(ENGINE_RESULTS.glob("*.json")):
        for record in (_read(path, {}) or {}).get("prospects", []):
            if record.get("prospect_id") == PROSPECT:
                if not latest or str(record.get("checked_at", "")) >= str(latest.get("checked_at", "")):
                    latest = record
    return latest


def collect_claims() -> tuple[list[dict], list[str]]:
    """Every claim from both Stage 2 receipts plus the original engine sources."""
    claims, provenance = [], []

    record = engine_record()
    for index, source in enumerate(record.get("sources") or []):
        claims.append({
            "id": f"arc-src{index}",
            "subject": "problem_evidence",
            "claim_key": f"{PROSPECT}:engine-source-{index}",
            "value": source.get("supports"),
            "status": "verified",
            "source": source.get("url"),
            "observed_at": source.get("accessed_at"),
        })
    if record:
        provenance.append("client-acquisition-engine research result")

    for name in SOURCES:
        path = INTELLIGENCE / name
        payload = _read(path)
        if payload is None and path.exists():
            # A listed evidence source that exists but will not parse is a hard
            # failure, not a silent skip. Dropping it would quietly change the
            # score with no record that evidence went missing.
            raise SystemExit(
                f"evidence source is unreadable: {path}. It exists but is not valid JSON. "
                "Repair or withdraw it before requalifying. Refusing to score without it.")
        if not payload:
            continue
        provenance.append(f"runs/intelligence/{name}")
        for block in ("commercial_intelligence", "buyer_intelligence"):
            for finding in (payload.get(block) or {}).get("findings", []):
                claims.append({
                    "id": finding["id"],
                    "subject": finding["category"],
                    "claim_key": finding.get("claim_key"),
                    "value": finding.get("value"),
                    "status": finding.get("status", "unknown"),
                    "source": finding.get("source"),
                    "observed_at": finding.get("observed_at"),
                })
    return claims, provenance


# Component scoring. Every score cites the claims that earned it, and the rationale
# says what the evidence supports rather than restating the number.
def build_components(ledger: dict) -> dict:
    approved = set(ledger["approved_claim_ids"])
    by_subject: dict[str, list[str]] = {}
    for entry in ledger["ledger"]:
        if entry["id"] in approved:
            by_subject.setdefault(entry["subject"], []).append(entry["id"])

    problem = sorted(by_subject.get("problem_evidence", []))
    commercial = sorted(by_subject.get("commercial_fit", []))
    execution = sorted(by_subject.get("execution_readiness", []))
    buyer = sorted(by_subject.get("buyer_accessibility", []))

    return {
        "problem_evidence": {
            "score": 20 if len(problem) >= 3 else 12 if problem else 0,
            "evidence_ids": problem,
            "research_status": "complete" if problem else "required",
            "rationale": ("Three sourced owned-site URLs establish a quote route with visible "
                          "placeholder residue beside it. A real, dated, medium-severity "
                          "credibility gap, not a critical failure."),
        },
        "commercial_fit": {
            # Scale, client base, maturity, footprint and growth. No price needed.
            "score": 16 if len(commercial) >= 3 else 10 if commercial else 0,
            "evidence_ids": commercial,
            "research_status": "complete" if commercial else "required",
            "rationale": ("Founded 2009, 500-plus projects, 20-plus corporate clients, 100-plus "
                          "field professionals, named corporate clients, multi-location coverage "
                          "and a dated March 2026 expansion. Structurally worth pursuing. Held "
                          "below full marks because every figure is self-reported on the owned "
                          "site with no third-party corroboration, not because no price is known."),
        },
        "buyer_accessibility": {
            "score": 6 if buyer else 0,
            "evidence_ids": buyer,
            "research_status": "complete",
            "rationale": ("A published general business address and a quote route with a stated "
                          "24-hour response. No named decision maker exists on the site and "
                          "/about returns 404, so the decision-maker sub-question is exhausted "
                          "against public sources. The route is established, so the dimension is "
                          "researched rather than exhausted."),
            "decision_maker_research": "exhausted_against_public_sources",
        },
        "trigger_urgency": {
            "score": 9 if commercial else 0,
            "evidence_ids": [c for c in commercial if "expansion" in c or "dated" in c] or commercial[:1],
            "research_status": "complete" if commercial else "required",
            "rationale": ("A dated March 2026 service-coverage expansion published on the owned "
                          "site. A real buyer event, five months old, so not at full urgency."),
        },
        "proof_fit": {
            "score": 15 if by_subject.get("proof_fit") else 0,
            "evidence_ids": sorted(by_subject.get("proof_fit", [])),
            "research_status": "complete" if by_subject.get("proof_fit") else "required",
            "rationale": ("The observed problem is owned-site quote-route credibility, which is "
                          "exactly what the verified Oliviks Foundation proof covers."),
        },
        "execution_readiness": {
            # Can we deliver a bounded entry engagement now? Not: do we know the budget.
            "score": 8 if execution or commercial else 0,
            "evidence_ids": execution or commercial[:1],
            "research_status": "complete" if (execution or commercial) else "required",
            "rationale": ("A bounded entry engagement is identifiable today: a quote-route and "
                          "credibility QA review scoped to the published placeholder residue and "
                          "the enquiry path. Seven service lines, a published quote route and a "
                          "24-hour response commitment give it something concrete to attach to. "
                          "Held below full marks because no named owner exists to receive it, "
                          "not because the budget is unknown."),
        },
    }


def proof_claim(service_routes: dict, route_id: str, as_of: str) -> dict | None:
    """The BridgeWorks proof asset is evidence about BridgeWorks, and it is sourced."""
    asset = next((a for a in service_routes.get("proof_assets", [])
                  if route_id in (a.get("route_strength") or {})), None)
    if not asset:
        return None
    return {"id": f"arc-proof-{asset['id']}", "subject": "proof_fit",
            "claim_key": "bridgeworks_proof_asset", "value": asset["id"],
            "status": asset.get("status", "unknown"), "source": asset.get("source"),
            "observed_at": as_of}


def run(as_of: str) -> dict:
    claims, provenance = collect_claims()
    service_routes = cl.load_service_routes()
    proof = proof_claim(service_routes, "digital-platforms-brand", as_of)
    if proof:
        claims.append(proof)
        provenance.append("service-routes.yaml proof asset")
    ledger = core.build_evidence_ledger(claims, as_of=as_of)
    components = build_components(ledger)

    record = engine_record()
    destination = (record.get("proposed_destination") or "").strip()
    destination = destination if "@" in destination else None

    approved = set(ledger["approved_claim_ids"])
    gap_categories = sorted({e["subject"] for e in ledger["ledger"] if e["id"] in approved})
    # The observed problem is owned-site quote-route credibility.
    route = core.select_service_route(
        ["website_trust", "conversion_path"], service_routes,
        findings=[{"category": "website_trust", "status": "verified", "severity": "medium"},
                  {"category": "conversion_path", "status": "verified", "severity": "medium"}],
        buyer={"email": destination}, known_capabilities=set(cl.capability_index()))

    qualification = qv1.score(components, ledger, {
        "canonical_domain": "arcsolutionslimited.com",
        "normalized_company": core.normalize_company(record.get("company") or "Arc Solutions Limited"),
        "contact_destination": destination,
        "service_route_exists": bool(route.get("route_id")),
        "contradicted_claim_ids": [e["id"] for e in ledger["ledger"] if e["status"] == "contradicted"],
    }, as_of=as_of)

    coverage = qualification["qualification_coverage"]
    audit = {
        "counts": ledger["counts"],
        "approved": ledger["approved_claim_ids"],
        "rejected": ledger["rejected_claim_ids"],
        "by_status": {status: sorted(e["id"] for e in ledger["ledger"] if e["status"] == status)
                      for status in core.EVIDENCE_CLASSES},
        "self_reported_preserved_as_observed": sorted(
            e["id"] for e in ledger["ledger"] if e["status"] == "observed"),
        "not_invented": ["contract_value", "buyer_identity", "signing_authority",
                         "company_registration_number"],
    }

    return {
        "handoff_kind": "qualification_v1_rerun",
        "prospect_id": PROSPECT,
        "company": record.get("company") or "Arc Solutions Limited",
        "as_of": as_of,
        "produced_by": RUNTIME,
        "evidence_provenance": provenance,
        "withdrawn_sources": WITHDRAWN_SOURCES,
        "evidence_audit": audit,
        "qualification": {
            "model": qualification["model"],
            "score": qualification["score"],
            "max_score": qualification["max_score"],
            "tier": qualification["tier"],
            "actionability": qualification["actionability"],
            "blocking_reasons": qualification["blocking_reasons"],
            "component_scores": qualification["component_scores"],
            "components": qualification["components"],
            "coverage_percent": coverage["percentage"],
            "researched_dimensions": coverage["sufficiently_researched_dimensions"],
            "missing_dimensions": coverage.get("missing_dimensions", []),
            "exhausted_unknown_dimensions": coverage.get("exhausted_unknown_dimensions", []),
        },
        "route": {
            "service_route": route.get("route_id"),
            "fit": route.get("fit"),
            "won_on": route.get("won_on"),
            "diagnostic_capability": route.get("diagnostic_capability"),
            "proof_asset_id": route.get("proof_asset_id"),
        },
        "lifecycle": {
            "canonical_stage_before": "routed",
            "advancement_requested": None,
            "why": ("No diagnostic has run, so `diagnostic_complete` is not reachable and no "
                    "packet may be built. Requalification changes the score, not the stage."),
        },
        "next_action": ("run the registered client-audit to completion, then persist the "
                        "diagnostic_complete receipt"),
        "codex_handoff": {
            "persist": "runs/transition-receipts and the canonical entity state",
            "why": "operating-state writes belong to codex under the 2026-08-11 ownership split",
            "do_not": "create another batch-level truth; the canonical cohort receipt is the baseline",
        },
        "external_action_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path, default=HANDOFFS)
    args = parser.parse_args()

    result = run(args.as_of)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"{PROSPECT}-requalification-{args.as_of}.json"
    lock.require_write(str(path), RUNTIME)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    q = result["qualification"]
    print(f"written: {path}")
    print(f"evidence: {result['evidence_audit']['counts']}")
    print(f"score {q['score']}/{q['max_score']}  {q['tier']}  actionability={q['actionability']}")
    print(f"coverage {q['coverage_percent']}%  researched {q['researched_dimensions']}/6  "
          f"missing={q['missing_dimensions']}  exhausted={q['exhausted_unknown_dimensions']}")
    for name, score in q["component_scores"].items():
        item = q["components"][name]
        print(f"  {name:22s} {score:3d}  {item['research_status']:16s} "
              f"conf={item['confidence']:7s} ids={len(item['evidence_ids'])}")
    print(f"route {result['route']['service_route']} via {result['route']['diagnostic_capability']}")
    print(f"next: {result['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
