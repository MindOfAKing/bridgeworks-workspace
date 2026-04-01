"""Fix april-calendar.ics and april-calendar.csv with corrected CEE FM facts."""
import re

ICS_PATH = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\content\april-calendar.ics"
CSV_PATH = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\content\april-calendar.csv"

REPLACEMENTS = [
    # Brand name in summaries and references
    ("Introducing CEEFM", "Introducing CEE FM"),
    # English copy corrections
    ("across Hungary\\, Romania\\, and Slovakia. Over 200 projects", "in Budapest and across Hungary. Over 50 projects"),
    ("across Hungary, Romania, and Slovakia. Over 200 projects", "in Budapest and across Hungary. Over 50 projects"),
    ("Today we serve properties across Central and Eastern Europe.", "Today we serve properties across Hungary."),
    ("Today we serve properties across Central and Eastern Europe", "Today we serve properties across Hungary"),
    ("Közép- és Kelet-Európa szerte szolgálunk ingatlanokat", "egész Magyarországon szolgálunk ingatlanokat"),
    ("Kozep- es Kelet-Europa szerte szolgalunk ingatlanokat", "egesz Magyarorszagon szolgalunk ingatlanokat"),
    # Hungarian copy corrections
    ("Magyarországon, Romániában és Szlovákiában. Több mint 200", "Budapesten és egész Magyarországon. Több mint 50"),
    ("Magyarorszagon\\, Romaniaban es Szlovakiaban. Tobb mint 200", "Budapesten es egesz Magyarorszagon. Tobb mint 50"),
    ("Magyarorszagon, Romaniaban es Szlovakiaban. Tobb mint 200", "Budapesten es egesz Magyarorszagon. Tobb mint 50"),
    # Post 8 corrections
    ("CEEFM manages student housing facilities in Budapest and across the region", "CEE FM manages student housing facilities in Budapest and across Hungary"),
    ("A CEEFM diakszallasokat kezel Budapesten es a regioban", "A CEE FM diakszallasokat kezel Budapesten es egesz Magyarorszagon"),
    # Post 12 corrections
    ("CEEFM has been that partner for 200+ properties", "CEE FM has been that partner for 50+ properties"),
    ("A CEEFM tobb mint 200 ingatlannak volt ilyen partnere", "A CEE FM tobb mint 50 ingatlannak volt ilyen partnere"),
    # Calendar metadata
    ("CEEFM Content Calendar", "CEE FM Content Calendar"),
    ("CEEFM April LinkedIn", "CEE FM April LinkedIn"),
    # Image brief references
    ("CEEFM brand colors", "CEE FM brand colors"),
    ("CEEFM logo watermark", "CEE FM logo watermark"),
    # Post 7 and other body references
    ("At CEEFM\\, our quality", "At CEE FM\\, our quality"),
    ("At CEEFM, our quality", "At CEE FM, our quality"),
    ("A CEEFM-nel a minosegi", "A CEE FM-nel a minosegi"),
    # Summaries
    ("Introducing CEEFM", "Introducing CEE FM"),
    # Image brief post 12
    ("'CEEFM'", "'CEE FM'"),
]

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {path}")

fix_file(ICS_PATH)
fix_file(CSV_PATH)
print("Done. Both files updated with corrected CEE FM facts.")