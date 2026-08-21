"""Acceptance tests for the first bounded real internal-GTM batch."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import real_gtm_batch  # noqa: E402


class RealBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = real_gtm_batch.build("2026-08-11")

    def test_batch_is_bounded_and_uses_existing_prospects(self):
        self.assertEqual(8, len(self.batch["prospects"]))
        self.assertEqual("complete_qualification_coverage",
                         self.batch["objective"]["priority_class"])

    def test_gbs_contained_state_is_not_in_the_enrichment_cohort(self):
        ids = {p["prospect_id"] for p in self.batch["prospects"]}
        self.assertNotIn("gbs-africa", ids)

    def test_every_prospect_has_both_intelligence_results_and_qualification(self):
        for row in self.batch["prospects"]:
            self.assertEqual("qualification-v1", row["qualification_v1"]["model"])
            self.assertEqual("bridgeworks-commercial-intelligence",
                             row["commercial_intelligence"]["capability"])
            self.assertEqual("bridgeworks-buyer-intelligence",
                             row["buyer_intelligence"]["capability"])

    def test_progressive_spend_blocks_premature_packets(self):
        self.assertEqual(0, self.batch["approval_packets_created"])
        self.assertTrue(all(row["approval_packet"] is None for row in self.batch["prospects"]))

    def test_two_justified_diagnostics_remain_non_executable(self):
        by_id = {row["prospect_id"]: row for row in self.batch["prospects"]}
        self.assertEqual("existing_partial_diagnostic", by_id["tilz-prosperitas"]["diagnostic"]["result"])
        self.assertEqual("completed_internal_test_draft", by_id["bv-integrated-ltd"]["diagnostic"]["result"])
        self.assertTrue(all(not row["external_action_authorized"] for row in self.batch["prospects"]))


if __name__ == "__main__":
    unittest.main()
