#!/usr/bin/env python3
"""Canonical lifecycle transitions: prerequisites, receipts, and artifact supersession.

HOW TO USE
    from transitions import PREREQUISITES, check, receipt, reconstruct, classify_artifact

    python operations/internal-gtm/scripts/transitions.py verify --prospect premier-fm

A lifecycle stage is a claim about work that was done. This module makes the claim
verifiable by a later runtime without reading anyone's prose report.

Every advancement writes a receipt carrying the twelve fields below. Every
advancement checks its prerequisite first. An artifact produced before its
prerequisite was met is not canonical: it is `superseded_pre_gate_artifact`, it is
non-executable, and it is kept as history rather than deleted.

    diagnostic_selected  -> requires a successful diagnostic completion
                            before diagnostic_complete
    diagnostic_complete  -> required before offer_selected
    offer_selected       -> required before outreach_prepared
    outreach_prepared    -> required before awaiting_approval

No packet becomes canonical by skipping these.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
RECEIPTS = GTM_ROOT / "runs" / "transition-receipts"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import gtm_core as core  # noqa: E402

RECEIPT_FIELDS = (
    "prospect_id", "from_stage", "to_stage", "triggering_capability",
    "required_gate_results", "evidence_snapshot", "evidence_hash", "qualification_version",
    "qualification_coverage", "diagnostic_id", "diagnostic_status",
    "approval_id", "runtime", "timestamp",
)

# Stage -> the stage that must already be receipted, and the gate that proves it.
PREREQUISITES = {
    "diagnostic_complete": {
        "requires_stage": "diagnostic_selected",
        "gate": "diagnostic_completed_successfully",
        "detail": "a diagnostic run must have completed, with an id and a terminal status",
    },
    "offer_selected": {
        "requires_stage": "diagnostic_complete",
        "gate": "diagnostic_complete_receipted",
        "detail": "an offer cannot be chosen before the diagnostic that justifies it finished",
    },
    "outreach_prepared": {
        "requires_stage": "offer_selected",
        "gate": "offer_selected_receipted",
        "detail": "outreach cannot be prepared before an offer exists",
    },
    "awaiting_approval": {
        "requires_stage": "outreach_prepared",
        "gate": "outreach_prepared_receipted",
        "detail": "an approval cannot be requested before the outreach it approves exists",
    },
}

TERMINAL_DIAGNOSTIC_STATUSES = ("complete", "partial_accepted")
SUPERSEDED = "superseded_pre_gate_artifact"
CANONICAL = "canonical"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def evidence_hash(ledger: dict) -> str:
    """A hash of the approved evidence, so a later runtime can verify the snapshot."""
    payload = [
        {"id": entry["id"], "status": entry["status"], "value": entry.get("value"),
         "source": entry.get("source"), "observed_at": entry.get("observed_at")}
        for entry in sorted(ledger.get("ledger", []), key=lambda e: str(e["id"]))
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def snapshot_hash(path_text: str) -> str:
    """Hash the exact snapshot file named by the receipt."""
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.is_file():
        raise FileNotFoundError(f"evidence snapshot does not exist: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(to_stage: str, history: list[dict], diagnostic: dict | None = None) -> dict:
    """Is this advancement permitted by the receipted history? No prose involved."""
    rule = PREREQUISITES.get(to_stage)
    if rule is None:
        return {"to_stage": to_stage, "allowed": True, "gate_results": {},
                "reason": "no prerequisite defined for this stage"}

    receipted = {entry["to_stage"] for entry in history}
    gate_results = {rule["gate"]: rule["requires_stage"] in receipted}

    if to_stage == "diagnostic_complete":
        status = (diagnostic or {}).get("status")
        has_id = bool((diagnostic or {}).get("diagnostic_id"))
        gate_results["diagnostic_has_id"] = has_id
        gate_results["diagnostic_status_terminal"] = status in TERMINAL_DIAGNOSTIC_STATUSES
        gate_results[rule["gate"]] = (
            rule["requires_stage"] in receipted and has_id
            and status in TERMINAL_DIAGNOSTIC_STATUSES)

    allowed = all(gate_results.values())
    return {
        "to_stage": to_stage,
        "requires_stage": rule["requires_stage"],
        "allowed": allowed,
        "gate_results": gate_results,
        "reason": rule["detail"] if not allowed else "prerequisite satisfied",
    }


class PrerequisiteError(RuntimeError):
    """Raised when an advancement would skip a required transition."""


def receipt(prospect_id: str, from_stage: str, to_stage: str, *,
            triggering_capability: str, ledger: dict, qualification: dict,
            diagnostic: dict | None = None, approval_id: str | None = None,
            runtime: str = "claude_code", history: list[dict] | None = None,
            evidence_snapshot_path: str, enforce: bool = True) -> dict:
    """Build a verifiable transition receipt. Refuses to skip a prerequisite."""
    history = history or []
    gate = check(to_stage, history, diagnostic)
    if enforce and not gate["allowed"]:
        raise PrerequisiteError(
            f"{prospect_id}: {from_stage} -> {to_stage} blocked. {gate['reason']}. "
            f"gates: {gate['gate_results']}")
    core.advance(from_stage, to_stage)

    coverage = qualification.get("qualification_coverage") or {}
    return {
        "prospect_id": prospect_id,
        "from_stage": from_stage,
        "to_stage": to_stage,
        "triggering_capability": triggering_capability,
        "required_gate_results": gate["gate_results"],
        "evidence_snapshot": {
            "path": evidence_snapshot_path,
            "sha256": snapshot_hash(evidence_snapshot_path),
        },
        "evidence_hash": evidence_hash(ledger),
        "qualification_version": qualification.get("model")
        or qualification.get("qualification_version"),
        "qualification_coverage": {
            "percentage": coverage.get("percentage"),
            "sufficiently_researched_dimensions": coverage.get("sufficiently_researched_dimensions"),
            "missing_dimensions": coverage.get("missing_dimensions", []),
            "exhausted_unknown_dimensions": coverage.get("exhausted_unknown_dimensions", []),
        },
        "diagnostic_id": (diagnostic or {}).get("diagnostic_id"),
        "diagnostic_status": (diagnostic or {}).get("status", "not_run"),
        "approval_id": approval_id,
        "runtime": runtime,
        "timestamp": _now(),
        "receipt_version": 1,
        "verifiable_without_prose": True,
    }


def reconstruct(prospect_id: str, artifacts: list[dict]) -> dict:
    """Work out the canonical stage from receipts and artifacts, not from a report.

    An artifact that claims a stage it has no receipt for does not move the
    canonical stage. It is recorded as superseded.
    """
    receipts = [a for a in artifacts if a.get("kind") == "transition_receipt"]
    receipts.sort(key=lambda r: (str(r.get("timestamp")), core.LIFECYCLE.index(r["to_stage"])))
    receipted_stages = [r["to_stage"] for r in receipts]

    canonical_stage = "account_discovered"
    verified_chain, broken = [], []
    for entry in receipts:
        if entry.get("from_stage") != canonical_stage:
            broken.append({
                "to_stage": entry.get("to_stage"),
                "reason": (f"receipt starts at {entry.get('from_stage')} but the verified "
                           f"chain is at {canonical_stage}"),
                "gate_results": {"from_stage_matches_verified_chain": False},
            })
            continue
        gate = check(entry["to_stage"], verified_chain,
                     {"diagnostic_id": entry.get("diagnostic_id"),
                      "status": entry.get("diagnostic_status")})
        if gate["allowed"]:
            verified_chain.append(entry)
            canonical_stage = entry["to_stage"]
        else:
            broken.append({"to_stage": entry["to_stage"], "reason": gate["reason"],
                           "gate_results": gate["gate_results"]})

    claimed = [a for a in artifacts if a.get("kind") != "transition_receipt"]
    classified = [classify_artifact(a, receipted_stages, canonical_stage) for a in claimed]

    return {
        "prospect_id": prospect_id,
        "canonical_lifecycle_stage": canonical_stage,
        "verified_transition_chain": [
            {"from": r["from_stage"], "to": r["to_stage"],
             "capability": r.get("triggering_capability"),
             "diagnostic_status": r.get("diagnostic_status"),
             "runtime": r.get("runtime"), "timestamp": r.get("timestamp")}
            for r in verified_chain
        ],
        "broken_transitions": broken,
        "artifacts": classified,
        "canonical_approval_packet_id": next(
            (a["artifact_id"] for a in classified
             if a["classification"] == CANONICAL and a["type"] == "approval_packet"), None),
        "superseded_artifacts": [a["artifact_id"] for a in classified
                                 if a["classification"] == SUPERSEDED],
        "method": ("reconstructed from receipts and artifacts. No runtime was treated as "
                   "authority for producing a later report."),
    }


def classify_artifact(artifact: dict, receipted_stages: list[str], canonical_stage: str) -> dict:
    """Canonical or superseded. Produced before its prerequisite means superseded."""
    claimed_stage = artifact.get("lifecycle_stage")
    artifact_id = artifact.get("artifact_id") or artifact.get("approval_payload_digest") or "unknown"
    kind = artifact.get("type") or ("approval_packet" if artifact.get("approval_state") else "artifact")

    if claimed_stage is None:
        return {"artifact_id": artifact_id, "type": kind, "classification": CANONICAL,
                "reason": "artifact claims no lifecycle stage"}

    rule = PREREQUISITES.get(claimed_stage)
    if rule and rule["requires_stage"] not in receipted_stages:
        return {
            "artifact_id": artifact_id, "type": kind, "classification": SUPERSEDED,
            "claimed_stage": claimed_stage,
            "reason": (f"claims {claimed_stage} with no receipt for the required "
                       f"{rule['requires_stage']}"),
            "executable": False,
        }
    if core.LIFECYCLE.index(claimed_stage) > core.LIFECYCLE.index(canonical_stage):
        return {
            "artifact_id": artifact_id, "type": kind, "classification": SUPERSEDED,
            "claimed_stage": claimed_stage,
            "reason": f"claims {claimed_stage} beyond the canonical stage {canonical_stage}",
            "executable": False,
        }
    return {"artifact_id": artifact_id, "type": kind, "classification": CANONICAL,
            "claimed_stage": claimed_stage, "executable": kind != "approval_packet"}


def load_receipts(prospect_id: str) -> list[dict]:
    path = RECEIPTS / f"{prospect_id}.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_receipt(entry: dict) -> Path:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    path = RECEIPTS / f"{entry['prospect_id']}.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({**entry, "kind": "transition_receipt"}, ensure_ascii=False) + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("verify", "fields"))
    parser.add_argument("--prospect")
    args = parser.parse_args()

    if args.command == "fields":
        print("\n".join(RECEIPT_FIELDS))
        return 0
    receipts = load_receipts(args.prospect)
    result = reconstruct(args.prospect, receipts)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
