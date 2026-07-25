from __future__ import annotations

import argparse
import csv
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import urlparse


ENGINE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ENGINE_ROOT / "research" / "prospect-operations"
DEFAULT_TARGET = SOURCE_ROOT / "prospect-source-current.csv"
LEGACY_SOURCE = ENGINE_ROOT.parents[1] / "operations" / "lead-engine-v1" / "01-prospects" / "prospect-batch-2026-07-14.csv"

BASE_FIELDS = [
    "status",
    "lane",
    "company",
    "website",
    "city",
    "country",
    "sector",
    "trigger_observation",
    "proof_to_use",
    "source",
    "contact_name",
    "contact_role",
    "contact_url",
    "email",
    "first_contact_sent",
    "follow_up_1_sent",
    "follow_up_2_sent",
    "linkedin_touch",
    "mini_observation_created",
    "next_action",
    "notes",
]
FIELDS = BASE_FIELDS + ["evidence_urls", "checked_at", "canonical_domain"]
ACTIVE_LANES = {
    "Lane A Budapest credibility-first SMEs",
    "Lane B African-owned businesses in Europe",
    "Lane D Nigeria growth businesses",
}


def clean(value: object, limit: int = 4000) -> str:
    return str(value or "").strip()[:limit]


def canonical_domain(value: object) -> str:
    text = clean(value, 2000)
    if not text:
        return ""
    parsed = urlparse(text if "://" in text else f"https://{text}")
    return parsed.netloc.lower().removeprefix("www.").split(":")[0]


def company_key(company: object, country: object) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", clean(company).lower()).strip()
    return f"{normalized}|{clean(country).lower()}"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {field: clean(row.get(field)) for field in FIELDS}
            for row in csv.DictReader(handle)
        ]


def atomic_write(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(raw_path, path)
    finally:
        try:
            os.unlink(raw_path)
        except FileNotFoundError:
            pass


def seed(source: Path, target: Path) -> dict:
    if target.exists():
        return {"ok": True, "created": False, "target": str(target), "rows": len(read_rows(target))}
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        legacy = list(csv.DictReader(handle))
    rows: list[dict[str, str]] = []
    for source_row in legacy:
        row = {field: clean(source_row.get(field)) for field in FIELDS}
        row["canonical_domain"] = canonical_domain(row["website"])
        rows.append(row)
    atomic_write(target, rows)
    return {"ok": True, "created": True, "target": str(target), "rows": len(rows)}


def load_candidates(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("prospects", [])
    if not isinstance(payload, list):
        raise ValueError("candidate input must be a list or an object with a prospects list")
    return [item for item in payload if isinstance(item, dict)]


def add_candidates(input_path: Path, target: Path) -> dict:
    rows = read_rows(target)
    domains = {row["canonical_domain"] for row in rows if row["canonical_domain"]}
    company_keys = {company_key(row["company"], row["country"]) for row in rows}
    added: list[str] = []
    skipped: list[dict[str, str]] = []

    for item in load_candidates(input_path):
        company = clean(item.get("company"), 240)
        country = clean(item.get("country"), 120)
        website = clean(item.get("website"), 2000)
        domain = canonical_domain(website)
        lane = clean(item.get("lane"), 240)
        evidence = item.get("evidence_urls", [])
        if isinstance(evidence, str):
            evidence = [part.strip() for part in evidence.split("|") if part.strip()]
        evidence = [clean(url, 2000) for url in evidence if clean(url)]
        reason = ""
        if not company or not country:
            reason = "company and country are required"
        elif lane not in ACTIVE_LANES:
            reason = "lane is not an approved active lane"
        elif not evidence or not all(url.startswith(("http://", "https://")) for url in evidence):
            reason = "at least one valid evidence URL is required"
        elif domain and domain in domains:
            reason = "duplicate domain"
        elif company_key(company, country) in company_keys:
            reason = "duplicate company and country"
        if reason:
            skipped.append({"company": company or "(missing)", "reason": reason})
            continue

        row = {field: clean(item.get(field)) for field in FIELDS}
        row.update(
            {
                "status": "research",
                "company": company,
                "country": country,
                "website": website,
                "lane": lane,
                "evidence_urls": " | ".join(evidence),
                "checked_at": clean(item.get("checked_at"), 40),
                "canonical_domain": domain,
            }
        )
        rows.append(row)
        added.append(company)
        if domain:
            domains.add(domain)
        company_keys.add(company_key(company, country))

    if added:
        atomic_write(target, rows)
    return {
        "ok": True,
        "target": str(target),
        "added": added,
        "added_count": len(added),
        "skipped": skipped,
        "total_rows": len(rows),
    }


def status(target: Path) -> dict:
    rows = read_rows(target)
    by_lane: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for row in rows:
        by_lane[row["lane"]] = by_lane.get(row["lane"], 0) + 1
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    return {"ok": True, "target": str(target), "rows": len(rows), "by_lane": by_lane, "by_status": by_status}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and maintain the BridgeWorks rolling prospect source.")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    subparsers = parser.add_subparsers(dest="command", required=True)
    seed_parser = subparsers.add_parser("seed")
    seed_parser.add_argument("--from-csv", type=Path, default=LEGACY_SOURCE)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--input", type=Path, required=True)
    subparsers.add_parser("status")
    args = parser.parse_args()
    try:
        if args.command == "seed":
            result = seed(args.from_csv.resolve(), args.target.resolve())
        elif args.command == "add":
            result = add_candidates(args.input.resolve(), args.target.resolve())
        else:
            result = status(args.target.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
