#!/usr/bin/env python3
"""The one canonical definition of a contacted company. Used everywhere.

HOW TO USE
    python operations/internal-gtm/scripts/contacted_companies.py --as-of 2026-08-11
    from contacted_companies import DEFINITION, accounting

DEFINITION
    A `contacted_company` is a canonical prospect entity with at least one verified
    Gmail SENT message whose recipient email or recipient domain is deterministically
    linked to that entity.

Deterministic link means one of these, and nothing else:

    1. the recipient domain equals the entity's canonical domain;
    2. the recipient domain equals one of the entity's alternate domains;
    3. the recipient address equals a contact address already recorded on the entity.

A name that looks similar is not a link. A send that cannot be linked by one of the
three rules is reported as `unmatched`, and a send that matches more than one entity
is reported as `ambiguous`. Neither is forced.

Claude, Codex, the dashboards and the Weekly Sales Review all read this module.
Nothing recomputes the definition locally.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
PHASE3 = GTM_ROOT / "migration" / "phase-3"
RECONCILIATION = PHASE3 / "prospect-reconciliation.json"
GMAIL_RECEIPT = PHASE3 / "gmail-contact-history-2026-08-11.json"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import gtm_core as core  # noqa: E402

DEFINITION = (
    "A contacted_company is a canonical prospect entity with at least one verified "
    "Gmail SENT message whose recipient email or recipient domain is deterministically "
    "linked to that entity, by canonical domain, alternate domain, or an already "
    "recorded contact address. Nothing else counts."
)

LINK_RULES = ("canonical_domain_match", "alternate_domain_match", "recorded_address_match")


def _read(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _entity_domains(entity: dict) -> set[str]:
    fields = entity.get("fields") or {}
    domains = set()
    key = entity.get("entity_key", "")
    if key.startswith("domain:"):
        domains.add(key.split(":", 1)[1])
    for name in ("website_url", "canonical_domain"):
        value = (fields.get(name) or {}).get("value")
        host = core.normalize_domain(value or "")
        if host:
            domains.add(host)
    for alternate in entity.get("alternate_domains", []) or []:
        host = core.normalize_domain(alternate)
        if host:
            domains.add(host)
    return domains


def _entity_addresses(entity: dict) -> set[str]:
    fields = entity.get("fields") or {}
    value = (fields.get("buyer_email") or {}).get("value")
    return {value.strip().lower()} if isinstance(value, str) and "@" in value else set()


def link(send: dict, entities: list[dict]) -> tuple[list[dict], str | None]:
    """Every entity this send deterministically links to, and the rule that matched."""
    destination = (send.get("destination") or "").strip().lower()
    recipient_domain = core.normalize_domain(destination.rsplit("@", 1)[-1]) if "@" in destination else ""
    matches = []
    for entity in entities:
        rule = None
        if recipient_domain and recipient_domain in _entity_domains(entity):
            key = entity.get("entity_key", "")
            rule = ("canonical_domain_match"
                    if key == f"domain:{recipient_domain}" else "alternate_domain_match")
        elif destination and destination in _entity_addresses(entity):
            rule = "recorded_address_match"
        if rule:
            matches.append({"entity_key": entity["entity_key"],
                            "company": entity.get("company"), "rule": rule})
    return matches, (matches[0]["rule"] if len(matches) == 1 else None)


def accounting(as_of: str) -> dict:
    """The four numbers, computed once, from the canonical definition."""
    reconciliation = _read(RECONCILIATION, {})
    receipt = _read(GMAIL_RECEIPT, {})
    entities = reconciliation.get("entities", [])
    sends = receipt.get("records", [])

    contacted: dict[str, dict] = {}
    ambiguous, unmatched = [], []
    sent_message_ids: set[str] = set()

    for send in sends:
        message_ids = send.get("sent_message_ids") or []
        matches, rule = link(send, entities)
        if not message_ids:
            continue
        if len(matches) == 1:
            entry = contacted.setdefault(matches[0]["entity_key"], {
                "entity_key": matches[0]["entity_key"],
                "company": matches[0]["company"] or send.get("company"),
                "link_rule": rule,
                "destinations": [],
                "sent_message_ids": [],
                "gmail_thread_ids": [],
            })
            entry["destinations"] = sorted(set(entry["destinations"]) | {send.get("destination")})
            entry["sent_message_ids"] = sorted(set(entry["sent_message_ids"]) | set(message_ids))
            entry["gmail_thread_ids"] = sorted(
                set(entry["gmail_thread_ids"]) | set(send.get("gmail_thread_ids") or []))
            sent_message_ids.update(message_ids)
        elif len(matches) > 1:
            ambiguous.append({"destination": send.get("destination"), "company": send.get("company"),
                              "sent_message_ids": message_ids, "candidates": matches,
                              "resolution": "left unlinked; more than one entity matched"})
        else:
            unmatched.append({"destination": send.get("destination"), "company": send.get("company"),
                              "sent_message_ids": message_ids,
                              "resolution": "no deterministic link to any canonical entity"})

    return {
        "as_of": as_of,
        "definition": DEFINITION,
        "link_rules": list(LINK_RULES),
        "contacted_company_count": len(contacted),
        "canonical_sent_message_count": len(sent_message_ids),
        "ambiguous_possible_match_count": len(ambiguous),
        "unmatched_sent_message_count": sum(len(u["sent_message_ids"]) for u in unmatched),
        "contacted_companies": [contacted[k] for k in sorted(contacted)],
        "ambiguous_possible_matches": ambiguous,
        "unmatched_sends": unmatched,
        "sources": {
            "canonical_entities": str(RECONCILIATION.relative_to(REPO_ROOT)).replace("\\", "/"),
            "gmail_receipt": str(GMAIL_RECEIPT.relative_to(REPO_ROOT)).replace("\\", "/"),
            "entities_considered": len(entities),
            "gmail_records_considered": len(sends),
        },
        "note": ("One definition, one computation. Do not recompute a contacted count "
                 "anywhere else. Ambiguous links are never forced into a match."),
        "external_action_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = accounting(args.as_of)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    for key in ("contacted_company_count", "canonical_sent_message_count",
                "ambiguous_possible_match_count", "unmatched_sent_message_count"):
        print(f"  {report[key]:4}  {key}")
    for entry in report["contacted_companies"]:
        print(f"    {entry['company']:34s} {entry['link_rule']:24s} "
              f"{len(entry['sent_message_ids'])} sent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
