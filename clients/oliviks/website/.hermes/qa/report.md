# Oliviks Website Copy Fill + WhatsApp Cart QA Report

Date: 2026-06-18
Source copy: Google Doc `1hBogVspntOtdWu8BkprHhscKfPBzGGUNu99tP2xIqbU`
Target: http://localhost:3000/menu

## Executive Summary

Result: PASS

The website has been filled with the approved Oliviks Kitchen copy and menu details from the Google Doc. The direct WhatsApp cart still works after the content update.

## Source Copy Applied

Homepage:
- `Real Nigerian Food. Made in Budapest.`
- Approved hero subheadline and pickup line
- Nigerian kitchen section
- Budapest proof section
- First-timer section
- Footer/CTA line

About page:
- `How Oliviks Started`
- Cynthia and Aese founder story
- Debrecen 2017 to 2019 detail
- Nigerian kitchen, not African-themed positioning
- 4.8 stars / 491 Google reviews / press proof

Menu page:
- `What We Cook`
- Approved menu introduction
- First-timer line
- Launch note for pepper soup and Abacha/Fish

Contact page:
- `Find Us`
- Address, phone, email, hours
- Catering copy
- Wolt/Foodora secondary note

Menu data:
- Replaced old dish descriptions with approved final menu descriptions
- Added confirmed items: Beef Pilau rice, Bitter leaf soup, Banga soup, Chin Chin, Fish roll
- Removed stale/non-approved menu items: Efo Riro, Okra Soup, Moi Moi, Akara, Amala, Salad, Extra Stew, Mixed Plate / Combo
- Kept pepper soup out of orderable products until a price is confirmed
- Kept Abacha and Fish out until owner approval

## Verification

Commands passed:

```bash
node .hermes/qa/approved-copy-probe.cjs
npx tsc --noEmit && npm run build
npx playwright test .hermes/qa/oliviks-cart.spec.ts --reporter=line
```

Results:

```text
Approved copy probe passed
✓ Compiled successfully in 3.1s
✓ Generating static pages (8/8)
2 passed (7.2s)
```

## Updated QA Evidence

- `.hermes/qa/cart-flow.png`
- `.hermes/qa/mobile-cart-reopen.png`
- `.hermes/qa/approved-copy-probe.cjs`
- `.hermes/source/oliviks-final-copy.txt`

## Remaining Launch Inputs

- Replace `Price TBC` placeholders when Pepper soup / Abacha and Fish final details are confirmed
- Vercel authentication for preview deployment

## Placeholder Decision

Per Emmanuel's direction, both items are now visible in the menu as placeholders:

- Pepper soup — `Price TBC`
- Abacha and Fish — `Price TBC`

## Owner Confirmation Draft

Saved at:

```text
.hermes/qa/client-confirmation-message.md
```
