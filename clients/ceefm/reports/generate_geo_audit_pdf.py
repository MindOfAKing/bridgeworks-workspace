"""
Generate branded PDF for CEEFM GEO Audit Report 2026-06-11.
BridgeWorks brand: Navy #0F1A2E, Gold #B8860B, Ivory #F5F0E8, Charcoal #1C2B3A.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                 Paragraph, Spacer, Table, TableStyle,
                                 KeepTogether, PageBreak, NextPageTemplate)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

NAVY    = HexColor('#0F1A2E')
GOLD    = HexColor('#B8860B')
IVORY   = HexColor('#F5F0E8')
CHARCOAL= HexColor('#1C2B3A')
WARM_GRAY = HexColor('#6B6560')
WHITE   = HexColor('#FFFFFF')
ROW_ALT = HexColor('#EDE8DF')

W, H = A4
ML = 22*mm
MR = 20*mm
MT = 18*mm
MB = 18*mm
BAR = 6
FRAME_W = W - ML - BAR - MR
TABLE_W = 430


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold accent bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, BAR, H, fill=1, stroke=0)
    # Navy cover band (top 32%)
    band_h = H * 0.32
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - band_h, W, band_h, fill=1, stroke=0)
    # Gold rule at band bottom
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - band_h - 1.5, W, 1.5, fill=1, stroke=0)
    # Title
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 26)
    canvas.drawString(ML + BAR, H - band_h + 72, 'CEEFM Kft')
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawString(ML + BAR, H - band_h + 48, 'GEO Audit Report')
    canvas.setFont('Helvetica', 11)
    canvas.setFillColor(GOLD)
    canvas.drawString(ML + BAR, H - band_h + 28, 'Final Score: 78/100 · Good Band · 2026-06-11')
    # Subtitle
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(ML + BAR, H - band_h - 18, 'Powered by BridgeWorks')
    # Meta block
    canvas.setFillColor(CHARCOAL)
    canvas.setFont('Helvetica', 9)
    meta_y = H - band_h - 44
    for line in [
        'URL: https://ceefm.eu',
        'Business Type: Professional Services / Local Business',
        'Pages Analyzed: 8',
        'Prior Audit: 2026-06-10 (77/100)',
        'Prepared by: BridgeWorks · office@bridgeworks.agency',
    ]:
        canvas.drawString(ML + BAR, meta_y, line)
        meta_y -= 14
    # Footer
    canvas.setFillColor(WARM_GRAY)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawCentredString(W / 2, 22, 'BridgeWorks · office@bridgeworks.agency · bridgeworks.agency')
    canvas.restoreState()


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, BAR, H, fill=1, stroke=0)
    canvas.setFillColor(WARM_GRAY)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawCentredString(W / 2, 22, 'BridgeWorks · office@bridgeworks.agency · bridgeworks.agency')
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(W - MR, 22, f'Page {doc.page}')
    canvas.restoreState()


def styles():
    base = dict(fontName='Helvetica', fontSize=9, leading=14, textColor=CHARCOAL,
                backColor=None, spaceBefore=0, spaceAfter=0)
    return {
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=15,
                              textColor=NAVY, spaceBefore=14, spaceAfter=6, leading=20),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=11,
                              textColor=NAVY, spaceBefore=10, spaceAfter=4, leading=15),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=9.5,
                              textColor=CHARCOAL, spaceBefore=8, spaceAfter=3, leading=13),
        'body': ParagraphStyle('body', **base),
        'bold': ParagraphStyle('bold', fontName='Helvetica-Bold', fontSize=9,
                                textColor=CHARCOAL, leading=14),
        'note': ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8.5,
                                textColor=WARM_GRAY, leading=13),
        'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=8,
                                   textColor=WARM_GRAY, leading=11),
        'gold_label': ParagraphStyle('gold_label', fontName='Helvetica-Bold', fontSize=9,
                                      textColor=GOLD, leading=13),
    }


def navy_table(data, col_widths, header=True):
    style = [
        ('FONTNAME',  (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE',  (0, 0), (-1, -1), 8.5),
        ('LEADING',   (0, 0), (-1, -1), 12),
        ('VALIGN',    (0, 0), (-1, -1), 'TOP'),
        ('GRID',      (0, 0), (-1, -1), 0.4, WARM_GRAY),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
    ]
    if header and len(data) > 0:
        style += [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]
        for i in range(1, len(data)):
            bg = IVORY if i % 2 == 1 else ROW_ALT
            style.append(('BACKGROUND', (0, i), (-1, i), bg))
    else:
        for i in range(len(data)):
            bg = IVORY if i % 2 == 0 else ROW_ALT
            style.append(('BACKGROUND', (0, i), (-1, i), bg))
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style))
    return t


class ScoreBar(Flowable):
    def __init__(self, label, score, max_score=100, bar_w=240, bar_h=14):
        super().__init__()
        self.label = label
        self.score = score
        self.max_score = max_score
        self.bar_w = bar_w
        self.bar_h = bar_h
        self.width = FRAME_W
        self.height = bar_h + 6

    def draw(self):
        c = self.canv
        # Label
        c.setFont('Helvetica', 8.5)
        c.setFillColor(CHARCOAL)
        c.drawString(0, 4, self.label)
        # Background bar
        bx = 160
        c.setFillColor(ROW_ALT)
        c.roundRect(bx, 2, self.bar_w, self.bar_h - 2, 2, fill=1, stroke=0)
        # Gold fill
        fill = (self.score / self.max_score) * self.bar_w
        c.setFillColor(GOLD)
        c.roundRect(bx, 2, fill, self.bar_h - 2, 2, fill=1, stroke=0)
        # Score text
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawCentredString(bx + fill / 2, 5, f'{self.score}/100')


def issue_block(num, title, priority, detail, S):
    header_data = [[
        Paragraph(f'{num}. {title}', ParagraphStyle('ih', fontName='Helvetica-Bold',
                  fontSize=9, textColor=WHITE, leading=13)),
        Paragraph(priority, ParagraphStyle('ip', fontName='Helvetica-Bold',
                  fontSize=8, textColor=GOLD, leading=13, alignment=TA_RIGHT)),
    ]]
    header = Table(header_data, colWidths=[TABLE_W * 0.78, TABLE_W * 0.22])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    body_data = [[Paragraph(detail, S['body'])]]
    body = Table(body_data, colWidths=[TABLE_W])
    body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ROW_ALT),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([header, body, Spacer(1, 6)])


def build(S):
    story = []

    # Section 1: Executive Summary
    story.append(Paragraph('Executive Summary', S['h1']))
    story.append(Paragraph(
        '<b>Overall GEO Score: 78/100 (Good)</b>', S['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'Three of the four High-priority issues from the June 10 audit were resolved: '
        'FAQPage schema is now live on the homepage, all eight pages are in the sitemap, '
        'and the llms.txt year error ("12 years") has been corrected to "16 years." '
        'These changes push the score from 77 to 78.',
        S['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'The site remains in the Good band. The one High-priority item that did not change is '
        'the Google Business Profile, not yet verified. That remains the highest single-action '
        'gain available. Once verified and linked in the schema, the score is expected to reach 81-82.',
        S['body']))
    story.append(Spacer(1, 10))

    # Score progression table
    story.append(Paragraph('Score Progression', S['h2']))
    prog = [
        ['Date', 'Score', 'Band', 'Driver'],
        ['2026-03', '16/100', 'Critical', 'Pre-engagement baseline'],
        ['2026-04-03', '29/100', 'Critical', 'Discovery audit, no fixes yet'],
        ['2026-04-22', '47/100', 'Poor', 'llms.txt, hreflang, partial schema'],
        ['2026-04-30 morning', '61/100', 'Fair', 'Schema completion, legal imprint, security headers'],
        ['2026-04-30 evening', '74/100', 'Fair (top)', 'Wikidata, IndexNow, Bing, GBP claim, LinkedIn polish'],
        ['2026-06-10', '77/100', 'Good', 'Funnel pages launched, TikTok'],
        ['2026-06-11', '78/100', 'Good', 'FAQPage schema, sitemap complete, llms.txt corrected'],
    ]
    prog_rows = []
    for row in prog:
        prog_rows.append([Paragraph(cell, S['body']) for cell in row])
    story.append(navy_table(prog_rows, [70, 55, 60, TABLE_W - 185]))
    story.append(Spacer(1, 4))
    story.append(Paragraph('The engagement closes with a 62-point gain from baseline.', S['bold']))
    story.append(Spacer(1, 12))

    # Score breakdown
    story.append(Paragraph('Score Breakdown', S['h2']))
    breakdown = [
        ['Category', 'Score', 'Weight', 'Weighted', 'Delta'],
        ['AI Citability', '78/100', '25%', '19.50', '+2'],
        ['Brand Authority', '71/100', '20%', '14.20', '0'],
        ['Content E-E-A-T', '72/100', '20%', '14.40', '0'],
        ['Technical GEO', '92/100', '15%', '13.80', '+2'],
        ['Schema & Structured Data', '83/100', '10%', '8.30', '+3'],
        ['Platform Optimization', '76/100', '10%', '7.60', '0'],
        ['Overall GEO Score', '', '', '77.8 → 78', '+1'],
    ]
    bd_rows = []
    for row in breakdown:
        bd_rows.append([Paragraph(cell, S['body']) for cell in row])
    story.append(navy_table(bd_rows, [160, 55, 45, 60, TABLE_W - 320]))
    story.append(Spacer(1, 10))

    # Score bars
    story.append(Paragraph('Category Scores', S['h2']))
    for label, score in [
        ('AI Citability', 78), ('Brand Authority', 71), ('Content E-E-A-T', 72),
        ('Technical GEO', 92), ('Schema & Structured Data', 83), ('Platform Optimization', 76),
    ]:
        story.append(ScoreBar(label, score))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # Section 2: Issues Resolved
    story.append(Paragraph('Issues Resolved Since June 10', S['h1']))
    resolved = [
        ['Issue', 'Status'],
        ['Funnel pages absent from sitemap', 'Fixed — all 8 URLs now in sitemap-0.xml'],
        ['FAQPage schema missing on homepage', 'Fixed — FAQPage JSON-LD live in page source'],
        ['llms.txt "12 years" error', 'Fixed — now reads "16 years of operational experience"'],
    ]
    res_rows = [[Paragraph(cell, S['body']) for cell in row] for row in resolved]
    story.append(navy_table(res_rows, [200, TABLE_W - 200]))
    story.append(Spacer(1, 10))

    # Section 3: Remaining Issues
    story.append(Paragraph('Remaining Issues for Victor to Action', S['h1']))
    story.append(Paragraph('High Priority', S['h2']))

    story.append(issue_block(1, 'Google Business Profile — not yet verified', 'HIGH',
        'The GBP was claimed but the postcard verification was not completed during the engagement. '
        'Every local "facility management Budapest" query that surfaces a Maps result currently '
        'excludes CEEFM. GBP verification also feeds the knowledge panel on Gemini, the Perplexity '
        'local results, and enables Google Reviews.<br/><br/>'
        '<b>Action:</b> Go to business.google.com, complete the postcard verification, then add the '
        'GBP URL to the sameAs array in BaseLayout.astro.<br/>'
        '<b>Expected impact:</b> +3 to +4 points overall. Score would reach 81-82.', S))

    story.append(issue_block(2, 'Privacy policy page returns 404', 'HIGH',
        'The contact form links to a privacy policy but the page does not exist. '
        'This is a GDPR compliance issue for a Hungarian company collecting personal data via web form.<br/><br/>'
        '<b>Action:</b> Create /privacy-policy/ (English) and /adatvedelem/ (Hungarian) pages '
        'with the required GDPR privacy notice. A solicitor or GDPR template service can provide the text.', S))

    story.append(issue_block(3, 'Homepage reads "10+ Years Experience"', 'HIGH',
        'The company was founded in 2010. As of 2026 that is 16 years. '
        'The llms.txt correctly says "16 years." The homepage hero stat still says "10+." '
        'AI crawlers quoting this stat will cite an inaccurate figure.<br/><br/>'
        '<b>Action:</b> Edit the hero component and change to "16 Years" or "Since 2010."', S))

    story.append(Paragraph('Medium Priority', S['h2']))

    story.append(issue_block(4, 'Meta descriptions missing on four funnel pages', 'MEDIUM',
        '/hospitality/, /residential/, /lakopark/, /vendeglatas/ have no meta description. '
        'Search engines and AI crawlers generate their own snippet text for these pages.<br/><br/>'
        '<b>Action:</b> Add a description prop to each of the four page files in src/pages/. '
        '130-155 characters each, with location and a specific service claim.', S))

    story.append(issue_block(5, 'Funnel pages are thin', 'MEDIUM',
        'Hospitality page is approximately 370 words. Residential page is approximately 670 words. '
        'For AI models to extract substantive answers from them, each page needs to be 800 words '
        'minimum with structured proof points.<br/><br/>'
        '<b>Action:</b> Expand both pages with process documentation, client outcome data, '
        'and a 3-5 question FAQ section per page with FAQPage schema.', S))

    story.append(issue_block(6, 'No About page', 'MEDIUM',
        '/about/ returns 404. A dedicated company history page with named leadership, founding date, '
        'client count, and service scope is a core E-E-A-T signal for both AI systems and human visitors.<br/><br/>'
        '<b>Action:</b> Create /about/ with company history, Victor\'s bio and LinkedIn profile, '
        'and verifiable company facts.', S))

    story.append(issue_block(7, 'llms.txt missing Limehome case study and page links', 'MEDIUM',
        'The strongest third-party proof point (Limehome Budapest, 9.4 cleanliness score, '
        '24 months above 9.0) is not referenced in llms.txt. AI crawlers reading this file '
        'first cannot discover the funnel pages.<br/><br/>'
        '<b>Action:</b> Add a ## Case Study section with the Limehome data. '
        'Add a ## Pages section with absolute URLs for all service pages.', S))

    story.append(Paragraph('Lower Priority', S['h2']))

    story.append(issue_block(8, 'Sitemap has no lastmod dates', 'LOW',
        'All 8 sitemap entries have no lastmod value. Crawlers cannot determine freshness.<br/><br/>'
        '<b>Action:</b> Add lastmod: true to @astrojs/sitemap in astro.config.mjs and redeploy.', S))

    story.append(issue_block(9, 'speakable property on wrong schema type', 'LOW',
        'speakable is attached to the ProfessionalService schema block. Schema.org only supports '
        'it on Article and WebPage types. The validator flags it as a warning.<br/><br/>'
        '<b>Action:</b> Remove speakable from the ProfessionalService block. Add a separate '
        'WebPage schema block per page that includes speakable with the same CSS selectors.', S))

    story.append(issue_block(10, 'No blog or topical content', 'LOW',
        'The site has no blog, guides, or resource pages. For AI models to cite ceefm.eu '
        'as an authority on facility management topics, the site needs content beyond service descriptions.<br/><br/>'
        '<b>Recommended topics:</b> "Facility management for aparthotels in Budapest," '
        '"EU hygiene compliance for residential buildings," '
        '"How to evaluate a facility management contract in Hungary."', S))

    story.append(Spacer(1, 10))

    # Section 4: What Was Built
    story.append(Paragraph('What Was Built During the Engagement', S['h1']))
    built = [
        ['Item', 'Status'],
        ['ProfessionalService JSON-LD schema (comprehensive)', 'Live'],
        ['FAQPage JSON-LD schema (homepage)', 'Live'],
        ['robots.txt with explicit AI crawler permissions (13 crawlers)', 'Live'],
        ['llms.txt (AI-first company summary)', 'Live'],
        ['Bilingual hreflang tags (en/hu)', 'Live'],
        ['Canonical URLs on all pages', 'Live'],
        ['Security headers (HSTS, CSP, X-Frame-Options)', 'Live'],
        ['Open Graph and Twitter Card meta tags', 'Live'],
        ['Bing Webmaster verification', 'Live'],
        ['GA4 analytics', 'Live'],
        ['Google Consent Mode v2', 'Live'],
        ['Cookie consent banner', 'Live'],
        ['Wikidata entity (Q139592822)', 'Live'],
        ['IndexNow integration', 'Live'],
        ['Sitemap including all 8 pages', 'Live'],
        ['4 service funnel pages (EN and HU)', 'Live'],
        ['LinkedIn company page polished', 'Done'],
        ['TikTok Business account created', 'Done'],
        ['Cold email sequence (11 delivered, pipeline built)', 'Done'],
    ]
    built_rows = [[Paragraph(cell, S['body']) for cell in row] for row in built]
    story.append(navy_table(built_rows, [TABLE_W - 70, 70]))
    story.append(Spacer(1, 10))

    # Closing
    closing_data = [[
        Paragraph(
            '<b>BridgeWorks</b><br/>office@bridgeworks.agency<br/>bridgeworks.agency',
            ParagraphStyle('cl', fontName='Helvetica', fontSize=8.5,
                           textColor=GOLD, leading=14, alignment=TA_CENTER)
        )
    ]]
    closing = Table(closing_data, colWidths=[TABLE_W])
    closing.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(closing)

    return story


def main():
    out = os.path.join(os.path.dirname(__file__), 'GEO-AUDIT-REPORT-2026-06-11.pdf')
    S = styles()

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=ML + BAR, rightMargin=MR, topMargin=MT, bottomMargin=MB + 14,
        title='GEO Audit Report — CEEFM Kft',
        author='BridgeWorks',
    )

    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    content_frame = Frame(ML + BAR, MB + 14, FRAME_W, H - MT - MB - 14, id='content')

    cover_tpl = PageTemplate(id='Cover', frames=[cover_frame], onPage=on_cover)
    content_tpl = PageTemplate(id='Content', frames=[content_frame], onPage=on_page)
    doc.addPageTemplates([cover_tpl, content_tpl])

    story = [NextPageTemplate('Content'), PageBreak()] + build(S)
    doc.build(story)
    print(f'Generated: {out}')

    from pypdf import PdfReader
    r = PdfReader(out)
    print(f'Pages: {len(r.pages)}')


if __name__ == '__main__':
    main()
