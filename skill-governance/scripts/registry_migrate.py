#!/usr/bin/env python3
"""Diff the live skill estate against the canonical registry before regenerating it.

HOW TO USE
    python skill-governance/scripts/registry_migrate.py diff
    python skill-governance/scripts/registry_migrate.py diff --json report.json
    python skill-governance/scripts/registry_migrate.py apply

`diff` writes nothing. It generates the registry into a temporary directory using
the exact live `registry_tool.generate` logic, compares it to the committed
registry, and classifies every difference into one of seven classes.

`apply` writes the regenerated registry, but merges governance fields forward
first: security scan results, non-active status, known provenance and hand-written
notes are carried over from the committed record. It refuses to run if the diff
reports a governance concern or a runtime conflict, because those need a decision,
not a merge.

Nothing here approves anything. A skill appearing in the estate is not a skill
approved for use.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skill-governance" / "scripts"
REGISTRY = ROOT / "skill-governance" / "capability-registry.yaml"

# Governance fields never regenerate correctly. They are decisions, not observations.
GOVERNANCE_FIELDS = ("security", "status", "source", "notes", "last_reviewed", "known_weaknesses")

CLASSES = (
    "new capability",
    "updated capability",
    "duplicate installation",
    "superseded implementation",
    "metadata gap",
    "runtime conflict",
    "governance concern",
)

# Capabilities BridgeWorks authored on 2026-08-01. These must appear.
AUGUST_FIRST = (
    "bridgeworks-lead-qualifier",
    "bridgeworks-prospect-router",
    "bridgeworks-geo-prospect-scan",
    "bridgeworks-revenue-system-scan",
    "bridgeworks-ai-workflow-scan",
)

# A skill whose files did not come from a BridgeWorks-controlled source root.
# Being installed is not approval. These are reported, never auto-approved.
INTERNAL_MARKERS = ("bridgeworks", "emmanuel", "mindofaking", "oliviks", "ceefm")


def load_registry_tool():
    spec = importlib.util.spec_from_file_location("registry_tool", SCRIPTS / "registry_tool.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def generate_into_temp(module) -> dict:
    """Run the live generator against a scratch path so nothing on disk changes."""
    original_registry, original_summary = module.REGISTRY, module.SUMMARY
    with tempfile.TemporaryDirectory() as folder:
        scratch = Path(folder)
        module.REGISTRY = scratch / "capability-registry.yaml"
        module.SUMMARY = scratch / "CAPABILITY-REGISTRY.md"
        try:
            return module.generate()
        finally:
            module.REGISTRY, module.SUMMARY = original_registry, original_summary


def _runtimes(record: dict) -> set[str]:
    return {i["runtime"] for i in record.get("installations", [])}


def _digest(path: Path) -> str | None:
    import hashlib

    skill_file = path / "SKILL.md"
    try:
        return hashlib.sha256(skill_file.read_bytes()).hexdigest()
    except OSError:
        return None


def _installations_diverge(record: dict) -> tuple[bool, dict[str, str | None]]:
    """Two runtimes holding different SKILL.md content is a real conflict.

    Two runtimes holding byte-identical content is a duplicate installation, which
    is a maintenance cost, not a correctness problem.
    """
    digests = {i["runtime"]: _digest(Path(i["path"])) for i in record.get("installations", [])}
    seen = {d for d in digests.values() if d}
    return len(seen) > 1, digests


def _provenance_lost(before: dict, after: dict) -> bool:
    """True only when regeneration would make provenance less specific, not more."""
    old_repo = (before.get("source") or {}).get("repository")
    new_repo = (after.get("source") or {}).get("repository")
    if old_repo in (None, "unknown"):
        return False
    return new_repo in (None, "unknown") or new_repo != old_repo


def _looks_external(record: dict) -> bool:
    haystack = f"{record['id']} {record.get('purpose','')}".lower()
    return not any(marker in haystack for marker in INTERNAL_MARKERS)


def classify(current: dict, fresh: dict) -> list[dict]:
    old = {s["id"]: s for s in current["skills"]}
    new = {s["id"]: s for s in fresh["skills"]}
    findings: list[dict] = []

    for skill_id in sorted(set(new) - set(old)):
        record = new[skill_id]
        findings.append({
            "id": skill_id,
            "class": "new capability",
            "runtimes": sorted(_runtimes(record)),
            "detail": f"present in the live estate, absent from the committed registry",
            "external_candidate": _looks_external(record),
            "auto_approve": False,
        })

    for skill_id in sorted(set(old) - set(new)):
        record = old[skill_id]
        findings.append({
            "id": skill_id,
            "class": "superseded implementation",
            "runtimes": sorted(_runtimes(record)),
            "detail": "in the committed registry, no longer installed in either live root",
            "auto_approve": False,
        })

    for skill_id in sorted(set(old) & set(new)):
        before, after = old[skill_id], new[skill_id]
        before_runtimes, after_runtimes = _runtimes(before), _runtimes(after)

        diverge, digests = _installations_diverge(after)
        if len(after.get("installations", [])) > 1 and not diverge:
            findings.append({
                "id": skill_id,
                "class": "duplicate installation",
                "runtimes": sorted(after_runtimes),
                "detail": "installed in both runtimes with byte-identical SKILL.md; one copy is redundant",
                "auto_approve": False,
            })
        if diverge:
            findings.append({
                "id": skill_id,
                "class": "runtime conflict",
                "runtimes": sorted(after_runtimes),
                "detail": "installed in both runtimes with different SKILL.md content; two versions are live",
                "digests": digests,
                "auto_approve": False,
            })
        if before_runtimes - after_runtimes:
            findings.append({
                "id": skill_id,
                "class": "superseded implementation",
                "runtimes": sorted(after_runtimes),
                "detail": f"no longer installed in {sorted(before_runtimes - after_runtimes)}",
                "auto_approve": False,
            })

        if _provenance_lost(before, after):
            findings.append({
                "id": skill_id,
                "class": "governance concern",
                "detail": f"provenance would become less specific: {before['source']!r} -> {after['source']!r}",
                "auto_approve": False,
            })
        for field in ("security", "status", "notes", "known_weaknesses"):
            if before.get(field) == after.get(field):
                continue
            default = (
                (field == "security" and before[field].get("result") == "unscanned")
                or (field == "status" and before[field] == "active")
                or (field == "notes" and str(before[field]).startswith("Fields marked unknown"))
                or (field == "known_weaknesses" and before[field] == ["unknown"])
            )
            if not default:
                findings.append({
                    "id": skill_id,
                    "class": "governance concern",
                    "detail": f"regeneration would overwrite curated `{field}`: {before[field]!r} -> {after[field]!r}",
                    "auto_approve": False,
                })

        changed = [f for f in ("purpose", "inputs", "outputs", "tools", "workflow_stages", "last_modified")
                   if before.get(f) != after.get(f)]
        if changed:
            findings.append({
                "id": skill_id,
                "class": "updated capability",
                "runtimes": sorted(after_runtimes),
                "detail": f"changed fields: {', '.join(changed)}",
                "auto_approve": False,
            })

        gaps = [f for f in ("inputs", "outputs", "tools") if after.get(f) == ["unknown"]]
        if gaps:
            findings.append({
                "id": skill_id,
                "class": "metadata gap",
                "detail": f"still unknown after regeneration: {', '.join(gaps)}",
                "auto_approve": False,
            })

    return findings


def merge_governance(current: dict, fresh: dict) -> dict:
    """Carry curated governance fields forward onto the regenerated records."""
    old = {s["id"]: s for s in current["skills"]}
    preserved: list[str] = []
    for record in fresh["skills"]:
        before = old.get(record["id"])
        if not before:
            continue
        if before["security"].get("result") != "unscanned":
            record["security"] = before["security"]
            preserved.append(f"{record['id']}.security")
        if before["status"] != "active":
            record["status"] = before["status"]
            preserved.append(f"{record['id']}.status")
        if before["source"].get("repository") not in (None, "unknown"):
            record["source"] = before["source"]
            preserved.append(f"{record['id']}.source")
        if not str(before["notes"]).startswith("Fields marked unknown"):
            record["notes"] = before["notes"]
            preserved.append(f"{record['id']}.notes")
        if before.get("known_weaknesses") != ["unknown"]:
            record["known_weaknesses"] = before["known_weaknesses"]
            preserved.append(f"{record['id']}.known_weaknesses")
    fresh["_preserved_from_previous"] = sorted(preserved)
    fresh["_previous_generated_at"] = current["generated_at"]
    return fresh


def annotate_divergence(fresh: dict, findings: list[dict]) -> int:
    """Record two-live-versions on the record itself, not only in the diff report.

    A conflict that exists only in a report is a conflict nobody sees again.
    """
    conflicts = {f["id"]: f for f in findings if f["class"] == "runtime conflict"}
    for record in fresh["skills"]:
        finding = conflicts.get(record["id"])
        if not finding:
            continue
        record["runtime_divergence"] = {
            "state": "two_live_versions",
            "digests": finding.get("digests", {}),
            "scanned_runtime": record["installations"][0]["runtime"],
            "note": (
                "The purpose, inputs, outputs and workflow_stages on this record describe the "
                "scanned runtime only. The other runtime holds different SKILL.md content. "
                "Resolve before treating either as authoritative."
            ),
            "detected_at": fresh["generated_at"],
        }
    return len(conflicts)


def summarize(findings: list[dict], current: dict, fresh: dict) -> dict:
    counts = {name: sum(1 for f in findings if f["class"] == name) for name in CLASSES}
    by_runtime_before: dict[str, int] = {}
    by_runtime_after: dict[str, int] = {}
    for record in current["skills"]:
        for installation in record["installations"]:
            by_runtime_before[installation["runtime"]] = by_runtime_before.get(installation["runtime"], 0) + 1
    for record in fresh["skills"]:
        for installation in record["installations"]:
            by_runtime_after[installation["runtime"]] = by_runtime_after.get(installation["runtime"], 0) + 1
    fresh_ids = {s["id"] for s in fresh["skills"]}
    return {
        "generated_at_before": current["generated_at"],
        "generated_at_after": fresh["generated_at"],
        "skills_before": len(current["skills"]),
        "skills_after": len(fresh["skills"]),
        "installations_before": by_runtime_before,
        "installations_after": by_runtime_after,
        "classified": counts,
        "august_first_capabilities": {name: name in fresh_ids for name in AUGUST_FIRST},
        "external_candidates_requiring_review": sorted(
            f["id"] for f in findings if f["class"] == "new capability" and f.get("external_candidate")
        ),
        "blocking": counts["governance concern"] + counts["runtime conflict"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("diff", "apply", "annotate-current"))
    parser.add_argument("--json", type=Path)
    parser.add_argument("--force", action="store_true",
                        help="apply despite runtime conflicts; governance concerns still block")
    args = parser.parse_args()

    module = load_registry_tool()
    current = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fresh = generate_into_temp(module)
    findings = classify(current, fresh)
    report = {"summary": summarize(findings, current, fresh), "findings": findings}

    if args.json:
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"written: {args.json}")

    summary = report["summary"]
    print(f"before {summary['skills_before']} skills {summary['installations_before']}")
    print(f"after  {summary['skills_after']} skills {summary['installations_after']}")
    for name in CLASSES:
        print(f"  {summary['classified'][name]:4d}  {name}")
    missing = [k for k, v in summary["august_first_capabilities"].items() if not v]
    print(f"august-01 capabilities present: {5 - len(missing)}/5" + (f", MISSING {missing}" if missing else ""))
    print(f"external candidates needing review: {len(summary['external_candidates_requiring_review'])}")

    if args.command == "diff":
        return 0

    if args.command == "annotate-current":
        for record in current["skills"]:
            record.pop("runtime_divergence", None)
        diverged = annotate_divergence(current, findings)
        baseline = REGISTRY.with_suffix(".yaml.baseline-2026-07-25")
        if baseline.is_file():
            baseline_data = json.loads(baseline.read_text(encoding="utf-8"))
            current["_previous_generated_at"] = baseline_data.get("generated_at")
        current["governance_policy"] = (
            "Installed is not approved. Existing status/security/provenance are preserved; "
            "runtime divergence is recorded on each affected capability."
        )
        REGISTRY.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        module.write_summary(current)
        print(f"runtime divergence annotated on {diverged} current records")
        print(f"written: {REGISTRY}")
        return 0

    concerns = [f for f in findings if f["class"] == "governance concern"]
    if concerns:
        print("\n".join(f"BLOCKED: {f['id']}: {f['detail']}" for f in concerns), file=sys.stderr)
        print("apply refused: curated governance metadata would be lost", file=sys.stderr)
        return 1
    if missing:
        print(f"apply refused: expected capabilities missing from the estate: {missing}", file=sys.stderr)
        return 1

    backup = REGISTRY.with_suffix(".yaml.pre-2026-08-11")
    shutil.copy2(REGISTRY, backup)
    merged = merge_governance(current, fresh)
    diverged = annotate_divergence(merged, findings)
    REGISTRY.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"runtime divergence annotated on {diverged} records")
    module.write_summary(merged)
    print(f"backup: {backup}")
    print(f"written: {REGISTRY}")
    print(f"governance fields preserved: {len(merged['_preserved_from_previous'])}")
    errors = module.validate()
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors), file=sys.stderr)
        return 1
    print("registry valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
