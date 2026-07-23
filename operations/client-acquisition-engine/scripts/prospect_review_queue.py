from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ENGINE_ROOT / "research" / "prospect-operations" / "review"
PACKET_ROOT = REVIEW_ROOT / "packets"
STATE_PATH = REVIEW_ROOT / "prospect-review-state.json"
EVENTS_PATH = REVIEW_ROOT / "prospect-review-events.jsonl"

SUPPORTED_CHANNELS = {
    "email": "email.send",
    "linkedin": "linkedin.message",
    "contact_form": "contact_form.submit",
}
READINESS_VALUES = {"ready", "hold", "needs_more_evidence"}
POLICY_VERSION = 2


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


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


def append_event(event_type: str, detail: dict[str, Any]) -> None:
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    record = {"at": now_iso(), "type": event_type, "detail": detail}
    with EVENTS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_text(value: Any, limit: int = 4000) -> str:
    return str(value or "").strip()[:limit]


def default_state() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "updated_at": "",
        "batches": {},
        "items": {},
    }


def load_state() -> dict[str, Any]:
    state = read_json(STATE_PATH, default_state())
    if not isinstance(state, dict):
        state = default_state()
    state.setdefault("batches", {})
    state.setdefault("items", {})
    return state


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    atomic_write(STATE_PATH, state)


def source_lines(record: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for source in record.get("sources", []):
        if not isinstance(source, dict):
            continue
        url = clean_text(source.get("url"), 2000)
        accessed = clean_text(source.get("accessed_at"), 80)
        supports = clean_text(source.get("supports"), 1000)
        if url:
            lines.append(f"- {url} (accessed {accessed or 'not recorded'}): {supports or 'support not recorded'}")
    return lines


def classify(record: dict[str, Any]) -> tuple[str, str]:
    research_status = clean_text(record.get("status"), 80)
    if research_status != "verified":
        return research_status or "invalid", clean_text(record.get("evidence_notes"), 1000)

    readiness = clean_text(record.get("outreach_readiness"), 80)
    if readiness == "ready":
        missing = []
        for field in [
            "commercial_gap",
            "proof_to_use",
            "proposed_channel",
            "proposed_destination",
            "draft_body",
        ]:
            if not clean_text(record.get(field)):
                missing.append(field)
        channel = clean_text(record.get("proposed_channel"), 80)
        if channel not in SUPPORTED_CHANNELS:
            missing.append("supported proposed_channel")
        if channel == "email" and not clean_text(record.get("draft_subject")):
            missing.append("draft_subject")
        if missing:
            return "needs_gap_research", f"Outreach-ready contract is incomplete: {', '.join(sorted(set(missing)))}."
        return "awaiting_mobile_approval", "Exact destination and proposed copy passed the local preparation contract."
    if readiness in {"hold", "needs_more_evidence"}:
        return readiness, clean_text(record.get("next_internal_action"), 1000)
    return (
        "needs_gap_research",
        "Research verified the entity and contact route, but did not establish an outreach-ready commercial gap and exact proposed action.",
    )


def external_task(record: dict[str, Any], packet_path: Path, result_path: Path) -> dict[str, Any] | None:
    review_status, _ = classify(record)
    if review_status != "awaiting_mobile_approval":
        return None
    channel = clean_text(record.get("proposed_channel"), 80)
    task_type = SUPPORTED_CHANNELS[channel]
    company = clean_text(record.get("company"), 240)
    destination = clean_text(record.get("proposed_destination"), 1000)
    payload = {
        "prospect_id": clean_text(record.get("prospect_id"), 160),
        "company": company,
        "channel": channel,
        "destination": destination,
        "subject": clean_text(record.get("draft_subject"), 240),
        "body": clean_text(record.get("draft_body"), 4000),
        "commercial_gap": clean_text(record.get("commercial_gap"), 2000),
        "proof_to_use": clean_text(record.get("proof_to_use"), 1000),
        "risk_notes": clean_text(record.get("risk_notes"), 1000),
        "source_urls": [
            clean_text(source.get("url"), 2000)
            for source in record.get("sources", [])
            if isinstance(source, dict) and clean_text(source.get("url"))
        ][:20],
        "packet_path": str(packet_path.resolve()),
        "result_path": str(result_path.resolve()),
        "approval_scope": "Approving authorizes only this exact destination, subject, and body.",
    }
    return {
        "type": task_type,
        "title": f"Approve {channel.replace('_', ' ')} outreach to {company}",
        "payload": payload,
        "dedupe_key": f"prospect-external:{clean_text(record.get('prospect_id'), 160)}:{file_sha256(result_path)[:16]}",
    }


def research_followup(record: dict[str, Any], result_path: Path) -> dict[str, Any] | None:
    review_status, reason = classify(record)
    if review_status != "needs_gap_research":
        return None
    prospect_id = clean_text(record.get("prospect_id"), 160)
    company = clean_text(record.get("company"), 240)
    return {
        "type": "prospect.research",
        "title": f"Establish an outreach-ready gap for {company}",
        "payload": {
            "mode": "gap_completion",
            "batch_id": clean_text(read_json(result_path, {}).get("batch_id"), 160),
            "prospect_id": prospect_id,
            "company": company,
            "result_path": str(result_path.resolve()),
            "current_recommended_angle": clean_text(record.get("recommended_angle"), 2000),
            "current_contact_route": clean_text(record.get("contact_route"), 1000),
            "reason": reason,
            "required_outcome": (
                "Update only this prospect in the existing result JSON with outreach_readiness, "
                "commercial_gap, proof_to_use, proposed_channel, proposed_destination, draft_subject, "
                "draft_body, next_internal_action, and risk_notes. Preserve every source and other prospect."
            ),
        },
        "dedupe_key": f"prospect-gap:{prospect_id}:{file_sha256(result_path)[:16]}",
    }


def render_packet(batch_id: str, result_path: Path, items: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for item in items:
        counts[item["review_status"]] = counts.get(item["review_status"], 0) + 1
    lines = [
        f"# Prospect Review Packet {batch_id}",
        "",
        f"Generated: {now_iso()}",
        f"Research result: `{result_path.resolve()}`",
        "Status: Internal preparation. No message, draft, form, or platform action has been executed.",
        "",
        "## Queue Summary",
        "",
        "| Review state | Count |",
        "|---|---:|",
    ]
    lines.extend([f"| {status} | {count} |" for status, count in sorted(counts.items())])
    lines.extend(
        [
            "",
            "Only `awaiting_mobile_approval` items create an external-action task in Mission Control. Approval is tied to the exact destination and copy shown below.",
            "",
        ]
    )
    for index, item in enumerate(items, start=1):
        record = item["record"]
        lines.extend(
            [
                f"## {index}. {clean_text(record.get('company'), 240)}",
                "",
                f"- Research status: `{clean_text(record.get('status'), 80)}`",
                f"- Review status: `{item['review_status']}`",
                f"- Decision-maker: {clean_text(record.get('decision_maker'), 500) or 'Not verified'}",
                f"- Contact route: {clean_text(record.get('contact_route'), 1000) or 'Not verified'}",
                f"- Commercial gap: {clean_text(record.get('commercial_gap'), 2000) or 'Not established'}",
                f"- Recommended angle: {clean_text(record.get('recommended_angle'), 2000) or 'Not established'}",
                f"- Proof: {clean_text(record.get('proof_to_use'), 1000) or 'Not selected'}",
                f"- Next internal action: {clean_text(record.get('next_internal_action'), 1000) or item['reason'] or 'No action recorded'}",
                f"- Risk notes: {clean_text(record.get('risk_notes'), 1000) or 'None recorded'}",
                "",
                "Evidence:",
                "",
            ]
        )
        lines.extend(source_lines(record) or ["- No source URLs recorded."])
        if item["review_status"] == "awaiting_mobile_approval":
            lines.extend(
                [
                    "",
                    "### Exact Proposed Action",
                    "",
                    f"- Channel: `{clean_text(record.get('proposed_channel'), 80)}`",
                    f"- Destination: `{clean_text(record.get('proposed_destination'), 1000)}`",
                    f"- Subject: {clean_text(record.get('draft_subject'), 240) or 'Not applicable'}",
                    "",
                    clean_text(record.get("draft_body"), 4000),
                    "",
                    "Decision: approve, reject, or leave awaiting approval in private Mission Control.",
                ]
            )
        else:
            lines.extend(
                [
                    "",
                    f"Preparation decision: {item['reason'] or 'Not ready for external action.'}",
                ]
            )
        lines.extend(["", "---", ""])
    lines.extend(
        [
            "## Guardrail",
            "",
            "Creating this packet does not authorize Gmail draft creation, sending, LinkedIn activity, form submission, publishing, CRM writes, paid enrichment, or device URL opening.",
            "",
        ]
    )
    return "\n".join(lines)


def prepare(result_path: Path) -> dict[str, Any]:
    result_path = result_path.resolve()
    result = read_json(result_path, {})
    if not isinstance(result, dict) or not result:
        raise ValueError(f"result JSON is not readable: {result_path}")
    batch_id = clean_text(result.get("batch_id"), 160)
    records = result.get("prospects")
    if not batch_id or not isinstance(records, list):
        raise ValueError("result JSON needs batch_id and a prospects list")

    state = load_state()
    result_hash = file_sha256(result_path)
    prior = state["batches"].get(batch_id, {})
    packet_path = PACKET_ROOT / f"{batch_id}-approval-review.md"
    if (
        prior.get("result_sha256") == result_hash
        and int(prior.get("policy_version", 0)) == POLICY_VERSION
        and packet_path.exists()
    ):
        append_event("review.reused", {"batch_id": batch_id, "result_sha256": result_hash})
        return {
            "ok": True,
            "created": False,
            "batch_id": batch_id,
            "packet_path": str(packet_path),
            "counts": prior.get("counts", {}),
            "external_tasks": prior.get("external_tasks", []),
            "research_followups": prior.get("research_followups", []),
        }

    items: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        review_status, reason = classify(record)
        counts[review_status] = counts.get(review_status, 0) + 1
        item = {"review_status": review_status, "reason": reason, "record": record}
        items.append(item)
        item_key = f"{batch_id}:{clean_text(record.get('prospect_id'), 160)}"
        state["items"][item_key] = {
            "batch_id": batch_id,
            "prospect_id": clean_text(record.get("prospect_id"), 160),
            "company": clean_text(record.get("company"), 240),
            "research_status": clean_text(record.get("status"), 80),
            "review_status": review_status,
            "reason": reason,
            "result_path": str(result_path),
            "updated_at": now_iso(),
        }

    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(render_packet(batch_id, result_path, items), encoding="utf-8", newline="\n")
    external_tasks = [
        task
        for item in items
        if (task := external_task(item["record"], packet_path, result_path)) is not None
    ]
    research_followups = [
        task
        for item in items
        if (task := research_followup(item["record"], result_path)) is not None
    ]
    state["batches"][batch_id] = {
        "batch_id": batch_id,
        "result_path": str(result_path),
        "result_sha256": result_hash,
        "packet_path": str(packet_path),
        "counts": counts,
        "external_tasks": external_tasks,
        "research_followups": research_followups,
        "policy_version": POLICY_VERSION,
        "prepared_at": now_iso(),
    }
    save_state(state)
    append_event(
        "review.prepared",
        {
            "batch_id": batch_id,
            "packet_path": str(packet_path),
            "counts": counts,
            "external_task_count": len(external_tasks),
            "research_followup_count": len(research_followups),
        },
    )
    return {
        "ok": True,
        "created": True,
        "batch_id": batch_id,
        "packet_path": str(packet_path),
        "counts": counts,
        "external_tasks": external_tasks,
        "research_followups": research_followups,
    }


def validate_gap_completion(result_path: Path, prospect_id: str) -> dict[str, Any]:
    result_path = result_path.resolve()
    result = read_json(result_path, {})
    records = result.get("prospects", []) if isinstance(result, dict) else []
    record = next(
        (
            item
            for item in records
            if isinstance(item, dict) and clean_text(item.get("prospect_id"), 160) == prospect_id
        ),
        None,
    )
    if record is None:
        return {"ok": False, "error": f"prospect_id not found in result: {prospect_id}"}
    review_status, reason = classify(record)
    if review_status == "needs_gap_research":
        return {
            "ok": False,
            "prospect_id": prospect_id,
            "review_status": review_status,
            "error": reason,
        }
    return {
        "ok": True,
        "prospect_id": prospect_id,
        "company": clean_text(record.get("company"), 240),
        "review_status": review_status,
        "outreach_readiness": clean_text(record.get("outreach_readiness"), 80),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare approval-gated prospect review packets.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--results", type=Path, required=True)
    prepare_parser.add_argument("--summary-only", action="store_true")
    validate_parser = subparsers.add_parser("validate-gap")
    validate_parser.add_argument("--results", type=Path, required=True)
    validate_parser.add_argument("--prospect-id", required=True)
    args = parser.parse_args()

    try:
        if args.command == "prepare":
            payload = prepare(args.results)
        else:
            payload = validate_gap_completion(args.results, args.prospect_id)
    except (OSError, ValueError) as exc:
        payload = {"ok": False, "error": str(exc)}
    if args.command == "prepare" and args.summary_only and payload.get("ok"):
        payload = {
            "ok": True,
            "created": payload.get("created", False),
            "batch_id": payload.get("batch_id", ""),
            "packet_path": payload.get("packet_path", ""),
            "counts": payload.get("counts", {}),
            "external_tasks": payload.get("external_tasks", []),
            "research_followups": payload.get("research_followups", []),
        }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
