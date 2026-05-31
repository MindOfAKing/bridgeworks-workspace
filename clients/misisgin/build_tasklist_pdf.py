"""Generate a BridgeWorks-branded PDF from the Misi's Gin engagement task list.
Brand constants: Ivory bg #F5F0E8, Navy #0F1A2E, Gold #B8860B, Charcoal #1C2B3A.
"""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, FrameBreak,
    NextPageTemplate, PageBreak, Flowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Segoe UI Symbol carries the ballot-box glyph that Helvetica lacks
pdfmetrics.registerFont(TTFont("SymUI", "C:/Windows/Fonts/seguisym.ttf"))

IVORY = HexColor("#F5F0E8")
NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
CHARCOAL = HexColor("#1C2B3A")
WARMGRAY = HexColor("#6B6560")
SAGE = HexColor("#4A6741")

SRC = "ENGAGEMENT-TASKLIST-misisgin.md"
OUT = "ENGAGEMENT-TASKLIST-misisgin.pdf"
FOOTER = "office@bridgeworks.agency  ·  bridgeworks.agency"

PAGE_W, PAGE_H = A4
MARGIN_L = 24 * mm
MARGIN_R = 18 * mm
MARGIN_T = 24 * mm
MARGIN_B = 22 * mm


def bg_and_chrome(canvas, doc, cover=False):
    canvas.saveState()
    # Ivory background
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # 6px gold left accent bar, full height
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 6, PAGE_H, fill=1, stroke=0)
    if not cover:
        # Footer
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(WARMGRAY)
        canvas.drawCentredString(PAGE_W / 2, 12 * mm, FOOTER)
        canvas.setFillColor(GOLD)
        canvas.drawRightString(PAGE_W - MARGIN_R, 12 * mm, str(doc.page))
    canvas.restoreState()


def on_cover(canvas, doc):
    bg_and_chrome(canvas, doc, cover=True)
    canvas.saveState()
    # Navy header band
    band_h = 78 * mm
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
    # Gold accent bar over the band (keep visible)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - band_h, 6, band_h, fill=1, stroke=0)
    # Cover text
    canvas.setFillColor(IVORY)
    canvas.setFont("Times-Bold", 30)
    canvas.drawString(MARGIN_L, PAGE_H - 34 * mm, "Engagement Task List")
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Bold", 20)
    canvas.drawString(MARGIN_L, PAGE_H - 47 * mm, "Misi's Gin")
    canvas.setFillColor(IVORY)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(MARGIN_L, PAGE_H - 58 * mm, "Kenyeres Mihály E.V.  ·  Budapest")
    canvas.setFont("Helvetica", 9)
    canvas.drawString(MARGIN_L, PAGE_H - 66 * mm,
                      "Prepared by BridgeWorks  ·  2026-05-31")
    # Footer on cover too
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(WARMGRAY)
    canvas.drawCentredString(PAGE_W / 2, 12 * mm, FOOTER)
    canvas.restoreState()


def on_body(canvas, doc):
    bg_and_chrome(canvas, doc, cover=False)


class HRule(Flowable):
    def __init__(self, width, color=GOLD, thickness=0.8):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness

    def wrap(self, aw, ah):
        return (self.width, 6)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 3, self.width, 3)


# Styles
H2 = ParagraphStyle("H2", fontName="Times-Bold", fontSize=15, leading=19,
                    textColor=NAVY, spaceBefore=14, spaceAfter=4)
H3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                    textColor=SAGE, spaceBefore=9, spaceAfter=2)
BODY = ParagraphStyle("BODY", fontName="Helvetica", fontSize=9.8, leading=14,
                      textColor=CHARCOAL, alignment=TA_LEFT, spaceAfter=4)
LEAD = ParagraphStyle("LEAD", parent=BODY, spaceBefore=2, spaceAfter=5)
CHECK = ParagraphStyle("CHECK", fontName="Helvetica", fontSize=9.6, leading=13.5,
                       textColor=CHARCOAL, leftIndent=12, firstLineIndent=-12,
                       spaceAfter=2.5)
BULLET = ParagraphStyle("BULLET", parent=CHECK)
ITALIC = ParagraphStyle("ITALIC", fontName="Helvetica-Oblique", fontSize=8.5,
                        leading=12, textColor=WARMGRAY, spaceBefore=6)


def inline(text):
    # escape & < >
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # inline code
    text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)
    return text


def parse(md):
    story = []
    content_w = PAGE_W - MARGIN_L - MARGIN_R
    lines = md.split("\n")
    skipped_first_h1 = False
    # skip the leading metadata block (between first # and the first ##) except keep nothing
    started = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            skipped_first_h1 = True
            continue
        if not started:
            # begin rendering once we hit the first ## section
            if line.startswith("## "):
                started = True
            else:
                continue
        if line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), H2))
            story.append(HRule(content_w))
            story.append(Spacer(1, 2))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), H3))
        elif line.startswith("- [ ] "):
            story.append(Paragraph('<font name="SymUI" color="#B8860B">&#9744;</font>'
                                   "&nbsp;&nbsp;" + inline(line[6:]), CHECK))
        elif line.startswith("- [x] "):
            story.append(Paragraph('<font name="SymUI" color="#B8860B">&#9745;</font>'
                                   "&nbsp;&nbsp;" + inline(line[6:]), CHECK))
        elif line.startswith("- "):
            story.append(Paragraph("<font color='#B8860B'>•</font>&nbsp;&nbsp;"
                                   + inline(line[2:]), BULLET))
        elif line.startswith("---"):
            story.append(Spacer(1, 4))
        elif line.startswith("*") and line.endswith("*") and len(line) > 2:
            story.append(Paragraph(inline(line.strip("*")), ITALIC))
        elif line.strip() == "":
            continue
        else:
            story.append(Paragraph(inline(line), LEAD))
    return story


def main():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()

    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Misi's Gin Engagement Task List", author="BridgeWorks",
    )
    frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                  PAGE_H - MARGIN_T - MARGIN_B, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=on_cover),
        PageTemplate(id="body", frames=[frame], onPage=on_body),
    ])

    story = [NextPageTemplate("body"), PageBreak()]
    story += parse(md)
    doc.build(story)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
