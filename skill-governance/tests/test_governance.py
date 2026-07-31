from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class RegistryTests(unittest.TestCase):
    def test_live_registry_validates(self):
        module = load("registry_tool")
        self.assertEqual(module.validate(), [])

    def test_malformed_registry_fails(self):
        module = load("registry_tool")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.yaml"
            path.write_text("{bad", encoding="utf-8")
            self.assertTrue(module.validate(path))

    def test_unknown_metadata_is_allowed(self):
        module = load("registry_tool")
        data = json.loads(module.REGISTRY.read_text(encoding="utf-8"))
        data["skills"][0]["inputs"] = ["unknown"]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "registry.yaml"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(module.validate(path), [])


class ScannerTests(unittest.TestCase):
    def test_rejects_target_outside_quarantine(self):
        with tempfile.TemporaryDirectory() as folder:
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "scan_skill.py"), folder],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("must be under", proc.stderr)

    def test_missing_scanner_fails(self):
        quarantine = ROOT / "quarantine"
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder) / "missing-scanner.exe"
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "scan_skill.py"), str(quarantine),
                 "--scanner", str(missing)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 3)

    def test_critical_result_is_nonzero(self):
        module = load("scan_skill")
        self.assertEqual(module.find_severity({"risk_assessment": {"severity": "CRITICAL"}}), "CRITICAL")
        self.assertNotEqual(module.result_exit(0, "CRITICAL"), 0)

    def test_warning_result_does_not_become_approval_error(self):
        module = load("scan_skill")
        self.assertEqual(module.result_exit(0, "MEDIUM"), 0)

    def test_install_hook_is_detected(self):
        module = load("scan_skill")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "setup.py").write_text("print('hook')", encoding="utf-8")
            self.assertIn("setup.py", module.find_install_hooks(path))


class DiffTests(unittest.TestCase):
    def test_duplicate_scores_above_unrelated(self):
        module = load("capability_diff")
        proposal = {"claimed_purpose": "Generate a BridgeWorks client proposal document"}
        duplicate = {"id": "x", "purpose": "Generate a BridgeWorks client proposal document",
                     "inputs": [], "outputs": [], "triggers": [], "tools": [],
                     "workflow_stages": [], "expected_deliverables": []}
        unrelated = {**duplicate, "purpose": "Analyze YouTube channel transcripts"}
        self.assertGreater(module.score(proposal, duplicate)[0], module.score(proposal, unrelated)[0])


class MarkItDownTests(unittest.TestCase):
    def test_missing_converter_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "manifest.json"
            manifest.write_text('{"samples":[]}', encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "markitdown_pilot.py"),
                 "--manifest", str(manifest), "--cli", str(Path(folder) / "missing.exe")],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 3)


if __name__ == "__main__":
    unittest.main()
