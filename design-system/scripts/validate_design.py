#!/usr/bin/env python3
"""Validate BridgeWorks tokens and lint authored text/CSS conservatively."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens.json"
BANNED = (
    "world-class", "innovative", "seamless", "ecosystem", "game-changing",
    "transformative", "robust", "cutting-edge", "passionate about",
    "leverage", "synergize", "in today's fast-paced world",
)


def token_errors(path: Path = TOKENS) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid tokens JSON: {exc}"]
    colors = data.get("color", {})
    for name, token in colors.items():
        value = token.get("$value")
        if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-F]{6}", value):
            errors.append(f"Invalid colour token {name}: {value}")
    body = data.get("font", {}).get("body", {}).get("$value", [])
    headline = data.get("font", {}).get("headline", {}).get("$value", [])
    if not body or body[0] != "Inter":
        errors.append("Body font must be Inter")
    if not headline or headline[0] != "Playfair Display":
        errors.append("Headline font must be Playfair Display")
    return errors


def authored_lines(text: str):
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or line.lstrip().startswith(">"):
            continue
        clean = re.sub(r"https?://\S+|`[^`]*`|\[[^\]]+\]\([^)]+\)", "", line)
        yield number, clean


def content_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for number, line in authored_lines(text):
        lower = line.lower()
        if "—" in line:
            errors.append(f"{path}:{number}: em dash")
        for phrase in BANNED:
            if re.search(rf"\b{re.escape(phrase)}\b", lower):
                errors.append(f"{path}:{number}: prohibited phrase '{phrase}'")
        for match in re.finditer(r"!\[([^\]]*)\]\([^)]+\)", line):
            if not match.group(1).strip():
                errors.append(f"{path}:{number}: image alt text is empty; confirm decorative intent")
    if path.suffix.lower() in {".css", ".scss", ".tsx", ".jsx", ".html"}:
        allowed = {
            "#0F1A2E", "#1C2B3A", "#243347", "#2D3F52", "#B8860B",
            "#D4A843", "#F5F0E8", "#4A6741", "#6B6560",
        }
        for colour in re.findall(r"#[0-9a-fA-F]{6}", text):
            upper = colour.upper()
            if upper not in allowed:
                errors.append(f"{path}: invalid or unreviewed BridgeWorks colour {colour}")
        fonts = re.findall(r"font-family\s*:\s*([^;}]+)", text, re.I)
        for font in fonts:
            if not any(name.lower() in font.lower() for name in ("inter", "playfair display", "courier new", "sans-serif", "serif", "monospace")):
                errors.append(f"{path}: disallowed typography {font.strip()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--tokens", type=Path, default=TOKENS)
    args = parser.parse_args()
    errors = token_errors(args.tokens)
    for path in args.files:
        errors.extend(content_errors(path))
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"Design validation passed for tokens and {len(args.files)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
