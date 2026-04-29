"""Generate the Oliviks Service Agreement PDF with BridgeWorks branding."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, Image as RLImage,
)
from reportlab.platypus.flowables import HRFlowable
import os

NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
WHITE = HexColor("#FFFFFF")

W, H = A4

CLIENT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\oliviks"
# Square lockup (bridge icon + BRIDGEWORKS wordmark). The files named "logo-primary"
# are wide banner composites — these "icon" files are the proper brand lockup.
LOGO_DARK = r"C:\Users\ELITEX21012G2\brand-assets\bridgeworks\logos\bridgeworks-icon-dark-800px.png"
LOGO_LIGHT = r"C:\Users\ELITEX21012G2\brand-assets\bridgeworks\logos\bridgeworks-icon-light-800px.png"
SIGNATURE = r"C:\Users\ELITEX21012G2\brand-assets\bridgeworks\signatures\emmanuel-signature.png"

for _p in (LOGO_DARK, LOGO_LIGHT):
    if not os.path.exists(_p):
        raise FileNotFoundError(f"Logo not found: {_p}")


def make_styles():
    s = {}
    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=16, leading=20,
        textColor=NAVY, spaceBefore=14, spaceAfter=6,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=NAVY, spaceBefore=12, spaceAfter=4,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
        textColor=NAVY, spaceBefore=8, spaceAfter=3,
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=CHARCOAL, spaceAfter=5,
    )
    s["body_bold"] = ParagraphStyle(
        "body_bold", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        textColor=CHARCOAL, spaceAfter=5,
    )
    s["small"] = ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8, leading=11,
        textColor=WARM_GRAY, spaceAfter=4,
    )
    s["small_italic"] = ParagraphStyle(
        "small_italic", fontName="Helvetica-Oblique", fontSize=8, leading=11,
        textColor=WARM_GRAY, spaceAfter=4,
    )
    s["table_head"] = ParagraphStyle(
        "table_head", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=WHITE,
    )
    s["table_cell"] = ParagraphStyle(
        "table_cell", fontName="Helvetica", fontSize=9, leading=12, textColor=CHARCOAL,
    )
    s["table_cell_bold"] = ParagraphStyle(
        "table_cell_bold", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=NAVY,
    )
    s["party"] = ParagraphStyle(
        "party", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=CHARCOAL, spaceAfter=2,
    )
    return s


STYLES = make_styles()


def P(text, style="body"):
    return Paragraph(text, STYLES[style])


def _draw_branded_chrome(c, page_num):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)
    # Square lockup, top right
    c.drawImage(LOGO_LIGHT, W - 55 - 30, H - 60, width=55, height=55, mask="auto")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawString(40, 22, "BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency")
    c.drawRightString(W - 30, 22, f"Page {page_num}")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(40, 35, W - 30, 35)


def _on_body_page(c, doc):
    _draw_branded_chrome(c, doc.page)


def _on_cover_page(c, doc):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, H, fill=1, stroke=0)

    band_h = H * 0.36
    band_y = H - band_h
    c.setFillColor(NAVY)
    c.rect(0, band_y, W, band_h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, band_y, W, band_y)

    # Square lockup, top right of navy band
    c.drawImage(LOGO_DARK, W - 130 - 30, H - 145, width=130, height=130, mask="auto")

    y_title = H - 95
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(40, y_title, "Service")
    y_title -= 36
    c.setFont("Helvetica-Bold", 30)
    c.drawString(40, y_title, "Agreement")
    y_title -= 32

    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawString(40, y_title, "BridgeWorks  ·  Oliviks KFT")

    y = band_y - 50
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Between:")
    y -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "BridgeWorks (Emmanuel Olayinka Ehigbai EV)")
    y -= 16
    c.setFont("Helvetica", 10)
    c.setFillColor(WARM_GRAY)
    for line in [
        "1149 Budapest, Várna utca 24, Hungary",
        "Tax number: 91048817-1-42",
        "office@bridgeworks.agency",
    ]:
        c.drawString(40, y, line)
        y -= 14

    y -= 10
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "And:")
    y -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Oliviks KFT")
    y -= 16
    c.setFont("Helvetica", 10)
    c.setFillColor(WARM_GRAY)
    for line in [
        "Registered seat: 1033 Budapest, Miklós u. 13, Hungary",
        "Tax number (adószám): 32383177241",
        "Represented by: Aese Agaigbe",
    ]:
        c.drawString(40, y, line)
        y -= 14

    y -= 14
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Date of Agreement: 29 April 2026")

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


def _section_divider():
    return HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceBefore=10, spaceAfter=10)


def build_contract():
    output = os.path.join(CLIENT_DIR, "CONTRACT-OLIVIKS-2026-04-29.pdf")

    doc = BaseDocTemplate(
        output, pagesize=A4, leftMargin=40, rightMargin=30, topMargin=50, bottomMargin=42,
        title="Service Agreement — Oliviks KFT",
        author="Emmanuel Ehigbai / BridgeWorks",
    )
    cover_frame = Frame(40, 42, W - 70, H - 84, id="cover", showBoundary=0)
    body_frame = Frame(40, 42, W - 70, H - 92, id="body", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=_on_cover_page),
        PageTemplate(id="Body", frames=[body_frame], onPage=_on_body_page),
    ])

    s = []
    s.append(NextPageTemplate("Body"))
    s.append(Spacer(1, 1))
    s.append(PageBreak())

    # ---- Parties ----
    s.append(P("Parties", "h1"))
    s.append(P("This Service Agreement (the &quot;Agreement&quot;) is entered into on 29 April 2026 between:"))
    s.append(P("Service Provider:", "h3"))
    s.append(P("Emmanuel Olayinka Ehigbai, individual entrepreneur (egyéni vállalkozó), trading as <b>BridgeWorks</b>", "party"))
    s.append(P("Registered office: 1149 Budapest, Várna utca 24, Hungary", "party"))
    s.append(P("Tax number (adószám): 91048817-1-42", "party"))
    s.append(P("EV registration number: 60424989", "party"))
    s.append(P("Bank: OTP Bank Nyrt., 11773030-01082234", "party"))
    s.append(P("Email: office@bridgeworks.agency", "party"))
    s.append(P("(&quot;BridgeWorks&quot;)", "party"))
    s.append(Spacer(1, 6))
    s.append(P("Client:", "h3"))
    s.append(P("<b>Oliviks KFT</b>", "party"))
    s.append(P("Registered seat: 1033 Budapest, Miklós u. 13, Hungary", "party"))
    s.append(P("Tax number (adószám): 32383177241", "party"))
    s.append(P("Represented by: Aese Agaigbe", "party"))
    s.append(P("Email: olivikskitchen@gmail.com", "party"))
    s.append(P("(&quot;Client&quot;)", "party"))
    s.append(Spacer(1, 4))
    s.append(P("Each a &quot;Party&quot; and together the &quot;Parties&quot;."))
    s.append(_section_divider())

    # ---- 1. Background ----
    s.append(P("1. Background", "h2"))
    s.append(P("The Parties have agreed that BridgeWorks will perform a one-time digital foundation rebuild for Oliviks Kitchen as defined in the Digital Growth Proposal dated 28 April 2026 (the &quot;Proposal&quot;). The Client has selected the <b>Foundation only</b> scope. The Proposal is attached as <b>Annex A</b> and forms part of this Agreement."))

    # ---- 2. Scope ----
    s.append(P("2. Scope of Services", "h2"))
    s.append(P("BridgeWorks will deliver the Foundation package, consisting of three workstreams."))
    s.append(P("2.1 Website Upgrade (oliviks.com)", "h3"))
    s.append(P("Rebuild and rewrite of homepage, About page, Contact page, and menu pages. Removal of duplicate pages and the default WordPress sample page. Real Google reviews embedded. Press logos surfaced (Origo, We Love Budapest, WMN). Wolt and Foodora badges added. Dish descriptions written for all 23 menu items. Meta descriptions, Open Graph tags, alt text, schema markup, page-speed pass, and mobile QA on iOS and Android."))
    s.append(P("2.2 Google Business Profile Optimization", "h3"))
    s.append(P("Secondary categories, attributes audit, bilingual business description (EN + HU), in-profile menu upload (23 dishes with photos and prices), photo audit and upload, Q&amp;A pre-population, four launch posts, review-response templates and backfill, NAP-consistency cleanup across Wolt, Foodora, Facebook, TripAdvisor, and Wanderlog, schema markup on oliviks.com, and a one-page handover document."))
    s.append(P("2.3 Email and WhatsApp Infrastructure", "h3"))
    s.append(P("Email provider account (MailerLite or Beehiiv free tier, owned by Client), email-capture popup on oliviks.com, three-email welcome sequence, weekly specials template (EN + HU), branded order-receipt email, GDPR compliance (consent checkbox, double opt-in, unsubscribe, privacy-policy update), WhatsApp broadcast list with website and counter QR opt-in, WooCommerce-to-list integration, and a one-page handover document."))
    s.append(P("The full deliverable list is set out in section &quot;Part A: Foundation&quot; of the Proposal (Annex A)."))

    # ---- 3. Out of Scope ----
    s.append(P("3. Out of Scope", "h2"))
    s.append(P("The following are not included and, if requested, will be quoted separately:"))
    for item in [
        "Ongoing operation of the systems built (covered in the optional Growth Retainer in the Proposal).",
        "Full theme migration off Elementor.",
        "E-commerce restructure (changing self-pickup to full delivery).",
        "Full Hungarian translation of every website page.",
        "Paid advertising spend or campaign management.",
        "Photo or video production beyond what the Client supplies.",
        "WhatsApp Business API integration.",
        "Email-provider monthly fees if the Client exceeds the free-tier subscriber limit.",
    ]:
        s.append(P(f"&bull; {item}"))
    s.append(P("3.1 Change Control", "h3"))
    s.append(P("Anything not listed in Annex A Part A or in section 2 is a Change Request. Change Requests are quoted separately and signed by both Parties before work begins."))

    s.append(PageBreak())

    # ---- 4. Timeline ----
    s.append(P("4. Timeline", "h2"))
    s.append(P("The engagement begins on the <b>kickoff date</b>, defined as the later of (a) the date BridgeWorks receives the first payment under section 5, and (b) the date the Client provides the access listed in section 6."))
    tl_rows = [
        [P("Workstream", "table_head"), P("Duration from kickoff", "table_head")],
        [P("Google Business Profile Optimization", "table_cell"), P("2 weeks", "table_cell")],
        [P("Email and WhatsApp Infrastructure", "table_cell"), P("2 weeks", "table_cell")],
        [P("Website Upgrade", "table_cell"), P("3 weeks", "table_cell")],
    ]
    s.append(_styled_table(tl_rows, [310, 165]))
    s.append(Spacer(1, 6))
    s.append(P("Final handover occurs at the end of week 3 from kickoff. Handover means the rebuilt website is live on oliviks.com, the Google Business Profile changes are published, and the email and WhatsApp systems are operational with a one-page handover document delivered for each."))
    s.append(P("Delays caused by the Client (late provision of access, photos, approvals, or feedback) extend each milestone day-for-day."))
    s.append(P("4.1 Revisions, Acceptance, and Defects", "h3"))
    s.append(P("Each workstream includes two rounds of revisions per deliverable. Further rounds are quoted at 15,000 HUF/hour and signed in writing before work begins."))
    s.append(P("The Client has 5 working days from BridgeWorks' written handover notice to submit specific written objections referencing deliverables in Annex A. Silence past 5 working days constitutes deemed acceptance, and payment 2 is invoiced immediately."))
    s.append(P("BridgeWorks will fix in-scope defects (broken pages, schema errors, opt-in failures, NAP inconsistencies) reported in writing within 14 days of handover at no additional charge. Out-of-scope changes after handover are quoted separately."))

    # ---- 5. Fees ----
    s.append(P("5. Fees and Payment", "h2"))
    s.append(P("5.1 Total fee", "h3"))
    s.append(P("<b>272,611 HUF</b>, fixed, one-time. No recurring fees under this Agreement."))
    s.append(P("5.2 Schedule", "h3"))
    pay_rows = [
        [P("When", "table_head"), P("Amount (HUF)", "table_head")],
        [P("On signing of this Agreement", "table_cell"), P("136,306", "table_cell")],
        [P("On final handover (end of week 3 from kickoff)", "table_cell"), P("136,305", "table_cell")],
        [P("<b>Total</b>", "table_cell_bold"), P("<b>272,611</b>", "table_cell_bold")],
    ]
    s.append(_styled_table(pay_rows, [310, 165]))
    s.append(Spacer(1, 6))
    s.append(P("5.3 Invoicing", "h3"))
    s.append(P("Invoices are issued by BridgeWorks via szamlazz.hu under Hungarian VAT exemption (Áfa törvény 188. §, alanyi adómentes — AAM). Currency: HUF. Payment method: bank transfer to the account stated above. Each invoice is payable within <b>8 days</b> of issue. Each successful invoice is automatically submitted to NAV."))
    s.append(P("5.4 Late payment", "h3"))
    s.append(P("If an invoice is not paid by its due date, BridgeWorks may suspend work after written notice. Statutory late-payment interest under Hungarian law applies. Work resumes within 2 working days of payment being received."))

    # ---- 6. Client Responsibilities ----
    s.append(P("6. Client Responsibilities", "h2"))
    s.append(P("The Client will provide, within 5 working days of signing:"))
    for item in [
        "WordPress admin access to oliviks.com.",
        "Manager-level access to the Oliviks Google Business Profile.",
        "30 to 50 production-quality photos (kitchen, food, team, exterior, interior), or written confirmation that BridgeWorks should source from existing assets.",
        "A nominated business WhatsApp number, or willingness to set one up.",
        "One first-subscriber incentive (e.g. &quot;Free puff puff with first order&quot;).",
        "Approval on copy drafts within 3 working days of receipt.",
        "A single point of contact authorised to give approvals on the Client's behalf.",
    ]:
        s.append(P(f"&bull; {item}"))
    s.append(P("The Client confirms that <b>Rákóczi tér 9, 1084 Budapest</b> is the public-facing kitchen address and that all platform listings (Wolt, Foodora, Facebook, TripAdvisor, Wanderlog) will be aligned to this address."))

    s.append(PageBreak())

    # ---- 7. IP ----
    s.append(P("7. Intellectual Property", "h2"))
    s.append(P("7.1 On full payment of all amounts due under this Agreement, all final deliverables produced for the Client (website copy, dish descriptions, profile content, email templates, WhatsApp templates, handover documents) become the Client's property. The Client may use, modify, and distribute them without further permission or fee."))
    s.append(P("7.2 BridgeWorks retains ownership of any underlying tools, templates, scripts, frameworks, or methodologies used to produce the deliverables. BridgeWorks grants the Client a perpetual, royalty-free licence to continue using the deliverables in their final form."))
    s.append(P("7.3 Third-party software (WordPress, Elementor, MailerLite/Beehiiv, plugins) remains owned by its respective licensors. The Client is responsible for any third-party licence fees beyond the free tiers in use at handover."))
    s.append(P("7.4 BridgeWorks may reference the engagement and use Oliviks Kitchen's name and logo as a portfolio case study, unless the Client requests otherwise in writing."))

    # ---- 8. Confidentiality ----
    s.append(P("8. Confidentiality", "h2"))
    s.append(P("8.1 Each Party will keep the other's non-public information confidential and use it only for the purposes of this Agreement. This obligation continues for 2 years after termination."))
    s.append(P("8.2 BridgeWorks may engage subcontractors and remains fully responsible for their work, including obligations under sections 8 (Confidentiality) and 9 (Data Protection)."))

    # ---- 9. Data Protection ----
    s.append(P("9. Data Protection", "h2"))
    s.append(P("BridgeWorks acts as a data processor for any personal data accessed during the engagement (subscriber emails, WhatsApp contacts, Google review responses). Processing follows GDPR. The Client remains the data controller. Either Party may request a separate Data Processing Agreement and BridgeWorks will execute one at no charge."))

    # ---- 10. Warranties ----
    s.append(P("10. Warranties and Liability", "h2"))
    s.append(P("10.1 BridgeWorks warrants that the services will be performed with reasonable skill and care."))
    s.append(P("10.2 BridgeWorks does not guarantee specific business outcomes, including search ranking position, traffic volume, conversion rate, or revenue uplift."))
    s.append(P("10.3 Each Party's total liability under this Agreement is limited to the total fees paid by the Client under section 5. Neither Party is liable for indirect, consequential, or loss-of-profit damages."))
    s.append(P("10.4 Section 10.3 does not apply to damages caused intentionally or by gross negligence (szándékosság vagy súlyos gondatlanság), or to harm caused to life, bodily integrity, or health."))

    # ---- 11. Term and Termination ----
    s.append(P("11. Term and Termination", "h2"))
    s.append(P("11.1 This Agreement commences on signing and ends on final handover and full payment."))
    s.append(P("11.2 Either Party may terminate for material breach with 7 days' written notice if the breach is not cured within that period."))
    s.append(P("11.3 If the Client terminates without cause before final handover, the Client pays for work performed up to the termination date, calculated as a pro-rata percentage of the total fee against the milestones reached. The first payment under section 5 is non-refundable."))
    s.append(P("11.4 If BridgeWorks terminates without cause, BridgeWorks refunds any amounts paid for work not yet performed and hands over all work-in-progress to the Client."))

    # ---- 12. General ----
    s.append(P("12. General", "h2"))
    s.append(P("12.1 <b>Governing law:</b> Hungarian law."))
    s.append(P("12.2 <b>Disputes:</b> The Parties will first attempt to resolve any dispute by good-faith discussion. Unresolved disputes fall under the jurisdiction of the competent Hungarian courts of Budapest."))
    s.append(P("12.3 <b>Entire Agreement:</b> This document and Annex A (the Proposal) are the entire agreement between the Parties on this subject and supersede prior discussions."))
    s.append(P("12.4 <b>Amendments:</b> Any change to this Agreement must be in writing and signed by both Parties. Email confirmation by both Parties' authorised representatives counts as written."))
    s.append(P("12.5 <b>Notices:</b> All formal notices go to the email addresses stated above."))
    s.append(P("12.6 <b>Counterparts and electronic signature:</b> This Agreement may be signed in counterparts and by electronic signature. Scanned signatures and PDFs exchanged by email are valid and binding."))
    s.append(P("12.7 <b>Force majeure:</b> Neither Party is liable for delay or failure caused by events outside reasonable control, including pandemics, infrastructure outages, or third-party platform shutdowns. The affected Party will notify the other within 5 working days and propose mitigation."))

    s.append(PageBreak())

    # ---- 13. Acceptance ----
    s.append(P("13. Acceptance", "h2"))
    s.append(P("The Parties confirm they have read, understood, and accept this Agreement."))
    s.append(Spacer(1, 24))

    # Source signature is 66x91 px. Display at width 70 keeps native aspect (~96 tall).
    sig_img = RLImage(SIGNATURE, width=70, height=96)
    sig_img.hAlign = "LEFT"

    sig_rows = [
        [P("<b>For Oliviks KFT</b>", "body_bold"), P("<b>For BridgeWorks (Emmanuel Olayinka Ehigbai EV)</b>", "body_bold")],
        [P("Name: ____________________________", "body"), P("Emmanuel Olayinka Ehigbai", "body")],
        [P("Title: _____________________________", "body"), P("Founder, BridgeWorks", "body")],
        [P("Date: _____________________________", "body"), P("office@bridgeworks.agency", "body")],
        [P("Signature: _________________________", "body"), P("Date: 29 April 2026", "body")],
        [P("", "body"), [P("Signature:", "body"), sig_img]],
    ]
    sig_table = Table(sig_rows, colWidths=[237, 238])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    s.append(sig_table)

    s.append(Spacer(1, 28))
    s.append(_section_divider())
    s.append(P("<b>Annex A:</b> Digital Growth Proposal, Oliviks Nigerian Kitchen, dated 28 April 2026 (separate document).", "small"))

    doc.build(s)
    print(f"Contract saved: {output}")
    return output


if __name__ == "__main__":
    build_contract()
