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


NAVY = colors.HexColor("#101B2D")
INK = colors.HexColor("#202936")
GOLD = colors.HexColor("#B98512")
CREAM = colors.HexColor("#F5F1E8")
MIST = colors.HexColor("#F3F5F6")
MID = colors.HexColor("#667085")
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
    canvas.rect(0, height - 20 * mm, width, 20 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, height - 21.5 * mm, width, 1.5 * mm, fill=1, stroke=0)

    if logo.exists():
        canvas.drawImage(str(logo), 22 * mm, height - 74 * mm, width=48 * mm, height=48 * mm, preserveAspectRatio=True, mask="auto")

    canvas.setFont(FONT_BOLD, 9)
    canvas.setFillColor(GOLD)
    canvas.drawString(22 * mm, height - 88 * mm, label.upper())

    title_style = ParagraphStyle(
        "CoverTitle",
        fontName=FONT_BOLD,
        fontSize=29,
        leading=33,
        textColor=NAVY,
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
    title_p.wrapOn(canvas, 165 * mm, 70 * mm)
    title_p.drawOn(canvas, 22 * mm, height - 152 * mm)

    y = height - 166 * mm
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

    canvas.setFont(FONT, 8.5)
    canvas.setFillColor(MID)
    canvas.drawString(22 * mm, 17 * mm, "BridgeWorks | office@bridgeworks.agency | Budapest")
    canvas.restoreState()


def body_page(canvas, doc):
    width, height = A4
    canvas.saveState()
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
    canvas.drawString(18 * mm, 9.5 * mm, "DRAFT FOR REVIEW")
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
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, MIST]),
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
        onPage=lambda canvas, current_doc: cover_page(
            canvas, current_doc, title, subtitle, metadata, args.logo, args.label
        ),
    )
    body_template = PageTemplate(id="body", frames=[frame], onPage=body_page)
    doc.addPageTemplates([cover_template, body_template])

    styles = build_styles()
    story = [NextPageTemplate("body"), PageBreak()]
    story.extend(build_story(lines, start, styles))
    doc.build(story)
    print(args.output)


if __name__ == "__main__":
    main()
