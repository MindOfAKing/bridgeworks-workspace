#!/usr/bin/env python3
"""Adapter between the internal GTM role model and the canonical capability registry.

HOW TO USE
    python operations/internal-gtm/scripts/capability_loader.py check
Prints the registry path, the role/capability counts, and any dangling reference.
Exit code 1 means a role points at a capability that does not exist.

There is exactly one capability registry: skill-governance/capability-registry.yaml.
This module reads it. It never writes it and never creates a second one.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
CANONICAL_REGISTRY = REPO_ROOT / "skill-governance" / "capability-registry.yaml"
ROLE_REGISTRY = GTM_ROOT / "role-registry.yaml"
ROUTING_POLICY = GTM_ROOT / "routing-policy.yaml"
SERVICE_ROUTES = GTM_ROOT / "service-routes.yaml"

# Role authority values that may never trigger an external action on their own.
NON_EXTERNAL_AUTHORITIES = {
    "read_only",
    "draft_only",
    "recommend_only",
    "internal_state_only",
    "repo_change_with_review",
    "internal_config_with_review",
}


class PolicyError(RuntimeError):
    """Raised when a call would break a GTM architecture rule."""


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry(path: Path = CANONICAL_REGISTRY) -> dict:
    return _read(path)


def load_roles(path: Path = ROLE_REGISTRY) -> dict:
    return _read(path)


def load_routing(path: Path = ROUTING_POLICY) -> dict:
    return _read(path)


def load_service_routes(path: Path = SERVICE_ROUTES) -> dict:
    return _read(path)


def assert_single_registry(gtm_root: Path = GTM_ROOT) -> None:
    """Fail if a second capability registry has been added under internal-gtm."""
    strays = [
        p for p in gtm_root.rglob("*")
        if p.is_file() and p.name.lower().startswith("capability-registry")
    ]
    if strays:
        listed = ", ".join(str(p.relative_to(gtm_root)) for p in strays)
        raise PolicyError(f"second capability registry found under internal-gtm: {listed}")


def capability_index(registry: dict | None = None) -> dict[str, dict]:
    data = registry if registry is not None else load_registry()
    return {skill["id"]: skill for skill in data["skills"]}


def role_index(roles: dict | None = None) -> dict[str, dict]:
    data = roles if roles is not None else load_roles()
    return {role["id"]: role for role in data["roles"]}


def dangling_capability_references() -> list[tuple[str, str]]:
    known = set(capability_index())
    dangling: list[tuple[str, str]] = []
    for role in load_roles()["roles"]:
        for capability in role["capabilities"]:
            if capability not in known:
                dangling.append((role["id"], capability))
    return dangling


def capabilities_for_role(role_id: str) -> list[dict]:
    roles = role_index()
    if role_id not in roles:
        raise PolicyError(f"unknown role: {role_id}")
    index = capability_index()
    resolved = []
    for capability in roles[role_id]["capabilities"]:
        if capability not in index:
            raise PolicyError(f"role {role_id} references unregistered capability {capability}")
        if index[capability].get("status") != "active":
            raise PolicyError(
                f"role {role_id} references non-active capability {capability}: "
                f"{index[capability].get('status')}"
            )
        resolved.append(index[capability])
    return resolved


def require_capability(role_id: str, capability_id: str) -> dict:
    """Return the registry record only if this role is permitted to use it."""
    roles = role_index()
    if role_id not in roles:
        raise PolicyError(f"unknown role: {role_id}")
    if capability_id not in roles[role_id]["capabilities"]:
        raise PolicyError(f"role {role_id} is not permitted capability {capability_id}")
    index = capability_index()
    if capability_id not in index:
        raise PolicyError(f"capability {capability_id} is not in the canonical registry")
    capability = index[capability_id]
    if capability.get("status") != "active":
        raise PolicyError(
            f"capability {capability_id} is registered but not active: {capability.get('status')}"
        )
    return capability


def assert_no_external_action(role_id: str) -> None:
    role = role_index()[role_id]
    if role["authority"] not in NON_EXTERNAL_AUTHORITIES:
        raise PolicyError(
            f"role {role_id} claims authority {role['authority']}, which this runtime does not grant"
        )


def route_for_task(task: str) -> dict:
    for route in load_routing()["routes"]:
        if route["task"] == task:
            return route
    raise PolicyError(f"no routing rule for task: {task}")


def capability_call_request(role_id: str, capability_id: str, task: str, payload: dict) -> dict:
    """Describe a capability run for the runtime to execute. It does not run anything."""
    require_capability(role_id, capability_id)
    assert_no_external_action(role_id)
    route = route_for_task(task)
    return {
        "kind": "capability_call_required",
        "role": role_id,
        "capability": capability_id,
        "task": task,
        "runtime": route["default"],
        "approval_required": bool(route.get("approval_required")),
        "review_required": bool(route.get("review_required")),
        "validation": route.get("validation"),
        "payload": payload,
    }


def check() -> int:
    try:
        assert_single_registry()
    except PolicyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    registry = load_registry()
    roles = load_roles()
    dangling = dangling_capability_references()
    print(f"canonical registry: {CANONICAL_REGISTRY}")
    print(f"capabilities: {len(registry['skills'])}")
    print(f"roles: {len(roles['roles'])}")
    print(f"referenced capabilities: {len({c for r in roles['roles'] for c in r['capabilities']})}")
    if dangling:
        for role_id, capability in dangling:
            print(f"ERROR: role {role_id} references missing capability {capability}", file=sys.stderr)
        return 1
    print("dangling references: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
