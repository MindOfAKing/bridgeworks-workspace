from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[3]
STAGE = REPO / "tmp" / "bridgeworks-drive-anonymized-2026-07-23"
ATTACHMENT = Path(
    r"C:\Users\User\.codex\attachments\e34c6681-7002-4788-9ebc-afd85f91af1a"
    r"\pasted-text-1.txt"
)

ASSETS = [
    ("acq_core", "1nCmsXFjtbHm1fQrFw1ph_akJjfZIbd7s", "ASSET-MANIFEST-2026-07-15.md", "text/markdown"),
    ("acq_core", "1sEwFSVBOz3RRQnNvYDoSlFS1w-qKVlfw", "TWO-WEEK-EXECUTION-RUN-SHEET-2026-07-14.md", "text/markdown"),
    ("acq_core", "1p5sStEHvufZrqx3r6lIcvHRwGX6bAoAo", "README.md", "text/markdown"),
    ("acq_core", "1mwWcppWfqhM3LNhetvd9IqqfgKfrhRnF", "EXPANDED-PROSPECT-VERIFICATION-2026-07-14.md", "text/markdown"),
    ("acq_core", "1iHMiiSbKqfZmA0W0nBp1sQJhpDFdeLv7", "CURRENT-STATE-AUDIT-2026-07-14.md", "text/markdown"),
    ("acq_core", "12Vsi38iF1ZBJYEHBDg2qH9zlYm_dKqel", "CONTENT-PIPELINE-2026-07-14.md", "text/markdown"),
    ("acq_core", "1_jUH2Y0K_UbaFS8qDg0YxEUbgVyUtVer", "CONTENT-CHANNEL-INVENTORY-2026-07-14.md", "text/markdown"),
    ("acq_core", "1jvcpiQu-xbZjh8gDmLEz15iUPF3TN7wR", "CEEFM-PROOF-MODULES-2026-07-14.md", "text/markdown"),
    ("acq_core", "1VD7pPB_VBNGairlrIuLU02TwOf95kOj5", "CEEFM-PROOF-INVENTORY-2026-07-14.md", "text/markdown"),
    ("acq_core", "1Bw3SV49pzV9KKmotg7nQPSHSMs24Iv_A", "AI-VISIBILITY-REPORT-OUTLINE-2026.md", "text/markdown"),
    ("acq_core", "1mCETNfi6jk3soqOCjAdsn-3-DRcPyKAM", "AI-VISIBILITY-REPORT-DRAFT-2026.md", "text/markdown"),
    ("acq_approvals", "11DmnTbXjc_9xltjP-E7KKhPInw0PWyA5", "WEEK-ONE-RELATIONSHIP-AND-REFERRAL-PACKET-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1taLCg1o_ueYDVP_HtJ0xlMc4LBEveEAY", "WEEK-ONE-LINKEDIN-PUBLISH-BUNDLES-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1HY-Ei2qvEEnP7DUlbNyZTSNpPYEh2U3i", "WEEK-ONE-CONSOLIDATED-REVIEW-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1MnrihRLuF0xJZhWyCFpotybXXORXYLpd", "OUTREACH-APPROVAL-PACKET-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1Yo_SiPWDDPiCGVlhmRdZWulDSU7MtXER", "NO-OWNED-SITE-OUTREACH-PACKET-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1xZSRQ15EldSiA5hhLJH-u4mcEJgdAu7W", "LANE-A-FIRST-CONTACT-APPROVAL-PACKET-2026-07-14.md", "text/markdown"),
    ("acq_approvals", "1j2ReiLqhDmmhdZQ5fQx7qwMQ3XZd6a4f", "BRIDGEWORKS-WEBSITE-CLAIM-CORRECTION-PACKET-2026-07-14.md", "text/markdown"),
    ("acq_research", "154dZkMhJmBUfwMRRQ7KFqV7O2xoe1zFT", "nimaz-aesthetic-mini-scan-2026-07-14.md", "text/markdown"),
    ("acq_research", "1fKg6EQXOakqzgiuuev6Sb5hLFKaC8rNg", "moso-agency-mini-scan-2026-07-14.md", "text/markdown"),
    ("acq_research", "1vASjuQtRw62eXpjzyuaBCnCHQ6-AIgU8", "dental-de-classique-mini-scan-2026-07-14.md", "text/markdown"),
    ("acq_research", "1jHfZ83FmNpUzerPR1S6s4BcZ25bf62Mw", "AI-VISIBILITY-MINI-SCAN-TEMPLATE.md", "text/markdown"),
    ("acq_research", "1Z5YhF_vXHK4atO4f84_ZMxn8Hc1wUm85", "LANE-A-OBSERVATION-BANK-2026-07-14.md", "text/markdown"),
    ("acq_research", "1-AdUK5Jk2GdsTSqr-T8TIWDM531S-FK-", "BRIDGEWORKS-WEBSITE-SOURCE-MAP-2026-07-14.md", "text/markdown"),
    ("acq_research", "15_vt9mvc8yrkJmWdCWQ42EUOf7sA5PhG", "AI-VISIBILITY-METHODOLOGY-V1-2026-07-14.md", "text/markdown"),
    ("acq_research", "1WC52NSaEViYqAk5rrZTRXWLzYzo9Uf2G", "ai-visibility-evidence-dataset-2026-07-14.csv", "text/csv"),
    ("acq_sales", "1_R4g3vzFwP8D-kz-1Y_qixbCaG6tD8oi", "SME-DIGITAL-FOUNDATION-PROPOSAL-TEMPLATE-2026.md", "text/markdown"),
    ("acq_sales", "1kH99pPA7MYC-r3yb8j14MFvh1kVT3MNc", "REPLY-TO-PROPOSAL-PLAYBOOK-2026-07-14.md", "text/markdown"),
    ("acq_sales", "1W8YF-ilWf4VbHD3TI8YKfS91C2ESBHM_", "DISCOVERY-CALL-BRIEF-TEMPLATE-2026.md", "text/markdown"),
    ("acq_sales", "168B6VijIFufKXcFufynXseZT95HXZMJq", "PAID-AI-READINESS-DIAGNOSTIC-OUTLINE-2026-07-15.md", "text/markdown"),
    ("acq_outputs", "1MrFrXH31CxK1VJBmkAmp9L2m5uaNROLm", "BridgeWorks-LinkedIn-CEEFM-16-to-77-REVIEW.png", "image/png"),
    ("acq_outputs", "1ana1VHFu_WGd2XZN_rIOqJnTakte0oRl", "BridgeWorks-LinkedIn-AI-Visibility-Report-2026-REVIEW.png", "image/png"),
    ("acq_outputs", "1ePlSpIhcd6XXL44Gu2_88eeb4amYbe46", "BridgeWorks-Small-Business-AI-Visibility-Report-2026-DRAFT.pdf", "application/pdf"),
    ("acq_outputs", "1DySAO0D2kVoCcfZfJOHQYStGqdtnDgcy", "BridgeWorks-CEEFM-Case-Study-2026-DRAFT.pdf", "application/pdf"),
    ("acq_outputs", "1KDFnpap-FblCkAglKYLHnVGzr-w6_SWb", "WEEK-01-AUTHORITY-QUEUE-2026-07-20.md", "text/markdown"),
    ("acq_score", "1jhZVV9t-qIyPX9wWE6OFvthSqBPeLRZJ", "render_branded_markdown_pdf.py", "text/x-python"),
    ("acq_score", "1iYTqWTxANPh1vNH17Oo022Pm6Vzhr2M1", "WEEKLY-SCORECARD-TEMPLATE.md", "text/markdown"),
    ("acq_score", "1342VsH1Va4JMhtjamOuN6CkRAs_rmFbQ", "WEEKLY-SCORECARD-2026-07-14.md", "text/markdown"),
    ("ol_delivery", "1NB8TY1lWf9IHg4GijTp38M4Y_EGayxjj", "OLIVIKS-HANDOVER-2026-07-14.pdf", "application/pdf"),
    ("ol_delivery", "14Bwt1o4Ocjbdj1BPtoL0gyehZoZUq-t6", "OLIVIKS-HANDOVER-2026-07-14.md", "text/markdown"),
    ("ol_delivery", "1GMBcKQM_ruO4rZtc252Hu9LcKOKzscsX", "FOUNDATION-HANDOVER-INVOICE-NOTE-2026-07-12.md", "text/markdown"),
    ("ol_delivery", "1dXVGFBQTfPWeP2lM6PbbJw_YubHAt5bw", "OLIVIKS-COMPLETION-CHECKLIST-2026-07-14.md", "text/markdown"),
    ("ol_delivery", "14iUf5S3JXq73dybr88mm5jdMDkjZMSfM", "FOUNDATION-DELIVERY-MATRIX-2026-07-09.md", "text/markdown"),
    ("ol_shots", "1nA4vsj8xLzzwTnRQWXy6mCXx0Rj6BpHu", "legacy-home-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1olU8Cs2LX9WH5jRBkECVp-TgzbMDlzWJ", "legacy-home-desktop-2026-07-14.png", "image/png"),
    ("ol_shots", "1UB3i9lAgpb8CnK0r_wUq6Mo79Ks6630a", "preview-privacy-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1U9rMRRl0KhqELzOgmhkLUu3gFryn6uV6", "preview-menu-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1HhVXIsdclu5oOkTU55szqhNncElNU3uE", "preview-menu-desktop-2026-07-14.png", "image/png"),
    ("ol_shots", "1TWaw-RUD9B-LceIBFkyDqasjfRxON7xI", "preview-home-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1xYs-f6d7nmB6grgv-XKa3MMEGIErLQUR", "preview-home-desktop-2026-07-14.png", "image/png"),
    ("ol_shots", "1Gke5To64d1EYOUKYMLNVmKwPoKgYHjP4", "preview-contact-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1pxYcb2pQogelYPJJuwpf1RG7Oargyl84", "preview-contact-desktop-2026-07-14.png", "image/png"),
    ("ol_shots", "111Tte7b0lZ1qjfh9pBwcyLZjt9PChLjI", "preview-catering-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1m-aBmzb3QjXAuBsoFrvOHOzkQUCOieHH", "preview-admin-mobile-2026-07-14.png", "image/png"),
    ("ol_shots", "1XEA2hZqxRG8AZRJn3Tty6dwhLDr1rOyG", "preview-admin-desktop-2026-07-14.png", "image/png"),
    ("ol_shots", "1Cazklfh4wWQip8NTvTsvr3foNufhDC1-", "preview-about-mobile-2026-07-14.png", "image/png"),
    ("ol_records", "1SDQyFOFK_88HgDDj_cWbwNfFMIn4B5jq", "OLIVIKS-EVIDENCE-INDEX-2026-07-14.md", "text/markdown"),
    ("ol_records", "1NGvEAYEauhksHXcCW3D9VPJ0_J1DEC2g", "oliviks-metric-sheet-2026-07-14.csv", "text/csv"),
    ("ol_records", "1ECnK5PlJC1mz9XOV1G0MfNeKapcANnA1", "OLIVIKS-LIVE-LAUNCH-CHECK-2026-07-14.md", "text/markdown"),
    ("ol_records", "1yrqmSKfDLahPJlryWxRtTwhVA1roGDD2", "OLIVIKS-FUNCTIONAL-PERFORMANCE-AUDIT-2026-07-14.md", "text/markdown"),
    ("ol_records", "1AqNxKCtz_z-lqBikjSbXtvKEIH6qW9N5", "OLIVIKS-SCOPE-AND-DECISIONS-2026-07-14.md", "text/markdown"),
    ("ol_records", "1VigcrTXwHN8dtQRdmhdG2ahB4tkKLYqK", "OLIVIKS-DELIVERY-VERIFICATION-2026-07-14.md", "text/markdown"),
    ("ol_records", "1t-jBwNNqVUwclQQslDxUI4f8NpTvWXa6", "OLIVIKS-PRE-CLOSE-RETROSPECTIVE-2026-07-14.md", "text/markdown"),
    ("ol_records", "1B611VEbH47cXHBL1MnRxVL5J3y_RG4m7", "OLIVIKS-ORDERING-JOURNEY-COMPARISON-2026-07-14.md", "text/markdown"),
    ("ol_records", "1IPOl1MJOVOKC33dOuqKWWUDO_rtouLQR", "OLIVIKS-DELIVERY-TIMELINE-2026-07-14.md", "text/markdown"),
    ("ol_web", "1vuQXEnxsuSfg3LgdD9Kk7poC_SjUiK-_", "completion-audit.json", "application/json"),
    ("ol_web", "1iT9Tqnfb5uixLPQvmyaOZ7ai4cvwJeRz", "sitemap.ts", "text/typescript"),
    ("ol_web", "1sFdbOntn1eA8KKHaSbYBglfvZw6LYCVV", "robots.ts", "text/typescript"),
    ("ol_web", "1gB7vFUXChLeJAsgIQKZ__r5yUmBXMcCh", "og-image.jpg", "image/jpeg"),
    ("ol_web", "1EuZnNSarUlikk3gKOgJYQdAsvz6VNjn9", "llms.txt", "text/plain"),
    ("ceefm", "1tabzCJGT9GpBfPOPwbfY1KbmGRy7WI_-", "CEEFM-CASE-STUDY-FINAL-2026-06-11.md", "text/markdown"),
    ("source", "1Rm94-1vRjkXKuLyknLeWBkEpbL3pD65C", "lead-qualification-scoring-prompt.md", "text/markdown"),
    ("source", "19D3pltzk2t9eEYSa1jxIHSk5IhPmcoIJ", "prospect-batch-2026-07-14.csv", "text/csv"),
    ("source", "1Bbos-x6fBECKKJNQf1BXfbKN1rErJKiP", "GOAL-BRIEF-SOURCE.txt", "text/plain"),
]

TEXT_REPLACEMENTS = [
    ("Oliviks Nigerian Kitchen", "Anonymized Hospitality Client"),
    ("Oliviks Kitchen", "Anonymized Hospitality Client"),
    ("Oliviks KFT", "Anonymized Hospitality Client"),
    ("Oliviks Kft", "Anonymized Hospitality Client"),
    ("Oliviks", "Anonymized Hospitality Client"),
    ("OLIVIKS", "ANONYMIZED HOSPITALITY CLIENT"),
    ("oliviks", "anonymized hospitality client"),
    ("CEE Facility Management Kft", "Anonymized B2B Services Client"),
    ("CEEFM Kft", "Anonymized B2B Services Client"),
    ("CEE Facility Management", "Anonymized B2B Services Client"),
    ("CEEFM", "Anonymized B2B Services Client"),
    ("ceefm", "anonymized-b2b-services-client"),
    ("Victor Danmagaji", "[redacted client contact]"),
    ("Victor", "[redacted client contact]"),
    ("Cynthia", "[redacted founder name]"),
    ("Aese", "[redacted founder name]"),
    ("Rakoczi ter 9", "[redacted client address]"),
    ("Rákóczi tér 9", "[redacted client address]"),
    ("1074 Budapest", "[redacted client locality]"),
]

SENSITIVE_PATTERNS = [
    (r"(?i)https?://[^\s)\]>'\"]*(?:ceefm|oliviks)[^\s)\]>'\"]*", "[redacted external client link]"),
    (r"(?i)\b[\w.+-]+@(hu\.)?ceefm\.com\b", "[redacted client email]"),
    (r"(?i)\b[\w.+-]+@oliviks\.com\b", "[redacted client email]"),
    (r"(?i)\bolivikskitchen@gmail\.com\b", "[redacted client email]"),
    (r"(?i)https?://(?:www\.)?(?:hu\.)?ceefm\.(?:com|eu)[^\s)\]>'\"]*", "[redacted client domain]"),
    (r"(?i)https?://(?:www\.)?oliviks\.com[^\s)\]>'\"]*", "[redacted client domain]"),
    (r"(?i)https?://shop\.oliviks\.com[^\s)\]>'\"]*", "[redacted ordering domain]"),
    (r"(?i)https?://oliviks-kitchen\.vercel\.app[^\s)\]>'\"]*", "[redacted preview domain]"),
    (r"(?i)\b(?:www\.)?(?:hu\.)?ceefm\.(?:com|eu)\b", "[redacted client domain]"),
    (r"(?i)\b(?:www\.)?oliviks\.com\b", "[redacted client domain]"),
    (r"(?i)\bshop\.oliviks\.com\b", "[redacted ordering domain]"),
    (r"(?i)\boliviks-kitchen\.vercel\.app\b", "[redacted preview domain]"),
    (r"(?i)\bEO-2026-\d+\b", "[redacted invoice reference]"),
    (r"\bHU\d{26}\b", "[redacted bank account]"),
    (r"\b\d{8}-\d-\d{2}\b", "[redacted tax number]"),
    (r"\b\d{8}-\d{8}(?:-\d{8})?\b", "[redacted bank account]"),
    (r"(?i)\b\d{1,3}(?:[,\s]\d{3})+\s*HUF\b", "[redacted invoice amount]"),
    (r"(?<!\d)\+?36[\s()-]*(?:\d[\s()-]*){8,9}(?!\d)", "[redacted client phone]"),
    (r"(?i)\bR[aá]k[oó]czi\s+t[eé]r\s+9\b", "[redacted client address]"),
    (r"(?i)data:image/[^;]+;base64,[A-Za-z0-9+/=]+", "[redacted embedded image evidence]"),
]


def source_path(group: str, title: str) -> Path:
    engine = REPO / "operations" / "client-acquisition-engine"
    if group == "acq_core":
        return engine / title
    if group == "acq_approvals":
        return engine / "approvals" / title
    if group == "acq_research":
        if title.endswith("-mini-scan-2026-07-14.md") or title == "AI-VISIBILITY-MINI-SCAN-TEMPLATE.md":
            return engine / "scans" / title
        return engine / "research" / title
    if group == "acq_sales":
        if title.startswith("SME-"):
            return engine / "templates" / title
        if title.startswith("PAID-"):
            return engine / "offers" / title
        return engine / "sales" / title
    if group == "acq_outputs":
        if title.endswith(".pdf"):
            return engine / "output" / "pdf" / title
        if title.endswith(".png"):
            return engine / "output" / "social" / "week-01" / title
        return engine / "content" / title
    if group == "acq_score":
        if title.endswith(".py"):
            return engine / "scripts" / title
        return engine / "scorecards" / title
    if group == "ol_delivery":
        if title == "FOUNDATION-DELIVERY-MATRIX-2026-07-09.md":
            return REPO / "clients" / "oliviks" / "delivery" / title
        if title == "OLIVIKS-COMPLETION-CHECKLIST-2026-07-14.md":
            return REPO / "clients" / "oliviks" / "delivery" / title
        return REPO / "clients" / "oliviks" / title
    if group == "ol_shots":
        branch = "before" if title.startswith("legacy-") else "after"
        return REPO / "clients" / "oliviks" / "evidence" / branch / title
    if group == "ol_records":
        base = REPO / "clients" / "oliviks" / "evidence"
        if title == "OLIVIKS-EVIDENCE-INDEX-2026-07-14.md":
            return base / title
        if title == "oliviks-metric-sheet-2026-07-14.csv":
            return base / "metrics" / title
        if "PERFORMANCE" in title or "VERIFICATION" in title or "LAUNCH-CHECK" in title:
            return base / "metrics" / title
        return base / "decisions" / title
    if group == "ol_web":
        web = REPO / "clients" / "oliviks" / "website"
        if title == "completion-audit.json":
            return web / "test-results" / "completion-audit-2026-07-14" / title
        if title in {"sitemap.ts", "robots.ts"}:
            return web / "src" / "app" / title
        return web / "public" / title
    if group == "ceefm":
        return REPO / "clients" / "ceefm" / title
    if group == "source":
        if title == "lead-qualification-scoring-prompt.md":
            return REPO / "pipeline" / "lead-qualification" / "scoring-prompt.md"
        if title == "prospect-batch-2026-07-14.csv":
            return REPO / "operations" / "lead-engine-v1" / "01-prospects" / title
        return ATTACHMENT
    raise ValueError(f"Unknown group: {group}")


def anonymized_name(name: str) -> str:
    replacements = [
        ("BridgeWorks-LinkedIn-CEEFM", "BridgeWorks-LinkedIn-Anonymized-B2B-Services"),
        ("BridgeWorks-CEEFM", "BridgeWorks-Anonymized-B2B-Services"),
        ("CEEFM", "ANONYMIZED-B2B-SERVICES"),
        ("ceefm", "anonymized-b2b-services"),
        ("OLIVIKS", "ANONYMIZED-HOSPITALITY-CLIENT"),
        ("Oliviks", "Anonymized-Hospitality-Client"),
        ("oliviks", "anonymized-hospitality-client"),
    ]
    for old, new in replacements:
        name = name.replace(old, new)
    return name


def sanitize_text(text: str, group: str) -> str:
    for pattern, replacement in SENSITIVE_PATTERNS:
        text = re.sub(pattern, replacement, text)
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    if group.startswith("ol_"):
        contextual_replacements = [
            ("Authentic Nigerian Food in Budapest", "Hospitality Client Website"),
            ("Real Nigerian Food. Made in Budapest.", "Hospitality Client Website"),
            ("Nigerian food,made to share.", "Hospitality offering, made to share."),
            ("Nigerian restaurant", "hospitality business"),
            ("Nigerian Food", "hospitality offering"),
            ("Nigerian food", "hospitality offering"),
            ("Nigerian", "hospitality"),
            ("Nigeria", "[redacted country]"),
            ("Budapest", "[redacted city]"),
            ("Hungarian", "[redacted country]"),
            ("Hungary", "[redacted country]"),
        ]
        for old, new in contextual_replacements:
            text = text.replace(old, new)
    text = re.sub(
        r"(?i)clients[/\\](?:anonymized-b2b-services-client|anonymized hospitality client)(?:[/\\][^\s)`'\"]*)?",
        "private-evidence/[redacted-client-path]",
        text,
    )
    return text


def scrub_json(value, key: str | None = None):
    sensitive_keys = {
        "address",
        "addresslocality",
        "addressregion",
        "email",
        "geo",
        "latitude",
        "longitude",
        "postalcode",
        "ratingvalue",
        "reviewcount",
        "streetaddress",
        "telephone",
    }
    if key and key.lower() in sensitive_keys:
        return "[redacted client detail]"
    if isinstance(value, dict):
        return {item_key: scrub_json(item_value, item_key) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [scrub_json(item) for item in value]
    if isinstance(value, str):
        if re.search(r"(?i)^(?:mailto:|tel:|https?://(?!127\.0\.0\.1))", value):
            return "[redacted external client link]"
    return value


def stage_text(source: Path, destination: Path, mime: str, group: str) -> None:
    text = source.read_text(encoding="utf-8-sig")
    text = sanitize_text(text, group)
    if mime == "application/json":
        parsed = scrub_json(json.loads(text))
        text = json.dumps(parsed, ensure_ascii=False, indent=2) + "\n"
    destination.write_text(text, encoding="utf-8", newline="\n")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, text_font, fill: str) -> None:
    left, top, right, bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=text_font, align="center", spacing=8)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    draw.multiline_text(
        (left + (right - left - width) / 2, top + (bottom - top - height) / 2),
        text,
        font=text_font,
        fill=fill,
        align="center",
        spacing=8,
    )


def evidence_placeholder(source: Path, destination: Path, title: str) -> None:
    with Image.open(source) as original:
        width, height = original.size
    width = max(width, 720)
    height = max(height, 720)
    image = Image.new("RGB", (width, height), "#F4F6F3")
    draw = ImageDraw.Draw(image)
    margin = max(40, min(width, height) // 14)
    accent = max(10, width // 90)
    draw.rectangle((0, 0, accent, height), fill="#7DA15A")
    draw.rectangle((margin, margin, width - margin, height - margin), outline="#18342B", width=max(2, width // 500))
    heading_size = max(28, min(72, width // 15))
    body_size = max(18, min(42, width // 28))
    small_size = max(15, min(30, width // 38))
    centered(
        draw,
        (margin * 2, margin * 2, width - margin * 2, height // 2),
        "ANONYMIZED\nEVIDENCE IMAGE",
        font(heading_size, bold=True),
        "#18342B",
    )
    centered(
        draw,
        (margin * 2, height // 2, width - margin * 2, height - margin * 2),
        f"{title}\n\nIdentifying interface details removed.\nOriginal evidence is retained privately.",
        font(body_size),
        "#30483F",
    )
    draw.text((margin * 1.5, height - margin * 0.75), "BRIDGEWORKS", font=font(small_size, bold=True), fill="#7DA15A")
    if destination.suffix.lower() in {".jpg", ".jpeg"}:
        image.save(destination, format="JPEG", quality=92, optimize=True)
    else:
        image.save(destination, format="PNG", optimize=True)


def clean_image(source: Path, destination: Path) -> None:
    with Image.open(source) as image:
        cleaned = image.convert("RGB") if destination.suffix.lower() in {".jpg", ".jpeg"} else image.convert("RGBA")
        if destination.suffix.lower() in {".jpg", ".jpeg"}:
            cleaned.save(destination, format="JPEG", quality=94, optimize=True)
        else:
            cleaned.save(destination, format="PNG", optimize=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if len(ASSETS) != 74:
        raise RuntimeError(f"Expected 74 assets, found {len(ASSETS)}")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    case_pdf = REPO / "operations" / "client-acquisition-engine" / "public-proof" / "output" / "BridgeWorks-Anonymized-B2B-Services-Case-Study-2026.pdf"
    case_png = REPO / "operations" / "client-acquisition-engine" / "public-proof" / "output" / "BridgeWorks-Anonymized-B2B-Services-Case-Study-2026.png"
    report_pdf = REPO / "operations" / "client-acquisition-engine" / "public-proof" / "output" / "BridgeWorks-AI-Visibility-Report-2026-PUBLIC-ANONYMIZED.pdf"

    records = []
    handover_pdf_record = None
    for group, file_id, old_name, mime in ASSETS:
        source = source_path(group, old_name)
        if not source.exists():
            raise FileNotFoundError(source)
        new_name = anonymized_name(old_name)
        group_dir = STAGE / group
        group_dir.mkdir(parents=True, exist_ok=True)
        destination = group_dir / new_name

        if old_name == "OLIVIKS-HANDOVER-2026-07-14.pdf":
            handover_pdf_record = (source, destination)
        elif old_name == "BridgeWorks-CEEFM-Case-Study-2026-DRAFT.pdf":
            shutil.copy2(case_pdf, destination)
        elif old_name == "BridgeWorks-Small-Business-AI-Visibility-Report-2026-DRAFT.pdf":
            shutil.copy2(report_pdf, destination)
        elif old_name == "BridgeWorks-LinkedIn-CEEFM-16-to-77-REVIEW.png":
            clean_image(case_png, destination)
        elif group == "ol_shots" or old_name == "og-image.jpg":
            evidence_placeholder(source, destination, new_name.rsplit(".", 1)[0])
        elif mime.startswith("image/"):
            clean_image(source, destination)
        elif mime == "application/pdf":
            shutil.copy2(source, destination)
        else:
            stage_text(source, destination, mime, group)

        records.append(
            {
                "group": group,
                "file_id": file_id,
                "old_name": old_name,
                "new_name": new_name,
                "mime_type": mime,
                "source": str(source),
                "staged": str(destination),
            }
        )

    if handover_pdf_record is None:
        raise RuntimeError("Handover PDF mapping is missing")
    _, handover_pdf = handover_pdf_record
    handover_md = STAGE / "ol_delivery" / "ANONYMIZED-HOSPITALITY-CLIENT-HANDOVER-2026-07-14.md"
    renderer = REPO / "operations" / "client-acquisition-engine" / "scripts" / "render_branded_markdown_pdf.py"
    subprocess.run(
        [
            sys.executable,
            str(renderer),
            str(handover_md),
            str(handover_pdf),
            "--label",
            "Anonymized client handover",
        ],
        check=True,
        cwd=REPO,
    )

    prohibited = re.compile(
        r"(?i)\b(?:ceefm|oliviks|victor\s+danmagaji|cynthia|aese)\b|"
        r"(?:hu\.)?ceefm\.(?:com|eu)|oliviks(?:-kitchen)?\.(?:com|vercel\.app)|"
        r"anonymized hospitality client(?:kitchen)?@|"
        r"(?:shop\.)?anonymized hospitality client\.com|"
        r"\bR[aá]k[oó]czi\s+t[eé]r\s+9\b"
    )
    failures = []
    for record in records:
        path = Path(record["staged"])
        if not path.exists() or path.stat().st_size == 0:
            failures.append(f"Missing or empty: {path}")
            continue
        if record["mime_type"].startswith("text/") or record["mime_type"] == "application/json":
            content = path.read_text(encoding="utf-8")
            match = prohibited.search(content)
            if match:
                failures.append(f"Prohibited identifier {match.group(0)!r}: {path}")
        if prohibited.search(record["new_name"]):
            failures.append(f"Prohibited identifier in filename: {record['new_name']}")
        record["bytes"] = path.stat().st_size
        record["sha256"] = sha256(path)

    if failures:
        raise RuntimeError("\n".join(failures))

    manifest = {
        "generated": "2026-07-23",
        "asset_count": len(records),
        "purpose": "In-place anonymized replacements for the canonical BridgeWorks Drive package.",
        "records": records,
    }
    manifest_path = STAGE / "drive-update-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"stage": str(STAGE), "assets": len(records), "manifest": str(manifest_path)}, indent=2))


if __name__ == "__main__":
    main()
