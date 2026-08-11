# CEEFM website update — 2026-08-11

**Status of the engagement: still closed.** This was unpaid ad-hoc support at Victor's request, not a reactivation. CEEFM remains a past client. Do not schedule content, outreach, reporting, or any recurring delivery off the back of this file.

**What prompted it:** Google Ads kept emailing that no Google tag was found on ceefm.eu. GA4 was present but Google Ads does not count it.

**Deployed to production and verified live on 2026-08-11.**

---

## What changed on the site

**Google Ads tag `AW-18378779634`** added as a second `gtag('config', ...)` on the existing gtag.js load in `BaseLayout.astro`. All 10 pages.

**Consent Mode v2 now actually grants advertising consent.** Previously `ad_storage`, `ad_user_data` and `ad_personalization` were hardcoded `denied` in three places including the Accept handler, so a visitor who accepted still produced `gcs=G101` and every conversion would have run cookieless. Accept now grants all four signals. The `consent default` stays all-denied, so nothing is set before a choice is made. Decline now sends an explicit denied update instead of relying on defaults.

**Conversion event `ads_conversion_Contact_Us_2`** fires from `ContactForm.tsx` on genuine submit success, guarded by a ref so the "send another" reset cannot double-count.

**Contact form success check fixed.** It previously trusted `response.ok`. Web3Forms can return HTTP 200 with `{"success": false}`, which was showing a success screen for submissions that never reached the inbox. It now parses the response body. This was a live bug independent of the tag work.

**Privacy and cookie policy published** at `/privacy` and `/hu/adatvedelem`. None existed before, and the contact form's GDPR line already promised one. Four sections, 207 words EN and 167 HU. Linked from the cookie banner, the footer, and the form's GDPR line.

**Cookie banner copy rewritten** EN and HU to cover advertising. It previously claimed "No personal data is shared with third parties", which the Ads tag makes false. Accept and Decline were also given equal visual weight, since a deprioritised reject option is treated as invalid consent under EDPB guidance and this banner now gathers advertising consent.

**Language toggle fixed.** `Nav.astro` hardcoded the toggle to the homepages, so the Hungarian policy built and served correctly but was unreachable from the UI. Nav now takes optional `altEn`/`altHu`. Defaults unchanged, so no other page's toggle moved.

**"Site by BridgeWorks"** credit added to the footer on all 10 pages, linking to bridgeworks.agency. Matches the Oliviks pattern.

---

## Verified on production, 2026-08-11

All 10 pages return 200 with the AW tag, consent default all-denied, exactly two grant sites, consent block ahead of gtag.js, BridgeWorks credit, and the locale-correct policy link. HSTS, CSP and cache headers intact, so `.htaccess` survived the upload.

On the wire, in a real browser:

- `gcs=G100` before consent, `gcs=G111` after, with `npa=0`
- Ads tag received `en=consent_update` with `gcs=G111`
- `googleads.g.doubleclick.net/pagead/viewthroughconversion/18378779634/?en=ads_conversion_Contact_Us_2` returned **200**

The conversion test used a stubbed form POST, so no test enquiry was sent to office@ceefm.eu.

---

## Open items for Victor

**A second conversion action is firing that BridgeWorks did not add.** `ads_conversion_Contact_Us_1` fires on **page load** of `/contact/`, not on submit. If it is counted as a primary conversion, every contact page visit registers as a lead and Smart Bidding will optimise toward page views. Check Google Ads → Goals → Conversions and either remove it or demote it to secondary.

**Confirm the conversion action's type is Website, not a GA4 import.** A GA4-import action will never match a page-side event no matter how correct the code is, and the symptom is identical to a broken tag. Set Count to "One".

**The policy has not been reviewed by Victor.** It is legal text published under CEEFM Kft's name stating facts about their data processing. He should read it.

**Remarketing is not described either way in the policy.** If the Ads account builds remarketing audiences, the policy under-discloses and needs a sentence.

**Hostinger collaborator access.** Victor granted Emmanuel Collaborator access covering domain, hosting and email on 2026-08-11 to make this deploy possible. It should be revoked once the tag is confirmed working; an ended engagement has no reason to retain mailbox access.

---

## Facts that changed

| Fact | Was | Now |
|---|---|---|
| Live pages | 8 | 10 |
| Sitemap URLs | 8 | 10 |
| Analytics | GA4 `G-F2TLLLG2DH` only | GA4 + Google Ads `AW-18378779634` |
| Ad consent on Accept | denied | granted |
| Privacy policy | none | `/privacy`, `/hu/adatvedelem` |

No new GEO audit was run. The last verified score remains 78/100 from 2026-06-11. Do not infer a score change from this work.

---

## Where the code lives

Source: `C:/Users/User/ceefm-astro/` (GitHub `MindOfAKing/ceefm-astro`, branch `main`).

Commits: `ca44ded` tag and consent, `f5e7a37` policy trim plus HU routing plus credit, `eba63b2` address removal, `35da0ae` further policy trim, `9a9bc35` deploy script.

Deploy: `python deploy-ftp.py` from the repo root, with `CEEFM_FTP_PASS` set in the environment. Uses FTPS. The repo previously had no deploy path at all; releases were manual File Manager uploads, and the Hostinger file browser has no extract function so a zip upload is not possible.
