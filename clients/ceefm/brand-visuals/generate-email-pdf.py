"""Generate branded BridgeWorks PDF proposal for CEE FM brand visual package."""
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
OUTPUT = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\brand-visuals\CEE-FM-Brand-Visual-Package-Proposal.pdf"
LOGO_DARK = r"C:\Users\ELITEX21012G2\bridgeworks-agency\public\logos\bridgeworks-logo-primary-dark-800px.png"
LOGO_LIGHT = r"C:\Users\ELITEX21012G2\bridgeworks-agency\public\logos\bridgeworks-logo-primary-light-800px.png"


def bg(c):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def accent(c):
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)


def footer(c, n):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawCentredString(W / 2, 22, "BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency")
    c.drawRightString(W - 30, 22, str(n))


def section(c, y, text):
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, text)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(40, y - 4, 40 + c.stringWidth(text, "Helvetica-Bold", 13), y - 4)
    return y - 22


def body(c, y, text, bold=False):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, 10)
    c.setFillColor(CHARCOAL)
    # Word wrap at ~500pt width
    words = text.split()
    line = ""
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, font, 10) > 500:
            c.drawString(40, y, line)
            y -= 15
            line = word
        else:
            line = test
    if line:
        c.drawString(40, y, line)
        y -= 15
    return y


def bullet(c, y, text):
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(45, y, ">")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10)
    # Word wrap bullets at ~485pt
    words = text.split()
    line = ""
    first = True
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, "Helvetica", 10) > 485:
            x = 60 if first else 60
            c.drawString(x, y, line)
            y -= 15
            line = word
            first = False
        else:
            line = test
    if line:
        c.drawString(60, y, line)
        y -= 15
    return y


def build():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("CEE FM Brand Visual Package Proposal")
    c.setAuthor("Emmanuel Ehigbai / BridgeWorks")

    # ---- PAGE 1: COVER ----
    bg(c)
    accent(c)

    # Navy header band (top 32%)
    band_h = H * 0.32
    band_y = H - band_h
    c.setFillColor(NAVY)
    c.rect(0, band_y, W, band_h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, band_y, W, band_y)

    # BridgeWorks logo in navy band (top-right)
    logo_w = 150
    logo_h = 38  # approximate aspect ratio of the logo
    c.drawImage(LOGO_DARK, W - logo_w - 30, H - 55, width=logo_w, height=logo_h, mask="auto")

    # Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(40, H - 85, "Brand Visual Package")
    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, H - 120, "Proposal")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 13)
    c.drawString(40, H - 155, "Powered by BridgeWorks")

    # Client info
    y = band_y - 60
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Prepared for:")
    y -= 22
    c.setFont("Helvetica", 12)
    c.drawString(40, y, "CEE FM Kft")
    y -= 18
    c.setFillColor(WARM_GRAY)
    c.drawString(40, y, "Budapest, Hungary")
    y -= 18
    c.drawString(40, y, "April 2026")

    y -= 45
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "From:")
    y -= 22
    c.setFont("Helvetica", 12)
    c.drawString(40, y, "Emmanuel Ehigbai")
    y -= 18
    c.setFillColor(WARM_GRAY)
    c.drawString(40, y, "BridgeWorks")
    y -= 18
    c.drawString(40, y, "office@bridgeworks.agency")

    footer(c, 1)
    c.showPage()

    # ---- PAGE 2: DELIVERABLES 1-4 ----
    bg(c)
    accent(c)
    c.drawImage(LOGO_LIGHT, W - 150 - 30, H - 45, width=150, height=38, mask="auto")
    y = H - 50

    y = section(c, y, "What You Get")
    y -= 5
    y = body(c, y, "This package gives CEE FM a complete, professional visual identity. Every asset you need for digital, print, and social media.")
    y -= 10

    y = section(c, y, "1. Brand Guidelines Document")
    y = bullet(c, y, "Logo usage rules (clear space, minimum size, do/don't examples)")
    y = bullet(c, y, "Color palette with hex, RGB, CMYK values")
    y = bullet(c, y, "Typography system (primary + secondary fonts, hierarchy)")
    y = bullet(c, y, "Photography direction and visual tone of voice")
    y = bullet(c, y, "Co-branding rules for partner materials")
    y -= 8

    y = section(c, y, "2. Logo Package")
    y = bullet(c, y, "Full color, white, black, single-color versions")
    y = bullet(c, y, "Icon/mark only for favicons and profile photos")
    y = bullet(c, y, "Horizontal and stacked lockups")
    y = bullet(c, y, "Formats: SVG, PNG (transparent), PDF, EPS")
    y = bullet(c, y, "Optimized for print, web, social media, favicon")
    y -= 8

    y = section(c, y, "3. Social Media Kit")
    y = bullet(c, y, "LinkedIn banner + post templates (5 layouts)")
    y = bullet(c, y, "Instagram post and story templates")
    y = bullet(c, y, "Quote/stat graphic template")
    y = bullet(c, y, "Team spotlight template")
    y = bullet(c, y, "Before/after project showcase template")
    y -= 8

    y = section(c, y, "4. Business Collateral")
    y = bullet(c, y, "Business card (front + back)")
    y = bullet(c, y, "Email signature (HTML)")
    y = bullet(c, y, "Letterhead + invoice template")
    y = bullet(c, y, "Proposal cover page")
    y = bullet(c, y, "PowerPoint deck template (10-15 slides)")

    footer(c, 2)
    c.showPage()

    # ---- PAGE 3: DELIVERABLES 5-6 + TIMELINE + INVESTMENT ----
    bg(c)
    accent(c)
    c.drawImage(LOGO_LIGHT, W - 150 - 30, H - 45, width=150, height=38, mask="auto")
    y = H - 50

    y = section(c, y, "5. Digital Assets")
    y = bullet(c, y, "Website hero banners (desktop + mobile)")
    y = bullet(c, y, "Service page headers for all 6 services")
    y = bullet(c, y, "Open Graph image for link previews")
    y = bullet(c, y, "Email newsletter header + blog featured image template")
    y = bullet(c, y, "Favicon + PWA icon set")
    y -= 8

    y = section(c, y, "6. Print-Ready Assets")
    y = bullet(c, y, "Company profile one-pager (A4, double-sided)")
    y = bullet(c, y, "Service brochure template")
    y = bullet(c, y, "Vehicle/uniform branding mockup")
    y = bullet(c, y, "Site signage template")
    y = bullet(c, y, "Staff ID badge template")
    y -= 5
    y = body(c, y, "All assets bilingual (English + Hungarian) where applicable. Delivered in editable formats plus final exports.")
    y -= 15

    # Timeline
    y = section(c, y, "Timeline: 3 Weeks from Approval")
    y -= 3
    rows = [
        ("Week 1", "Logo package + brand guidelines draft"),
        ("Week 2", "Social media kit + digital assets + business collateral"),
        ("Week 3", "Print assets + final brand guidelines PDF + full handover"),
    ]
    for week, desc in rows:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(55, y, week)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10)
        c.drawString(130, y, desc)
        y -= 18
    y -= 15

    # Investment box
    y = section(c, y, "Investment")
    y -= 8
    box_h = 55
    box_y = y - box_h + 5
    c.setFillColor(NAVY)
    c.roundRect(40, box_y, W - 80, box_h, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, box_y + 28, "250,000 HUF + VAT")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, box_y + 10, "Complete brand visual package")
    y = box_y - 18

    y = body(c, y, "Because we already work together, this is offered at a significant discount.")
    y = body(c, y, "Standard rate for this scope: 450,000 HUF.")
    y = body(c, y, "Budapest agencies typically charge 500,000 to 1,200,000 HUF for comparable work.")
    y -= 3
    y = body(c, y, "This covers the complete package above. No recurring fees. All files are yours to keep.")
    y -= 15

    # Next steps
    y = section(c, y, "Next Steps")
    y -= 3
    y = bullet(c, y, "Confirm you would like to proceed")
    y = bullet(c, y, "We begin within the same week")
    y = bullet(c, y, "Full handover in 3 weeks")
    y -= 20

    # Closing
    y = body(c, y, "If you have any questions, I am happy to discuss.")
    y -= 10
    y = body(c, y, "Best,", bold=True)
    y = body(c, y, "Emmanuel Ehigbai")
    y = body(c, y, "BridgeWorks")
    y = body(c, y, "office@bridgeworks.agency")

    footer(c, 3)
    c.showPage()
    c.save()
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    build()
