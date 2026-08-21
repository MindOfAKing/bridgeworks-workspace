"""Determinism, evidence discipline, and the approval gate."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = GTM_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import capability_loader as cl  # noqa: E402
import gtm_core as core  # noqa: E402


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class NormalizationTests(unittest.TestCase):
    def test_legal_suffixes_are_stripped(self):
        self.assertEqual(core.normalize_company("Northline Facility Services Kft."), "northline facility services")
        self.assertEqual(core.normalize_company("NORTHLINE FACILITY SERVICES"), "northline facility services")

    def test_domain_is_reduced_to_host(self):
        for value in ("https://www.example.com/hu/page?a=1", "HTTP://Example.com", "example.com."):
            self.assertEqual(core.normalize_domain(value), "example.com")

    def test_non_domains_return_empty(self):
        for value in ("", "not a domain", "localhost"):
            self.assertEqual(core.normalize_domain(value), "")


class DedupeTests(unittest.TestCase):
    records = [
        {"company": "Northline Facility Services Kft.", "website_url": "https://www.northline.example.com/", "source": "a"},
        {"company": "NORTHLINE FACILITY SERVICES", "website_url": "http://northline.example.com/en", "source": "b"},
        {"company": "Danube Property Care Bt.", "website_url": "https://danube.example.org", "source": "a"},
    ]

    def test_exact_duplicates_merge(self):
        result = core.dedupe(self.records)
        self.assertEqual(len(result.unique), 2)
        self.assertEqual(len(result.merges), 1)
        self.assertEqual(result.merges[0]["rule"], "exact_key_match")

    def test_provenance_is_preserved_on_merge(self):
        result = core.dedupe(self.records)
        merged = next(r for r in result.unique if r["entity_key"] == "domain:northline.example.com")
        self.assertEqual(merged["source_provenance"], ["a", "b"])

    def test_order_independent(self):
        forward = core.dedupe(self.records).unique
        backward = core.dedupe(list(reversed(self.records))).unique
        self.assertEqual([r["entity_key"] for r in forward], [r["entity_key"] for r in backward])

    def test_merged_record_is_byte_identical_either_way(self):
        forward = core.dedupe(self.records).unique
        backward = core.dedupe(list(reversed(self.records))).unique
        self.assertEqual(json.dumps(forward, sort_keys=True), json.dumps(backward, sort_keys=True))

    def test_keyless_record_is_rejected_not_merged(self):
        result = core.dedupe([{"company": "", "website_url": "", "source": "x"}])
        self.assertEqual(result.unique, [])
        self.assertEqual(result.rejected[0]["reason"], "no_domain_or_company")


class EvidenceTests(unittest.TestCase):
    def test_claim_without_source_is_never_approved(self):
        ledger = core.build_evidence_ledger(
            [{"id": "a", "subject": "ai_visibility", "value": "x", "status": "verified",
              "source": None, "observed_at": "2026-08-10"}], as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], [])
        self.assertEqual(ledger["ledger"][0]["reason"], "no_source")

    def test_old_observation_becomes_stale(self):
        ledger = core.build_evidence_ledger(
            [{"id": "a", "subject": "schema", "value": "absent", "status": "verified",
              "source": "https://example.com", "observed_at": "2026-01-02"}], as_of="2026-08-11")
        self.assertEqual(ledger["ledger"][0]["status"], "stale")
        self.assertEqual(ledger["approved_claim_ids"], [])

    def test_conflicting_values_are_contradicted(self):
        ledger = core.build_evidence_ledger([
            {"id": "a", "subject": "conversion_path", "claim_key": "enquiry_form_present",
             "value": "no_form", "status": "observed",
             "source": "https://example.com/contact", "observed_at": "2026-08-08"},
            {"id": "b", "subject": "conversion_path", "claim_key": "enquiry_form_present",
             "value": "form_present", "status": "verified",
             "source": "https://example.com/", "observed_at": "2026-08-08"},
        ], as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], [])
        self.assertEqual(ledger["counts"]["contradicted"], 2)

    def test_distinct_findings_in_one_category_are_not_contradictions(self):
        """Regression: real geo-audit data marked every finding in a category contradicted."""
        claims = [
            {"id": "a", "subject": "ai_visibility", "claim_key": "a", "value": "no_wikipedia_entity",
             "status": "verified", "source": "https://example.com/1", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "ai_visibility", "claim_key": "b", "value": "llms_txt_absent",
             "status": "verified", "source": "https://example.com/2", "observed_at": "2026-08-10"},
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], ["a", "b"])
        self.assertEqual(ledger["counts"]["contradicted"], 0)

    def test_shared_claim_key_still_detects_the_real_conflict(self):
        claims = [
            {"id": "a", "subject": "search_visibility", "claim_key": "homepage_title_tag",
             "value": "absent", "status": "verified", "source": "https://example.com/", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "search_visibility", "claim_key": "homepage_title_tag",
             "value": "present", "status": "verified", "source": "https://example.com/", "observed_at": "2026-08-10"},
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], [])
        self.assertEqual(ledger["counts"]["contradicted"], 2)

    def test_implicit_key_is_subject_and_source_never_subject_alone(self):
        """Step 7 invariant. Same topic, different pages, different facts: not a conflict."""
        claims = [
            {"id": "a", "subject": "conversion_path", "value": "no_confirmation_state",
             "status": "verified", "source": "https://example.com/contact", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "conversion_path", "value": "form_three_clicks_deep",
             "status": "verified", "source": "https://example.com/", "observed_at": "2026-08-10"},
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], ["a", "b"])
        self.assertEqual(ledger["counts"]["contradicted"], 0)

    def test_same_subject_same_page_disagreement_is_caught_without_a_declared_key(self):
        claims = [
            {"id": "a", "subject": "ownership", "value": "no_named_owner", "status": "verified",
             "source": "https://example.com/about", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "ownership", "value": "named_owner_present", "status": "verified",
             "source": "https://example.com/about", "observed_at": "2026-08-10"},
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], [])
        self.assertEqual(ledger["counts"]["contradicted"], 2)

    def test_declared_key_beats_page_coincidence(self):
        """Two findings on one page, explicitly different propositions, stay approved."""
        claims = [
            {"id": "a", "subject": "process_gaps", "claim_key": "handoff_owner_named",
             "value": "absent", "status": "verified",
             "source": "https://example.com/ops", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "process_gaps", "claim_key": "sla_published",
             "value": "absent", "status": "verified",
             "source": "https://example.com/ops", "observed_at": "2026-08-10"},
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(ledger["approved_claim_ids"], ["a", "b"])

    def test_invariant_validator_warns_on_implicit_collisions(self):
        claims = [
            {"id": "a", "subject": "measurement", "value": 1, "source": "https://example.com/x"},
            {"id": "b", "subject": "measurement", "value": 2, "source": "https://example.com/x"},
            {"id": "c", "subject": "measurement", "value": 3, "source": "https://example.com/y"},
        ]
        warnings = core.validate_claim_invariant(claims)
        self.assertEqual(len(warnings), 1)
        self.assertIn("a, b", warnings[0])

    def test_invariant_holds_for_manual_workflow_claims(self):
        """Non-GEO coverage: an AI-workflow diagnostic with many findings per subject."""
        claims = [
            {"id": f"w{i}", "subject": "manual_followup", "value": v, "status": "verified",
             "source": f"https://example.com/step-{i}", "observed_at": "2026-08-10"}
            for i, v in enumerate(["no_auto_ack", "no_owner_assignment", "no_sla_timer", "no_escalation"])
        ]
        ledger = core.build_evidence_ledger(claims, as_of="2026-08-11")
        self.assertEqual(len(ledger["approved_claim_ids"]), 4)
        self.assertEqual(ledger["counts"]["contradicted"], 0)

    def test_verified_beats_observed_for_quality(self):
        ledger = core.build_evidence_ledger([
            {"id": "a", "subject": "s1", "value": 1, "status": "observed",
             "source": "https://example.com", "observed_at": "2026-08-10"},
            {"id": "b", "subject": "s2", "value": 2, "status": "verified",
             "source": "https://example.com", "observed_at": "2026-08-10"},
        ], as_of="2026-08-11")
        self.assertEqual(ledger["evidence_quality"], "verified")


class RankingTests(unittest.TestCase):
    """The superseded route-fit rubric is gone. qualification-v1 is tested in
    test_qualification_v1.py against the canonical gtm_core scorer."""

    def test_ranking_is_stable(self):
        rows = [{"company": "b", "entity_key": "company:b", "qualification_score": 50},
                {"company": "a", "entity_key": "company:a", "qualification_score": 50},
                {"company": "c", "entity_key": "company:c", "qualification_score": 90}]
        ranked = core.rank(rows)
        self.assertEqual([r["company"] for r in ranked], ["c", "a", "b"])

    def test_the_old_signals_rubric_is_no_longer_callable(self):
        with self.assertRaises(core.QualificationError):
            core.score_qualification({"route_fit": "exact", "evidence_quality": "verified"})



class LifecycleTests(unittest.TestCase):
    def test_forward_only(self):
        self.assertEqual(core.advance("qualified", "routed"), "routed")
        with self.assertRaises(core.LifecycleError):
            core.advance("routed", "qualified")

    def test_send_is_not_reachable_from_code(self):
        with self.assertRaises(core.LifecycleError):
            core.advance("awaiting_approval", "sent")

    def test_lifecycle_matches_the_state_schema(self):
        schema = json.loads((GTM_ROOT / "schemas" / "gtm-state.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(tuple(schema["properties"]["lifecycle_stage"]["enum"]), core.LIFECYCLE)


class PacketTests(unittest.TestCase):
    evidence = core.build_evidence_ledger(
        [{"id": "g1", "subject": "ai_visibility", "value": "no_citations", "status": "verified",
          "source": "https://example.com", "observed_at": "2026-08-10"},
         {"id": "g4", "subject": "local_presence", "value": "likely", "status": "inferred",
          "source": None, "observed_at": "2026-08-10"}], as_of="2026-08-11")
    prospect = {"prospect_id": "fixture", "company": "Example", "qualification_score": 80,
                "qualification_tier": "HOT"}
    route = {"route_id": "content-visibility-demand", "matched_gaps": ["ai_visibility"]}

    def offer(self):
        return core.select_offer_wedge("content-visibility-demand", "HOT", cl.load_service_routes())

    def test_packet_stops_at_the_approval_gate(self):
        packet = core.build_outreach_packet(
            self.prospect, self.evidence, self.route, self.offer(), ["g1"], "2026-08-11")
        self.assertEqual(packet["lifecycle_stage"], "awaiting_approval")
        self.assertEqual(packet["approval_state"], "pending_approval")
        self.assertFalse(packet["external_action_authorized"])
        self.assertTrue(packet["no_send"])

    def test_unapproved_citation_raises(self):
        with self.assertRaises(core.ApprovalError):
            core.build_outreach_packet(
                self.prospect, self.evidence, self.route, self.offer(), ["g1", "g4"], "2026-08-11")

    def test_digest_is_stable_and_content_bound(self):
        first = core.build_outreach_packet(
            self.prospect, self.evidence, self.route, self.offer(), ["g1"], "2026-08-11")
        second = core.build_outreach_packet(
            self.prospect, self.evidence, self.route, self.offer(), ["g1"], "2026-08-11")
        self.assertEqual(first["approval_payload_digest"], second["approval_payload_digest"])
        changed = dict(self.prospect, buyer_email="other@example.com")
        third = core.build_outreach_packet(
            changed, self.evidence, self.route, self.offer(), ["g1"], "2026-08-11")
        self.assertNotEqual(first["approval_payload_digest"], third["approval_payload_digest"])

    def test_no_price_is_asserted(self):
        packet = core.build_outreach_packet(
            self.prospect, self.evidence, self.route, self.offer(), ["g1"], "2026-08-11")
        self.assertEqual(packet["body"]["price"], "confirmed_at_booking")


class ServiceRouteTests(unittest.TestCase):
    routes = cl.load_service_routes()

    def test_five_canonical_routes(self):
        self.assertEqual(len(self.routes["routes"]), 5)
        self.assertEqual(
            {r["name"] for r in self.routes["routes"]},
            {"Strategy & Transformation", "Digital Platforms & Brand Systems",
             "Content, Visibility & Demand", "AI & Workflow Automation",
             "Execution & Operating Systems"})

    def test_priority_covers_every_route(self):
        self.assertEqual(set(self.routes["route_priority"]), {r["id"] for r in self.routes["routes"]})

    def test_single_match_is_exact_fit(self):
        result = core.select_service_route(["ai_visibility", "schema"], self.routes)
        self.assertEqual(result["route_id"], "content-visibility-demand")
        self.assertEqual(result["fit"], "exact")

    def test_stronger_evidence_wins_not_display_order(self):
        findings = [
            {"category": "conversion_path", "status": "verified", "severity": "high"},
            {"category": "conversion_path", "status": "verified", "severity": "high"},
            {"category": "ai_visibility", "status": "observed", "severity": "low"},
        ]
        result = core.select_service_route(
            ["ai_visibility", "conversion_path"], self.routes, findings=findings)
        self.assertEqual(result["route_id"], "digital-platforms-brand")
        self.assertEqual(result["fit"], "adjacent")
        self.assertEqual(result["won_on"], "evidence_strength")
        self.assertIn("content-visibility-demand", result["secondary_routes"])

    def test_geo_does_not_win_a_true_tie(self):
        """Step 6 regression: GEO must not take a tie because it is the mature family."""
        findings = [
            {"category": "ai_visibility", "status": "verified", "severity": "high"},
            {"category": "conversion_path", "status": "verified", "severity": "high"},
        ]
        result = core.select_service_route(
            ["ai_visibility", "conversion_path"], self.routes, findings=findings)
        self.assertEqual(result["fit"], "tie")
        self.assertIsNone(result["route_id"])
        self.assertEqual(
            sorted(result["tied_routes"]), ["content-visibility-demand", "digital-platforms-brand"])
        self.assertIn("strategic_recommendation", result["escalation"])

    def test_maturity_is_never_in_the_ranking_key(self):
        findings = [
            {"category": "ai_visibility", "status": "verified", "severity": "high"},
            {"category": "conversion_path", "status": "verified", "severity": "high"},
        ]
        result = core.select_service_route(
            ["ai_visibility", "conversion_path"], self.routes, findings=findings)
        maturities = {c["route_id"]: c["capability_maturity"] for c in result["candidates"]}
        self.assertEqual(maturities["content-visibility-demand"], "mature")
        for candidate in result["candidates"]:
            self.assertNotIn(candidate["capability_maturity"], candidate["ranking_key"])

    def test_buyer_role_breaks_a_tie_before_maturity(self):
        findings = [
            {"category": "ai_visibility", "status": "verified", "severity": "high"},
            {"category": "conversion_path", "status": "verified", "severity": "high"},
        ]
        result = core.select_service_route(
            ["ai_visibility", "conversion_path"], self.routes, findings=findings,
            buyer={"role": "Head of Sales"})
        self.assertEqual(result["route_id"], "digital-platforms-brand")
        self.assertEqual(result["won_on"], "buyer_relevance")

    def test_tie_break_order_matches_the_config(self):
        self.assertEqual(
            self.routes["tie_break"]["order"],
            ["evidence_strength", "commercial_pain", "buyer_relevance",
             "proof_fit", "urgency", "entry_offer_credibility"])

    def test_unmapped_gaps_produce_no_route(self):
        result = core.select_service_route(["something_unmapped"], self.routes)
        self.assertIsNone(result["route_id"])
        self.assertEqual(result["fit"], "none")

    def test_every_proof_asset_reference_resolves(self):
        known = {asset["id"] for asset in self.routes["proof_assets"]}
        for route in self.routes["routes"]:
            self.assertIn(route["proof_asset_id"], known)


class SliceTests(unittest.TestCase):
    def setUp(self):
        self.geo = load("run_geo_slice")
        self.market = load("run_market_discovery")
        self.examples = GTM_ROOT / "examples"

    def payload(self, name):
        return json.loads((self.examples / name).read_text(encoding="utf-8"))

    def test_geo_slice_reaches_awaiting_approval(self):
        record = self.geo.run(self.payload("geo-slice-input.json"), as_of="2026-08-11")
        self.assertEqual(record["lifecycle_stage"], "awaiting_approval")
        self.assertIn(record["qualification"]["tier"], ("HOT", "STRONG", "QUALIFIED"))
        self.assertEqual(record["qualification"]["model"], "qualification-v1")
        self.assertEqual(record["route"]["route_id"], "content-visibility-demand")
        self.assertFalse(record["external_action_authorized"])

    def test_geo_slice_only_cites_approved_claims(self):
        record = self.geo.run(self.payload("geo-slice-input.json"), as_of="2026-08-11")
        cited = {claim["id"] for claim in record["packet"]["body"]["cited_claims"]}
        self.assertNotIn("g4", cited)
        self.assertTrue(cited.issubset(set(record["evidence"]["approved_claim_ids"])))

    def test_missing_destination_cannot_reach_awaiting_approval(self):
        payload = self.payload("geo-slice-input.json")
        payload["buyer"]["email"] = None
        record = self.geo.run(payload, as_of="2026-08-11")
        self.assertIn(record["lifecycle_stage"], ("qualified", "outreach_prepared"))
        self.assertNotEqual(record["lifecycle_stage"], "awaiting_approval")
        # qualification-v1 blocks earlier than the packet builder did. A missing
        # destination is now a hard gate at qualification, so no packet is built.
        self.assertNotIn("packet", record)
        self.assertEqual(record["qualification"]["actionability"], "blocked_missing_destination")
        self.assertEqual(record["next_action"], "resolve_blocking_condition")
        self.assertIn(record["next_action"],
                      ("resolve_blocking_condition", "verify_exact_destination"))

    def test_geo_slice_blocks_without_a_diagnostic(self):
        record = self.geo.run(self.payload("geo-slice-input-no-diagnostic.json"), as_of="2026-08-11")
        # Strict sequencing: with no evidence, no qualification and no route, the
        # stage cannot jump to diagnostic_selected. Requesting a capability is not
        # a transition.
        self.assertEqual(record["lifecycle_stage"], "account_discovered")
        self.assertEqual(record["blocked_on"]["capability"], "geo-audit")
        self.assertNotIn("packet", record)

    def test_geo_slice_is_deterministic(self):
        payload = self.payload("geo-slice-input.json")
        first = self.geo.run(payload, as_of="2026-08-11")
        second = self.geo.run(self.payload("geo-slice-input.json"), as_of="2026-08-11")
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_market_slice_dedupes_and_ranks(self):
        record = self.market.run(self.payload("market-discovery-input.json"), as_of="2026-08-11")
        self.assertEqual(len(record["research_queue"]), 3)
        self.assertEqual(len(record["dedupe"]["merges"]), 1)
        self.assertEqual(len(record["dedupe"]["rejected"]), 1)
        scores = [row["qualification_score"] for row in record["research_queue"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        top = record["research_queue"][0]
        self.assertEqual(top["qualification_model"], "qualification-v1")
        self.assertIn(top["qualification_tier"], dict((n, t) for t, n in core.QUALIFICATION_TIERS))
        self.assertGreater(top["qualification_score"],
                           record["research_queue"][-1]["qualification_score"])

    def test_market_slice_is_order_independent(self):
        payload = self.payload("market-discovery-input.json")
        reversed_payload = dict(payload, candidates=list(reversed(payload["candidates"])))
        forward = self.market.run(payload, as_of="2026-08-11")["research_queue"]
        backward = self.market.run(reversed_payload, as_of="2026-08-11")["research_queue"]
        self.assertEqual([r["entity_key"] for r in forward], [r["entity_key"] for r in backward])

    def test_market_slice_blocks_without_candidates(self):
        record = self.market.run({"market": "test", "sector_hypothesis": "test"}, as_of="2026-08-11")
        self.assertEqual(record["lifecycle_stage"], "market_hypothesis")
        self.assertEqual(record["blocked_on"]["capability"], "competitive-research")

    def test_no_slice_output_authorizes_an_external_action(self):
        for name in ("geo-slice-input.json", "geo-slice-input-no-diagnostic.json"):
            record = self.geo.run(self.payload(name), as_of="2026-08-11")
            self.assertFalse(record["external_action_authorized"])
        record = self.market.run(self.payload("market-discovery-input.json"), as_of="2026-08-11")
        self.assertFalse(record["external_action_authorized"])


if __name__ == "__main__":
    unittest.main()
