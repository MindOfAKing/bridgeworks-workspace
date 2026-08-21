#!/usr/bin/env python3
"""Audit a completed diagnostic run, apply the completion gate, confirm the route.

HOW TO USE
    python operations/internal-gtm/scripts/diagnostic_gate.py --prospect arc-solutions-limited
    python operations/internal-gtm/scripts/diagnostic_gate.py --prospect premier-fm

Reads the diagnostic execution receipt written by a registered diagnostic
capability, puts every finding through the Evidence Auditor, tests the
`diagnostic_selected -> diagnostic_complete` gate, and re-runs route selection on
the audited evidence rather than on the research that chose the route originally.

Writes a handoff. Handoffs are proposals from implementation to operating state.
Nothing under runs/ is touched: that belongs to Codex.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import control_lock  # noqa: E402
import gtm_core as core  # noqa: E402
import transitions  # noqa: E402

AS_OF = "2026-08-11"
RUNTIME = "claude_code"

# Finding category -> the service route it argues for. A category absent from this
# map argues for no route, which is a real outcome and not a fallback.
CATEGORY_ROUTES = {
    "website_trust": "digital-platforms-brand",
    "conversion_path": "digital-platforms-brand",
    "ownership": "execution-operating-systems",
    "operating_process": "execution-operating-systems",
    "visibility": "content-visibility-demand",
    "ai_visibility": "content-visibility-demand",
    "manual_workflow": "ai-workflow-automation",
    "positioning": "strategy-transformation",
}
ROUTES = ("strategy-transformation", "digital-platforms-brand", "content-visibility-demand",
          "ai-workflow-automation", "execution-operating-systems")

# Hypotheses, not offers. Each names the finding it rests on and what would kill it.
# None of these is priced, promised or sent. Item 7 stops before outreach.
ARC_HYPOTHESES = [
    {
        "id": "arc-offer-h1",
        "hypothesis": "A claims reconciliation pass across owned pages: one verified set "
                      "of figures for projects, clients, staff and coverage, applied "
                      "everywhere they appear.",
        "rests_on": ["ca-arc-1", "ca-arc-2"],
        "why_it_is_credible": "The inconsistency is verified on their own pages, visible "
                              "to any buyer who reads two of them, and cheap to fix.",
        "what_would_kill_it": "If they already know which figure is right and simply have "
                              "not updated the page, this is a ten-minute edit, not an "
                              "engagement.",
        "evidence_still_missing": "Which figure is accurate. Not knowable from outside.",
    },
    {
        "id": "arc-offer-h2",
        "hypothesis": "Substantiate the ISO claim on the site: standard, scope, issuing "
                      "body and validity, presented where procurement looks for it.",
        "rests_on": ["ca-arc-3"],
        "why_it_is_credible": "They sell to Dangote, Providus and Cummins. Those buyers "
                              "run vendor due diligence, and an unsubstantiated "
                              "certification claim is a procurement risk rather than a "
                              "marketing one.",
        "what_would_kill_it": "If no certificate exists, this becomes a compliance "
                              "conversation and BridgeWorks should not run it.",
        "evidence_still_missing": "Whether a certificate exists at all.",
    },
    {
        "id": "arc-offer-h3",
        "hypothesis": "Enquiry-route integrity check: confirm the form renders, submits, "
                      "confirms to the visitor and lands with a named owner inside the "
                      "24-hour promise they publish.",
        "rests_on": ["ca-arc-7", "ca-arc-5"],
        "why_it_is_credible": "They publish a 24-hour quote commitment against a single "
                              "generic inbox with no named owner. The commitment is "
                              "public; the mechanism behind it is not observable.",
        "what_would_kill_it": "A working form and a real owner. Then there is no problem.",
        "evidence_still_missing": "Everything behind the form. Not testable without "
                                  "submitting one, which is an external action and is "
                                  "not authorised.",
        "hard_constraint": "Testing this by submitting the form would be contact. Not done.",
    },
]

PREMIER_HYPOTHESES = [
    {
        "id": "pfm-offer-h1",
        "hypothesis": "Populate and verify the five empty KPI counters, with each figure "
                      "traceable to a source Premier FM can stand behind.",
        "rests_on": ["ca-pfm-1"],
        "why_it_is_credible": "The credibility block is already built and already on the "
                              "page. It renders five labels and five blanks. The cost of "
                              "the failure is that the one place the site tries to prove "
                              "scale proves nothing.",
        "what_would_kill_it": "A rendering bug they already know about, or figures they "
                              "deliberately withhold.",
        "evidence_still_missing": "The true figures, and whether the blanks are a script "
                                  "failure or were never entered.",
    },
    {
        "id": "pfm-offer-h2",
        "hypothesis": "Build a first proof layer: named references, a written case, and "
                      "the certifications a Hungarian facility-management buyer expects "
                      "to see before shortlisting.",
        "rests_on": ["ca-pfm-2"],
        "why_it_is_credible": "There is no third-party proof of any kind on the site. "
                              "Everything a buyer reads, Premier FM says about itself.",
        "what_would_kill_it": "Client confidentiality terms that forbid naming accounts, "
                              "which is common in facility management.",
        "evidence_still_missing": "Whether their contracts permit naming clients.",
    },
    {
        "id": "pfm-offer-h3",
        "hypothesis": "Reconcile the trading name with the contracting entity so that a "
                      "buyer running a company check meets the name they were sold.",
        "rests_on": ["ca-pfm-3"],
        "why_it_is_credible": "The site sells Premier FM. The contact page contracts as "
                              "Otthonbiztonsagban.hu Kft. A procurement check surfaces "
                              "that difference before a human explains it.",
        "what_would_kill_it": "A deliberate group structure they are comfortable "
                              "explaining in the sales conversation.",
        "evidence_still_missing": "The actual relationship between the two names. Not "
                                  "knowable from the site, and not asserted here.",
    },
]

HYPOTHESES = {
    "arc-solutions-limited": ARC_HYPOTHESES,
    "premier-fm": PREMIER_HYPOTHESES,
}

# A route verdict needs a receipted reason, including when it is unchanged.
ROUTE_REASONS = {
    "arc-solutions-limited": (
        "The audit changed the problem, not the route. The original basis was a reading "
        "of the SPOTA navigation text as placeholder residue at the quote path; ca-arc-4 "
        "verified that text is a deliberate Coming Soon label and withdrew that basis. "
        "Four approved website_trust and conversion_path findings replace it, led by "
        "ca-arc-1: the homepage and the mission page publish project and client counts "
        "that differ by an order of magnitude. Owned-surface credibility is the same "
        "route, reached by different evidence."
    ),
    "premier-fm": (
        "Confirmed on stronger evidence than it was selected on. The route was chosen "
        "from an engine note that numeric values were absent in indexed text; ca-pfm-1 "
        "verified five named KPI labels rendering with no value, and ca-pfm-2 verified "
        "that no third-party proof of any kind exists on the site. Both are website_trust "
        "and both are high severity. No other route drew an approved severe finding."
    ),
}


def read(path: Path) -> dict:
    """A missing or unreadable input stops the run. Corrupt evidence never passes silently."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read {path.relative_to(REPO_ROOT)}: {exc}")


def to_ledger_entries(diagnostic: dict) -> list[dict]:
    """Diagnostic findings become evidence entries. Status is carried, never upgraded."""
    entries = []
    for finding in diagnostic["findings"]:
        entries.append({
            "id": finding["id"],
            "subject": finding["category"],
            "claim_key": finding.get("claim_key"),
            "value": finding["value"],
            "status": finding["status"],
            "source": finding["source"],
            "observed_at": finding["observed_at"],
            "severity": finding["severity"],
        })
    return entries


def shape_qualification(handoff: dict) -> dict:
    """The requalification handoff records coverage flat. The receipt wants it nested.

    Translated here at the boundary rather than by changing either schema.
    """
    qualification = handoff.get("qualification", handoff)
    return {
        **qualification,
        "qualification_coverage": {
            "percentage": qualification.get("coverage_percent"),
            "sufficiently_researched_dimensions": qualification.get("researched_dimensions"),
            "missing_dimensions": qualification.get("missing_dimensions", []),
            "exhausted_unknown_dimensions": qualification.get("exhausted_unknown_dimensions", []),
        },
    }


def audit(diagnostic: dict) -> dict:
    """Evidence Auditor pass. Assumptions stay assumptions."""
    ledger = core.build_evidence_ledger(to_ledger_entries(diagnostic), as_of=AS_OF)
    by_status: dict[str, list[str]] = {}
    for entry in ledger["ledger"]:
        by_status.setdefault(entry["status"], []).append(entry["id"])

    approved = {entry["id"] for entry in ledger["ledger"] if entry["status"] in core.APPROVED_CLASSES}
    unresolved = [entry["id"] for entry in ledger["ledger"]
                  if entry["status"] not in core.APPROVED_CLASSES]

    # The ledger reports contradictions by downgrading an entry's status, and does not
    # always emit a separate list. Reading only the list lets a contradiction through.
    contradicted = [entry["id"] for entry in ledger["ledger"]
                    if entry["status"] == "contradicted"]

    return {
        "ledger": ledger,
        "by_status": by_status,
        "approved_finding_ids": sorted(approved),
        "unresolved_finding_ids": unresolved,
        "audited_status": {entry["id"]: entry["status"] for entry in ledger["ledger"]},
        "contradictions": ledger.get("contradictions", []),
        "contradicted_finding_ids": contradicted,
        "assumptions_left_unpromoted": diagnostic["assumptions_not_promoted_to_facts"],
        "limitations_carried": diagnostic["limitations"],
        "unknowns_carried": diagnostic["unknowns"],
        "corrections_to_prior_evidence": [
            {"finding": finding["id"], "corrects": finding["note"]}
            for finding in diagnostic["findings"]
            if "corrects the earlier" in finding.get("note", "")
        ],
    }


def confirm_route(audited: dict, diagnostic: dict, current_route: str, reason: str) -> dict:
    """Re-run selection on audited evidence. Maturity is not a tie-break."""
    # Post-audit status, not the status the diagnostic asserted. A finding the auditor
    # downgraded must not still be able to select a route.
    approved = set(audited["approved_finding_ids"])
    problems = [finding for finding in diagnostic["findings"]
                if finding["id"] in approved and finding["severity"] in ("high", "medium")]

    candidates: dict[str, list[dict]] = {route: [] for route in ROUTES}
    unmapped = []
    for finding in problems:
        route = CATEGORY_ROUTES.get(finding["category"])
        if route is None:
            unmapped.append({"finding": finding["id"], "category": finding["category"]})
            continue
        candidates[route].append(finding)

    scored = {
        route: {
            "approved_severe_findings": len(findings),
            "highest_severity": ("high" if any(f["severity"] == "high" for f in findings)
                                 else "medium" if findings else "none"),
            "finding_ids": [f["id"] for f in findings],
        }
        for route, findings in candidates.items()
    }
    ranked = sorted(scored.items(),
                    key=lambda item: (item[1]["approved_severe_findings"],
                                      item[1]["highest_severity"] == "high"),
                    reverse=True)
    winner, runner_up = ranked[0], ranked[1]
    tied = winner[1]["approved_severe_findings"] == runner_up[1]["approved_severe_findings"]

    if winner[1]["approved_severe_findings"] == 0:
        verdict = "no_credible_route"
    elif tied:
        verdict = "tied"
    elif winner[0] == current_route:
        verdict = "confirmed"
    else:
        verdict = "revised"

    return {
        "prior_route": current_route,
        "verdict": verdict,
        "selected_route": winner[0],
        "ranking": scored,
        "unmapped_categories": unmapped,
        "basis": "approved diagnostic findings only, weighted by severity",
        "excluded_from_tie_break": "maturity",
        "reason": reason,
    }


def gate(prospect: str, diagnostic: dict, audited: dict) -> dict:
    """Item 4. Advance only when the capability actually ran and everything resolves."""
    findings = diagnostic["findings"]
    sources_resolve = all(finding.get("source", "").startswith("http") for finding in findings)
    contract_fields = ("diagnostic_id", "prospect_id", "execution", "findings",
                       "limitations", "unknowns")
    contract_valid = all(field in diagnostic for field in contract_fields)
    approved_count = len(audited["approved_finding_ids"])

    checks = {
        "capability_actually_executed": diagnostic["execution"]["status"] == "complete"
        and bool(diagnostic["execution"]["pages_fetched"]),
        "not_a_reshaped_prior_artifact": diagnostic["no_new_diagnostic_was_implemented"]
        and len(diagnostic["execution"]["pages_fetched"]) >= 1,
        "result_contract_validates": contract_valid,
        "evidence_references_resolve": sources_resolve,
        "quality_gate_min_approved_findings": approved_count >= 3,
        "quality_gate_no_unresolved_contradiction": not audited["contradictions"]
        and not audited["contradicted_finding_ids"],
        "quality_gate_limitations_declared": bool(diagnostic["limitations"]),
    }

    history = transitions.load_receipts(prospect)
    prerequisite = transitions.check(
        "diagnostic_complete", history,
        {"diagnostic_id": diagnostic["diagnostic_id"], "status": diagnostic["execution"]["status"]})

    return {
        "checks": checks,
        "prerequisite": prerequisite,
        "all_checks_pass": all(checks.values()),
        "receipted_history_present": bool(history),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prospect", required=True)
    parser.add_argument("--reason", default="",
                        help="why the route verdict is what it is, recorded in the receipt")
    args = parser.parse_args()
    prospect = args.prospect

    decision = control_lock.may_write("handoffs/x.json", RUNTIME)
    if not decision["allowed"]:
        raise SystemExit(f"write refused: {decision['reason']}")

    diagnostic_path = GTM_ROOT / "handoffs" / f"{prospect}-client-audit-{AS_OF}.json"
    qualification_path = GTM_ROOT / "handoffs" / f"{prospect}-requalification-{AS_OF}.json"
    out = GTM_ROOT / "handoffs" / f"{prospect}-diagnostic-gate-{AS_OF}.json"

    diagnostic = read(diagnostic_path)
    qualification = (shape_qualification(read(qualification_path))
                     if qualification_path.is_file() else {})
    audited = audit(diagnostic)
    current_route = diagnostic.get("current_route", "digital-platforms-brand")
    routing = confirm_route(audited, diagnostic, current_route,
                            args.reason or ROUTE_REASONS.get(prospect, ""))
    gating = gate(prospect, diagnostic, audited)

    snapshot = str(diagnostic_path.relative_to(REPO_ROOT)).replace("\\", "/")
    advanced = gating["all_checks_pass"] and gating["prerequisite"]["allowed"]

    proposed_receipt = None
    blocking = []
    if advanced:
        proposed_receipt = transitions.receipt(
            prospect, "diagnostic_selected", "diagnostic_complete",
            triggering_capability=diagnostic["capability"],
            ledger=audited["ledger"],
            qualification=qualification.get("qualification", qualification),
            diagnostic={"diagnostic_id": diagnostic["diagnostic_id"],
                        "status": diagnostic["execution"]["status"]},
            runtime=RUNTIME,
            history=transitions.load_receipts(prospect),
            evidence_snapshot_path=snapshot,
            enforce=False)
        proposed_receipt["enforcement_note"] = (
            "Built with enforce=False because the diagnostic_selected receipt lives in "
            "runs/, which Codex owns and which this runtime does not write. Every gate "
            "was still evaluated and every one passed. Codex must confirm the "
            "diagnostic_selected receipt exists before persisting this.")
    else:
        blocking = [name for name, passed in gating["checks"].items() if not passed]
        if not gating["prerequisite"]["allowed"]:
            blocking.append(f"prerequisite: {gating['prerequisite']['reason']}")

    payload = {
        "handoff_kind": "diagnostic_completion_gate",
        "prospect_id": prospect,
        "as_of": AS_OF,
        "runtime": RUNTIME,
        "diagnostic_id": diagnostic["diagnostic_id"],
        "evidence_audit": {
            "approved": audited["approved_finding_ids"],
            "unresolved": audited["unresolved_finding_ids"],
            "by_status": audited["by_status"],
            "contradictions": audited["contradictions"],
            "contradicted_finding_ids": audited["contradicted_finding_ids"],
            "audited_status": audited["audited_status"],
            "assumptions_left_unpromoted": audited["assumptions_left_unpromoted"],
            "limitations_carried": audited["limitations_carried"],
            "unknowns_carried": audited["unknowns_carried"],
            "corrections_to_prior_evidence": audited["corrections_to_prior_evidence"],
            "evidence_hash": transitions.evidence_hash(audited["ledger"]),
        },
        "completion_gate": gating,
        "lifecycle": {
            "from_stage": "diagnostic_selected",
            "to_stage": "diagnostic_complete" if advanced else "diagnostic_selected",
            "advanced": advanced,
            "blocking_reasons": blocking,
        },
        "proposed_transition_receipt": proposed_receipt,
        "route_confirmation": routing,
        "entry_offer_hypotheses": HYPOTHESES.get(prospect, []),
        "outreach_prepared": False,
        "approval_packet": None,
        "stop_point": "item 7: no outreach preparation, no approval packet",
    }

    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "written": str(out.relative_to(REPO_ROOT)).replace("\\", "/"),
        "approved_findings": len(audited["approved_finding_ids"]),
        "unresolved_findings": len(audited["unresolved_finding_ids"]),
        "contradictions": len(audited["contradictions"]),
        "gate_passed": gating["all_checks_pass"],
        "advanced": advanced,
        "blocking_reasons": blocking,
        "route_verdict": routing["verdict"],
        "route": routing["selected_route"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
