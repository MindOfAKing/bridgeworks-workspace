# CEEFM Google Ads Campaign Plan
## Week 8 Launch Brief

**Client:** CEEFM Kft
**Prepared by:** BridgeWorks · Emmanuel Ehigbai · office@bridgeworks.agency
**Date:** May 2026
**Engagement:** CEEFM-PROP-001 · Week 7/16
**Status:** For Victor's review and budget approval

---

## What this document is

This is the Google Ads launch plan for CEEFM. It covers the campaign structure, the budget recommendation, the ad copy approach, and what needs to happen in Week 7 before the campaign goes live in Week 8.

Victor confirmed on May 10 that he wants ads running earlier than the original Week 9 plan. Week 7 (May 11-17) is used to finalise the setup. Week 8 (May 18-24) is the launch.

---

## Foundation status before launch

Google Ads works harder when the landing page and digital entity are in good shape. Here is where CEEFM stands entering Week 7.

| Item | Status | Notes |
|---|---|---|
| Website speed (LCP mobile) | In progress | Target: under 3 seconds. Re-run scheduled Week 7. |
| Google Business Profile | In progress | Postcard dispatched. Victor to complete required fields. Verification window closes May 14. |
| NAP consistency (10+ platforms) | In progress | Google, LinkedIn, Facebook Business (new), Bing registered. |
| Facebook Business page | Scheduled Week 7 | Entity signal + employer branding. |
| TikTok Business account | Scheduled Week 7 | Employer branding, demand warming. |
| Bing Webmaster Tools | Scheduled Week 7 | First-pass indexing confirmation. |
| Service pages (Tier 1) | Scheduled Week 7-8 | Interim: ads land on /contact. Transition to service pages when live. |
| RSA ad copy | Complete | 15 headlines + 4 descriptions in EN and HU. Prepared April 2026. |
| Conversion tracking | To set up Week 7 | Google Ads tag + goal: contact form submission. |

The site is not perfect before Week 8. That is acceptable. The contact page converts cleanly and the RSA copy is ready. Service-specific landing pages follow in Week 8-9 and will improve cost per lead as they go live.

---

## Campaign architecture

Three campaigns. Each targets a distinct buyer type. Start with Campaign 1 at the highest budget allocation. Expand based on Week 8-9 data.

### Campaign 1: Hospitality and Aparthotel FM (50% of budget)

This is CEEFM's strongest proof point. The Limehome partnership (9.4 cleanliness score, 24 months running) is a direct reference for every hotel and aparthotel GM searching for a vetted FM partner.

**Ad groups:**
- Aparthotel cleaning Budapest (`takarítás Budapest aparthotel`, `aparthotel cleaning service`, `aparthotel takarítás`)
- Hotel FM partner Budapest (`szálloda takarítás Budapest`, `hotel facility management Budapest`, `hotel housekeeping outsourcing Hungary`)

**Match types:** Phrase match for volume. Exact match for the top 2 keywords per group to control spend.

**Landing page (interim):** ceefm.eu/contact and ceefm.eu/hu/kapcsolat
**Landing page (Week 8+):** ceefm.eu/services/facility-management-budapest/ and ceefm.eu/hu/szolgaltatasok/aparthotel-takaritas/

---

### Campaign 2: Residential Property FM (30% of budget)

Building managers (közös képviselő) retender cleaning contracts regularly. CEEFM's contract model, documentation, and account management approach are built for this buyer.

**Ad groups:**
- Apartment block cleaning (`társasház takarítás Budapest`, `lakópark facility management`, `takarító cég ajánlat Budapest`)
- Common area FM (`közös képviselő takarítás`, `residential FM Budapest`)

**Landing page (interim):** ceefm.eu/contact
**Landing page (Week 8+):** ceefm.eu/hu/szolgaltatasok/tarsashaz-takaritas/

---

### Campaign 3: Commercial and Office FM (20% of budget)

Lower search volume than residential, but the contract values are higher. This campaign tests demand. Pause if cost per click runs above 500 HUF consistently in the first 30 days.

**Ad groups:**
- Office cleaning (`irodatakarítás Budapest`, `office facility management`, `commercial cleaning Budapest`)
- Building operations (`épületüzemeltetés`, `létesítménygazdálkodás Budapest`)

**Landing page (interim):** ceefm.eu/contact
**Landing page (Week 8+):** ceefm.eu/services/facility-management-budapest/

---

## Budget recommendation

**Recommended starting budget: 150,000 HUF per month (Week 8 and 9)**

This is a test budget. It is enough to gather clean data without overcommitting before we know which ad groups convert.

### How this breaks down

| Campaign | Allocation | Monthly budget |
|---|---|---|
| Hospitality / Aparthotel | 50% | 75,000 HUF |
| Residential FM | 30% | 45,000 HUF |
| Commercial / Office | 20% | 30,000 HUF |
| **Total** | | **150,000 HUF** |

Daily spend: approximately 5,000 HUF.

### Why 150,000 HUF and not more or less

**Too low (under 80,000 HUF/month):** FM keywords in Budapest range from 150 to 450 HUF per click. Under 80,000 HUF/month means fewer than 8-10 clicks per day across all campaigns. That is not enough data to optimise. You would wait 60 days to make a single confident bid adjustment.

**150,000 HUF/month:** At an average CPC of 270 HUF, this delivers roughly 550 clicks per month across all campaigns. At a 3% contact form conversion rate, that is 16 submissions per month. At a 25% close rate from submissions, that is 4 qualified conversations per month.

One FM contract for a medium-sized property runs 200,000 to 600,000 HUF per month for CEEFM. A single signed client from this budget more than pays for three months of ad spend.

**Too high (over 300,000 HUF/month):** The search volume for these niche keywords does not support that spend efficiently in the first 30 days. You would either run out of relevant impressions and bleed into broad-match junk, or drive up CPCs competing against your own ads.

### When to scale

After 30 days (end of Week 12), review:
- Which ad group produced the lowest cost per submission
- Which keyword drove the most clicks at the lowest CPC
- Whether the Hospitality campaign is outperforming Commercial

If any one campaign is producing submissions at under 10,000 HUF per submission, increase its daily budget by 50%. Do not scale what is not producing. The data will tell you clearly.

**Scale target (Week 11-12):** 200,000-250,000 HUF/month, concentrated in the two best-performing ad groups.

---

## Ad copy

The RSA copy is already prepared. It covers 15 headlines and 4 descriptions in both English and Hungarian.

**Key proof points baked into the headlines:**
- Limehome partnership reference
- 9.4 cleanliness score
- 98% client retention
- 50+ properties managed
- Site assessment in 5 days
- Operating since 2010
- EU-compliant documentation

**Display URL:** ceefm.eu/facility-mgmt/Budapest (EN) · ceefm.eu/letesitmeny/Budapest (HU)

The full RSA copy document is available separately at GOOGLE-ADS-RSA-COPY-EN-HU.md.

---

## Conversion tracking

Before Week 8, the following must be in place:

1. **Google Ads conversion tag** installed on ceefm.eu (via Google Tag Manager or direct code injection)
2. **Goal: contact form submission** — fires when the user lands on the thank-you confirmation page after submitting /contact or /hu/kapcsolat
3. **Phone call tracking** — if a phone number is in the ad, a Google forwarding number records calls as conversions (optional but recommended once GBP is verified)

Without conversion tracking, the campaign runs blind. There is no meaningful optimisation possible.

BridgeWorks will handle tag installation in Week 7.

---

## Week 7 actions before launch

**BridgeWorks:**
- [ ] Google Ads account: create campaigns, ad groups, keywords, and RSA ads in EN and HU
- [ ] Set up conversion tracking (contact form goal)
- [ ] Install Facebook Business page for CEEFM (entity signal + tracking foundation)
- [ ] Install TikTok Business account
- [ ] Confirm Bing Webmaster Tools first-pass indexing
- [ ] Mobile PageSpeed re-run (LCP target: under 3s)
- [ ] Set campaigns to "Paused" and ready. Launch Week 8.

**Victor:**
- [ ] Approve the 150,000 HUF/month starting budget
- [ ] Confirm which billing card or Google Ads account to use for billing
- [ ] Complete the required fields on Google Business Profile (link already sent)
- [ ] Confirm the contact form email (where submissions land) is monitored daily

---

## What to expect in the first 30 days

| Metric | Target (Week 8-9) | Notes |
|---|---|---|
| Impressions | 3,000-6,000/month | Niche keywords, low volume, targeted |
| Clicks | 400-600/month | At 270 HUF average CPC |
| CTR | 8-14% | FM searches are high-intent; branded terms pull higher |
| Contact form submissions | 12-20/month | At 3% conversion rate |
| Cost per submission | 8,000-12,000 HUF | Target under 15,000 HUF |
| Qualified meetings | 3-5/month | At 25% close rate from submissions |

These are targets, not guarantees. The numbers tighten significantly once service-specific landing pages replace the contact page. Landing pages matched to ad group themes typically improve conversion rate by 40-80%.

---

## Questions for Victor before Week 8

1. Approved monthly budget: 150,000 HUF? Or adjust?
2. Google Ads billing: existing CEEFM Google account, or BridgeWorks manages under an MCC?
3. Contact form monitoring: who checks submissions and how fast?
4. Priority service to lead with: Hospitality (Limehome angle) or Residential (társasház)?

---

*Prepared by BridgeWorks · office@bridgeworks.agency · bridgeworks.agency*
*CEEFM-PROP-001 · Week 7 delivery*
