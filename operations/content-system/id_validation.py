#!/usr/bin/env python3
"""
Shared Content ID / Master Thesis ID validation for the BridgeWorks
cross-model content system.

Single source of truth for the ID formats, the brand/channel matrix,
and what counts as a fully valid ID, so content_id.py (issuance) and
reconciliation_checks.py (scanning existing files) cannot drift apart.
Neither script should redefine these rules; both import this module.

Formats:
  CONTENT-YYYY-WW-BRAND-CHANNEL-NN
  THESIS-YYYY-WW-NN

WW must be a real ISO 8601 week (1-52 or 1-53 depending on the year).
NN must be 01-99. Sequence 00 is not a valid sequence position (there
is no "zeroth" item), and issuance is designed so it can never produce
it: next_content_sequence/next_thesis_sequence in content_id.py always
compute max(existing, default=0) + 1, so the first ID issued for any
combination is already 01.

A value can match the CONTENT-/THESIS- shape (the right number of
hyphen-delimited groups, right digit counts) while still being
semantically invalid: an unknown brand, a channel not permitted for
that brand, a week that isn't a real ISO week, or a sequence of 00 or
outside 01-99. check_content_id() / check_thesis_id() return a result
object that keeps "matches the shape" and "is fully valid" as two
separate questions, on purpose -- calling something "well-formed" or
"valid" is only correct once both are true.
"""

from dataclasses import dataclass
from datetime import date
import re

BRAND_CHANNELS = {
    "BW": {"LI", "IG", "FB", "WA", "X", "TT"},
    "EE": {"LI", "IG", "FB", "WA"},
}
BRAND_CODES = set(BRAND_CHANNELS)
CHANNEL_CODES = {c for channels in BRAND_CHANNELS.values() for c in channels}

MIN_SEQUENCE = 1
MAX_SEQUENCE = 99

CONTENT_ID_RE = re.compile(
    r"^CONTENT-(?P<year>\d{4})-(?P<week>\d{2})-(?P<brand>[A-Z]+)-(?P<channel>[A-Z]+)-(?P<seq>\d{2})$"
)
THESIS_ID_RE = re.compile(r"^THESIS-(?P<year>\d{4})-(?P<week>\d{2})-(?P<seq>\d{2})$")


def is_valid_iso_week(year, week):
    """A year only has 52 or 53 ISO weeks. Reject anything outside that,
    including week 00, which the regex shape alone would not catch."""
    try:
        date.fromisocalendar(year, week, 1)
        return True
    except ValueError:
        return False


def is_valid_sequence(seq):
    return MIN_SEQUENCE <= seq <= MAX_SEQUENCE


def channel_allowed(brand, channel):
    return channel in BRAND_CHANNELS.get(brand, set())


@dataclass
class ContentIdCheck:
    raw: str
    shape_ok: bool
    year: int = None
    week: int = None
    brand: str = None
    channel: str = None
    seq: int = None
    brand_known: bool = False
    channel_permitted: bool = False
    week_valid: bool = False
    seq_valid: bool = False

    @property
    def fully_valid(self):
        return (
            self.shape_ok
            and self.brand_known
            and self.channel_permitted
            and self.week_valid
            and self.seq_valid
        )

    def errors(self):
        if not self.shape_ok:
            return ["does not match CONTENT-YYYY-WW-BRAND-CHANNEL-NN"]
        errs = []
        if not self.brand_known:
            errs.append(f"unknown brand '{self.brand}'")
        if self.brand_known and not self.channel_permitted:
            errs.append(
                f"channel '{self.channel}' not permitted for brand '{self.brand}' "
                f"(allowed: {sorted(BRAND_CHANNELS[self.brand])})"
            )
        if not self.week_valid:
            errs.append(f"week {self.week:02d} is not a valid ISO week for {self.year}")
        if not self.seq_valid:
            errs.append(
                f"sequence {self.seq:02d} is out of range "
                f"({MIN_SEQUENCE:02d}-{MAX_SEQUENCE:02d})"
            )
        return errs

    def describe(self):
        return (
            f"year={self.year} week={self.week:02d} brand={self.brand} "
            f"channel={self.channel} seq={self.seq:02d}"
        )


@dataclass
class ThesisIdCheck:
    raw: str
    shape_ok: bool
    year: int = None
    week: int = None
    seq: int = None
    week_valid: bool = False
    seq_valid: bool = False

    @property
    def fully_valid(self):
        return self.shape_ok and self.week_valid and self.seq_valid

    def errors(self):
        if not self.shape_ok:
            return ["does not match THESIS-YYYY-WW-NN"]
        errs = []
        if not self.week_valid:
            errs.append(f"week {self.week:02d} is not a valid ISO week for {self.year}")
        if not self.seq_valid:
            errs.append(
                f"sequence {self.seq:02d} is out of range "
                f"({MIN_SEQUENCE:02d}-{MAX_SEQUENCE:02d})"
            )
        return errs

    def describe(self):
        return f"year={self.year} week={self.week:02d} seq={self.seq:02d}"


def check_content_id(value):
    m = CONTENT_ID_RE.match(value)
    if not m:
        return ContentIdCheck(raw=value, shape_ok=False)
    d = m.groupdict()
    year, week, seq = int(d["year"]), int(d["week"]), int(d["seq"])
    brand, channel = d["brand"], d["channel"]
    brand_known = brand in BRAND_CODES
    return ContentIdCheck(
        raw=value,
        shape_ok=True,
        year=year,
        week=week,
        brand=brand,
        channel=channel,
        seq=seq,
        brand_known=brand_known,
        channel_permitted=brand_known and channel_allowed(brand, channel),
        week_valid=is_valid_iso_week(year, week),
        seq_valid=is_valid_sequence(seq),
    )


def check_thesis_id(value):
    m = THESIS_ID_RE.match(value)
    if not m:
        return ThesisIdCheck(raw=value, shape_ok=False)
    d = m.groupdict()
    year, week, seq = int(d["year"]), int(d["week"]), int(d["seq"])
    return ThesisIdCheck(
        raw=value,
        shape_ok=True,
        year=year,
        week=week,
        seq=seq,
        week_valid=is_valid_iso_week(year, week),
        seq_valid=is_valid_sequence(seq),
    )
