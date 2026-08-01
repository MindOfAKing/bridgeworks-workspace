# Oliviks shop — CSS patch (shop.oliviks.com)

**Status: NOT APPLIED.** This is a patch for you to paste. I did not log into wp-admin.

## HOW TO USE

1. Open `https://shop.oliviks.com/wp-admin`
2. Go to **Appearance → Customize → Additional CSS**
3. Paste the block from "The patch" below at the end of whatever is already there
4. Click **Publish**
5. Hard-reload `https://shop.oliviks.com/` and check the footer

To undo: delete the block and Publish again. Nothing else is touched.

## Why this is a patch and not a code change

The marketing site (`oliviks.com`) is the Next.js repo in `clients/oliviks/website`. I fixed that in source, on a branch, with a build to verify it.

The shop is a different animal: WordPress 7.0.2 + WooCommerce 10.9.4 on the Rishi theme with Elementor. None of it is in git. There is no source file to edit. The only route in is the customizer, which means logging into a live client storefront with saved credentials and changing production. That is your call to make, not mine, so the fix is written out here for you to apply and review.

## What is broken

Measured on the live site, 2026-08-01.

### 1. The entire footer is invisible (severity: high)

`.rishi-footer` is styled dark: background `#111111`, text cream at 70% opacity. Correct.

But two rows inside it, `.footer-middle-row` and `.footer-bottom-row`, paint a **cream** background over that dark ground. The text colour stays cream. Cream on cream.

**10 of 14 footer text elements measure a contrast ratio of exactly 1.00:1.** Not "low contrast" — the same colour. The footer navigation, the shop category links, the contact address, Privacy Policy, Terms and Conditions: all present in the DOM, all unreadable.

Four more items were then recoloured to near-black, presumably to cope with the accidental cream background. Those need to go back to cream once the ground is restored, or they invert the problem:

| Element | Current colour |
|---|---|
| `.widget-title` ("Shop", "Company") | `rgb(17,17,17)` |
| `.contact-info .contact-text` (address) | `rgb(0,0,0)` |
| `.widget_text p` ("Place an order online or...") | `rgb(0,0,0)` |

### 2. Header menu toggle (severity: medium)

`.rishi_header_trigger` is papaya `#FAB73A` on chalk `#F7F9F4` — **1.66:1**, against the 3:1 WCAG needs for a control. It is also **20x20px**, under the 24x24 minimum. This is the primary navigation control on mobile.

### 3. No keyboard focus (severity: medium)

The loaded stylesheets contain **21 rules that remove the focus outline** and only 5 `:focus-visible` rules. Same defect the marketing site had.

## The patch

```css
/* ── Oliviks shop: legibility patch (BridgeWorks, 2026-08-01) ────────────── */

/* 1. The footer is designed dark (.rishi-footer = #111111, cream text at 70%).
      Two inner rows paint cream over it, so cream text lands on cream and the
      whole footer renders invisible. Remove the stray grounds. */
.rishi-footer .footer-middle-row,
.rishi-footer .footer-bottom-row {
  background-color: transparent !important;
}

/* 2. These four were recoloured to near-black to cope with the broken light
      footer. Return them to the footer's own cream. */
.rishi-footer .widget-title,
.rishi-footer .contact-info .contact-text,
.rishi-footer .widget_text p {
  color: #f7f9f4 !important;
}

/* 3. Menu toggle: papaya on chalk is 1.66:1 at 20x20px. Barn red on chalk is
      10.62:1, and 44px is a comfortable thumb target. */
.rishi-header-trigger a.rishi_header_trigger {
  color: #761212 !important;
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 4. Restore keyboard focus. Ink core reads on the chalk grounds, papaya halo
      reads on the barn-red and ink ones, so one layer always carries contrast.
      Pointer users never see it. */
a:focus-visible,
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: 2px solid #121210 !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 5px rgba(250, 183, 58, 0.95) !important;
}
```

## Verified before handover

I injected this exact CSS into a live page in my own browser session, measured, then removed it. The site was not modified.

| Check | Before | After |
|---|---|---|
| Footer elements failing WCAG AA | 10 of 14 | **0 of 14** |
| Worst footer contrast | 1.00:1 | 8.96:1 |
| Menu toggle contrast | 1.66:1 | 10.62:1 |
| Menu toggle target | 20x20px | 44x44px |

## Checked and found fine

- The `woocommerce-demo-store` banner is repurposed as the pickup notice, not the WooCommerce default "no orders will be fulfilled" text. Leave it.
- The "Snacks" category tile reads black on beige, not papaya on beige. My first scan misread it. No change needed.
- The `.skip-link` low contrast is the standard visually-hidden skip link. Not a defect.

## Not covered

I audited the shop home page only. Product, cart, and checkout pages were confirmed to return HTTP 200 but were not audited. Say the word and I will run the same pass over the checkout flow, which is where a legibility defect costs actual orders.
