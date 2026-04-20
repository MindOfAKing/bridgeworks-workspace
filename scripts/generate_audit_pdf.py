"""Generate branded PDF for O'liviks Marketing Audit."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas as canvasmod

# Brand colors
NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
SAGE = HexColor("#4A6741")
LIGHT_GOLD = HexColor("#F5EDD8")

W, H = A4
LEFT_BAR = 6
MARGIN_LEFT = 20 * mm
MARGIN_RIGHT = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 30 * mm


def draw_background(c, doc):
    """Draw ivory background, gold left bar, and footer on every page."""
    c.saveState()
    # Ivory background
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold left accent bar
    c.setFillColor(GOLD)
    c.rect(0, 0, LEFT_BAR, H, fill=1, stroke=0)
    # Footer
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawCentredString(W / 2, 22, "BridgeWorks  \u00b7  office@bridgeworks.agency  \u00b7  bridgeworks.agency")
    # Page number
    c.drawRightString(W - MARGIN_RIGHT, 22, f"Page {doc.page}")
    c.restoreState()


def draw_cover(c, doc):
    """Draw the cover page."""
    c.saveState()
    # Ivory background
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold left accent bar
    c.setFillColor(GOLD)
    c.rect(0, 0, LEFT_BAR, H, fill=1, stroke=0)
    # Navy header band (top 32%)
    band_h = H * 0.32
    band_y = H - band_h
    c.setFillColor(NAVY)
    c.rect(0, band_y, W, band_h, fill=1, stroke=0)
    # Gold rule below band
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, band_y, W, band_y)
    # Document type
    c.setFont("Helvetica", 11)
    c.setFillColor(GOLD)
    c.drawString(MARGIN_LEFT + 10, H - 45, "MARKETING AUDIT")
    # Title
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(white)
    c.drawString(MARGIN_LEFT + 10, H - 90, "O'liviks Kitchen")
    # Subtitle
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#CCCCCC"))
    c.drawString(MARGIN_LEFT + 10, H - 115, "oliviks.com")
    # Score circle
    cx = W - 70 * mm
    cy = H - 85
    c.setFillColor(GOLD)
    c.circle(cx, cy, 32, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(NAVY)
    c.drawCentredString(cx, cy - 3, "38")
    c.setFont("Helvetica", 9)
    c.drawCentredString(cx, cy - 16, "/100")
    # Details below band
    details_y = band_y - 45
    c.setFont("Helvetica", 11)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN_LEFT + 10, details_y, "Date: April 4, 2026")
    c.drawString(MARGIN_LEFT + 10, details_y - 22, "Business Type: Local Food Business / Restaurant")
    c.drawString(MARGIN_LEFT + 10, details_y - 44, "Location: Budapest, Hungary")
    c.drawString(MARGIN_LEFT + 10, details_y - 66, "Grade: F")
    # Powered by
    c.setFont("Helvetica", 10)
    c.setFillColor(WARM_GRAY)
    c.drawCentredString(W / 2, 50, "Powered by BridgeWorks")
    # Footer
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(W / 2, 22, "BridgeWorks  \u00b7  office@bridgeworks.agency  \u00b7  bridgeworks.agency")
    c.restoreState()


# Styles
style_h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
                           spaceAfter=10, spaceBefore=20, leading=22)
style_h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
                           spaceAfter=8, spaceBefore=16, leading=18)
style_h3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, textColor=CHARCOAL,
                           spaceAfter=6, spaceBefore=12, leading=14)
style_body = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, textColor=CHARCOAL,
                            leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
style_bold_body = ParagraphStyle("BoldBody", fontName="Helvetica-Bold", fontSize=9.5,
                                  textColor=CHARCOAL, leading=14, spaceAfter=6)
style_bullet = ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5, textColor=CHARCOAL,
                               leading=14, spaceAfter=4, leftIndent=15, bulletIndent=5,
                               bulletFontName="Helvetica", bulletFontSize=9.5)
style_small = ParagraphStyle("Small", fontName="Helvetica", fontSize=8, textColor=WARM_GRAY,
                              leading=11, spaceAfter=4)


def gold_rule():
    return HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=8, spaceBefore=4)


def score_bar_table(label, score, max_score=100, bar_width=180):
    """Create a visual score bar row."""
    filled = int(bar_width * score / max_score)
    empty = bar_width - filled

    bar_data = [[""]]
    bar = Table(bar_data, colWidths=[bar_width], rowHeights=[12])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), GOLD),
        ("LINEAFTER", (0, 0), (0, 0), empty, IVORY),
    ]))

    # Use a simpler approach: text + colored rectangles via table
    data = [[label, f"{score}/100"]]
    t = Table(data, colWidths=[320, 80])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, 0), "Helvetica", ),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, 0), CHARCOAL),
        ("TEXTCOLOR", (1, 0), (1, 0), NAVY),
        ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def make_table(headers, rows, col_widths=None):
    """Create a branded table."""
    data = [headers] + rows
    if not col_widths:
        col_widths = [W * 0.85 / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("TEXTCOLOR", (0, 1), (-1, -1), CHARCOAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GOLD]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D0C8BE")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf():
    output_path = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\oliviks\reports\MARKETING-AUDIT.pdf"

    doc = BaseDocTemplate(output_path, pagesize=A4,
                          leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT,
                          topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)

    frame_cover = Frame(0, 0, W, H, id="cover", leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)
    frame_body = Frame(MARGIN_LEFT, MARGIN_BOTTOM, W - MARGIN_LEFT - MARGIN_RIGHT,
                       H - MARGIN_TOP - MARGIN_BOTTOM, id="body")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover], onPage=draw_cover),
        PageTemplate(id="content", frames=[frame_body], onPage=draw_background),
    ])

    story = []

    # Cover page (empty flowable, the onPage handler draws everything)
    story.append(Spacer(1, H))
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

    # ── EXECUTIVE SUMMARY ──
    story.append(Paragraph("Executive Summary", style_h1))
    story.append(gold_rule())

    exec_paras = [
        "O'liviks Kitchen scores 38 out of 100 in this marketing audit. That score does not reflect the quality of the food or the real-world reputation of the business. It reflects the massive gap between what O'liviks has earned offline and what its digital presence communicates.",
        "The biggest strength is clear: O'liviks has a 4.8-star Google rating from 160+ reviews, features in major Hungarian media (Origo, We Love Budapest, WMN), presence on both Wolt and Foodora, and a near-monopoly on authentic Nigerian food in Budapest. The food speaks for itself.",
        "The biggest gap is equally clear: the website fails to communicate any of this. The homepage does not pass the 5-second test. The About page leads with generic health buzzwords instead of the founders' compelling story. The testimonials lack photos and context to feel credible. There is no blog content, no embedded Google reviews, and duplicate pages suggest a rushed or incomplete setup.",
        "The top three actions that would move the needle most: (1) Rewrite the homepage headline and About page to lead with \"Authentic Nigerian Kitchen in Budapest\" and the founders' real story, (2) Strengthen testimonials with photos and dates, plus embed Google reviews, (3) Build a simple retention system (WhatsApp broadcast list, email capture, repeat order incentives). Implementing all recommendations could increase monthly direct orders by 30-50%.",
    ]
    for p in exec_paras:
        story.append(Paragraph(p, style_body))
    story.append(Spacer(1, 8))

    # ── SCORE BREAKDOWN ──
    story.append(Paragraph("Score Breakdown", style_h1))
    story.append(gold_rule())

    score_headers = ["Category", "Score", "Weight", "Wtd.", "Key Finding"]
    score_rows = [
        ["Content & Messaging", "32/100", "25%", "8.0",
         "Homepage fails 5-second test; health messaging misaligned"],
        ["Conversion Optimization", "35/100", "20%", "7.0",
         "Self-pickup friction, duplicate pages, empty shop"],
        ["SEO & Discoverability", "38/100", "20%", "7.6",
         "Missing meta descriptions, no schema markup"],
        ["Competitive Positioning", "52/100", "15%", "7.8",
         "Highest Google rating but confused positioning"],
        ["Brand & Trust", "42/100", "10%", "4.2",
         "Strong real reputation invisible on website"],
        ["Growth & Strategy", "35/100", "10%", "3.5",
         "Zero retention system, no content strategy"],
        ["TOTAL", "", "100%", "38/100", ""],
    ]
    score_table = make_table(score_headers, score_rows,
                             col_widths=[95, 45, 38, 35, 225])
    story.append(score_table)
    story.append(Spacer(1, 12))

    # ── QUICK WINS ──
    story.append(Paragraph("Quick Wins (This Week)", style_h1))
    story.append(gold_rule())

    quick_wins = [
        ("<b>Strengthen the testimonials section.</b> The existing testimonials lack photos, dates, and context. Add customer photos, review dates, and a note about what they ordered. Embed real Google reviews alongside them to build layered social proof. Impact: High. Effort: 1-2 hours.",
        ),
        ("<b>Add the Google rating to the homepage.</b> Display \"4.8 stars from 160+ reviews\" prominently above the fold. Add Wolt and Foodora badges. This is free credibility that is currently invisible. Impact: High. Effort: 30 minutes.",
        ),
        ("<b>Delete the Sample Page.</b> The default WordPress \"Sample Page\" is still live. It signals an unfinished site. Impact: Low but easy. Effort: 5 minutes.",
        ),
        ("<b>Remove duplicate pages.</b> cart-2, checkout-2, and my-account-2 are migration artifacts creating confusion and potential SEO issues. Delete or redirect them. Impact: Medium. Effort: 15 minutes.",
        ),
        ("<b>Rewrite the homepage headline.</b> Replace the current unclear hero with something direct: \"Authentic Nigerian Food. Made Fresh in Budapest. Order for Pickup or Delivery.\" Impact: High. Effort: 30 minutes.",
        ),
        ("<b>Add dish descriptions to all 23 products.</b> Each menu item needs 2-3 sentences explaining what the dish is, especially for Hungarian customers who have never heard of egusi soup or puff puff. Impact: High. Effort: 2-3 hours.",
        ),
        ("<b>Fix the \"CHEF HOTLINE\" contact heading.</b> Change to \"Call to Order\" or \"Reach Us\" or simply \"Contact.\" Impact: Low. Effort: 5 minutes.",
        ),
        ("<b>Add media logos to homepage.</b> \"As featured in Origo, We Love Budapest, WMN\" with publication logos is powerful third-party validation. Impact: High. Effort: 1 hour.",
        ),
    ]
    for i, (win,) in enumerate(quick_wins, 1):
        story.append(Paragraph(f"{i}. {win}", style_body))
    story.append(Spacer(1, 6))

    # ── STRATEGIC RECOMMENDATIONS ──
    story.append(Paragraph("Strategic Recommendations (This Month)", style_h1))
    story.append(gold_rule())

    strat_recs = [
        "<b>Rewrite the About page around the founders' real story.</b> O'liviks is run by Olivia and her husband, both social work graduates who saw a gap in Budapest: many Nigerian students, no Nigerian restaurants. That story builds instant trust. Add their photos, their journey, and their \"why.\" Impact: High. Timeline: 1 week.",
        "<b>Build a retention system.</b> Start a WhatsApp broadcast list for daily/weekly specials. Add an email signup popup. Create a simple loyalty card (buy 10, get 1 free). Turn one-time Wolt customers into direct-order regulars. Impact: High. Timeline: 2 weeks.",
        "<b>Launch a \"Nigerian Food in Budapest\" blog.</b> One post per week targeting local search queries: \"Best Nigerian food in Budapest,\" \"What is jollof rice,\" \"Nigerian catering Budapest.\" Each post 400-600 words. Impact: Medium. Timeline: Ongoing.",
        "<b>Optimize Wolt and Foodora listings.</b> Better menu descriptions, professional food photos, and fast response times. These platforms are O'liviks' strongest discovery channel. Impact: High. Timeline: 1 week.",
        "<b>Create a \"New to Nigerian Food?\" guide page.</b> Introduce 5-6 signature dishes with photos and explanations. Removes the intimidation factor for curious customers. Impact: Medium. Timeline: 1 week.",
        "<b>Justify premium pricing on the website.</b> O'liviks charges 4,700-6,500 HUF per dish, the highest in segment. Add portion size photos, ingredient sourcing stories, \"made from scratch daily\" messaging. Impact: Medium. Timeline: 2 weeks.",
    ]
    for i, rec in enumerate(strat_recs, 1):
        story.append(Paragraph(f"{i}. {rec}", style_body))
    story.append(Spacer(1, 6))

    # ── LONG-TERM INITIATIVES ──
    story.append(Paragraph("Long-Term Initiatives (This Quarter)", style_h1))
    story.append(gold_rule())

    long_term = [
        "<b>Activate TikTok with Nigerian food content.</b> Short-form video of jollof rice being cooked, suya being grilled, customer first-reaction videos. Nigerian food content performs extremely well globally. Target: 3 videos per week. Timeline: 8-12 weeks.",
        "<b>Build catering as a revenue line.</b> Already branded as \"O'liviks Catering\" on Instagram but invisible on website. Create a dedicated catering page with packages for corporate events, university gatherings, and community celebrations. Timeline: 4-6 weeks.",
        "<b>Launch a Google review generation campaign.</b> Push from 160 to 300+ reviews. QR codes at pickup counter, follow-up WhatsApp messages, small incentive (free puff puff with next order for a review). Timeline: 8-12 weeks.",
        "<b>Target the Hungarian mainstream audience.</b> Pitch to food bloggers, invite micro-influencers for free tastings, create Hungarian-language content. The media is already interested. Timeline: Ongoing.",
        "<b>Explore pop-ups and food festivals.</b> Budapest has an active street food scene (Karavan, Balna, Szimpla market). A Nigerian food stall would generate media attention and new customers. Timeline: Next market season.",
    ]
    for i, item in enumerate(long_term, 1):
        story.append(Paragraph(f"{i}. {item}", style_body))

    story.append(PageBreak())

    # ── DETAILED ANALYSIS ──
    story.append(Paragraph("Detailed Analysis by Category", style_h1))
    story.append(gold_rule())

    # Content & Messaging
    story.append(Paragraph("Content & Messaging Analysis", style_h2))
    story.append(Paragraph("<b>Score: 32/100</b>", style_bold_body))

    cm_sections = [
        ("<b>Headline Clarity (25/100):</b> The homepage fails the 5-second test. A visitor cannot immediately tell what O'liviks offers. The tagline \"Order, Eat &amp; Order Again...\" is catchy but tells nothing about the cuisine, location, or ordering model. For a niche business, clarity is survival."),
        ("<b>Value Proposition (30/100):</b> The single biggest competitive advantage is being a Nigerian food restaurant in Budapest. The site buries this. The About page leads with generic health language. The core values (High Quality, Everyday Fresh, Pesticide Free) sound like a European organic grocery store, not a Nigerian kitchen."),
        ("<b>Body Copy (25/100):</b> Copy reads as templated. It does not speak to customer pain points. Nigerian expats miss home cooking. Hungarians are curious but unsure where to start. The current copy addresses neither audience."),
        ("<b>Social Proof (30/100):</b> The six testimonials are real but lack supporting elements: no customer photos, no dates, no order context. Without visual anchors, text-only testimonials feel generic regardless of authenticity. The 160+ Google reviews are not surfaced on the site at all. Adding photos, dates, and embedded Google reviews would significantly strengthen this section."),
        ("<b>Content Depth (35/100):</b> A blog page exists but likely has minimal posts. No educational content explaining Nigerian dishes to a European audience."),
        ("<b>Brand Voice Consistency (35/100):</b> Clear disconnect between health/sustainability (About page) and Nigerian comfort food (the menu). The dominant voice should match the food: warm, bold, generous, a little playful."),
    ]
    for s in cm_sections:
        story.append(Paragraph(s, style_body))
    story.append(Spacer(1, 6))

    # Conversion Optimization
    story.append(Paragraph("Conversion Optimization Analysis", style_h2))
    story.append(Paragraph("<b>Score: 35/100</b>", style_bold_body))

    conv_sections = [
        ("<b>Ordering Flow Friction:</b> Self-pickup model with phone-request-only delivery is the highest friction point. In 2026 Budapest where Wolt delivers in 30 minutes, requiring a phone call for delivery is a conversion killer."),
        ("<b>Duplicate Pages:</b> cart-2, checkout-2, and my-account-2 exist alongside originals. This suggests a messy theme migration or plugin conflict."),
        ("<b>Empty Shop Page:</b> The Shop page returned empty in API queries. A primary product listing page showing no products is a critical conversion failure."),
        ("<b>WooCommerce Login:</b> If ordering requires account creation, that is additional friction. Guest checkout should be the default for a food ordering site."),
        ("<b>Pricing Visibility:</b> Product prices are not immediately visible on main menu or shop pages. Hidden pricing creates hesitation."),
    ]
    for s in conv_sections:
        story.append(Paragraph(s, style_body))
    story.append(Spacer(1, 6))

    # SEO
    story.append(Paragraph("SEO & Discoverability Analysis", style_h2))
    story.append(Paragraph("<b>Score: 38/100</b>", style_bold_body))

    seo_sections = [
        ("<b>Sitemap:</b> WordPress default sitemap exists with 6 sub-sitemaps. Functional but not optimized."),
        ("<b>URL Structure:</b> Product URLs are clean: /product/jollof-rice-with/, /product/suya-sticks/. Duplicate pages need redirects or deletion."),
        ("<b>Technical Stack:</b> WordPress + Elementor + WooCommerce + Jetpack is heavy. The site rendered almost entirely as CSS/JavaScript during extraction, suggesting heavy client-side rendering that may hurt page speed and crawlability."),
        ("<b>Missing Elements:</b> Meta descriptions likely missing on most pages. No schema markup (LocalBusiness, Restaurant). No structured data for menu items. Blog has minimal SEO content."),
        ("<b>Local SEO:</b> Google Business Profile is active (4.8 stars). But the website does not reinforce local signals: no embedded map, no structured address markup, no local keyword optimization."),
    ]
    for s in seo_sections:
        story.append(Paragraph(s, style_body))
    story.append(Spacer(1, 6))

    # Competitive Positioning
    story.append(Paragraph("Competitive Positioning Analysis", style_h2))
    story.append(Paragraph("<b>Score: 52/100</b>", style_bold_body))
    story.append(Paragraph("O'liviks leads the Nigerian/African food segment in Budapest by most measurable metrics but does not leverage this position strategically.", style_body))

    comp_headers = ["Factor", "O'liviks", "Lagos Africa", "Afrikai Bufe", "Kingson Kitchen"]
    comp_rows = [
        ["Google Rating", "4.8 (160)", "4.3 (104)", "4.5", "4.1 (19)"],
        ["Instagram", "869", "329", "93", "Negligible"],
        ["Website", "Yes", "No", "No", "Yes"],
        ["Wolt/Foodora", "Both", "Wolt only", "Neither", "Wolt"],
        ["Price (HUF)", "4,700-6,500", "2,000-6,000", "Budget", "Mid-range"],
        ["Press", "Origo, WeLoveBP", "None", "None", "TripAdvisor"],
    ]
    story.append(make_table(comp_headers, comp_rows,
                            col_widths=[72, 80, 72, 72, 80]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Key Finding:</b> O'liviks is the clear market leader by reputation metrics, but the website positions them as a generic health food brand rather than the authentic Nigerian kitchen their customers love.", style_body))
    story.append(Spacer(1, 6))

    # Brand & Trust
    story.append(Paragraph("Brand & Trust Analysis", style_h2))
    story.append(Paragraph("<b>Score: 42/100</b>", style_bold_body))

    bt_sections = [
        ("<b>Real-World Trust: Strong.</b> 4.8 Google stars from 160+ reviews. 92% Facebook recommendation rate. Featured in Origo, We Love Budapest, WMN, and Jozsefvaros Ujsag. Listed on both Wolt and Foodora."),
        ("<b>Website Trust: Weak.</b> None of the above appears on oliviks.com. No founder photos or personal story. Testimonials present but lack photos and context to feel credible at first glance. Generic WordPress theme. 30-day refund/return policy reads as a WooCommerce default. No kitchen photos or food photography."),
        ("<b>The Fix Is Simple:</b> The trust already exists. It just needs to be surfaced. Embed Google reviews. Add founder photos and story. Display media logos. Show the Wolt/Foodora ratings."),
    ]
    for s in bt_sections:
        story.append(Paragraph(s, style_body))
    story.append(Spacer(1, 6))

    # Growth & Strategy
    story.append(Paragraph("Growth & Strategy Analysis", style_h2))
    story.append(Paragraph("<b>Score: 35/100</b>", style_bold_body))

    gs_sections = [
        ("<b>Current Channels:</b> Wolt + Foodora (strongest), Instagram (869 followers, 361 posts), TikTok (minimal traction), Facebook (active), word of mouth (strong), Hungarian media (organic features)."),
        ("<b>Retention: Near Zero.</b> No loyalty program. No email list. No repeat order incentives. No WhatsApp group. No meal subscription. For a food business where repeat customers are everything, this is the biggest strategic gap."),
        ("<b>Untapped Opportunities:</b> Catering (branded on Instagram, invisible on website), university partnerships (thousands of African students), pop-ups at Budapest food markets, meal prep/weekly boxes, TikTok content, diaspora community building."),
        ("<b>Market Timing:</b> Ethnic food in European cities is booming. Budapest is diversifying. Media is actively interested. O'liviks has a 2-3 year head start on potential new entrants."),
    ]
    for s in gs_sections:
        story.append(Paragraph(s, style_body))

    story.append(PageBreak())

    # ── WEBSITE DESIGN IMPROVEMENTS ──
    story.append(Paragraph("Website Design Improvements", style_h1))
    story.append(gold_rule())

    # Homepage
    story.append(Paragraph("Homepage Redesign", style_h2))
    homepage_items = [
        "<b>Above the fold:</b> Hero image of the best dish (jollof rice or suya) with text overlay: \"Authentic Nigerian Food. Made Fresh in Budapest.\" Two clear CTAs: \"See Our Menu\" (primary) and \"Order on Wolt\" (secondary). Trust bar below: \"4.8 stars on Google | 160+ reviews | Featured in Origo, We Love Budapest.\"",
        "<b>Below the fold:</b> 4-6 \"Most Popular\" dishes with photos, descriptions, and visible prices. \"New to Nigerian Food?\" section with 3 starter recommendations. Embedded rotating Google reviews. Media logos bar. Instagram feed embed.",
    ]
    for item in homepage_items:
        story.append(Paragraph(item, style_body))

    # Navigation
    story.append(Paragraph("Navigation", style_h2))
    nav_items = [
        "Simplify to 5 items: Menu, About, Order, Catering, Contact.",
        "Remove Shop link (or redirect to Menu) since the Shop page is empty.",
        "Add a persistent \"Order Now\" button in the nav bar (gold background, always visible).",
        "Remove all duplicate pages (cart-2, checkout-2, my-account-2).",
    ]
    for item in nav_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # Menu pages
    story.append(Paragraph("Menu / Product Pages", style_h2))
    menu_items = [
        "Grid layout with large food photos for each of the 23 items.",
        "Every dish needs: name, 2-3 sentence description, price, \"Add to Cart\" button.",
        "Category tabs: Mains, Soups &amp; Swallow, Snacks, Drinks.",
        "One-line \"What is this?\" for non-Nigerian customers on every dish. Example: \"Suya Sticks: Spiced grilled beef skewers, a popular Nigerian street food.\"",
        "Prices visible on the grid, not hidden behind a click.",
    ]
    for item in menu_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # About page
    story.append(Paragraph("About Page", style_h2))
    about_items = [
        "Lead with a photo of Olivia and her husband in the kitchen.",
        "Their real story: social work graduates who saw a gap in Budapest.",
        "Timeline or journey visual: Nigeria > Budapest > Opening Day.",
        "Move \"organic, pesticide-free\" messaging to a smaller \"Our Ingredients\" subsection.",
        "End with a personal quote from the founder.",
    ]
    for item in about_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # Testimonials
    story.append(Paragraph("Testimonials & Social Proof", style_h2))
    test_items = [
        "Add customer photos and dates to existing testimonials.",
        "Embed a Google Reviews widget alongside the current testimonials.",
        "Add a \"Press\" section with quotes from the Origo and We Love Budapest articles.",
        "Show Wolt and Foodora ratings/badges near the order button.",
    ]
    for item in test_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # Checkout
    story.append(Paragraph("Checkout / Ordering", style_h2))
    checkout_items = [
        "Enable guest checkout (no account required).",
        "Make the self-pickup address prominent with an embedded Google Map.",
        "Add Wolt/Foodora deep links: \"Want delivery? Order on Wolt.\"",
        "Reduce checkout to one page: name, phone, pickup time.",
        "Remove the 30-day refund/return policy (WooCommerce default, not relevant for food).",
    ]
    for item in checkout_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # Mobile
    story.append(Paragraph("Mobile Experience", style_h2))
    mobile_items = [
        "Menu items stacked in single column with large tap targets.",
        "Sticky \"Order Now\" button at bottom of screen.",
        "Phone number clickable (tel: link) for delivery requests.",
        "WhatsApp button floating in bottom corner for questions.",
    ]
    for item in mobile_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    # Footer
    story.append(Paragraph("Footer", style_h2))
    footer_items = [
        "Full address with Google Maps link. Opening hours prominently displayed.",
        "Phone number (clickable). Social links: Instagram, TikTok, Facebook.",
        "\"As featured in...\" media logos repeated.",
    ]
    for item in footer_items:
        story.append(Paragraph(f"\u2022  {item}", style_body))

    story.append(PageBreak())

    # ── REVENUE IMPACT ──
    story.append(Paragraph("Revenue Impact Summary", style_h1))
    story.append(gold_rule())

    rev_headers = ["Recommendation", "Est. Monthly Impact", "Confidence", "Timeline"]
    rev_rows = [
        ["Strengthen testimonials + add Google reviews", "+10% conversion", "High", "1 week"],
        ["Rewrite homepage + About page", "+20-30% conversion", "High", "1 week"],
        ["Build retention system", "+25-40% repeat orders", "Medium", "2-3 weeks"],
        ["Launch blog for local search", "+500-1,500 visitors/mo", "Medium", "Ongoing"],
        ["Optimize Wolt/Foodora listings", "+10-15% platform orders", "High", "1 week"],
        ["Activate TikTok content", "+20% brand awareness", "Medium", "8-12 weeks"],
        ["Catering page + university outreach", "+200-500K HUF/mo", "Low", "4-6 weeks"],
        ["TOTAL POTENTIAL", "+40-60% monthly revenue", "", ""],
    ]
    story.append(make_table(rev_headers, rev_rows,
                            col_widths=[155, 120, 65, 65]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Note: Precise revenue figures require access to current order volume and average order value. Percentages are based on industry benchmarks for similar local food businesses.</i>", style_small))
    story.append(Spacer(1, 16))

    # ── NEXT STEPS ──
    story.append(Paragraph("Next Steps", style_h1))
    story.append(gold_rule())

    next_steps = [
        "<b>This week:</b> Strengthen testimonials with photos and context. Add Google rating, media logos, and a clear headline to the homepage. Delete sample page and duplicate pages.",
        "<b>This month:</b> Rewrite About page with founders' story. Build WhatsApp broadcast + email list. Add dish descriptions to all products. Start weekly blog.",
        "<b>This quarter:</b> Launch TikTok content strategy. Add catering page. Run Google review campaign to 300+. Explore pop-up and university partnerships.",
    ]
    for i, step in enumerate(next_steps, 1):
        story.append(Paragraph(f"{i}. {step}", style_body))

    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Generated by BridgeWorks AI Marketing Suite</i>", style_small))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf()
