#!/usr/bin/env python3
"""Reconcile every local prospect store into one canonical view. Read-only.

HOW TO USE
    python operations/internal-gtm/adapters/prospect_reconcile.py \
        --as-of 2026-08-11 --out operations/internal-gtm/migration/phase-3/prospect-reconciliation.json

Sources, in the order their fields win a conflict:

  1. Live Gmail receipt     communication ground truth. If Gmail says a message
                            was sent, it was sent, whatever any CSV says.
  2. Mission Control        current approval state and exact payload digest.
  3. Live HubSpot receipt   CRM object identity, never prospect truth by itself.
  4. Local Gmail send log   older communication ground truth.
  5. Acquisition engine     current research state and results.
  6. Canonical register     legacy generated view.
  7. Lead Engine v1         legacy prospect batches.
  8. pipeline/prospecting   older tracker.

Conflict rules, enforced in code:

  - Evidence never silently upgrades. A field only moves to a higher-authority
    value, and the change is recorded with both values and the source.
  - Two sources asserting different values at the same authority stay
    `contradicted`. Neither is chosen.
  - Stale stays stale until reverified. An old `checked_at` is not refreshed by
    copying a newer row from a different store.
  - No field is written without provenance. Every value carries where it came from.

This writes a report. It merges nothing.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
ENGINE = REPO_ROOT / "operations" / "client-acquisition-engine"
OPS = ENGINE / "research" / "prospect-operations"
LEAD_ENGINE = REPO_ROOT / "operations" / "lead-engine-v1"
PIPELINE = REPO_ROOT / "pipeline" / "prospecting"
PHASE3 = GTM_ROOT / "migration" / "phase-3"
MISSION_CONTROL = REPO_ROOT.parent / "emmanuel-os-context" / "00-command-center" / "mission-control"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import gtm_core as core  # noqa: E402

# Lower number wins a conflict. Gmail is communication ground truth.
AUTHORITY = {
    "gmail_live": 0,
    "mission_control_approval": 1,
    "hubspot_live": 1,
    "gmail_send_log": 2,
    "acquisition_engine_results": 3,
    "acquisition_engine_source": 4,
    "canonical_register": 5,
    "lead_engine_v1": 6,
    "pipeline_prospecting": 7,
}

STALENESS_DAYS = core.DEFAULT_STALENESS_DAYS


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def collect() -> list[dict]:
    """Every prospect row from every local store, tagged with its source."""
    records: list[dict] = []

    # Immutable receipt created from a read-only Gmail query. A canonical domain
    # is mandatory here so communication truth joins the business record instead
    # of becoming an orphaned company-name bucket.
    gmail_live = _read_json(PHASE3 / "gmail-contact-history-2026-08-11.json", {})
    live_gmail_companies = {
        core.normalize_company(entry.get("company") or "")
        for entry in gmail_live.get("records", [])
    }
    for entry in gmail_live.get("records", []):
        domain = core.normalize_domain(entry.get("canonical_domain", ""))
        sent_ids = entry.get("sent_message_ids") or []
        thread_ids = entry.get("gmail_thread_ids") or []
        records.append({
            "company": entry.get("company"), "source": "gmail_live",
            "website_url": f"https://{domain}" if domain else "",
            "buyer_email": entry.get("destination"),
            "contacted": bool(sent_ids),
            "sent_at": entry.get("latest_sent_at"),
            "sent_message_id": sent_ids[0] if sent_ids else None,
            "sent_message_ids": sent_ids,
            "gmail_thread_id": thread_ids[0] if thread_ids else None,
            "gmail_thread_ids": thread_ids,
            "draft_message_ids": entry.get("draft_message_ids") or [],
            "communication_checked_at": gmail_live.get("checked_at"),
            "reply_state": entry.get("reply_state"),
        })

    # Mission Control is authoritative only for the approval task. Resolve its
    # business domain from the acquisition source first, then the exact approved
    # destination. A non-email destination is not promoted to buyer_email.
    source_rows = _rows(OPS / "prospect-source-current.csv")
    source_by_company = {
        core.normalize_company(row.get("company") or ""): row for row in source_rows
        if core.normalize_company(row.get("company") or "")
    }
    queue = _read_json(MISSION_CONTROL / "orchestrator-queue.json", [])
    for task in queue if isinstance(queue, list) else []:
        if task.get("status") != "awaiting_approval" or task.get("lane") != "acquisition":
            continue
        payload = task.get("payload") or {}
        company = payload.get("company") or task.get("title")
        source_row = source_by_company.get(core.normalize_company(company or ""), {})
        destination = payload.get("destination") or ""
        website = source_row.get("website") or source_row.get("canonical_domain") or ""
        if not website:
            website = destination if "://" in destination else (
                f"https://{destination.rsplit('@', 1)[-1]}" if "@" in destination else "")
        records.append({
            "company": company, "source": "mission_control_approval",
            "prospect_id": payload.get("prospect_id"),
            "website_url": website,
            "buyer_email": destination if "@" in destination else None,
            "approval_state": task.get("status"),
            "approval_task_id": task.get("id"),
            "approval_payload_digest": task.get("payload_digest"),
            "approval_dedupe_key": task.get("dedupe_key"),
            "approval_updated_at": task.get("updated_at"),
        })

    # HubSpot is read-only in Phase 3. Its object ID is imported only where an
    # exact domain query returned one record; absence is evidence, not deletion.
    hubspot = _read_json(PHASE3 / "hubspot-company-evidence-2026-08-11.json", {})
    for entry in hubspot.get("records", []):
        matches = entry.get("matches") or []
        for match in matches:
            domain = core.normalize_domain(entry.get("domain", ""))
            records.append({
                "company": match.get("name") or domain, "source": "hubspot_live",
                "website_url": match.get("website") or (f"https://{domain}" if domain else ""),
                "hubspot_id": str(match.get("id")) if match.get("id") is not None else None,
                "hubspot_checked_at": hubspot.get("checked_at"),
            })

    send_log = _read_json(LEAD_ENGINE / "03-outreach-drafts" / "outreach-send-log-2026-06-23.json", {})
    for company, entry in sorted(send_log.items()):
        if core.normalize_company(company) in live_gmail_companies:
            continue
        records.append({
            "company": company, "source": "gmail_send_log",
            "contacted": True,
            "sent_at": entry.get("time"),
            "sent_message_id": entry.get("sent_msg"),
            "gmail_thread_id": entry.get("thread"),
        })

    for path in sorted((OPS / "results").glob("*.json")):
        for record in _read_json(path, {}).get("prospects", []):
            domain = ""
            for source in record.get("sources", []):
                domain = core.normalize_domain(source.get("url", "")) or domain
                if domain:
                    break
            records.append({
                "company": record.get("company"), "source": "acquisition_engine_results",
                "prospect_id": record.get("prospect_id"),
                "website_url": f"https://{domain}" if domain else "",
                "checked_at": (record.get("checked_at") or "")[:10] or None,
                "engine_readiness": record.get("outreach_readiness"),
                "engine_status": record.get("status"),
                "buyer_email": record.get("proposed_destination")
                if "@" in (record.get("proposed_destination") or "") else None,
            })

    for row in source_rows:
        records.append({"company": row.get("company"), "source": "acquisition_engine_source",
                        "website_url": row.get("website") or row.get("domain") or "",
                        "lane": row.get("lane"), "row_status": row.get("status")})

    for row in _rows(OPS / "operating-output" / "canonical-prospect-register.csv"):
        touched = {c: row.get(c) for c in
                   ("first_contact_sent", "follow_up_1_sent", "follow_up_2_sent", "linkedin_touch")
                   if (row.get(c) or "").strip()}
        records.append({
            "company": row.get("company"), "source": "canonical_register",
            "prospect_id": row.get("prospect_id"),
            "website_url": row.get("website") or "",
            "buyer_email": (row.get("email") or "").strip() or None,
            "contacted": bool(touched) or None,
            "contact_evidence": touched or None,
            "hubspot_id": (row.get("hubspot_id") or "").strip() or None,
            "row_status": row.get("status"),
        })

    for name in ("prospect-batch-2026-07-14.csv", "prospect-tracker.csv", "adjacent-lane-watchlist.csv"):
        for row in _rows(LEAD_ENGINE / "01-prospects" / name):
            records.append({"company": row.get("company") or row.get("Company"),
                            "source": "lead_engine_v1",
                            "website_url": row.get("website") or row.get("Website") or "",
                            "row_status": row.get("status") or row.get("Status")})

    for row in _rows(PIPELINE / "prospect-tracker.csv"):
        records.append({"company": row.get("company") or row.get("Company"),
                        "source": "pipeline_prospecting",
                        "website_url": row.get("website") or row.get("Website") or "",
                        "row_status": row.get("status") or row.get("Status")})

    return [r for r in records if (r.get("company") or "").strip() or r.get("website_url")]


def orphan_resolution_receipt() -> list[dict]:
    """Deterministically account for legacy company-only Gmail send records."""
    old = _read_json(LEAD_ENGINE / "03-outreach-drafts" / "outreach-send-log-2026-06-23.json", {})
    live = _read_json(PHASE3 / "gmail-contact-history-2026-08-11.json", {})
    live_by_company = {
        core.normalize_company(row.get("company") or ""): row for row in live.get("records", [])
    }
    local_rows = _rows(OPS / "prospect-source-current.csv") + _rows(
        OPS / "operating-output" / "canonical-prospect-register.csv")
    receipt = []
    for company, old_entry in sorted(old.items()):
        normalized = core.normalize_company(company)
        current = live_by_company.get(normalized)
        historical = sorted({
            core.normalize_domain(row.get("website") or row.get("domain") or row.get("canonical_domain") or "")
            for row in local_rows
            if core.normalize_company(row.get("company") or "") == normalized
            and core.normalize_domain(row.get("website") or row.get("domain") or row.get("canonical_domain") or "")
        })
        canonical = core.normalize_domain((current or {}).get("canonical_domain", ""))
        destination = (current or {}).get("destination") or ""
        recipient_domain = core.normalize_domain(destination.rsplit("@", 1)[-1]) if "@" in destination else ""
        old_message = old_entry.get("sent_msg")
        live_messages = (current or {}).get("sent_message_ids") or []
        deterministic = bool(
            current and canonical and recipient_domain == canonical
            and canonical in historical and old_message in live_messages
        )
        receipt.append({
            "legacy_company": company,
            "legacy_key": f"company:{normalized}",
            "resolution": "confirmed_match" if deterministic else "possible_match",
            "canonical_key": f"domain:{canonical}" if canonical else None,
            "recipient_email": destination or None,
            "recipient_domain": recipient_domain or None,
            "canonical_domain": canonical or None,
            "gmail_message_ids": live_messages or ([old_message] if old_message else []),
            "gmail_thread_ids": (current or {}).get("gmail_thread_ids") or
                                ([old_entry.get("thread")] if old_entry.get("thread") else []),
            "known_buyer_or_contact": destination or None,
            "historical_domains": historical,
            "rule": ("exact normalized company + recipient domain = canonical domain + historical domain "
                     "+ legacy message ID present in live Gmail result"),
        })
    return receipt


MERGE_FIELDS = (
    "website_url", "buyer_email", "contacted", "sent_at", "sent_message_id",
    "sent_message_ids", "gmail_thread_id", "gmail_thread_ids", "draft_message_ids",
    "communication_checked_at", "reply_state", "checked_at", "engine_readiness",
    "engine_status", "hubspot_id", "hubspot_checked_at", "approval_state",
    "approval_task_id", "approval_payload_digest", "approval_dedupe_key",
    "approval_updated_at", "lane", "row_status", "prospect_id",
)


def reconcile(records: list[dict], as_of: str) -> dict:
    buckets: dict[str, list[dict]] = {}
    unkeyed: list[dict] = []
    for record in records:
        key = core.entity_key(record)
        (buckets.setdefault(key, []) if key else unkeyed).append(record)

    entities, conflicts = [], []
    for key in sorted(buckets):
        group = buckets[key]
        fields: dict[str, dict] = {}
        for record in sorted(group, key=lambda r: AUTHORITY[r["source"]]):
            authority = AUTHORITY[record["source"]]
            for name in MERGE_FIELDS:
                value = record.get(name)
                if value in (None, "", [], {}):
                    continue
                held = fields.get(name)
                if held is None:
                    fields[name] = {"value": value, "source": record["source"], "authority": authority}
                elif held["value"] == value:
                    held.setdefault("corroborated_by", []).append(record["source"])
                elif authority < held["authority"]:
                    conflicts.append({"entity_key": key, "field": name,
                                      "kept": {"value": value, "source": record["source"]},
                                      "replaced": {"value": held["value"], "source": held["source"]},
                                      "rule": "higher authority wins, both recorded"})
                    fields[name] = {"value": value, "source": record["source"], "authority": authority,
                                    "superseded": held}
                elif authority == held["authority"]:
                    held["status"] = "contradicted"
                    held.setdefault("conflicting", []).append(
                        {"value": value, "source": record["source"]})
                    conflicts.append({"entity_key": key, "field": name,
                                      "values": [held["value"], value],
                                      "sources": [held["source"], record["source"]],
                                      "rule": "same authority disagreement stays contradicted"})
                else:
                    fields[name] = {**held}
                    fields[name].setdefault("lower_authority_alternatives", []).append(
                        {"value": value, "source": record["source"]})

        checked = (fields.get("checked_at") or {}).get("value")
        age = core._days_between(checked, as_of) if checked else None
        entities.append({
            "entity_key": key,
            "company": next((r["company"] for r in group if r.get("company")), None),
            "normalized_company": core.normalize_company(
                next((r.get("company") or "" for r in group if r.get("company")), "")) or None,
            "sources": sorted({r["source"] for r in group}),
            "source_count": len(group),
            "fields": fields,
            "evidence_age_days": age,
            "evidence_state": ("stale" if age is not None and age > STALENESS_DAYS
                               else "current" if age is not None else "unknown"),
            "contacted": bool((fields.get("contacted") or {}).get("value")),
            "gmail_verified_send": bool((fields.get("sent_message_id") or {}).get("value")),
        })

    # A store with no website column keys by company, a store with one keys by
    # domain. The same business then lands in two buckets. Report the candidates.
    # Never merge them here: a shared normalized name is a lead, not proof.
    by_name: dict[str, list[dict]] = {}
    for entity in entities:
        if entity["normalized_company"]:
            by_name.setdefault(entity["normalized_company"], []).append(entity)
    cross_key_candidates = []
    for name, group in sorted(by_name.items()):
        kinds = {e["entity_key"].split(":", 1)[0] for e in group}
        if len(group) > 1 and len(kinds) > 1:
            cross_key_candidates.append({
                "normalized_company": name,
                "entity_keys": sorted(e["entity_key"] for e in group),
                "sources": sorted({s for e in group for s in e["sources"]}),
                "holds_gmail_send": any(e["gmail_verified_send"] for e in group),
                "resolution": "verify the domain by hand, then re-key the company-only record",
            })

    by_source: dict[str, int] = {}
    for record in records:
        by_source[record["source"]] = by_source.get(record["source"], 0) + 1

    orphan_receipt = orphan_resolution_receipt()
    return {
        "as_of": as_of,
        "authority_order": AUTHORITY,
        "input_rows": len(records),
        "input_rows_by_source": by_source,
        "unique_entities": len(entities),
        "unkeyed_rows": len(unkeyed),
        "entities_in_more_than_one_store": sum(1 for e in entities if len(e["sources"]) > 1),
        "contacted_entities": sum(1 for e in entities if e["contacted"]),
        "gmail_verified_sends": sum(1 for e in entities if e["gmail_verified_send"]),
        "gmail_sent_message_count": sum(
            len((e["fields"].get("sent_message_ids") or {}).get("value") or []) for e in entities),
        "hubspot_linked_entities": sum(1 for e in entities if (e["fields"].get("hubspot_id") or {}).get("value")),
        "awaiting_approval_entities": sum(
            1 for e in entities
            if (e["fields"].get("approval_state") or {}).get("value") == "awaiting_approval"),
        "stale_entities": sum(1 for e in entities if e["evidence_state"] == "stale"),
        "cross_key_candidates": cross_key_candidates,
        "cross_key_candidate_count": len(cross_key_candidates),
        "orphaned_gmail_sends": [c for c in cross_key_candidates if c["holds_gmail_send"]],
        "resolved_orphaned_gmail_sends": orphan_receipt,
        "resolved_orphaned_gmail_send_count": sum(
            1 for item in orphan_receipt if item["resolution"] == "confirmed_match"),
        "possible_orphaned_gmail_send_matches": [
            item for item in orphan_receipt if item["resolution"] == "possible_match"],
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "entities": entities,
        "writes_performed": 0,
        "note": "This is a canonical read-only state snapshot. No source store, CRM record, queue task or mailbox item was merged, written or overwritten.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = reconcile(collect(), args.as_of)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    for key in ("input_rows", "unique_entities", "entities_in_more_than_one_store", "unkeyed_rows",
                "contacted_entities", "gmail_verified_sends", "gmail_sent_message_count",
                "hubspot_linked_entities", "awaiting_approval_entities",
                "stale_entities", "conflict_count",
                "cross_key_candidate_count"):
        print(f"  {report[key]:6}  {key}")
    print(f"  rows by source: {report['input_rows_by_source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
