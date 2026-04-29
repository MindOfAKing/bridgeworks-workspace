"""Generate the Oliviks proposal PDFs (full + summary) with BridgeWorks branding."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image as RLImage,
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
SAGE = HexColor("#4A6741")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
WHITE = HexColor("#FFFFFF")

W, H = A4

CLIENT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\oliviks"
LOGO_DARK = r"C:\Users\ELITEX21012G2\brand-assets\bridgeworks\logos\bridgeworks-logo-primary-dark-800px.png"
LOGO_LIGHT = r"C:\Users\ELITEX21012G2\brand-assets\bridgeworks\logos\bridgeworks-logo-primary-light-800px.png"

# Fail loudly if logos are missing rather than producing an unbranded PDF.
for _p in (LOGO_DARK, LOGO_LIGHT):
    if not os.path.exists(_p):
        raise FileNotFoundError(f"Logo not found: {_p}")

# Styles
def make_styles():
    s = {}
    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=18, leading=22,
        textColor=NAVY, spaceBefore=18, spaceAfter=8,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13, leading=16,
        textColor=NAVY, spaceBefore=14, spaceAfter=6,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=NAVY, spaceBefore=10, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=CHARCOAL, spaceAfter=5,
    )
    s["body_bold"] = ParagraphStyle(
        "body_bold", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        textColor=CHARCOAL, spaceAfter=5,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=CHARCOAL, leftIndent=14, bulletIndent=2, spaceAfter=3,
    )
    s["small"] = ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8, leading=11,
        textColor=WARM_GRAY, spaceAfter=4,
    )
    s["small_italic"] = ParagraphStyle(
        "small_italic", fontName="Helvetica-Oblique", fontSize=8, leading=11,
        textColor=WARM_GRAY, spaceAfter=4,
    )
    s["callout"] = ParagraphStyle(
        "callout", fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=NAVY, leftIndent=10, rightIndent=10, spaceBefore=8, spaceAfter=8,
        backColor=HexColor("#FAF5E8"), borderColor=GOLD, borderWidth=0,
        borderPadding=8,
    )
    s["table_head"] = ParagraphStyle(
        "table_head", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=WHITE,
    )
    s["table_cell"] = ParagraphStyle(
        "table_cell", fontName="Helvetica", fontSize=9, leading=12,
        textColor=CHARCOAL,
    )
    s["table_cell_bold"] = ParagraphStyle(
        "table_cell_bold", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=NAVY,
    )
    return s

STYLES = make_styles()


def _draw_branded_chrome(c, page_num, doc_title, show_logo=True):
    """Background, accent bar, top logo strip, footer. Drawn on every body page."""
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)
    if show_logo:
        # Logo source aspect 800:300 (~2.67:1). Keep that ratio to avoid stretching.
        c.drawImage(LOGO_LIGHT, W - 130 - 30, H - 53, width=130, height=49, mask="auto")
    # Footer
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawString(40, 22, f"BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency")
    c.drawRightString(W - 30, 22, f"Page {page_num}")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(40, 35, W - 30, 35)


def _on_body_page(c, doc):
    _draw_branded_chrome(c, doc.page, "")


def _on_cover_page(c, doc, title_lines, subtitle, prepared_for_lines, from_lines):
    """Cover page with navy header band, gold accent, logo, title."""
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)

    # Navy header band, top 36% of page
    band_h = H * 0.36
    band_y = H - band_h
    c.setFillColor(NAVY)
    c.rect(0, band_y, W, band_h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, band_y, W, band_y)

    # Logo top right (dark variant on navy band). Source aspect 800:300 (~2.67:1).
    c.drawImage(LOGO_DARK, W - 200 - 30, H - 95, width=200, height=75, mask="auto")

    # Title in band
    y_title = H - 95
    c.setFillColor(WHITE)
    for i, line in enumerate(title_lines):
        size = 28 if i == 0 else 22
        c.setFont("Helvetica-Bold", size)
        c.drawString(40, y_title, line)
        y_title -= size + 6

    # Subtitle in gold
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawString(40, y_title - 4, subtitle)

    # Prepared for / from blocks below band
    y = band_y - 50
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Prepared for:")
    y -= 20
    for line in prepared_for_lines:
        c.setFont("Helvetica", 11)
        c.setFillColor(CHARCOAL if line == prepared_for_lines[0] else WARM_GRAY)
        c.drawString(40, y, line)
        y -= 16

    y -= 22
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "From:")
    y -= 20
    for line in from_lines:
        c.setFont("Helvetica", 11)
        c.setFillColor(CHARCOAL if line == from_lines[0] else WARM_GRAY)
        c.drawString(40, y, line)
        y -= 16

    # Footer on cover
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawString(40, 22, "BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency")
    c.drawRightString(W - 30, 22, "Page 1")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(40, 35, W - 30, 35)


def _styled_table(rows, col_widths, header=True):
    t = Table(rows, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D7D2C7")),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
        ]
    t.setStyle(TableStyle(style))
    return t


def _price_box(amount_eur, label):
    """Big navy price box."""
    rows = [[Paragraph(amount_eur, ParagraphStyle("p", fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, alignment=TA_CENTER, leading=26))],
            [Paragraph(label, ParagraphStyle("p", fontName="Helvetica", fontSize=10, textColor=GOLD, alignment=TA_CENTER, leading=12))]]
    t = Table(rows, colWidths=[W - 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (0, 0), 14),
        ("BOTTOMPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 1), (0, 1), 0),
        ("BOTTOMPADDING", (0, 1), (0, 1), 12),
    ]))
    return t


def _callout(text):
    """Light gold callout box."""
    rows = [[Paragraph(text, ParagraphStyle("p", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14))]]
    t = Table(rows, colWidths=[W - 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FAF5E8")),
        ("LINEBEFORE", (0, 0), (0, 0), 3, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def _section_divider():
    return HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceBefore=10, spaceAfter=10)


def P(text, style="body"):
    return Paragraph(text, STYLES[style])


def build_cover_template(title_lines, subtitle, prepared_for_lines, from_lines):
    def _on_cover(c, doc):
        _on_cover_page(c, doc, title_lines, subtitle, prepared_for_lines, from_lines)
    return _on_cover


def build_full_proposal():
    output = os.path.join(CLIENT_DIR, "PROPOSAL-OLIVIKS-2026-04-28.pdf")

    cover_callback = build_cover_template(
        title_lines=["Digital Growth", "Proposal"],
        subtitle="Powered by BridgeWorks",
        prepared_for_lines=[
            "Oliviks Nigerian Kitchen",
            "Rákóczi tér 9, 1084 Budapest",
            "Hungary",
            "28 April 2026",
        ],
        from_lines=[
            "Emmanuel Ehigbai",
            "Founder, BridgeWorks",
            "office@bridgeworks.agency",
        ],
    )

    doc = BaseDocTemplate(
        output, pagesize=A4, leftMargin=40, rightMargin=30, topMargin=50, bottomMargin=42,
        title="Digital Growth Proposal — Oliviks Nigerian Kitchen",
        author="Emmanuel Ehigbai / BridgeWorks",
    )
    cover_frame = Frame(40, 42, W - 70, H - 84, id="cover", showBoundary=0)
    body_frame = Frame(40, 42, W - 70, H - 92, id="body", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_callback),
        PageTemplate(id="Body", frames=[body_frame], onPage=_on_body_page),
    ])

    s = []
    # Cover content is drawn entirely on the canvas via onPage; just push a page break.
    s.append(Spacer(1, 1))  # forces cover frame to render
    s.append(PageBreak())

    # Switch to body template
    from reportlab.platypus import NextPageTemplate
    s.insert(1, NextPageTemplate("Body"))

    # ---- Executive Summary ----
    s.append(P("Executive Summary", "h1"))
    s.append(P("You have something rare. A 4.8-star rating from over 160 reviews. Coverage in Origo, We Love Budapest, and WMN. Listings on both Wolt and Foodora. A near-monopoly on authentic Nigerian food in Budapest."))
    s.append(P("The website does not show any of this."))
    s.append(P("The marketing audit we ran on 4 April scored your digital presence at 38 out of 100. The food, the reputation, and the press are working. The site that is supposed to communicate all of it is not."))
    s.append(P("This proposal closes that gap."))
    s.append(P("There are two parts. <b>Part A: Foundation</b> is the work this proposal commits to. It is a one-time rebuild that fixes everything the audit flagged as a Quick Win and Strategic Recommendation on the site, the Google profile, and the retention infrastructure. <b>Part B: Optional Growth Retainer</b> is a recommended next step. It runs the systems Part A builds and executes the audit's longer-term recommendations every month. You can decide on Part B at any time."))
    s.append(P("Optional add-ons sit at the bottom. They are useful but not required."))
    s.append(P("The full investment for Part A is <b>272,611 HUF</b>. The retainer, if you choose it, is <b>218,088 HUF per month</b> with a 3-month minimum. All figures are in HUF. Invoices issued via szamlazz.hu under Hungarian VAT exemption (Áfa törvény 188. §, alanyi adómentes)."))
    s.append(_section_divider())

    # ---- Audit Recap ----
    s.append(P("What the Audit Found", "h1"))
    s.append(P("The 4 April audit reviewed six categories. The summary:"))
    audit_rows = [
        [P("Category", "table_head"), P("Score", "table_head"), P("What it means", "table_head")],
        [P("Content & Messaging", "table_cell"), P("32/100", "table_cell"), P("Homepage fails the 5-second test. Health language clashes with Nigerian-kitchen identity.", "table_cell")],
        [P("Conversion Optimization", "table_cell"), P("35/100", "table_cell"), P("Self-pickup friction, duplicate pages, empty Shop page, no clear pricing path.", "table_cell")],
        [P("SEO & Discoverability", "table_cell"), P("38/100", "table_cell"), P("Default WordPress setup. Missing meta descriptions. Duplicate pages. No schema.", "table_cell")],
        [P("Competitive Positioning", "table_cell"), P("52/100", "table_cell"), P("Highest Google rating in segment but confused positioning.", "table_cell")],
        [P("Brand & Trust", "table_cell"), P("42/100", "table_cell"), P("Real-world reputation strong. Website does not surface any of it.", "table_cell")],
        [P("Growth & Strategy", "table_cell"), P("35/100", "table_cell"), P("Smart platform presence. Zero retention system. No content.", "table_cell")],
        [P("<b>Overall</b>", "table_cell_bold"), P("<b>38/100</b>", "table_cell_bold"), P("", "table_cell")],
    ]
    s.append(_styled_table(audit_rows, [120, 50, 305]))
    s.append(Spacer(1, 8))
    s.append(P("Estimated revenue impact if all recommendations are implemented: <b>40 to 60 percent monthly uplift</b>. The Foundation in this proposal addresses every Quick Win and most Strategic Recommendations. The optional Retainer addresses the rest."))
    s.append(PageBreak())

    # ---- Part A: Foundation ----
    s.append(P("Part A: Foundation", "h1"))
    s.append(P("A one-time rebuild. Stands alone. You can stop here if you choose."))
    s.append(_callout("Total: 272,611 HUF (one-time, no recurring fees)"))
    s.append(P("This part has three lines: Website Upgrade, Google Business Profile Optimization, and Email and WhatsApp Infrastructure. Bought together they save 36,348 HUF against the separate price."))

    # A1 Website Upgrade
    s.append(P("A1. Website Upgrade", "h2"))
    s.append(P("<b>Price:</b> 163,566 HUF &nbsp;&nbsp;&nbsp; <b>Timeline:</b> 3 weeks from kickoff"))
    s.append(P("<b>The problem this solves:</b>", "h3"))
    s.append(P("The audit flagged that the homepage fails the 5-second test, the About page leads with health buzzwords instead of the founders' story, the testimonials read as fake, dish descriptions are missing, duplicate pages from a past migration are still live, and the Sample Page from the WordPress install is still public. None of the press coverage or Google reviews show on the site."))
    s.append(P("<b>What we deliver:</b>", "h3"))
    a1_rows = [
        [P("#", "table_head"), P("Deliverable", "table_head")],
        [P("1", "table_cell"), P('Homepage rewritten and rebuilt. Clear hero ("Authentic Nigerian Food. Made Fresh in Budapest. Order for Pickup or Delivery."), 4.8 stars from 160+ reviews displayed above the fold, Wolt and Foodora badges, "As featured in" media bar with Origo, We Love Budapest, and WMN logos.', "table_cell")],
        [P("2", "table_cell"), P("About page rebuilt around Olivia and her husband's story. Founder photos. The journey from Nigeria to Budapest. The gap they spotted. The health and organic message moved to a separate Our Ingredients section so it stops fighting the Nigerian-kitchen identity.", "table_cell")],
        [P("3", "table_cell"), P("Fake testimonials removed. Real Google reviews embedded. Review carousel added to the homepage.", "table_cell")],
        [P("4", "table_cell"), P("Dish descriptions written for all 23 menu products. Two to three sentences per dish, written for Hungarian and expat customers who have never heard of egusi soup or puff puff.", "table_cell")],
        [P("5", "table_cell"), P("Cleanup. /sample-page/ deleted. /cart-2 redirected to /cart. /checkout-2 redirected to /checkout. /my-account-2 redirected to /my-account.", "table_cell")],
        [P("6", "table_cell"), P('Contact page rebuilt. "CHEF HOTLINE" renamed. Google Map embedded. Address marked up in structured data.', "table_cell")],
        [P("7", "table_cell"), P("Empty Shop page issue resolved. Either populated or removed from navigation.", "table_cell")],
        [P("8", "table_cell"), P("Pricing made visible on every menu item.", "table_cell")],
        [P("9", "table_cell"), P("SEO basics. Meta descriptions written for every main page. Open Graph tags set. Alt text on every image. Focus keyword per page.", "table_cell")],
        [P("10", "table_cell"), P("Page speed pass. Image compression. Caching plugin configured. Elementor bloat reduced where possible.", "table_cell")],
        [P("11", "table_cell"), P("Mobile responsive QA across all pages on iOS and Android.", "table_cell")],
        [P("12", "table_cell"), P("Pre-handover backup of the existing site.", "table_cell")],
    ]
    s.append(_styled_table(a1_rows, [25, 450]))
    s.append(Spacer(1, 6))
    s.append(P("<b>What these technical bits mean for you:</b>", "h3"))
    s.append(P("<b>Meta descriptions</b> are the one or two lines of text that show under your business name on Google search results. We rewrite them so people clicking from search arrive ready to order."))
    s.append(P("<b>Open Graph tags</b> control what shows up when oliviks.com gets shared on Facebook, LinkedIn, or WhatsApp. Right now your shared links may look broken or generic. After this work they show your logo, a clear headline, and a real photo."))
    s.append(P("<b>Alt text</b> is a hidden text description on every image. It helps screen readers for visually impaired customers and lets your food photos appear in Google image searches."))
    s.append(P("<b>Page speed and caching</b> make your pages load faster. Slower sites lose mobile customers and rank lower on Google. We tune your site to load fast on a phone."))
    s.append(P("<b>301 redirects</b> automatically forward people who land on old or broken URLs to the right page. So if someone hits /cart-2, they end up on /cart instead of an error."))
    s.append(P("<b>Mobile responsive QA</b> is the manual test of every page on a phone-size screen. Most of your customers order from their phone. We make sure none of them see a broken layout."))
    s.append(Spacer(1, 4))
    s.append(P("<b>What you provide:</b>", "h3"))
    s.append(P("&bull; WordPress admin access &nbsp;&bull; Founder photos (or willingness to take new ones for the About page) &nbsp;&bull; Logo files for Origo, We Love Budapest, WMN, Wolt, Foodora (we source if not provided) &nbsp;&bull; Approval on copy drafts before publishing"))
    s.append(P("<b>Not included:</b>", "h3"))
    s.append(P("&bull; Full theme migration off Elementor (separate project) &nbsp;&bull; E-commerce restructure (changing self-pickup to full delivery) &nbsp;&bull; Full Hungarian translation of every page"))
    s.append(PageBreak())

    # A2 GBP
    s.append(P("A2. Google Business Profile Optimization", "h2"))
    s.append(P("<b>Price:</b> 65,427 HUF &nbsp;&nbsp;&nbsp; <b>Timeline:</b> 2 weeks from kickoff"))
    s.append(P("<b>Already in place (we do not charge for this):</b>", "h3"))
    s.append(P("Profile claimed, address, phone, website link, hours, primary category, one attribute, an order link, and the 4.8 stars from 160+ reviews. We have already verified this on Google Maps."))
    s.append(P("<b>The problem this solves:</b>", "h3"))
    s.append(P("Your profile is live but only partly optimized. Only one category is set. Almost no attributes. The menu is not uploaded inside the profile itself. There is no Q&A populated by you. Wolt currently shows the wrong kitchen address (Bacsó Béla utca 31), which conflicts with your Google profile (Rákóczi tér 9). This conflict tells Google your business location is unreliable, which lowers ranking."))
    s.append(P("<b>What we deliver:</b>", "h3"))
    a2_rows = [
        [P("#", "table_head"), P("Deliverable", "table_head")],
        [P("1", "table_cell"), P("Secondary categories added: Nigerian Restaurant, Caterer, Takeaway, Delivery Restaurant.", "table_cell")],
        [P("2", "table_cell"), P("Full attributes audit and completion: delivery, takeaway, dine-in, vegan options, wheelchair access, Wi-Fi, parking, payment methods, family-friendly, reservations.", "table_cell")],
        [P("3", "table_cell"), P("Business description rewritten in 750 characters, optimized for Budapest Nigerian-food search queries, in English and Hungarian.", "table_cell")],
        [P("4", "table_cell"), P("Menu uploaded directly inside Google Business Profile. All 23 dishes, each with photo, two-to-three-sentence description, and price.", "table_cell")],
        [P("5", "table_cell"), P("Photo audit and upload of up to 50 photos across food, kitchen, team, exterior, interior. Primary photo set.", "table_cell")],
        [P("6", "table_cell"), P('Q&A pre-populated with 8 to 10 owner-answered questions ("Do you deliver?", "Is the food spicy?", "What is jollof rice?", "Do you cater events?", "Where do I park?", "Vegan options?").', "table_cell")],
        [P("7", "table_cell"), P("Four launch posts published. Weekly post template handed over for ongoing use.", "table_cell")],
        [P("8", "table_cell"), P("Review response system. Reply templates for 5-star, 4-star, 3-star, 1-2-star reviews in English and Hungarian. Backfill of unresponded reviews from the existing 160.", "table_cell")],
        [P("9", "table_cell"), P("NAP consistency cleanup across Wolt, Foodora, Facebook, TripAdvisor, and Wanderlog. Every listing updated to match the correct Rákóczi tér 9 address.", "table_cell")],
        [P("10", "table_cell"), P("Website-side schema markup added to oliviks.com. LocalBusiness, Restaurant, and FoodEstablishment markup. Google Map embedded on the contact page.", "table_cell")],
        [P("11", "table_cell"), P("Baseline screenshot of Google Business Profile Insights (calls, direction requests, photo views, search queries) before optimization. Same screenshot 4 weeks later for comparison.", "table_cell")],
        [P("12", "table_cell"), P("One-page handover document: how to add a post, respond to a review, upload a photo.", "table_cell")],
    ]
    s.append(_styled_table(a2_rows, [25, 450]))
    s.append(Spacer(1, 6))
    s.append(P("<b>What these technical bits mean for you:</b>", "h3"))
    s.append(P('<b>Secondary categories</b> are extra labels Google uses to file your business in more search categories. Adding "Nigerian Restaurant", "Caterer", and "Takeaway" means you show up when people search any of those, not just "African restaurant".'))
    s.append(P("<b>Attributes</b> are the checkboxes Google offers for filtering search results: delivery, vegan options, wheelchair access, and so on. Customers filtering by their needs see businesses that have set those attributes. The ones that haven't get skipped."))
    s.append(P("<b>NAP consistency</b> means having the same Name, Address, and Phone across every platform. When Wolt shows one address and Google shows another, Google does not trust the listing. Fixing this is one of the highest-impact local SEO moves."))
    s.append(P('<b>Schema markup (LocalBusiness, Restaurant, FoodEstablishment)</b> is invisible code on your website that tells Google "this is a restaurant, here are the hours, here is the menu". Google then shows rich results (star rating, hours, menu link) directly in search, which increases clicks.'))
    s.append(P("<b>Q&amp;A on Google Business Profile</b> is a public section where anyone can ask a question. If you don't answer, customers do, often wrongly. Pre-loading owner-marked answers means accurate info reaches every potential customer."))
    s.append(P("<b>Google Business Profile Insights</b> is Google's free analytics dashboard for your profile. It shows calls, direction requests, photo views, and search queries. We screenshot it before we start and again 4 weeks later, so you have month-on-month proof in numbers."))
    s.append(_callout("Address confirmation required: by accepting this proposal you confirm that Rákóczi tér 9, 1084 Budapest is the public-facing kitchen address. Wolt and other listings will be updated to match."))
    s.append(P("<b>What you provide:</b>", "h3"))
    s.append(P("&bull; Manager-level access to the Google Business Profile &nbsp;&bull; 30 to 50 photos (or one of the optional photo add-ons below) &nbsp;&bull; Owner approval on description and Q&A drafts before publishing"))
    s.append(P("<b>Not included:</b>", "h3"))
    s.append(P("&bull; Ongoing Google Business Profile management (covered in the optional retainer) &nbsp;&bull; Google Ads setup or ad spend &nbsp;&bull; Guarantee of ranking improvement"))
    s.append(PageBreak())

    # A3 Email + WhatsApp
    s.append(P("A3. Email and WhatsApp Infrastructure", "h2"))
    s.append(P("<b>Price:</b> 79,966 HUF &nbsp;&nbsp;&nbsp; <b>Timeline:</b> 2 weeks from kickoff"))
    s.append(P("<b>The problem this solves:</b>", "h3"))
    s.append(P("The audit flagged retention as your single biggest strategic gap. No email list. No WhatsApp broadcast list. No way to bring a Wolt customer back as a higher-margin direct customer. We build the system here. The optional retainer fills it with content every month."))
    s.append(P("<b>What we deliver:</b>", "h3"))
    a3_rows = [
        [P("#", "table_head"), P("Deliverable", "table_head")],
        [P("1", "table_cell"), P("Email provider account set up (MailerLite or Beehiiv free tier). You own the account.", "table_cell")],
        [P("2", "table_cell"), P('Email capture popup on oliviks.com. First-order incentive of your choice ("Free puff puff with first order" or similar).', "table_cell")],
        [P("3", "table_cell"), P("Welcome sequence: 3 emails. Email 1: thank you and discount code. Email 2: founders' story. Email 3: invitation to weekly specials.", "table_cell")],
        [P("4", "table_cell"), P("Weekly specials email template, designed in English and Hungarian, ready to fill in each week.", "table_cell")],
        [P("5", "table_cell"), P("Order receipt email rebranded. Replaces the default WooCommerce email with a branded version.", "table_cell")],
        [P("6", "table_cell"), P("GDPR compliance: consent checkbox on capture form, double opt-in flow, unsubscribe link, privacy policy update.", "table_cell")],
        [P("7", "table_cell"), P("WhatsApp broadcast list set up as a parallel retention channel. Business WhatsApp number, broadcast list created, opt-in flow via website form and QR code at the pickup counter.", "table_cell")],
        [P("8", "table_cell"), P("WooCommerce integration. Customers automatically added to the email list with double opt-in after their first order.", "table_cell")],
        [P("9", "table_cell"), P("One-page handover document: how to send a weekly specials email, how to send a WhatsApp broadcast, how to add a subscriber.", "table_cell")],
    ]
    s.append(_styled_table(a3_rows, [25, 450]))
    s.append(Spacer(1, 6))
    s.append(P("<b>What these technical bits mean for you:</b>", "h3"))
    s.append(P("<b>Welcome sequence</b> is the set of automated emails that go out the day after someone signs up, then a few days later, then a week later. It turns a one-time visitor into a three-touchpoint relationship without any manual work from you."))
    s.append(P("<b>Double opt-in</b> means a new subscriber clicks a link to confirm their email before being added to your list. GDPR requires this in Hungary. It also keeps your list clean (no fake addresses) and improves email delivery rates."))
    s.append(P("<b>WooCommerce integration</b> is the link between your shop and your email list. When someone places an order, they get added to your list automatically (after confirming). Every paying customer becomes a marketing contact for free."))
    s.append(P("<b>WhatsApp broadcast list</b> is a feature in WhatsApp Business that lets you message many customers at once, with each person receiving it as a private one-to-one message (not a group chat). Open rates on WhatsApp are typically 70 to 90 percent versus 20 to 30 percent on email. For weekly specials, this is the most effective channel."))
    s.append(P("<b>What you provide:</b>", "h3"))
    s.append(P("&bull; A business WhatsApp number (or willingness to set one up) &nbsp;&bull; Privacy policy approval &nbsp;&bull; One first-subscriber incentive offer you are willing to give"))
    s.append(P("<b>Not included:</b>", "h3"))
    s.append(P("&bull; Email provider monthly fees if you exceed the free tier &nbsp;&bull; Ongoing email writing (in optional retainer) &nbsp;&bull; WhatsApp Business API integration"))
    s.append(_section_divider())

    # Foundation summary table
    s.append(P("Foundation Investment", "h2"))
    fnd_rows = [
        [P("Line", "table_head"), P("Price", "table_head")],
        [P("Website Upgrade", "table_cell"), P("163,566 HUF", "table_cell")],
        [P("Google Business Profile Optimization", "table_cell"), P("65,427 HUF", "table_cell")],
        [P("Email and WhatsApp Infrastructure", "table_cell"), P("79,966 HUF", "table_cell")],
        [P("Bundle saving (3 lines together)", "table_cell"), P("-36,348 HUF", "table_cell")],
        [P("<b>Foundation Total</b>", "table_cell_bold"), P("<b>272,611 HUF</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(fnd_rows, [375, 100]))
    s.append(PageBreak())

    # ---- Part B: Optional Retainer ----
    s.append(P("Part B: Optional Growth Retainer", "h1"))
    s.append(P("This is a recommended next step. It is not required. The Foundation above stands alone."))
    s.append(_callout("218,088 HUF per month. 3-month minimum (654,264 HUF total). Month-to-month after month 3 at the same rate."))
    s.append(P("<b>The problem this solves:</b>", "h3"))
    s.append(P("Building the systems is one thing. Running them every week is another. The retainer operates the email list, the WhatsApp broadcasts, the Google Business Profile maintenance, the Wolt and Foodora optimization, and the blog. It also executes the longer-term recommendations from the audit (the Nigerian Food in Budapest blog, TikTok content, the Google review generation campaign)."))
    s.append(P("You can decide on the retainer when you accept this proposal, after Foundation handover, or never. Foundation is the commitment. Retainer is the option."))

    s.append(P("Audit recommendations addressed by the retainer", "h3"))
    audit_map_rows = [
        [P("Audit recommendation", "table_head"), P("Where it lives in the retainer", "table_head")],
        [P("Strategic Rec 2 (run the retention system)", "table_cell"), P("Weekly WhatsApp specials, monthly email newsletter", "table_cell")],
        [P("Strategic Rec 3 (Nigerian Food in Budapest blog)", "table_cell"), P("One blog post per week", "table_cell")],
        [P("Strategic Rec 4 (Wolt and Foodora ongoing)", "table_cell"), P("Monthly listing audit", "table_cell")],
        [P("Long-Term 1 (Activate TikTok content)", "table_cell"), P("Social captions for Oliviks-shot content", "table_cell")],
        [P("Long-Term 3 (Google review campaign to 300+)", "table_cell"), P("Monthly WhatsApp follow-up batch with review link", "table_cell")],
        [P("Long-Term 4 (Hungarian mainstream audience)", "table_cell"), P("Blog posts in HU and social cross-posts", "table_cell")],
    ]
    s.append(_styled_table(audit_map_rows, [240, 235]))
    s.append(Spacer(1, 8))

    s.append(P("Monthly deliverables", "h3"))
    rt_rows = [
        [P("#", "table_head"), P("Deliverable", "table_head")],
        [P("1", "table_cell"), P("One blog post per week (4 per month). 400 to 600 words each. Targeting Budapest Nigerian-food and African-catering search queries. Published with images, schema markup, and internal links.", "table_cell")],
        [P("2", "table_cell"), P("Weekly WhatsApp specials broadcast. Drafted and sent on your behalf or scheduled for you to send.", "table_cell")],
        [P("3", "table_cell"), P("Monthly email newsletter to the subscriber list. Weekly specials roundup, new menu items, founder note, links to recent blog posts.", "table_cell")],
        [P("4", "table_cell"), P("Wolt and Foodora monthly listing audit. Response-time check, menu refresh, photo refresh, description updates, suggestions for promotional placement.", "table_cell")],
        [P("5", "table_cell"), P("Google Business Profile monthly maintenance. 4 posts published, new photos uploaded when you supply them, Q&A monitored and answered, every new review responded to within 48 hours.", "table_cell")],
        [P("6", "table_cell"), P("Google review generation campaign. Monthly batch of WhatsApp follow-up messages to recent customers requesting reviews, with a direct review link.", "table_cell")],
        [P("7", "table_cell"), P("Loyalty card administration. Paper-based punch-card system rolled out in month 1, manually tracked via WhatsApp. Digital version added in month 2 or 3 if volume justifies.", "table_cell")],
        [P("8", "table_cell"), P("Social captions written for your content. 3 per week for Instagram and TikTok. You provide raw photos and short video.", "table_cell")],
        [P("9", "table_cell"), P("Monthly performance report. One page covering Google Business Profile insights, website analytics, email opens, WhatsApp engagement, blog traffic, and review-count delta.", "table_cell")],
        [P("10", "table_cell"), P("30-minute monthly review call with Olivia.", "table_cell")],
    ]
    s.append(_styled_table(rt_rows, [25, 450]))
    s.append(Spacer(1, 6))
    s.append(P("<b>What you provide each month:</b>", "h3"))
    s.append(P("&bull; Five-minute weekly check-in (Slack, WhatsApp, or email) on blog topic and weekly specials &nbsp;&bull; Photo and video raw content from the kitchen for social use &nbsp;&bull; Anonymized contact list of recent customers for the review generation flow"))
    s.append(P("<b>Not included in the retainer:</b>", "h3"))
    s.append(P("&bull; Paid ad spend or paid campaign management &nbsp;&bull; New website pages beyond minor edits (catering page is an optional add-on) &nbsp;&bull; Photo or video production &nbsp;&bull; Translation of the full website &nbsp;&bull; TikTok and Reel video editing"))
    s.append(PageBreak())

    # ---- Optional Add-Ons ----
    s.append(P("Optional Add-Ons", "h1"))
    s.append(P("Add only if desired. Quoted separately. Both addressable later if you change your mind."))

    s.append(P("Photo Shoot", "h2"))
    s.append(P("<b>Price:</b> 90,870 HUF &nbsp;&nbsp;&nbsp; <b>Timeline:</b> Half-day on-site, edited photos delivered within 1 week"))
    s.append(P("Half-day shoot at the Rákóczi tér 9 kitchen. 10 to 12 dish photos, kitchen interior, exterior, team, behind-the-scenes. Photos edited and delivered ready to upload to Google Business Profile, Wolt, Foodora, and the website. Full ownership transferred. No licensing fees."))
    s.append(P("<b>Recommended if</b> you do not already have 30 to 50 production-quality photos available."))

    s.append(P("Catering Page", "h2"))
    s.append(P("<b>Price:</b> 79,966 HUF &nbsp;&nbsp;&nbsp; <b>Timeline:</b> 1 week"))
    s.append(P("Dedicated /catering page on oliviks.com, in English and Hungarian. Catering packages copy (corporate events, university gatherings, African community celebrations). Sample menu with per-head pricing tiers. Separate inquiry form (event size, date, location, dietary needs, budget). Schema markup for the page. Three photos placed. Two LinkedIn and Instagram caption templates announcing the catering service."))
    s.append(P("Addresses Long-Term Initiative 2 from the audit (build catering as a revenue line)."))
    s.append(P("<b>You provide:</b> catering pricing decisions, sample menu sign-off, three photos."))
    s.append(_section_divider())

    # ---- Investment Summary ----
    s.append(P("Investment Summary", "h1"))
    s.append(P("All prices in HUF. All invoices issued in HUF via szamlazz.hu under Hungarian VAT exemption (Áfa törvény 188. §, alanyi adómentes)."))
    inv_rows = [
        [P("Scenario", "table_head"), P("Total (HUF)", "table_head")],
        [P("Foundation only", "table_cell"), P("272,611", "table_cell")],
        [P("Foundation + Retainer (3 months)", "table_cell"), P("926,875", "table_cell")],
        [P("Foundation + Retainer + Photo Shoot", "table_cell"), P("1,017,745", "table_cell")],
        [P("Foundation + Retainer + Photo Shoot + Catering Page", "table_cell"), P("1,097,711", "table_cell")],
    ]
    s.append(_styled_table(inv_rows, [375, 100]))
    s.append(Spacer(1, 12))

    # Payment structure
    s.append(P("Payment Structure", "h2"))
    s.append(P("If Foundation only", "h3"))
    pay1 = [
        [P("When", "table_head"), P("Amount (HUF)", "table_head")],
        [P("On contract signing", "table_cell"), P("136,306 (50% setup)", "table_cell")],
        [P("On website handover (end of week 3)", "table_cell"), P("136,305 (50% setup balance)", "table_cell")],
        [P("<b>Total</b>", "table_cell_bold"), P("<b>272,611</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(pay1, [310, 165]))
    s.append(Spacer(1, 8))
    s.append(P("If Foundation + Retainer", "h3"))
    pay2 = [
        [P("When", "table_head"), P("Amount (HUF)", "table_head")],
        [P("On contract signing", "table_cell"), P("354,394 (50% setup + month 1)", "table_cell")],
        [P("On website handover (end of week 3)", "table_cell"), P("136,305 (50% setup balance)", "table_cell")],
        [P("Month 2, 1st of month", "table_cell"), P("218,088", "table_cell")],
        [P("Month 3, 1st of month", "table_cell"), P("218,088", "table_cell")],
        [P("<b>Total</b>", "table_cell_bold"), P("<b>926,875</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(pay2, [310, 165]))
    s.append(Spacer(1, 6))
    s.append(P("Add-ons invoiced separately on agreement. Each invoice is issued in HUF via szamlazz.hu.", "small"))
    s.append(PageBreak())

    # ---- Why BridgeWorks ----
    s.append(P("Why BridgeWorks", "h1"))
    s.append(P("BridgeWorks is an AI-powered digital growth studio based in Budapest, working with small and medium businesses across Central Europe and Nigeria. We build and run the digital systems that turn real-world reputation into online revenue."))
    s.append(P("Current proof of work: CEEFM Kft, a Budapest facility management company, where we are running a 16-week digital growth engagement (currently in week 5 of 16, with measurable AI visibility improvements logged from 16/100 to 82/100 over 4 weeks)."))
    s.append(P("Founder: Emmanuel Ehigbai. MSc International Economy and Business with Distinction, Budapest Business University 2025. Stipendium Hungaricum scholar. Based in Budapest."))
    s.append(_section_divider())

    # ---- Acceptance ----
    s.append(P("Acceptance", "h1"))
    s.append(P("By signing below, you accept this proposal as written and authorize BridgeWorks to begin work."))
    s.append(P("Address confirmation:", "h3"))
    s.append(P("[ ] I confirm Rákóczi tér 9, 1084 Budapest is the public-facing kitchen address. Wolt and other listings will be updated to match.", "body_bold"))
    s.append(Spacer(1, 6))
    s.append(P("Engagement scope (tick one):", "h3"))
    s.append(P("[ ] Foundation only (272,611 HUF)", "body_bold"))
    s.append(P("[ ] Foundation + Retainer 3 months (926,875 HUF)", "body_bold"))
    s.append(Spacer(1, 6))
    s.append(P("Optional add-ons (tick any):", "h3"))
    s.append(P("[ ] Photo Shoot (+90,870 HUF)", "body_bold"))
    s.append(P("[ ] Catering Page (+79,966 HUF)", "body_bold"))
    s.append(Spacer(1, 18))

    sig_rows = [
        [P("<b>For Oliviks Nigerian Kitchen</b>", "body_bold"), P("<b>For BridgeWorks</b>", "body_bold")],
        [P("Name: ____________________________", "body"), P("Emmanuel Ehigbai", "body")],
        [P("Title: _____________________________", "body"), P("Founder, BridgeWorks", "body")],
        [P("Date: _____________________________", "body"), P("office@bridgeworks.agency", "body")],
        [P("Signature: _________________________", "body"), P("Date: 28 April 2026", "body")],
    ]
    sig_table = Table(sig_rows, colWidths=[237, 238])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(sig_table)
    s.append(Spacer(1, 18))
    s.append(P("Proposal valid until 12 May 2026.", "small_italic"))

    doc.build(s)
    print(f"Full proposal saved: {output}")
    return output


def build_summary():
    output = os.path.join(CLIENT_DIR, "PROPOSAL-OLIVIKS-SUMMARY-2026-04-28.pdf")

    cover_callback = build_cover_template(
        title_lines=["Cost Summary", ""],
        subtitle="Digital Growth Proposal · BridgeWorks",
        prepared_for_lines=[
            "Oliviks Nigerian Kitchen",
            "Rákóczi tér 9, 1084 Budapest",
            "Hungary",
            "28 April 2026",
        ],
        from_lines=[
            "Emmanuel Ehigbai",
            "Founder, BridgeWorks",
            "office@bridgeworks.agency",
        ],
    )

    doc = BaseDocTemplate(
        output, pagesize=A4, leftMargin=40, rightMargin=30, topMargin=50, bottomMargin=42,
        title="Cost Summary — Oliviks Nigerian Kitchen",
        author="Emmanuel Ehigbai / BridgeWorks",
    )
    cover_frame = Frame(40, 42, W - 70, H - 84, id="cover", showBoundary=0)
    body_frame = Frame(40, 42, W - 70, H - 92, id="body", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_callback),
        PageTemplate(id="Body", frames=[body_frame], onPage=_on_body_page),
    ])

    from reportlab.platypus import NextPageTemplate
    s = []
    s.append(NextPageTemplate("Body"))
    s.append(Spacer(1, 1))
    s.append(PageBreak())

    s.append(P("Cost Summary", "h1"))
    s.append(P("This is the cost summary. The full proposal document accompanies it."))
    s.append(_section_divider())

    s.append(P("What is being proposed", "h2"))
    s.append(P("<b>Part A: Foundation (one-time, this is the proposal).</b> A one-time digital rebuild that fixes everything the 4 April marketing audit flagged. Three lines: Website Upgrade, Google Business Profile Optimization, Email and WhatsApp Infrastructure. Bundled at 272,611 HUF."))
    s.append(P("<b>Part B: Optional Growth Retainer (recommended next step).</b> Operates the systems built in Part A and executes the audit's longer-term recommendations every month. 218,088 HUF per month with a 3-month minimum. You can decide on this at any time."))
    s.append(P("<b>Optional add-ons</b> (only if needed): Photo Shoot 90,870 HUF, Catering Page 79,966 HUF."))
    s.append(_section_divider())

    s.append(P("Cost breakdown", "h2"))
    s.append(P("Part A: Foundation", "h3"))
    fnd = [
        [P("Line", "table_head"), P("Price (HUF)", "table_head")],
        [P("Website Upgrade", "table_cell"), P("163,566", "table_cell")],
        [P("Google Business Profile Optimization", "table_cell"), P("65,427", "table_cell")],
        [P("Email and WhatsApp Infrastructure", "table_cell"), P("79,966", "table_cell")],
        [P("Bundle saving (3 lines together)", "table_cell"), P("-36,348", "table_cell")],
        [P("<b>Foundation Total</b>", "table_cell_bold"), P("<b>272,611</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(fnd, [375, 100]))
    s.append(Spacer(1, 8))

    s.append(P("Part B: Optional Retainer", "h3"))
    ret = [
        [P("Item", "table_head"), P("Price (HUF)", "table_head")],
        [P("Monthly retainer", "table_cell"), P("218,088 / month", "table_cell")],
        [P("Minimum commitment", "table_cell"), P("3 months", "table_cell")],
        [P("<b>3-month total</b>", "table_cell_bold"), P("<b>654,264</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(ret, [375, 100]))
    s.append(Spacer(1, 8))

    s.append(P("Optional add-ons", "h3"))
    addons = [
        [P("Item", "table_head"), P("Price (HUF)", "table_head")],
        [P("Photo Shoot (half-day on-site)", "table_cell"), P("90,870", "table_cell")],
        [P("Catering Page (dedicated page in EN+HU)", "table_cell"), P("79,966", "table_cell")],
    ]
    s.append(_styled_table(addons, [375, 100]))
    s.append(_section_divider())

    s.append(P("Total scenarios", "h2"))
    sc = [
        [P("Scenario", "table_head"), P("Total (HUF)", "table_head")],
        [P("Foundation only", "table_cell"), P("272,611", "table_cell")],
        [P("Foundation + Retainer (3 months)", "table_cell"), P("926,875", "table_cell")],
        [P("Foundation + Retainer + Photo Shoot", "table_cell"), P("1,017,745", "table_cell")],
        [P("Foundation + Retainer + Photo Shoot + Catering Page", "table_cell"), P("1,097,711", "table_cell")],
    ]
    s.append(_styled_table(sc, [375, 100]))
    s.append(_section_divider())

    s.append(P("Payment structure", "h2"))
    s.append(P("If Foundation only", "h3"))
    p1 = [
        [P("When", "table_head"), P("Amount (HUF)", "table_head")],
        [P("On contract signing", "table_cell"), P("136,306", "table_cell")],
        [P("On website handover (end of week 3)", "table_cell"), P("136,305", "table_cell")],
        [P("<b>Total</b>", "table_cell_bold"), P("<b>272,611</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(p1, [310, 165]))
    s.append(Spacer(1, 6))
    s.append(P("If Foundation + Retainer", "h3"))
    p2 = [
        [P("When", "table_head"), P("Amount (HUF)", "table_head")],
        [P("On contract signing (50% setup + month 1)", "table_cell"), P("354,394", "table_cell")],
        [P("On website handover (end of week 3)", "table_cell"), P("136,305", "table_cell")],
        [P("Month 2, 1st of month", "table_cell"), P("218,088", "table_cell")],
        [P("Month 3, 1st of month", "table_cell"), P("218,088", "table_cell")],
        [P("<b>Total</b>", "table_cell_bold"), P("<b>926,875</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(p2, [310, 165]))
    s.append(Spacer(1, 4))
    s.append(P("Add-ons invoiced separately on agreement.", "small"))
    s.append(_section_divider())

    s.append(P("Invoicing notes", "h2"))
    s.append(P("All prices stated in HUF. Invoices issued in HUF via szamlazz.hu under Hungarian VAT exemption (Áfa törvény 188. §, alanyi adómentes)."))
    s.append(P("Payable in HUF.", "body_bold"))
    s.append(_section_divider())

    s.append(P("Next step", "h2"))
    s.append(P("Reply with the scenario you want and any add-ons. Contract follows within 24 hours."))
    s.append(Spacer(1, 16))
    s.append(P("Cost summary valid until 12 May 2026.", "small_italic"))

    doc.build(s)
    print(f"Summary saved: {output}")
    return output


if __name__ == "__main__":
    build_full_proposal()
    build_summary()
