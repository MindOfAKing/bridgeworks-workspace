"""Transition prerequisites, receipts, artifact supersession, exhausted_unknown."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import gtm_core as core  # noqa: E402
import objective_hierarchy as oh  # noqa: E402
import qualification_v1 as qv1  # noqa: E402
import transitions as tr  # noqa: E402

LEDGER = core.build_evidence_ledger(
    [{"id": "a", "subject": "website_trust", "value": "x", "status": "verified",
      "source": "https://e.com", "observed_at": "2026-08-10"}], as_of="2026-08-11")
QUALIFICATION = {"model": "qualification-v1", "score": 70,
                 "qualification_coverage": {"percentage": 100.0, "missing_dimensions": []}}
CONTEXT = {"canonical_domain": "e.com", "contact_destination": "a@e.com",
           "service_route_exists": True}
# The receipt hashes a real evidence snapshot, so the path must exist.
SNAPSHOT = str((GTM_ROOT / "runs" / "geo" / "gbs-africa-2026-08-11.json")
               .relative_to(GTM_ROOT.parents[1])).replace("\\", "/")


def chain(*stages, diagnostic=None):
    history, previous = [], stages[0]
    for stage in stages[1:]:
        entry = tr.receipt("p", previous, stage, triggering_capability="test",
                           ledger=LEDGER, qualification=QUALIFICATION,
                           diagnostic=diagnostic, history=history,
                           evidence_snapshot_path=SNAPSHOT)
        history.append({**entry, "kind": "transition_receipt"})
        previous = stage
    return history


class PrerequisiteTests(unittest.TestCase):
    def test_every_required_prerequisite_is_declared(self):
        self.assertEqual(tr.PREREQUISITES["diagnostic_complete"]["requires_stage"],
                         "diagnostic_selected")
        self.assertEqual(tr.PREREQUISITES["offer_selected"]["requires_stage"],
                         "diagnostic_complete")
        self.assertEqual(tr.PREREQUISITES["outreach_prepared"]["requires_stage"],
                         "offer_selected")
        self.assertEqual(tr.PREREQUISITES["awaiting_approval"]["requires_stage"],
                         "outreach_prepared")

    def test_diagnostic_complete_needs_a_real_completed_run(self):
        history = chain("account_discovered", "evidence_collected", "qualified",
                        "routed", "diagnostic_selected")
        gate = tr.check("diagnostic_complete", history,
                        {"diagnostic_id": None, "status": "not_run"})
        self.assertFalse(gate["allowed"])
        self.assertFalse(gate["gate_results"]["diagnostic_has_id"])

    def test_a_completed_diagnostic_passes_the_gate(self):
        history = chain("account_discovered", "evidence_collected", "qualified",
                        "routed", "diagnostic_selected")
        gate = tr.check("diagnostic_complete", history,
                        {"diagnostic_id": "geo-audit:x", "status": "complete"})
        self.assertTrue(gate["allowed"])

    def test_an_offer_cannot_be_selected_before_the_diagnostic_completes(self):
        history = chain("account_discovered", "evidence_collected", "qualified",
                        "routed", "diagnostic_selected")
        with self.assertRaises(tr.PrerequisiteError):
            tr.receipt("p", "diagnostic_selected", "offer_selected",
                       triggering_capability="test", ledger=LEDGER,
                       qualification=QUALIFICATION, history=history,
                       evidence_snapshot_path=SNAPSHOT)

    def test_a_packet_cannot_skip_outreach_prepared(self):
        history = chain("account_discovered", "evidence_collected", "qualified")
        with self.assertRaises(tr.PrerequisiteError):
            tr.receipt("p", "qualified", "awaiting_approval",
                       triggering_capability="test", ledger=LEDGER,
                       qualification=QUALIFICATION, history=history,
                       evidence_snapshot_path=SNAPSHOT)


class ReceiptTests(unittest.TestCase):
    def test_a_receipt_carries_every_required_field(self):
        history = chain("account_discovered", "evidence_collected")
        for field in tr.RECEIPT_FIELDS:
            self.assertIn(field, history[-1], field)

    def test_a_later_runtime_can_verify_without_prose(self):
        history = chain("account_discovered", "evidence_collected", "qualified")
        verified = tr.reconstruct("p", history)
        self.assertEqual(verified["canonical_lifecycle_stage"], "qualified")
        self.assertEqual(len(verified["verified_transition_chain"]), 2)

    def test_the_evidence_hash_changes_when_the_evidence_does(self):
        other = core.build_evidence_ledger(
            [{"id": "b", "subject": "schema", "value": "absent", "status": "verified",
              "source": "https://e.com", "observed_at": "2026-08-10"}], as_of="2026-08-11")
        self.assertNotEqual(tr.evidence_hash(LEDGER), tr.evidence_hash(other))

    def test_the_receipt_records_the_runtime(self):
        entry = tr.receipt("p", "account_discovered", "evidence_collected",
                           triggering_capability="test", ledger=LEDGER,
                           qualification=QUALIFICATION, runtime="codex",
                           evidence_snapshot_path=SNAPSHOT)
        self.assertEqual(entry["runtime"], "codex")


class SupersessionTests(unittest.TestCase):
    def test_a_packet_without_its_prerequisite_is_superseded_and_not_executable(self):
        result = tr.classify_artifact(
            {"artifact_id": "digest", "type": "approval_packet",
             "lifecycle_stage": "awaiting_approval"},
            receipted_stages=["account_discovered", "qualified"],
            canonical_stage="qualified")
        self.assertEqual(result["classification"], tr.SUPERSEDED)
        self.assertFalse(result["executable"])

    def test_an_artifact_beyond_the_canonical_stage_is_superseded(self):
        result = tr.classify_artifact(
            {"artifact_id": "run", "type": "slice_run", "lifecycle_stage": "offer_selected"},
            receipted_stages=["diagnostic_complete"], canonical_stage="diagnostic_complete")
        self.assertEqual(result["classification"], tr.SUPERSEDED)

    def test_superseded_artifacts_are_kept_not_deleted(self):
        result = tr.classify_artifact(
            {"artifact_id": "digest", "type": "approval_packet",
             "lifecycle_stage": "awaiting_approval"},
            receipted_stages=[], canonical_stage="qualified")
        self.assertIn("artifact_id", result)
        self.assertIn("reason", result)


class ExhaustedUnknownTests(unittest.TestCase):
    def test_the_status_is_in_the_canonical_tuple(self):
        self.assertIn("exhausted_unknown", core.RESEARCH_STATUSES)
        self.assertEqual(core.RESEARCH_EXHAUSTED, "exhausted_unknown")

    def test_it_scores_zero_like_required(self):
        result = qv1.score(
            {"commercial_fit": {"score": 0, "evidence_ids": [],
                                "research_status": "exhausted_unknown"}},
            LEDGER, CONTEXT, "2026-08-11")
        self.assertEqual(result["component_scores"]["commercial_fit"], 0)

    def test_it_is_distinguishable_from_missing_research(self):
        result = qv1.score(
            {"commercial_fit": {"score": 0, "evidence_ids": [],
                                "research_status": "exhausted_unknown"}},
            LEDGER, CONTEXT, "2026-08-11")
        coverage = result["qualification_coverage"]
        self.assertIn("commercial_fit", coverage["exhausted_unknown_dimensions"])
        self.assertNotIn("commercial_fit", coverage["missing_dimensions"])
        self.assertEqual(coverage["by_dimension"]["commercial_fit"]["zero_because"],
                         "exhausted_unknown")

    def test_the_scheduler_does_not_reopen_it(self):
        import qualification_enrichment as enrich
        result = qv1.score(
            {"commercial_fit": {"score": 0, "evidence_ids": [],
                                "research_status": "exhausted_unknown"}},
            LEDGER, CONTEXT, "2026-08-11")
        plan = enrich.plan(result, {"prospect_id": "p", "company": "C"})
        self.assertNotIn("commercial_fit", [i["dimension"] for i in plan["needs_research"]])
        self.assertIn("commercial_fit", plan["skipped_reresearch"])

    def test_advancement_thresholds_did_not_change(self):
        """The state distinction lands now. The gates move later, not today."""
        self.assertEqual(core.QUALIFICATION_TIERS, ((85, "HOT"), (70, "STRONG"),
                                                    (55, "QUALIFIED"), (40, "WATCH"),
                                                    (0, "DO_NOT_PURSUE")))


class CommercialEventTests(unittest.TestCase):
    def test_a_high_score_alone_is_not_active_revenue(self):
        p = {"prospect_id": "tilz", "qualification_tier": "STRONG", "qualification_score": 72,
             "lifecycle_stage": "diagnostic_selected", "contacted": False,
             "actionability": "blocked_incomplete_diagnostic",
             "qualification_coverage": {"percentage": 83.3, "by_dimension": {}}}
        self.assertIsNone(oh.commercial_event(p))
        decision = oh.select({"as_of": "2026-08-11", "prospects": [p], "approvals_waiting": 0,
                              "unresolved_batches": [], "validated_new_market_gap": False})
        self.assertEqual(decision["priority_class"], "resolve_blocking_evidence")

    def test_a_dated_sourced_reply_is_active_revenue(self):
        p = {"prospect_id": "x", "qualification_tier": "WATCH", "qualification_score": 45,
             "lifecycle_stage": "sent", "contacted": True, "actionability": "actionable",
             "commercial_events": [{"type": "reply_received", "observed_at": "2026-08-10",
                                    "source": "gmail:thread-1"}],
             "qualification_coverage": {"percentage": 50.0, "by_dimension": {}}}
        self.assertIsNotNone(oh.commercial_event(p))
        decision = oh.select({"as_of": "2026-08-11", "prospects": [p], "approvals_waiting": 0,
                              "unresolved_batches": [], "validated_new_market_gap": False})
        self.assertEqual(decision["priority_class"], "advance_active_revenue")

    def test_an_undated_event_does_not_count(self):
        p = {"prospect_id": "x", "commercial_events": [{"type": "reply_received"}]}
        self.assertIsNone(oh.commercial_event(p))

    def test_every_named_event_type_is_supported(self):
        for name in ("reply_received", "active_conversation", "meeting_booked",
                     "discovery_held", "proposal_sent", "in_negotiation",
                     "explicit_buying_signal"):
            self.assertIn(name, oh.COMMERCIAL_EVENTS)


class CanonicalStateTests(unittest.TestCase):
    """The reconciliation result for the two disputed prospects."""

    def setUp(self):
        import reconcile_state
        self.rs = reconcile_state

    def test_premier_fm_never_completed_a_diagnostic(self):
        state = self.rs.reconcile("premier-fm")
        self.assertEqual(state["diagnostic"]["status"], "not_run")
        self.assertEqual(state["canonical_lifecycle_stage"], "diagnostic_selected")

    def test_the_premier_fm_packets_are_superseded_and_non_executable(self):
        state = self.rs.reconcile("premier-fm")
        self.assertIsNone(state["canonical_approval_packet_id"])
        self.assertTrue(state["superseded_artifacts"])

    def test_gbs_africa_did_complete_a_real_diagnostic(self):
        state = self.rs.reconcile("gbs-africa")
        self.assertEqual(state["diagnostic"]["status"], "complete")
        self.assertEqual(state["canonical_lifecycle_stage"], "diagnostic_complete")

    def test_no_runtime_is_treated_as_authority_for_reporting_later(self):
        state = self.rs.reconcile("premier-fm")
        self.assertIn("No runtime was treated as authority", state["method"])


if __name__ == "__main__":
    unittest.main()
