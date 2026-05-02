"""
Translate the English bodies in may-calendar.md to Hungarian via DeepL.

Reads `may-calendar.md`, finds each `**English version:**` block, sends the
English body to DeepL (target HU), and replaces the existing
`**Hungarian version:**` body. Preserves the EN and HU hashtag lines and the
`**Image brief:**` section unchanged. Brand names stay untouched.

Run: python translate-calendar.py
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ENV_PATH = Path("c:/Users/ELITEX21012G2/Projects/.env")
CALENDAR_PATH = Path(__file__).parent / "may-calendar.md"
BACKUP_PATH = Path(__file__).parent / "may-calendar.md.bak"

CONTEXT = (
    "BridgeWorks is a digital growth agency for small businesses. CEEFM is a "
    "Budapest facility management company. Translate in a B2B services / "
    "facility management context, professional but direct register. Keep brand "
    "names BridgeWorks, CEEFM, LinkedIn, WhatsApp, Limehome, SolaCare, Google, "
    "Bing unchanged. Translate \"engagement\" as business collaboration "
    "(együttműködés), never as the romantic sense (eljegyzés). Keep numbers, "
    "currencies (HUF, EUR), units (m2, kWh), and percentages exactly as "
    "written. Preserve markdown formatting including bold (**), bullet "
    "characters (-, →, 1.), and line breaks."
)


def load_deepl_key() -> str:
    if not ENV_PATH.exists():
        sys.exit(f"Missing {ENV_PATH}")
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("DEEPL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("DEEPL_API_KEY not found in .env")


def deepl_translate(texts: list[str], api_key: str) -> list[str]:
    url = (
        "https://api-free.deepl.com/v2/translate"
        if api_key.endswith(":fx")
        else "https://api.deepl.com/v2/translate"
    )
    body = json.dumps({
        "text": texts,
        "source_lang": "EN",
        "target_lang": "HU",
        "context": CONTEXT,
        "preserve_formatting": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [t["text"] for t in data["translations"]]


# Post-fix DeepL's romantic-sense "engagement" mapping
HU_FIXES = [
    (re.compile(r"\beljegyzés(e|ek|ünk|ünket|t|ben|re|ről|i)?\b"),
     lambda m: "együttműködés" + (m.group(1) or "")),
    (re.compile(r"\bEljegyzés(e|ek|ünk|ünket|t|ben|re|ről|i)?\b"),
     lambda m: "Együttműködés" + (m.group(1) or "")),
]


def apply_fixes(text: str) -> str:
    for pattern, repl in HU_FIXES:
        text = pattern.sub(repl, text)
    return text


# Match a full post block:
#   **English version:**\n\n<EN body>\n\n`#hashtags`\n\n
#   **Hungarian version:**\n\n<HU body>\n\n`#hashtags`\n\n
#   **Image brief:**
# We only want to replace the HU body. EN body and both hashtag lines stay put.
POST_PATTERN = re.compile(
    r"(\*\*English version:\*\*\n\n)"          # 1: EN header
    r"(.*?)"                                    # 2: EN body
    r"(\n\n`#[^\n]*`\n\n)"                      # 3: EN hashtag line + spacing
    r"(\*\*Hungarian version:\*\*\n\n)"         # 4: HU header
    r"(.*?)"                                    # 5: HU body (TO REPLACE)
    r"(\n\n`#[^\n]*`\n\n)"                      # 6: HU hashtag line + spacing
    r"(\*\*Image brief:\*\*)",                  # 7: Image brief header
    re.DOTALL,
)


def main():
    api_key = load_deepl_key()
    src = CALENDAR_PATH.read_text(encoding="utf-8")

    # Save backup before overwriting
    BACKUP_PATH.write_text(src, encoding="utf-8")

    matches = list(POST_PATTERN.finditer(src))
    print(f"Found {len(matches)} post blocks to translate.")
    if not matches:
        sys.exit("No matches. Check post structure.")

    en_bodies = [m.group(2) for m in matches]
    print("Calling DeepL...")
    hu_translations = deepl_translate(en_bodies, api_key)
    hu_translations = [apply_fixes(t) for t in hu_translations]
    print(f"Got {len(hu_translations)} translations back.")

    # Replace from the back so byte offsets stay valid
    out = src
    for match, new_hu in zip(reversed(matches), reversed(hu_translations)):
        start, end = match.span()
        rebuilt = (
            match.group(1)  # **English version:**\n\n
            + match.group(2)  # EN body unchanged
            + match.group(3)  # EN hashtags + spacing
            + match.group(4)  # **Hungarian version:**\n\n
            + new_hu          # NEW HU body
            + match.group(6)  # HU hashtags + spacing (original, kept)
            + match.group(7)  # **Image brief:**
        )
        out = out[:start] + rebuilt + out[end:]

    CALENDAR_PATH.write_text(out, encoding="utf-8")
    print(f"Updated: {CALENDAR_PATH}")
    print(f"Backup:  {BACKUP_PATH}")


if __name__ == "__main__":
    main()
