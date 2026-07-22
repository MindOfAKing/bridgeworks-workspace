#!/usr/bin/env python3
"""
Reconciliation checks for the BridgeWorks cross-model content system.

Implements the mechanically-checkable items from the "Consistency and
reconciliation" list in operations/cross-model-content-cycle-runbook.md.
Several items on that list require human or model judgment (semantic
duplicates, claim contradictions) and are NOT implemented here. See
"What this does not check" below and README.md.

HOW TO USE
  Scan the default roots (bridgeworks-workspace content-relevant folders
  plus the local Content Studio mirror) for stale-client mentions and
  Content ID problems:
    python reconciliation_checks.py

  Scan specific paths instead:
    python reconciliation_checks.py --root "C:/Users/User/Projects/BridgeWorks-Content-Studio"

VALIDATION
  All ID format and semantic validation (shape, brand, channel-for-brand,
  ISO week, sequence range including rejecting 00) comes from
  id_validation.py, the same module content_id.py uses. This script does
  not define its own copy of what makes an ID valid -- see that module's
  docstring for the full rule set. The only thing still defined locally
  is CONTENT_ID_ATTEMPT_RE, a loose "this token is probably trying to be
  an ID" text-scanning heuristic used to find candidates worth validating;
  it is not itself a validation rule.

What this checks:
  1. Stale-client mentions: flags any text file containing "CEEFM" for
     manual review. Does not judge whether the mention is an approved,
     anonymized case-study reference (allowed) or an active-client
     framing (not allowed). That judgment needs a human or a model
     reading the surrounding sentence.
  2. Content ID / Master Thesis ID format AND semantic problems: any
     token that looks like it is attempting one of these IDs (starts
     with CONTENT- or THESIS-, followed by a 4-digit year) but does not
     pass id_validation's full check -- this now includes sequence 00,
     invalid ISO weeks, unknown brand codes, brand/channel combinations
     outside the permitted matrix, and malformed sequence values, not
     just the shape regex.
  3. Content ID reference classification. The same well-formed ID is
     legitimately expected to appear in more than one place across its
     lifecycle (ledger row, content-item record, approval card,
     publishing receipt, analytics record), so a flat "appears more
     than once" check is wrong. This tool instead separates:
       a. Duplicate ledger issuance -- the same ID on two or more rows
          of registry/content-id-ledger.csv or
          registry/master-thesis-ledger.csv. This is always a real bug.
       b. Multiple canonical content-item definitions -- the same
          Content ID declared as the "Content ID:" field of more than
          one record that is not itself an approval card, publishing
          receipt, or analytics record (see "How file role is decided"
          below). This is a real bug: two different records claiming
          to be the same content item.
       c. Legitimate downstream references -- the same "Content ID:"
          field appearing inside a record recognizable as an approval
          card, publishing receipt, or analytics record. Expected and
          not flagged; counted for visibility only.
       d. Master Thesis ID reuse -- "Master thesis ID:" is designed to
          be shared by every channel item under one weekly thesis.
          Never flagged; counted for visibility only.
       e. Everything else (an ID mentioned in prose, a code example, a
          filename, or documentation like the runbook's own
          "CONTENT-YYYY-WW-BRAND-CHANNEL-NN" illustration) is a bare
          mention, not a record. Never flagged.
     Only IDs that pass full validation (id_validation) are eligible to
     be counted as a canonical/downstream/thesis reference in the first
     place -- an invalid ID (e.g. sequence 00) is reported under check 2
     instead, not silently treated as a real reference.
  4. Exact-duplicate files: two or more files with an identical SHA-256
     hash (the same content saved twice under different names).

How file role is decided (for check 3): a text file is treated as an
approval card, publishing receipt, or analytics record if it contains a
line starting with one of the marker labels used by this system's own
templates ("Decision:", "What was published:", "Measurement date:").
Otherwise, any "Content ID:" field found in it is treated as a
canonical content-item definition. This is a file-level heuristic, not
a section-level one: it assumes one record per file, matching this
system's own template convention (copy one template, fill it, save it
as its own file). A file that deliberately mixes multiple records will
not be classified correctly; that is a known limitation, not a silent
guess dressed up as certainty.

What this does not check (needs human or AI-model judgment, not a script):
  - Semantic-duplicate detection (same message reworded)
  - Claim-contradiction detection (two units make incompatible claims)
  - Old-date / old-launch-language detection (superseded prices, past
    dates used as if current)
  - Simultaneous-writer detection (needs live process state, not files)
  - Approval-state conflict detection beyond the file-role heuristic
    above (needs the approval system, not just file content)
"""

import argparse
import csv
import hashlib
from pathlib import Path
import re
import sys

from id_validation import check_content_id, check_thesis_id

TEXT_EXTENSIONS = {".md", ".csv", ".txt", ".json"}
SKIP_DIR_NAMES = {"node_modules", ".git", "99_Superseded"}

CEEFM_RE = re.compile(r"CEEFM", re.IGNORECASE)

# Loose "this looks like an attempted ID" finder, not a validity check.
# Requires a 4-digit year right after the prefix so format placeholders
# in documentation, e.g. "CONTENT-YYYY-WW-BRAND-CHANNEL-NN", don't get
# picked up as candidates at all. Every candidate this finds is then
# validated for real via id_validation.check_content_id/check_thesis_id.
CONTENT_ID_ATTEMPT_RE = re.compile(r"\b(?:CONTENT|THESIS)-\d{4}-[A-Z0-9-]+\b")

CONTENT_ID_FIELD_RE = re.compile(r"^Content ID:\s*(\S.*?)\s*$")
THESIS_ID_FIELD_RE = re.compile(r"^Master thesis ID:\s*(\S.*?)\s*$")

DOWNSTREAM_MARKERS = (
    re.compile(r"^Decision:", re.MULTILINE),
    re.compile(r"^What was published:", re.MULTILINE),
    re.compile(r"^Measurement date:", re.MULTILINE),
)

LEDGER_FILES = {
    "content-id-ledger.csv": ("content_id", lambda v: check_content_id(v).fully_valid),
    "master-thesis-ledger.csv": ("thesis_id", lambda v: check_thesis_id(v).fully_valid),
}

DEFAULT_ROOTS = [
    "C:/Users/User/Projects/bridgeworks-workspace/operations",
    "C:/Users/User/Projects/bridgeworks-workspace/sessions",
    "C:/Users/User/Projects/bridgeworks-workspace/content",
    "C:/Users/User/Projects/BridgeWorks-Content-Studio",
]


def iter_text_files(root):
    root_path = Path(root)
    if not root_path.exists():
        print(f"  (root not found, skipping: {root})", file=sys.stderr)
        return
    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


# ---------------------------------------------------------------------------
# 1. Stale-client mentions
# ---------------------------------------------------------------------------

def check_stale_client(roots):
    hits = []
    for root in roots:
        for path in iter_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if CEEFM_RE.search(line):
                    hits.append((str(path), lineno, line.strip()[:160]))
    return hits


# ---------------------------------------------------------------------------
# 2. Content ID / Master Thesis ID format AND semantic problems
# ---------------------------------------------------------------------------

def check_content_id_format(roots):
    bad = []
    for root in roots:
        for path in iter_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                for m in CONTENT_ID_ATTEMPT_RE.finditer(line):
                    token = m.group(0)
                    if token.startswith("CONTENT-"):
                        result = check_content_id(token)
                    else:
                        result = check_thesis_id(token)
                    if not result.fully_valid:
                        reason = "; ".join(result.errors())
                        bad.append((str(path), lineno, token, reason))
    return bad


# ---------------------------------------------------------------------------
# 3. Content ID reference classification
# ---------------------------------------------------------------------------

def check_ledger_duplicates(roots):
    """Only looks at the two registry CSVs, wherever they appear under the
    scanned roots. Two or more rows issuing the same ID is always a bug."""
    problems = {}
    for root in roots:
        root_path = Path(root)
        if not root_path.exists():
            continue
        for filename, (id_column, is_valid) in LEDGER_FILES.items():
            for path in root_path.rglob(filename):
                if any(part in SKIP_DIR_NAMES for part in path.parts):
                    continue
                try:
                    with open(path, newline="", encoding="utf-8") as f:
                        rows = list(csv.DictReader(f))
                except OSError:
                    continue
                seen = {}
                for i, row in enumerate(rows, start=2):  # header is row 1
                    value = (row.get(id_column) or "").strip()
                    if is_valid(value):
                        seen.setdefault(value, []).append(i)
                for value, line_numbers in seen.items():
                    if len(line_numbers) > 1:
                        problems.setdefault(value, []).append(
                            (str(path), line_numbers)
                        )
    return problems


def classify_file_role(text):
    for marker in DOWNSTREAM_MARKERS:
        if marker.search(text):
            return "downstream"
    return "canonical"


def check_field_references(roots):
    """Scans text files (not the ledgers) for 'Content ID:' and 'Master
    thesis ID:' field lines, and classifies each occurrence. Only field
    values that pass full id_validation are counted here at all -- an
    invalid ID in a "Content ID:" field is reported by check 2, not
    silently folded into the reference counts."""
    canonical = {}   # id -> [(path, lineno), ...]
    downstream = {}  # id -> [(path, lineno), ...]
    thesis_refs = {}  # id -> [(path, lineno), ...]

    for root in roots:
        for path in iter_text_files(root):
            if path.name in LEDGER_FILES:
                continue  # ledgers are handled separately, with row semantics
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            role = classify_file_role(text)
            lines = text.splitlines()

            for lineno, line in enumerate(lines, start=1):
                m = CONTENT_ID_FIELD_RE.match(line.strip())
                if m and check_content_id(m.group(1)).fully_valid:
                    bucket = downstream if role == "downstream" else canonical
                    bucket.setdefault(m.group(1), []).append((str(path), lineno))

                m = THESIS_ID_FIELD_RE.match(line.strip())
                if m and check_thesis_id(m.group(1)).fully_valid:
                    thesis_refs.setdefault(m.group(1), []).append((str(path), lineno))

    return canonical, downstream, thesis_refs


# ---------------------------------------------------------------------------
# 4. Exact-duplicate files
# ---------------------------------------------------------------------------

def check_exact_duplicate_files(roots):
    by_hash = {}
    for root in roots:
        root_path = Path(root)
        if not root_path.exists():
            continue
        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
            by_hash.setdefault(digest, []).append(str(path))
    return {h: paths for h, paths in by_hash.items() if len(paths) > 1}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="BridgeWorks content reconciliation checks")
    parser.add_argument(
        "--root",
        action="append",
        dest="roots",
        help="Path to scan. Repeatable. Defaults to the content-relevant "
        "bridgeworks-workspace folders plus the local Content Studio mirror.",
    )
    args = parser.parse_args()
    roots = args.roots or DEFAULT_ROOTS

    print("Scanning:")
    for r in roots:
        print(f"  {r}")

    print("\n=== 1. Stale-client mentions (CEEFM) ===")
    stale = check_stale_client(roots)
    if not stale:
        print("  none found")
    for path, lineno, line in stale:
        print(f"  {path}:{lineno}: {line}")
    print(
        f"  -> {len(stale)} line(s) mention CEEFM. Review each: an approved, anonymized "
        f"or explicitly named (2026-07-14 consent) case-study reference is fine; an "
        f"active-client framing is not (CEEFM closed 2026-06-19, per current decision)."
    )

    print("\n=== 2. Content ID / Master Thesis ID format and semantic problems ===")
    bad_ids = check_content_id_format(roots)
    if not bad_ids:
        print("  no malformed or semantically invalid IDs found")
    for path, lineno, token, reason in bad_ids:
        print(f"  {path}:{lineno}: '{token}': {reason}")

    print("\n=== 3a. Duplicate ledger issuance (real bug if any) ===")
    ledger_dupes = check_ledger_duplicates(roots)
    if not ledger_dupes:
        print("  none found")
    for value, locations in ledger_dupes.items():
        print(f"  {value} issued more than once:")
        for path, line_numbers in locations:
            print(f"    {path} rows {line_numbers}")

    canonical, downstream, thesis_refs = check_field_references(roots)

    print("\n=== 3b. Multiple canonical content-item definitions (real bug if any) ===")
    canonical_dupes = {cid: locs for cid, locs in canonical.items() if len(locs) > 1}
    if not canonical_dupes:
        print("  none found")
    for cid, locs in canonical_dupes.items():
        print(f"  {cid} defined as a canonical record in {len(locs)} places:")
        for path, lineno in locs:
            print(f"    {path}:{lineno}")

    print("\n=== 3c. Legitimate downstream references (informational, not flagged) ===")
    if not downstream:
        print("  none found")
    for cid, locs in downstream.items():
        where = ", ".join(f"{Path(p).name}:{ln}" for p, ln in locs)
        print(f"  {cid}: {len(locs)} downstream reference(s) -- {where}")

    print("\n=== 3d. Master Thesis ID reuse across channel items (informational, not flagged) ===")
    if not thesis_refs:
        print("  none found")
    for tid, locs in thesis_refs.items():
        where = ", ".join(f"{Path(p).name}:{ln}" for p, ln in locs)
        print(f"  {tid}: referenced in {len(locs)} record(s) -- {where}")

    print("\n=== 4. Exact-duplicate files (same SHA-256) ===")
    dupe_files = check_exact_duplicate_files(roots)
    if not dupe_files:
        print("  no exact-duplicate files found")
    for digest, paths in dupe_files.items():
        print(f"  {digest[:12]}...:")
        for p in paths:
            print(f"    {p}")


if __name__ == "__main__":
    main()
