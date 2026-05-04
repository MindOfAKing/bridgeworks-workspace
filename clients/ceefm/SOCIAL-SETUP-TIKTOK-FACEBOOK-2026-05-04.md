# CEEFM Social Account Setup -- TikTok + Facebook
**Date:** 2026-05-04
**Owner:** Emmanuel (account creation), BridgeWorks (content + assets)
**Goal:** Both accounts live with profile, cover, bio, links, and at least one Day-1 post by end of week.

---

## HOW TO USE

1. Open the platform's signup flow.
2. Pick the first available handle from the priority list.
3. Paste the bio + about text from this doc.
4. Upload the profile pic and cover from `brand-visuals/`.
5. Run the post-launch checklist at the bottom.

---

## Asset paths (already generated)

| Use | File |
|---|---|
| Profile pic (both platforms) | `brand-visuals/logo/ceefm-logo.png` (500x500, square) |
| Facebook cover -- green (default) | `brand-visuals/facebook/ceefm-facebook-cover-green-1640x628.png` |
| Facebook cover -- navy (alt) | `brand-visuals/facebook/ceefm-facebook-cover-navy-1640x628.png` |
| LinkedIn banner reference | `brand-visuals/linkedin/ceefm-linkedin-banner-stripped-green-1128x191.png` |

TikTok has no banner -- profile pic only.

---

## Handle priority (try in order)

1. `ceefm`
2. `ceefm.eu` (Facebook accepts dot, TikTok does not)
3. `ceefmkft`
4. `ceefmbudapest`
5. `ceefmhungary`

For TikTok, drop the dot variant. If `ceefm` is taken, jump to `ceefmkft`.

---

## TikTok setup

### Account type
Business account (not Creator). Required for the website link in bio and analytics.

### Category
Local Services -> Cleaning Services. If unavailable, pick "Business Services."

### Profile fields

**Display name:** `CEEFM`

**Bio (80 char limit):**
```
Budapest FM | Hotels • Aparthotels • Residential | EN/HU | ceefm.eu
```

**Website link:** `https://ceefm.eu`

**Contact email:** `office@ceefm.eu`

### Settings to enable
- Switch to Business account
- Add category
- Add website link
- Allow comments + duets + stitches (default)
- Turn off "Suggest your account to others" only if you want a quiet launch (recommend leaving on)

### Day-1 content (so the profile is not empty)
Repost the existing 9:16 hotel ad video. Already produced bilingual:
- `brand-visuals/ad-samples/final-ad-hotel-HU.mp4` (Hungarian)
- `brand-visuals/ad-samples/final-ad-hotel-EN.mp4` (English)

**Caption (HU):**
```
A különbség egy 4 csillagos és egy 5 csillagos szoba között 11 perc figyelem.
Budapest. Szállodák, aparthotelek, lakóingatlanok.
ceefm.eu

#Letesitmenykezeles #Budapest #Aparthotel #Szalloda #Vendeglatas
```

**Caption (EN, post 1 day later or as second video):**
```
The difference between a 4-star and a 5-star room is 11 minutes of attention.
Budapest. Hotels, aparthotels, residential.
ceefm.eu

#FacilityManagement #Budapest #Aparthotel #HotelOperations #Hospitality
```

Note: TikTok's video aspect is 9:16. The existing final-ad-hotel files were produced at 16:9 for LinkedIn/YouTube. **Verify aspect before upload** -- if 16:9, we need to re-export 9:16 from the Remotion source in `brand-visuals/remotion-video/`. Flag if the upload looks letterboxed.

---

## Facebook Page setup

### Page type
Business or Brand -> Property Management Company

### Page name
`CEEFM` (matches the brand and the LinkedIn page)

### Page username
`/ceefm` if available. Fallbacks: `/ceefm.eu`, `/ceefmkft`.

### Profile fields

**Short description (intro, 100 char limit):**
```
Premium facility management for hotels, aparthotels, and residential properties in Budapest.
```

**About / Long description (English):**
```
CEEFM Kft is a Budapest-based facility management company founded in 2010. We deliver integrated cleaning, maintenance, and property operations for hotels, aparthotels, and residential buildings.

Trusted by Limehome and over 50 properties across Budapest. Bilingual operations (English and Hungarian). Reachable 24/7 for managed sites.

Web: ceefm.eu
Email: office@ceefm.eu
Phone: +36 30 600 5400
```

**About / Long description (Hungarian):**
```
A CEEFM Kft. egy 2010-ben alapított budapesti létesítménygazdálkodási cég. Integrált takarítást, karbantartást és ingatlanüzemeltetést biztosítunk szállodák, aparthotelek és lakóépületek számára.

A Limehome és több mint 50 budapesti ingatlan megbízható partnere. Kétnyelvű működés (angol és magyar). A kezelt helyszínek számára 24/7 elérhetőek vagyunk.

Web: ceefm.eu
E-mail: office@ceefm.eu
Telefon: +36 30 600 5400
```

Use the English version as the primary About on the page. Pin a Hungarian intro post on day 1 to surface the HU copy.

### Contact info
- Phone: +36 30 600 5400
- Email: office@ceefm.eu
- Website: https://ceefm.eu
- Address: 2724 Újlengyel, Petőfi Sándor utca 48 (registered seat). **Do not list a Budapest telephely until Victor confirms.**
- Hours: 24/7 for managed sites; office hours Mon-Fri 09:00-17:00

### Services to add (use "Services" tab)
1. Hotel facility management
2. Aparthotel operations
3. Residential FM
4. Cleaning and housekeeping
5. Maintenance and HVAC
6. Property compliance
7. SolaCare (solar O&M)

### Cover image
Upload `ceefm-facebook-cover-green-1640x628.png`. Position is automatic -- safe zone is centred.

### Profile picture
Upload `ceefm-logo.png`. Facebook will crop to circle. Verify the logo mark is centred.

### Day-1 content (3 posts to avoid an empty page)

**Post 1 -- Welcome (pin this)**
```
We are now on Facebook.

CEEFM has managed facilities across Budapest since 2010. Hotels, aparthotels, residential buildings. Cleaning, maintenance, compliance, supervision -- under one contract.

Follow for weekly operations content in English and Hungarian.

ceefm.eu | office@ceefm.eu | +36 30 600 5400
```
Image: profile pic or `ad-samples/ad-01-brand-awareness.png`

**Post 2 -- Same content as the May 5 LinkedIn post (Tue)**
Use `content/may-calendar.md` Post 1 (Pre-summer FM checklist) -- both EN and HU. Image: `content/images/may-2026-week/may-post-01-summer-prep.png`. Schedule for Tue 9:00 CEST to match LinkedIn.

**Post 3 -- Same content as the May 6 LinkedIn post (Wed)**
Use Post 2 (Per-task to integrated FM shift). Image: `may-post-02-integrated-vs-vendors.png`.

After day 1: post the same content as LinkedIn at the same time. Friday amplification posts (polls, stat cards) work especially well on Facebook.

---

## Cross-link checklist (after both accounts are live)

- [ ] Add Facebook URL to `ceefm.eu` schema `sameAs` (currently only LinkedIn). File: `ceefm-astro/src/layouts/Layout.astro` or wherever the ProfessionalService JSON-LD lives.
- [ ] Add TikTok URL to `sameAs` array in the same schema.
- [ ] Add both URLs to `llms.txt` Hungarian and English sections.
- [ ] Add both URLs to LinkedIn company page "Websites" section.
- [ ] Add both URLs to Google Business Profile (when claimed in Wk 6).
- [ ] Add both URLs to email signature template.
- [ ] Add Facebook Pixel + TikTok Pixel to `ceefm.eu` (defer to Wk 7 unless ads are imminent).

---

## Open questions for Victor

1. Does CEEFM already own the @ceefm handle on either platform from a previous attempt? Check before claiming.
2. Approve "Trusted by Limehome" wording on the Facebook cover. (Already approved on LinkedIn banner -- assuming yes.)
3. Approve Hungarian profile pic alt text and OG image: should it carry the `+36 30 600 5400` phone or stay logo-only?
4. Sign off on the green cover variant vs the navy alt. Default green; switch to navy if Victor prefers.

---

## Done when

- Both accounts are live with handle, profile pic, cover (FB), bio, contact info, and link.
- Day-1 posts are up.
- LinkedIn and `ceefm.eu` reference both URLs.
- Posting cadence is wired into the existing LinkedIn workflow (same content, same time).
