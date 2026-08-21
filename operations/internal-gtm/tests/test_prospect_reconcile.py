"""Canonical prospect reconciliation keeps operational systems in their lanes."""

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "adapters" / "prospect_reconcile.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prospect_reconcile", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestProspectReconciliation(unittest.TestCase):
    def test_gmail_truth_wins_and_joins_by_domain(self):
        mod = load_module()
        report = mod.reconcile([
            {
                "company": "Example Ltd", "source": "gmail_live",
                "website_url": "https://example.com", "contacted": True,
                "sent_message_id": "msg-1", "sent_message_ids": ["msg-1", "msg-2"],
            },
            {
                "company": "Example Limited", "source": "acquisition_engine_source",
                "website_url": "https://www.example.com/", "contacted": False,
                "row_status": "research",
            },
        ], "2026-08-11")
        assert report["unique_entities"] == 1
        entity = report["entities"][0]
        assert entity["entity_key"] == "domain:example.com"
        assert entity["contacted"] is True
        assert entity["fields"]["contacted"]["source"] == "gmail_live"
        assert report["gmail_sent_message_count"] == 2

    def test_approval_and_hubspot_fields_do_not_claim_contact(self):
        mod = load_module()
        report = mod.reconcile([
            {
                "company": "Example", "source": "mission_control_approval",
                "website_url": "https://example.com", "approval_state": "awaiting_approval",
                "approval_task_id": "task-1", "approval_payload_digest": "abc",
            },
            {
                "company": "Example", "source": "hubspot_live",
                "website_url": "https://example.com", "hubspot_id": "123",
            },
        ], "2026-08-11")
        entity = report["entities"][0]
        assert entity["contacted"] is False
        assert entity["fields"]["approval_state"]["value"] == "awaiting_approval"
        assert entity["fields"]["hubspot_id"]["value"] == "123"

    def test_live_evidence_receipts_are_read_only_and_counted(self):
        gmail = json.loads((ROOT / "migration" / "phase-3" /
                            "gmail-contact-history-2026-08-11.json").read_text(encoding="utf-8"))
        hubspot = json.loads((ROOT / "migration" / "phase-3" /
                              "hubspot-company-evidence-2026-08-11.json").read_text(encoding="utf-8"))
        assert gmail["read_only"] is True
        assert gmail["summary"]["contacted_companies"] == 10
        assert gmail["summary"]["sent_messages"] == 19
        assert hubspot["read_only"] is True
        assert hubspot["summary"]["companies_found"] == 14

    def test_legacy_orphaned_sends_resolve_only_on_deterministic_evidence(self):
        mod = load_module()
        receipt = mod.orphan_resolution_receipt()
        self.assertEqual(len(receipt), 3)
        self.assertTrue(all(item["resolution"] == "confirmed_match" for item in receipt))
        for item in receipt:
            self.assertEqual(item["recipient_domain"], item["canonical_domain"])
            self.assertIn(item["canonical_domain"], item["historical_domains"])
            self.assertTrue(item["gmail_message_ids"])
            self.assertTrue(item["gmail_thread_ids"])
