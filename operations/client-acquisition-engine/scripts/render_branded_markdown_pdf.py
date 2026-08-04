from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    LongTable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


NAVY = colors.HexColor("#0F1A2E")
INK = colors.HexColor("#1C2B3A")
GOLD = colors.HexColor("#B8860B")
CREAM = colors.HexColor("#F5F0E8")
MIST = colors.HexColor("#EEE8DE")
MID = colors.HexColor("#6B6560")
WHITE = colors.white


def register_fonts() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("BridgeSans", str(regular)))
        pdfmetrics.registerFont(TTFont("BridgeSans-Bold", str(bold)))
        return "BridgeSans", "BridgeSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def inline_markup(value: str) -> str:
    escaped = html.escape(value.strip())
    escaped = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", r'<link href="\2" color="#7A5A10"><u>\1</u></link>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)
    return escaped


def parse_front_matter(lines: list[str]) -> tuple[str, str, list[str], int]:
    title = lines[0].removeprefix("# ").strip()
    cursor = 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1

    subtitle = ""
    if cursor < len(lines) and lines[cursor].startswith("## "):
        subtitle = lines[cursor][3:].strip()
        cursor += 1

    metadata: list[str] = []
    while cursor < len(lines):
        line = lines[cursor].strip()
        if line.startswith("## "):
            break
        if line:
            metadata.append(line)
        cursor += 1
    return title, subtitle, metadata, cursor


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=9.4,
            leading=14.2,
            textColor=INK,
            spaceAfter=4.5 * mm,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=NAVY,
            spaceBefore=8 * mm,
            spaceAfter=4 * mm,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=styles["Heading3"],
            fontName=FONT_BOLD,
            fontSize=12.2,
            leading=15,
            textColor=NAVY,
            spaceBefore=5 * mm,
            spaceAfter=2.5 * mm,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=9.2,
            leading=13.5,
            leftIndent=6 * mm,
            firstLineIndent=-3.5 * mm,
            textColor=INK,
            spaceAfter=1.5 * mm,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=styles["BodyText"],
            fontName=FONT_BOLD,
            fontSize=12,
            leading=17,
            leftIndent=8 * mm,
            rightIndent=8 * mm,
            textColor=NAVY,
            borderColor=GOLD,
            borderWidth=0,
            borderPadding=5 * mm,
            backColor=CREAM,
            spaceBefore=3 * mm,
            spaceAfter=5 * mm,
        ),
        "table": ParagraphStyle(
            "TableCell",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=7.6,
            leading=10.2,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=styles["BodyText"],
            fontName=FONT_BOLD,
            fontSize=7.7,
            leading=10.2,
            textColor=WHITE,
        ),
    }


def cover_page(canvas, doc, title: str, subtitle: str, metadata: list[str], logo: Path, label: str):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, height * 0.68, width, height * 0.32, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 2.1 * mm, height, fill=1, stroke=0)
    canvas.rect(0, height * 0.68 - 1.5 * mm, width, 1.5 * mm, fill=1, stroke=0)

    if logo.exists():
        canvas.drawImage(str(logo), 22 * mm, height - 49 * mm, width=34 * mm, height=26 * mm, preserveAspectRatio=True, mask="auto")

    canvas.setFont(FONT_BOLD, 9)
    canvas.setFillColor(GOLD)
    canvas.drawString(22 * mm, height - 60 * mm, label.upper())

    title_style = ParagraphStyle(
        "CoverTitle",
        fontName=FONT_BOLD,
        fontSize=26,
        leading=30,
        textColor=WHITE,
        alignment=TA_LEFT,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName=FONT,
        fontSize=14,
        leading=19,
        textColor=MID,
        alignment=TA_LEFT,
    )
    meta_style = ParagraphStyle(
        "CoverMeta",
        fontName=FONT,
        fontSize=9.5,
        leading=14,
        textColor=INK,
        alignment=TA_LEFT,
    )

    title_p = Paragraph(inline_markup(title), title_style)
    _, title_h = title_p.wrap(165 * mm, 60 * mm)
    title_p.drawOn(canvas, 22 * mm, height - 60 * mm - title_h)
    canvas.setFont(FONT, 13)
    canvas.setFillColor(GOLD)
    canvas.drawString(22 * mm, height * 0.68 + 4 * mm, "Powered by BridgeWorks")

    y = height * 0.68 - 18 * mm
    if subtitle:
        sub_p = Paragraph(inline_markup(subtitle), subtitle_style)
        _, sub_h = sub_p.wrap(165 * mm, 45 * mm)
        sub_p.drawOn(canvas, 22 * mm, y - sub_h)
        y -= sub_h + 10 * mm

    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(22 * mm, y, 76 * mm, y)
    y -= 10 * mm

    for item in metadata[:6]:
        p = Paragraph(inline_markup(item), meta_style)
        _, ph = p.wrap(165 * mm, 20 * mm)
        p.drawOn(canvas, 22 * mm, y - ph)
        y -= ph + 2.5 * mm

    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MID)
    canvas.drawCentredString(width / 2, 22, "BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency")
    canvas.restoreState()


def body_page(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 2.1 * mm, height, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 11 * mm, width, 11 * mm, fill=1, stroke=0)
    canvas.setFont(FONT_BOLD, 7.5)
    canvas.setFillColor(WHITE)
    canvas.drawString(18 * mm, height - 7.3 * mm, "BRIDGEWORKS")
    canvas.setFont(FONT, 7.5)
    canvas.drawRightString(width - 18 * mm, height - 7.3 * mm, doc.title[:80])
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MID)
    canvas.drawCentredString(width / 2, 9.5 * mm, "BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency")
    canvas.drawRightString(width - 18 * mm, 9.5 * mm, str(doc.page))
    canvas.restoreState()


def parse_table(lines: list[str], start: int, styles) -> tuple[LongTable, int]:
    rows: list[list[str]] = []
    cursor = start
    while cursor < len(lines) and lines[cursor].strip().startswith("|"):
        cells = [cell.strip() for cell in lines[cursor].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            rows.append(cells)
        cursor += 1

    width = 174 * mm
    columns = max(len(row) for row in rows)
    normalized = [row + [""] * (columns - len(row)) for row in rows]
    data = []
    for row_index, row in enumerate(normalized):
        style = styles["table_head"] if row_index == 0 else styles["table"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])

    if columns == 2:
        col_widths = [54 * mm, 120 * mm]
    elif columns == 3:
        col_widths = [42 * mm, 42 * mm, 90 * mm]
    elif columns == 4:
        col_widths = [34 * mm, 34 * mm, 38 * mm, 68 * mm]
    else:
        col_widths = [width / columns] * columns

    table = LongTable(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("BACKGROUND", (0, 1), (-1, -1), CREAM),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, MIST]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D7DCE1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table, cursor


def build_story(lines: list[str], start: int, styles) -> list:
    story: list = []
    cursor = start
    paragraph_lines: list[str] = []

    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            story.append(Paragraph(inline_markup(text), styles["body"]))
            paragraph_lines.clear()

    while cursor < len(lines):
        raw = lines[cursor]
        line = raw.strip()

        if not line:
            flush_paragraph()
            cursor += 1
            continue

        if line == "<!-- keep-start -->":
            flush_paragraph()
            end = cursor + 1
            while end < len(lines) and lines[end].strip() != "<!-- keep-end -->":
                end += 1
            if end >= len(lines):
                raise ValueError("Missing <!-- keep-end --> marker")
            story.append(KeepTogether(build_story(lines[cursor + 1 : end], 0, styles)))
            cursor = end + 1
            continue

        if line == "<!-- keep-end -->":
            cursor += 1
            continue

        spacer = re.fullmatch(r"<!-- spacer:(\d+) -->", line)
        if spacer:
            flush_paragraph()
            story.append(Spacer(1, int(spacer.group(1)) * mm))
            cursor += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[3:]), styles["h2"]))
            cursor += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[4:]), styles["h3"]))
            cursor += 1
            continue

        if line.startswith("|") and cursor + 1 < len(lines) and lines[cursor + 1].strip().startswith("|"):
            flush_paragraph()
            table, cursor = parse_table(lines, cursor, styles)
            story.extend([table, Spacer(1, 4 * mm)])
            continue

        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), styles["quote"]))
            cursor += 1
            continue

        bullet = re.match(r"^-\s+(.*)$", line)
        checkbox = re.match(r"^-\s+\[[ xX~!]\]\s+(.*)$", line)
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if checkbox:
            flush_paragraph()
            story.append(Paragraph("- " + inline_markup(checkbox.group(1)), styles["bullet"]))
            cursor += 1
            continue
        if bullet:
            flush_paragraph()
            story.append(Paragraph("- " + inline_markup(bullet.group(1)), styles["bullet"]))
            cursor += 1
            continue
        if numbered:
            flush_paragraph()
            story.append(Paragraph(numbered.group(1) + ". " + inline_markup(numbered.group(2)), styles["bullet"]))
            cursor += 1
            continue

        paragraph_lines.append(raw)
        cursor += 1

    flush_paragraph()
    return story


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--label", default="BridgeWorks evidence report")
    parser.add_argument(
        "--logo",
        type=Path,
        default=Path("clients/emmanuel/brand-system/bridgeworks-watermark.png"),
    )
    args = parser.parse_args()

    lines = args.input.read_text(encoding="utf-8").splitlines()
    title, subtitle, metadata, start = parse_front_matter(lines)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(args.output),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=19 * mm,
        bottomMargin=19 * mm,
        title=title,
        author="BridgeWorks",
        subject=args.label,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    cover_template = PageTemplate(
        id="cover",
        frames=[frame],
        autoNextPageTemplate="body",
        onPage=lambda canvas, current_doc: cover_page(
            canvas, current_doc, title, subtitle, metadata, args.logo, args.label
        ),
    )
    body_template = PageTemplate(
        id="body",
        frames=[frame],
        autoNextPageTemplate="body",
        onPage=body_page,
    )
    doc.addPageTemplates([cover_template, body_template])

    styles = build_styles()
    story = [PageBreak()]
    story.extend(build_story(lines, start, styles))
    doc.build(story)
    print(args.output)


if __name__ == "__main__":
    main()
