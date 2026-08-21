#!/usr/bin/env python3
"""Adapter: client-acquisition-engine research records -> internal-gtm slice input.

HOW TO USE
    python operations/internal-gtm/adapters/acquisition_engine.py \
        --prospect premier-fm --as-of 2026-08-11
    python operations/internal-gtm/adapters/acquisition_engine.py \
        --prospect premier-fm --classify operations/internal-gtm/adapters/classifications/premier-fm.json

The acquisition engine stores each researched prospect as verified sources plus
free-text observations. Code can lift the identity, buyer, destination, source
URLs and access dates without judgment. It cannot decide which gap category a
sentence describes, so without a classification file this adapter stops and
returns the exact classification call to make. It reads the engine. It never
writes to it.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
ENGINE = REPO_ROOT / "operations" / "client-acquisition-engine"
RESULTS = ENGINE / "research" / "prospect-operations" / "results"
STATE = ENGINE / "research" / "prospect-operations" / "prospect-research-state.json"
REGISTER = ENGINE / "research" / "prospect-operations" / "operating-output" / "canonical-prospect-register.csv"

sys.path.insert(0, str(GTM_ROOT / "scripts"))
import capability_loader as cl  # noqa: E402
import gtm_core as core  # noqa: E402

# Contact columns in the canonical register. Any non-empty value means contacted.
CONTACT_COLUMNS = ("first_contact_sent", "follow_up_1_sent", "follow_up_2_sent", "linkedin_touch")

# Gap categories the router understands, from service-routes.yaml.
VALID_CATEGORIES = {
    category
    for route in cl.load_service_routes()["routes"]
    for category in route["gap_categories"]
}


def find_result(prospect_id: str) -> tuple[dict, Path]:
    """Return the newest research result for this prospect."""
    found: list[tuple[str, dict, Path]] = []
    for path in sorted(RESULTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("prospects", []):
            if record.get("prospect_id") == prospect_id:
                found.append((data.get("completed_at", ""), record, path))
    if not found:
        raise SystemExit(f"no research result for prospect_id {prospect_id}")
    found.sort(key=lambda item: item[0])
    return found[-1][1], found[-1][2]


def register_row(prospect_id: str) -> dict | None:
    if not REGISTER.is_file():
        return None
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("prospect_id") == prospect_id:
                return row
    return None


def contact_history(prospect_id: str) -> dict:
    row = register_row(prospect_id)
    if row is None:
        return {"in_register": False, "contacted": False, "evidence": "absent from canonical register"}
    touched = {column: row.get(column, "") for column in CONTACT_COLUMNS if row.get(column, "").strip()}
    return {
        "in_register": True,
        "register_status": row.get("status"),
        "contacted": bool(touched),
        "evidence": touched or "all contact columns empty",
    }


def _email(record: dict) -> str | None:
    destination = (record.get("proposed_destination") or "").strip()
    if "@" in destination and not destination.startswith("http"):
        return destination
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", record.get("contact_route", "") or "")
    return match.group(0) if match else None


def _buyer_name(record: dict) -> str | None:
    text = (record.get("decision_maker") or "").strip()
    if not text or text.lower().startswith("no current named"):
        return None
    match = re.match(r"([A-Z][\w.'-]+(?: [A-Z][\w.'-]+){1,3})", text)
    return match.group(1) if match else None


def _domain(record: dict) -> str:
    owned = record.get("owned_domain") or ""
    match = re.search(r"([a-z0-9-]+(?:\.[a-z0-9-]+)+)", owned.lower())
    if match:
        return match.group(1)
    for source in record.get("sources", []):
        host = core.normalize_domain(source.get("url", ""))
        if host:
            return host
    return ""


def classification_request(record: dict, prospect_id: str) -> dict:
    """The judgment step this adapter refuses to guess."""
    request = cl.capability_call_request(
        role_id="evidence-auditor",
        capability_id="client-audit",
        task="simple_stage_classification",
        payload={
            "prospect_id": prospect_id,
            "instruction": (
                "For each source index, name the one gap category its `supports` text "
                "evidences, or null if it evidences no gap. Use only the allowed list. "
                "Do not invent a category and do not classify from the company name."
            ),
            "allowed_categories": sorted(VALID_CATEGORIES),
            "sources": [
                {"index": index, "url": source.get("url"), "accessed_at": source.get("accessed_at"),
                 "supports": source.get("supports")}
                for index, source in enumerate(record.get("sources", []))
            ],
            "observations": record.get("observations", []),
            "commercial_gap": record.get("commercial_gap"),
        },
    )
    request["output_schema"] = {
        "gap_severity": "high | medium | low | none",
        "source_categories": {"<index>": "<category or null>"},
        "rationale": "<one sentence per assigned category, quoting the supporting text>",
    }
    return request


def to_slice_input(prospect_id: str, classification: dict | None, as_of: str) -> dict:
    record, result_path = find_result(prospect_id)
    history = contact_history(prospect_id)
    domain = _domain(record)
    buyer_email = _email(record)
    buyer_name = _buyer_name(record)

    payload = {
        "prospect_id": prospect_id,
        "company": record.get("company"),
        "website_url": f"https://{domain}" if domain else "",
        "source": f"client-acquisition-engine:{result_path.name}",
        "buyer": {"name": buyer_name, "role": None, "email": buyer_email},
        "trigger": {
            "type": "research_verification",
            "summary": record.get("recommended_angle"),
            "observed_at": (record.get("checked_at") or "")[:10] or None,
            "source": (record.get("sources") or [{}])[0].get("url"),
        },
        "_provenance": {
            "engine_result": str(result_path.relative_to(REPO_ROOT)),
            "engine_status": record.get("status"),
            "engine_outreach_readiness": record.get("outreach_readiness"),
            "contact_history": history,
            "adapter": "operations/internal-gtm/adapters/acquisition_engine.py",
        },
    }

    if classification is None:
        payload["_blocked_on"] = classification_request(record, prospect_id)
        return payload

    mapping = {str(k): v for k, v in classification["source_categories"].items()}
    unknown = sorted({v for v in mapping.values() if v and v not in VALID_CATEGORIES})
    if unknown:
        raise SystemExit(f"classification uses categories the router does not know: {', '.join(unknown)}")

    findings = []
    for index, source in enumerate(record.get("sources", [])):
        category = mapping.get(str(index))
        if not category:
            continue
        findings.append({
            "id": f"src{index}",
            "category": category,
            # One source, one proposition. See gtm_core.claim_contradiction_key.
            "claim_key": f"{prospect_id}:{category}:source-{index}",
            "severity": classification.get("gap_severity", "none"),
            "claim": source.get("supports"),
            "value": source.get("supports"),
            "source": source.get("url"),
            "observed_at": source.get("accessed_at"),
            "status": "verified",
        })
    payload["diagnostic"] = {
        "capability": classification.get("capability", "client-audit"),
        "run_id": f"acquisition-engine:{result_path.stem}",
        "completed_at": (record.get("checked_at") or "")[:10],
        "score": classification.get("score"),
        "findings": findings,
    }
    payload["_classification_rationale"] = classification.get("rationale")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prospect", required=True)
    parser.add_argument("--classify", type=Path)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    classification = json.loads(args.classify.read_text(encoding="utf-8")) if args.classify else None
    payload = to_slice_input(args.prospect, classification, args.as_of)
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.out}")
        if "_blocked_on" in payload:
            print("blocked: classification required before this can enter the GEO slice")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
