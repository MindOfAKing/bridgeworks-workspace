from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_design.py"
SPEC = importlib.util.spec_from_file_location("validate_design", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DesignTests(unittest.TestCase):
    def test_tokens_are_valid(self):
        self.assertEqual(MODULE.token_errors(), [])

    def test_authored_em_dash_fails_but_quote_is_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.md"
            path.write_text("Bad — sentence.\n> Quoted — source.\n", encoding="utf-8")
            errors = MODULE.content_errors(path)
            self.assertEqual(len(errors), 1)

    def test_unreviewed_css_colour_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.css"
            path.write_text("body { color: #FFFFFF; }", encoding="utf-8")
            self.assertTrue(MODULE.content_errors(path))


if __name__ == "__main__":
    unittest.main()
