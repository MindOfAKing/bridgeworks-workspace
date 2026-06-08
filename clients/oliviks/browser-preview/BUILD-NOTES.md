# Oliviks Browser Preview Build Notes

Date: 2026-06-06
Status: First browser-mode build shell after Manus teaser.

## Stance

Manus is treated as a teaser/prototype, not the deliverable.

This build uses:
- Foundation scope.
- Correct founder facts: Cynthia and Aese, Nigerian couple, Masters in Debrecen.
- Direct website ordering as primary conversion path.
- Wolt/Foodora as secondary discovery/delivery channels only.
- Current public oliviks.com menu/product data visible from source pages.

## Files

- `index.html`
- `styles.css`
- `script.js`

Open `index.html` locally in a browser to preview.

## Applied Corrections

- Cynthia and Aese story included.
- About moved out of the home teaser and into a dedicated story section.
- Direct order CTA is primary.
- Snacks menu is explicit.
- Woman/kitchen interior photo is not used on the homepage.

## Important Product Decision

Full Vercel/Next replacement is possible, but direct checkout/cart/payment becomes new scope unless WooCommerce remains the ordering backend.

Recommended production path:
1. Use this browser preview as design/content direction.
2. Implement in WordPress/WooCommerce if current direct-order checkout remains active.
3. Or deploy static/Vercel front end only if it links into the existing direct order/menu flow.
4. Do not replace the order system until checkout, payment, order notifications, and kitchen workflow are specified.

## Still Needed

- Exact 23-product list from WooCommerce/admin.
- Exact Foodora URL if it stays in footer or secondary links.
- Confirmation of direct ordering flow.
- Confirmation of hours and phone.
- Real photos from client.
- Real form behavior decision: remove form, use WhatsApp, or wire backend.
- WordPress implementation or Vercel deployment decision.
