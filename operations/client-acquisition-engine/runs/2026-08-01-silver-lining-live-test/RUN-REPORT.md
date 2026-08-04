# Live Prospect Audit Test Report

**Date:** 1 August 2026  
**Operator:** BridgeWorks Codex  
**Status:** Complete, not sent  
**Final prospect:** Silver Lining Consulting, Dubai  
**Decision-maker:** Joanne Bjelanovic, founder and fractional CFO

## Result

A 15-page branded audit was produced from public evidence. It includes:

- commercial diagnosis;
- directional scorecard;
- buyer-journey review;
- competitor contrast;
- offer ladder;
- free value asset;
- tailored homepage copy;
- search and Google actions;
- LinkedIn content and direct-message examples;
- automation and CRM workflow;
- 90-day action plan;
- initial BridgeWorks outreach message;
- sources, limitations, and non-actions.

## Timing

The verified-prospect production phase ran from approximately 11:38 to 11:49 Europe/Budapest time.

That phase included:

- HubSpot duplicate check;
- public decision-maker confirmation;
- five-page website inspection;
- late-loaded form verification;
- technical signal extraction;
- public search and Maps sampling;
- competitor research;
- audit writing;
- PDF rendering;
- visual QA and one cover correction.

Approximate measured production time: 11 minutes.

This does not include the earlier one-time work of reading the local skills, inspecting prior client audits, and improving the shared PDF renderer. It also does not include the rejected-candidate screen.

## Rejected candidate

**Candidate:** Crownline Properties, London

**Reason for rejection:** The site footer disclosed that the website was for demonstration purposes and that all listings were fictional. Registration details also appeared to be placeholders.

**Lesson:** Search snippets and polished pages are not enough. Every prospect must pass a legitimacy gate before enrichment, CRM creation, audit production, or outreach.

## Evidence corrections made during QA

### Contact form

The first DOM read returned no form because the Squarespace form loaded after the initial page event.

A rendered screenshot showed the form. A second browser inspection after the late render confirmed the fields.

The final audit therefore does not claim that the site has no form. It states the narrower, verified finding:

- “Schedule” links lead to a multi-field enquiry form rather than an appointment calendar.
- The form does not include “Fractional CFO” among its service choices.

### Google and Maps

The sampled exact-name search did not surface an unambiguous listing.

The audit does not claim that no Google Business Profile exists. It recommends owner verification.

## Tool findings

### HubSpot

The exact domain was not found in the connected HubSpot account.

No company, contact, deal, task, or note was created.

### Apollo

The direct global people-search endpoint was unavailable on the connected free plan.

No enrichment was attempted. No Apollo credits were spent.

The decision-maker was verified using the company website, public LinkedIn citations, and a public career profile.

### LinkedIn

The company profile, founder profile, and recent public activity were found.

No follow, connection, direct message, or post interaction was performed.

## What made the audit valuable

The strongest recommendations depend on Silver Lining’s actual business:

1. The founder is publicly positioned as a fractional CFO, while the website leads with broad consulting.
2. The firm’s finance, operations, and strategy range becomes a delivery advantage after a clear fractional CFO entry point.
3. The contact form omits the strongest public category.
4. Competitors explain the buying model, process, cost logic, and deliverables more clearly.
5. The audit turns those gaps into a free diagnostic, a 30-day sprint, a recurring engagement, replacement homepage copy, and a 90-day plan.

This is materially different from sending a typo list or generic SEO score.

## Workflow changes required before scaling

1. Add the legitimacy gate before Apollo or CRM work.
2. Require two-mode page inspection: structured DOM plus rendered visual.
3. Separate facts, directional scores, inferences, and recommendations.
4. Require at least three recommendations that could not be reused unchanged for another company.
5. Require a tailored demonstration, not only a critique.
6. Require a source and limitation section in every PDF.
7. Require message copy to state who BridgeWorks is, why the business was selected, what was reviewed, and that no sequence enrolment occurred.
8. Keep all external actions behind explicit approval.

## Recommended experiment design

Do not cement the entire system from one audit.

Run ten controlled prospects across:

- Dubai;
- London;
- Ireland;
- Germany or the Netherlands;
- Nigeria or Ghana;
- one higher-value Hungary account for comparison.

Test two audit entry angles:

- five prospects receive a commercial growth audit;
- five prospects receive a narrower operational or workflow audit.

Measure:

- permission-to-send rate;
- PDF open or acknowledgement rate;
- positive reply rate;
- discovery calls;
- objections;
- time per approved audit;
- percentage rejected by the legitimacy gate;
- which recommendations prospects mention in replies.

Only automate the winning research pattern and message after the ten-prospect test.

## Final artefacts

- `SILVER-LINING-DEMAND-CONVERSION-AUDIT.md`
- `BridgeWorks-Silver-Lining-Demand-Conversion-Audit-2026-08-01.pdf`
- `evidence/homepage.png`
- `evidence/contact-page.png`
- `pdf-render/`
