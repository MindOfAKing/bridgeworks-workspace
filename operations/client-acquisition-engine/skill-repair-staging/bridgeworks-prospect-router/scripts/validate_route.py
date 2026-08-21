#!/usr/bin/env python3
"""Compatibility CLI backed by canonical internal-GTM service-route controls."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_control():
    candidates = [Path.cwd(), Path.home() / "Projects" / "bridgeworks-workspace"]
    for root in candidates:
        scripts = root / "operations" / "internal-gtm" / "scripts"
        if (scripts / "gtm_core.py").is_file():
            sys.path.insert(0, str(scripts))
            import capability_loader  # type: ignore
            import gtm_core  # type: ignore
            return gtm_core, capability_loader.load_service_routes()
    raise RuntimeError("canonical internal-GTM control plane not found")


def validate(data: dict) -> dict:
    core, routes = _load_control()
    return core.validate_initial_contact_plan(data, routes)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_route.py <route.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = validate(data)
    except (OSError, json.JSONDecodeError, RuntimeError) as exc:
        result = {"valid": False, "errors": [str(exc)]}
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
