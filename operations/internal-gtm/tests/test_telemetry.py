"""Telemetry records decisions truthfully and never invents an outcome."""

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


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.mod = load("telemetry")
        self.runs = GTM_ROOT / "runs" / "geo"

    def test_every_listed_dimension_is_comparable(self):
        required = {
            "market", "segment", "trigger_type", "buyer_role", "buyer_reachability",
            "qualification_score", "qualification_tier", "problem_evidence",
            "commercial_fit", "buyer_accessibility", "trigger_urgency", "proof_fit",
            "execution_readiness", "primary_service_route",
            "diagnostic_capability", "diagnostic_score", "diagnostic_result",
            "proof_asset_id", "offer_hypothesis", "outreach_angle", "channel",
        }
        self.assertTrue(required.issubset(set(self.mod.DECISION_DIMENSIONS)))

    def test_record_matches_the_schema_shape(self):
        schema = json.loads((GTM_ROOT / "schemas" / "gtm-telemetry.schema.json").read_text(encoding="utf-8"))
        record = json.loads((self.runs / "gbs-africa-2026-08-11.json").read_text(encoding="utf-8"))
        row = self.mod.from_run_record(record, self.runs / "gbs-africa-2026-08-11.json")
        self.assertEqual(set(row), set(schema["properties"]))
        self.assertEqual(set(row["decision"]), set(schema["properties"]["decision"]["properties"]))
        self.assertEqual(set(row["outcome"]), set(schema["properties"]["outcome"]["properties"]))

    def test_decisions_are_captured_from_the_run(self):
        record = json.loads((self.runs / "gbs-africa-2026-08-11.json").read_text(encoding="utf-8"))
        row = self.mod.from_run_record(record, self.runs / "gbs-africa-2026-08-11.json")
        self.assertEqual(row["decision"]["primary_service_route"], "content-visibility-demand")
        self.assertIn(row["decision"]["diagnostic_capability"],
                      ("geo-audit", "bridgeworks-geo-prospect-scan"))
        self.assertEqual(row["decision"]["qualification_version"], "qualification-v1")
        self.assertIn(row["decision"]["qualification_tier"],
                      ("HOT", "STRONG", "QUALIFIED", "WATCH", "DO_NOT_PURSUE"))
        for name in ("problem_evidence", "commercial_fit", "buyer_accessibility",
                     "trigger_urgency", "proof_fit", "execution_readiness"):
            self.assertIn(name, row["decision"], name)
        self.assertEqual(row["decision"]["route_won_on"], "evidence_strength")
        # GBS Africa is blocked on contradicted evidence under qualification-v1, so
        # no offer or proof asset is selected. A null here is the correct record.
        self.assertIn(row["decision"]["proof_asset_id"], (None, "ceefm-geo-16-to-77"))

    def test_no_outcome_is_ever_invented(self):
        for path in sorted(self.runs.glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if not record.get("prospect"):
                continue
            row = self.mod.from_run_record(record, path)
            for field in ("sent_at", "sent_message_id", "reply_classification", "positive_reply",
                          "meeting_booked_at", "proposal_sent_at", "final_state", "revenue_if_won"):
                self.assertIsNone(row["outcome"][field], f"{path.name}:{field}")
            self.assertFalse(row["provenance"]["external_action_authorized"])

    def test_rebuild_never_clobbers_a_real_outcome(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "t.jsonl"
            self.mod.build(self.runs, store)
            rows = self.mod.load(store)
            rows[0]["outcome"]["sent_at"] = "2026-08-12T09:00:00+02:00"
            rows[0]["outcome"]["sent_message_id"] = "19ef5dd74e105f4e"
            store.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
            self.mod.build(self.runs, store)
            after = {r["record_id"]: r for r in self.mod.load(store)}
            self.assertEqual(after[rows[0]["record_id"]]["outcome"]["sent_at"], "2026-08-12T09:00:00+02:00")

    def test_rebuild_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "t.jsonl"
            first = self.mod.build(self.runs, store)
            body = store.read_text(encoding="utf-8")
            second = self.mod.build(self.runs, store)
            self.assertEqual(first["total"], second["total"])
            self.assertEqual(second["added"], 0)
            self.assertEqual(body, store.read_text(encoding="utf-8"))

    def test_every_canonical_prospect_has_a_telemetry_row(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "t.jsonl"
            self.mod.build(self.runs, store)
            rows = self.mod.load(store)
            represented = {row.get("entity_key") for row in rows if row.get("entity_key")}
            reconciliation = json.loads((GTM_ROOT / "migration" / "phase-3" /
                                         "prospect-reconciliation.json").read_text(encoding="utf-8"))
            expected = {entity["entity_key"] for entity in reconciliation["entities"]}
            self.assertTrue(expected.issubset(represented))

    def test_zero_denominator_rate_is_null_not_zero(self):
        record = json.loads((self.runs / "gbs-africa-2026-08-11.json").read_text(encoding="utf-8"))
        row = self.mod.from_run_record(record, self.runs / "gbs-africa-2026-08-11.json")
        result = self.mod.compare([row], "primary_service_route")
        group = next(iter(result["groups"].values()))
        self.assertEqual(group["counts"]["sent"], 0)
        self.assertIsNone(group["rates"]["sent_to_replied"]["rate"])

    def test_unsent_prospects_are_not_in_a_conversion_denominator(self):
        record = json.loads((self.runs / "gbs-africa-2026-08-11.json").read_text(encoding="utf-8"))
        row = self.mod.from_run_record(record, self.runs / "gbs-africa-2026-08-11.json")
        result = self.mod.compare([row], "qualification_tier")
        group = next(iter(result["groups"].values()))
        self.assertEqual(group["rates"]["prepared_to_sent"]["numerator"], 0)
        self.assertEqual(group["rates"]["prepared_to_sent"]["numerator"], 0,
                             "an unsent prospect must never count as sent")

    def test_a_verified_send_implies_the_prepared_stage(self):
        row = self.mod.from_run_record(
            json.loads((self.runs / "gbs-africa-2026-08-11.json").read_text(encoding="utf-8")),
            self.runs / "gbs-africa-2026-08-11.json")
        row["outcome"]["approval_state"] = None
        row["outcome"]["sent_at"] = "2026-08-11T08:00:00Z"
        result = self.mod.compare([row], "primary_service_route")
        group = result["groups"]["content-visibility-demand"]
        self.assertEqual(group["counts"]["prepared"], 1)
        self.assertEqual(group["counts"]["sent"], 1)

    def test_unknown_dimension_raises(self):
        with self.assertRaises(ValueError):
            self.mod.compare(self.mod.load(self.mod.STORE), "vibes")


if __name__ == "__main__":
    unittest.main()
