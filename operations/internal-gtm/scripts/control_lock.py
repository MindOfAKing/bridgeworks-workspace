#!/usr/bin/env python3
"""Single-writer ownership for the internal-GTM control plane. Repo-local, no service.

HOW TO USE
    python operations/internal-gtm/scripts/control_lock.py status
    python operations/internal-gtm/scripts/control_lock.py acquire \
        --owner claude_code --scope implementation --task "arc requalification" --ttl 60
    python operations/internal-gtm/scripts/control_lock.py release --owner claude_code --lock <id>

Two runtimes editing the same control plane is how the Premier FM disagreement
started: one wrote a packet while the other was reconciling the state that packet
depended on. This makes that a failure instead of a race.

Ownership is standing. Locks are for the moment.

    claude_code   implementation writes: gtm_core, lifecycle, transitions,
                  qualification, routing, schemas, role and capability logic,
                  skills, agents, tests, refactoring.
    codex         operating-state writes: canonical prospect reconciliation,
                  migration state, execution receipts, shadow-run state, scheduler
                  state, approved browser actions, external execution records.

A runtime that meets an active conflicting lock **fails closed**. It does not wait,
retry or edit anyway. The state file is one JSON file in the repo, so any runtime
can read it without a database and the history travels with the commit.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

GTM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = GTM_ROOT.parents[1]
LOCK_FILE = GTM_ROOT / "control-plane" / "locks.json"

DEFAULT_TTL_MINUTES = 60
MAX_TTL_MINUTES = 240

# Standing ownership. Path patterns are relative to operations/internal-gtm.
OWNERSHIP = {
    "implementation": {
        "owner": "claude_code",
        "patterns": [
            "scripts/*.py", "adapters/*.py", "tests/*.py", "schemas/*.json",
            "role-registry.yaml", "routing-policy.yaml", "service-routes.yaml",
            "roles/*.md", "runtime-adaptations/*", "migration/verify_map.py",
            # A handoff is a proposal from implementation to operating state.
            # It is not canonical until Codex persists it as a receipt.
            "handoffs/*",
        ],
        "covers": ("gtm_core, lifecycle, transitions, qualification, routing, schemas, "
                   "role and capability logic, skills, agents, tests, refactoring"),
    },
    "operating_state": {
        "owner": "codex",
        "patterns": [
            "runs/*", "runs/**/*", "migration/phase-3/*.json",
            "control-plane/scheduler-state.json",
        ],
        "covers": ("canonical prospect reconciliation, migration state, execution "
                   "receipts, shadow-run state, scheduler state, approved browser "
                   "actions, external execution records"),
    },
}

STATE_ACTIVE = "active"
STATE_RELEASED = "released"
STATE_EXPIRED = "expired"


class LockConflict(RuntimeError):
    """Raised when a write would collide with another runtime's active lock."""


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(moment: datetime) -> str:
    return moment.isoformat()


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load(path: Path = LOCK_FILE) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": 1, "locks": []}


def save(data: dict, path: Path = LOCK_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _expire(data: dict, now: datetime | None = None) -> dict:
    """An expired lock stops blocking. It is never permanent."""
    now = now or _now()
    for lock in data["locks"]:
        if lock["state"] == STATE_ACTIVE and _parse(lock["expires_at"]) <= now:
            lock["state"] = STATE_EXPIRED
            lock["expired_at"] = _iso(now)
    return data


def active_locks(data: dict, now: datetime | None = None) -> list[dict]:
    return [lock for lock in _expire(data, now)["locks"] if lock["state"] == STATE_ACTIVE]


def scope_patterns(scope: str) -> list[str]:
    if scope in OWNERSHIP:
        return OWNERSHIP[scope]["patterns"]
    return [scope]


def _prefix(pattern: str) -> str:
    """The literal part of a pattern, before the first wildcard."""
    cut = len(pattern)
    for marker in ("*", "?", "["):
        found = pattern.find(marker)
        if found != -1:
            cut = min(cut, found)
    return pattern[:cut]


def _overlaps(a: list[str], b: list[str]) -> bool:
    """Two scopes conflict only when their paths can actually intersect.

    A shared first path segment is not enough. `migration/verify_map.py` is
    implementation and `migration/phase-3/*.json` is operating state; they live
    under the same folder and must not block each other.
    """
    for left in a:
        for right in b:
            if left == right:
                return True
            if fnmatch.fnmatch(left, right) or fnmatch.fnmatch(right, left):
                return True
            left_prefix, right_prefix = _prefix(left), _prefix(right)
            if not left_prefix or not right_prefix:
                continue
            longer, shorter = sorted((left_prefix, right_prefix), key=len, reverse=True)
            if longer.startswith(shorter) and (
                    shorter.endswith("/") or longer[len(shorter):].startswith("/")
                    or longer == shorter):
                return True
    return False


def conflicting(data: dict, owner: str, scope: str, now: datetime | None = None) -> list[dict]:
    wanted = scope_patterns(scope)
    return [lock for lock in active_locks(data, now)
            if lock["owner"] != owner and _overlaps(wanted, lock["patterns"])]


def acquire(owner: str, scope: str, task: str, ttl_minutes: int = DEFAULT_TTL_MINUTES,
            path: Path = LOCK_FILE, now: datetime | None = None) -> dict:
    """Take the lock, or fail closed. Never waits, never edits anyway."""
    now = now or _now()
    ttl = max(1, min(int(ttl_minutes), MAX_TTL_MINUTES))
    data = _expire(load(path), now)

    blockers = conflicting(data, owner, scope, now)
    if blockers:
        raise LockConflict(
            f"{owner} cannot take {scope}: held by "
            + ", ".join(f"{b['owner']} until {b['expires_at']} for {b['task']!r}" for b in blockers)
            + ". Fail closed: do not edit concurrently.")

    patterns = scope_patterns(scope)
    existing = next((lock for lock in active_locks(data, now)
                     if lock["owner"] == owner and _overlaps(patterns, lock["patterns"])), None)
    if existing:
        # Same owner continuing the same work. Extend rather than stack.
        existing["expires_at"] = _iso(now + timedelta(minutes=ttl))
        existing["task"] = task
        existing["continuations"] = existing.get("continuations", 0) + 1
        existing["last_continued_at"] = _iso(now)
        save(data, path)
        return existing

    lock = {
        "lock_id": uuid.uuid5(uuid.NAMESPACE_URL, f"{owner}:{scope}:{_iso(now)}").hex[:12],
        "owner": owner,
        "scope": scope,
        "patterns": patterns,
        "task": task,
        "acquired_at": _iso(now),
        "expires_at": _iso(now + timedelta(minutes=ttl)),
        "state": STATE_ACTIVE,
        "released_at": None,
        "continuations": 0,
    }
    data["locks"].append(lock)
    save(data, path)
    return lock


def release(lock_id: str, owner: str, path: Path = LOCK_FILE,
            now: datetime | None = None) -> dict:
    now = now or _now()
    data = load(path)
    for lock in data["locks"]:
        if lock["lock_id"] == lock_id:
            if lock["owner"] != owner:
                raise LockConflict(f"{owner} cannot release a lock held by {lock['owner']}")
            lock["state"] = STATE_RELEASED
            lock["released_at"] = _iso(now)
            save(data, path)
            return lock
    raise LockConflict(f"no such lock: {lock_id}")


def may_write(path_or_scope: str, owner: str, lock_path: Path = LOCK_FILE,
              now: datetime | None = None) -> dict:
    """Standing ownership plus live locks. Both must allow the write."""
    relative = path_or_scope
    for prefix in (str(GTM_ROOT).replace("\\", "/") + "/", "operations/internal-gtm/"):
        if relative.replace("\\", "/").startswith(prefix):
            relative = relative.replace("\\", "/")[len(prefix):]
            break

    standing = None
    for scope, rule in OWNERSHIP.items():
        if any(fnmatch.fnmatch(relative, pattern) for pattern in rule["patterns"]):
            standing = (scope, rule["owner"])
            break

    data = load(lock_path)
    blockers = [lock for lock in active_locks(data, now)
                if lock["owner"] != owner
                and any(fnmatch.fnmatch(relative, pattern) for pattern in lock["patterns"])]

    if standing and standing[1] != owner:
        return {"allowed": False, "path": relative, "owner": owner,
                "reason": (f"standing ownership: {standing[0]} belongs to {standing[1]}. "
                           f"{owner} may propose a change, not write it.")}
    if blockers:
        return {"allowed": False, "path": relative, "owner": owner,
                "reason": (f"active lock held by {blockers[0]['owner']} until "
                           f"{blockers[0]['expires_at']} for {blockers[0]['task']!r}"),
                "blocking_lock": blockers[0]["lock_id"]}
    return {"allowed": True, "path": relative, "owner": owner,
            "standing_scope": standing[0] if standing else "unowned"}


def require_write(path_or_scope: str, owner: str, **kwargs) -> None:
    """Fail closed. Call this before writing a control-plane file."""
    decision = may_write(path_or_scope, owner, **kwargs)
    if not decision["allowed"]:
        raise LockConflict(f"write refused for {decision['path']}: {decision['reason']}")


def status(path: Path = LOCK_FILE) -> dict:
    data = _expire(load(path))
    save(data, path)
    return {
        "lock_file": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "ownership": {scope: {"owner": rule["owner"], "covers": rule["covers"]}
                      for scope, rule in OWNERSHIP.items()},
        "active": [{k: lock[k] for k in ("lock_id", "owner", "scope", "task",
                                         "acquired_at", "expires_at", "state")}
                   for lock in data["locks"] if lock["state"] == STATE_ACTIVE],
        "history": len(data["locks"]),
        "policy": "a runtime meeting a conflicting active lock fails closed",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "acquire", "release", "check"))
    parser.add_argument("--owner", default=os.environ.get("GTM_RUNTIME", "claude_code"))
    parser.add_argument("--scope", default="implementation")
    parser.add_argument("--task", default="unspecified")
    parser.add_argument("--ttl", type=int, default=DEFAULT_TTL_MINUTES)
    parser.add_argument("--lock")
    parser.add_argument("--path")
    args = parser.parse_args()

    try:
        if args.command == "status":
            print(json.dumps(status(), indent=2, ensure_ascii=False))
        elif args.command == "acquire":
            lock = acquire(args.owner, args.scope, args.task, args.ttl)
            print(json.dumps(lock, indent=2, ensure_ascii=False))
        elif args.command == "release":
            print(json.dumps(release(args.lock, args.owner), indent=2, ensure_ascii=False))
        else:
            print(json.dumps(may_write(args.path or "", args.owner), indent=2, ensure_ascii=False))
    except LockConflict as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
