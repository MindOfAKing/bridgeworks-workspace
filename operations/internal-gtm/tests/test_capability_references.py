"""Every role capability must exist in the one canonical registry."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = GTM_ROOT / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class CapabilityReferenceTests(unittest.TestCase):
    def setUp(self):
        self.cl = load("capability_loader")

    def test_canonical_registry_exists(self):
        self.assertTrue(self.cl.CANONICAL_REGISTRY.is_file(), self.cl.CANONICAL_REGISTRY)

    def test_no_dangling_capability_references(self):
        self.assertEqual(self.cl.dangling_capability_references(), [])

    def test_only_one_capability_registry(self):
        self.cl.assert_single_registry()

    def test_second_registry_is_rejected(self):
        import tempfile

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "capability-registry.yaml").write_text("{}", encoding="utf-8")
            with self.assertRaises(self.cl.PolicyError):
                self.cl.assert_single_registry(path)

    def test_every_role_resolves(self):
        for role in self.cl.load_roles()["roles"]:
            resolved = self.cl.capabilities_for_role(role["id"])
            self.assertEqual(len(resolved), len(role["capabilities"]), role["id"])

    def test_role_cannot_borrow_another_roles_capability(self):
        with self.assertRaises(self.cl.PolicyError):
            self.cl.require_capability("data-steward", "geo-audit")

    def test_geo_audit_is_reused_not_reinvented(self):
        record = self.cl.require_capability("prospect-router", "geo-audit")
        self.assertEqual(record["id"], "geo-audit")

    def test_routing_sends_skill_engineering_to_claude_code(self):
        self.assertEqual(self.cl.route_for_task("skill_agent_engineering")["default"], "claude_code")

    def test_browser_shutdown_requires_approval(self):
        self.assertTrue(self.cl.route_for_task("browser_shutdown_or_console_action")["approval_required"])

    def test_capability_call_request_carries_runtime_and_no_authority_to_send(self):
        request = self.cl.capability_call_request(
            "prospect-router", "geo-audit", "diagnostic_capability_run", {"website_url": "https://example.com"}
        )
        self.assertEqual(request["runtime"], "claude_code")
        self.assertFalse(request["approval_required"])

    def test_unknown_task_raises(self):
        with self.assertRaises(self.cl.PolicyError):
            self.cl.route_for_task("send_the_email")

    def test_registered_but_unreviewed_capability_cannot_run(self):
        original_roles = self.cl.role_index
        original_capabilities = self.cl.capability_index
        try:
            self.cl.role_index = lambda roles=None: {
                "gtm-director": {"capabilities": ["candidate-skill"]}
            }
            self.cl.capability_index = lambda registry=None: {
                "candidate-skill": {"id": "candidate-skill", "status": "unknown"}
            }
            with self.assertRaises(self.cl.PolicyError):
                self.cl.require_capability("gtm-director", "candidate-skill")
        finally:
            self.cl.role_index = original_roles
            self.cl.capability_index = original_capabilities


if __name__ == "__main__":
    unittest.main()
