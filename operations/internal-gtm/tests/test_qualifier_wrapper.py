"""The native qualifier CLI serves legacy callers without polluting the canonical schema."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import gtm_core as core  # noqa: E402

WRAPPER = (REPO_ROOT / "operations" / "client-acquisition-engine" / "skill-repair-staging"
           / "bridgeworks-lead-qualifier" / "scripts" / "score_prospect.py")
INSTALLED = Path.home() / ".codex" / "skills" / "bridgeworks-lead-qualifier" / "scripts" / "score_prospect.py"

LEDGER = core.build_evidence_ledger(
    [{"id": "a", "subject": "problem_evidence", "value": "x", "status": "verified",
      "source": "https://e.com", "observed_at": "2026-08-10"}], as_of="2026-08-11")

CANONICAL_INPUT = {
    "qualification_version": "qualification-v1",
    "components": {
        "problem_evidence": {"score": 20, "evidence_ids": ["a"], "research_status": "complete"},
    },
    "evidence": LEDGER,
    "context": {"canonical_domain": "e.com", "contact_destination": "a@e.com",
                "service_route_exists": True},
    "as_of": "2026-08-11",
}

LEGACY_INPUT = {
    "ratings": {"fit": 22, "active_change": 22, "problem_evidence": 18,
                "capacity": 13, "buyer_access": 13},
    "verified_signal_count": 8,
    "reachable_buyer_path": True,
    "evidenced_service_route": True,
    "exclusions": [],
}


def load_wrapper():
    spec = importlib.util.spec_from_file_location("score_prospect", WRAPPER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def run_cli(payload: dict) -> tuple[int, dict]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(payload, handle)
        path = handle.name
    proc = subprocess.run([sys.executable, str(WRAPPER), path],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))
    try:
        return proc.returncode, json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.returncode, {"_stdout": proc.stdout, "_stderr": proc.stderr}


class WrapperRegressionTests(unittest.TestCase):
    """Regression: the CLI read `result["valid"]`, which qualification-v1 never has."""

    def test_a_canonical_result_does_not_crash_the_cli(self):
        code, payload = run_cli(CANONICAL_INPUT)
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload.get("qualification_version"), "qualification-v1")

    def test_the_canonical_schema_gains_no_valid_field(self):
        module = load_wrapper()
        result = module.score(CANONICAL_INPUT)
        self.assertNotIn("valid", result)
        self.assertNotIn("errors", result)

    def test_legacy_callers_are_served_at_the_boundary(self):
        code, payload = run_cli(CANONICAL_INPUT)
        self.assertEqual(code, 0)
        self.assertIn("legacy_compatibility", payload)
        self.assertTrue(payload["legacy_compatibility"]["valid"])
        self.assertIn("boundary", payload["legacy_compatibility"]["translated_at"])

    def test_a_legacy_payload_still_works(self):
        code, payload = run_cli(LEGACY_INPUT)
        self.assertEqual(code, 0, payload)
        self.assertTrue(payload["legacy_compatibility"]["valid"])
        self.assertTrue(payload.get("requires_qualification_v1_rescore"))

    def test_actionability_never_changes_the_exit_code(self):
        """A blocked prospect is a successful scoring, not a failed one."""
        module = load_wrapper()
        blocked = dict(CANONICAL_INPUT)
        blocked["context"] = {**CANONICAL_INPUT["context"], "contact_destination": None}
        result = module.score(blocked)
        self.assertNotEqual(result["actionability"], "actionable")
        self.assertEqual(module.exit_code(result), 0)

    def test_a_malformed_input_still_exits_non_zero(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            handle.write("{not json")
            path = handle.name
        proc = subprocess.run([sys.executable, str(WRAPPER), path],
                              capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(json.loads(proc.stdout)["valid"])

    def test_an_invalid_legacy_payload_exits_non_zero(self):
        code, _ = run_cli({"ratings": {"fit": "not an integer"}})
        self.assertEqual(code, 1)

    def test_the_installed_copy_matches_the_staged_source(self):
        if not INSTALLED.is_file():
            self.skipTest("qualifier not installed in the Codex estate")
        self.assertEqual(INSTALLED.read_bytes(), WRAPPER.read_bytes())

    def test_the_repair_did_not_touch_arc_operating_state(self):
        """This is an implementation fix. It must not have written prospect state."""
        source = WRAPPER.read_text(encoding="utf-8")
        for forbidden in ("arc-solutions", "runs/transition-receipts", "runs/intelligence"):
            self.assertNotIn(forbidden, source, forbidden)


if __name__ == "__main__":
    unittest.main()
