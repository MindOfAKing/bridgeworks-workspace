#!/usr/bin/env python3
"""Run SkillSpector against a quarantined target without installing it."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "skill-governance"
QUARANTINE = (GOV / "quarantine").resolve()
REPORTS = GOV / "reports"
DEFAULT_SCANNER = GOV / ".venv-skillspector" / "Scripts" / "skillspector.exe"
NOTICE = "A security scan can identify known suspicious patterns, but it does not prove that a skill is safe, necessary, correct, or appropriate."


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def git_info(target: Path) -> tuple[str, str]:
    base = target if target.is_dir() else target.parent
    repo_root = next((p for p in (base, *base.parents) if (p / ".git").exists()), base)
    def run(*args: str) -> str:
        try:
            return subprocess.check_output(
                ["git", "-c", f"safe.directory={repo_root}", "-C", str(base), *args], text=True,
                stderr=subprocess.DEVNULL, timeout=5,
            ).strip() or "unknown"
        except (OSError, subprocess.SubprocessError):
            return "unknown"
    return run("remote", "get-url", "origin"), run("rev-parse", "HEAD")


def find_severity(value) -> str:
    if isinstance(value, dict):
        for key in ("risk_severity", "severity"):
            if isinstance(value.get(key), str):
                return value[key].upper()
        for child in value.values():
            found = find_severity(child)
            if found != "UNKNOWN":
                return found
    elif isinstance(value, list):
        severities = [find_severity(item) for item in value]
        for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            if level in severities:
                return level
    return "UNKNOWN"


def find_install_hooks(target: Path) -> list[str]:
    base = target if target.is_dir() else target.parent
    hooks: list[str] = []
    for name in ("setup.py", "setup.cfg", "pyproject.toml", "package.json", "Makefile", "Dockerfile"):
        for path in base.rglob(name):
            hooks.append(str(path.relative_to(base)))
    for path in base.rglob("*"):
        if path.is_file() and re_match_hook(path.name):
            hooks.append(str(path.relative_to(base)))
    return sorted(set(hooks))[:100]


def re_match_hook(name: str) -> bool:
    lowered = name.lower()
    return lowered.startswith(("install.", "postinstall.", "preinstall.")) or lowered in {
        "install.sh", "install.ps1", "install.bat", "install.cmd"
    }


def result_exit(scanner_exit: int, severity: str) -> int:
    if scanner_exit != 0:
        return scanner_exit or 4
    return 10 if severity == "CRITICAL" else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--scanner", type=Path, default=DEFAULT_SCANNER)
    parser.add_argument("--allow-outside-quarantine", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        print(f"ERROR: target does not exist: {target}", file=sys.stderr)
        return 2
    if not args.allow_outside_quarantine and not inside(target, QUARANTINE):
        print(f"ERROR: target must be under {QUARANTINE}", file=sys.stderr)
        return 2
    scanner = args.scanner.resolve()
    if not scanner.is_file():
        print(f"ERROR: isolated scanner missing: {scanner}", file=sys.stderr)
        return 3
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = target.name.replace(" ", "-")
    raw_dir = REPORTS / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"skillspector-{slug}-{stamp}.json"
    summary_path = REPORTS / f"skillspector-{slug}-{stamp}.md"
    repository, commit = git_info(target)
    hooks = find_install_hooks(target)
    target_label = str(target.relative_to(ROOT)) if inside(target, ROOT) else str(target)
    command = [
        str(scanner), "scan", str(target), "--no-llm",
        "--format", "json", "--output", str(raw_path),
    ]
    proc = subprocess.run(command, capture_output=True, text=True, timeout=900)
    if not raw_path.exists():
        raw_path.write_text(proc.stdout or "{}", encoding="utf-8")
    try:
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
        severity = find_severity(payload)
    except json.JSONDecodeError:
        severity = "UNKNOWN"
    summary_path.write_text(
        "\n".join([
            "# SkillSpector scan summary", "",
            f"- Target: `{target_label}`",
            f"- Repository: `{repository}`",
            f"- Commit: `{commit}`",
            f"- Scanner: `{scanner}`",
            f"- UTC timestamp: `{stamp}`",
            f"- Exit code: `{proc.returncode}`",
            f"- Severity: `{severity}`",
            f"- Install/build hook candidates: `{len(hooks)}`",
            f"- Raw output: `{raw_path.relative_to(ROOT)}`",
            "", "Hook candidates:", "",
            *([f"- `{item}`" for item in hooks] if hooks else ["- None found by filename inspection."]),
            "", f"> {NOTICE}", "",
            "A manual security, overlap, permission, isolated-test, and pilot review is still required.",
        ]) + "\n",
        encoding="utf-8",
    )
    print(summary_path)
    if proc.returncode != 0:
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
    return result_exit(proc.returncode, severity)


if __name__ == "__main__":
    raise SystemExit(main())
