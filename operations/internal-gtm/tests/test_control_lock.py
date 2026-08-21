"""Single-writer ownership: conflict blocks, expiry heals, continuation works, release restores."""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GTM_ROOT / "scripts"))

import control_lock as cl  # noqa: E402

NOW = datetime(2026, 8, 11, 9, 0, tzinfo=timezone.utc)


class LockTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "locks.json"

    def tearDown(self):
        self.folder.cleanup()

    def test_a_conflicting_lock_blocks_the_write(self):
        cl.acquire("codex", "operating_state", "reconciling prospects", 60, self.path, NOW)
        with self.assertRaises(cl.LockConflict):
            cl.acquire("claude_code", "operating_state", "editing receipts", 60, self.path, NOW)

    def test_the_blocked_runtime_fails_closed_rather_than_waiting(self):
        cl.acquire("codex", "operating_state", "reconciling", 60, self.path, NOW)
        try:
            cl.acquire("claude_code", "operating_state", "same files", 60, self.path, NOW)
            self.fail("expected a conflict")
        except cl.LockConflict as exc:
            self.assertIn("Fail closed", str(exc))
            self.assertIn("codex", str(exc))

    def test_different_scopes_do_not_block_each_other(self):
        cl.acquire("codex", "operating_state", "reconciling", 60, self.path, NOW)
        lock = cl.acquire("claude_code", "implementation", "editing gtm_core", 60, self.path, NOW)
        self.assertEqual(lock["owner"], "claude_code")
        self.assertEqual(len(cl.active_locks(cl.load(self.path), NOW)), 2)

    def test_an_expired_lock_does_not_block_forever(self):
        cl.acquire("codex", "operating_state", "reconciling", 30, self.path, NOW)
        later = NOW + timedelta(minutes=31)
        self.assertEqual(cl.conflicting(cl.load(self.path), "claude_code", "operating_state", later), [])
        lock = cl.acquire("claude_code", "operating_state", "taking over", 60, self.path, later)
        self.assertEqual(lock["owner"], "claude_code")

    def test_expiry_is_recorded_not_silently_dropped(self):
        cl.acquire("codex", "operating_state", "reconciling", 30, self.path, NOW)
        data = cl._expire(cl.load(self.path), NOW + timedelta(minutes=31))
        self.assertEqual(data["locks"][0]["state"], cl.STATE_EXPIRED)
        self.assertIn("expired_at", data["locks"][0])

    def test_the_same_owner_continues_rather_than_stacking(self):
        first = cl.acquire("claude_code", "implementation", "part one", 30, self.path, NOW)
        second = cl.acquire("claude_code", "implementation", "part two", 30, self.path,
                            NOW + timedelta(minutes=5))
        self.assertEqual(first["lock_id"], second["lock_id"])
        self.assertEqual(second["continuations"], 1)
        self.assertEqual(second["task"], "part two")
        self.assertEqual(len(cl.active_locks(cl.load(self.path), NOW + timedelta(minutes=5))), 1)

    def test_continuation_extends_the_expiry(self):
        first = cl.acquire("claude_code", "implementation", "part one", 30, self.path, NOW)
        later = NOW + timedelta(minutes=20)
        second = cl.acquire("claude_code", "implementation", "part two", 30, self.path, later)
        self.assertGreater(second["expires_at"], first["expires_at"])

    def test_release_restores_write_access(self):
        lock = cl.acquire("codex", "operating_state", "reconciling", 60, self.path, NOW)
        cl.release(lock["lock_id"], "codex", self.path, NOW)
        self.assertEqual(cl.conflicting(cl.load(self.path), "claude_code", "operating_state", NOW), [])
        taken = cl.acquire("claude_code", "operating_state", "now free", 60, self.path, NOW)
        self.assertEqual(taken["owner"], "claude_code")

    def test_only_the_holder_can_release(self):
        lock = cl.acquire("codex", "operating_state", "reconciling", 60, self.path, NOW)
        with self.assertRaises(cl.LockConflict):
            cl.release(lock["lock_id"], "claude_code", self.path, NOW)

    def test_a_lock_records_every_required_field(self):
        lock = cl.acquire("claude_code", "implementation", "arc requalification", 60,
                          self.path, NOW)
        for field in ("owner", "scope", "patterns", "task", "acquired_at",
                      "expires_at", "state", "released_at"):
            self.assertIn(field, lock, field)

    def test_ttl_is_bounded(self):
        lock = cl.acquire("claude_code", "implementation", "long task", 10_000, self.path, NOW)
        span = cl._parse(lock["expires_at"]) - cl._parse(lock["acquired_at"])
        self.assertLessEqual(span, timedelta(minutes=cl.MAX_TTL_MINUTES))


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "locks.json"

    def tearDown(self):
        self.folder.cleanup()

    def test_claude_code_owns_implementation(self):
        for target in ("scripts/gtm_core.py", "schemas/gtm-state.schema.json",
                       "tests/test_gtm_core.py", "service-routes.yaml"):
            decision = cl.may_write(target, "claude_code", self.path)
            self.assertTrue(decision["allowed"], target)

    def test_codex_owns_operating_state(self):
        for target in ("runs/telemetry/gtm-telemetry.jsonl",
                       "runs/transition-receipts/premier-fm.jsonl"):
            decision = cl.may_write(target, "codex", self.path)
            self.assertTrue(decision["allowed"], target)

    def test_codex_may_not_write_implementation(self):
        decision = cl.may_write("scripts/gtm_core.py", "codex", self.path)
        self.assertFalse(decision["allowed"])
        self.assertIn("may propose a change, not write it", decision["reason"])

    def test_claude_code_may_not_write_operating_state(self):
        decision = cl.may_write("runs/transition-receipts/premier-fm.jsonl",
                                "claude_code", self.path)
        self.assertFalse(decision["allowed"])
        self.assertIn("belongs to codex", decision["reason"])

    def test_require_write_raises_rather_than_returning_false(self):
        with self.assertRaises(cl.LockConflict):
            cl.require_write("scripts/gtm_core.py", "codex", lock_path=self.path)

    def test_an_absolute_path_resolves_to_the_same_decision(self):
        absolute = str(GTM_ROOT / "scripts" / "gtm_core.py")
        self.assertFalse(cl.may_write(absolute, "codex", self.path)["allowed"])

    def test_both_ownership_scopes_name_what_they_cover(self):
        for scope, rule in cl.OWNERSHIP.items():
            self.assertTrue(rule["covers"], scope)
            self.assertIn(rule["owner"], ("claude_code", "codex"))


if __name__ == "__main__":
    unittest.main()
