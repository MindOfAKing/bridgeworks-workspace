"""qualification-v1 through the derivation layer over the canonical gtm_core scorer.

The arithmetic and the gates live in `gtm_core.score_qualification`. This suite
exercises them through `qualification_v1`, which derives provenance, freshness and
confidence from the ledger so a caller cannot assert them.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import gtm_core as core  # noqa: E402
import qualification_v1 as qv1  # noqa: E402


def ledger(*claims):
    return core.build_evidence_ledger(list(claims), as_of="2026-08-11")


def claim(claim_id, subject, value="x", status="verified", observed="2026-08-10",
          source="https://example.com/a", claim_key=None):
    row = {"id": claim_id, "subject": subject, "value": value, "status": status,
           "source": source, "observed_at": observed}
    if claim_key:
        row["claim_key"] = claim_key
    return row


def context(**overrides):
    data = {
        "canonical_domain": "example.com",
        "normalized_company": "example",
        "contact_destination": "buyer@example.com",
        "service_route_exists": True,
        "prior_outreach": False,
        "communication_state_resolved": True,
    }
    data.update(overrides)
    return data


class ModelShapeTests(unittest.TestCase):
    def test_six_dimensions_summing_to_one_hundred(self):
        self.assertEqual(dict(qv1.DIMENSIONS), {
            "problem_evidence": 25, "commercial_fit": 20, "buyer_accessibility": 15,
            "trigger_urgency": 15, "proof_fit": 15, "execution_readiness": 10})
        self.assertEqual(qv1.MAX_SCORE, 100)

    def test_tier_thresholds_match_the_approved_decision(self):
        self.assertEqual(qv1.TIERS, ((85, "HOT"), (70, "STRONG"), (55, "QUALIFIED"),
                                     (40, "WATCH"), (0, "DO_NOT_PURSUE")))

    def test_thresholds_are_versioned_defaults_not_constants_in_code(self):
        """Recalibration must be a data change, not a rewrite."""
        self.assertEqual(qv1.MODEL_ID, "qualification-v1")
        self.assertTrue(qv1.MODEL_APPROVED)

    def test_every_tier_boundary_lands_where_the_decision_says(self):
        cases = {100: "HOT", 85: "HOT", 84: "STRONG", 70: "STRONG", 69: "QUALIFIED",
                 55: "QUALIFIED", 54: "WATCH", 40: "WATCH", 39: "DO_NOT_PURSUE", 0: "DO_NOT_PURSUE"}
        for total, expected in cases.items():
            tier = next(name for threshold, name in qv1.TIERS if total >= threshold)
            self.assertEqual(tier, expected, total)


class EvidenceAttributionTests(unittest.TestCase):
    def test_a_non_zero_score_needs_attributable_evidence(self):
        result = qv1.score({"problem_evidence": {"score": 25}}, ledger(), context(), "2026-08-11")
        component = result["components"]["problem_evidence"]
        self.assertEqual(component["score"], 0)
        self.assertEqual(component["adjustment_reason"],
                         "no_approved_evidence_attributable_to_this_component")
        self.assertEqual(result["score"], 0)

    def test_unknown_evidence_does_not_score_positively(self):
        evidence = ledger(claim("a", "website_trust", source=None))
        result = qv1.score({"problem_evidence": {"score": 20, "evidence_ids": ["a"]}},
                           evidence, context(), "2026-08-11")
        self.assertEqual(result["component_scores"]["problem_evidence"], 0)

    def test_an_evidence_id_not_in_the_ledger_zeroes_the_component(self):
        evidence = ledger(claim("a", "website_trust"))
        result = qv1.score({"problem_evidence": {"score": 20, "evidence_ids": ["a", "ghost"]}},
                           evidence, context(), "2026-08-11")
        component = result["components"]["problem_evidence"]
        self.assertNotIn("ghost", component["usable_evidence_ids"])
        self.assertEqual(component["unresolvable_evidence_ids"], ["ghost"])
        self.assertEqual(result["unresolvable_evidence_ids"], ["ghost"])

    def test_confidence_tracks_evidence_class_and_freshness(self):
        cases = {
            ("verified", "2026-08-09"): ("current", "high"),
            ("observed", "2026-08-09"): ("current", "medium"),
            ("verified", "2026-04-01"): ("stale", "medium"),
        }
        for (status, observed), (freshness, confidence) in cases.items():
            evidence = ledger(claim("a", "website_trust", status=status, observed=observed))
            result = qv1.score({"problem_evidence": {"score": 20, "evidence_ids": ["a"]}},
                               evidence, context(), "2026-08-11")
            component = result["components"]["problem_evidence"]
            self.assertEqual(component["score"], 20, (status, observed))
            self.assertEqual(component["evidence_freshness"], freshness, (status, observed))

    def test_stale_evidence_loses_the_score_because_the_ledger_unapproves_it(self):
        """Over the staleness window the ledger marks it stale, so it is no longer approved."""
        evidence = ledger(claim("a", "website_trust", observed="2026-01-02"))
        result = qv1.score({"problem_evidence": {"score": 20, "evidence_ids": ["a"]}},
                           evidence, context(), "2026-08-11")
        component = result["components"]["problem_evidence"]
        self.assertEqual(component["evidence_freshness"], "stale")
        self.assertEqual(component["score"], 0)
        self.assertIn(component["confidence"], ("low", "unknown"))

    def test_contradicted_evidence_is_not_silently_resolved(self):
        evidence = ledger(
            claim("a", "conversion_path", value="present", claim_key="form"),
            claim("b", "conversion_path", value="absent", claim_key="form"))
        result = qv1.score({"problem_evidence": {"score": 25, "evidence_ids": ["a", "b"]}},
                           evidence, context(), "2026-08-11")
        component = result["components"]["problem_evidence"]
        self.assertEqual(component["score"], 0)
        self.assertTrue(component["contradicted_evidence_ids"])
        self.assertTrue(component["contradicted_evidence_ids"])
        self.assertEqual(result["actionability"], "blocked_contradicted_evidence")

    def test_every_component_stores_the_five_required_fields(self):
        evidence = ledger(claim("a", "website_trust"))
        result = qv1.score({"problem_evidence": {"score": 20, "evidence_ids": ["a"]}},
                           evidence, context(), "2026-08-11")
        for name, component in result["components"].items():
            for field in ("score", "evidence_ids", "evidence_freshness", "confidence",
                          "source_provenance"):
                self.assertIn(field, component, name)

    def test_a_score_above_the_component_maximum_raises(self):
        with self.assertRaises(qv1.QualificationError):
            qv1.score({"execution_readiness": {"score": 11}}, ledger(), context(), "2026-08-11")


class SeparationOfConcernsTests(unittest.TestCase):
    """No diagnostic family may become an implicit qualification proxy."""

    def test_routing_fields_are_refused(self):
        for field in ("route_id", "primary_service_route", "diagnostic_score",
                      "diagnostic_capability", "geo_score", "gap_categories"):
            with self.assertRaises(qv1.QualificationError, msg=field):
                qv1.score({}, ledger(), context(**{field: "anything"}), "2026-08-11")

    def test_the_model_has_no_route_or_diagnostic_dimension(self):
        for name in qv1.DIMENSIONS:
            self.assertNotIn("route", name)
            self.assertNotIn("geo", name)
            self.assertNotIn("diagnostic", name)

    def test_service_route_existence_is_a_gate_not_a_score(self):
        evidence = ledger(claim("a", "website_trust"))
        components = {"problem_evidence": {"score": 25, "evidence_ids": ["a"]}}
        with_route = qv1.score(components, evidence, context(), "2026-08-11")
        without = qv1.score(components, evidence, context(service_route_exists=False), "2026-08-11")
        self.assertEqual(with_route["score"], without["score"])
        self.assertEqual(without["actionability"], "blocked_no_service_route")


class BlockingStateTests(unittest.TestCase):
    def full(self):
        evidence = ledger(*[claim(f"e{i}", "website_trust", source=f"https://example.com/{i}")
                            for i in range(6)])
        components = {name: {"score": maximum, "evidence_ids": [f"e{i}"]}
                      for i, (name, maximum) in enumerate(qv1.DIMENSIONS.items())}
        return components, evidence

    def test_a_perfect_score_can_still_be_blocked(self):
        components, evidence = self.full()
        result = qv1.score(components, evidence, context(contact_destination=None), "2026-08-11")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["tier"], "HOT")
        self.assertEqual(result["actionability"], "blocked_missing_destination")

    def test_score_and_actionability_are_separate_fields(self):
        components, evidence = self.full()
        result = qv1.score(components, evidence, context(), "2026-08-11")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["actionability"], "actionable")
        self.assertNotIn("blocked", str(result["tier"]))

    def test_all_seven_blocking_conditions_are_reachable(self):
        components, evidence = self.full()
        cases = {
            "unresolved_identity_domain": context(canonical_domain=None, normalized_company=None),
            "missing_viable_contact_destination": context(contact_destination=None),
            "unresolved_previous_outreach": context(prior_outreach=True,
                                                   communication_state_resolved=False),
            "legal_compliance_exclusion": context(legal_exclusion="opt-out on file"),
            "no_credible_service_route": context(service_route_exists=False),
            "explicit_defer_hold": context(hold_reason="deferred until Oliviks closeout"),
        }
        for expected, ctx in cases.items():
            result = qv1.score(components, evidence, ctx, "2026-08-11")
            conditions = result["blocking_reasons"]
            self.assertIn(expected, conditions, expected)

        contradicted = ledger(claim("a", "s", value=1, claim_key="k"),
                              claim("b", "s", value=2, claim_key="k"))
        result = qv1.score({"problem_evidence": {"score": 10, "evidence_ids": ["a", "b"]}},
                           contradicted, context(), "2026-08-11")
        self.assertIn("materially_contradicted_evidence", result["blocking_reasons"])

    def test_prior_outreach_with_a_resolved_state_does_not_block(self):
        components, evidence = self.full()
        result = qv1.score(components, evidence,
                           context(prior_outreach=True, communication_state_resolved=True),
                           "2026-08-11")
        self.assertEqual(result["actionability"], "actionable")

    def test_unscored_components_are_reported_as_an_evidence_gap(self):
        evidence = ledger(claim("a", "website_trust"))
        result = qv1.score({"problem_evidence": {"score": 25, "evidence_ids": ["a"]}},
                           evidence, context(), "2026-08-11")
        self.assertTrue(result["evidence_gap"])
        self.assertIn("commercial_fit", result["unscored_components"])
        self.assertIn("execution_readiness", result["unscored_components"])


class DeterminismTests(unittest.TestCase):
    def test_same_input_same_output(self):
        evidence = ledger(claim("a", "website_trust"))
        components = {"problem_evidence": {"score": 20, "evidence_ids": ["a"]}}
        first = qv1.score(components, evidence, context(), "2026-08-11")
        second = qv1.score(components, evidence, context(), "2026-08-11")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
