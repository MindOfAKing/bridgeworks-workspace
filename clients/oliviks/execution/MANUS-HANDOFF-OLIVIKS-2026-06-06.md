# Manus Handoff - Oliviks Kitchen Preview

Date: 2026-06-06
Source preview: https://predeploy-83661fe4-oliviks-kitchen-hiixwhqr-fzbofrhfhbwsfvke.manus.space/
Source Manus share: https://manus.im/share/FeaPwfyPse7b9aUhRwBUKT
Status: Manus execution stopped when credits ran out. Continue from this handoff.

## What Was Inspectable

The preview URL is a bundled React/Vite-style site. The Manus share page was dynamic and only exposed metadata via raw fetch, so the exact chat transcript/step list was not available from static HTML. The deployed preview bundle was inspectable.

Local temporary inspection files created by Codex:
- C:\tmp\oliviks-manus-index.js
- C:\tmp\oliviks-manus-index.css

## What Manus Appears To Have Built

Routes detected:
- `/` home
- `/menu`
- `/about`
- `/contact`
- `/404`

Site-wide pieces detected:
- Header/navigation with Menu, About, Contact.
- Footer with phone, email, address, quick links, social links.
- Logo loaded from oliviks.com.
- Hero/food imagery loaded from Manus/CloudFront assets.
- Tailwind CSS, React, framer-motion style animations, shadcn-like component stack.
- Main CTA to Wolt.
- Secondary references to Foodora.
- Phone: +36 70 567 3070.
- Email: olivikskitchen@gmail.com.
- WhatsApp link: https://wa.me/36705673070.
- Address displayed as Rakoczi ter 9, 1084 Budapest, Hungary.
- Google Maps embed on contact page.
- Metadata title: Oliviks Nigerian Kitchen | Authentic Nigerian Food in Budapest.
- Meta description references 4.8 stars from 160+ reviews.

Home page content detected:
- Social proof: 4.8 out of 5 / 160+ Google Reviews.
- Press strip: Origo, We Love Budapest, WMN.
- Copy around authentic Nigerian cuisine in Budapest.
- CTA: Order Now, Explore Menu, Call +36 70 567 3070.
- Section: Taste the Heart of Nigeria.
- Section: From Nigeria to Budapest, with Love.
- Reviews section: What People Say / Loved by Our Community.
- Final CTA: Ready to Taste Nigeria?

Menu page content detected:
- Heading: Explore Our Dishes.
- Copy: Authentic Nigerian cuisine made fresh daily. Order for self-pickup or via Wolt for delivery.
- CTAs: Order on Wolt (Delivery), Call for Private Delivery.
- Category filters/cards:
  - Rice Dishes
  - Soups & Stews
  - Snacks
  - Side Dishes
- Menu items detected:
  - Jollof Rice with Protein of Choice
  - Vegetable Soup with One Swallow
  - Ogbono Soup with One Swallow
  - Oha Soup with One Swallow
  - Egusi Soup with One Swallow
  - Puff Puff
  - Plantain Chips
  - One Pack of Spicy Kuli Kuli
  - Fried Plantain
  - V-Soy Multi Grain Drink
  - Coca-Cola Cherry Coke 330ml

About page content detected:
- Heading: From Nigeria to Budapest.
- Section: The Journey.
- Section: Our Philosophy.
- Section: What We Stand For / Our Values.
- Values detected:
  - Authenticity
  - Fresh Ingredients
  - Community
  - Quality

Contact page content detected:
- Contact cards for address, phone, email, opening hours, WhatsApp.
- Opening hours shown:
  - Monday-Saturday: 11:00-21:00
  - Sunday: 12:00-20:00
- Contact form fields: name, email, message.
- Form behavior detected in bundle: local toast only, no real backend submit.

## Critical Corrections Needed Before Client Use

1. Founder story is wrong in Manus build.
   - Current Manus text still says: Olivia and her husband.
   - Correct fact from Emmanuel on 2026-06-05: Oliviks was created by Cynthia and Aese, a Nigerian couple who studied for their Masters in Debrecen before creating Oliviks Kitchen.

2. About page still leans into the old health/organic positioning.
   - Manus copy says fresh, organic, sustainably sourced, healthy, wholesome.
   - Audit/proposal direction says this should be secondary. Lead with Nigerian identity, founders, comfort food, and Budapest community.

3. Menu appears incomplete.
   - Proposal promised dish descriptions for all 23 menu products.
   - Manus build exposes about 11 detected menu items.
   - Some category states show: No items in this category yet.

4. Foodora link is generic.
   - Detected link: https://www.foodora.hu
   - Needs the exact Oliviks Foodora listing URL.

5. Contact form is not production-ready.
   - Bundle shows form submit only triggers a success toast and clears fields.
   - Needs real email/backend integration or removal/replacement with direct contact CTAs.

6. Retention infrastructure is not done.
   - No MailerLite/Beehiiv setup detected.
   - No email popup, double opt-in, welcome sequence, WooCommerce integration, privacy update, or WhatsApp broadcast opt-in QR flow detected.

7. Google Business Profile work is not done by this preview.
   - No evidence of GBP categories, attributes, GBP menu upload, Q&A, posts, review templates/backfill, Insights baseline, or 4-week follow-up setup.

8. NAP cleanup is not done by this preview.
   - No evidence of Wolt/Foodora/Facebook/TripAdvisor/Wanderlog cleanup.

9. WordPress implementation path is unresolved.
   - The preview is a standalone React build, not a confirmed WordPress/Elementor implementation on oliviks.com.
   - Need decide: migrate design into WordPress, replace site with static/React, or use as visual/copy reference only.

10. Live data needs verification.
   - Phone, hours, prices, menu items, delivery flow, address, and platform links must be confirmed with client or live account evidence before publishing.

## Immediate Continuation Plan

### Step 1 - Capture Manus Output

- Keep the preview URL and Manus share URL in this handoff.
- If possible, get the actual Manus source/export/project files from Manus before the preview disappears.
- If source export is unavailable, use the inspected bundle and screenshots as reference, but rebuild cleanly rather than editing the minified bundle.

### Step 2 - Correct Core Content

Apply the corrected founder story everywhere:
- Cynthia and Aese.
- Nigerian couple.
- Masters in Debrecen.
- Created Oliviks Kitchen after seeing the gap for real Nigerian food in Hungary/Budapest.

Replace the Manus About page paragraph:
`Olivia and her husband started Oliviks...`

With:
`Cynthia and Aese created Oliviks Kitchen after studying for their Masters in Debrecen and seeing how few places in Hungary served the Nigerian food they knew from home. What began as a way to share real Nigerian comfort food has become a Budapest kitchen for Nigerians, expats, and local guests discovering jollof, egusi, suya, puff puff, and more.`

### Step 3 - Complete Menu

- Pull exact WooCommerce product list from oliviks.com admin once access exists.
- Map each product to category, price, image, description, allergens/notes if available.
- Use the existing Website Copy Pack as the first-pass description base.
- Remove empty category placeholder states before handover.

### Step 4 - Production Decision

Choose one route:
- Route A: WordPress/Elementor implementation. Use Manus design as a reference and implement inside current WordPress.
- Route B: Static/React replacement. Requires hosting/domain decision, form handling, and client approval because it is bigger than the WordPress quick-win scope.
- Route C: Hybrid. Keep WordPress/WooCommerce for ordering, use Manus pages as landing-style front pages where feasible.

Recommended conservative route: Route A unless Emmanuel explicitly wants to replace the website stack.

### Step 5 - Finish Proposal Scope Not Covered By Manus

Website:
- Backup current site.
- Remove fake testimonials.
- Add real Google review proof.
- Delete/redirect sample and duplicate pages.
- Add meta descriptions, Open Graph tags, alt text, schema, speed pass, mobile QA.

GBP:
- Baseline Insights screenshot.
- Categories/attributes/description/menu/photos/Q&A/posts/review templates/NAP cleanup.

Retention:
- Email provider, popup, double opt-in, welcome sequence, weekly template, WooCommerce integration, WhatsApp opt-in and QR, privacy policy update.

## Next Safe Action

Ask Emmanuel to either:
1. provide/export the Manus project source files, or
2. approve rebuilding from the inspected preview and the BridgeWorks execution docs.

Do not publish the Manus preview as-is. It is a useful draft, but it still contains wrong founder facts and unfinished production behavior.
