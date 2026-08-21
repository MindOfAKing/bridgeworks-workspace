#!/usr/bin/env python3
"""Native CLI for canonical qualification-v1, with labelled legacy read support.

The canonical qualification-v1 result has no `valid` field and never will. Older
callers that read `valid` are served by `legacy_view`, which translates at this
boundary. Nothing here writes a compatibility field back into the canonical schema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_core():
    candidates = [Path.cwd(), Path.home() / "Projects" / "bridgeworks-workspace"]
    for root in candidates:
        scripts = root / "operations" / "internal-gtm" / "scripts"
        if (scripts / "gtm_core.py").is_file():
            sys.path.insert(0, str(scripts))
            import gtm_core  # type: ignore
            return gtm_core
    raise RuntimeError("canonical internal-GTM core not found")


def score(data: dict) -> dict:
    core = _load_core()
    if data.get("qualification_version") == core.QUALIFICATION_VERSION or "components" in data:
        scripts = Path(core.__file__).resolve().parent
        sys.path.insert(0, str(scripts))
        import qualification_v1  # type: ignore
        return qualification_v1.derive_and_score(
            data.get("components") or {}, data.get("evidence") or {},
            data.get("context") or {}, data.get("as_of") or "unknown")
    result = core.score_legacy_readiness(data)
    result.update({
        "state_ownership": False,
        "status_scope": "historical_compatibility_only",
        "requires_qualification_v1_rescore": True,
    })
    return result


def is_canonical(result: dict) -> bool:
    """A qualification-v1 result. It has no `valid` field and must not gain one."""
    return "qualification_version" in result or result.get("model") == "qualification-v1"


def legacy_view(result: dict) -> dict:
    """Translate at the wrapper boundary, so the canonical schema stays clean.

    Older callers read `valid` and `errors`. qualification-v1 has neither, because
    scoring either produced a result or raised. Adding `valid` to the canonical
    schema to satisfy a CLI would put a compatibility field in the model itself,
    which is exactly what the decision forbids. So the shim lives here.
    """
    if not is_canonical(result):
        return {"valid": bool(result.get("valid")), "errors": result.get("errors", [])}
    return {
        "valid": True,
        "errors": [],
        "note": ("qualification-v1 carries no `valid` field. A returned result is a "
                 "successful scoring. Actionability is a separate field and is not "
                 "a validity signal."),
        "actionability": result.get("actionability"),
        "translated_at": "wrapper boundary, not in the canonical schema",
    }


def exit_code(result: dict) -> int:
    """Zero when scoring succeeded. Actionability never changes the exit code."""
    if is_canonical(result):
        return 0
    return 0 if result.get("valid") else 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: score_prospect.py <prospect.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = score(data)
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 1
    payload = dict(result)
    payload["legacy_compatibility"] = legacy_view(result)
    print(json.dumps(payload, indent=2))
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
