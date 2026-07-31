#!/usr/bin/env python3
"""Generate and validate the installed-skill capability registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "skill-governance" / "capability-registry.yaml"
SUMMARY = ROOT / "skill-governance" / "CAPABILITY-REGISTRY.md"
LIVE_ROOTS = {
    "claude": Path.home() / ".claude" / "skills",
    "codex": Path.home() / ".codex" / "skills",
}
SOURCE_ROOTS = [
    Path.home() / "Projects" / "claude-skills",
    Path.home() / "Projects" / "bridgeworks-codex" / "plugin" / "skills",
    ROOT / "operations" / "content-system" / "skills",
]
REQUIRED = {
    "id", "name", "path", "purpose", "category", "triggers", "inputs",
    "outputs", "tools", "permissions", "overlaps_with", "source", "status",
    "security", "last_reviewed", "notes",
}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    result: dict[str, str] = {}
    for key in ("name", "description"):
        match = re.search(rf"(?m)^{key}:\s*(.+)$", block)
        if match:
            result[key] = match.group(1).strip().strip("\"'")
    return result


def bullets_under(text: str, headings: tuple[str, ...]) -> list[str]:
    lines = text.splitlines()
    found: list[str] = []
    active = False
    for line in lines:
        if line.startswith("#"):
            title = line.lstrip("#").strip().lower()
            active = any(h in title for h in headings)
            continue
        if active:
            match = re.match(r"\s*[-*]\s+\**([^:*]+)", line)
            if match:
                item = match.group(1).strip().strip("*")
                if item and item.lower() not in {"unknown", "none"}:
                    found.append(item[:120])
            elif line.strip() and not line.startswith((" ", "\t")):
                active = False
    return list(dict.fromkeys(found))[:12]


def git_value(path: Path, args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), *args],
            text=True, stderr=subprocess.DEVNULL, timeout=5,
        ).strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance(skill_file: Path) -> dict[str, str | None]:
    file_hash = digest(skill_file)
    for source_root in SOURCE_ROOTS:
        candidate = source_root / skill_file.parent.name / "SKILL.md"
        if candidate.is_file() and digest(candidate) == file_hash:
            repo = git_value(source_root, ["rev-parse", "--show-toplevel"])
            commit = git_value(source_root, ["rev-parse", "HEAD"])
            remote = git_value(Path(repo), ["remote", "get-url", "origin"]) if repo else None
            return {"type": "internal", "repository": remote or repo, "version": commit}
    return {"type": "internal", "repository": "unknown", "version": "unknown"}


def categories(name: str, description: str) -> list[str]:
    allowed = (
        "geo", "seo", "market", "youtube", "proposal", "sales", "research",
        "content", "design", "document", "automation", "reporting", "memory",
        "development", "client-ops", "image",
    )
    haystack = f"{name} {description}".lower()
    found = [item for item in allowed if item in haystack]
    return found or ["general"]


def explicit_tools(text: str) -> list[str]:
    patterns = {
        "browser": r"\bbrowser\b|\bplaywright\b",
        "web_search": r"\bweb search\b|\bsearch the web\b",
        "gmail": r"\bgmail\b",
        "notebooklm": r"\bnotebooklm\b",
        "youtube_api": r"youtube data api|youtube_api_key",
        "filesystem": r"\bsave to\b|\bwrite (?:a |the )?file\b|\bcreate (?:a |the )?file\b",
        "python": r"\bpython(?:3)?\b|\.py\b",
        "git": r"\bgit\b",
    }
    lower = text.lower()
    return [name for name, pattern in patterns.items() if re.search(pattern, lower)]


def generate() -> dict:
    records: dict[str, dict] = {}
    for runtime, root in LIVE_ROOTS.items():
        if not root.is_dir():
            continue
        for skill_file in sorted(root.glob("*/SKILL.md")):
            text = skill_file.read_text(encoding="utf-8", errors="replace")
            meta = frontmatter(text)
            name = meta.get("name") or skill_file.parent.name
            skill_id = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
            description = meta.get("description", "unknown")
            modified = datetime.fromtimestamp(skill_file.stat().st_mtime).date().isoformat()
            inputs = bullets_under(text, ("input", "required information"))
            outputs = bullets_under(text, ("output", "what this produces", "deliverable"))
            tools = explicit_tools(text)
            permissions = {
                "network": True if any(t in tools for t in ("browser", "web_search", "gmail", "notebooklm", "youtube_api", "git")) else "unknown",
                "filesystem_write": True if "filesystem" in tools else "unknown",
                "credentials": True if re.search(r"api[_ -]?key|credential|oauth|token", text, re.I) else "unknown",
            }
            installation = {"runtime": runtime, "path": str(skill_file.parent)}
            if skill_id in records:
                records[skill_id]["installations"].append(installation)
                records[skill_id]["notes"] = "Installed in multiple runtimes; review overlap before editing either copy."
                continue
            trigger_phrases = re.findall(r'"([^"]{3,80})"', description)
            records[skill_id] = {
                "id": skill_id,
                "name": name,
                "path": str(skill_file.parent),
                "installations": [installation],
                "purpose": description,
                "category": categories(name, description),
                "triggers": trigger_phrases[:10] or [description],
                "inputs": inputs or ["unknown"],
                "outputs": outputs or ["unknown"],
                "tools": tools or ["unknown"],
                "permissions": permissions,
                "workflow_stages": [h.lower() for h in re.findall(r"(?m)^##\s+(?:Step \d+:\s*)?(.+)$", text)[:15]] or ["unknown"],
                "expected_deliverables": outputs or ["unknown"],
                "overlaps_with": [],
                "source": provenance(skill_file),
                "status": "active",
                "security": {"last_scanned": None, "scanner": None, "result": "unscanned"},
                "last_modified": modified,
                "last_reviewed": date.today().isoformat(),
                "tests": [str(p) for p in skill_file.parent.rglob("*") if p.is_file() and "test" in p.name.lower()][:10] or ["unknown"],
                "known_weaknesses": ["unknown"],
                "notes": "Fields marked unknown were not explicit in SKILL.md.",
            }
    skills = list(records.values())
    for skill in skills:
        stem = set(re.findall(r"[a-z0-9]+", skill["id"])) - {"skill", "report"}
        overlaps = []
        for other in skills:
            if other["id"] == skill["id"]:
                continue
            other_stem = set(re.findall(r"[a-z0-9]+", other["id"])) - {"skill", "report"}
            if stem and other_stem and len(stem & other_stem) / len(stem | other_stem) >= 0.5:
                overlaps.append(other["id"])
        skill["overlaps_with"] = sorted(overlaps)[:12]
    data = {
        "schema_version": 1,
        "generated_at": date.today().isoformat(),
        "scope": "Unique skills installed in live Claude and Codex skill roots.",
        "field_policy": "unknown means the value was not explicit in the inspected SKILL.md.",
        "skills": sorted(skills, key=lambda item: item["id"]),
    }
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_summary(data)
    return data


def write_summary(data: dict) -> None:
    skills = data["skills"]
    installations = sum(len(s.get("installations", [])) for s in skills)
    lines = [
        "# Capability Registry",
        "",
        f"Generated: {data['generated_at']}",
        "",
        f"Scope: {len(skills)} unique live capabilities across {installations} installations.",
        "",
        "Unknown values are deliberate. They mean the source instructions did not verify the field.",
        "",
        "| ID | Purpose | Runtime(s) | Category | Security |",
        "|---|---|---|---|---|",
    ]
    for skill in skills:
        purpose = skill["purpose"].replace("|", "\\|")[:150]
        runtimes = ", ".join(i["runtime"] for i in skill["installations"])
        lines.append(
            f"| `{skill['id']}` | {purpose} | {runtimes} | "
            f"{', '.join(skill['category'])} | {skill['security']['result']} |"
        )
    lines.extend([
        "",
        "## Validation",
        "",
        "Run `python skill-governance/scripts/registry_tool.py validate` from the repository root.",
        "Generation reads every live `SKILL.md`, extracts explicit metadata, records hashes/provenance matches, and leaves unsupported details as `unknown`.",
    ])
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(path: Path = REGISTRY) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Registry is not valid JSON-compatible YAML: {exc}"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        return errors + ["skills must be a non-empty list"]
    seen: set[str] = set()
    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"skills[{index}] must be an object")
            continue
        missing = REQUIRED - set(skill)
        if missing:
            errors.append(f"skills[{index}] missing: {', '.join(sorted(missing))}")
        skill_id = skill.get("id")
        if not isinstance(skill_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill_id):
            errors.append(f"skills[{index}].id is invalid")
        elif skill_id in seen:
            errors.append(f"duplicate id: {skill_id}")
        seen.add(skill_id)
        if skill.get("status") not in {"active", "experimental", "deprecated", "unknown"}:
            errors.append(f"{skill_id}: invalid status")
        for key in ("category", "triggers", "inputs", "outputs", "tools", "overlaps_with"):
            if not isinstance(skill.get(key), list):
                errors.append(f"{skill_id}: {key} must be a list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("generate", "validate"))
    parser.add_argument("--path", type=Path, default=REGISTRY)
    args = parser.parse_args()
    if args.command == "generate":
        data = generate()
        print(f"Generated {len(data['skills'])} unique skills at {REGISTRY}")
    errors = validate(args.path)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"Registry valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
