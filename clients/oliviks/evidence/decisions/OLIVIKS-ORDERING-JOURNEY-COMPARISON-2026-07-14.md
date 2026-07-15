# Oliviks Ordering Journey Comparison

Date: 2026-07-14
Status: Preview comparison. Repeat on the production root after cutover.

## Scope Boundary

The Foundation engagement did not include a full ecommerce rebuild. The new marketing site is responsible for making the next action obvious and routing the customer to the existing WooCommerce shop, WhatsApp, Wolt, or Marwa.

## Legacy Public Journey

The current `https://oliviks.com/` response remains the legacy WordPress/WooCommerce surface.

Read-only homepage extraction found:

- 86 total `href` values.
- 11 inline `?add-to-cart=` actions.
- Separate links for the shop home, cart, contact, account, menu, and individual products.
- A large number of theme, plugin, feed, and WordPress resource links in the document.

The legacy path allows ordering, but the customer is exposed to several overlapping route types and a heavier page before reaching the product or cart state.

## New Preview Journey

The new homepage at `https://oliviks-kitchen.vercel.app/` exposes 23 total links and five clear ordering destinations:

1. Existing WooCommerce shop.
2. WhatsApp order intent.
3. WhatsApp question intent.
4. Wolt.
5. Marwa.

The local production-build menu contains:

- 33 direct WooCommerce product links.
- 4 WhatsApp order links.
- 37 total shop links when page-level shop calls to action are included.

The contact route also provides phone, email, WhatsApp, and catering paths without forcing a purchase action.

## Messaging Change

| Legacy emphasis | New emphasis |
|---|---|
| Shop and cart mechanics appear alongside the marketing surface. | The marketing site first explains the food, proof, location, and service. |
| Several route types compete for attention. | Primary calls to action use `Order Online`, `Browse the Menu`, or a specific WhatsApp intent. |
| Product discovery and brand explanation share the heavier WordPress surface. | The menu is browsable on the fast marketing site, then routes to the matching WooCommerce product. |
| Ordering-system complexity is visible to the visitor. | Existing ecommerce is preserved behind a clearer handoff. |

## Evidence-Based Conclusion

The new journey is clearer because it separates explanation from transaction while retaining the existing fulfillment system. The evidence supports a reduced-link, lower-resource, intent-specific handoff. It does not support a claim that BridgeWorks rebuilt checkout or delivery operations.

## Launch Checks Still Required

- Confirm all 33 product slugs still resolve after root cutover.
- Confirm the root-domain navigation no longer exposes obsolete WordPress routes.
- Record the backup and redirect decision for `/sample-page/`, `/cart-2`, `/checkout-2`, `/my-account-2`, and other retired paths.
- Test one non-purchasing route to the shop and one WhatsApp intent on the production domain.
- Capture the final production screenshots and client approval.
