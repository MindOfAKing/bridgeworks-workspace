from __future__ import annotations

import csv
import datetime as dt
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = ROOT / "pipeline" / "prospecting"
AUDIT_PREVIEW_TRACKER_CSV = PIPELINE_DIR / "audit-preview-tracker.csv"
DAILY_OUTREACH_QUEUE_CSV = PIPELINE_DIR / "daily-outreach-queue.csv"
PROSPECT_TRACKER_CSV = PIPELINE_DIR / "prospect-tracker.csv"
OUTPUT_DIR = PIPELINE_DIR / "audit-previews"


BRAND = {
    "navy": (11, 31, 59),  # #0B1F3B
    "gold": (198, 158, 91),  # #C69E5B
    "sage": (120, 141, 120),  # muted sage
    "ivory": (249, 246, 239),  # warm off-white
    "text": (20, 20, 20),
}


def _rgb(r: int, g: int, b: int) -> str:
    return f"{r/255:.4f} {g/255:.4f} {b/255:.4f}"


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "company"


def _today_iso() -> str:
    return dt.date.today().isoformat()


@dataclass(frozen=True)
class Prospect:
    prospect_id: str
    company: str
    website: str
    audit_type: str
    thesis: str
    contact_name: str | None


class SimplePDF:
    """
    Minimal PDF writer for branded text reports.
    No external dependencies.
    Uses built-in PDF fonts (Helvetica).
    """

    def __init__(self, title: str):
        self._title = title
        self._pages: list[bytes] = []
        self._page_w = 595.28
        self._page_h = 841.89

    def add_page(self, commands: Iterable[str]) -> None:
        content = "\n".join(commands).encode("utf-8")
        self._pages.append(content)

    def save(self, path: Path) -> None:
        # PDF objects:
        # 1: Catalog
        # 2: Pages
        # per page:
        #   page object
        #   content stream object
        #
        # resources: font dictionary
        objects: list[bytes] = []

        def obj(data: bytes) -> int:
            objects.append(data)
            return len(objects)

        # Font resources (built-in)
        # F1 = Helvetica, F2 = Helvetica-Bold
        resources_obj = obj(
            b"<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
            b"/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> >> >>"
        )

        page_objs: list[int] = []
        content_objs: list[int] = []

        for page_content in self._pages:
            stream = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(page_content), page_content)
            content_obj = obj(stream)
            content_objs.append(content_obj)
            page_obj = obj(
                (
                    f"<< /Type /Page /Parent 2 0 R "
                    f"/MediaBox [0 0 {self._page_w:.2f} {self._page_h:.2f}] "
                    f"/Resources {resources_obj} 0 R "
                    f"/Contents {content_obj} 0 R >>"
                ).encode("utf-8")
            )
            page_objs.append(page_obj)

        kids = " ".join(f"{p} 0 R" for p in page_objs).encode("utf-8")
        pages_obj = obj(b"<< /Type /Pages /Kids [ " + kids + b" ] /Count %d >>" % len(page_objs))

        catalog_obj = obj(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_obj)

        # Info dictionary
        _ = obj(
            (
                "<< "
                f"/Title ({_pdf_escape(self._title)}) "
                "/Producer (BridgeWorks audit-preview engine) "
                ">>"
            ).encode("utf-8")
        )

        # Build file with xref
        header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        offsets: list[int] = [0]
        body = bytearray()
        body.extend(header)

        for i, data in enumerate(objects, start=1):
            offsets.append(len(body))
            body.extend(f"{i} 0 obj\n".encode("utf-8"))
            body.extend(data)
            body.extend(b"\nendobj\n")

        xref_start = len(body)
        body.extend(b"xref\n")
        body.extend(f"0 {len(objects)+1}\n".encode("utf-8"))
        body.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            body.extend(f"{off:010d} 00000 n \n".encode("utf-8"))

        trailer = (
            "<< "
            f"/Size {len(objects)+1} "
            f"/Root {catalog_obj} 0 R "
            f"/Info {len(objects)} 0 R "
            ">>"
        ).encode("utf-8")
        body.extend(b"trailer\n")
        body.extend(trailer)
        body.extend(b"\nstartxref\n")
        body.extend(f"{xref_start}\n".encode("utf-8"))
        body.extend(b"%%EOF\n")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(bytes(body))


def _pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(text: str, max_chars: int) -> list[str]:
    words = re.split(r"\s+", text.strip())
    lines: list[str] = []
    current: list[str] = []
    for w in words:
        candidate = " ".join([*current, w]).strip()
        if len(candidate) <= max_chars:
            current.append(w)
            continue
        if current:
            lines.append(" ".join(current))
        current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def _text_block(
    x: float,
    y: float,
    lines: list[str],
    font: str,
    size: int,
    leading: int,
    rgb: tuple[int, int, int] | None = None,
) -> list[str]:
    cmds: list[str] = ["BT"]
    if rgb is not None:
        cmds.append(f"{_rgb(*rgb)} rg")
    cmds.append(f"/{font} {size} Tf")
    cmds.append(f"{x:.2f} {y:.2f} Td")
    for i, line in enumerate(lines):
        if i > 0:
            cmds.append(f"0 -{leading} Td")
        cmds.append(f"({_pdf_escape(line)}) Tj")
    cmds.append("ET")
    return cmds


def _rect(x: float, y: float, w: float, h: float, rgb: tuple[int, int, int], fill: bool = True) -> str:
    op = "f" if fill else "S"
    return f"{_rgb(*rgb)} rg\n{x:.2f} {y:.2f} {w:.2f} {h:.2f} re\n{op}"


def build_preview_pdf(prospect: Prospect, output_path: Path) -> None:
    report_type_title = {
        "geo-audit-preview": "GEO Audit Preview",
        "market-audit-preview": "Market Audit Preview",
        "conversion-audit-preview": "Conversion Audit Preview",
        "technical-audit-preview": "Technical Audit Preview",
        "speed-to-lead-preview": "Speed-To-Lead Audit Preview",
    }.get(prospect.audit_type, "BridgeWorks Audit Preview")

    # Findings are intentionally scoped. Specific enough to be credible, not a full roadmap.
    findings = _generate_findings(prospect)
    impact, quick_win, bigger_opportunity, next_step, call_topic, cta = _generate_impact_and_next_step(
        prospect
    )

    pdf = SimplePDF(f"BridgeWorks Audit Preview - {prospect.company}")

    margin_x = 44
    top_y = 800

    # Page 1: Cover
    p1: list[str] = []
    p1.append(_rect(0, 0, 595.28, 841.89, BRAND["ivory"]))
    p1.append(_rect(0, 760, 595.28, 81.89, BRAND["navy"]))
    p1.extend(_text_block(margin_x, 812, ["BridgeWorks.agency"], "F2", 20, 24, BRAND["ivory"]))
    p1.extend(_text_block(margin_x, 782, [report_type_title], "F1", 12, 14, BRAND["ivory"]))

    p1.extend(
        _text_block(
            margin_x,
            720,
            ["BridgeWorks Audit Preview"],
            "F2",
            22,
            26,
            BRAND["navy"],
        )
    )
    p1.extend(_text_block(margin_x, 690, [prospect.company], "F2", 16, 20, BRAND["text"]))
    p1.extend(_text_block(margin_x, 670, [prospect.website], "F1", 11, 14, BRAND["sage"]))
    p1.extend(_text_block(margin_x, 650, [f"Date: {_today_iso()}"], "F1", 11, 14, BRAND["text"]))

    p1.extend(_text_block(margin_x, 610, ["Audit thesis"], "F2", 12, 16, BRAND["navy"]))
    thesis_lines = _wrap(prospect.thesis, 88)
    p1.extend(_text_block(margin_x, 590, thesis_lines, "F1", 11, 14, BRAND["text"]))

    p1.extend(
        _text_block(
            margin_x,
            120,
            [
                "Free preview. Short on purpose.",
                "Full paid audit includes prioritization and implementation detail.",
            ],
            "F1",
            10,
            13,
            BRAND["sage"],
        )
    )
    pdf.add_page(p1)

    # Page 2: Findings
    p2: list[str] = []
    p2.append(_rect(0, 0, 595.28, 841.89, BRAND["ivory"]))
    p2.append(_rect(0, 800, 595.28, 41.89, BRAND["navy"]))
    p2.extend(_text_block(margin_x, 816, ["Findings (3)"], "F2", 14, 18, BRAND["ivory"]))

    y = 760
    for idx, f in enumerate(findings, start=1):
        p2.extend(_text_block(margin_x, y, [f"Finding {idx}"], "F2", 12, 16, BRAND["navy"]))
        y -= 18
        p2.extend(_text_block(margin_x, y, ["What I saw"], "F2", 10, 14, BRAND["gold"]))
        y -= 14
        p2.extend(_text_block(margin_x, y, _wrap(f["what"], 92), "F1", 11, 14, BRAND["text"]))
        y -= 14 * (len(_wrap(f["what"], 92)) + 1)

        p2.extend(_text_block(margin_x, y, ["Why it matters"], "F2", 10, 14, BRAND["gold"]))
        y -= 14
        p2.extend(_text_block(margin_x, y, _wrap(f["why"], 92), "F1", 11, 14, BRAND["text"]))
        y -= 14 * (len(_wrap(f["why"], 92)) + 1)

        p2.extend(
            _text_block(
                margin_x,
                y,
                [f"Severity: {f['severity']}"],
                "F2",
                10,
                14,
                BRAND["sage"],
            )
        )
        y -= 30
        if y < 140:
            break

    pdf.add_page(p2)

    # Page 3: Business Impact
    p3: list[str] = []
    p3.append(_rect(0, 0, 595.28, 841.89, BRAND["ivory"]))
    p3.append(_rect(0, 800, 595.28, 41.89, BRAND["navy"]))
    p3.extend(_text_block(margin_x, 816, ["Business impact"], "F2", 14, 18, BRAND["ivory"]))

    p3.extend(_text_block(margin_x, 760, ["Likely effect"], "F2", 12, 16, BRAND["navy"]))
    p3.extend(_text_block(margin_x, 740, _wrap(impact, 92), "F1", 11, 14, BRAND["text"]))

    p3.extend(_text_block(margin_x, 660, ["Quick win"], "F2", 12, 16, BRAND["navy"]))
    p3.extend(_text_block(margin_x, 640, _wrap(quick_win, 92), "F1", 11, 14, BRAND["text"]))

    p3.extend(_text_block(margin_x, 560, ["Bigger opportunity"], "F2", 12, 16, BRAND["navy"]))
    p3.extend(_text_block(margin_x, 540, _wrap(bigger_opportunity, 92), "F1", 11, 14, BRAND["text"]))

    pdf.add_page(p3)

    # Page 4: Next Step
    p4: list[str] = []
    p4.append(_rect(0, 0, 595.28, 841.89, BRAND["ivory"]))
    p4.append(_rect(0, 800, 595.28, 41.89, BRAND["navy"]))
    p4.extend(_text_block(margin_x, 816, ["Recommended next step"], "F2", 14, 18, BRAND["ivory"]))

    p4.extend(_text_block(margin_x, 760, ["Recommendation"], "F2", 12, 16, BRAND["navy"]))
    p4.extend(_text_block(margin_x, 740, _wrap(next_step, 92), "F1", 11, 14, BRAND["text"]))

    p4.extend(_text_block(margin_x, 660, ["Suggested call topic"], "F2", 12, 16, BRAND["navy"]))
    p4.extend(_text_block(margin_x, 640, _wrap(call_topic, 92), "F1", 11, 14, BRAND["text"]))

    p4.append(_rect(margin_x, 380, 595.28 - 2 * margin_x, 120, BRAND["navy"]))
    p4.extend(_text_block(margin_x + 18, 470, ["CTA"], "F2", 12, 16, BRAND["ivory"]))
    p4.extend(_text_block(margin_x + 18, 448, _wrap(cta, 78), "F2", 14, 18, BRAND["ivory"]))

    p4.extend(
        _text_block(
            margin_x,
            120,
            ["Emmanuel", "BridgeWorks.agency"],
            "F1",
            10,
            13,
            BRAND["sage"],
        )
    )
    pdf.add_page(p4)

    pdf.save(output_path)


def _generate_findings(prospect: Prospect) -> list[dict[str, str]]:
    t = prospect.audit_type
    c = prospect.company
    if t == "market-audit-preview":
        return [
            {
                "what": f"{c} has strong proof signals, but the key stats and credibility points are not surfaced early enough to shape the reader's decision quickly.",
                "why": "In property services, buyers skim. If the proof does not hit in the first scroll, enquiries drop and comparison shopping increases.",
                "severity": "High",
            },
            {
                "what": "The offer is credible, but the path from proof to enquiry is likely too indirect. The next step for a new visitor is not obvious.",
                "why": "Proof without a clear next step creates passive trust, not action. The site can be trusted and still under-convert.",
                "severity": "Medium",
            },
            {
                "what": "Your proof could be made more 'AI-visible' by structuring it consistently across key pages (so summaries and assistants can quote it cleanly).",
                "why": "AI and search assistants amplify the clearest, most structured facts. If proof is scattered, you lose free visibility in AI search results.",
                "severity": "Medium",
            },
        ]
    if t == "speed-to-lead-preview":
        return [
            {
                "what": "The quote/contact path does not set a clear response-time expectation for new enquiries.",
                "why": "In B2B services, speed-to-lead often beats pricing. Slow or uncertain response reduces win rate and increases churn to competitors.",
                "severity": "High",
            },
            {
                "what": "Post-submit reassurance and next steps are likely weak or missing (what happens after someone requests a quote).",
                "why": "If prospects do not know what happens next, they hesitate or submit multiple enquiries elsewhere. It also increases no-shows later.",
                "severity": "High",
            },
            {
                "what": "Trust proof is present or implied, but it is not converted into a simple trust path for decision-makers (logos, outcomes, and scope clarity).",
                "why": "Commercial buyers need risk reduction. A sharper trust path increases qualified enquiries and reduces back-and-forth.",
                "severity": "Medium",
            },
        ]
    if t == "conversion-audit-preview":
        return [
            {
                "what": "The primary CTA is likely generic or split across too many options.",
                "why": "When the CTA is not a single clear action, conversion drops and lead quality worsens.",
                "severity": "High",
            },
            {
                "what": "Proof is present but not anchored to the exact buyer fear (risk, reliability, response time, and standards).",
                "why": "Buyers need proof that matches their risk. Generic proof does not move the needle.",
                "severity": "Medium",
            },
            {
                "what": "The lead path likely has friction (extra clicks, unclear form fields, or weak confirmation).",
                "why": "Small friction compounds. It reduces enquiries and makes tracking harder.",
                "severity": "Medium",
            },
        ]
    if t == "technical-audit-preview":
        return [
            {
                "what": "Core discoverability signals (metadata, indexation hygiene, and structured data) are likely incomplete or inconsistent.",
                "why": "If search and AI cannot parse the site cleanly, you lose visibility on high-intent queries.",
                "severity": "High",
            },
            {
                "what": "Tracking and measurement may not be set to answer one simple question: which pages and channels create enquiries.",
                "why": "Without clean measurement, budget and content decisions become guesswork.",
                "severity": "Medium",
            },
            {
                "what": "Performance and page experience likely have quick wins that improve both rankings and conversion.",
                "why": "Faster pages reduce bounce and increase form completion rates.",
                "severity": "Medium",
            },
        ]
    # geo-audit-preview fallback
    return [
        {
            "what": "Key service facts are not expressed in a consistent, quotable way across the site.",
            "why": "AI visibility rewards clear, structured facts. If your facts are unclear, you get omitted or misrepresented.",
            "severity": "High",
        },
        {
            "what": "Authority signals (proof, references, and location relevance) likely need to be concentrated on a few pages.",
            "why": "Search and assistants prioritize the pages that look like the source of truth.",
            "severity": "Medium",
        },
        {
            "what": "The site likely misses one simple 'citability' asset that assistants can quote directly.",
            "why": "Citability increases mentions and referral traffic without paid spend.",
            "severity": "Medium",
        },
    ]


def _generate_impact_and_next_step(prospect: Prospect) -> tuple[str, str, str, str, str, str]:
    t = prospect.audit_type
    if t == "market-audit-preview":
        impact = (
            "Even with strong real-world credibility, the site can underperform on enquiries if proof is not "
            "organized into a simple decision path. That usually shows up as fewer inbound leads and more "
            "price-shopping."
        )
        quick_win = (
            "Move the strongest proof points into the first scroll on the key landing page, then add one clear "
            "CTA that matches the buyer's intent."
        )
        bigger = (
            "Build a single 'proof hub' page that packages your strongest facts into a clear story and makes them "
            "easy for both humans and AI search assistants to quote."
        )
        next_step = (
            "A focused proof and conversion audit: identify the 3-5 proof assets that move the most revenue, then "
            "rebuild the enquiry path around them."
        )
        call_topic = "How to turn existing proof into more inbound enquiries"
        cta = "Reply with a good time for a 15-minute walk-through this week."
        return impact, quick_win, bigger, next_step, call_topic, cta

    if t == "speed-to-lead-preview":
        impact = (
            "If response expectations are unclear or slow, you lose deals before pricing is even discussed. "
            "Speed-to-lead improvements usually increase win rate and lead quality fast."
        )
        quick_win = (
            "Add a clear response-time promise on the quote path and ensure every enquiry triggers a confirmation "
            "message that sets the next step."
        )
        bigger = (
            "Set up a simple lead routing and follow-up system: instant acknowledgement, internal alert, and a "
            "short follow-up sequence for non-responders."
        )
        next_step = (
            "A speed-to-lead audit and fix sprint: map the enquiry path end-to-end, then implement a response "
            "promise, routing, and a basic follow-up sequence."
        )
        call_topic = "Where leads are being lost between form submit and first reply"
        cta = "If useful, I can walk you through the findings in 15 minutes."
        return impact, quick_win, bigger, next_step, call_topic, cta

    # Default
    impact = "The current setup likely leaks enquiries and reduces trust from high-intent visitors."
    quick_win = "Clarify the primary CTA and add one visible proof block near it."
    bigger = "Create a tighter lead path and a clearer trust story across the top pages."
    next_step = "A short paid audit to prioritize what to fix first, based on revenue impact."
    call_topic = "What to fix first to lift enquiries"
    cta = "Reply with a day/time and I will walk you through it."
    return impact, quick_win, bigger, next_step, call_topic, cta


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def _initial_email_sent_ids(queue_rows: list[dict[str, str]]) -> set[str]:
    sent: set[str] = set()
    for r in queue_rows:
        if (r.get("action") or "").strip().lower() != "initial email":
            continue
        if (r.get("status") or "").strip().lower() != "sent":
            continue
        pid = (r.get("prospect_id") or "").strip()
        if pid:
            sent.add(pid)
    return sent


def due_prospects() -> list[Prospect]:
    tracker_rows = _read_csv(AUDIT_PREVIEW_TRACKER_CSV)
    queue_rows = _read_csv(DAILY_OUTREACH_QUEUE_CSV)
    sent_ids = _initial_email_sent_ids(queue_rows)

    contact_by_id: dict[str, str] = {}
    for r in queue_rows:
        pid = (r.get("prospect_id") or "").strip()
        if not pid:
            continue
        name = (r.get("contact_name") or "").strip()
        if name:
            contact_by_id[pid] = name

    due: list[Prospect] = []
    for r in tracker_rows:
        if (r.get("audit_preview_required") or "").strip().upper() != "TRUE":
            continue
        status = (r.get("audit_preview_status") or "").strip()
        if status not in {"Ready to generate", "Not started"}:
            continue
        pid = (r.get("prospect_id") or "").strip()
        if not pid or pid not in sent_ids:
            continue

        due.append(
            Prospect(
                prospect_id=pid,
                company=(r.get("company") or "").strip(),
                website=(r.get("website") or "").strip(),
                audit_type=(r.get("audit_type") or "").strip(),
                thesis=(r.get("preview_thesis") or "").strip(),
                contact_name=contact_by_id.get(pid),
            )
        )
    return due


def generate_pdfs() -> list[tuple[Prospect, Path]]:
    due = due_prospects()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[tuple[Prospect, Path]] = []
    today = _today_iso()
    for p in due:
        slug = _slugify(p.company)
        out = OUTPUT_DIR / f"bridgeworks-audit-preview-{slug}-{today}.pdf"
        build_preview_pdf(p, out)
        generated.append((p, out))
    return generated


def update_trackers(pdf_outputs: list[tuple[Prospect, Path]], gmail_draft_ids: dict[str, str] | None = None) -> None:
    gmail_draft_ids = gmail_draft_ids or {}
    tracker_rows = _read_csv(AUDIT_PREVIEW_TRACKER_CSV)
    queue_rows = _read_csv(DAILY_OUTREACH_QUEUE_CSV)

    # Ensure columns exist
    tracker_fieldnames = list(tracker_rows[0].keys()) if tracker_rows else []
    for col in ["follow_up_1_draft_id", "last_generated_date"]:
        if col not in tracker_fieldnames:
            tracker_fieldnames.append(col)

    outputs_by_id = {p.prospect_id: out for p, out in pdf_outputs}
    today = _today_iso()

    for r in tracker_rows:
        pid = (r.get("prospect_id") or "").strip()
        if pid in outputs_by_id:
            out = outputs_by_id[pid]
            r["audit_preview_pdf"] = str(out.as_posix())
            r["last_generated_date"] = today
            draft_id = gmail_draft_ids.get(pid)
            if draft_id:
                r["follow_up_1_draft_id"] = draft_id
                r["audit_preview_status"] = "Follow-up 1 draft ready"
                r["next_action"] = "Review and manually send follow-up 1 in Gmail."
            else:
                r["audit_preview_status"] = "Audit preview ready"
                r["next_action"] = "Create follow-up 1 Gmail draft with PDF attached."

    _write_csv(AUDIT_PREVIEW_TRACKER_CSV, tracker_rows, tracker_fieldnames)

    # Update daily queue next_step when it matches the PDF task
    queue_fieldnames = list(queue_rows[0].keys()) if queue_rows else []
    for r in queue_rows:
        pid = (r.get("prospect_id") or "").strip()
        if pid not in outputs_by_id:
            continue
        if gmail_draft_ids.get(pid):
            r["next_step"] = "Review follow-up 1 Gmail draft and send manually."
        else:
            r["next_step"] = "Find email contact. Then create follow-up 1 Gmail draft with PDF attached."

    if queue_rows:
        _write_csv(DAILY_OUTREACH_QUEUE_CSV, queue_rows, queue_fieldnames)


def main() -> None:
    pdfs = generate_pdfs()
    print(f"generated_pdfs={len(pdfs)}")
    for p, out in pdfs:
        print(f"{p.prospect_id}\t{p.company}\t{out}")


if __name__ == "__main__":
    main()
