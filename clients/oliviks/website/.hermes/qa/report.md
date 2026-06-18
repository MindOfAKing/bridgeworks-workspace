# Oliviks WhatsApp Cart QA Report

Date: 2026-06-18
Target: http://localhost:3000/menu
Scope: Direct WhatsApp cart flow after Tasks 2–5.

## Executive Summary

Result: PASS

The core customer path works locally:

1. Open menu.
2. Add Jollof Rice to order.
3. Cart opens automatically.
4. Quantity can increase and decrease.
5. WhatsApp link is generated with the correct phone number and encoded order message.
6. Cart can close and reopen from the desktop header.
7. Cart can close and reopen from the mobile header menu.
8. Cart can clear the order.
9. No browser console errors were captured during the tested flows.

## Automated Checks Run

Command:

```bash
npx playwright test .hermes/qa/oliviks-cart.spec.ts --reporter=line
```

Result:

```text
Running 2 tests using 1 worker
[1/2] menu add-to-order cart flow builds a WhatsApp order link
[2/2] mobile header can reopen an existing cart
2 passed (7.5s)
```

Production verification:

```bash
npx tsc --noEmit && npm run build
```

Result:

```text
✓ Compiled successfully in 2.6s
✓ Generating static pages (8/8)
```

## WhatsApp Link Verification

Expected phone number:

```text
36705673070
```

Expected message content confirmed in test:

```text
Hi Oliviks Kitchen, I'd like to place an order:
- 2x Jollof Rice (2,500 – 4,000 Ft)
Please confirm availability, final total, and pickup time.
```

## Evidence Files

- `.hermes/qa/cart-flow.png` — desktop full-page cart flow evidence.
- `.hermes/qa/cart-viewport.png` — desktop viewport-only cart overlay evidence.
- `.hermes/qa/mobile-cart-reopen.png` — mobile cart reopen evidence.
- `.hermes/qa/oliviks-cart.spec.ts` — Playwright QA spec.
- `.hermes/qa/capture-viewport.cjs` — helper used to capture viewport screenshot.

## Findings

### Blocking issues

None found.

### Minor notes

1. Full-page screenshots can make fixed cart overlays look like they stop partway down the page. The viewport-only screenshot confirms the drawer covers the viewport correctly.
2. On mobile, the cart is usable and preserves the order. Visual polish can still be improved later if desired, but no blocking issue was found in the tested path.
3. The header cart count says item count by quantity, e.g. `2 items ready to send` for 2x of one dish. This is acceptable for now but could be changed to `2 total items` later for clarity.

## Verdict

The local QA path passes. The Oliviks direct WhatsApp cart loop is functional and build-safe.
