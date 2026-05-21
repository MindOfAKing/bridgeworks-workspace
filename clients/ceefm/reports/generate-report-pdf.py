"""Generate a CEEFM client report PDF from a markdown source.

Used to build the 4-PDF April 2026 report package:
  - CEEFM-April-2026-Executive-Report
  - CEEFM-May-2026-Action-Plan
  - CEEFM-April-2026-Delivery-Appendix
  - CEEFM-April-2026-Performance-Analytics-Appendix

Branded chrome on every page (ivory background, gold left accent rule, navy footer
band with BridgeWorks icon, page number, agency credit). Cover page has navy header
band with the document title, CEEFM logo, and BridgeWorks agency mark.

Usage:
    python generate-report-pdf.py SOURCE.md OUTPUT.pdf [SUBTITLE]

If SUBTITLE is omitted, the cover sub-line uses a default.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Paths and brand
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent
CHARTS_DIR = BASE / "charts" / "2026-04"
CAPTIONS_FILE = CHARTS_DIR / "captions.md"

def _first_existing_path(*candidates: Path) -> Path | None:
    for p in candidates:
        try:
            if p.exists():
                return p
        except OSError:
            continue
    return None


CEEFM_LOGO = _first_existing_path(
    (BASE.parent / "brand-visuals" / "logo" / "ceefm-logo.png"),
)

BW_ICON_LIGHT = _first_existing_path(
    (BASE.parent / "brand-visuals" / "bridgeworks" / "bridgeworks-icon-light-400px.png"),
    Path("C:/Users/ELITEX21012G2/brand-assets/bridgeworks/logos/bridgeworks-icon-light-400px.png"),
)

BW_ICON_DARK = _first_existing_path(
    (BASE.parent / "brand-visuals" / "bridgeworks" / "bridgeworks-icon-dark-400px.png"),
    Path("C:/Users/ELITEX21012G2/brand-assets/bridgeworks/logos/bridgeworks-icon-dark-400px.png"),
)

NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
SAGE = HexColor("#4A6741")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
WHITE = HexColor("#FFFFFF")
TABLE_HEADER_BG = NAVY
TABLE_ROW_ALT = HexColor("#EFE9DD")

W, H = A4
MARGIN_L = 2.2 * cm
MARGIN_R = 2.2 * cm
MARGIN_T = 2.6 * cm
MARGIN_B = 2.6 * cm

IMAGE_ANCHORS = {
    "01-": "GEO / AI Visibility Score",
    "02-": "Category breakdown",
    "03-": "Marketing Audit",
    "04-": "LinkedIn",
    "05-": "LinkedIn",
    "06-": "LinkedIn",
    "07-": "Sitemap",
    "08-": "Funnel",
    "B-": "Security headers",
    "H-": "llms.txt",
    "X1-": "Schema completeness",
    "X2-": "Stat counters",
    "X3-": "HU production typos",
}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

base_styles = getSampleStyleSheet()


def make_styles() -> dict[str, ParagraphStyle]:
    s: dict[str, ParagraphStyle] = {}
    s["body"] = ParagraphStyle(
        "body",
        parent=base_styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=CHARCOAL,
        spaceAfter=6,
    )
    s["body_quote"] = ParagraphStyle(
        "body_quote",
        parent=s["body"],
        leftIndent=18,
        rightIndent=18,
        textColor=NAVY,
        fontName="Helvetica-Oblique",
        spaceAfter=8,
    )
    s["h1"] = ParagraphStyle(
        "h1",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=10,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
    )
    s["h3"] = ParagraphStyle(
        "h3",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=6,
    )
    s["h4"] = ParagraphStyle(
        "h4",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=4,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        parent=s["body"],
        leftIndent=18,
        bulletIndent=4,
        spaceAfter=3,
    )
    s["caption"] = ParagraphStyle(
        "caption",
        parent=s["body"],
        fontSize=8.5,
        leading=11,
        textColor=WARM_GRAY,
        alignment=1,
        spaceBefore=4,
        spaceAfter=10,
    )
    s["meta"] = ParagraphStyle(
        "meta",
        parent=s["body"],
        fontSize=9,
        textColor=WARM_GRAY,
    )
    s["cover_kicker"] = ParagraphStyle(
        "cover_kicker",
        parent=s["body"],
        fontSize=10,
        textColor=GOLD,
        spaceAfter=8,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=32,
        textColor=IVORY,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub",
        parent=s["body"],
        fontSize=12,
        textColor=IVORY,
        leading=16,
    )
    s["cover_meta"] = ParagraphStyle(
        "cover_meta",
        parent=s["body"],
        fontSize=10,
        textColor=IVORY,
        leading=14,
    )
    s["cover_credit"] = ParagraphStyle(
        "cover_credit",
        parent=s["body"],
        fontSize=10,
        textColor=CHARCOAL,
        leading=14,
    )
    return s


# ---------------------------------------------------------------------------
# Page chrome
# ---------------------------------------------------------------------------


def draw_chrome(canvas, doc):
    """Single chrome callback: cover styling on page 1, body styling on pages 2+.
    Uses one PageTemplate with one Frame to avoid empty transition pages from NextPageTemplate."""
    if doc.page == 1:
        draw_cover_chrome(canvas, doc)
    else:
        draw_body_chrome(canvas, doc)


def draw_body_chrome(canvas, doc):
    """Body page: ivory background, gold left accent, BridgeWorks icon in footer, page number, credit."""
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 6, H, fill=1, stroke=0)

    # Footer chrome
    footer_y = 18
    icon_size = 16
    if BW_ICON_DARK and BW_ICON_DARK.exists():
        try:
            canvas.drawImage(
                str(BW_ICON_DARK),
                MARGIN_L,
                footer_y - 4,
                width=icon_size,
                height=icon_size,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(WARM_GRAY)
    canvas.drawString(
        MARGIN_L + icon_size + 6,
        footer_y,
        "BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency",
    )
    canvas.drawRightString(W - MARGIN_R, footer_y, f"Page {doc.page}")
    canvas.restoreState()


def draw_cover_chrome(canvas, doc):
    """Cover: navy header band, gold accent bar, CEEFM logo in band, BridgeWorks icon in footer."""
    canvas.saveState()
    # Background ivory
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold left accent
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 6, H, fill=1, stroke=0)
    # Navy header band (top 45%)
    band_h = H * 0.45
    band_y = H - band_h
    canvas.setFillColor(NAVY)
    canvas.rect(0, band_y, W, band_h, fill=1, stroke=0)
    # Gold thin rule beneath band
    canvas.setFillColor(GOLD)
    canvas.rect(0, band_y - 4, W, 4, fill=1, stroke=0)

    # CEEFM logo top-right of the navy band (client mark)
    if CEEFM_LOGO and CEEFM_LOGO.exists():
        try:
            logo_size = 64
            canvas.drawImage(
                str(CEEFM_LOGO),
                W - MARGIN_R - logo_size,
                H - MARGIN_T - 6,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    # BridgeWorks icon bottom-right above the footer (agency mark)
    if BW_ICON_DARK and BW_ICON_DARK.exists():
        try:
            bw_size = 28
            canvas.drawImage(
                str(BW_ICON_DARK),
                W - MARGIN_R - bw_size,
                42,
                width=bw_size,
                height=bw_size,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    # Footer
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(WARM_GRAY)
    canvas.drawString(
        MARGIN_L,
        18,
        "Prepared by BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency",
    )
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*")
INLINE_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
INLINE_CODE = re.compile(r"`([^`]+?)`")
INLINE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def md_inline_to_html(text: str) -> str:
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    text = INLINE_CODE.sub(
        lambda m: f'<font name="Helvetica-Oblique" color="#4A6741">{m.group(1)}</font>',
        text,
    )
    text = INLINE_BOLD.sub(r"<b>\1</b>", text)
    text = INLINE_ITALIC.sub(r"<i>\1</i>", text)
    text = INLINE_LINK.sub(r'<link href="\2" color="#4A6741"><u>\1</u></link>', text)
    return text


def parse_table_block(lines: list[str]) -> Table | None:
    rows: list[list[str]] = []
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        if re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return None

    para_style = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=11, textColor=CHARCOAL)
    header_style = ParagraphStyle("header_cell", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=IVORY)

    data: list[list[Paragraph]] = []
    for i, row in enumerate(rows):
        styled = []
        for cell in row:
            html = md_inline_to_html(cell)
            styled.append(Paragraph(html, header_style if i == 0 else para_style))
        data.append(styled)
    n_cols = max(len(r) for r in data)
    avail = W - MARGIN_L - MARGIN_R
    col_w = avail / n_cols
    table = Table(data, colWidths=[col_w] * n_cols, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), IVORY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [IVORY, TABLE_ROW_ALT]),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, GOLD),
                ("BOX", (0, 0), (-1, -1), 0.3, WARM_GRAY),
            ]
        )
    )
    return table


def load_captions() -> dict[str, str]:
    if not CAPTIONS_FILE.exists():
        return {}
    captions: dict[str, str] = {}
    for line in CAPTIONS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+([^\s].+\.png)\s*$", line.strip())
        if m:
            current = m.group(1)
            captions[current] = ""
            continue
    # second pass for caption text
    captions2: dict[str, str] = {}
    current: str | None = None
    for line in CAPTIONS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(.+\.png)\s*$", line.strip())
        if m:
            current = m.group(1).strip()
            captions2[current] = ""
            continue
        if current and line.strip():
            captions2[current] = (captions2[current] + " " + line.strip()).strip()
    return captions2


def find_chart_files(allowed_prefixes: list[str] | None = None) -> dict[str, list[Path]]:
    """Find chart PNGs in the charts dir. If allowed_prefixes is given, only return files whose
    filename starts with one of those prefixes."""
    if not CHARTS_DIR.exists():
        return {}
    found: dict[str, list[Path]] = {prefix: [] for prefix in IMAGE_ANCHORS}
    for f in sorted(CHARTS_DIR.glob("*.png")):
        for prefix in IMAGE_ANCHORS:
            if not f.name.startswith(prefix):
                continue
            if allowed_prefixes is not None and prefix not in allowed_prefixes:
                continue
            found[prefix].append(f)
            break
    return found


def make_image_flowables(path: Path, caption: str | None) -> list:
    """Image + caption + spacer. No KeepTogether (lets engine break naturally)."""
    avail = W - MARGIN_L - MARGIN_R
    img = Image(str(path), width=avail, height=avail * 0.55, kind="proportional")
    flow = [img]
    if caption:
        flow.append(Paragraph(md_inline_to_html(caption), make_styles()["caption"]))
    flow.append(Spacer(1, 8))
    return flow


# ---------------------------------------------------------------------------
# Markdown -> Platypus flowables
# ---------------------------------------------------------------------------


def parse_markdown(md_text: str, styles: dict[str, ParagraphStyle]) -> list:
    lines = md_text.splitlines()
    flowables: list = []
    i = 0
    pending_table: list[str] = []

    def flush_table():
        nonlocal pending_table
        if pending_table:
            tbl = parse_table_block(pending_table)
            if tbl is not None:
                flowables.append(tbl)
                flowables.append(Spacer(1, 6))
            pending_table = []

    skip_first_h1 = True

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|"):
            pending_table.append(line)
            i += 1
            continue
        else:
            flush_table()

        if stripped in ("---", "***"):
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        if not stripped:
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        if stripped.startswith("#"):
            level = 0
            while level < len(stripped) and stripped[level] == "#":
                level += 1
            text = stripped[level:].strip()
            if level == 1 and skip_first_h1:
                skip_first_h1 = False
                i += 1
                continue
            style_key = {1: "h1", 2: "h2", 3: "h3", 4: "h4"}.get(level, "h4")
            flowables.append(Paragraph(md_inline_to_html(text), styles[style_key]))
            i += 1
            continue

        if stripped.startswith(">"):
            text = stripped.lstrip(">").strip()
            flowables.append(Paragraph(md_inline_to_html(text), styles["body_quote"]))
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            bullet_text = stripped[2:].strip()
            flowables.append(
                Paragraph(f"&bull; {md_inline_to_html(bullet_text)}", styles["bullet"])
            )
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)", stripped)
        if m:
            flowables.append(
                Paragraph(
                    f"{stripped.split(' ', 1)[0]} {md_inline_to_html(m.group(1))}",
                    styles["bullet"],
                )
            )
            i += 1
            continue

        para_lines = [stripped]
        j = i + 1
        while (
            j < len(lines)
            and lines[j].strip()
            and not lines[j].strip().startswith(("#", "-", "*", "|", ">", "```"))
            and not re.match(r"^\d+\.\s", lines[j].strip())
        ):
            para_lines.append(lines[j].strip())
            j += 1
        para_text = " ".join(para_lines)
        flowables.append(Paragraph(md_inline_to_html(para_text), styles["body"]))
        i = j

    flush_table()
    return flowables


def insert_images(flowables: list, charts: dict[str, list[Path]], captions: dict[str, str]) -> list:
    """Insert image flowables after the first paragraph that starts with each anchor text."""
    if not charts:
        return flowables

    anchor_to_images: dict[str, list] = {}
    for prefix, paths in charts.items():
        if not paths:
            continue
        anchor = IMAGE_ANCHORS[prefix]
        for path in paths:
            cap = captions.get(path.name, path.stem.replace("-", " ").title())
            anchor_to_images.setdefault(anchor, []).extend(make_image_flowables(path, cap))

    if not anchor_to_images:
        return flowables

    out: list = []
    for fl in flowables:
        out.append(fl)
        if isinstance(fl, Paragraph):
            try:
                plain = re.sub(r"<[^>]+>", "", fl.text or "")
            except Exception:
                plain = ""
            for anchor_text, imgs in list(anchor_to_images.items()):
                if anchor_text.lower() in plain.lower():
                    out.extend(imgs)
                    del anchor_to_images[anchor_text]
                    break
    return out


# ---------------------------------------------------------------------------
# Cover
# ---------------------------------------------------------------------------


def cover_flowables(styles: dict[str, ParagraphStyle], title: str, subtitle: str) -> list:
    """Cover flowables sized to fit cleanly above the lower-third 'prepared for/by' block.
    The chrome callback paints the navy header band; this flow lays text on top of and below it."""
    flow = [
        Spacer(1, 1.0 * cm),
        Paragraph("CONFIDENTIAL  ·  CLIENT REPORT", styles["cover_kicker"]),
        Spacer(1, 0.15 * cm),
        Paragraph(title, styles["cover_title"]),
        Spacer(1, 0.3 * cm),
        Paragraph(subtitle, styles["cover_sub"]),
        Spacer(1, 0.4 * cm),
        Paragraph("CEEFM Kft  ·  BridgeWorks", styles["cover_meta"]),
        Paragraph("Issued: 2026-04-30", styles["cover_meta"]),
        # Single moderate spacer pushes the Prepared blocks below the navy band; a smaller
        # value avoids overflow that creates a transition page.
        Spacer(1, 7.0 * cm),
        Paragraph(
            "<b>Prepared for</b><br/>Victor Danmagaji<br/>Managing Director, CEEFM Kft",
            styles["cover_credit"],
        ),
        Spacer(1, 0.3 * cm),
        Paragraph(
            "<b>Prepared by</b><br/>Emmanuel Ehigbai<br/>BridgeWorks  ·  office@bridgeworks.agency",
            styles["cover_credit"],
        ),
        PageBreak(),
    ]
    return flow


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


def build(source_md: Path, output_pdf: Path, title: str, subtitle: str, allowed_chart_prefixes: list[str] | None = None) -> None:
    if not source_md.exists():
        raise SystemExit(f"Missing source markdown: {source_md}")

    md_text = source_md.read_text(encoding="utf-8")
    styles = make_styles()
    captions = load_captions()
    charts = find_chart_files(allowed_prefixes=allowed_chart_prefixes)

    body_flowables = parse_markdown(md_text, styles)
    body_flowables = insert_images(body_flowables, charts, captions)

    flow = cover_flowables(styles, title, subtitle) + body_flowables

    page_frame = Frame(
        MARGIN_L,
        MARGIN_B,
        W - MARGIN_L - MARGIN_R,
        H - MARGIN_T - MARGIN_B,
        id="page",
        showBoundary=0,
    )

    doc = BaseDocTemplate(
        str(output_pdf),
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title=title,
        author="Emmanuel Ehigbai / BridgeWorks",
        subject=f"CEEFM April 2026 {title}",
    )
    doc.addPageTemplates(
        [PageTemplate(id="page", frames=[page_frame], onPage=draw_chrome)]
    )
    doc.build(flow)

    n_charts = sum(len(v) for v in charts.values()) if charts else 0
    print(f"Wrote {output_pdf}")
    print(f"Available chart pool: {n_charts}; embedded where anchors matched")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(
            "Usage: generate-report-pdf.py SOURCE.md OUTPUT.pdf [SUBTITLE] [CHARTS_FILTER]\n"
            "  CHARTS_FILTER: comma-separated chart prefix list (e.g. '01-,02-,03-,X1-')\n"
            "                 'all' = embed all matching, 'none' = embed none. Default: all."
        )
    source_md = Path(args[0]).resolve()
    output_pdf = Path(args[1]).resolve()
    stem = output_pdf.stem
    title = stem.replace("-", " ").replace("CEEFM ", "").replace("April 2026 ", "").replace("May 2026 ", "")
    subtitle = args[2] if len(args) >= 3 else "Engagement Update  ·  Month 1 of 16  ·  Weeks 1-5"
    allowed: list[str] | None
    if len(args) >= 4:
        flag = args[3].strip().lower()
        if flag == "all":
            allowed = None
        elif flag == "none":
            allowed = []
        else:
            allowed = [p.strip() for p in args[3].split(",") if p.strip()]
    else:
        allowed = None
    build(source_md, output_pdf, title=title, subtitle=subtitle, allowed_chart_prefixes=allowed)


if __name__ == "__main__":
    main()
