#!/usr/bin/env python3
"""Produce a per-file Phase 2 inventory without changing the source engine."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
SOURCE = REPO_ROOT / "operations" / "client-acquisition-engine"
OUTPUT = GTM_ROOT / "migration" / "phase-2"


EXACT: dict[str, set[str]] = {
    "canonical prospect data": {
        "SERVICE-LINE-PROSPECT-LIST-2026-08-01.csv",
        "research/prospect-operations/prospect-source-current.csv",
        "research/prospect-operations/prospect-research-state.json",
        "research/prospect-operations/review/prospect-review-state.json",
        "research/prospect-operations/operating-output/canonical-prospect-register.csv",
    },
    "research evidence": {
        "EXPANDED-PROSPECT-VERIFICATION-2026-07-14.md",
        "research/ai-visibility-evidence-dataset-2026-07-14.csv",
        "research/AI-VISIBILITY-METHODOLOGY-V1-2026-07-14.md",
        "research/BRIDGEWORKS-WEBSITE-SOURCE-MAP-2026-07-14.md",
        "research/LANE-A-OBSERVATION-BANK-2026-07-14.md",
        "scans/dental-de-classique-mini-scan-2026-07-14.md",
        "scans/moso-agency-mini-scan-2026-07-14.md",
        "scans/nimaz-aesthetic-mini-scan-2026-07-14.md",
        "runs/2026-08-01-silver-lining-live-test/evidence/homepage.png",
        "runs/2026-08-01-silver-lining-live-test/evidence/contact-page.png",
    },
    "market/ICP logic": {
        "SALES-ACQUISITION-SYSTEM-2026-08-01.md",
        "PROSPECT-FRAMEWORK-RECONCILIATION-2026-08-02.md",
        "PROSPECTING-OUTREACH-OPERATING-SYSTEM-2026-07-26.md",
        "SERVICE-LINE-SALES-CONTENT-2026-08-01.md",
    },
    "trigger discovery": {"MARKET-MONEY-DISCOURSE-OPERATING-BRIEF-2026-08-01.md", "scripts/prospect_source_queue.py"},
    "proof inventory": {
        "ASSET-MANIFEST-2026-07-15.md", "CEEFM-PROOF-INVENTORY-2026-07-14.md",
        "CEEFM-PROOF-MODULES-2026-07-14.md", "AI-VISIBILITY-REPORT-DRAFT-2026.md",
        "AI-VISIBILITY-REPORT-OUTLINE-2026.md", "public-proof/README.md",
        "public-proof/AI-VISIBILITY-REPORT-PUBLIC-ANONYMIZED-2026.md",
        "public-proof/ANONYMIZATION-STANDARD-2026-07-16.md",
        "public-proof/CASE-STUDY-CENTRAL-EUROPEAN-B2B-SERVICES-2026.md",
        "public-proof/PROOF-MODULES-ANONYMIZED-2026.md",
        "public-proof/PUBLICATION-PACKET-ANONYMIZED-2026-07-16.md",
    },
    "qualification": {
        "scripts/prospect_research_queue.py", "runs/2026-08-01-appinio-live-test/01-qualification.yaml",
        "runs/2026-08-02-bridgeworks-dogfood/01-qualification-input.json",
        "runs/2026-08-02-bridgeworks-dogfood/01-qualification.yaml",
    },
    "routing": {
        "PROSPECTING-CAPABILITY-ORCHESTRATION-AUDIT-2026-08-01.md", "SALES-TOOL-EXECUTION-MAP-2026-08-01.md",
        "runs/2026-08-01-appinio-live-test/02-route-plan.yaml", "runs/2026-08-01-appinio-live-test/02-route-validation.json",
        "runs/2026-08-02-bridgeworks-dogfood/02-route-plan.yaml", "runs/2026-08-02-bridgeworks-dogfood/02-route-validation.json",
    },
    "diagnostic selection": {
        "offers/PAID-AI-READINESS-DIAGNOSTIC-OUTLINE-2026-07-15.md", "scans/AI-VISIBILITY-MINI-SCAN-TEMPLATE.md",
        "runs/2026-08-01-appinio-live-test/03-appinio-revenue-system-decision-snapshot.md",
        "runs/2026-08-01-silver-lining-live-test/SILVER-LINING-DEMAND-CONVERSION-AUDIT.md",
    },
    "outreach preparation": {
        "scripts/outreach_engine.py", "scripts/test_outreach_engine.py",
        "sales/DISCOVERY-CALL-BRIEF-TEMPLATE-2026.md", "sales/REPLY-TO-PROPOSAL-PLAYBOOK-2026-07-14.md",
        "templates/SME-DIGITAL-FOUNDATION-PROPOSAL-TEMPLATE-2026.md",
        "research/prospect-operations/operating-output/campaign-ready-batch.csv",
        "research/prospect-operations/operating-output/hubspot-companies-import-preview.csv",
        "research/prospect-operations/operating-output/hubspot-contacts-import-preview.csv",
        "research/prospect-operations/operating-output/immediate-existing-prospect-batch-2026-07-26.md",
        "runs/2026-08-01-appinio-live-test/04-outreach-drafts.md",
        "runs/2026-08-01-appinio-live-test/05-execution-handoff.md",
        "runs/2026-08-02-bridgeworks-dogfood/05-execution-handoff.md",
    },
    "automation/scheduling": {
        "ORCHESTRATOR-RUNBOOK-2026-07-16.md", "orchestrator-schedule.json",
        "scripts/prospect_review_queue.py", "scripts/render_branded_markdown_pdf.py",
        "scripts/stage_anonymized_drive_assets.py", "research/prospect-operations/README.md",
        "research/prospect-operations/prospect-research-events.jsonl",
        "research/prospect-operations/review/prospect-review-events.jsonl",
    },
    "reporting": {
        "CONTENT-CHANNEL-INVENTORY-2026-07-14.md", "CONTENT-PIPELINE-2026-07-14.md",
        "OUTREACH-QUEUE-REASSESSMENT-2026-08-02.md", "README.md",
        "content/WEEK-01-AUTHORITY-QUEUE-2026-07-20.md",
        "research/prospect-operations/operating-output/README.md",
        "research/prospect-operations/operating-output/build-manifest.json",
        "research/prospect-operations/operating-output/weekly-conversion-report.md",
        "runs/2026-08-01-silver-lining-live-test/RUN-REPORT.md",
        "runs/2026-08-02-bridgeworks-dogfood/00-test-contract.md",
        "runs/2026-08-02-bridgeworks-dogfood/03-bridgeworks-prospect-to-proof-control-loop.md",
        "runs/2026-08-02-bridgeworks-dogfood/04-dogfood-findings.md",
        "scorecards/WEEKLY-SCORECARD-TEMPLATE.md",
    },
    "historical artifact": {
        "CURRENT-STATE-AUDIT-2026-07-14.md", "TWO-WEEK-EXECUTION-RUN-SHEET-2026-07-14.md",
        "scorecards/WEEKLY-SCORECARD-2026-07-14.md",
        "research/prospect-operations/live-source-snapshot-2026-07-26.json",
        "runs/BW-AO-20260723-1439-001.md", "runs/BW-AO-20260723-dry-run-002.md",
        "runs/BW-AO-20260724-activation-001.md",
    },
}


def classify(rel: str) -> str:
    if rel.endswith(".pyc") or rel.startswith(("output/", "outputs/", "public-proof/output/")):
        return "generated/transient output"
    if rel.startswith("runs/2026-08-01-appinio-live-test/") and (rel.endswith(".pdf") or "/preview-" in rel):
        return "generated/transient output"
    if rel.startswith("runs/2026-08-01-silver-lining-live-test/") and (rel.endswith(".pdf") or "/pdf-render/" in rel):
        return "generated/transient output"
    if rel.startswith("runs/2026-08-02-bridgeworks-dogfood/") and (rel.endswith(".pdf") or rel.endswith("pdf-text.txt") or "/preview-" in rel):
        return "generated/transient output"
    if rel.startswith("skill-repair-staging/"):
        return "duplicate"
    if rel.startswith("research/prospect-operations/batches/"):
        return "historical artifact"
    if rel.startswith("research/prospect-operations/results/"):
        return "research evidence"
    if rel.startswith("research/prospect-operations/imports/"):
        return "trigger discovery"
    if rel.startswith("research/prospect-operations/review/packets/") or rel.startswith("approvals/"):
        return "approval packet"
    if rel.startswith("research/prospect-operations/operating-output/") and "three-fixes-response-pack" in rel:
        return "outreach preparation"
    for category, paths in EXACT.items():
        if rel in paths:
            return category
    raise RuntimeError(f"unclassified source file: {rel}")


def target_for(rel: str, category: str) -> str:
    if rel.startswith("scripts/") or rel.endswith(".mjs"):
        return "adapters"
    if category == "canonical prospect data":
        return "control" if rel.endswith(("state.json", "review-state.json")) else "acquisition"
    if category in {"market/ICP logic", "trigger discovery"}:
        return "acquisition"
    if category in {"research evidence", "proof inventory"}:
        return "evidence"
    if category in {"qualification", "routing", "diagnostic selection", "outreach preparation"}:
        return "opportunities"
    if category == "approval packet":
        return "approvals"
    if category == "automation/scheduling":
        return "control"
    return "learning"


def disposition_for(category: str) -> str:
    return {
        "canonical prospect data": "IMPORT_RECONCILED",
        "research evidence": "KEEP_SOURCE",
        "market/ICP logic": "KEEP_SOURCE",
        "trigger discovery": "KEEP_SOURCE",
        "proof inventory": "KEEP_SOURCE",
        "qualification": "SUPERSEDED_AFTER_MIGRATION",
        "routing": "SUPERSEDED_AFTER_MIGRATION",
        "diagnostic selection": "IMPORT_RECONCILED",
        "outreach preparation": "SUPERSEDED_AFTER_MIGRATION",
        "approval packet": "IMPORT_RECONCILED",
        "automation/scheduling": "SUPERSEDED_AFTER_MIGRATION",
        "reporting": "KEEP_SOURCE",
        "historical artifact": "LEARNING_ARCHIVE",
        "duplicate": "DUPLICATE_INSTALLED",
        "generated/transient output": "REGENERATE_DERIVATIVE",
    }[category]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    files = []
    excluded_prefix = "outputs/019fbc62-d3a4-77a3-845e-8b0b145befb7/build/node_modules/"
    for path in SOURCE.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(SOURCE).as_posix()
        if rel.startswith(excluded_prefix) or "__pycache__" in path.parts:
            continue
        category = classify(rel)
        files.append({
            "relative_path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "classification": category,
            "target": target_for(rel, category),
            "disposition": disposition_for(category),
            "provenance_rule": "preserve source path, SHA-256, source URL/date fields, and original status",
        })
    files.sort(key=lambda row: row["relative_path"].lower())
    counts = Counter(row["classification"] for row in files)
    expected = {
        "canonical prospect data": 5, "research evidence": 17, "market/ICP logic": 4,
        "trigger discovery": 8, "proof inventory": 11, "qualification": 4, "routing": 6,
        "diagnostic selection": 4, "outreach preparation": 18, "approval packet": 14,
        "automation/scheduling": 8, "reporting": 13, "historical artifact": 25,
        "duplicate": 19, "generated/transient output": 43,
    }
    if len(files) != 199 or dict(counts) != expected:
        raise RuntimeError(f"inventory mismatch: files={len(files)} counts={dict(counts)}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT / "acquisition-engine-file-inventory-2026-08-11.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(files[0]))
        writer.writeheader()
        writer.writerows(files)
    json_path = OUTPUT / "acquisition-engine-inventory-summary-2026-08-11.json"
    json_path.write_text(json.dumps({
        "source": str(SOURCE), "file_count": len(files), "bytes": sum(row["bytes"] for row in files),
        "counts": dict(counts), "excluded_junction": excluded_prefix.rstrip("/"),
        "excluded_ephemeral_cache": "**/__pycache__/**",
        "no_moves_or_deletions": True,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "csv": str(csv_path), "summary": str(json_path), "files": len(files), "counts": dict(counts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
