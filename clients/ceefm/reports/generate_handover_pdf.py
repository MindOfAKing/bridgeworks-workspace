"""
Generate branded CEEFM Handover PDF
BridgeWorks brand: Navy/Gold/Ivory — ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable

NAVY      = HexColor('#0F1A2E')
GOLD      = HexColor('#B8860B')
IVORY     = HexColor('#F5F0E8')
CHARCOAL  = HexColor('#1C2B3A')
WARM_GRAY = HexColor('#6B6560')
ROW_ALT   = HexColor('#EDE8DF')
BORDER    = HexColor('#C8C0B0')

W, H = A4
ML = 22 * mm
MR = 20 * mm
MT = 18 * mm
MB = 18 * mm
BAR = 6

FRAME_W = W - ML - BAR - MR  # ~470 pt
TABLE_W = 430


# ── Page callbacks ────────────────────────────────────────────

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    band_h = H * 0.32
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - band_h, W, band_h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, BAR, H, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.5)
    canvas.line(0, H - band_h, W, H - band_h)

    tx = ML + BAR + 8
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 28)
    canvas.drawString(tx, H - band_h + band_h * 0.60, 'CEEFM Kft')
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawString(tx, H - band_h + band_h * 0.44, 'Digital Growth Engagement')
    canvas.drawString(tx, H - band_h + band_h * 0.31, 'Handover Document')
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica', 13)
    canvas.drawString(tx, H - band_h + band_h * 0.13, 'Powered by BridgeWorks')

    y = H - band_h - 18 * mm
    meta = [
        ('Prepared by',  'Emmanuel Ehigbai / BridgeWorks'),
        ('Prepared for', 'Victor Danmagaji / CEEFM Kft'),
        ('Date',         '2026-06-10'),
        ('Engagement',   'CEEFM Digital Growth -- 16-Week Engagement (CEEFM-PROP-001)'),
        ('Status',       'Engagement concluded'),
    ]
    for label, val in meta:
        canvas.setFont('Helvetica-Bold', 9)
        canvas.setFillColor(NAVY)
        canvas.drawString(tx, y, label + ':')
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(CHARCOAL)
        canvas.drawString(tx + 82, y, val)
        y -= 7 * mm

    canvas.setFillColor(WARM_GRAY)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawCentredString(W / 2, 22, 'BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency')
    canvas.restoreState()


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, BAR, H, fill=1, stroke=0)
    canvas.setFillColor(WARM_GRAY)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawCentredString(W / 2, 22, 'BridgeWorks  ·  office@bridgeworks.agency  ·  bridgeworks.agency')
    pn = canvas.getPageNumber()
    canvas.drawRightString(W - MR, 22, str(pn))
    canvas.restoreState()


# ── Styles ────────────────────────────────────────────────────

def styles():
    def s(name, **kw):
        return ParagraphStyle(name, **kw)
    return {
        'h1': s('h1', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY,
                spaceBefore=14, spaceAfter=6, leading=22),
        'h2': s('h2', fontName='Helvetica-Bold', fontSize=12, textColor=NAVY,
                spaceBefore=10, spaceAfter=4, leading=16),
        'h3': s('h3', fontName='Helvetica-Bold', fontSize=10, textColor=CHARCOAL,
                spaceBefore=7, spaceAfter=3, leading=14),
        'body': s('body', fontName='Helvetica', fontSize=9, textColor=CHARCOAL,
                  spaceBefore=3, spaceAfter=3, leading=13),
        'bold': s('bold', fontName='Helvetica-Bold', fontSize=9, textColor=CHARCOAL,
                  spaceBefore=3, spaceAfter=3, leading=13),
        'note': s('note', fontName='Helvetica-Oblique', fontSize=8.5, textColor=WARM_GRAY,
                  spaceBefore=3, spaceAfter=3, leading=12, leftIndent=10),
        'code': s('code', fontName='Courier', fontSize=8, textColor=CHARCOAL,
                  spaceBefore=2, spaceAfter=2, leading=12, leftIndent=12,
                  backColor=HexColor('#E0D9CE')),
        'caption': s('caption', fontName='Helvetica', fontSize=8, textColor=WARM_GRAY,
                     spaceBefore=2, spaceAfter=2, leading=11),
    }


# ── Table helpers ─────────────────────────────────────────────

def navy_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  NAVY),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  white),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 8.5),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR',     (0, 1), (-1, -1), CHARCOAL),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [IVORY, ROW_ALT]),
        ('GRID',          (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def priority_block(num, title, time_est, detail, S):
    hdr = Table([[f'Priority {num}: {title}', f'Est. time: {time_est}']],
                colWidths=[320, 110])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), NAVY),
        ('TEXTCOLOR',     (0, 0), (-1, -1), white),
        ('FONTNAME',      (0, 0), (0, 0),   'Helvetica-Bold'),
        ('FONTNAME',      (1, 0), (1, 0),   'Helvetica'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('ALIGN',         (1, 0), (1, 0),   'RIGHT'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    body_text = detail.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')
    body = Table([[Paragraph(body_text, S['body'])]], colWidths=[430])
    body.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), ROW_ALT),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID',          (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    return KeepTogether([hdr, body, Spacer(1, 8)])


# ── Score bar flowable ────────────────────────────────────────

class ScoreBar(Flowable):
    def __init__(self, label, score, bar_w=220):
        Flowable.__init__(self)
        self.label = label
        self.score = score
        self.bar_w = bar_w
        self.width = 130 + bar_w
        self.height = 16

    def draw(self):
        c = self.canv
        c.setFont('Helvetica', 8.5)
        c.setFillColor(CHARCOAL)
        c.drawString(0, 3, self.label)
        bx = 130
        c.setFillColor(HexColor('#D8D0C4'))
        c.rect(bx, 2, self.bar_w, 12, fill=1, stroke=0)
        fill = (self.score / 100) * self.bar_w
        c.setFillColor(GOLD)
        c.rect(bx, 2, fill, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawString(bx + fill - 30, 4, f'{self.score}/100')

    def wrap(self, aw, ah):
        return (self.width, self.height + 4)


# ── Story builder ─────────────────────────────────────────────

def build(S):
    story = []

    def rule():
        return HRFlowable(width='100%', thickness=1.5, color=GOLD, spaceAfter=8)

    def h1(t): return Paragraph(t, S['h1'])
    def h2(t): return Paragraph(t, S['h2'])
    def h3(t): return Paragraph(t, S['h3'])
    def p(t):  return Paragraph(t, S['body'])
    def note(t): return Paragraph(t, S['note'])
    def sp(n=6): return Spacer(1, n)

    # ─ Section 1 ─────────────────────────────────────────────
    story += [h1('Section 1: What Was Built'), rule()]

    # 1.1
    story += [h2('1.1  Website -- ceefm.eu'),
              p('Stack: Astro (static site generator), hosted on Hostinger. No CMS. '
                'Pages are .astro files. Source: C:/Users/User/ceefm-astro/'),
              sp(4), p('<b>Pages live:</b>')]
    story.append(navy_table([
        ['URL', 'Lang', 'Purpose'],
        ['ceefm.eu/', 'EN', 'Main homepage'],
        ['ceefm.eu/hu/', 'HU', 'Hungarian homepage'],
        ['ceefm.eu/contact/', 'EN', 'Contact + assessment form'],
        ['ceefm.eu/hu/kapcsolat/', 'HU', 'Hungarian contact'],
        ['ceefm.eu/hospitality/', 'EN', 'Hospitality FM funnel page'],
        ['ceefm.eu/residential/', 'EN', 'Residential FM funnel page'],
        ['ceefm.eu/vendeglatas/', 'HU', 'Vendéglátás funnel page'],
        ['ceefm.eu/lakopark/', 'HU', 'Lakópark funnel page'],
    ], [185, 40, 205]))
    story += [sp(6), p('<b>Technical infrastructure on the site:</b>')]
    story.append(navy_table([
        ['Item', 'Location', 'Status'],
        ['ProfessionalService JSON-LD schema', 'BaseLayout.astro lines 79-155', 'Live'],
        ['robots.txt with AI crawler permissions (13 crawlers)', '/public/robots.txt', 'Live'],
        ['llms.txt (AI-first company summary)', '/public/llms.txt', 'Live'],
        ['Security headers (HSTS, CSP, X-Frame-Options)', '/public/.htaccess', 'Live'],
        ['Bilingual hreflang tags (en/hu)', 'BaseLayout.astro lines 58-60', 'Live'],
        ['Canonical URLs on all pages', 'BaseLayout.astro line 55', 'Live'],
        ['Open Graph + Twitter Card meta tags', 'BaseLayout.astro lines 63-77', 'Live'],
        ['GA4 analytics (G-F2TLLLG2DH)', 'BaseLayout.astro lines 185-189', 'Live'],
        ['Google Consent Mode v2', 'BaseLayout.astro lines 162-182', 'Live'],
        ['Bing Webmaster verification', 'BaseLayout.astro line 54', 'Live'],
        ['Cookie consent banner', 'BaseLayout.astro lines 196-237', 'Live'],
        ['Hungarian legal imprint', 'Footer.astro', 'Live'],
        ['LCP hero image preload (WebP)', 'BaseLayout.astro lines 27-46', 'Live'],
        ['FAQPage JSON-LD schema (homepage)', 'index.astro extraJsonLd prop', 'Live'],
        ['Wikidata entity (Q139592822)', 'sameAs in schema', 'Live'],
        ['IndexNow integration', 'On rebuild/deploy', 'Live'],
        ['Sitemap (all 8 pages)', '/dist/sitemap-0.xml', 'Live'],
    ], [220, 150, 60]))
    story += [sp(4),
              note('To deploy changes: edit .astro files, run npm run build in ceefm-astro/, '
                   'upload the dist/ folder to Hostinger via FTP or the Hostinger File Manager.')]

    # 1.2
    story += [sp(8), h2('1.2  GEO Score Progression'),
              p('The site started the engagement at 16/100 (Critical). '
                'It closes at 78/100 (Good) -- a 62-point improvement over 16 weeks.'), sp(4)]
    geo_tbl = navy_table([
        ['Audit Date', 'Score', 'Band', 'Key Driver'],
        ['March 2026',          '16/100', 'Critical',   'Baseline before engagement'],
        ['April 3',             '29/100', 'Critical',   'Discovery audit, no fixes yet'],
        ['April 22',            '47/100', 'Poor',       'llms.txt, hreflang, partial schema'],
        ['April 30 (morning)',  '61/100', 'Fair',       'Full schema, legal imprint, security headers'],
        ['April 30 (evening)',  '74/100', 'Fair (top)', 'Wikidata, IndexNow, Bing, GBP claim, LinkedIn'],
        ['June 10',             '77/100', 'Good',       'Funnel pages, TikTok launch'],
        ['June 11 (final)',      '78/100', 'Good',       'FAQPage schema, sitemap complete, llms.txt corrected'],
    ], [95, 55, 70, 210])
    geo_tbl._cellvalues  # access to apply extra style
    geo_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0),  NAVY),
        ('TEXTCOLOR',    (0, 0), (-1, 0),  white),
        ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1, -1), 8.5),
        ('FONTNAME',     (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR',    (0, 1), (-1, -1), CHARCOAL),
        ('ROWBACKGROUNDS',(0,1), (-1, -1), [IVORY, ROW_ALT]),
        ('FONTNAME',     (0, 7), (-1, 7),  'Helvetica-Bold'),
        ('TEXTCOLOR',    (1, 7), (2, 7),   GOLD),
        ('GRID',         (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(geo_tbl)
    story += [sp(6), p('<b>Final category scores (June 11):</b>'), sp(3)]
    for label, score in [
        ('AI Citability (25%)', 78),
        ('Brand Authority (20%)', 71),
        ('Content E-E-A-T (20%)', 72),
        ('Technical GEO (15%)', 92),
        ('Schema & Structured Data (10%)', 83),
        ('Platform Optimization (10%)', 76),
    ]:
        story += [ScoreBar(label, score), sp(2)]

    # 1.3
    story += [sp(8), h2('1.3  Content Delivered')]
    for title, desc in [
        ('April 2026 content calendar',
         '12 strategic posts + 4 Friday amplification posts = 16 total. EN + HU versions. '
         'Source: content/april-calendar.md'),
        ('May 2026 content calendar',
         '12 strategic posts + 4 Friday amplification posts = 16 total. EN + HU versions. '
         'Weeks 6-9 (May 5-29). Source: content/may-calendar.md'),
        ('Monthly reports delivered',
         'April Executive Report, April Delivery Appendix, April Performance Analytics, '
         'May Action Plan -- all as MD and PDF.'),
        ('GEO audit reports delivered',
         'Initial, April 30 morning, April 30 evening, June 10 final, June 11 closing audit.'),
    ]:
        story.append(p(f'<b>{title}:</b> {desc}'))

    # 1.4
    story += [sp(8), h2('1.4  Cold Email Infrastructure'),
              p('95 Budapest property management companies scored and tiered into Tier 1 (33), '
                'Tier 2 (37), Tier 3 (25). Personalised EN + HU templates. '
                '51 referral partner contacts identified. '
                'Script: C:/Users/User/Projects/02-Clients/prospects/send_ceefm_outreach.py'),
              sp(4)]
    story.append(navy_table([
        ['Company', 'Email', 'Status', 'Notes'],
        ['Budapest Residence', 'info@bpresidence.hu', 'Sent + FU', ''],
        ['Managerent Kft', 'info@managerent.hu', 'Sent + FU', ''],
        ['Florin Apart Hotel', 'info@florinaparthotel.hu', 'Sent + FU', ''],
        ['BQA Short Rent Kft', 'may@bqa-budapest.com', 'Sent', ''],
        ['Crystal Property Mgmt', 'eszter.solymar@crystalproperty.hu', 'Sent', ''],
        ['Pyramidon Property', 'pergel.laszlo@pyramidon.hu', 'Sent', ''],
        ['Tower International', 'info@towerbudapest.com', 'Sent', ''],
        ['GPM Home Management', 'reservation@gpm.hu', 'Sent', ''],
        ['Gellerico Apartments', 'info@gellerico.com', 'Bounced', 'Find via gellerico.com'],
        ['Tarsashaz Management', 'iroda@tarsashazmanagement.hu', 'Bounced', 'LinkedIn: Gabor Gerbner'],
        ['Walk Inn Apartments', 'info@walkinn.hu', 'Bounced', 'LinkedIn: Reka Michaletzky'],
        ['Vagabond Group', 'info@vagabondhospitality.com', 'Bounced', 'LinkedIn: William Hardy'],
        ['Budapest Apartments', 'office@budapestapartments.com', 'Bounced', 'Drop -- no alternative'],
    ], [120, 130, 55, 125]))
    story += [sp(4),
              note('Delivered: 11.  Bounced: 5 (4 with LinkedIn DM alternatives identified).  '
                   'Replies: 0 as of June 10. B2B cold outreach window is 4-6 weeks -- '
                   'first signal window closes late June.'),
              p('84 Tier 1/2 prospects remain in the scored database. '
                'Full list: deliverables/PROSPECT-LIST-WAVE-1.csv')]

    # 1.5
    story += [sp(8), h2('1.5  LinkedIn Company Page'),
              p('Optimised and posting 3x/week (Tue/Wed/Thu) since April 2026. '
                'Followers: 146 at end of April. Top post: April 1 company introduction. '
                'May calendar ran through May 29. June posts not drafted.'),
              note('Action: Continue 3x/week cadence. Follow May calendar format. '
                   'All posts need EN and HU versions.')]

    # 1.6
    story += [sp(8), h2('1.6  TikTok'),
              p('TikTok Business account created. One video uploaded: before-and-after room clean, '
                'no voiceover, two clips.'),
              note('Action: Post 2-3 videos per month. Before-and-after work, behind-the-scenes maintenance, '
                   'quick tips for property managers. Active TikTok profiles are AI entity credibility signals.')]

    # 1.7
    story += [sp(8), h2('1.7  Other Deliverables'), p('All in deliverables/:'), sp(4)]
    story.append(navy_table([
        ['File', 'What It Is'],
        ['APARTHOTEL-OPERATING-STANDARD-V1-DRAFT', '14-category operating framework. Publish as PDF or site page to generate leads.'],
        ['COLD-OUTREACH-SEQUENCE-EN-HU.md', '3-email sequence templates for future outreach waves'],
        ['GBP-BUSINESS-DESCRIPTION-EN-HU.md', 'Ready-to-paste Google Business Profile description in EN and HU'],
        ['GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md', 'Full Google Ads plan using the 120,000 HUF credit'],
        ['GOOGLE-ADS-RSA-COPY-EN-HU.md', 'Responsive Search Ad copy in EN and HU, ready to paste'],
        ['LINKEDIN-COMPANY-PAGE-OPTIMISATION.md', 'LinkedIn page setup and optimisation guide'],
        ['SEO-KEYWORD-RESEARCH-TOP-20.md', 'Top 20 search terms for Budapest facility management'],
        ['VIDEO-SCRIPT-GOOGLE-ADS-EN-HU.md', 'Video ad scripts for the 12 Remotion video assets'],
        ['outreach/CEEFM-full-outreach-playbook', 'Full operating guide for the outreach system'],
    ], [200, 230]))

    # ─ Section 2 ─────────────────────────────────────────────
    story += [PageBreak(), h1('Section 2: What Is Live and How to Maintain It'), rule()]

    story += [h2('2.1  Website')]
    for label, desc in [
        ('Host', 'Hostinger. Victor has login credentials.'),
        ('Text changes', 'Edit ceefm-astro/src/data/content.ts. Run npm run build. Upload dist/ to Hostinger.'),
        ('Add a page', 'Create .astro file in ceefm-astro/src/pages/. Import BaseLayout. '
                       'Add URL to the sitemap config. Rebuild and upload.'),
        ('Analytics', 'GA4 at analytics.google.com. Property ID: G-F2TLLLG2DH.'),
        ('Do not touch', 'BaseLayout.astro schema block -- a mistake breaks structured data sitewide. '
                         '.htaccess security headers -- stable, no changes needed.'),
    ]:
        story.append(p(f'<b>{label}:</b> {desc}'))

    story += [sp(8), h2('2.2  LinkedIn')]
    for label, desc in [
        ('Cadence', '3 posts per week. Tuesday / Wednesday / Thursday. 9:00 AM CEST.'),
        ('Format', 'EN version and HU version per post. Under 1,300 characters. '
                   'Hashtags go as the first comment after publishing.'),
        ('Best-performing types', 'Industry insight with specific numbers. '
                                  'Behind-the-scenes operational detail. '
                                  'Before-and-after or quality-check stories.'),
        ('What not to post', 'Generic FM statements, vague brand content, '
                             'anything without a specific claim or story.'),
    ]:
        story.append(p(f'<b>{label}:</b> {desc}'))

    story += [sp(8), h2('2.3  Cold Email System'),
              p('Script: C:/Users/User/Projects/02-Clients/prospects/send_ceefm_outreach.py. '
                'Uses Gmail App Password. Full guide: '
                'deliverables/outreach/CEEFM-full-outreach-playbook-2026-05-15.md'), sp(4)]
    for i, step in enumerate([
        'Pick next 10-15 companies from CEEFM-client-outreach-queue-2026-05-15.csv (Tier 1 first, then Tier 2).',
        'Confirm email addresses are correct.',
        'Run the script in dry-run mode first to preview output.',
        'Confirm each send interactively.',
        'Watch office@ceefm.eu through late June for first replies (4-6 week window).',
    ], 1):
        story.append(p(f'{i}.  {step}'))

    # ─ Section 3 ─────────────────────────────────────────────
    story += [PageBreak(), h1('Section 3: Priority Action List'), rule(),
              p('Listed in priority order. Items 1-3 are quick fixes under 2 hours combined '
                'that will move the GEO score from 78 to 81+.'), sp(8)]

    priorities = [
        ('1', 'Complete Google Business Profile Verification', '10 minutes',
         'The GBP postcard was mailed to the Ujlengyel registered address in early May.\n\n'
         '1. Go to business.google.com\n'
         '2. Log in with the account used to create the CEEFM GBP listing\n'
         '3. Enter the postcard verification code\n'
         '4. Confirm business details are accurate\n'
         '5. Add the resulting Maps URL to the sameAs array in BaseLayout.astro (lines 128-131)\n\n'
         'Impact: puts CEEFM on Google Maps, enables local knowledge panel, adds the critical '
         'entity signal AI Overview systems use for local queries. GEO score: +3 to +4.'),

        ('2', 'Fix Homepage Stat: 10+ Years to 16 Years', '5 minutes',
         'The company was founded in 2010. That is 16 years as of 2026. '
         'The hero stat still reads "10+ Years Experience". '
         'The llms.txt correctly reads "16 years of operational experience".\n\n'
         'Edit the hero component: change to "16 Years" or "Since 2010".'),

        ('3', 'Fix Privacy Policy 404', '2-3 hours',
         'The contact form links to a privacy policy page that returns 404. '
         'This is a GDPR compliance issue for a company collecting personal data via web form.\n\n'
         'Create /privacy-policy/ (English) and /adatvedelem/ (Hungarian) pages. '
         'A solicitor or GDPR template service can provide the required text.'),

        ('4', 'Send LinkedIn DMs for Bounced Contacts', '30 min (Victor\'s action)',
         'Three companies bounced on email. LinkedIn DMs are the backup channel. '
         'Victor sends these from his personal LinkedIn. Message copy is in the outreach playbook.\n\n'
         'Gabor Gerbner (Tarsashaz Management): hu.linkedin.com/in/gabor-gerbner-18996775\n'
         'Reka Michaletzky (Walk Inn Apartments): hu.linkedin.com/in/reka-michaletzky\n'
         'William Hardy (Vagabond Group): linkedin.com/in/william-hardy-86518a50'),

        ('5', 'Continue Cold Outreach', 'Ongoing',
         '84 scored companies remain. Send 10-15 per wave. '
         'Space sends 1-2 weeks apart. '
         'Follow with one follow-up email 5-7 days after each initial send.'),

        ('6', 'Add Meta Descriptions to Four Funnel Pages', '30 minutes',
         '/hospitality/, /residential/, /lakopark/, /vendeglatas/ have no meta description. '
         'Add a description prop to each page file in src/pages/. '
         '130-155 characters each, with Budapest and a specific service claim.'),

        ('7', 'Expand Funnel Page Content', '4-6 hours',
         'Hospitality page: ~370 words. Residential page: ~670 words. '
         'Each needs 800+ words with structured proof points for AI citation. '
         'Add a 3-5 question FAQ section per page with FAQPage schema.'),

        ('8', 'Publish Aparthotel Operating Standard', '2-3 hours',
         'The 14-category framework is drafted at '
         'deliverables/APARTHOTEL-OPERATING-STANDARD-V1-DRAFT-2026-05-18.md. '
         'Convert to PDF and post as a site page (e.g. /aparthotel-standard) '
         'with a contact form. Generates qualified leads from Budapest aparthotel operators.'),

        ('9', 'Create /about Page', '3-4 hours',
         'A dedicated /about URL significantly improves E-E-A-T signals. '
         'Include: Victor\'s name and professional background, founding story, '
         'Limehome relationship, 8-person team count, industry memberships.'),

        ('10', 'Activate Google Ads', 'After GBP verification',
         'The 120,000 HUF Google Ads credit is pre-loaded and ready. '
         'Campaign plan: deliverables/GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md. '
         'RSA copy: deliverables/GOOGLE-ADS-RSA-COPY-EN-HU.md.\n\n'
         'Activate after GBP is verified so ad traffic lands on a site with a verified Maps listing.'),
    ]

    for num, title, time_est, detail in priorities:
        story.append(priority_block(num, title, time_est, detail, S))

    # ─ Section 4 ─────────────────────────────────────────────
    story += [PageBreak(), h1('Section 4: File Index'), rule(),
              p('All engagement files: C:/Users/User/Projects/bridgeworks-workspace/clients/ceefm/'),
              sp(4)]
    story.append(navy_table([
        ['Path', 'Contents'],
        ['CEEFM-HANDOVER-2026-06-10.md', 'This document'],
        ['content/april-calendar.md', 'April 2026 content (16 posts EN + HU)'],
        ['content/may-calendar.md', 'May 2026 content (16 posts EN + HU)'],
        ['content/images/', 'All generated post images'],
        ['deliverables/APARTHOTEL-OPERATING-STANDARD-V1-DRAFT', '14-category operating framework'],
        ['deliverables/COLD-OUTREACH-SEQUENCE-EN-HU.md', '3-email sequence templates'],
        ['deliverables/GBP-BUSINESS-DESCRIPTION-EN-HU.md', 'Ready-to-paste GBP description EN + HU'],
        ['deliverables/GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md', 'Google Ads campaign plan'],
        ['deliverables/GOOGLE-ADS-RSA-COPY-EN-HU.md', 'Responsive Search Ad copy EN + HU'],
        ['deliverables/LINKEDIN-COMPANY-PAGE-OPTIMISATION.md', 'LinkedIn page setup guide'],
        ['deliverables/PROSPECT-LIST-WAVE-1.csv', '95 scored prospects'],
        ['deliverables/SEO-KEYWORD-RESEARCH-TOP-20.md', 'Top 20 search terms'],
        ['deliverables/outreach/CEEFM-full-outreach-playbook', 'Full outreach operating guide'],
        ['deliverables/outreach/CEEFM-client-outreach-queue.csv', 'Outreach queue (84 remaining)'],
        ['invoices/E-EO-2026-1_Setup-fee.pdf', 'Invoice: Setup fee'],
        ['invoices/E-EO-2026-2_April-retainer.pdf', 'Invoice: Month 1 retainer'],
        ['reports/GEO-AUDIT-REPORT-2026-06-10.md', 'June 10 GEO audit'],
        ['reports/GEO-AUDIT-REPORT-2026-06-11.md', 'June 11 final GEO audit (78/100)'],
        ['reports/MARKETING-AUDIT-2026-06-11.md', 'Full marketing audit (49/100)'],
        ['reports/CEEFM-April-2026-Executive-Report.md', 'April executive report'],
        ['reports/CEEFM-April-2026-Delivery-Appendix.md', 'April delivery appendix'],
        ['reports/CEEFM-April-2026-Performance-Analytics-Appendix.md', 'April analytics appendix'],
        ['reports/CEEFM-May-2026-Action-Plan.md', 'May action plan'],
    ], [240, 190]))
    story += [sp(4),
              Paragraph('Website source code: C:/Users/User/ceefm-astro/', S['caption']),
              Paragraph('Cold email scripts: C:/Users/User/Projects/02-Clients/prospects/', S['caption'])]

    # ─ Summary ───────────────────────────────────────────────
    story += [PageBreak(), h1('Summary'), rule(),
              p('The engagement delivered a 62-point GEO score improvement (16 to 78, Critical to Good), '
                'a bilingual Astro website with comprehensive AI-visibility infrastructure, '
                'two months of LinkedIn content, a scored prospect database of 95 companies, '
                'a live cold email pipeline with 11 emails delivered, TikTok account launch, '
                'and a 14-category Aparthotel Operating Standard framework.'), sp(8)]

    sum_tbl = navy_table([
        ['Metric', 'Result'],
        ['GEO Score at start', '16/100 (Critical)'],
        ['GEO Score at close', '78/100 (Good)'],
        ['Score improvement', '+62 points over 16 weeks'],
        ['Website pages live', '8 (EN + HU)'],
        ['LinkedIn posts delivered', '32 (April + May calendars)'],
        ['Prospects scored', '95 companies'],
        ['Cold emails delivered', '11'],
        ['Prospects remaining in queue', '84'],
        ['Deliverable documents', '13+'],
    ], [220, 210])
    sum_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  NAVY),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  white),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 8.5),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR',     (0, 1), (-1, -1), CHARCOAL),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [IVORY, ROW_ALT]),
        ('FONTNAME',      (0, 3), (-1, 3),  'Helvetica-Bold'),
        ('TEXTCOLOR',     (1, 3), (1, 3),   GOLD),
        ('GRID',          (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sum_tbl)
    story += [sp(10),
              p('The remaining path to 81+ GEO is three quick fixes: GBP verification, '
                'fixing the "10+ Years" homepage stat, and the privacy policy page. '
                'Combined effort: under 3 hours.'),
              sp(4), p('BridgeWorks remains available for future engagements.'), sp(14)]

    closing = Table([['office@bridgeworks.agency  ·  bridgeworks.agency']], colWidths=[430])
    closing.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), NAVY),
        ('TEXTCOLOR',     (0, 0), (-1, -1), GOLD),
        ('FONTNAME',      (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 10),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(closing)

    return story


# ── Main ──────────────────────────────────────────────────────

def main():
    out = r'C:\Users\User\Projects\bridgeworks-workspace\clients\ceefm\reports\CEEFM-HANDOVER-2026-06-10.pdf'

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=ML + BAR, rightMargin=MR,
        topMargin=MT, bottomMargin=MB + 15,
    )

    frame = Frame(ML + BAR, MB + 15, FRAME_W, H - MT - MB - 15, id='body')

    doc.addPageTemplates([
        PageTemplate(id='Cover',   frames=[frame], onPage=on_cover),
        PageTemplate(id='Content', frames=[frame], onPage=on_page),
    ])

    S = styles()
    story = [NextPageTemplate('Content'), PageBreak()]  # page 1 = cover
    story += build(S)

    doc.build(story)
    print(f'Done: {out}')


if __name__ == '__main__':
    main()
