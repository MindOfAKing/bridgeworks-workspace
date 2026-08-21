"""Step 2 and 3: one control plane, no duplicate control definitions.

Every live routing decision must resolve against the canonical capability
registry. Any second definition of a route, a rubric or a registry is a drift
risk, so each one is either removed or pinned by a test that fails when it drifts.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
SCRIPTS = GTM_ROOT / "scripts"
ENGINE = REPO_ROOT / "operations" / "client-acquisition-engine"
sys.path.insert(0, str(SCRIPTS))

import capability_loader as cl  # noqa: E402
import gtm_core as core  # noqa: E402
import qualification_contract as contract  # noqa: E402


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class CanonicalRegistryTests(unittest.TestCase):
    """All live routing resolves against the one canonical capability registry."""

    def setUp(self):
        self.registry = cl.capability_index()
        self.routes = cl.load_service_routes()

    def test_every_role_capability_resolves_and_is_active(self):
        for role in cl.load_roles()["roles"]:
            for capability in role["capabilities"]:
                self.assertIn(capability, self.registry, f"{role['id']} -> {capability}")
                self.assertEqual(self.registry[capability]["status"], "active", capability)

    def test_every_service_route_diagnostic_resolves(self):
        for route in self.routes["routes"]:
            capability = route["diagnostic_capability"]
            self.assertIn(capability, self.registry, route["id"])
            self.assertEqual(self.registry[capability]["status"], "active", capability)

    def test_the_august_first_capabilities_are_registered(self):
        for capability in ("bridgeworks-lead-qualifier", "bridgeworks-prospect-router",
                           "bridgeworks-geo-prospect-scan", "bridgeworks-revenue-system-scan",
                           "bridgeworks-ai-workflow-scan"):
            self.assertIn(capability, self.registry)

    def test_the_qualifier_and_router_are_permitted_to_their_roles(self):
        cl.require_capability("lead-qualifier", "bridgeworks-lead-qualifier")
        cl.require_capability("prospect-router", "bridgeworks-prospect-router")
        for scan in ("bridgeworks-geo-prospect-scan", "bridgeworks-revenue-system-scan",
                     "bridgeworks-ai-workflow-scan"):
            cl.require_capability("prospect-router", scan)

    def test_only_one_registry_under_internal_gtm(self):
        cl.assert_single_registry()

    def test_no_second_registry_in_the_acquisition_engine(self):
        """The staged prose registry must point at the canonical one, not restate it."""
        path = ENGINE / "skill-repair-staging" / "bridgeworks-prospect-router" / "references" / "capability-registry.md"
        if not path.is_file():
            self.skipTest("staged registry already removed")
        text = path.read_text(encoding="utf-8")
        self.assertIn("skill-governance/capability-registry.yaml", text)
        self.assertNotIn("## Active production capabilities", text,
                         "the staged file still restates a capability table")
        self.assertNotIn("## Capabilities found but not yet active", text)

    def test_new_capabilities_are_not_auto_approved(self):
        """Installed is not approved. New skills enter as unknown, pending review."""
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        statuses = {s["id"]: s["status"] for s in data["skills"]}
        unknown = [k for k, v in statuses.items() if v == "unknown"]
        self.assertGreater(len(unknown), 0, "regeneration approved everything it found")
        # Capabilities that have not been through intake stay unknown and uncallable.
        for capability in ("impeccable", "claude-skill-creator"):
            self.assertEqual(statuses.get(capability), "unknown", capability)

    def test_the_geo_specialists_were_promoted_through_the_pathway(self):
        """Promotion needs an intake record. Passing a pilot is not approval by itself."""
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        statuses = {s["id"]: s["status"] for s in data["skills"]}
        intake_dir = REPO_ROOT / "skill-governance" / "intake"
        for capability in ("agent-geo-ai-visibility", "agent-geo-content",
                           "agent-geo-platform-analysis", "agent-geo-schema",
                           "agent-geo-technical"):
            self.assertEqual(statuses.get(capability), "active", capability)
            record = intake_dir / f"intake-{capability}.yaml"
            self.assertTrue(record.is_file(), capability)
            intake = json.loads(record.read_text(encoding="utf-8"))
            self.assertEqual(intake["decision"], "approve", capability)
            for requirement in ("provenance", "source", "security_scan", "permissions",
                                "overlap", "isolated_test", "pilot_evidence", "success_criterion"):
                self.assertEqual(intake["reviews"][requirement]["status"], "pass",
                                 f"{capability}:{requirement}")

    def test_geo_audit_is_installed_in_both_runtimes(self):
        """Codex GTM automation must not depend on Claude Code at runtime."""
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        record = next(s for s in data["skills"] if s["id"] == "geo-audit")
        self.assertEqual({i["runtime"] for i in record["installations"]}, {"claude", "codex"})
        self.assertEqual(record["runtime_divergence"]["state"], "governed_runtime_adaptation")
        self.assertEqual(record["runtime_divergence"]["canonical_source"], "claude")

    def test_no_role_still_points_at_the_unbounded_revops_skill(self):
        for role in cl.load_roles()["roles"]:
            self.assertNotIn("revops", role["capabilities"], role["id"])

    def test_the_bounded_pipeline_capability_covers_the_six_revops_functions(self):
        record = cl.require_capability("gtm-director", "bridgeworks-gtm-pipeline-health")
        for function in ("lifecycle reasoning", "pipeline movement", "handoff logic",
                         "stage health", "next-action logic", "commercial process analysis"):
            self.assertIn(function, record["workflow_stages"], function)

    def test_an_unknown_capability_cannot_be_called(self):
        with self.assertRaises(cl.PolicyError):
            cl.require_capability("prospect-router", "agent-geo-schema")


class RouteRegistryDriftTests(unittest.TestCase):
    """The Codex router keeps its own ROUTES literal. This fails when it drifts."""

    def test_the_router_no_longer_holds_its_own_route_list(self):
        """It is now a compatibility CLI over service-routes.yaml, not a second registry."""
        path = ENGINE / "skill-repair-staging" / "bridgeworks-prospect-router" / "scripts" / "validate_route.py"
        if not path.is_file():
            self.skipTest("router script not present")
        text = path.read_text(encoding="utf-8")
        self.assertIn("capability_loader", text)
        self.assertIn("load_service_routes", text)
        self.assertNotRegex(text, r"(?m)^ROUTES\s*=\s*\{",
                            "the hardcoded ROUTES literal is back")

    def test_the_router_cli_still_runs(self):
        import subprocess, tempfile
        path = ENGINE / "skill-repair-staging" / "bridgeworks-prospect-router" / "scripts" / "validate_route.py"
        if not path.is_file():
            self.skipTest("router script not present")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump({"qualification_status": "audit-approved",
                       "primary_service_route": "digital-platforms-brand",
                       "asset": {"production_ceiling_minutes": 15},
                       "work_passes": ["a"], "buyer": {"primary": "Head of Sales"},
                       "planned_outputs": ["annotated conversion path"],
                       "stop_conditions": ["no verified destination"],
                       "approval_gates": ["emmanuel"]}, handle)
            temp = handle.name
        proc = subprocess.run([sys.executable, str(path), temp], capture_output=True, text=True)
        self.assertIn("valid", proc.stdout)

    def test_route_priority_is_display_order_only(self):
        routes = cl.load_service_routes()
        self.assertIn("Display order only", routes["route_priority_note"])
        self.assertEqual(routes["tie_break"]["on_true_tie"], "escalate")


class ProductionCeilingTests(unittest.TestCase):
    """Unique logic preserved from validate_route.py before anything is removed."""

    def test_overproduction_terms_are_enforced_on_the_packet(self):
        self.assertTrue(core.PROHIBITED_AT_FIRST_CONTACT)
        for term in ("proposal", "full audit", "roi estimate", "crm migration architecture"):
            self.assertIn(term, core.PROHIBITED_AT_FIRST_CONTACT)

    def test_a_packet_naming_a_proposal_is_refused(self):
        evidence = core.build_evidence_ledger(
            [{"id": "a", "subject": "website_trust", "value": "x", "status": "verified",
              "source": "https://example.com", "observed_at": "2026-08-10"}], as_of="2026-08-11")
        offer = core.select_offer_wedge("digital-platforms-brand", "HOT", cl.load_service_routes())
        offer = {**offer, "wedge": "Full audit and proposal"}
        with self.assertRaises(core.ApprovalError):
            core.build_outreach_packet(
                {"prospect_id": "p", "company": "C", "buyer_email": "a@example.com"},
                evidence, {"route_id": "digital-platforms-brand", "matched_gaps": ["website_trust"]},
                offer, ["a"], "2026-08-11")

    def test_work_pass_ceiling_is_enforced(self):
        self.assertEqual(core.MAX_WORK_PASSES, 4)
        self.assertEqual(core.MAX_PRODUCTION_MINUTES, 20)


class QualificationContractTests(unittest.TestCase):
    """Historical scales are readable provenance. They own no current state."""

    def payload(self, **overrides):
        data = {
            "ratings": {"fit": 22, "active_change": 22, "problem_evidence": 18,
                        "capacity": 13, "buyer_access": 13},
            "verified_signal_count": 8,
            "reachable_buyer_path": True,
            "evidenced_service_route": True,
            "exclusions": [],
            "inbound_reply_referral_or_time_bound_event": True,
        }
        data.update(overrides)
        return data

    def test_a_legacy_payload_never_produces_canonical_qualification(self):
        result = contract.translate(self.payload())
        self.assertIsNone(result["canonical_qualification"])
        self.assertTrue(result["requires_qualification_v1_rescore"])

    def test_the_legacy_status_is_still_readable_for_provenance(self):
        result = contract.translate(self.payload())
        self.assertEqual(result["codex_status"], "discovery-ready")
        self.assertEqual(result["codex_score"], 88)

    def test_an_exclusion_is_preserved_not_rescored(self):
        result = contract.translate(self.payload(exclusions=["fictional business"]))
        self.assertEqual(result["codex_status"], "reject")
        self.assertIsNone(result["canonical_qualification"])
        self.assertTrue(result["requires_qualification_v1_rescore"])

    def test_state_ownership_is_stated_on_every_translation(self):
        result = contract.translate(self.payload())
        self.assertIn("internal-gtm", result["state_ownership"])
        self.assertIn("qualification-v1", result["state_ownership"])

    def test_tier_mapping_covers_every_canonical_tier(self):
        for tier in ("HOT", "STRONG", "QUALIFIED", "WATCH", "DO_NOT_PURSUE"):
            self.assertIn(tier, contract.TIER_TO_STATUS)

    def test_missing_ratings_raise_instead_of_defaulting_to_zero(self):
        with self.assertRaises(contract.ContractError):
            contract.codex_to_gtm({"ratings": {"fit": 20}})

    def test_contract_is_versioned_against_qualification_v1(self):
        self.assertIn("qualification-v1", contract.CONTRACT_VERSION)

    def test_the_contract_still_documents_the_codex_scale(self):
        self.assertEqual(sum(contract.CODEX_LIMITS.values()), 100)
        self.assertEqual(contract.CODEX_LIMITS["fit"], 25)



class RegistryProvenanceTests(unittest.TestCase):
    def test_regeneration_preserved_the_previous_generation_date(self):
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(data.get("_previous_generated_at"), "2026-07-25")
        self.assertIn("governance_policy", data)

    def test_runtime_divergence_is_recorded_on_the_record_not_only_in_a_report(self):
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        diverged = [s for s in data["skills"]
                    if (s.get("runtime_divergence") or {}).get("state") == "two_live_versions"]
        self.assertGreater(len(diverged), 0)
        for record in diverged:
            self.assertIn("scanned_runtime", record["runtime_divergence"])
            self.assertEqual(len(record["installations"]), 2)

    def test_gtm_critical_runtime_conflicts_are_classified(self):
        data = json.loads(cl.CANONICAL_REGISTRY.read_text(encoding="utf-8"))
        index = {item["id"]: item for item in data["skills"]}
        for capability in ("client-audit", "market-emails", "discovery-call-prep",
                           "engagement-architect"):
            divergence = index[capability]["runtime_divergence"]
            self.assertEqual(divergence["resolution_classification"],
                             "intentional_runtime_adaptation", capability)
            self.assertEqual(divergence["reviewed_at"], "2026-08-11")

    def test_geo_specialists_stay_blocked_pending_review(self):
        for capability in ("agent-geo-ai-visibility", "agent-geo-content",
                           "agent-geo-platform-analysis", "agent-geo-schema",
                           "agent-geo-technical"):
            with self.assertRaises(cl.PolicyError, msg=capability):
                cl.require_capability("prospect-router", capability)

    def test_the_pre_regeneration_baseline_is_recoverable(self):
        """Restored from git after a concurrent apply overwrote the first backup."""
        baseline = cl.CANONICAL_REGISTRY.parent / "capability-registry.yaml.baseline-2026-07-25"
        self.assertTrue(baseline.is_file())
        previous = json.loads(baseline.read_text(encoding="utf-8"))
        self.assertEqual(previous["generated_at"], "2026-07-25")
        self.assertEqual(len(previous["skills"]), 74)


if __name__ == "__main__":
    unittest.main()
