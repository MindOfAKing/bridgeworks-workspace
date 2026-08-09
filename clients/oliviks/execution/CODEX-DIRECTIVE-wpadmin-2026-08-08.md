# CODEX DIRECTIVE — Oliviks shop wp-admin repair pass (2026-08-08)

You are working in shop.oliviks.com wp-admin, in Chrome. Emmanuel gives you the
login in the chat (user `bridgeworks`); the password is NEVER written to any file.
There is a math captcha on the login page — solve it and log in normally.

Theme: Rishi + Elementor. LiteSpeed page cache is active: after each front-end
change, purge cache (LiteSpeed Cache > Toolbox > Purge All) before verifying.

Context you need: customers pay through Teya and orders ARE captured, but every
order email fails with "Could not instantiate mail function" — host PHP mail is
broken. Orders arrive silently; nobody is notified. That is Task 1 and it is the
priority. Details and evidence: order #7386 notes in WooCommerce.

---

## Task 1 (P0) — Make order emails send: install WP Mail SMTP

1. Plugins > Add New > install and activate **"WP Mail SMTP by WPForms"** (free).
2. Run its setup wizard. From Email: `olivikskitchen@gmail.com`, From Name:
   `Oliviks Kitchen`, force-from ON.
3. Mailer choice, in order of preference:
   - **Option A — Google / Gmail mailer or "Other SMTP" with Gmail**
     (`smtp.gmail.com`, port 587, TLS, username olivikskitchen@gmail.com).
     This needs a **Google App Password** for olivikskitchen@gmail.com
     (myaccount.google.com/apppasswords, requires 2-Step Verification on).
     Emmanuel or Aese must create it and paste it to you in chat — do not
     proceed with the regular Gmail password, it will not work.
   - **Option B** if no App Password can be made right now: pick "Other SMTP"
     and STOP, report what mail credentials would be needed. Do not leave a
     half-configured mailer active.
4. VERIFY: WP Mail SMTP > Tools > Email Test → send to olivikskitchen@gmail.com,
   confirm "test email sent successfully" AND that it lands in the inbox.
5. VERIFY on a real order: WooCommerce > Orders > #7386 > Order actions >
   **"Resend new order notification"**. Confirm the email arrives at
   olivikskitchen@gmail.com and renders with the Oliviks branding.

## Task 2 (P1) — Checkout URL tidy

The live checkout is page **436** at slug `checkout-2`. The dead old checkout
(empty Elementor page) is page **11** and squats on the `/checkout/` slug.

1. Pages > find page 11 ("Checkout", the one whose content is an empty Elementor
   layout with just the pickup-notice text widget) > **Trash**. Do NOT trash 436.
2. Edit page 436 > change slug `checkout-2` → `checkout` > Update.
3. VERIFY: WooCommerce > Settings > Advanced > Checkout page still shows the
   page (436). Open https://shop.oliviks.com/checkout/ in a fresh tab with an
   item in the cart: billing form + order summary + Place order button render.
   https://shop.oliviks.com/checkout-2/ should now 301 or 404 — either is fine.

## Task 3 (P1) — Site title

Settings > General:
- Site Title: `Organic Store` → `Oliviks Kitchen`
- Tagline: if it still says any theme demo text, set `Nigerian Kitchen & Catering
  in Budapest`; if already sensible, leave it.
- VERIFY: cart/checkout header branding no longer says "Organic Store".

## Task 4 (P1) — CSS: invisible footer links + invisible cart button

Appearance > Customize > Additional CSS. Find the existing `/* Footer */` block
(it forces a dark #111111 footer) and REPLACE that block with:

```css
/* Footer — light ground, matching what the theme actually paints (2026-08-08) */
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

Then APPEND this new block at the end of Additional CSS:

```css
/* Cart/checkout primary buttons — papaya on ink (2026-08-08) */
.wc-block-cart__submit-button,
.wc-block-components-checkout-place-order-button,
.wc-block-components-button.wp-element-button {
  background-color: #FAB73A !important;
  color: #111111 !important;
  border: none !important;
}
.wc-block-cart__submit-button:hover,
.wc-block-components-checkout-place-order-button:hover,
.wc-block-components-button.wp-element-button:hover {
  background-color: #e5a42f !important;
  color: #111111 !important;
}

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

/* Restore keyboard focus */
a:focus-visible, button:focus-visible, input:focus-visible,
textarea:focus-visible, select:focus-visible {
  outline: 2px solid #121210 !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 5px rgba(250,183,58,0.95) !important;
}
```

Publish, purge LiteSpeed, then VERIFY:
- Home page footer: links under SHOP and COMPANY are readable (barn red on
  cream), GET SOCIAL icons visible.
- Product/cart/checkout footers still readable (they were fine — must stay fine).
- Cart with an item: "Proceed to Checkout" is yellow with dark text.
- If the three bottom-row links (Oliviks, Privacy Policy, Terms) are STILL
  cream/invisible: they are colored by the footer builder, not CSS — go to
  Customize > Footer > Bottom Row and set their link color to #761212 there.

## Task 5 (P2) — Footer credit

In the footer builder (Customize > Footer > copyright/bottom row text): replace
"- Powered by Kreativewin" with `Site by BridgeWorks` linked to
https://bridgeworks.agency (plain text if links are not allowed there).

## GUARDRAILS
- Do NOT touch WooCommerce > Payments / the Teya (Borgun) gateway settings.
- Do NOT edit or delete any order except the #7386 "resend notification" action.
- Do NOT deactivate or delete any existing plugin; the only install is WP Mail SMTP.
- Do NOT put the wp-admin password or any app password into any file, note, or
  commit — chat only.
- If login fails twice or Google blocks the app-password step, STOP and report.
- Purge LiteSpeed cache after changes; verify on the live site in a fresh
  private window (cache can show you stale pages otherwise).

## REPORT BACK
One line per task: done/blocked + what you verified (test email received? #7386
notification received? /checkout/ renders form? footer links readable on home
AND product page? title fixed? credit swapped?).
