# Oliviks shop audit — shop.oliviks.com

**Supersedes the first version of this file, which was wrong.** See "Correction" at the bottom.

**Nothing here has been applied.** I did not log into wp-admin.

Audited 2026-08-01 across the home, product, cart, and checkout pages. Single-context run (no subagents), which Impeccable classes as a degraded critique.

---

## P0 — The shop cannot take an order

`https://shop.oliviks.com/checkout/`, with a real item in the cart, renders **the header, the pickup notice, and the footer. Nothing else.**

Verified in a live browser session:

| Element | Present |
|---|---|
| `form.checkout` | no |
| `#customer_details` | no |
| `#order_review` | no |
| Place Order button | no |
| Form fields on the page | 0 (only the header search box) |
| Console errors | none |

The page exists and is correctly identified — `body` carries `woocommerce-checkout woocommerce-page`, WooCommerce enqueues `checkout.min.js`, and the page is ID 11 on the `elementor_header_footer` template. There is simply no checkout content between the header and the footer.

**A customer can browse, add to cart, and click Proceed to Checkout, and then hit a dead page.** No orders can be completed. Given every "Order Online" button on oliviks.com funnels here, this is the whole online ordering channel.

**Fix:** open page ID 11 (Checkout) in wp-admin and restore its content — the `[woocommerce_checkout]` shortcode for the classic checkout, or the Checkout block. Most likely it was emptied during an Elementor edit. Confirm by placing a real test order afterwards.

I could not diagnose further without wp-admin. **Do this before anything else on this list.**

---

## P1 — "Organic Store" appears in the header

The WordPress **Site Title** is still the theme demo's `Organic Store`. It renders as the branding link wherever the logo is not used — confirmed visible on **cart and checkout**, the two highest-trust pages on the site.

The customer reaches payment and the header says they are buying from Organic Store.

**Fix:** Settings → General → Site Title → `Oliviks Kitchen`. Not CSS.

---

## P1 — Footer links are invisible on the home page

`#wp-custom-css` (our own Additional CSS from the July brand pass) contains:

```css
.site-footer, footer { background-color:#111111 !important; color:rgba(247,249,244,0.7) !important; }
.site-footer a, footer a { color:rgba(247,249,244,0.7) !important; }
```

The Rishi footer builder then paints `.footer-middle-row` and `.footer-bottom-row` **cream** over that dark ground. Cream text lands on cream.

**On the home page, 10 of 15 footer elements measure exactly 1.00:1** — the same colour, not merely low contrast. Footer navigation, category links, the address, Privacy Policy, Terms and Conditions.

WooCommerce pages escape this by accident: another rule in the same block, `.woocommerce a { color:#761212 !important; }`, repaints footer links barn red there, giving 10.62:1. So product, cart, and checkout footers look fine and the home page is broken.

**This is why the fix is not a one-liner.** I tested both directions on both page types:

| Direction | Home page | Product page |
|---|---|---|
| Make the footer dark (add the rows to the `#111111` rule) | 10 failures → **0** | 0 failures → **3** (barn red on ink, 1.68:1) |
| Make the footer light (cream ground, barn red links) | 10 failures → **3** | already fine |

Neither is complete. Three links in `.footer-bottom-row` — Oliviks, Privacy Policy, Terms and Conditions — **resisted every stylesheet override I tried**, including `!important` selectors with strictly higher specificity than the rule that is winning. I could not force them from CSS.

**Recommendation:** do not stack more `!important` on top. Edit the existing `/* Footer */` block in Additional CSS to commit to a light footer — matching what the theme already paints and what the WooCommerce pages already do correctly — and set the bottom-row link colour in the Rishi footer builder itself (Customize → Footer → Bottom Row), which is where those three links are being coloured from.

Replace the current `/* Footer */` block with:

```css
/* Footer — light ground, matching what the theme actually paints */
.site-footer, footer {
  background-color: #F7F9F4 !important;
  color: #111111 !important;
  font-family: 'Inter', sans-serif !important;
}
.site-footer a, footer a,
.woocommerce .site-footer a, .woocommerce footer a,
.rishi-footer .widget a,
.rishi-footer .rishi-footer-navigation a { color: #761212 !important; }
.site-footer a:hover, footer a:hover { color: #5a0d0d !important; }
.rishi-footer .widget-title,
.rishi-footer p, .rishi-footer span,
.rishi-footer .contact-info .contact-text { color: #111111 !important; }
```

Then check the three bottom-row links in the browser. If they are still cream, set them in the footer builder, not here.

---

## P2 — Smaller, each verified

| Issue | Detail | Fix |
|---|---|---|
| Breadcrumb sends customers off-site | The "Shop" breadcrumb on every product page points at `/shop/`, which 301s to `oliviks.com/menu` | Point it at the shop root, or remove the `/shop` redirect |
| Previous developer's credit | Footer reads "Powered by Kreativewin" on the client's storefront | Footer builder → copyright text |
| Menu toggle | Papaya on chalk at **1.66:1**, target **20×20px** | CSS block below |
| Remove-from-cart control | The `×` is **15×15px**, under the 24×24 minimum, and it is destructive | CSS block below |
| No `h1` | Neither cart nor checkout has one | Theme/template |
| "Upsell" tab | A product tab is literally labelled `Upsell` to customers | Rename to "You might also like" |
| Keyboard focus | 21 rules remove the focus outline; only 5 `:focus-visible` rules exist | CSS block below |

```css
/* Controls: contrast and target size */
.rishi-header-trigger a.rishi_header_trigger {
  color: #761212 !important;
  min-width: 44px; min-height: 44px;
  display: inline-flex; align-items: center; justify-content: center;
}
.woocommerce a.remove, .remove_from_cart_button {
  min-width: 32px; min-height: 32px;
  display: inline-flex; align-items: center; justify-content: center;
}

/* Restore keyboard focus. Ink core reads on chalk, papaya halo reads on
   barn red and ink, so one layer always carries contrast. */
a:focus-visible, button:focus-visible, input:focus-visible,
textarea:focus-visible, select:focus-visible {
  outline: 2px solid #121210 !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 5px rgba(250,183,58,0.95) !important;
}
```

Verified by injection: toggle 1.66:1 → **10.62:1**, 20×20 → **44×44**.

---

## P3 — Content, not code

- **Product descriptions are thin.** "Egusi soup with one swallow" carries 62 characters on the shop. The same dish on oliviks.com has a full paragraph. The marketing site is doing the selling and the shop is where the decision actually gets made. The copy already exists in `website/src/data/menu.ts`.
- **"Reviews (0)"** shows on every product while the business holds 4.8 from 493 Google reviews. Either hide the tab or seed it.

---

## Checked and found fine

- Product page: zero contrast failures, one `h1`, no heading-level jumps, no unlabeled fields, no images missing `alt`, 5 live regions.
- Cart page: zero contrast failures, labelled quantity and remove controls with good `aria-label` text.
- The `woocommerce-demo-store` banner is repurposed as the pickup notice, not the WooCommerce default. Leave it.
- The "Snacks" category tile reads black on beige. An earlier scan of mine misread it as papaya on beige.
- The low-contrast `.skip-link` is the standard visually-hidden skip link.

## Method

Everything above was measured in a live browser session: WCAG ratios computed from composited layer colours, patches injected and then removed. **The live site was not modified.** One product was added to the cart to render cart and checkout, then removed — verified empty afterwards. No order was placed and no personal data was entered.

## Correction

The first version of this file said the footer's two cream rows should be made transparent so the dark ground shows through, and reported that as verified. It was verified **on the home page only**. On product, cart, and checkout pages that same change turns readable barn-red footer links (10.62:1) into barn red on ink (1.68:1) — it would have broken three pages to fix one. The corrected direction is above.
