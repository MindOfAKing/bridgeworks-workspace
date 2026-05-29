"""Render ceefm.eu with Playwright (using installed Edge) and dump structured content
for GEO citability scoring. Also confirms the Edge HTML->PDF path works."""
import json, sys
from playwright.sync_api import sync_playwright

URL = "https://www.ceefm.eu/"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge", headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=45000)
        title = page.title()
        # headings in order
        headings = page.eval_on_selector_all(
            "h1,h2,h3",
            "els => els.map(e => ({tag:e.tagName, text:e.innerText.trim()})).filter(h=>h.text)"
        )
        # main text
        body = page.inner_text("body")
        # detect FAQ/tables/lists
        n_tables = page.eval_on_selector_all("table", "e=>e.length")
        n_lists = page.eval_on_selector_all("ul,ol", "e=>e.length")
        has_faq = "faq" in body.lower() or "frequently asked" in body.lower()
        # languages: check for /hu link
        hu = page.eval_on_selector_all("a[href*='/hu']", "e=>e.length") > 0
        # json-ld
        jsonld = page.eval_on_selector_all(
            "script[type='application/ld+json']", "els=>els.map(e=>e.innerText)"
        )
        browser.close()
    out = {
        "title": title,
        "headings": headings,
        "n_tables": n_tables,
        "n_lists": n_lists,
        "has_faq": has_faq,
        "has_hu": hu,
        "jsonld_count": len(jsonld),
        "jsonld_types": [],
        "body": body,
    }
    import re
    for j in jsonld:
        for m in re.findall(r'"@type"\s*:\s*"([^"]+)"', j):
            out["jsonld_types"].append(m)
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    run()
