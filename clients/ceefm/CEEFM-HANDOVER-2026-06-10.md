# CEEFM Kft — Digital Growth Engagement Handover

**Prepared by:** Emmanuel Ehigbai / BridgeWorks · office@bridgeworks.agency
**Prepared for:** Victor Danmagaji / CEEFM Kft · office@ceefm.eu
**Date:** 2026-06-10
**Engagement:** CEEFM Digital Growth — 16-Week Engagement (CEEFM-PROP-001)
**Status:** Engagement concluded. Handover document.

---

## Overview

This document records everything built, deployed, and delivered during the CEEFM digital growth engagement. It is structured so CEEFM can operate, maintain, and extend every system independently.

Three sections:

1. What was built and where to find it
2. What is live and how to maintain it
3. What is unfinished and what to do next

The GEO audit run on 2026-06-10 is referenced throughout. The full audit report is at `reports/GEO-AUDIT-REPORT-2026-06-10.md`.

---

## Section 1: What Was Built

### 1.1 Website — ceefm.eu

**Stack:** Astro (static site generator), hosted on Hostinger. No CMS. Pages are `.astro` files. Source code is in `C:/Users/User/ceefm-astro/`.

**Pages live:**

| URL | Language | Purpose |
|---|---|---|
| https://ceefm.eu/ | EN | Main homepage |
| https://ceefm.eu/hu/ | HU | Hungarian homepage |
| https://ceefm.eu/contact/ | EN | Contact + assessment form |
| https://ceefm.eu/hu/kapcsolat/ | HU | Hungarian contact |
| https://ceefm.eu/hospitality | EN | Hospitality FM funnel page |
| https://ceefm.eu/residential | EN | Residential FM funnel page |
| https://ceefm.eu/vendeglatas | HU | Vendéglátás funnel page |
| https://ceefm.eu/lakopark | HU | Lakópark funnel page |

**Note:** The four funnel pages exist and are live but are not yet in the sitemap. See Section 3.

**Technical infrastructure on the site:**

| Item | Location | Status |
|---|---|---|
| ProfessionalService JSON-LD schema | BaseLayout.astro lines 79-155 | Live |
| robots.txt with AI crawler permissions | /public/robots.txt | Live |
| llms.txt (AI-first company summary) | /public/llms.txt | Live |
| Security headers (HSTS, CSP, X-Frame-Options) | /public/.htaccess | Live |
| Bilingual hreflang tags | BaseLayout.astro lines 58-60 | Live |
| Canonical URLs | BaseLayout.astro line 55 | Live |
| Open Graph + Twitter Card tags | BaseLayout.astro lines 63-77 | Live |
| GA4 analytics (G-F2TLLLG2DH) | BaseLayout.astro lines 185-189 | Live |
| Google Consent Mode v2 | BaseLayout.astro lines 162-182 | Live |
| Bing Webmaster verification | BaseLayout.astro line 54 | Live |
| Cookie consent banner | BaseLayout.astro lines 196-237 | Live |
| Hungarian legal imprint | Footer.astro | Live |
| LCP hero image preload (WebP) | BaseLayout.astro lines 27-46 | Live |

**To deploy changes:** Edit the `.astro` files, run `npm run build` in the `ceefm-astro/` folder, then upload the `dist/` folder contents to Hostinger via FTP or the Hostinger file manager.

---

### 1.2 GEO Score Progression

The site started the engagement with a GEO score of 16/100 (Critical). It ends at 77/100 (Good) -- a 61-point improvement over 16 weeks.

| Audit Date | Score | Band | Key Driver |
|---|---|---|---|
| March 2026 | 16/100 | Critical | Baseline before engagement |
| April 3 | 29/100 | Critical | Discovery audit, no fixes yet |
| April 22 | 47/100 | Poor | llms.txt, hreflang, partial schema |
| April 30 (morning) | 61/100 | Fair | Full schema, legal imprint, security headers |
| April 30 (evening) | 74/100 | Fair (top) | Wikidata, IndexNow, Bing, GBP claim, LinkedIn |
| **June 10** | **77/100** | **Good** | Funnel pages, TikTok launch |

The full June 2026 audit report is at: `reports/GEO-AUDIT-REPORT-2026-06-10.md`

To reach 80+, three actions are required. All are listed in Section 3.

---

### 1.3 Content Delivered

**April 2026 content calendar:** 12 strategic posts + 4 Friday amplification posts = 16 posts total. EN + HU versions. Images generated. Posted to CEEFM LinkedIn.

Source: `content/april-calendar.md`

**May 2026 content calendar:** 12 strategic posts + 4 Friday amplification posts = 16 posts total. EN + HU versions. Covering weeks 6-9 of the engagement (May 5 - May 29). Images in `content/images/may-2026-week/`.

Source: `content/may-calendar.md`

**Monthly reports delivered:**
- `reports/CEEFM-April-2026-Executive-Report.md` (+ PDF)
- `reports/CEEFM-April-2026-Delivery-Appendix.md` (+ PDF)
- `reports/CEEFM-April-2026-Performance-Analytics-Appendix.md` (+ PDF)
- `reports/CEEFM-May-2026-Action-Plan.md` (+ PDF)

**GEO audit reports delivered:**
- `reports/GEO-AUDIT-REPORT.md` (initial)
- `reports/GEO-AUDIT-REPORT-2026-04-30.md` (April 30)
- `reports/GEO-AUDIT-REPORT-2026-04-30-evening.md` (same-day revision)
- `reports/GEO-AUDIT-REPORT-2026-06-10.md` (this document's companion, June 10 final)

---

### 1.4 Cold Email Infrastructure

A full cold outreach system was built and run from `C:/Users/User/Projects/02-Clients/prospects/`.

**What was built:**

- Python script (`send_ceefm_outreach.py`): SMTP-based sender, reads from a contacts list, deduplicates via `sent_log.json`, dry-run mode, interactive confirmation per send.
- Prospect scoring pipeline: 95 Budapest property management companies scored on portfolio size, district, service match, and website health. Tiered into Tier 1 (33), Tier 2 (37), Tier 3 (25).
- Personalised email templates: EN and HU versions per property type (hospitality vs residential).
- Referral partner list: 51 referral contacts (architects, property lawyers, building surveyors, HOA administrators).

**Outreach status at handover:**

| Company | Email | Status | Notes |
|---|---|---|---|
| Budapest Residence | info@bpresidence.hu | Sent + follow-up sent | |
| Managerent Kft | info@managerent.hu | Sent + follow-up sent | |
| Florin Apart Hotel | info@florinaparthotel.hu | Sent + follow-up sent | |
| BQA Short Rent Kft | may@bqa-budapest.com | Sent | |
| Crystal Property Management | eszter.solymar@crystalproperty.hu | Sent | |
| Pyramidon Property Management | pergel.laszlo@pyramidon.hu | Sent | |
| Tower International Kft | info@towerbudapest.com | Sent | |
| GPM Home Management | reservation@gpm.hu | Sent | |
| Gellerico Apartments | info@gellerico.com | Bounced | Mailbox not found. Find contact via gellerico.com or Booking.com/Airbnb host profile. |
| Társasház Management | iroda@tarsashazmanagement.hu | Bounced | No MX record. LinkedIn DM: hu.linkedin.com/in/gábor-gerbner-18996775 |
| Walk Inn Apartments | info@walkinn.hu | Bounced | No MX record. LinkedIn DM: hu.linkedin.com/in/reka-michaletzky |
| Vagabond Group | info@vagabondhospitality.com | Bounced | No MX record. LinkedIn DM: linkedin.com/in/william-hardy-86518a50 |
| Budapest Apartments | office@budapestapartments.com | Bounced | Mailbox not found. Drop -- no alternative found. |

**Delivered:** 11 emails
**Bounced:** 5 (4 with LinkedIn DM alternatives identified)
**Replies received:** 0 (as of June 10 -- B2B cold outreach window is 4-6 weeks; first signal window closes around late June)

**The three LinkedIn DMs for bounced contacts are written and ready.** They are in the outreach playbook at `deliverables/outreach/CEEFM-full-outreach-playbook-2026-05-15.md`. Victor needs to send these manually from his LinkedIn account.

**Remaining Tier 1 prospects not yet contacted:** 84 companies remain in the scored database. The full list is at `deliverables/PROSPECT-LIST-WAVE-1.csv` and `deliverables/outreach/CEEFM-client-outreach-queue-2026-05-15.csv`.

---

### 1.5 LinkedIn Company Page

The CEE FM LinkedIn company page was optimised and has been posting 3x/week (Tuesday, Wednesday, Thursday) since April 2026.

April analytics baseline (from `reports/linkedin-analytics/LINKEDIN-ANALYTICS-SUMMARY-2026-04.md`):
- Followers: 146 at end of April
- Impressions growing across the month
- Top post: April 1 company introduction

May calendar posts were scheduled through May 29. June posts are not drafted (engagement ended before the June calendar was produced).

**What CEEFM needs to do:** Continue the 3x/week posting cadence. The May calendar format and post structure are templates to follow. All posts need an EN version and a HU version. Post EN and HU as separate posts on the same day or as a bilingual single post.

---

### 1.6 TikTok

TikTok Business account for CEEFM was set up during the engagement. The account is live. One video was uploaded (before-and-after room clean, no voiceover, two clips).

**What CEEFM needs to do:** Post 2-3 videos per month. Content ideas: before-and-after property work, behind-the-scenes maintenance, quick tips for property managers. The goal is consistent presence, not viral reach. AI systems use active TikTok profiles as entity credibility signals.

---

### 1.7 Other Deliverables

All deliverables are in `deliverables/`. Key items:

| File | What It Is |
|---|---|
| `APARTHOTEL-OPERATING-STANDARD-V1-DRAFT-2026-05-18.md` | 14-category operating framework. Internal draft. Publish as a PDF or site page to generate leads. |
| `COLD-OUTREACH-SEQUENCE-EN-HU.md` | 3-email sequence templates for future outreach waves |
| `GBP-BUSINESS-DESCRIPTION-EN-HU.md` | Ready-to-paste Google Business Profile description in EN and HU |
| `GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md` | Full Google Ads plan using the 120,000 HUF credit |
| `GOOGLE-ADS-RSA-COPY-EN-HU.md` | Responsive Search Ad copy in EN and HU, ready to paste |
| `LINKEDIN-COMPANY-PAGE-OPTIMISATION.md` | LinkedIn page setup and optimisation guide |
| `SEO-KEYWORD-RESEARCH-TOP-20.md` | Top 20 search terms for Budapest facility management |
| `VIDEO-SCRIPT-GOOGLE-ADS-EN-HU.md` | Video ad scripts for the 12 Remotion video assets |
| `outreach/CEEFM-full-outreach-playbook-2026-05-15.md` | Full operating guide for the outreach system |

---

## Section 2: What Is Live and How to Maintain It

### 2.1 Website

**Who hosts it:** Hostinger. Victor has login credentials.

**How to make text changes:** The site content is in `ceefm-astro/src/data/content.ts` (or the equivalent content file). Edit the text, rebuild, and re-upload. For schema or meta tag changes, edit `BaseLayout.astro`.

**How to add a page:** Create a new `.astro` file in `ceefm-astro/src/pages/`, import `BaseLayout`, and add the URL to `sitemap-0.xml`. Rebuild and upload.

**Do not touch:**
- `BaseLayout.astro` schema block unless you know what you are changing and why. A mistake here can break structured data sitewide.
- `.htaccess` security headers. These are stable and should not need changes.

**Analytics:** GA4 dashboard is at analytics.google.com. Property ID: G-F2TLLLG2DH. Data flows immediately after Consent Mode acceptance by visitors.

---

### 2.2 LinkedIn

**Cadence:** 3 posts per week, Tuesday / Wednesday / Thursday. 9:00 AM CEST for strategic posts.

**Format:** Each post needs an EN version and a HU version. Keep posts under 1,300 characters for the main body. Add hashtags as the first comment after publishing, not in the body.

**Content types that performed best (April data):**
- Industry insight with specific numbers
- Behind-the-scenes operational detail
- Before-and-after or quality-check stories

**What not to post:** Generic FM statements, vague brand content, anything without a specific claim or story.

---

### 2.3 Cold Email System

The Python script is at `C:/Users/User/Projects/02-Clients/prospects/send_ceefm_outreach.py`. It uses a Gmail App Password for authentication. The full operating guide is in `deliverables/outreach/CEEFM-full-outreach-playbook-2026-05-15.md`.

**To send the next wave:**
1. Pick the next 10-15 companies from `CEEFM-client-outreach-queue-2026-05-15.csv` (Tier 1 first, then Tier 2).
2. Confirm email addresses are correct.
3. Run the script in dry-run mode first to preview output.
4. Confirm each send interactively.

**Watch the inbox:** Replies may come 4-6 weeks after the send date. The last send was May 21. Monitor office@ceefm.eu through late June for first replies.

---

## Section 3: What Is Unfinished and What to Do Next

These items are listed in priority order. The top three are quick fixes (under 1 hour combined) that will move the GEO score from 63 to approximately 70.

---

### Priority 1: Complete Google Business Profile Verification (10 minutes)

The GBP postcard was mailed to the Újlengyel registered address in early May. The verification code should have arrived by now.

**How to complete:**
1. Go to business.google.com
2. Log in with the Google account used to create the CEEFM GBP listing
3. Enter the postcard verification code
4. Confirm business details are accurate
5. Add the resulting Maps URL to the `sameAs` array in `BaseLayout.astro` line 128-131

This is the single highest-impact remaining action. It puts CEEFM on Google Maps, enables the local knowledge panel, and adds a critical entity signal that AI Overview systems use for local queries.

The ready-to-paste business description is at `deliverables/GBP-BUSINESS-DESCRIPTION-EN-HU.md`.

---

### Priority 2: Add Funnel Pages to Sitemap (20 minutes)

Four pages are live but not in `sitemap-0.xml`. AI crawlers following the sitemap never find them.

**Current sitemap-0.xml URLs:**
```
https://ceefm.eu/
https://ceefm.eu/contact/
https://ceefm.eu/hu/
https://ceefm.eu/hu/kapcsolat/
```

**Add these four:**
```
https://ceefm.eu/hospitality
https://ceefm.eu/residential
https://ceefm.eu/vendeglatas
https://ceefm.eu/lakopark
```

Also add `<lastmod>2026-06-10</lastmod>` to all entries. Rebuild and redeploy.

---

### Priority 3: Fix llms.txt Year Error (5 minutes)

Open `ceefm-astro/public/llms.txt`. Change:
```
12 years of operational experience
```
To:
```
Operating since 2010 (16+ years of operational experience)
```

Rebuild and redeploy.

---

### Priority 4: Add FAQPage Schema (1 hour)

The homepage FAQ section exists but has no schema markup. AI systems treat it as plain text. Adding FAQPage JSON-LD makes each question extractable for Google rich results and AI Overviews.

Add the following to `index.astro`, passing it as `extraJsonLd` to BaseLayout:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[FAQ question 1 from content.ts]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FAQ answer 1]"
      }
    }
  ]
}
```

Repeat for each FAQ pair. Mirror the same schema in `hu/index.astro`.

---

### Priority 5: Fix numberOfEmployees in Schema (5 minutes)

In `BaseLayout.astro` around line 145, change:
```json
"numberOfEmployees": {
  "@type": "QuantitativeValue",
  "minValue": 11,
  "maxValue": 50
}
```
To:
```json
"numberOfEmployees": {
  "@type": "QuantitativeValue",
  "value": 8
}
```

---

### Priority 6: Send LinkedIn DMs for Bounced Contacts (30 minutes, Victor's action)

Three companies bounced on email. LinkedIn DMs are the backup channel. Victor needs to send these from his personal LinkedIn account. The message copy is in the outreach playbook.

| Contact | LinkedIn |
|---|---|
| Gábor Gerbner (Társasház Management) | hu.linkedin.com/in/gábor-gerbner-18996775 |
| Réka Michaletzky (Walk Inn) | hu.linkedin.com/in/reka-michaletzky |
| William Hardy (Vagabond Group) | linkedin.com/in/william-hardy-86518a50 |

---

### Priority 7: Continue Cold Outreach (ongoing)

84 scored companies remain in the database. The outreach infrastructure is built and operational. Continue sending 10-15 companies per wave, spacing sends 1-2 weeks apart. Follow with one follow-up email 5-7 days after the initial send.

---

### Priority 8: Publish Aparthotel Operating Standard (2-3 hours)

The 14-category framework is drafted at `deliverables/APARTHOTEL-OPERATING-STANDARD-V1-DRAFT-2026-05-18.md`. It was promised in the May LinkedIn content as a June publication. Converting it to a PDF and posting it as a site page (e.g. `/aparthotel-standard`) with a contact form gating it would generate qualified leads from Budapest aparthotel operators.

---

### Priority 9: Create /about Page (3-4 hours)

A dedicated `/about` URL with Victor's bio, company history, headcount, and credentials would significantly improve E-E-A-T signals. It should include: Victor's name and professional background, the founding story, the Limehome relationship, the 8-person team count, and any industry memberships.

---

### Priority 10: Activate Google Ads (when ready)

The 120,000 HUF Google Ads credit is pre-loaded and ready. The campaign plan is at `deliverables/GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md`. RSA copy is at `deliverables/GOOGLE-ADS-RSA-COPY-EN-HU.md`. The recommendation is to activate after GBP is verified (so the ad traffic lands on a site with a verified Maps listing).

---

## Section 4: File Index

All engagement files are at:
`C:/Users/User/Projects/bridgeworks-workspace/clients/ceefm/`

```
ceefm/
├── CLAUDE.md                          Client context file
├── CEEFM-HANDOVER-2026-06-10.md       This document
├── content/
│   ├── april-calendar.md              April 2026 content (12+4 posts)
│   ├── may-calendar.md                May 2026 content (12+4 posts)
│   ├── MAY-CALENDAR-DESIGN.md         Design decisions behind May calendar
│   └── images/                        All generated post images
├── deliverables/
│   ├── APARTHOTEL-OPERATING-STANDARD-V1-DRAFT-2026-05-18.md
│   ├── COLD-OUTREACH-SEQUENCE-EN-HU.md
│   ├── GBP-BUSINESS-DESCRIPTION-EN-HU.md
│   ├── GOOGLE-ADS-CAMPAIGN-PLAN-WEEK8.md
│   ├── GOOGLE-ADS-RSA-COPY-EN-HU.md
│   ├── LINKEDIN-COMPANY-PAGE-OPTIMISATION.md
│   ├── PROSPECT-LIST-WAVE-1.csv
│   ├── SEO-KEYWORD-RESEARCH-TOP-20.md
│   ├── VIDEO-SCRIPT-GOOGLE-ADS-EN-HU.md
│   └── outreach/
│       ├── CEEFM-full-outreach-playbook-2026-05-15.md
│       ├── CEEFM-client-outreach-queue-2026-05-15.csv
│       └── CEEFM-full-outreach-packet-2026-05-15.xlsx
├── invoices/
│   ├── E-EO-2026-1_Setup-fee.pdf
│   └── E-EO-2026-2_April-retainer-(Month-1).pdf
└── reports/
    ├── GEO-AUDIT-REPORT-2026-06-10.md  Final GEO audit (this engagement)
    ├── CEEFM-April-2026-Executive-Report.md
    ├── CEEFM-April-2026-Delivery-Appendix.md
    ├── CEEFM-April-2026-Performance-Analytics-Appendix.md
    └── CEEFM-May-2026-Action-Plan.md
```

Website source code: `C:/Users/User/ceefm-astro/`
Cold email scripts: `C:/Users/User/Projects/02-Clients/prospects/`

---

## Summary

The engagement delivered a 61-point GEO score improvement (16 → 77, Critical → Good), a bilingual server-rendered website with comprehensive AI-visibility infrastructure, two months of LinkedIn content, a scored prospect database of 95 companies, a live cold email pipeline, TikTok launch, and an Aparthotel Operating Standard framework.

The remaining path to 80+ is three quick fixes: GBP verification, adding funnel pages to the sitemap, and FAQPage schema. Combined effort: under 2 hours. The cold email pipeline is operational and 84 prospects remain in the queue.

BridgeWorks remains available for future engagements.

**office@bridgeworks.agency · bridgeworks.agency**
