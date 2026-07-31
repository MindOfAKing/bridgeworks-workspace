#!/usr/bin/env python3
"""Compare a proposed skill intake record with explicit registry evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "skill-governance" / "capability-registry.yaml"


def words(value) -> set[str]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return set(re.findall(r"[a-z0-9]+", text.lower())) - {
        "the", "and", "for", "with", "from", "use", "when", "this", "that",
        "skill", "unknown", "user", "asks",
    }


def score(proposal: dict, skill: dict) -> tuple[int, list[str]]:
    evidence: list[str] = []
    total = 0
    fields = {
        "purpose": (proposal.get("claimed_purpose", ""), skill.get("purpose", "")),
        "inputs": (proposal.get("inputs", []), skill.get("inputs", [])),
        "outputs": (proposal.get("outputs", []), skill.get("outputs", [])),
        "triggers": (proposal.get("triggers", []), skill.get("triggers", [])),
        "tools": (proposal.get("tools", []), skill.get("tools", [])),
        "workflow": (proposal.get("workflow_stages", []), skill.get("workflow_stages", [])),
        "deliverables": (proposal.get("expected_deliverables", []), skill.get("expected_deliverables", [])),
    }
    weights = {"purpose": 4, "inputs": 1, "outputs": 2, "triggers": 1, "tools": 1, "workflow": 2, "deliverables": 2}
    for name, (left, right) in fields.items():
        a, b = words(left), words(right)
        if not a or not b:
            continue
        overlap = a & b
        ratio = len(overlap) / len(a | b)
        if overlap:
            total += round(ratio * 100 * weights[name])
            evidence.append(f"{name}: shared terms {', '.join(sorted(overlap)[:10])}")
    if skill["id"] in proposal.get("existing_internal_overlap", []):
        total += 100
        evidence.append("proposal explicitly names this internal overlap")
    return total, evidence


def classify(matches: list[tuple[int, dict, list[str]]], proposal: dict) -> tuple[str, str]:
    if not proposal.get("claimed_purpose") or proposal.get("claimed_purpose") == "unknown":
        return "Unclear and requires manual review", "Reject pending complete metadata"
    top = matches[0][0] if matches else 0
    if top >= 180:
        return "Duplicate", "Reject"
    if top >= 110:
        return "Improvement candidate", "Reference only or cherry-pick procedure"
    if top >= 60:
        return "Partial gap", "Pilot isolated component"
    if proposal.get("framework_replacement"):
        return "Conflicting framework", "Reject"
    return "Genuine capability gap", "Pilot isolated component"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    proposal = json.loads(args.proposal.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    matches = []
    for skill in registry["skills"]:
        value, evidence = score(proposal, skill)
        if value:
            matches.append((value, skill, evidence))
    matches.sort(key=lambda item: (-item[0], item[1]["id"]))
    classification, recommendation = classify(matches, proposal)
    output = args.output or ROOT / "skill-governance" / "reports" / f"capability-diff-{args.proposal.stem}.md"
    lines = [
        "# Capability Diff", "",
        "## Proposed component", "",
        str(proposal.get("requested_component", "unknown")), "",
        "## Claimed function", "",
        str(proposal.get("claimed_purpose", "unknown")), "",
        "## Classification", "", classification, "",
        "## Existing equivalents", "",
    ]
    if matches:
        for value, skill, _ in matches[:8]:
            lines.append(f"- `{skill['id']}` (evidence score {value}): `{skill['path']}`")
    else:
        lines.append("- None identified. Manual review is still required.")
    lines += [
        "", "## Genuine missing capability", "",
        "Manual reviewer must confirm which deliverable or workflow stage is absent.", "",
        "## Conflicts or duplication", "",
        "Review the cited source files. Automated evidence is advisory and does not decide installation.", "",
        "## Permission difference", "",
        f"Proposed: `{json.dumps(proposal.get('permissions', {}), ensure_ascii=False)}`", "",
        "## Recommendation", "", f"- {recommendation}", "",
        "## Evidence", "",
    ]
    for value, skill, evidence in matches[:8]:
        lines.append(f"### {skill['id']} ({value})")
        lines.append(f"Source: `{skill['path'] / Path('SKILL.md') if isinstance(skill['path'], Path) else skill['path'] + '/SKILL.md'}`")
        lines.extend(f"- {item}" for item in evidence)
        lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
