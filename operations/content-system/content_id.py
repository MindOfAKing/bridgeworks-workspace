#!/usr/bin/env python3
"""
Content ID and Master Thesis ID generator/validator for the BridgeWorks
cross-model content system.

HOW TO USE
  Generate a new Content ID (auto-assigns the next sequence number):
    python content_id.py new --brand BW --channel LI --date 2026-07-22

  Validate an existing ID:
    python content_id.py check CONTENT-2026-30-BW-LI-01

  Generate a new Master Thesis ID for a week:
    python content_id.py new-thesis --date 2026-07-22

  List all IDs issued so far:
    python content_id.py list

IDs are appended to registry/content-id-ledger.csv and
registry/master-thesis-ledger.csv so sequence numbers never repeat and
duplicates are refused. Both ledgers are the source of truth for "next NN";
do not hand-edit them without understanding the sequencing logic below.

VALIDATION
  The ID formats, the brand/channel matrix, ISO week validation, and
  sequence-range validation (01-99, never 00) all live in
  id_validation.py and are imported here, not redefined. Keep it that
  way -- reconciliation_checks.py imports the same module so the two
  scripts cannot silently drift apart on what counts as a valid ID.

CONCURRENCY
  Claude Code Desktop, Claude Code VS Code, and Codex can all invoke this
  script against the same ledger files. Each `new` / `new-thesis` call
  takes an exclusive, Windows-safe, dependency-free file lock (atomic
  `O_CREAT | O_EXCL` file creation, stdlib only, no fcntl/msvcrt) around
  its own ledger before reading "what's the next sequence number" and
  writing the new row. A second process that arrives while the lock is
  held waits (default up to 10s), then proceeds once free. A lock older
  than 30s is treated as abandoned (a crashed process) and broken so the
  tool cannot deadlock itself permanently. If the lock genuinely cannot
  be acquired in time, the tool exits with a clear error instead of
  guessing -- it never issues an ID without holding the lock.

Format (from operations/cross-model-content-cycle-runbook.md):
  CONTENT-YYYY-WW-BRAND-CHANNEL-NN
  Example: CONTENT-2026-30-BW-LI-01

Format (BridgeWorks convention, not yet named in the runbook, proposed
here to satisfy the "Master thesis ID" field required by
mobile-publishing-pack-spec.md):
  THESIS-YYYY-WW-NN
  Example: THESIS-2026-30-01

WW is a real ISO 8601 week number (1-52 or 1-53 depending on the year).
NN is a two-digit sequence, 01-99 -- 00 is never valid and issuance can
never produce it (next_content_sequence/next_thesis_sequence always
start counting at 1; see the assertion in new_content_id/new_thesis_id).

Brand and permitted channels (from operations/content-channel-model.md;
hardened per the 2026-07-22 correction passes):
  BW  BridgeWorks (company channels): LI, IG, FB, WA, X, TT
  EE  Emmanuel Ehigbai (personal channels): LI, IG, FB, WA only

  EE has no X or TT combination under the current channel model --
  personal X/TikTok presence is not part of the approved system. BW
  channel meanings: LI = BridgeWorks Page, IG = @bridgeworksagency,
  FB = BridgeWorks Page, WA = Hungarian WhatsApp Business (preparation
  only), X = reserved for days 31-60, TT = reserved for days 61-90.
  EE channel meanings: LI = personal profile, IG = personal, FB =
  personal, WA = Nigerian WhatsApp Status (manual posting only).

This script only issues and validates IDs. It does not decide what gets
approved or published. See cross-model-content-cycle-runbook.md for that.
"""

import argparse
import contextlib
import csv
from datetime import date, datetime, timezone
from pathlib import Path
import sys
import time

from id_validation import (
    BRAND_CHANNELS,
    BRAND_CODES,
    CONTENT_ID_RE,
    MAX_SEQUENCE,
    MIN_SEQUENCE,
    THESIS_ID_RE,
    channel_allowed,
    check_content_id,
    check_thesis_id,
)

ROOT = Path(__file__).resolve().parent
CONTENT_LEDGER = ROOT / "registry" / "content-id-ledger.csv"
THESIS_LEDGER = ROOT / "registry" / "master-thesis-ledger.csv"

LOCK_TIMEOUT_SECONDS = 10
LOCK_STALE_SECONDS = 30
LOCK_POLL_SECONDS = 0.05


# ---------------------------------------------------------------------------
# Locking / atomic ledger access
# ---------------------------------------------------------------------------

@contextlib.contextmanager
def locked_ledger(ledger_path):
    """
    Exclusive mutex for one ledger file, using atomic exclusive file
    creation (os.O_CREAT | os.O_EXCL, via the "x" open mode). This is
    atomic at the OS level on both Windows and POSIX, so it needs no
    third party dependency and no platform-specific module (no fcntl,
    no msvcrt). Only one process can hold the lock at a time; everyone
    else waits or times out. The read-check-write sequence for issuing
    an ID must happen entirely inside this context so two concurrent
    callers can never both compute the same "next sequence number".
    """
    lock_path = ledger_path.with_name(ledger_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    acquired = False
    while not acquired:
        try:
            fd = open(lock_path, "x")
            fd.close()
            acquired = True
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
            except OSError:
                age = 0.0
            if age > LOCK_STALE_SECONDS:
                # Almost certainly a crashed process left this behind.
                # Break it rather than deadlocking every future run.
                try:
                    lock_path.unlink()
                except OSError:
                    pass
                continue
            if time.monotonic() - start > LOCK_TIMEOUT_SECONDS:
                raise SystemExit(
                    f"Could not acquire the lock on {ledger_path.name} within "
                    f"{LOCK_TIMEOUT_SECONDS}s ({lock_path.name} held by another "
                    f"process). Another Claude Code interface or Codex may be "
                    f"issuing an ID right now. Try again."
                )
            time.sleep(LOCK_POLL_SECONDS)
    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Ledger I/O
# ---------------------------------------------------------------------------

def read_ledger(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_ledger(path, fieldnames, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Issuance
# ---------------------------------------------------------------------------

def iso_year_week(d):
    iso = d.isocalendar()
    return iso[0], iso[1]


def next_sequence(existing_ids, prefix, id_re):
    """Always returns at least MIN_SEQUENCE (1): max(..., default=0) + 1
    can never be 0, so sequence 00 cannot be issued by construction, not
    just by convention. See the assertion at each call site."""
    used = []
    for cid in existing_ids:
        if cid.startswith(prefix):
            m = id_re.match(cid)
            if m:
                used.append(int(m.group("seq")))
    return max(used, default=0) + 1


def new_content_id(brand, channel, on_date):
    brand = brand.upper()
    channel = channel.upper()
    if brand not in BRAND_CODES:
        raise SystemExit(f"Unknown brand code '{brand}'. Use one of: {sorted(BRAND_CODES)}")
    if not channel_allowed(brand, channel):
        raise SystemExit(
            f"'{channel}' is not a permitted channel for brand '{brand}'. "
            f"{brand} is allowed: {sorted(BRAND_CHANNELS[brand])}"
        )

    year, week = iso_year_week(on_date)
    prefix = f"CONTENT-{year}-{week:02d}-{brand}-{channel}-"

    with locked_ledger(CONTENT_LEDGER):
        rows = read_ledger(CONTENT_LEDGER)
        existing_ids = [r["content_id"] for r in rows]
        seq = next_sequence(existing_ids, prefix, CONTENT_ID_RE)
        assert seq >= MIN_SEQUENCE, "sequence counter produced a value below 1"
        if seq > MAX_SEQUENCE:
            raise SystemExit(
                f"Sequence overflow: {prefix}NN already has {MAX_SEQUENCE} IDs issued "
                f"for {year} week {week:02d}, brand {brand}, channel {channel}. "
                f"Refusing to issue a 3-digit sequence that would break the "
                f"CONTENT-YYYY-WW-BRAND-CHANNEL-NN format."
            )
        new_id = f"{prefix}{seq:02d}"

        if new_id in existing_ids:
            raise SystemExit(f"Refusing to issue duplicate ID {new_id}. Check the ledger.")

        append_ledger(
            CONTENT_LEDGER,
            ["content_id", "issued_utc", "brand", "channel", "year", "week", "notes"],
            {
                "content_id": new_id,
                "issued_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "brand": brand,
                "channel": channel,
                "year": str(year),
                "week": f"{week:02d}",
                "notes": "",
            },
        )
    return new_id


def new_thesis_id(on_date):
    year, week = iso_year_week(on_date)
    prefix = f"THESIS-{year}-{week:02d}-"

    with locked_ledger(THESIS_LEDGER):
        rows = read_ledger(THESIS_LEDGER)
        existing_ids = [r["thesis_id"] for r in rows]
        seq = next_sequence(existing_ids, prefix, THESIS_ID_RE)
        assert seq >= MIN_SEQUENCE, "sequence counter produced a value below 1"
        if seq > MAX_SEQUENCE:
            raise SystemExit(
                f"Sequence overflow: {prefix}NN already has {MAX_SEQUENCE} IDs issued "
                f"for {year} week {week:02d}. Refusing to issue a 3-digit sequence "
                f"that would break the THESIS-YYYY-WW-NN format."
            )
        new_id = f"{prefix}{seq:02d}"

        if new_id in existing_ids:
            raise SystemExit(f"Refusing to issue duplicate ID {new_id}. Check the ledger.")

        append_ledger(
            THESIS_LEDGER,
            ["thesis_id", "issued_utc", "year", "week", "notes"],
            {
                "thesis_id": new_id,
                "issued_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "year": str(year),
                "week": f"{week:02d}",
                "notes": "",
            },
        )
    return new_id


# ---------------------------------------------------------------------------
# Check / list
# ---------------------------------------------------------------------------

def _report_check(value, kind, result):
    """Never prints "well-formed" or "valid" unless shape AND every
    semantic check (brand, channel-for-brand, ISO week, sequence range)
    has already passed. A shape match that fails semantics is reported
    as exactly that -- matches the shape, fails validation -- not as a
    qualified or partial "well-formed" ID."""
    if result.fully_valid:
        print(f"{value}: valid {kind}")
        print(f"  {result.describe()}")
        return
    print(f"{value}: matches the {kind} shape but fails validation")
    for err in result.errors():
        print(f"  - {err}")
    raise SystemExit(1)


def check_id(value):
    content_result = check_content_id(value)
    if content_result.shape_ok:
        _report_check(value, "Content ID", content_result)
        return

    thesis_result = check_thesis_id(value)
    if thesis_result.shape_ok:
        _report_check(value, "Master Thesis ID", thesis_result)
        return

    print(f"{value}: does not match CONTENT-YYYY-WW-BRAND-CHANNEL-NN or THESIS-YYYY-WW-NN")
    raise SystemExit(1)


def list_ids():
    content_rows = read_ledger(CONTENT_LEDGER)
    thesis_rows = read_ledger(THESIS_LEDGER)
    print(f"Content IDs issued: {len(content_rows)}")
    for r in content_rows:
        print(f"  {r['content_id']}  ({r['issued_utc']})")
    print(f"Master Thesis IDs issued: {len(thesis_rows)}")
    for r in thesis_rows:
        print(f"  {r['thesis_id']}  ({r['issued_utc']})")


def parse_date(value):
    if value is None:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def main():
    parser = argparse.ArgumentParser(description="BridgeWorks Content ID / Master Thesis ID tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Issue a new Content ID")
    p_new.add_argument("--brand", required=True, help="BW or EE")
    p_new.add_argument("--channel", required=True, help="LI, IG, FB, WA, and for BW only, X or TT")
    p_new.add_argument("--date", help="YYYY-MM-DD, defaults to today")

    p_thesis = sub.add_parser("new-thesis", help="Issue a new Master Thesis ID")
    p_thesis.add_argument("--date", help="YYYY-MM-DD, defaults to today")

    p_check = sub.add_parser("check", help="Validate an existing ID's format")
    p_check.add_argument("id_value")

    sub.add_parser("list", help="List all IDs issued so far")

    args = parser.parse_args()

    try:
        if args.command == "new":
            on_date = parse_date(args.date)
            print(new_content_id(args.brand, args.channel, on_date))
        elif args.command == "new-thesis":
            on_date = parse_date(args.date)
            print(new_thesis_id(on_date))
        elif args.command == "check":
            check_id(args.id_value)
        elif args.command == "list":
            list_ids()
    except SystemExit as e:
        # Route explicit SystemExit(str) messages to stderr with a clean
        # exit code, rather than letting Python decide the framing.
        if e.code is not None and not isinstance(e.code, int):
            print(str(e.code), file=sys.stderr)
            sys.exit(1)
        raise


if __name__ == "__main__":
    main()
