"""Generate revised CEEFM payment plan PDF - Digital Growth only (no brand visuals)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# Brand colors
NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
WHITE = HexColor("#FFFFFF")

W, H = A4
OUTPUT = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\CEEFM_Installment_Payment_Plan_v2.pdf"
HAS_LOGO = False


def bg(c):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def accent(c):
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)


def footer(c):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawCentredString(W / 2, 22, "BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency  |  Budapest, Hungary")


def section(c, y, text):
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, text)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(40, y - 5, W - 40, y - 5)
    return y - 28


def table_row(c, y, cols, widths, bold=False, bg_color=None, text_color=None):
    """Draw a table row. cols = list of strings, widths = list of col widths."""
    row_h = 28
    x = 40
    if bg_color:
        c.setFillColor(bg_color)
        c.rect(x, y - row_h + 8, sum(widths), row_h, fill=1, stroke=0)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, 10)
    color = text_color or CHARCOAL
    c.setFillColor(color)
    for i, col in enumerate(cols):
        if i == len(cols) - 1:
            # Right-align the last column (amount)
            c.drawRightString(x + widths[i], y, col)
        else:
            c.drawString(x + 8, y, col)
        x += widths[i]
    return y - row_h


def build():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("CEEFM Kft - Revised Installment Payment Plan")
    c.setAuthor("Emmanuel Ehigbai / BridgeWorks")

    # ---- SINGLE PAGE ----
    bg(c)
    accent(c)

    # Navy header band
    band_h = H * 0.18
    band_y = H - band_h
    c.setFillColor(NAVY)
    c.rect(0, band_y, W, band_h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, band_y, W, band_y)

    # Logo text fallback
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W - 30, H - 30, "B R I D G E W O R K S")

    # Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, H - 55, "Installment Payment Plan")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawString(40, H - 75, "CEEFM Kft  |  Digital Growth Strategy & Execution")
    c.setFillColor(HexColor("#AAAAAA"))
    c.setFont("Helvetica", 9)
    c.drawString(40, H - 92, "Ref: CEEFM-PAY-003  |  Issued: 10 April 2026  |  Replaces: CEEFM-PAY-002")

    # Prepared for / by
    y = band_y - 30
    box_w = (W - 80 - 20) / 2

    # Left box
    c.setFillColor(WHITE)
    c.roundRect(40, y - 65, box_w, 70, 4, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#E2DDD5"))
    c.setLineWidth(0.5)
    c.roundRect(40, y - 65, box_w, 70, 4, fill=0, stroke=1)
    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(52, y - 2, "PREPARED FOR")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(52, y - 18, "Victor")
    c.setFont("Helvetica", 10)
    c.drawString(52, y - 33, "CEEFM Kft")
    c.setFillColor(WARM_GRAY)
    c.drawString(52, y - 48, "Budapest, Hungary")

    # Right box
    rx = 40 + box_w + 20
    c.setFillColor(WHITE)
    c.roundRect(rx, y - 65, box_w, 70, 4, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#E2DDD5"))
    c.roundRect(rx, y - 65, box_w, 70, 4, fill=0, stroke=1)
    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(rx + 12, y - 2, "PREPARED BY")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(rx + 12, y - 18, "Emmanuel Ehigbai")
    c.setFont("Helvetica", 10)
    c.drawString(rx + 12, y - 33, "BridgeWorks")
    c.setFillColor(WARM_GRAY)
    c.drawString(rx + 12, y - 48, "Budapest, Hungary")

    y = y - 95

    # Engagement Summary
    y = section(c, y, "Engagement Summary")
    col_w = [W - 80 - 120, 120]

    y = table_row(c, y, ["Engagement", "Fee"], col_w, bold=True, bg_color=GOLD, text_color=WHITE)
    y = table_row(c, y, ["Digital Growth Strategy & Execution (Monthly Retainer)", "\u20ac2,650"], col_w)

    # Total row
    y = table_row(c, y, ["Total", "\u20ac2,650"], col_w, bold=True, bg_color=HexColor("#F0EDE6"))

    y -= 8
    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(40, y, "* Brand Visual Identity Package removed per client request (10 April 2026).")
    y -= 25

    # Payment Schedule
    y = section(c, y, "Payment Schedule")
    sched_w = [30, 90, 260, 80]
    y = table_row(c, y, ["#", "Date", "Description", "Amount"], sched_w, bold=True, bg_color=GOLD, text_color=WHITE)

    schedule = [
        ("1", "15 April 2026", "Setup fee", "\u20ac735"),
        ("2", "30 April 2026", "Remaining setup balance", "\u20ac315"),
        ("3", "31 May 2026", "Monthly retainer", "\u20ac400"),
        ("4", "30 June 2026", "Monthly retainer", "\u20ac400"),
        ("5", "31 July 2026", "Monthly retainer", "\u20ac400"),
        ("6", "31 August 2026", "Monthly retainer", "\u20ac400"),
    ]

    for i, (num, date, desc, amt) in enumerate(schedule):
        row_bg = HexColor("#F0EDE6") if i % 2 == 1 else None
        y = table_row(c, y, [num, date, desc, amt], sched_w, bg_color=row_bg)

    # Total row
    y = table_row(c, y, ["", "", "Total", "\u20ac2,650"], sched_w, bold=True, bg_color=HexColor("#F0EDE6"))

    y -= 20

    # Signatures
    y = section(c, y, "Acknowledgement & Signatures")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10)
    c.drawString(40, y, "By signing below, both parties agree to the installment schedule outlined above.")
    y -= 40

    # Signature lines
    line_w = 200
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.5)
    c.line(40, y, 40 + line_w, y)
    c.line(W - 40 - line_w, y, W - 40, y)

    y -= 14
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(CHARCOAL)
    c.drawString(40, y, "Victor \u2014 CEEFM Kft")
    c.drawString(W - 40 - line_w, y, "Emmanuel Ehigbai \u2014 BridgeWorks")

    y -= 16
    c.setFont("Helvetica", 9)
    c.setFillColor(WARM_GRAY)
    c.drawString(40, y, "Date: ____________________")
    c.drawString(W - 40 - line_w, y, "Date: ____________________")

    footer(c)
    c.showPage()
    c.save()
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    build()
