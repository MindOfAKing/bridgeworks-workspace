from __future__ import annotations

import copy
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from daily_objective import select_daily_objective


def snapshot(**overrides):
    data = {
        "as_of": "2026-08-11",
        "prospects": [],
        "approvals_waiting": 0,
        "unresolved_batches": [],
        "validated_new_market_gap": False,
        "capacity": {"qualified_untouched_target": 4, "approval_backlog_cap": 3},
    }
    data.update(overrides)
    return data


def hot(prospect_id="p1", **overrides):
    row = {
        "prospect_id": prospect_id,
        "qualification_tier": "HOT",
        "qualification_score": 90,
        "lifecycle_stage": "qualified",
        "contacted": False,
        "missing_evidence": False,
        "missing_buyer": False,
        "evidence_contradicted": False,
        "contact_state_conflict": False,
        "last_verified_at": "2026-08-10",
        "actionability": "actionable",
        "unsafe_state": "none",
        "missing_qualification_dimensions": [],
    }
    row.update(overrides)
    return row


class ObjectiveSelectorTests(unittest.TestCase):
    def test_existing_approval_pressure_blocks_discovery(self):
        result = select_daily_objective(snapshot(approvals_waiting=9, validated_new_market_gap=True))
        self.assertEqual("surface_approval_decision", result["objective_type"])
        self.assertFalse(result["supply"]["allowed"])

    def test_qualification_coverage_precedes_overdue_research(self):
        result = select_daily_objective(snapshot(unresolved_batches=[
            {"batch_id": "newer", "updated_at": "2026-08-06", "prospect_ids": ["p2"]},
            {"batch_id": "older", "updated_at": "2026-07-26", "prospect_ids": ["p1"]},
        ], prospects=[hot("unscored", qualification_tier=None, qualification_score=None,
                           actionability="research_required",
                           missing_qualification_dimensions=["commercial_fit"])]))
        self.assertEqual("complete_qualification_coverage", result["objective_type"])
        self.assertEqual("complete_qualification_coverage", result["priority_class"])

    def test_missing_evidence_precedes_missing_buyer(self):
        result = select_daily_objective(snapshot(prospects=[
            hot("buyer", missing_buyer=True), hot("evidence", missing_evidence=True)
        ]))
        self.assertEqual("complete_missing_evidence", result["objective_type"])

    def test_contradiction_blocks_packet_progress(self):
        result = select_daily_objective(snapshot(prospects=[hot(evidence_contradicted=True,
            unsafe_state="unsafe_active", unsafe_reasons=["executable_approval"])]))
        self.assertEqual("reconcile_unsafe_active_state", result["objective_type"])
        self.assertEqual("stop_unsafe_external_action", result["priority_class"])

    def test_contained_contradiction_does_not_outrank_revenue(self):
        contained = hot("gbs", evidence_contradicted=True, unsafe_state="unsafe_contained",
                        actionability="blocked_contradicted_evidence")
        revenue = hot("revenue", commercial_events=[{
            "type": "reply_received", "observed_at": "2026-08-10",
            "source": "gmail:thread-1",
        }])
        result = select_daily_objective(snapshot(prospects=[contained, revenue]))
        self.assertNotEqual("reconcile_unsafe_active_state", result["objective_type"])
        self.assertNotEqual("stop_unsafe_external_action", result.get("priority_class"))
        self.assertNotIn("gbs", result["prospect_ids"])

    def test_contained_contradiction_is_still_a_reconciliation_task(self):
        contained = hot("gbs", evidence_contradicted=True, unsafe_state="unsafe_contained",
                        actionability="blocked_contradicted_evidence")
        result = select_daily_objective(snapshot(prospects=[contained]))
        self.assertEqual("reconcile_unsafe_contained_state", result["objective_type"])
        self.assertEqual("resolve_blocking_evidence", result["priority_class"])

    def test_sufficient_coverage_advances_existing_prospect(self):
        prospects = [hot(f"p{i}") for i in range(4)]
        result = select_daily_objective(snapshot(prospects=prospects, validated_new_market_gap=True))
        self.assertNotEqual("generate_new_companies", result["objective_type"])
        self.assertFalse(result["supply"]["allowed"])

    def test_supply_requires_low_coverage_no_backlog_and_market_gap(self):
        result = select_daily_objective(snapshot(validated_new_market_gap=True))
        self.assertEqual("generate_new_companies", result["objective_type"])
        self.assertTrue(result["supply"]["allowed"])

    def test_missing_connector_state_is_blocked_not_zero(self):
        data = snapshot()
        data["approvals_waiting"] = None
        result = select_daily_objective(data)
        self.assertEqual("blocked_unverified", result["objective_type"])

    def test_legacy_readiness_cannot_create_qualification(self):
        prospect = hot(qualification_tier=None, qualification_score=None,
                       lifecycle_stage="evidence_collected", engine_readiness="ready")
        result = select_daily_objective(snapshot(prospects=[prospect]))
        self.assertEqual("complete_qualification_coverage", result["objective_type"])
        self.assertEqual(1, result["metrics"]["requires_qualification_v1"])

    def test_shuffled_inputs_are_identical(self):
        data = snapshot(prospects=[hot("b", missing_buyer=True), hot("a", missing_buyer=True)])
        shuffled = copy.deepcopy(data)
        random.Random(7).shuffle(shuffled["prospects"])
        first = select_daily_objective(data)
        second = select_daily_objective(shuffled)
        self.assertEqual(first["objective_type"], second["objective_type"])
        self.assertEqual(first["prospect_ids"], second["prospect_ids"])

    def test_one_budapest_date_dedupe_key_for_both_triggers(self):
        result = select_daily_objective(snapshot())
        self.assertEqual("gtm-objective:2026-08-11", result["dedupe_key"])
        self.assertTrue(result["shadow_safe"])
        self.assertFalse(result["external_action_authorized"])


if __name__ == "__main__":
    unittest.main()
