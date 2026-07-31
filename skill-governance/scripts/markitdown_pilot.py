#!/usr/bin/env python3
"""Convert declared local samples with isolated MarkItDown and record metrics."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "skill-governance"
DEFAULT_CLI = GOV / ".venv-markitdown" / "Scripts" / "markitdown.exe"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cli", type=Path, default=DEFAULT_CLI)
    parser.add_argument("--output", type=Path, default=GOV / "reports" / "markitdown-pilot-data.json")
    args = parser.parse_args()
    if not args.cli.is_file():
        print(f"ERROR: isolated MarkItDown missing: {args.cli}")
        return 3
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    out_dir = GOV / "reports" / "markitdown-output"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    failures = 0
    for sample in manifest["samples"]:
        source = Path(sample["path"]).resolve()
        target = out_dir / f"{sample['id']}.md"
        started = time.perf_counter()
        proc = subprocess.run(
            [str(args.cli), str(source), "-o", str(target)],
            capture_output=True, text=True, timeout=300,
        )
        elapsed = time.perf_counter() - started
        text = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
        if proc.returncode:
            failures += 1
        source_bytes = source.stat().st_size if source.exists() else 0
        results.append({
            **sample,
            "source_bytes": source_bytes,
            "markdown_bytes": len(text.encode("utf-8")),
            "markdown_characters": len(text),
            "approx_source_tokens_by_bytes": round(source_bytes / 4),
            "approx_markdown_tokens_by_chars": round(len(text) / 4),
            "processing_seconds": round(elapsed, 3),
            "exit_code": proc.returncode,
            "stderr": proc.stderr[-500:],
            "output": str(target),
        })
    payload = {
        "date": date.today().isoformat(),
        "cli": str(args.cli),
        "method_note": "Token figures are rough byte/character divided by four estimates, not tokenizer counts.",
        "results": results,
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(args.output)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
