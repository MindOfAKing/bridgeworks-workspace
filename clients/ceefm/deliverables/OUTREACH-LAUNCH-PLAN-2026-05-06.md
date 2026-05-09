# CEEFM Cold Outreach — Launch Plan

**Date:** 6 May 2026
**Prepared by:** BridgeWorks · office@bridgeworks.agency
**Status:** Approved to launch (GEO 74/100, above the 70 threshold)
**Sequence file:** `deliverables/COLD-OUTREACH-SEQUENCE-EN-HU.md`

---

## Launch Readiness Check

| Criterion | Required | Status |
|-----------|----------|--------|
| GEO / AI Visibility Score above 70 | Yes | **Cleared — 74/100** |
| SPF, DKIM, DMARC on office@ceefm.eu | Yes | **Cleared — set up 2026-04-18** |
| Cold outreach copy (EN + HU) | Yes | **Cleared — 3-email sequence ready** |
| Mailbox warm-up (2-week ramp) | Yes | **Not started — critical path item** |
| Prospect list (first wave, 25-50) | Yes | **Not built — action required** |
| Sending platform configured | Yes | **Not configured — action required** |
| Service pages live | Preferred | Waivable for Wave 1 (homepage covers it) |
| Limehome case study page live | Preferred | Waivable (Limehome cited in email body) |

**Bottom line:** The copy is ready and the site is credible enough. Two things must happen before a single email sends: the prospect list must exist, and the mailbox must not be sending cold volume from a cold state.

---

## The Mailbox Warm-Up Issue

`office@ceefm.eu` was created on 2026-04-18. It is 18 days old. It has received contact form submissions and outbound emails but zero cold outreach volume.

Sending 50 cold emails from an 18-day-old inbox on Day 1 will likely push a significant portion into spam. Gmail and Outlook score new sender reputation by volume/reply ratio. A spam spike now can damage the domain's sending reputation permanently.

**The fix is simple and starts today.**

### Warm-up ramp (start immediately, 2026-05-06)

| Days | Max sends per day | What to send |
|------|-------------------|--------------|
| 1-5 (May 6-10) | 5 | Victor's warm contacts: existing property contacts, referrals, people he knows |
| 6-10 (May 11-15) | 15 | Wave 1A cold list: 15 highest-fit prospects |
| 11-16 (May 16-21) | 30 | Wave 1B cold list: next 30 prospects |
| 17+ (May 22+) | 50+ | Full cadence |

**Using Victor's warm contacts first** solves two problems at once: it warms the inbox on real replies and gives CEEFM early traction before the cold list goes out.

---

## Apollo.io — Account Status

The account is on the free plan. Two things this means:

| Feature | Free Plan | What We Need |
|---------|-----------|--------------|
| People / company prospect search | Blocked | Upgrade required |
| Contact enrichment (email lookup) | 100 credits available | Available now |
| Sequence builder | Available | Available now |
| Email sending via SMTP | Available | Available now |

**Decision needed from Emmanuel:** Upgrade Apollo to Basic ($49/month) or build the prospect list manually.

- **Upgrade:** Unlocks prospect search. Build the 50-contact list in Apollo directly. Enrichment credits then verify emails before sending. Recommended if we want to move fast.
- **Manual build:** Use LinkedIn (free), Limehome's public partner network, and the Hungarian company registry (Cégadatbázis, e-cegjegyzek.hu) to find and qualify prospects. Import into Apollo for enrichment. Takes longer but costs nothing beyond the credits already available.

**Recommended: Upgrade for the duration of the engagement ($49 × 3 months = $147 / ~53,000 HUF). The ROI on a single signed FM contract makes this trivial.**

---

## Building the Prospect List (Manual Method — No Upgrade Required)

If upgrading Apollo is not immediately approved, use this process to build Wave 1 (25 contacts) within 3-4 days.

### Step 1 — LinkedIn (free, ~2 hours)

Search filters:
- Location: Budapest, Hungary
- Title keywords: "general manager", "operations manager", "property manager", "ügyvezető", "ingatlankezelő"
- Company keywords: aparthotel, apart hotel, serviced apartments, hotel, szálloda, lakópark, ingatlan

Target company types:
1. **Aparthotel operators:** Look for properties marketed as "apart hotel" or "serviced apartments" on Booking.com Budapest — cross-reference on LinkedIn for company name, then find the GM or operations lead.
2. **Property management companies (PM):** Search "ingatlankezelés Budapest" on LinkedIn Companies. Filter 11-200 employees.
3. **Boutique hotels:** 3-4 star independent hotels, not chains. Chains have centralised FM.

Record in the prospect spreadsheet (template below): Full name, title, company, LinkedIn URL, property type, email (if visible), language preference (EN/HU).

### Step 2 — Cégadatbázis (Hungarian company registry)

Go to e-cegjegyzek.hu. Search by TEÁOR code:
- **9820** — Saját tulajdonú ingatlan bérbeadása (residential FM)
- **6820** — Saját tulajdonú ingatlan bérbeadása (commercial)
- **5511** — Szállodai szolgáltatás
- **5520** — Üdülési, egyéb átmeneti szálláshely-szolgáltatás (aparthotel)

Filter by Budapest (Bp.) headquarters, active company status. Export company name and registered address. Cross-reference on LinkedIn to find the right contact.

### Step 3 — Victor's own network

Victor should provide a list of 5-10 current or past professional contacts who:
- Manage or own Budapest hospitality or residential properties
- Have heard of CEEFM but are not current clients
- Would not be surprised to receive a note from Victor directly

These go into Days 1-5 (warm send). They should NOT receive the cold template — they get a personalised one-line version.

---

## Prospect Spreadsheet Structure

Save as `deliverables/PROSPECT-LIST-WAVE-1.csv`:

```
FirstName, LastName, Title, Company, PropertyType, LinkedInURL, Email, Language, Warmth, SendDate, Status
```

**Warmth** field values:
- `warm` — Victor knows them personally
- `research` — Found via LinkedIn/registry, never spoken

**PropertyType** values (sets the `[PropertyType]` token in Email 1):
- `aparthotel`
- `residential portfolio`
- `boutique hotel`

---

## Sending Setup in Apollo (Once List Is Built)

1. Connect `office@ceefm.eu` to Apollo via SMTP (Settings → Email Accounts → Add Account → Gmail/Other SMTP). Hostinger SMTP settings: port 587, STARTTLS.
2. Create a new sequence called "CEEFM Budapest FM Outreach – Wave 1".
3. Add three steps — Email, 4-day delay, Email, 5-day delay, Email.
4. Paste the EN copy from `COLD-OUTREACH-SEQUENCE-EN-HU.md` (or HU, based on each contact's language field).
5. Upload the prospect list CSV via Apollo Contacts → Import.
6. Tag each contact with `wave-1`, `aparthotel`/`residential`/`boutique-hotel`, and `en` or `hu`.
7. Add tagged contacts to the sequence. Review the token population before activating.
8. Set daily send limit at 5 to start (ramp per the schedule above).

---

## Email Copy — What Still Needs Updating

The sequence in `COLD-OUTREACH-SEQUENCE-EN-HU.md` has one line that needs a decision before it sends:

> "Brief portfolio: ceefm.eu/contact"

Once the /about page and first service pages are live (Week 7, May 11-17), update this to:
> "How we work: ceefm.eu/services/facility-management-budapest/"

Until then, ceefm.eu/contact works fine as the CTA destination.

The Limehome metrics (9.4 cleanliness score, 9.0+ Booking score, 24 consecutive months) are live-verified and should not be changed.

---

## KPI Targets — Wave 1 (25 prospects)

| Metric | Target |
|--------|--------|
| Email 1 open rate | 40%+ |
| Full sequence reply rate | 6%+ (= 1-2 replies from 25) |
| Click to /contact | 2%+ of opens |
| Site assessment requests | 1+ from Wave 1 |

B2B cold outreach in EU markets benchmarks at 20-30% open rate and 3-5% reply rate. CEEFM's Limehome anchor is a strong credibility hook and should outperform the benchmark.

---

## GDPR Compliance (EU — Required)

- Do not buy lists. Manual/verified lists only.
- Legitimate interest basis applies to B2B cold outreach where the recipient's professional role makes the message relevant. Document the basis before sending.
- Every email must include an unsubscribe option. Apollo handles this automatically via the {{unsubscribe_link}} token — confirm it is present in every email template before activating.
- Store consent and opt-out records. Apollo logs these automatically.
- Do not send from a personal email (Victor's private Gmail). All sends from `office@ceefm.eu` only.

---

## Launch Timeline

| Date | Action | Owner |
|------|--------|-------|
| 6 May (today) | Victor provides 5-10 warm contacts | Victor |
| 7-9 May | Build LinkedIn + Cégadatbázis list to 25 prospects | BridgeWorks |
| 8 May | Apollo upgrade decision | Emmanuel |
| 9 May | Connect office@ceefm.eu SMTP to Apollo | BridgeWorks |
| 9 May | Create sequence in Apollo, load copy, set tokens | BridgeWorks |
| 10 May | Review complete prospect list with Victor | Both |
| 10 May | First 5 warm-contact emails sent (Days 1-5 ramp begins) | BridgeWorks |
| 11-15 May | Wave 1A: 15 cold prospects, 5/day | BridgeWorks |
| 16-21 May | Wave 1B: next 10 prospects, 10/day | BridgeWorks |
| 20 May | First reply/response review | BridgeWorks + Victor |
| 25 May | Wave 2 list built (25 more), Sequence 2 activated | BridgeWorks |

---

office@bridgeworks.agency · bridgeworks.agency
