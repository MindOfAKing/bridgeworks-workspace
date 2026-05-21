from pathlib import Path
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OPS = Path("C:/Users/ELITEX21012G2/Projects/bridgeworks-workspace/operations")
SOURCE = OPS / "bridgeworks-business-sop.md"
OUTPUT = OPS / "BridgeWorks Business Operating SOP.pdf"
FONT_DIR = OPS / "fonts"

pdfmetrics.registerFont(TTFont("Playfair", str(FONT_DIR / "PlayfairDisplay-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Playfair-Bold", str(FONT_DIR / "PlayfairDisplay-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Inter", str(FONT_DIR / "Inter-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Inter-Light", str(FONT_DIR / "Inter-Light.ttf")))
pdfmetrics.registerFont(TTFont("Inter-Medium", str(FONT_DIR / "Inter-Medium.ttf")))

NAVY = colors.HexColor("#0F1A2E")
CHARCOAL = colors.HexColor("#1C2B3A")
GOLD = colors.HexColor("#B8860B")
GOLD_LIGHT = colors.HexColor("#D4A843")
SAGE = colors.HexColor("#4A6741")
IVORY = colors.HexColor("#F5F0E8")
MUTED = colors.HexColor("#6B7280")
LINE = colors.HexColor("#D8CDBE")
CODE_BG = colors.HexColor("#EFE7DC")

PAGE_W, PAGE_H = A4
LEFT = 22 * mm
RIGHT = 18 * mm
TOP = 24 * mm
BOTTOM = 22 * mm
MAX_W = PAGE_W - LEFT - RIGHT

c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle("BridgeWorks Business Operating SOP")
c.setAuthor("BridgeWorks")
page_no = 0
y = PAGE_H - TOP


def clean(text):
    text = text.replace("—", "-").replace("–", "-").replace("™", "TM")
    text = text.replace("€", "EUR ").replace("§", "Section ").replace("·", "-")
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def draw_bridge_icon(x, y, scale=1.0, light=True):
    fill = IVORY if light else NAVY
    c.setFillColor(fill)
    c.roundRect(x, y, 36 * scale, 12 * scale, 3 * scale, stroke=0, fill=1)
    c.roundRect(x + 88 * scale, y + 4 * scale, 36 * scale, 12 * scale, 3 * scale, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5 * scale)
    path = c.beginPath()
    path.moveTo(x + 36 * scale, y + 12 * scale)
    path.curveTo(x + 48 * scale, y + 32 * scale, x + 76 * scale, y + 36 * scale, x + 88 * scale, y + 16 * scale)
    c.drawPath(path, stroke=1, fill=0)


def draw_lockup(x, y, scale=1.0, light=True):
    draw_bridge_icon(x, y - 2 * scale, scale=0.18 * scale, light=light)
    text_x = x + 31 * scale
    color = IVORY if light else NAVY
    c.setFillColor(color)
    c.setFont("Playfair", 16 * scale)
    c.drawString(text_x, y, "BridgeWorks")
    width = pdfmetrics.stringWidth("BridgeWorks", "Playfair", 16 * scale)
    c.setFillColor(GOLD)
    c.setFont("Playfair", 16 * scale)
    c.drawString(text_x + width, y, ".agency")


def cover():
    global page_no
    page_no += 1
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, PAGE_W, 58 * mm, stroke=0, fill=1)
    c.setStrokeColor(SAGE)
    c.setLineWidth(5)
    c.arc(35 * mm, 70 * mm, PAGE_W - 35 * mm, 185 * mm, 0, 180)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.arc(45 * mm, 78 * mm, PAGE_W - 45 * mm, 176 * mm, 0, 180)
    draw_lockup(24 * mm, PAGE_H - 34 * mm, scale=1.35, light=True)
    c.setFillColor(GOLD_LIGHT)
    c.setFont("Inter-Medium", 8.5)
    c.drawString(24 * mm, PAGE_H - 69 * mm, "STANDARD OPERATING PROCEDURE")
    c.setFillColor(IVORY)
    c.setFont("Playfair-Bold", 43)
    c.drawString(24 * mm, PAGE_H - 92 * mm, "Business")
    c.drawString(24 * mm, PAGE_H - 109 * mm, "Operating SOP")
    c.setFillColor(colors.HexColor("#E8DDCA"))
    c.setFont("Inter-Light", 12)
    c.drawString(24 * mm, PAGE_H - 128 * mm, "A practical operating manual for running BridgeWorks")
    c.drawString(24 * mm, PAGE_H - 136 * mm, "as a solo AI-powered digital growth studio.")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(24 * mm, 62 * mm, PAGE_W - 24 * mm, 62 * mm)
    c.setFillColor(IVORY)
    c.setFont("Inter-Medium", 8)
    c.drawString(24 * mm, 39 * mm, "OWNER")
    c.setFont("Inter", 10)
    c.drawString(24 * mm, 32 * mm, "Emmanuel Ehigbai")
    c.setFont("Inter-Medium", 8)
    c.drawString(24 * mm, 22 * mm, "VERSION")
    c.setFont("Inter", 10)
    c.drawString(24 * mm, 15 * mm, "1.0 | 17 May 2026")
    c.setFillColor(GOLD)
    c.rect(PAGE_W - 30 * mm, 0, 6 * mm, PAGE_H, stroke=0, fill=1)
    c.showPage()


def header_footer():
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 12.8 * mm, PAGE_W, 0.8 * mm, stroke=0, fill=1)
    draw_lockup(LEFT, PAGE_H - 8 * mm, scale=0.62, light=True)
    c.setFont("Inter-Medium", 7.3)
    c.setFillColor(colors.Color(245 / 255, 240 / 255, 232 / 255, alpha=0.72))
    c.drawRightString(PAGE_W - RIGHT, PAGE_H - 6.7 * mm, "BUSINESS OPERATING SOP")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.line(LEFT, BOTTOM - 4 * mm, PAGE_W - RIGHT, BOTTOM - 4 * mm)
    c.setFont("Inter", 7.2)
    c.setFillColor(MUTED)
    c.drawString(LEFT, BOTTOM - 8 * mm, "bridgeworks.agency")
    c.drawRightString(PAGE_W - RIGHT, BOTTOM - 8 * mm, f"Page {page_no}")


def new_page():
    global page_no, y
    page_no += 1
    header_footer()
    y = PAGE_H - TOP


def ensure(space):
    global y
    if y - space < BOTTOM:
        c.showPage()
        new_page()


def wrap_lines(text, font, size, width):
    avg = max(1, pdfmetrics.stringWidth("abcdefghijklmnopqrstuvwxyz", font, size) / 26)
    chars = max(28, int(width / avg))
    return textwrap.wrap(text, width=chars, break_long_words=True) or [""]


def draw_text(text, font="Inter", size=9.4, leading=12.9, color=CHARCOAL, indent=0, bullet=None):
    global y
    text = clean(text.strip())
    if not text:
        y -= 4
        return
    width = MAX_W - indent
    lines = wrap_lines(text, font, size, width)
    ensure(len(lines) * leading + 4)
    c.setFont(font, size)
    c.setFillColor(color)
    first = True
    for line in lines:
        prefix = bullet if first and bullet else ""
        c.drawString(LEFT + indent, y, prefix + line)
        y -= leading
        first = False
    y -= 1


def draw_h1(text):
    global y
    ensure(35)
    y -= 5
    c.setFont("Playfair-Bold", 20)
    c.setFillColor(NAVY)
    c.drawString(LEFT, y, clean(text))
    y -= 8
    c.setStrokeColor(LINE)
    c.line(LEFT, y, PAGE_W - RIGHT, y)
    y -= 10


def draw_h2(text):
    global y
    ensure(24)
    y -= 3
    c.setFont("Inter-Medium", 12)
    c.setFillColor(SAGE)
    c.drawString(LEFT, y, clean(text))
    y -= 14


def draw_code(lines):
    global y
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(clean(line), width=82, break_long_words=True, replace_whitespace=False) or [""])
    while wrapped:
        ensure(24)
        capacity = max(1, int((y - BOTTOM - 12) / 10))
        chunk = wrapped[:capacity]
        wrapped = wrapped[capacity:]
        height = len(chunk) * 10 + 8
        c.setFillColor(CODE_BG)
        c.rect(LEFT, y - height + 3, MAX_W, height, stroke=0, fill=1)
        c.setFont("Inter", 7.8)
        c.setFillColor(CHARCOAL)
        yy = y - 9
        for line in chunk:
            c.drawString(LEFT + 4, yy, line)
            yy -= 10
        y -= height + 5


cover()
new_page()

in_code = False
code_lines = []
for raw_line in SOURCE.read_text(encoding="utf-8").splitlines():
    line = raw_line.rstrip()
    if line.startswith("# BridgeWorks Business Operating SOP"):
        continue
    if line.startswith("```"):
        if in_code:
            draw_code(code_lines)
            code_lines = []
            in_code = False
        else:
            in_code = True
        continue
    if in_code:
        code_lines.append(line)
        continue
    if not line.strip():
        y -= 3
        continue
    if line.startswith("## "):
        draw_h1(line[3:])
    elif line.startswith("### "):
        draw_h2(line[4:])
    elif re.match(r"^\d+\.\s+", line):
        draw_text(line, indent=6 * mm)
    elif line.startswith("- "):
        draw_text(line[2:], indent=6 * mm, bullet="- ")
    elif line.startswith("|"):
        continue
    elif line.startswith(("Version:", "Owner:", "Last updated:", "Applies to:")):
        draw_text(line, size=8.2, leading=11, color=MUTED)
    else:
        draw_text(line)

c.save()
print(OUTPUT)
