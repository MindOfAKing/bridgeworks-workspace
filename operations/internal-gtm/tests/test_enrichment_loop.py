"""Coverage, the enrichment loop, and the canonical contacted-company definition."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import contacted_companies as contacted  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_enrichment as enrich  # noqa: E402
import qualification_v1 as qv1  # noqa: E402


def claim(cid, subject, status="verified", observed="2026-08-10", source="https://e.com/a"):
    return {"id": cid, "subject": subject, "value": cid, "status": status,
            "source": source, "observed_at": observed}


def score(components, claims, **context):
    ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
    base = {"canonical_domain": "e.com", "normalized_company": "e",
            "contact_destination": "a@e.com", "service_route_exists": True}
    base.update(context)
    return qv1.score(components, ledger, base, "2026-08-11")


class CoverageTests(unittest.TestCase):
    def test_coverage_stores_the_five_required_fields_per_dimension(self):
        result = score({"problem_evidence": {"score": 20, "evidence_ids": ["a"],
                                             "research_status": "complete"}},
                       [claim("a", "website_trust")])
        for name, item in result["qualification_coverage"]["by_dimension"].items():
            for field in ("score", "evidence_state", "evidence_ids", "confidence", "research_status"):
                self.assertIn(field, item, f"{name}:{field}")

    def test_coverage_reports_both_a_count_and_a_percentage(self):
        result = score({"problem_evidence": {"score": 20, "evidence_ids": ["a"],
                                             "research_status": "complete"}},
                       [claim("a", "website_trust")])
        coverage = result["qualification_coverage"]
        self.assertIn("sufficiently_researched_dimensions", coverage)
        self.assertIn("percentage", coverage)
        self.assertEqual(coverage["total_dimensions"], 6)

    def test_coverage_is_never_added_to_the_score(self):
        """Two prospects, same evidence, different declared coverage. Same score."""
        claims = [claim("a", "website_trust")]
        low = score({"problem_evidence": {"score": 20, "evidence_ids": ["a"],
                                          "research_status": "complete"}}, claims)
        high = score({"problem_evidence": {"score": 20, "evidence_ids": ["a"],
                                           "research_status": "complete"},
                      "trigger_urgency": {"score": 0, "evidence_ids": [],
                                          "research_status": "not_applicable"}}, claims)
        self.assertEqual(low["score"], high["score"])
        self.assertNotEqual(low["qualification_coverage"]["percentage"],
                            high["qualification_coverage"]["percentage"])

    def test_missing_research_is_distinguishable_from_a_verified_negative(self):
        result = score({
            "problem_evidence": {"score": 20, "evidence_ids": ["a"], "research_status": "complete"},
            "commercial_fit": {"score": 0, "evidence_ids": ["b"], "research_status": "complete",
                               "rationale": "verified sole trader, below the engagement floor"},
        }, [claim("a", "website_trust"), claim("b", "commercial_fit")])
        dimensions = result["qualification_coverage"]["by_dimension"]
        self.assertEqual(dimensions["commercial_fit"]["score"], 0)
        self.assertEqual(dimensions["commercial_fit"]["zero_because"], "verified_negative")
        self.assertEqual(dimensions["execution_readiness"]["zero_because"], "missing_research")
        self.assertIn("commercial_fit",
                      result["qualification_coverage"]["verified_negative_dimensions"])
        self.assertNotIn("commercial_fit", result["qualification_coverage"]["missing_dimensions"])

    def test_unknown_evidence_still_scores_zero(self):
        result = score({"problem_evidence": {"score": 25, "evidence_ids": ["a"],
                                             "research_status": "complete"}},
                       [claim("a", "website_trust", source=None)])
        self.assertEqual(result["component_scores"]["problem_evidence"], 0)

    def test_a_not_applicable_dimension_leaves_the_denominator(self):
        result = score({"trigger_urgency": {"score": 0, "evidence_ids": [],
                                            "research_status": "not_applicable"}},
                       [claim("a", "website_trust")])
        self.assertIn("trigger_urgency",
                      result["qualification_coverage"]["not_applicable_dimensions"])


class EnrichmentLoopTests(unittest.TestCase):
    def result(self):
        return score({
            "problem_evidence": {"score": 20, "evidence_ids": ["a"], "research_status": "complete"},
        }, [claim("a", "website_trust")])

    def test_missing_commercial_fit_routes_to_commercial_intelligence(self):
        plan = enrich.plan(self.result(), {"prospect_id": "p", "company": "C"})
        routed = {item["dimension"]: item["capability"] for item in plan["needs_research"]}
        self.assertEqual(routed["commercial_fit"], "bridgeworks-commercial-intelligence")

    def test_missing_buyer_accessibility_routes_to_buyer_intelligence(self):
        plan = enrich.plan(self.result(), {"prospect_id": "p", "company": "C"})
        routed = {item["dimension"]: item["capability"] for item in plan["needs_research"]}
        self.assertEqual(routed["buyer_accessibility"], "bridgeworks-buyer-intelligence")

    def test_a_covered_dimension_is_never_re_researched(self):
        plan = enrich.plan(self.result(), {"prospect_id": "p", "company": "C"})
        self.assertIn("problem_evidence", plan["skipped_reresearch"])
        self.assertNotIn("problem_evidence", [i["dimension"] for i in plan["needs_research"]])

    def test_every_call_resolves_against_the_canonical_registry(self):
        plan = enrich.plan(self.result(), {"prospect_id": "p", "company": "C"})
        self.assertTrue(plan["capability_calls"])
        for call in plan["capability_calls"]:
            self.assertEqual(call["kind"], "capability_call_required")
            self.assertFalse(call["approval_required"])

    def test_the_plan_authorizes_nothing(self):
        plan = enrich.plan(self.result(), {"prospect_id": "p", "company": "C"})
        self.assertFalse(plan["external_action_authorized"])

    def test_one_dimension_to_capability_map_not_two(self):
        """The scheduler and the planner must not disagree about who researches what."""
        from daily_objective import ENRICHMENT_CAPABILITIES
        for dimension in ("commercial_fit", "buyer_accessibility", "execution_readiness"):
            route = enrich.research_route(dimension)
            self.assertEqual(route["capability"], ENRICHMENT_CAPABILITIES[dimension], dimension)

    def test_the_survey_counts_real_run_records(self):
        report = enrich.survey(GTM_ROOT / "runs" / "geo")
        self.assertGreater(report["prospects_with_qualification"], 0)
        self.assertIn("commercial_fit", report["missing_by_dimension"])


class ContactedCompanyTests(unittest.TestCase):
    def setUp(self):
        self.report = contacted.accounting("2026-08-11")

    def test_the_definition_is_stated_in_the_output(self):
        self.assertIn("verified Gmail SENT message", self.report["definition"])
        self.assertEqual(self.report["link_rules"], list(contacted.LINK_RULES))

    def test_all_four_numbers_are_produced(self):
        for key in ("contacted_company_count", "canonical_sent_message_count",
                    "ambiguous_possible_match_count", "unmatched_sent_message_count"):
            self.assertIn(key, self.report)
            self.assertIsInstance(self.report[key], int)

    def test_every_contacted_company_names_the_rule_that_linked_it(self):
        for entry in self.report["contacted_companies"]:
            self.assertIn(entry["link_rule"], contacted.LINK_RULES)
            self.assertTrue(entry["sent_message_ids"])

    def test_a_similar_name_alone_never_links(self):
        entities = [{"entity_key": "domain:example.com", "company": "Example Ltd",
                     "fields": {"website_url": {"value": "https://example.com"}}}]
        matches, _ = contacted.link({"destination": "info@totally-different.com"}, entities)
        self.assertEqual(matches, [])

    def test_two_matching_entities_stay_ambiguous(self):
        entities = [
            {"entity_key": "domain:example.com", "company": "A",
             "fields": {"buyer_email": {"value": "info@example.com"}}},
            {"entity_key": "company:b", "company": "B",
             "fields": {"buyer_email": {"value": "info@example.com"}}},
        ]
        matches, rule = contacted.link({"destination": "info@example.com"}, entities)
        self.assertEqual(len(matches), 2)
        self.assertIsNone(rule, "an ambiguous link must not be resolved to one rule")

    def test_the_count_matches_the_sum_of_its_parts(self):
        total = sum(len(e["sent_message_ids"]) for e in self.report["contacted_companies"])
        self.assertEqual(total, self.report["canonical_sent_message_count"])


if __name__ == "__main__":
    unittest.main()
