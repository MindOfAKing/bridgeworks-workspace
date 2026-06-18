# Session 2026-06-18 — Oliviks Direct WhatsApp Cart QA

## What was worked on

### Oliviks Kitchen Web Rebuild
- Continued from Task 1 price hydration.
- Completed Task 2: global `OrderProvider` cart state in `src/context/OrderContext.tsx`.
- Completed Task 3: `Add to Order` buttons wired into `src/components/MenuList.tsx`.
- Completed Task 4: slide-out `OrderCartPanel` and WhatsApp message compiler in `src/lib/orderMessage.ts`.
- Completed Task 5: header `View order` cart badge for desktop and mobile reopen.
- Ran local Playwright QA against `http://localhost:3000/menu`.

## Verification

Commands passed:

```bash
npx playwright test .hermes/qa/oliviks-cart.spec.ts --reporter=line
npx tsc --noEmit && npm run build
```

Results:

```text
2 passed (7.5s)
✓ Compiled successfully in 2.6s
✓ Generating static pages (8/8)
```

## QA evidence

Saved under:

```text
clients/oliviks/website/.hermes/qa/
```

Files:
- `report.md`
- `oliviks-cart.spec.ts`
- `cart-flow.png`
- `cart-viewport.png`
- `mobile-cart-reopen.png`

## Decisions / notes

- Keep ordering zero-transaction-fee and direct to WhatsApp.
- Do not invent total pricing for range-priced items. WhatsApp message asks Oliviks to confirm availability, final total, and pickup time.
- No n8n or external workflow layer needed.
- `.hermes` is excluded from production TypeScript builds in `tsconfig.json`.

## Next recommended action

1. Review current implementation visually with Emmanuel.
2. Confirm deployment target and whether this should replace the current live `oliviks.com` path or remain in preview first.
3. Before live cutover, confirm final menu/price details, owner wording, and real photos.

---

## 2026-06-18 Update — Approved Google Doc Copy Applied

Source:

```text
https://docs.google.com/document/d/1hBogVspntOtdWu8BkprHhscKfPBzGGUNu99tP2xIqbU/edit?tab=t.0
```

Applied to:
- `src/app/page.tsx`
- `src/app/about/page.tsx`
- `src/app/menu/page.tsx`
- `src/app/contact/page.tsx`
- `src/components/OrderCTA.tsx`
- `src/components/MenuList.tsx`
- `src/data/site.ts`
- `src/data/menu.ts`

Menu decisions:
- Added confirmed items: Beef Pilau rice, Bitter leaf soup, Banga soup, Chin Chin, Fish roll.
- Removed stale/non-approved orderable items: Efo Riro, Okra Soup, Moi Moi, Akara, Amala, Salad, Extra Stew, Mixed Plate / Combo.
- Pepper soup is visible as a `Price TBC` placeholder.
- Abacha and Fish is visible as a `Price TBC` placeholder.

Verification:

```text
Approved copy probe passed
npx tsc --noEmit && npm run build: passed
Playwright cart QA: 2 passed (7.0s after placeholders)
```

---

## 2026-06-18 Deployment Update — Vercel Live

Vercel setup:
- Authenticated locally as `mindofaking`.
- Linked local folder `clients/oliviks/website` to `emmanuel-ehigbai/oliviks-kitchen`.
- Created live alias: `https://oliviks-kitchen.vercel.app`.

Remote deployment result:

```text
✓ Compiled successfully in 11.6s
✓ Generating static pages (8/8)
✓ Ready in 57s
```

Public verification:
- `https://oliviks-kitchen.vercel.app` returned HTTP 200.
- `https://oliviks-kitchen.vercel.app/menu` returned HTTP 200.
- Live menu contains `Pepper soup`, `Abacha and Fish`, and `Price TBC` placeholders.

Note:
- The long deployment URL returned HTTP 401 due Vercel protection, but the public alias is reachable.

Next:
- Review live site.
- Decide whether to share with client, add custom domain, or adjust placeholder prices/details first.

---

## 2026-06-18 Logo Update — Vercel Live

Source:
- Desktop WordPress export folder: `C:/Users/User/Desktop/Oliviks previous website/.../oliviks_Logo-1.png`.
- Copied into site as `public/images/oliviks-logo.png`.

Code changes:
- `src/components/Header.tsx` now uses `next/image` to render the logo in the sticky header.
- `src/app/layout.tsx` now references the logo in icons and OpenGraph metadata.
- `.hermes/qa/logo-probe.cjs` added as the RED/GREEN source probe.

Verification:

```text
Logo probe passed
npx tsc --noEmit && npm run build: passed
Remote Vercel production build: passed
```

Live verification:
- `https://oliviks-kitchen.vercel.app` returned HTTP 200.
- `https://oliviks-kitchen.vercel.app/images/oliviks-logo.png` returned HTTP 200.
- Homepage markup includes `oliviks-logo.png` and `Oliviks Kitchen & Catering logo`.

Next:
- Review header logo size on desktop and mobile.
- Consider a transparent/cropped logo variant later if the red background feels too heavy in the header.
