"""Seven priority classes, unsafe severity, and ranking without maturity."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import objective_hierarchy as oh  # noqa: E402

AS_OF = "2026-08-11"


def prospect(pid="p", **overrides):
    row = {
        "prospect_id": pid, "qualification_tier": "STRONG", "qualification_score": 70,
        "lifecycle_stage": "qualified", "contacted": False, "actionability": "actionable",
        "evidence_contradicted": False, "contact_state_conflict": False,
        "last_verified_at": "2026-08-10",
        "qualification_coverage": {"percentage": 100.0, "by_dimension": {
            "problem_evidence": {"score": 25, "confidence": "high", "evidence_ids": ["a"],
                                 "research_status": "complete"}}},
    }
    row.update(overrides)
    return row


def snapshot(prospects=None, **overrides):
    data = {"as_of": AS_OF, "prospects": prospects or [], "approvals_waiting": 0,
            "unresolved_batches": [], "validated_new_market_gap": False}
    data.update(overrides)
    return data


class UnsafeSeverityTests(unittest.TestCase):
    def test_a_contained_contradiction_is_not_top_priority(self):
        """The GBS Africa case: blocked by lifecycle and approval gates."""
        p = prospect("gbs-africa", evidence_contradicted=True,
                     actionability="blocked_contradicted_evidence", lifecycle_stage="qualified")
        result = oh.classify_unsafe(p, snapshot([p]))
        self.assertEqual(result["severity"], oh.UNSAFE_CONTAINED)
        self.assertEqual(result["priority_class"], "resolve_blocking_evidence")
        self.assertFalse(result["may_cause_external_action"])

    def test_an_unsafe_state_at_an_executable_stage_is_active(self):
        p = prospect(evidence_contradicted=True, lifecycle_stage="awaiting_approval")
        result = oh.classify_unsafe(p, snapshot([p]))
        self.assertEqual(result["severity"], oh.UNSAFE_ACTIVE)
        self.assertEqual(result["priority_class"], "stop_unsafe_external_action")

    def test_an_executable_approval_makes_it_active(self):
        p = prospect(evidence_contradicted=True, approval_task_ids=["task-1"])
        self.assertEqual(oh.classify_unsafe(p, snapshot([p]))["severity"], oh.UNSAFE_ACTIVE)

    def test_a_contradiction_affecting_several_prospects_is_active(self):
        a = prospect("a", evidence_contradicted=True, contradicted_subjects=["pricing"])
        b = prospect("b", evidence_contradicted=True, contradicted_subjects=["pricing"])
        self.assertEqual(oh.classify_unsafe(a, snapshot([a, b]))["severity"], oh.UNSAFE_ACTIVE)

    def test_contaminated_shared_state_is_active(self):
        p = prospect(evidence_contradicted=True, shared_state_contaminated=True)
        self.assertEqual(oh.classify_unsafe(p, snapshot([p]))["severity"], oh.UNSAFE_ACTIVE)

    def test_a_contact_state_conflict_is_active_because_a_send_could_repeat(self):
        p = prospect(contact_state_conflict=True)
        self.assertEqual(oh.classify_unsafe(p, snapshot([p]))["severity"], oh.UNSAFE_ACTIVE)


class HierarchyTests(unittest.TestCase):
    def test_the_seven_classes_are_in_the_approved_order(self):
        self.assertEqual(oh.PRIORITY_CLASSES, (
            "stop_unsafe_external_action", "advance_active_revenue",
            "complete_qualification_coverage", "resolve_blocking_evidence",
            "execute_due_followup_or_nurture", "recover_overdue_research",
            "generate_new_supply"))

    def test_contained_unsafe_does_not_outrank_revenue(self):
        contained = prospect("blocked", evidence_contradicted=True,
                             actionability="blocked_contradicted_evidence")
        revenue = prospect("revenue", qualification_tier="HOT", qualification_score=90,
                           commercial_events=[{"type": "reply_received",
                                               "observed_at": "2026-08-10",
                                               "source": "gmail:thread-1"}])
        decision = oh.select(snapshot([contained, revenue]))
        self.assertEqual(decision["priority_class"], "advance_active_revenue")
        self.assertEqual(decision["prospect_ids"], ["revenue"])

    def test_active_unsafe_does_outrank_revenue(self):
        active = prospect("active", evidence_contradicted=True, lifecycle_stage="awaiting_approval")
        revenue = prospect("revenue", qualification_tier="HOT", qualification_score=90,
                           commercial_events=[{"type": "reply_received",
                                               "observed_at": "2026-08-10",
                                               "source": "gmail:thread-1"}])
        decision = oh.select(snapshot([active, revenue]))
        self.assertEqual(decision["priority_class"], "stop_unsafe_external_action")

    def test_coverage_can_be_selected_over_creating_supply(self):
        gap = prospect("gap", qualification_tier=None,
                       qualification_coverage={"percentage": 0.0, "by_dimension": {}})
        decision = oh.select(snapshot([gap], validated_new_market_gap=True))
        self.assertEqual(decision["priority_class"], "complete_qualification_coverage")
        self.assertIn("complete_qualification_coverage", decision["supply_blocked_by"])

    def test_every_class_records_why_it_was_not_selected(self):
        decision = oh.select(snapshot([prospect()]))
        for entry in decision["considered_classes"]:
            if not entry["selected"]:
                self.assertTrue(entry["why_not"], entry["priority_class"])

    def test_supply_only_fires_when_every_higher_class_is_empty(self):
        decision = oh.select(snapshot([], validated_new_market_gap=True))
        self.assertEqual(decision["priority_class"], "generate_new_supply")
        self.assertEqual(decision["supply_blocked_by"], [])

    def test_supply_stays_shut_without_a_validated_market_gap(self):
        decision = oh.select(snapshot([]))
        self.assertNotEqual(decision.get("priority_class"), "generate_new_supply")


class RankingTests(unittest.TestCase):
    def test_ranking_factors_exclude_maturity(self):
        self.assertEqual(oh.RANK_ORDER, ("expected_commercial_value", "urgency",
                                         "evidence_confidence", "low_effort"))
        for factor in oh.RANK_ORDER:
            self.assertNotIn("maturity", factor)

    def test_the_explanation_names_the_excluded_factors(self):
        explanation = oh.explain_rank(prospect(), date.fromisoformat(AS_OF))
        self.assertIn("route_maturity", explanation["factors_deliberately_excluded"])
        self.assertIn("implementation_maturity", explanation["factors_deliberately_excluded"])

    def test_higher_expected_value_ranks_first(self):
        gap = {"percentage": 50.0, "by_dimension": {}}
        low = prospect("low", qualification_tier="WATCH", qualification_score=45,
                       qualification_coverage=gap)
        high = prospect("high", qualification_tier="HOT", qualification_score=90,
                        qualification_coverage=gap)
        decision = oh.select(snapshot([low, high]), cohort_size=2)
        self.assertEqual(decision["prospect_ids"][0], "high")

    def test_fresher_evidence_breaks_a_value_tie(self):
        gap = {"percentage": 50.0, "by_dimension": {}}
        stale = prospect("stale", last_verified_at="2026-06-01", qualification_coverage=gap)
        fresh = prospect("fresh", last_verified_at="2026-08-10", qualification_coverage=gap)
        decision = oh.select(snapshot([stale, fresh]), cohort_size=2)
        self.assertEqual(decision["prospect_ids"][0], "fresh")

    def test_selection_is_deterministic(self):
        gap = {"percentage": 50.0, "by_dimension": {}}
        rows = [prospect("b", qualification_coverage=gap), prospect("a", qualification_coverage=gap)]
        first = oh.select(snapshot(rows), cohort_size=2)
        second = oh.select(snapshot(list(reversed(rows))), cohort_size=2)
        self.assertEqual(first["prospect_ids"], second["prospect_ids"])

    def test_nothing_selected_authorizes_an_external_action(self):
        decision = oh.select(snapshot([prospect()]))
        self.assertFalse(decision["external_action_authorized"])


class LiveStateTests(unittest.TestCase):
    """Against the real snapshot. The GBS Africa reclassification must hold."""

    def setUp(self):
        sys.path.insert(0, str(GTM_ROOT / "adapters"))
        import engine_snapshot
        self.snapshot = engine_snapshot.build(AS_OF)

    def test_gbs_africa_is_contained_not_active(self):
        decision = oh.select(self.snapshot, cohort_size=8)
        classifications = {u["prospect_id"]: u["severity"] for u in decision["unsafe_classification"]}
        if "gbs-africa" in classifications:
            self.assertEqual(classifications["gbs-africa"], oh.UNSAFE_CONTAINED)

    def test_no_prospect_claims_active_revenue_without_a_commercial_event(self):
        """A high score is not active revenue. Only a dated, sourced event is."""
        decision = oh.select(self.snapshot, cohort_size=8)
        self.assertNotEqual(decision["priority_class"], "generate_new_supply")
        with_events = [p for p in self.snapshot["prospects"] if oh.commercial_event(p)]
        if not with_events:
            self.assertNotEqual(decision["priority_class"], "advance_active_revenue")


if __name__ == "__main__":
    unittest.main()
