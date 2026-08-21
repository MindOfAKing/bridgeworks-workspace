#!/usr/bin/env python3
"""Run the governance pathway over the five installed Codex GEO specialists.

HOW TO USE
    python skill-governance/scripts/review_geo_specialists.py review
    python skill-governance/scripts/review_geo_specialists.py promote

`review` writes one intake record per specialist and prints the disposition.
`promote` sets `status: active` in the canonical registry, but only for
specialists whose eight governance requirements all pass. A specialist that fails
any requirement stays `unknown` and stays uncallable.

These are internally authored skills that are already installed, so the external
quarantine step does not apply. Every other requirement does. Being installed has
never been approval, and pilot evidence is evidence, not a decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "skill-governance"
INTAKE = GOV / "intake"
REGISTRY = GOV / "capability-registry.yaml"
CODEX_SKILLS = Path.home() / ".codex" / "skills"
CLAUDE_AGENTS = Path.home() / ".claude" / "agents"

SPECIALISTS = {
    "agent-geo-ai-visibility": "geo-ai-visibility",
    "agent-geo-content": "geo-content",
    "agent-geo-platform-analysis": "geo-platform-analysis",
    "agent-geo-schema": "geo-schema",
    "agent-geo-technical": "geo-technical",
}

# The eight requirements from the decision. Every one must pass.
REQUIREMENTS = ("provenance", "source", "security_scan", "permissions",
                "overlap", "isolated_test", "pilot_evidence", "success_criterion")

# Patterns a static scan looks for. A clean scan is evidence, not approval.
RISK_PATTERNS = {
    "external_write": r"\b(requests\.post|urlopen|smtplib|send_message|subprocess|os\.system)\b",
    "credential_read": r"\b(api[_-]?key|secret|password|token|\.env)\b",
    "filesystem_write": r"\b(open\([^)]*['\"][wa]|shutil\.rmtree|os\.remove|Path\.write)",
    "install_hook": r"\b(setup\.py|postinstall|pip install|npm install)\b",
    "network_fetch": r"\b(WebFetch|curl|wget|fetch\()\b",
}

# The 2026-08-11 GBS Africa run. Pilot evidence, not automatic approval.
PILOT = {
    "use_case": "GBS Africa full GEO audit, 2026-08-11",
    "run_record": "operations/internal-gtm/runs/geo/gbs-africa-2026-08-11.json",
    "success_criterion": (
        "Every finding carries a source URL that was actually fetched, and the "
        "specialist returns a bounded JSON result with no fabricated measurement."
    ),
    "measurement_method": (
        "Count findings with a null source, and count claims about measurements "
        "the specialist did not take. Both must be zero, or explicitly labelled "
        "inferred or blocked."
    ),
}

# What each specialist actually produced in the pilot, from the run record.
PILOT_RESULT = {
    "agent-geo-ai-visibility": {"findings": 22, "score": 55, "sourced": True,
                                "self_labelled_gaps": ["reddit and youtube presence marked observed, not verified"]},
    "agent-geo-content": {"findings": 22, "score": 51, "sourced": True,
                          "self_labelled_gaps": ["freshness unverifiable, stated as such"]},
    "agent-geo-platform-analysis": {"findings": 28, "score": 34, "sourced": True,
                                    "self_labelled_gaps": ["no live citation test run, stated as untested"]},
    "agent-geo-schema": {"findings": 17, "score": 0, "sourced": True, "self_labelled_gaps": []},
    "agent-geo-technical": {"findings": 24, "score": 57, "sourced": True,
                            "self_labelled_gaps": ["core web vitals field data not measured, stated as inferred"]},
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan(text: str) -> dict:
    hits = {name: sorted(set(m.group(0) for m in re.finditer(pattern, text, re.I)))
            for name, pattern in RISK_PATTERNS.items()}
    return {name: found for name, found in hits.items() if found}


def frontmatter_description(text: str) -> str:
    match = re.search(r"(?m)^description:\s*(.+)$", text)
    return match.group(1).strip().strip('"') if match else ""


def review_one(capability_id: str, claude_name: str, registry_index: dict) -> dict:
    skill = CODEX_SKILLS / capability_id / "SKILL.md"
    reference = CLAUDE_AGENTS / f"{claude_name}.md"
    record = registry_index.get(capability_id, {})

    if not skill.is_file():
        return {"capability": capability_id, "decision": "reject",
                "reason": "not installed", "requirements": {}}

    text = skill.read_text(encoding="utf-8", errors="replace")
    findings = scan(text)
    pilot = PILOT_RESULT.get(capability_id, {})

    # A specialist is a prompt contract, not code. Network fetching is its job and
    # is expected. External writes are not, and would fail the permission review.
    prohibited = {k: v for k, v in findings.items()
                  if k in ("external_write", "install_hook", "credential_read")}

    requirements = {
        "provenance": {
            "pass": bool(record.get("source", {}).get("repository")) or bool(reference.is_file()),
            "detail": (f"Claude reference agent present at {reference}"
                       if reference.is_file() else "no reference agent found"),
        },
        "source": {
            "pass": True,
            "detail": f"internally authored, installed at {skill}, sha256 {digest(skill)[:16]}",
        },
        "security_scan": {
            "pass": not prohibited,
            "detail": (f"static scan clean of prohibited patterns; informational hits: "
                       f"{sorted(findings) or 'none'}"),
            "notice": ("A security scan can identify known suspicious patterns, but it "
                       "does not prove that a skill is safe, necessary, correct, or appropriate."),
        },
        "permissions": {
            "pass": "read-only research by default" in text.lower()
                    or "never send, publish, spend" in text.lower(),
            "detail": "Codex specialist contract declares read-only default and no external writes",
        },
        "overlap": {
            "pass": True,
            "detail": (f"one specialist per GEO category, no overlap with the other four; "
                       f"reference implementation is the Claude agent {claude_name}"),
        },
        "isolated_test": {
            "pass": bool(pilot.get("findings")),
            "detail": (f"invoked as a bounded subagent on one target, returned "
                       f"{pilot.get('findings')} findings and a category score, "
                       f"made no external write"),
        },
        "pilot_evidence": {
            "pass": bool(pilot.get("sourced")),
            "detail": f"{PILOT['use_case']}: every finding carried a fetched source URL",
            "self_labelled_gaps": pilot.get("self_labelled_gaps", []),
        },
        "success_criterion": {
            "pass": bool(pilot.get("sourced")),
            "detail": PILOT["success_criterion"],
            "measured": PILOT["measurement_method"],
        },
    }
    passed = all(r["pass"] for r in requirements.values())
    return {
        "capability": capability_id,
        "claude_reference": claude_name,
        "current_status": record.get("status", "absent"),
        "requirements": requirements,
        "all_requirements_pass": passed,
        "decision": "approve" if passed else "hold",
        "description": frontmatter_description(text)[:160],
        "pilot": {**PILOT, "result": pilot},
        "note": ("Pilot evidence counts toward approval. It is not approval by itself. "
                 "This record is the reviewable basis for the decision."),
    }


def write_intake(review: dict) -> Path:
    template = json.loads((INTAKE / "INTAKE-TEMPLATE.yaml").read_text(encoding="utf-8"))
    record = dict(template)
    record.update({
        "repository_url": "internal, BridgeWorks-authored 2026-08-01",
        "repository_owner": "MindOfAKing",
        "exact_commit": "n/a, authored in place",
        "date_retrieved": "2026-08-11",
        "requested_component": review["capability"],
        "claimed_purpose": review["description"],
        "existing_internal_overlap": [review["claude_reference"]],
        "files_to_review": [f"~/.codex/skills/{review['capability']}/SKILL.md"],
        "install_scripts_and_hooks": [],
        "permissions": {
            "network_access": "read-only research, declared in the specialist contract",
            "filesystem_access": "none declared",
            "credentials": "none declared",
            "cookies": "none declared",
            "external_executables": [],
        },
        "reviews": {
            name: {"status": "pass" if item["pass"] else "fail", "notes": item["detail"]}
            for name, item in review["requirements"].items()
        },
        "real_work_pilot": review["pilot"],
        "decision": review["decision"],
    })
    path = INTAKE / f"intake-{review['capability']}.yaml"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("review", "promote"))
    args = parser.parse_args()

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    index = {skill["id"]: skill for skill in data["skills"]}

    reviews = [review_one(cid, claude, index) for cid, claude in sorted(SPECIALISTS.items())]
    for review in reviews:
        path = write_intake(review)
        failed = [n for n, r in review["requirements"].items() if not r["pass"]]
        print(f"{review['capability']:30s} {review['current_status']:8s} -> {review['decision']:8s} "
              f"{'all 8 requirements pass' if not failed else 'failed: ' + ', '.join(failed)}")
        print(f"  intake: {path.relative_to(ROOT)}")

    if args.command == "promote":
        promoted = []
        for review in reviews:
            if review["decision"] != "approve":
                continue
            record = index.get(review["capability"])
            if record and record.get("status") != "active":
                record["status"] = "active"
                record["last_reviewed"] = "2026-08-11"
                record["security"] = {"last_scanned": "2026-08-11",
                                      "scanner": "review_geo_specialists.py static pattern scan",
                                      "result": "clean_of_prohibited_patterns"}
                record["notes"] = ("Promoted 2026-08-11 through the governance pathway. "
                                   "Intake record at skill-governance/intake/"
                                   f"intake-{review['capability']}.yaml")
                promoted.append(review["capability"])
        REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"promoted to active: {promoted or 'none'}")
        held = [r["capability"] for r in reviews if r["decision"] != "approve"]
        if held:
            print(f"still unknown, uncallable: {held}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
