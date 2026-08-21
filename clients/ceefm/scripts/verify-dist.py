#!/usr/bin/env python3
"""Pre-upload check for the CEEFM Astro build.

Run against dist/ BEFORE `python deploy-ftp.py`. Catches a build that is
missing the Ads tag, the consent grants, the privacy pages, or .htaccess,
while the mistake is still free.

    python verify-dist.py C:/Users/User/ceefm-astro/dist

Exits 0 if every required check passes, 1 otherwise.
Stdlib only. Verifies build output, never the Google Ads account.
"""

import sys
import re
from pathlib import Path

GA4_ID = "G-F2TLLLG2DH"
ADS_ID = "AW-18378779634"
ADS_LABEL = "8ze4CP2Tyt4cEPLX17tE"
EVENT_NAME = "ads_conversion_Contact_Us_2"

PAGES = [
    "index.html",
    "contact/index.html",
    "hospitality/index.html",
    "residential/index.html",
    "lakopark/index.html",
    "vendeglatas/index.html",
    "privacy/index.html",
    "hu/index.html",
    "hu/kapcsolat/index.html",
    "hu/adatvedelem/index.html",
]

ASSETS = [".htaccess", "robots.txt", "llms.txt", ".well-known/security.txt"]

failures = []
warnings = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL  {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"  WARN  {msg}")


def ok(msg):
    print(f"  ok    {msg}")


def main(dist):
    dist = Path(dist)
    if not dist.is_dir():
        print(f"Not a directory: {dist}")
        return 1

    print(f"\nVerifying {dist}\n")

    print("Pages")
    html = {}
    for rel in PAGES:
        p = dist / rel
        if not p.is_file():
            fail(f"missing page {rel}")
            continue
        html[rel] = p.read_text(encoding="utf-8", errors="replace")
    if len(html) == len(PAGES):
        ok(f"all {len(PAGES)} pages present")

    print("\nTags")
    before = len(failures)
    for rel, body in html.items():
        if ADS_ID not in body:
            fail(f"{rel} missing {ADS_ID}")
        if GA4_ID not in body:
            fail(f"{rel} missing {GA4_ID}")
    if len(failures) == before and html:
        ok(f"{ADS_ID} and {GA4_ID} on every page")

    print("\nConsent Mode")
    before = len(failures)
    for rel, body in html.items():
        if "'default'" not in body and '"default"' not in body:
            fail(f"{rel} has no consent default block")
            continue
        # the default block must deny ad_storage before any choice is made
        head = body[: body.find("googletagmanager.com/gtag/js")] or body
        if "denied" not in head:
            fail(f"{rel} consent default does not deny before gtag.js loads")
        if "granted" not in body:
            fail(f"{rel} has no consent grant path, Accept would never grant")
    if len(failures) == before and html:
        ok("consent default denies, grant path present, on every page")

    print("\nConversion binding")
    bundles = list((dist / "_astro").glob("ContactForm*.js")) if (dist / "_astro").is_dir() else []
    if not bundles:
        fail("no ContactForm*.js bundle found in dist/_astro")
    else:
        src = "\n".join(b.read_text(encoding="utf-8", errors="replace") for b in bundles)
        by_label = ADS_LABEL in src
        by_event = EVENT_NAME in src
        if by_label and by_event:
            warn("bundle fires BOTH the label and the event name, risk of double counting")
        elif by_label:
            ok(f"bound by label, send_to {ADS_ID}/{ADS_LABEL} (Option A)")
        elif by_event:
            ok(f"bound by event name, {EVENT_NAME} (current production)")
        else:
            fail("bundle fires no Ads conversion at all")

        # regression guard on the Web3Forms false-success fix
        if re.search(r"\.ok\s*\?", src) and "success" not in src:
            fail("form appears to trust response.ok alone, the false-success bug is back")
        else:
            ok("form parses the response body, not just response.ok")

    print("\nStatic assets")
    for rel in ASSETS:
        p = dist / rel
        if p.is_file():
            ok(rel)
        else:
            fail(f"missing {rel}")

    ht = dist / ".htaccess"
    if ht.is_file():
        body = ht.read_text(encoding="utf-8", errors="replace")
        for token, label in [("Strict-Transport-Security", "HSTS"),
                             ("Content-Security-Policy", "CSP")]:
            if token not in body:
                fail(f".htaccess missing {label}")

    print("\nSitemap")
    sm = dist / "sitemap-0.xml"
    if not sm.is_file():
        fail("missing sitemap-0.xml")
    else:
        locs = re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8", errors="replace"))
        if len(locs) != len(PAGES):
            fail(f"sitemap has {len(locs)} URLs, expected {len(PAGES)}")
        else:
            ok(f"{len(locs)} URLs")
        for u in locs:
            if u.startswith("https://www."):
                warn(f"sitemap URL uses www, site is configured apex: {u}")

    print("\nFooter credit")
    missing = [rel for rel, body in html.items() if "bridgeworks" not in body.lower()]
    if missing:
        warn(f"BridgeWorks credit absent on {len(missing)} page(s): {', '.join(missing)}")
    elif html:
        ok("present on every page")

    print()
    if failures:
        print(f"{len(failures)} FAILURE(S), {len(warnings)} warning(s). Do not upload.\n")
        return 1
    print(f"All required checks passed, {len(warnings)} warning(s).")
    print("Build output is sound. This says nothing about the Google Ads account:")
    print("still confirm the conversion action's binding before relying on it.\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
