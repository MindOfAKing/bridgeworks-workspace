"""Step 9: the shadow harness observes, it never acts."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = GTM_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(GTM_ROOT / "adapters"))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class ShadowTests(unittest.TestCase):
    def setUp(self):
        self.mod = load("shadow_log")

    def test_a_shadow_run_does_not_touch_the_engine(self):
        row = self.mod.build_row("2026-08-11")
        self.assertTrue(row["engine_untouched"])
        self.assertFalse(row["external_action_authorized"])

    def test_every_required_field_is_recorded(self):
        row = self.mod.build_row("2026-08-11")
        for field in ("old_workflow_action", "new_workflow_action", "pipeline_depth",
                      "qualified_untouched", "overdue_research", "missing_evidence",
                      "approvals_waiting", "new_supply_justified", "observed_difference",
                      "human_correction", "requires_qualification_v1"):
            self.assertIn(field, row)

    def test_the_old_job_is_evaluated_not_executed(self):
        row = self.mod.build_row("2026-08-11")
        self.assertIn(row["old_workflow_action"]["action"],
                      {"prepare_research_batch", "no_eligible_rows", "unavailable"})
        self.assertIn("would_prepare", row["old_workflow_action"])

    def test_appending_the_same_day_updates_rather_than_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / "shadow.jsonl"
            row = self.mod.build_row("2026-08-11")
            self.mod.append(row, log)
            result = self.mod.append(row, log)
            self.assertEqual(result["days_recorded"], 1)

    def test_a_human_correction_survives_a_rerun(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / "shadow.jsonl"
            row = self.mod.build_row("2026-08-11")
            row["human_correction"] = "Emmanuel: should have been advance_qualified_prospect"
            self.mod.append(row, log)
            self.mod.append(self.mod.build_row("2026-08-11"), log)
            stored = json.loads(log.read_text(encoding="utf-8").strip())
            self.assertIn("Emmanuel", stored["human_correction"])

    def test_cutover_is_not_ready_before_ten_days(self):
        result = self.mod.report(self.mod.LOG)
        self.assertEqual(result["days_required"], 10)
        if result["days_recorded"] < 10:
            self.assertFalse(result["ready_for_cutover"])

    def test_human_criteria_cannot_be_self_certified(self):
        result = self.mod.report(self.mod.LOG)
        self.assertIsNone(result["criteria"]["objectives_agreed_by_emmanuel"]["pass"])
        self.assertIsNone(result["criteria"]["blocked_days_matched_a_real_failure"]["pass"])


if __name__ == "__main__":
    unittest.main()
