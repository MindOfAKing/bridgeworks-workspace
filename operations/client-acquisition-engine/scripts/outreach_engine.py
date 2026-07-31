from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ENGINE_ROOT = Path(__file__).resolve().parents[1]
OPS_ROOT = ENGINE_ROOT / "research" / "prospect-operations"
DEFAULT_SOURCE = OPS_ROOT / "prospect-source-current.csv"
DEFAULT_SNAPSHOT = OPS_ROOT / "live-source-snapshot-2026-07-26.json"
DEFAULT_PACKET = ENGINE_ROOT / "approvals" / "LANE-A-FIRST-CONTACT-APPROVAL-PACKET-2026-07-14.md"
DEFAULT_OUTPUT = OPS_ROOT / "operating-output"

SOURCE_FIELDS = [
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
    "evidence_urls",
    "checked_at",
    "canonical_domain",
]

REGISTER_FIELDS = [
    "prospect_id",
    *SOURCE_FIELDS,
    "icp_segment",
    "dedupe_key",
    "evidence_state",
    "outreach_authority",
]

CAMPAIGN_FIELDS = [
    "batch_id",
    "wave",
    "prospect_id",
    "company",
    "contact",
    "to",
    "subject",
    "body",
    "evidence",
    "source_status",
    "approval_state",
    "sending_authority",
    "follow_up_1_due",
    "follow_up_2_due",
]

ACTIVE_LANES = {
    "Lane A Budapest credibility-first SMEs": "CEE credibility-first SME",
    "Lane B African-owned businesses in Europe": "African-owned business in Europe",
    "Lane D Nigeria growth businesses": "Nigeria growth business",
}


def clean(value: Any, limit: int = 8000) -> str:
    return str(value or "").strip()[:limit]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "prospect"


def domain(value: str) -> str:
    value = clean(value, 2000)
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else f"https://{value}")
    return parsed.netloc.lower().removeprefix("www.").split(":")[0]


def company_key(company: str, country: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", company.lower()).strip()
    return f"{normalized}|{country.lower().strip()}"


def stable_id(row: dict[str, str]) -> str:
    key = row.get("canonical_domain") or company_key(row["company"], row["country"])
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:10]
    return f"BW-P-{digest}"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {field: clean(row.get(field)) for field in SOURCE_FIELDS}
            for row in csv.DictReader(handle)
        ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(raw, path)
    finally:
        try:
            os.unlink(raw)
        except FileNotFoundError:
            pass


def load_snapshot(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def reconcile(rows: list[dict[str, str]], snapshot: dict[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    touches: dict[str, list[dict[str, str]]] = defaultdict(list)
    for touch in snapshot.get("gmail", {}).get("touches", []):
        touches[slug(clean(touch.get("company")))].append(touch)

    changes: list[dict[str, str]] = []
    for row in rows:
        row["canonical_domain"] = row["canonical_domain"] or domain(row["website"])
        company_touches = sorted(touches.get(slug(row["company"]), []), key=lambda item: item["sent_at"])
        if not company_touches:
            continue
        before = json.dumps(row, sort_keys=True)
        first = next((item for item in company_touches if item.get("kind") == "first_contact"), company_touches[0])
        follow_up = next((item for item in company_touches if item.get("kind") == "follow_up_1"), None)
        if row["status"] not in {"won", "lost", "rejected"}:
            row["status"] = "sent-no-reply"
        row["first_contact_sent"] = clean(first.get("sent_at"))
        if follow_up:
            row["follow_up_1_sent"] = clean(follow_up.get("sent_at"))
        row["next_action"] = "Hold further outreach. Check reply state and require a new exact approval before any recontact."
        evidence = " | ".join(
            f"Gmail message {item.get('message_id')} sent {item.get('sent_at')}"
            for item in company_touches
        )
        if evidence not in row["notes"]:
            row["notes"] = " | ".join(part for part in [row["notes"], evidence] if part)
        if json.dumps(row, sort_keys=True) != before:
            changes.append(
                {
                    "company": row["company"],
                    "status": row["status"],
                    "first_contact_sent": row["first_contact_sent"],
                    "follow_up_1_sent": row["follow_up_1_sent"],
                }
            )
    return rows, changes


def validate(rows: list[dict[str, str]]) -> dict[str, Any]:
    domains: dict[str, list[str]] = defaultdict(list)
    companies: dict[str, list[str]] = defaultdict(list)
    missing = Counter()
    for row in rows:
        key = row["canonical_domain"]
        if key:
            domains[key].append(row["company"])
        companies[company_key(row["company"], row["country"])].append(row["company"])
        for field in ["website", "email", "contact_name", "contact_role", "evidence_urls", "checked_at"]:
            if not row[field]:
                missing[field] += 1
    return {
        "rows": len(rows),
        "duplicate_domains": {key: value for key, value in domains.items() if len(value) > 1},
        "duplicate_company_country": {key: value for key, value in companies.items() if len(value) > 1},
        "missing": dict(missing),
        "status_counts": dict(Counter(row["status"] for row in rows)),
        "lane_counts": dict(Counter(row["lane"] for row in rows)),
    }


def build_register(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    register: list[dict[str, str]] = []
    for row in rows:
        prospect_id = stable_id(row)
        evidence_state = "current" if row["evidence_urls"] and row["checked_at"] else "missing-or-stale"
        register.append(
            {
                "prospect_id": prospect_id,
                **row,
                "icp_segment": ACTIVE_LANES.get(row["lane"], "deferred"),
                "dedupe_key": row["canonical_domain"] or company_key(row["company"], row["country"]),
                "evidence_state": evidence_state,
                "outreach_authority": "draft-only",
            }
        )
    return register


def parse_packet(path: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^###\s+\d+\.\s+(.+?)\s*$", text, re.MULTILINE))
    rows_by_company = {slug(row["company"]): row for row in rows}
    rows_by_email = {row["email"].lower(): row for row in rows if row["email"]}
    parsed: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## Guardrails", start)
        block = text[start:end]
        company = match.group(1).strip()
        wave = "priority" if match.start() < text.find("\n## Test Segment") else "test"
        to_match = re.search(r"^To:\s*(.+?)\s{2,}$", block, re.MULTILINE)
        contact_match = re.search(r"^Contact:\s*(.+?)\s{2,}$", block, re.MULTILINE)
        subject_match = re.search(r"^Subject:\s*(.+?)\s*$", block, re.MULTILINE)
        evidence_match = re.search(r"^Evidence:\s*(.+?)\s*$", block, re.MULTILINE)
        if not (to_match and subject_match and evidence_match):
            continue
        recipient = clean(to_match.group(1))
        source_row = rows_by_email.get(recipient.lower()) or rows_by_company.get(slug(company))
        body_start = subject_match.end()
        body_end = evidence_match.start()
        body = block[body_start:body_end].strip()
        parsed.append(
            {
                "batch_id": f"BW-OUTREACH-{date.today().isoformat()}",
                "wave": wave,
                "prospect_id": "",
                "company": company,
                "contact": clean(contact_match.group(1) if contact_match else ""),
                "to": recipient,
                "subject": clean(subject_match.group(1)),
                "body": body,
                "evidence": clean(evidence_match.group(1)),
                "source_status": source_row["status"] if source_row else "unmatched",
                "approval_state": "awaiting_explicit_approval",
                "sending_authority": "none",
                "follow_up_1_due": "set only after verified send + 3 business days",
                "follow_up_2_due": "set only after verified send + 7 business days",
            }
        )
        parsed[-1]["prospect_id"] = stable_id(source_row) if source_row else ""
    return parsed


def hubspot_previews(
    register: list[dict[str, str]], snapshot: dict[str, Any]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    existing_domains = {domain(value) for value in snapshot["hubspot"]["existing_domains"]}
    existing_emails = {clean(value).lower() for value in snapshot["hubspot"]["existing_contact_emails"]}
    companies: list[dict[str, str]] = []
    contacts: list[dict[str, str]] = []
    for row in register:
        if row["canonical_domain"] and row["canonical_domain"] not in existing_domains:
            companies.append(
                {
                    "Company name": row["company"],
                    "Company domain name": row["canonical_domain"],
                    "City": row["city"],
                    "Country/Region": row["country"],
                    "Description": (
                        f"BridgeWorks staging ID {row['prospect_id']}. Lane: {row['lane']}. "
                        f"Sector: {row['sector']}. Source: {row['source']}. "
                        f"Next internal action: {row['next_action']}"
                    ),
                }
            )
        email = row["email"].lower()
        if not email or email in existing_emails:
            continue
        name_parts = row["contact_name"].split()
        if name_parts:
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])
        else:
            first_name = row["company"]
            last_name = "Team"
        contacts.append(
            {
                "First name": first_name,
                "Last name": last_name,
                "Email": row["email"],
                "Job title": row["contact_role"],
                "Associated company domain": row["canonical_domain"],
                "Lifecycle stage": "Lead",
                "Lead status": "New",
            }
        )
    return companies, contacts


def weekly_report(
    audit: dict[str, Any],
    snapshot: dict[str, Any],
    campaign: list[dict[str, str]],
    company_imports: list[dict[str, str]],
    contact_imports: list[dict[str, str]],
) -> str:
    status = audit["status_counts"]
    touches = snapshot["gmail"]["touches"]
    unique_contacted = len({slug(item["company"]) for item in touches})
    priority = sum(1 for item in campaign if item["wave"] == "priority")
    test = sum(1 for item in campaign if item["wave"] == "test")
    return f"""# BridgeWorks Prospecting Weekly Conversion Report

Week ending: {date.today().isoformat()}
Mode: draft-only

## Funnel

| Metric | Current |
|---|---:|
| Staging prospects | {audit['rows']} |
| Active research queue | {status.get('research', 0) + status.get('research-high-scale', 0) + status.get('scan-drafted-awaiting-approval', 0)} |
| Priority campaign-ready drafts | {priority} |
| Test-segment drafts | {test} |
| Unique companies contacted in verified Gmail evidence | {unique_contacted} |
| Verified outbound messages | {len(touches)} |
| Replies | {snapshot['gmail']['reply_count_for_verified_outreach_threads']} |
| Bounces | {snapshot['gmail']['bounce_count']} |
| Discovery calls | 0 |
| HubSpot deals | {snapshot['hubspot']['deal_count']} |
| Wins | 0 |

## CRM Preparation

| Artifact | Rows |
|---|---:|
| New-company import preview after domain dedupe | {len(company_imports)} |
| New-contact import preview after email dedupe | {len(contact_imports)} |

## Conversion Rates

- Reply rate: 0 / {len(touches)} = 0%.
- Positive reply rate: 0 / {len(touches)} = 0%.
- Discovery rate: 0 / {unique_contacted} = 0%.
- Proposal and win rates are not measurable because HubSpot has zero deals.

## Control Notes

- Campaign rows have no sending authority. Approval is exact-copy and exact-destination only.
- Follow-up dates are created only after a verified send event.
- Bounce, opt-out, and negative reply immediately suppress further outreach.
- HubSpot becomes the commercial source of truth only after an approved import and reconciliation pass.
"""


def run(
    source: Path,
    snapshot_path: Path,
    packet: Path,
    output: Path,
    write_source: bool,
) -> dict[str, Any]:
    rows = read_csv(source)
    snapshot = load_snapshot(snapshot_path)
    rows, changes = reconcile(rows, snapshot)
    audit = validate(rows)
    if audit["duplicate_domains"] or audit["duplicate_company_country"]:
        raise ValueError("deduplication validation failed")
    if write_source:
        write_csv(source, SOURCE_FIELDS, rows)

    register = build_register(rows)
    campaign = parse_packet(packet, rows)
    companies, contacts = hubspot_previews(register, snapshot)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "canonical-prospect-register.csv", REGISTER_FIELDS, register)
    write_csv(
        output / "hubspot-companies-import-preview.csv",
        ["Company name", "Company domain name", "City", "Country/Region", "Description"],
        companies,
    )
    write_csv(
        output / "hubspot-contacts-import-preview.csv",
        [
            "First name",
            "Last name",
            "Email",
            "Job title",
            "Associated company domain",
            "Lifecycle stage",
            "Lead status",
        ],
        contacts,
    )
    write_csv(output / "campaign-ready-batch.csv", CAMPAIGN_FIELDS, campaign)
    report = weekly_report(audit, snapshot, campaign, companies, contacts)
    (output / "weekly-conversion-report.md").write_text(report, encoding="utf-8", newline="\n")
    manifest = {
        "ok": True,
        "mode": "draft-only",
        "source": str(source),
        "source_reconciled": write_source,
        "reconciliation_changes": changes,
        "audit": audit,
        "campaign_rows": len(campaign),
        "priority_campaign_rows": sum(1 for item in campaign if item["wave"] == "priority"),
        "test_campaign_rows": sum(1 for item in campaign if item["wave"] == "test"),
        "hubspot_company_import_rows": len(companies),
        "hubspot_contact_import_rows": len(contacts),
        "external_actions_executed": 0,
    }
    (output / "build-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build BridgeWorks draft-only prospecting operating artifacts.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write-source", action="store_true")
    args = parser.parse_args()
    try:
        result = run(
            args.source.resolve(),
            args.snapshot.resolve(),
            args.packet.resolve(),
            args.output.resolve(),
            args.write_source,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
