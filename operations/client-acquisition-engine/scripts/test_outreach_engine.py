from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import outreach_engine as engine


class OutreachEngineTests(unittest.TestCase):
    def test_domain_normalization(self) -> None:
        self.assertEqual(engine.domain("https://www.Example.com/path"), "example.com")
        self.assertEqual(engine.domain("example.com"), "example.com")

    def test_reconcile_verified_touches(self) -> None:
        row = {field: "" for field in engine.SOURCE_FIELDS}
        row.update({"company": "Example Co", "country": "Hungary", "status": "research"})
        snapshot = {
            "gmail": {
                "touches": [
                    {"company": "Example Co", "sent_at": "2026-07-01", "kind": "first_contact", "message_id": "m1"},
                    {"company": "Example Co", "sent_at": "2026-07-04", "kind": "follow_up_1", "message_id": "m2"},
                ]
            }
        }
        rows, changes = engine.reconcile([row], snapshot)
        self.assertEqual(rows[0]["status"], "sent-no-reply")
        self.assertEqual(rows[0]["first_contact_sent"], "2026-07-01")
        self.assertEqual(rows[0]["follow_up_1_sent"], "2026-07-04")
        self.assertEqual(len(changes), 1)

    def test_packet_parser_preserves_approval_gate(self) -> None:
        packet = """## Priority Wave
### 1. Example Co

To: hello@example.com  
Contact: Alex Example  
Subject: One specific issue

Hi Alex,

This is a sufficiently specific draft body for an approval-only campaign record.

Best,
Emmanuel

Evidence: https://example.com/

## Test Segment
"""
        row = {field: "" for field in engine.SOURCE_FIELDS}
        row.update(
            {
                "company": "Example Company Legal Name",
                "country": "Hungary",
                "email": "hello@example.com",
                "status": "drafted-awaiting-approval",
            }
        )
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "packet.md"
            path.write_text(packet, encoding="utf-8")
            parsed = engine.parse_packet(path, [row])
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["approval_state"], "awaiting_explicit_approval")
        self.assertEqual(parsed[0]["sending_authority"], "none")
        self.assertEqual(parsed[0]["source_status"], "drafted-awaiting-approval")
        self.assertTrue(parsed[0]["prospect_id"])


if __name__ == "__main__":
    unittest.main()
