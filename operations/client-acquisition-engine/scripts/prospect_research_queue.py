from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENGINE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ENGINE_ROOT.parents[1]
SOURCE_CSV = WORKSPACE_ROOT / "operations" / "lead-engine-v1" / "01-prospects" / "prospect-batch-2026-07-14.csv"
RESEARCH_ROOT = ENGINE_ROOT / "research" / "prospect-operations"
STATE_PATH = RESEARCH_ROOT / "prospect-research-state.json"
EVENTS_PATH = RESEARCH_ROOT / "prospect-research-events.jsonl"
BATCH_ROOT = RESEARCH_ROOT / "batches"

ACTIVE_LANE_PREFIX = "Lane A Budapest credibility-first SMEs"
ELIGIBLE_STATUSES = {"research", "research-high-scale", "scan-drafted-awaiting-approval"}
RESULT_STATUSES = {"verified", "needs_more_evidence", "rejected", "held"}
OUTREACH_READINESS = {"ready", "hold", "needs_more_evidence"}
OUTREACH_CHANNELS = {"email", "linkedin", "contact_form"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "prospect"


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(raw_path, path)
    finally:
        try:
            os.unlink(raw_path)
        except FileNotFoundError:
            pass


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def append_event(event_type: str, detail: dict[str, Any]) -> None:
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    record = {"at": now_iso(), "type": event_type, "detail": detail}
    with EVENTS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_rows() -> list[dict[str, str]]:
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [{str(key): str(value or "").strip() for key, value in row.items()} for row in rows]


def source_hash() -> str:
    return hashlib.sha256(SOURCE_CSV.read_bytes()).hexdigest()


def default_state() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source_csv": str(SOURCE_CSV),
        "source_sha256": "",
        "updated_at": "",
        "prospects": {},
        "batches": [],
    }


def load_state() -> dict[str, Any]:
    state = read_json(STATE_PATH, default_state())
    if not isinstance(state, dict):
        state = default_state()
    state.setdefault("prospects", {})
    state.setdefault("batches", [])
    return state


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    state["source_sha256"] = source_hash()
    atomic_write(STATE_PATH, state)


def rank_row(row: dict[str, str]) -> tuple[int, str]:
    score = {
        "scan-drafted-awaiting-approval": 120,
        "research": 70,
        "research-high-scale": 35,
    }.get(row.get("status", ""), 0)
    text = " ".join(
        [
            row.get("sector", ""),
            row.get("trigger_observation", ""),
            row.get("next_action", ""),
            row.get("notes", ""),
        ]
    ).lower()
    if "property" in text or "facility" in text:
        score += 20
    if "cleaning" in text:
        score += 15
    if "dental" in text or "clinic" in text:
        score += 10
    for phrase, penalty in [
        ("benchmark only", 35),
        ("watchlist only", 35),
        ("later lane", 25),
        ("high-scale", 20),
    ]:
        if phrase in text:
            score -= penalty
    return score, row.get("company", "").lower()


def eligible_rows(rows: list[dict[str, str]], state: dict[str, Any]) -> list[dict[str, str]]:
    prospects = state.get("prospects", {})
    eligible: list[dict[str, str]] = []
    for row in rows:
        if not row.get("lane", "").startswith(ACTIVE_LANE_PREFIX):
            continue
        if row.get("status") not in ELIGIBLE_STATUSES:
            continue
        next_action = row.get("next_action", "").lower()
        if next_action.startswith("later") or "later lane" in next_action or "watchlist only" in next_action:
            continue
        key = slugify(row.get("company", ""))
        prior = prospects.get(key, {})
        research_status = str(prior.get("research_status", "unassigned"))
        if research_status in {"in_research", "researched", "rejected", "held"}:
            continue
        if research_status == "needs_more_evidence" and int(prior.get("research_attempts", 0)) >= 2:
            continue
        eligible.append(row)
    return sorted(eligible, key=lambda row: (-rank_row(row)[0], rank_row(row)[1]))


def open_batch_for_date(state: dict[str, Any], date: str) -> dict[str, Any] | None:
    for batch in reversed(state.get("batches", [])):
        if batch.get("date") == date and batch.get("status") in {"prepared", "in_research"}:
            payload = read_json(Path(str(batch.get("json_path", ""))), {})
            if isinstance(payload, dict) and payload:
                return payload
    return None


def research_checklist(row: dict[str, str]) -> list[str]:
    checklist = [
        "Confirm the canonical owned domain or record that none was located.",
        "Verify the current primary conversion, booking, enquiry, or WhatsApp route.",
        "Verify a decision-maker or responsible role from a public source.",
        "Verify one usable contact route without creating a draft or sending a message.",
        "Capture two specific, current observations with source URLs and access dates.",
        "Confirm or revise the BridgeWorks angle using only observed evidence.",
        "State whether outreach is ready, held, or needs more evidence.",
        "If outreach is ready, identify one sourced commercial gap, exact channel and destination, selected proof, and concise proposed copy.",
        "Check the tracker and approval packets for duplicate-contact risk.",
    ]
    sector = row.get("sector", "").lower()
    if "clinic" in sector or "dental" in sector:
        checklist.append("Do not make claims about clinical quality, outcomes, or patient safety.")
    return checklist


def render_batch_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Prospect Research Batch {payload['batch_id']}",
        "",
        f"Prepared: {payload['prepared_at']}",
        f"Source: `{payload['source_csv']}`",
        "",
        "## Operating Boundary",
        "",
        "Research and internal preparation only. Do not send, message, submit, publish, create a Gmail draft, or open a prospect URL on a mobile device.",
        "",
        "Treat every source claim as time-sensitive. Record URLs and access dates. If evidence conflicts, mark the item `needs_more_evidence`.",
        "",
    ]
    for index, item in enumerate(payload["prospects"], start=1):
        lines.extend(
            [
                f"## {index}. {item['company']}",
                "",
                f"- Market: {item['city']}, {item['country']}",
                f"- Sector: {item['sector']}",
                f"- Current tracker state: `{item['source_status']}`",
                f"- Current website field: {item['website'] or 'Not recorded'}",
                f"- Existing signal: {item['trigger_observation'] or 'Not recorded'}",
                f"- Existing angle: {item['proof_to_use'] or 'Not recorded'}",
                f"- Next action: {item['next_action'] or 'Not recorded'}",
                "",
                "Checklist:",
                "",
            ]
        )
        lines.extend([f"- [ ] {step}" for step in item["checklist"]])
        lines.extend(["", "---", ""])
    lines.extend(
        [
            "## Completion Contract",
            "",
            "Write one JSON result per prospect using the companion batch JSON fields. Every factual observation must point to a source URL. Run the queue script's `complete` command only after the result file passes validation.",
            "",
        ]
    )
    return "\n".join(lines)


def prepare(limit: int, date: str) -> dict[str, Any]:
    state = load_state()
    existing = open_batch_for_date(state, date)
    if existing:
        append_event("batch.reused", {"batch_id": existing.get("batch_id"), "date": date})
        return {"ok": True, "created": False, "batch": existing}

    selected = eligible_rows(load_rows(), state)[: max(1, min(limit, 10))]
    if not selected:
        append_event("batch.empty", {"date": date, "reason": "no eligible active-lane prospects"})
        return {"ok": True, "created": False, "batch": None, "reason": "no eligible active-lane prospects"}

    batch_number = 1 + sum(1 for item in state.get("batches", []) if item.get("date") == date)
    batch_id = f"{date}-batch-{batch_number:02d}"
    prospects = []
    for row in selected:
        item = {
            "prospect_id": slugify(row.get("company", "")),
            "company": row.get("company", ""),
            "city": row.get("city", ""),
            "country": row.get("country", ""),
            "sector": row.get("sector", ""),
            "source_status": row.get("status", ""),
            "website": row.get("website", ""),
            "contact_name": row.get("contact_name", ""),
            "contact_role": row.get("contact_role", ""),
            "contact_url": row.get("contact_url", ""),
            "trigger_observation": row.get("trigger_observation", ""),
            "proof_to_use": row.get("proof_to_use", ""),
            "next_action": row.get("next_action", ""),
            "notes": row.get("notes", ""),
            "checklist": research_checklist(row),
        }
        prospects.append(item)
        prior_attempts = int(state["prospects"].get(item["prospect_id"], {}).get("research_attempts", 0))
        state["prospects"][item["prospect_id"]] = {
            "company": item["company"],
            "research_status": "in_research",
            "research_attempts": prior_attempts + 1,
            "batch_id": batch_id,
            "updated_at": now_iso(),
        }

    json_path = BATCH_ROOT / f"{batch_id}.json"
    markdown_path = BATCH_ROOT / f"{batch_id}.md"
    payload = {
        "schema_version": 2,
        "batch_id": batch_id,
        "date": date,
        "prepared_at": now_iso(),
        "status": "prepared",
        "source_csv": str(SOURCE_CSV),
        "source_sha256": source_hash(),
        "limits": {
            "max_prospects": len(prospects),
            "external_actions_allowed": False,
            "paid_enrichment_allowed": False,
        },
        "required_result_fields": [
            "prospect_id",
            "company",
            "checked_at",
            "status",
            "sources",
            "owned_domain",
            "conversion_route",
            "decision_maker",
            "contact_route",
            "observations",
            "recommended_angle",
            "evidence_notes",
            "outreach_readiness",
            "commercial_gap",
            "proof_to_use",
            "proposed_channel",
            "proposed_destination",
            "draft_subject",
            "draft_body",
            "next_internal_action",
            "risk_notes",
        ],
        "prospects": prospects,
    }
    atomic_write(json_path, payload)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_batch_markdown(payload), encoding="utf-8", newline="\n")
    state["batches"].append(
        {
            "batch_id": batch_id,
            "date": date,
            "status": "prepared",
            "prepared_at": payload["prepared_at"],
            "json_path": str(json_path),
            "markdown_path": str(markdown_path),
            "result_path": "",
            "prospect_count": len(prospects),
        }
    )
    save_state(state)
    append_event("batch.prepared", {"batch_id": batch_id, "prospects": [item["company"] for item in prospects]})
    return {
        "ok": True,
        "created": True,
        "batch": payload,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def validate_result(batch: dict[str, Any], result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {item["prospect_id"]: item["company"] for item in batch.get("prospects", [])}
    records = result.get("prospects", [])
    if result.get("batch_id") != batch.get("batch_id"):
        errors.append("result batch_id does not match the batch")
    if not isinstance(records, list):
        return errors + ["prospects must be a list"]
    seen: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"prospects[{index}] must be an object")
            continue
        prospect_id = str(record.get("prospect_id", ""))
        seen.add(prospect_id)
        if prospect_id not in expected:
            errors.append(f"prospects[{index}] has unknown prospect_id {prospect_id!r}")
        if record.get("company") != expected.get(prospect_id):
            errors.append(f"prospects[{index}] company does not match the batch")
        if record.get("status") not in RESULT_STATUSES:
            errors.append(f"prospects[{index}] status must be one of {sorted(RESULT_STATUSES)}")
        sources = record.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"prospects[{index}] must include at least one source")
        else:
            for source_index, source in enumerate(sources):
                if not isinstance(source, dict) or not str(source.get("url", "")).startswith(("http://", "https://")):
                    errors.append(f"prospects[{index}].sources[{source_index}] needs an http(s) URL")
                if not isinstance(source, dict) or not source.get("accessed_at"):
                    errors.append(f"prospects[{index}].sources[{source_index}] needs accessed_at")
        observations = record.get("observations")
        if record.get("status") == "verified" and (not isinstance(observations, list) or len(observations) < 2):
            errors.append(f"prospects[{index}] verified result needs at least two observations")
        for field in [
            "checked_at",
            "owned_domain",
            "conversion_route",
            "decision_maker",
            "contact_route",
            "recommended_angle",
            "evidence_notes",
        ]:
            if field not in record:
                errors.append(f"prospects[{index}] is missing {field}")
        if int(batch.get("schema_version", 1)) >= 2:
            for field in [
                "outreach_readiness",
                "commercial_gap",
                "proof_to_use",
                "proposed_channel",
                "proposed_destination",
                "draft_subject",
                "draft_body",
                "next_internal_action",
                "risk_notes",
            ]:
                if field not in record:
                    errors.append(f"prospects[{index}] is missing {field}")
            readiness = str(record.get("outreach_readiness", ""))
            if readiness not in OUTREACH_READINESS:
                errors.append(f"prospects[{index}] outreach_readiness must be one of {sorted(OUTREACH_READINESS)}")
            if record.get("status") != "verified" and readiness == "ready":
                errors.append(f"prospects[{index}] cannot be outreach-ready unless research status is verified")
            if record.get("status") == "verified" and readiness == "ready":
                channel = str(record.get("proposed_channel", ""))
                if channel not in OUTREACH_CHANNELS:
                    errors.append(f"prospects[{index}] proposed_channel must be one of {sorted(OUTREACH_CHANNELS)}")
                for field in ["commercial_gap", "proof_to_use", "proposed_destination", "draft_body"]:
                    if not str(record.get(field, "")).strip():
                        errors.append(f"prospects[{index}] outreach-ready result needs {field}")
                if channel == "email":
                    destination = str(record.get("proposed_destination", "")).strip()
                    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", destination):
                        errors.append(f"prospects[{index}] email destination is invalid")
                    if not str(record.get("draft_subject", "")).strip():
                        errors.append(f"prospects[{index}] email outreach needs draft_subject")
                body_words = len(str(record.get("draft_body", "")).split())
                if body_words < 25 or body_words > 180:
                    errors.append(f"prospects[{index}] draft_body must contain 25 to 180 words")
            if readiness != "ready" and not str(record.get("next_internal_action", "")).strip():
                errors.append(f"prospects[{index}] non-ready result needs next_internal_action")
    missing = sorted(set(expected) - seen)
    if missing:
        errors.append(f"result is missing prospects: {', '.join(missing)}")
    return errors


def complete(batch_path: Path, result_path: Path) -> dict[str, Any]:
    batch = read_json(batch_path, {})
    result = read_json(result_path, {})
    if not isinstance(batch, dict) or not batch:
        raise ValueError(f"batch JSON is not readable: {batch_path}")
    if not isinstance(result, dict) or not result:
        raise ValueError(f"result JSON is not readable: {result_path}")
    errors = validate_result(batch, result)
    if errors:
        return {"ok": False, "errors": errors}

    state = load_state()
    status_by_id = {item["prospect_id"]: item["status"] for item in result["prospects"]}
    for prospect_id, result_status in status_by_id.items():
        record = state["prospects"].setdefault(prospect_id, {})
        record["research_status"] = "researched" if result_status == "verified" else result_status
        record["result_status"] = result_status
        result_record = next(item for item in result["prospects"] if item["prospect_id"] == prospect_id)
        record["outreach_readiness"] = str(result_record.get("outreach_readiness", "not_assessed"))
        record["result_path"] = str(result_path.resolve())
        record["updated_at"] = now_iso()
    for batch_record in state.get("batches", []):
        if batch_record.get("batch_id") == batch.get("batch_id"):
            batch_record["status"] = "completed"
            batch_record["completed_at"] = now_iso()
            batch_record["result_path"] = str(result_path.resolve())
    save_state(state)
    append_event(
        "batch.completed",
        {"batch_id": batch.get("batch_id"), "result_path": str(result_path.resolve()), "statuses": status_by_id},
    )
    return {"ok": True, "batch_id": batch.get("batch_id"), "statuses": status_by_id}


def status() -> dict[str, Any]:
    state = load_state()
    counts: dict[str, int] = {}
    for item in state.get("prospects", {}).values():
        key = str(item.get("research_status", "unknown"))
        counts[key] = counts.get(key, 0) + 1
    return {
        "ok": True,
        "source_csv": str(SOURCE_CSV),
        "source_sha256": source_hash(),
        "state_path": str(STATE_PATH),
        "event_path": str(EVENTS_PATH),
        "eligible_active_lane": len(eligible_rows(load_rows(), state)),
        "research_status_counts": counts,
        "batches": state.get("batches", [])[-10:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Durable BridgeWorks prospect research queue.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Prepare the next evidence-first batch.")
    prepare_parser.add_argument("--limit", type=int, default=5)
    prepare_parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    prepare_parser.add_argument("--summary-only", action="store_true")

    complete_parser = subparsers.add_parser("complete", help="Validate and record a completed batch.")
    complete_parser.add_argument("--batch", type=Path, required=True)
    complete_parser.add_argument("--results", type=Path, required=True)

    subparsers.add_parser("status", help="Show queue and batch status.")
    args = parser.parse_args()

    if args.command == "prepare":
        payload = prepare(args.limit, args.date)
        if args.summary_only:
            batch = payload.get("batch") or {}
            payload = {
                "ok": payload.get("ok", False),
                "created": payload.get("created", False),
                "batch_id": batch.get("batch_id", ""),
                "prospect_count": len(batch.get("prospects", [])),
                "prospects": [item.get("company", "") for item in batch.get("prospects", [])],
                "json_path": payload.get("json_path") or str(BATCH_ROOT / f"{batch.get('batch_id', '')}.json"),
                "markdown_path": payload.get("markdown_path") or str(BATCH_ROOT / f"{batch.get('batch_id', '')}.md"),
                "reason": payload.get("reason", ""),
            }
    elif args.command == "complete":
        payload = complete(args.batch, args.results)
    else:
        payload = status()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
