# Scope and Price: AI-Powered Weekly Home Cleaning

Date: 2026-08-21
Prepared by: BridgeWorks
Status: Internal scoping. Not client-ready. Confirm assumptions before quoting.
Source: Service summary and website copy supplied for "AI-Powered Weekly Home Cleaning", Budapest districts 1, 2 and 12.

## The scoping problem

The brief is labelled "service summary for web designer" but it describes two different builds sitting on top of each other.

1. A marketing website. Homepage, how-it-works, service page, three district landing pages, pricing, FAQ, about, contact, CTAs. Weeks of work.
2. A software product. Subscription setup wizard, privacy-zone configuration, smart lock and code-based access control, automatic check-in and check-out, camera capture with baseline comparison, AI detection of missed areas, generated visit reports, client dashboard with history and ratings, cleaner identity records. Months of work, with hardware, recurring infrastructure cost, and serious EU data protection exposure.

The copy is written as though item 2 already exists. Pricing item 1 alone gives a number that is wrong the moment a customer clicks "Book Weekly Cleaning" and expects a dashboard. So this document prices three tiers and names what each one actually delivers.

## Tier 1: Trust Site

The website in the brief, built honestly. Sells the subscription, takes the payment, routes the enquiry. No portal, no cameras, no locks.

Scope:

- Core site, five pages: Home, How It Works, Weekly Subscription, About, Contact
- Three district landing pages: 1st (Castle), 2nd (Hillside), 12th (Hegyvidek)
- Pricing table and FAQ built as sections
- Multi-step subscription request flow: district, plan, home size, privacy zones, access method, preferred day and time
- Submission routed to email, WhatsApp alert, and a tracker within 5 minutes
- Card checkout or deposit link for first payment
- Google Business Profile set up for the three-district service area
- Domain email and WhatsApp Business infrastructure
- Mobile-first, Hungarian and English
- LocalBusiness and Service schema, analytics, cookie consent

| Line | EUR |
|---|---|
| Core site, five pages | 850 |
| District landing pages, 3 at 150 | 450 |
| Subscription intake flow and notification routing | 500 |
| Google Business Profile optimisation | 180 |
| Email and WhatsApp infrastructure | 220 |
| Second language, HU and EN | 250 |
| Subtotal | 2,450 |
| Bundle saving, six lines together | -300 |
| **Total** | **2,150** |

Timeline: 3 to 4 weeks. Payment: 50 percent to start, 50 percent on handover.
Ongoing: Care retainer from EUR 350 per month, 3-month minimum. Optional.

## Tier 2: Trust Site plus Client Portal

The honest version of the product promise. Everything the copy claims about documentation, access logs and visit reports, delivered without cameras or AI vision.

Adds to Tier 1:

- Recurring billing: plan selection, pause, change, cancel
- Client portal: login, visit history, per-visit report page, photos, timestamps, cleaner name, rating, comment, change request
- Cleaner mobile checklist app (PWA): secure check-in, standardised checklist, before and after photo upload, check-out
- Generated visit report: tasks completed, duration, photos, cleaner identity, issues flagged. Templated, not AI
- Admin console: schedule, assign cleaners, client records, privacy-zone configuration
- GDPR pack: privacy policy, photo consent flow, retention rules, processor agreements

| Line | EUR |
|---|---|
| Tier 1 in full | 2,150 |
| Recurring billing | 1,100 |
| Client portal | 2,200 |
| Cleaner mobile checklist app | 1,400 |
| Admin console | 900 |
| GDPR pack | 600 |
| Subtotal | 8,350 |
| Bundle saving | -400 |
| **Total** | **7,950** |

Timeline: 8 to 10 weeks. Payment: 40 / 30 / 30 against milestones.
Ongoing: Care retainer EUR 600 per month, 3-month minimum. Not optional at this tier. A live portal handling payments and customer photos needs monitoring.

## Tier 3: Full system as written

Everything the copy actually promises. Cameras, smart locks, AI quality checking.

Adds to Tier 2:

| Component | EUR |
|---|---|
| Smart lock and time-limited code integration, lock-event check-in | 3,500 to 6,000 |
| Camera capture, per-room zone enforcement, secure storage | 4,500 to 8,000 |
| Vision model baseline comparison and missed-area flagging | 5,000 to 9,000 |
| Cleaner identity verification | 1,500 to 3,000 |
| DPIA and employee-monitoring compliance, external counsel | 2,000 to 4,000 |
| **Added to Tier 2** | **16,500 to 30,000** |

All in: EUR 24,500 to 38,000. Before hardware per home, install labour, storage, connectivity, and ongoing infrastructure. Timeline 5 to 8 months.

Recommendation: do not build this yet. Reasons are in the risk section.

## Recommendation

Build Tier 1 now. Sell subscriptions. If clients sign up and stay, build Tier 2 next. Build Tier 3 only with proven demand, real revenue, and legal sign-off in hand.

Rewrite the website copy so it sells what Tier 1 and Tier 2 actually deliver. "Documented visits, photo proof, tracked entry, named cleaner" is a strong, true offer. It closes the same trust gap. It does not require a single camera.

## Risks and flags

1. **The copy promises a product that does not exist.** Selling weekly subscriptions on this copy, with cameras and smart locks and AI verification named as live features, is a refund and consumer-protection problem in the EU, not only a marketing one. Fix the copy before the site ships.

2. **Cameras in private homes in the EU.** A DPIA under GDPR Article 35 is almost certainly mandatory here. Systematic monitoring inside private dwellings, combined with recording of workers, is close to the centre of what Article 35 targets. NAIH is the Hungarian authority. Recording employees also needs a written employer policy and a proportionality test under the Hungarian Labour Code. Get counsel before any camera ships, not after.

3. **The AI quality check is the hardest part and the least reliable.** Detecting a missed corner or a forgotten bin from before and after photos of arbitrary rooms produces false positives. False positives create exactly the disputes the product claims to remove. This is the component most likely to damage the brand.

4. **Language.** Districts 1, 2 and 12 are high-value and expat-heavy. Hungarian and English are both required. Shipping Hungarian only loses a large share of the target market. Priced in.

5. **Stripe is not live.** The open loop on the board has a Friday decision date. Tier 1's payment line depends on it. Barion is the local fallback and handles HUF cleanly.

6. **FX.** The HUF figures in the Oliviks contract use 363.5 HUF per EUR. Live EUR/HUF is materially higher than that. Quoting at 363.5 undercharges by roughly 8 to 10 percent. Refresh the rate before any HUF number goes out.

7. **No brand system assumed.** If the client has no logo, palette or type system, add Brand Build Foundation at EUR 1,200. The copy leans hard on premium trust positioning and will not carry it with a default template look.

## Assumptions to confirm

- Greenfield. No existing site, no existing platform, no existing booking system.
- Both Hungarian and English.
- Client supplies photography and brand assets, or add the brand line above.
- Tier 1 subscription means a request form plus card checkout. Not live calendar, route or capacity logic.
- Three district pages. Additional districts at EUR 150 each.
- BridgeWorks builds direct for the operator. If this arrives through an agency or a middle party, add a coordination margin.
- Camera hardware, smart locks and their install are the operator's cost in every tier, never bundled into the build fee.

## Rate card lines used

From `pipeline/lead-qualification/scoring-prompt.md` and `operations/lead-engine-v1/04-offers/bridgeworks-offer-ladder.md`:

- Website new build: EUR 850
- Google Business Profile: EUR 180
- Email infrastructure: EUR 220
- AI Automation Starter: EUR 500
- Care retainer Starter: EUR 350/mo, Growth: EUR 600/mo, 3-month minimum
- Brand Build Foundation: EUR 1,200

Pricing rule applied: bundle savings only, no discount without scope reduction.
