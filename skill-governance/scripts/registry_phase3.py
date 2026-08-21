#!/usr/bin/env python3
"""Plan and apply the Phase 3 live-estate capability-registry regeneration.

`plan` scans the live Claude/Codex estate into a candidate, preserves governance
metadata from the current registry, and writes a classified diff. It never changes
the canonical registry. `apply` refuses to write while the plan has blockers.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import registry_tool as rt  # noqa: E402


REPORT_DIR = ROOT / "skill-governance" / "reports" / "phase-3"
CANDIDATE = REPORT_DIR / "capability-registry-candidate-2026-08-11.yaml"
CANDIDATE_SUMMARY = REPORT_DIR / "CAPABILITY-REGISTRY-CANDIDATE-2026-08-11.md"
DIFF_JSON = REPORT_DIR / "capability-registry-diff-2026-08-11.json"
DIFF_MD = REPORT_DIR / "capability-registry-diff-2026-08-11.md"
REVIEW_RECEIPT = REPORT_DIR / "bridgeworks-capability-review-2026-08-11.json"
CANONICAL = ROOT / "skill-governance" / "capability-registry.yaml"
CANONICAL_SUMMARY = ROOT / "skill-governance" / "CAPABILITY-REGISTRY.md"

REVIEWED_INTERNAL = {
    "bridgeworks-lead-qualifier": "Native deterministic tests passed: 6 status cases and 1 validation case.",
    "bridgeworks-prospect-router": "Native deterministic tests passed: 1 valid and 7 invalid route cases.",
    "bridgeworks-geo-prospect-scan": "Exact staged/native mirror verified; bounded read-only diagnostic contract reviewed in Phase 2.",
    "bridgeworks-revenue-system-scan": "Exact staged/native mirror verified; bounded read-only diagnostic contract reviewed in Phase 2.",
    "bridgeworks-ai-workflow-scan": "Exact staged/native mirror verified; bounded read-only diagnostic contract reviewed in Phase 2.",
}

PRESERVE_FIELDS = {
    "status", "security", "last_reviewed", "source", "known_weaknesses",
    "tests", "notes",
}
GENERIC = (None, "unknown", ["unknown"], {"type": "internal", "repository": "unknown", "version": "unknown"})


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_live() -> dict:
    old_registry, old_summary = rt.REGISTRY, rt.SUMMARY
    try:
        rt.REGISTRY, rt.SUMMARY = CANDIDATE, CANDIDATE_SUMMARY
        return rt.generate()
    finally:
        rt.REGISTRY, rt.SUMMARY = old_registry, old_summary


def is_generic(value: object) -> bool:
    return value in GENERIC


def plan() -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    current = load(CANONICAL)
    scanned = scan_live()
    old = {item["id"]: item for item in current["skills"]}
    live = {item["id"]: item for item in scanned["skills"]}
    changes: list[dict] = []
    blockers: list[dict] = []

    for skill_id, candidate in live.items():
        previous = old.get(skill_id)
        if previous is None:
            candidate["status"] = "unknown"
            candidate["last_reviewed"] = None
            changes.append({
                "id": skill_id,
                "classification": "new capability",
                "detail": "Present in the live estate but absent from the July 25 registry; not auto-approved.",
            })
        else:
            metadata_preserved = []
            for field in PRESERVE_FIELDS:
                if field in previous:
                    scanned_value = candidate.get(field)
                    if field in {"status", "security", "last_reviewed"} or is_generic(scanned_value):
                        candidate[field] = copy.deepcopy(previous[field])
                        metadata_preserved.append(field)
            for field, value in previous.items():
                if field not in candidate:
                    candidate[field] = copy.deepcopy(value)
                    metadata_preserved.append(field)

            old_inst = {(x.get("runtime"), x.get("path")) for x in previous.get("installations", [])}
            new_inst = {(x.get("runtime"), x.get("path")) for x in candidate.get("installations", [])}
            if old_inst != new_inst:
                classification = "duplicate installation" if len(new_inst) > 1 else "runtime conflict"
                entry = {
                    "id": skill_id,
                    "classification": classification,
                    "detail": "Live runtime installations differ from the July 25 registry.",
                    "before": sorted(old_inst),
                    "after": sorted(new_inst),
                }
                changes.append(entry)
                if not new_inst:
                    blockers.append(entry)

            changed_fields = sorted(
                key for key in candidate
                if key not in PRESERVE_FIELDS and candidate.get(key) != previous.get(key)
            )
            if changed_fields:
                changes.append({
                    "id": skill_id,
                    "classification": "updated capability",
                    "detail": "Live instructions changed generated descriptive metadata.",
                    "fields": changed_fields,
                })
            if metadata_preserved:
                changes.append({
                    "id": skill_id,
                    "classification": "metadata gap",
                    "detail": "Existing governance metadata was preserved instead of regenerated.",
                    "fields": sorted(set(metadata_preserved)),
                })

    for skill_id, previous in old.items():
        if skill_id in live:
            continue
        retained = copy.deepcopy(previous)
        retained["status"] = "unknown"
        retained["runtime_state"] = "not_found_in_live_scan"
        retained["notes"] = (str(retained.get("notes") or "") +
                             " Not found in the 2026-08-11 live scan; retained pending governance decision.").strip()
        live[skill_id] = retained
        entry = {
            "id": skill_id,
            "classification": "governance concern",
            "detail": "Registry entry was not found in the live scan. Retained; no automatic removal or supersession.",
            "blocker": True,
        }
        changes.append(entry)
        blockers.append(entry)

    candidate_data = {
        **{key: value for key, value in scanned.items() if key != "skills"},
        "generated_at": date.today().isoformat(),
        "governance_policy": "New skills are unknown until reviewed. Existing governance metadata is preserved.",
        "skills": sorted(live.values(), key=lambda item: item["id"]),
    }
    CANDIDATE.write_text(json.dumps(candidate_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Write the candidate summary explicitly without touching the canonical summary.
    old_summary = rt.SUMMARY
    try:
        rt.SUMMARY = CANDIDATE_SUMMARY
        rt.write_summary(candidate_data)
    finally:
        rt.SUMMARY = old_summary

    counts = Counter(item["classification"] for item in changes)
    runtime_counts = Counter(
        inst["runtime"] for skill in candidate_data["skills"]
        for inst in skill.get("installations", [])
        if skill.get("runtime_state") != "not_found_in_live_scan"
    )
    report = {
        "generated_at": date.today().isoformat(),
        "current_unique_capabilities": len(old),
        "candidate_unique_capabilities": len(candidate_data["skills"]),
        "live_scanned_unique_capabilities": len(scanned["skills"]),
        "live_installations_by_runtime": dict(sorted(runtime_counts.items())),
        "classification_counts": dict(sorted(counts.items())),
        "changes": changes,
        "blockers": blockers,
        "safe_to_apply": not blockers,
        "candidate": str(CANDIDATE),
    }
    DIFF_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Capability registry Phase 3 pre-write diff", "",
        f"Generated: {report['generated_at']}", "",
        f"Current unique capabilities: {len(old)}", 
        f"Live scanned unique capabilities: {len(scanned['skills'])}",
        f"Candidate unique capabilities: {len(candidate_data['skills'])}",
        f"Safe to apply: {'yes' if report['safe_to_apply'] else 'no'}", "",
        "## Classification counts", "",
        "| Classification | Count |", "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(counts.items()))
    lines += ["", "## Classified differences", "", "| ID | Classification | Detail |", "|---|---|---|"]
    for item in changes:
        lines.append(f"| `{item['id']}` | {item['classification']} | {item['detail']} |")
    if blockers:
        lines += ["", "## Blocking governance concerns", ""]
        lines.extend(f"- `{item['id']}`: {item['detail']}" for item in blockers)
    DIFF_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def apply_candidate() -> dict:
    report = load(DIFF_JSON)
    if report.get("blockers"):
        raise RuntimeError("candidate has unresolved blockers; canonical registry was not changed")
    candidate = load(CANDIDATE)
    errors = rt.validate(CANDIDATE)
    if errors:
        raise RuntimeError("candidate validation failed: " + "; ".join(errors))
    CANONICAL.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old_summary = rt.SUMMARY
    try:
        rt.SUMMARY = CANONICAL_SUMMARY
        rt.write_summary(candidate)
    finally:
        rt.SUMMARY = old_summary
    return {"applied": True, "skills": len(candidate["skills"]), "canonical": str(CANONICAL)}


def review_internal() -> dict:
    data = load(CANONICAL)
    index = {item["id"]: item for item in data["skills"]}
    missing = sorted(set(REVIEWED_INTERNAL) - set(index))
    if missing:
        raise RuntimeError("review targets missing from canonical registry: " + ", ".join(missing))
    reviewed = []
    for skill_id, evidence in REVIEWED_INTERNAL.items():
        skill = index[skill_id]
        if skill.get("source", {}).get("type") != "internal":
            raise RuntimeError(f"{skill_id} is not classified as internal")
        skill["status"] = "active"
        skill["last_reviewed"] = date.today().isoformat()
        skill["governance_review"] = {
            "decision": "active",
            "reviewed_at": date.today().isoformat(),
            "scope": "internal BridgeWorks use; no external-action authority",
            "evidence": evidence,
        }
        reviewed.append(skill_id)
    CANONICAL.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old_summary = rt.SUMMARY
    try:
        rt.SUMMARY = CANONICAL_SUMMARY
        rt.write_summary(data)
    finally:
        rt.SUMMARY = old_summary
    receipt = {
        "reviewed_at": date.today().isoformat(),
        "activated_internal_capabilities": sorted(reviewed),
        "external_or_unreviewed_new_capabilities_activated": [],
        "authority": "Phase 3 explicit capability-registry authorization",
    }
    REVIEW_RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("plan", "apply", "review-internal"))
    args = parser.parse_args()
    try:
        if args.command == "plan":
            result = plan()
        elif args.command == "apply":
            result = apply_candidate()
        else:
            result = review_internal()
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
