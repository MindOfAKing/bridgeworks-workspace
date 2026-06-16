# Oliviks Kitchen — Build Prompts
## v0 + Google Stitch
### Generated: 2026-06-15

---

## Site Status

### Already built (Next.js, App Router, Tailwind)
- `/` Homepage — Hero, trust strip, popular dishes, CTA
- `/menu` Menu page — full 23-item catalog by category
- `/about` About — founders story, values
- `/contact` Contact — info cards, map embed, contact form

### Missing — prompts below
- `/catering` Catering inquiry page
- `/gallery` Photo gallery
- `/faq` FAQ accordion

### Data fixes applied this session
- Hours corrected: Mon–Sat 11:00–20:00, Sunday CLOSED (was 11:00–21:00 / Sun open)
- Review count corrected: 491 (was 160)
- Prices still null in menu.ts — resolve WooCommerce vs approved copy mismatch with Aese before filling

### Price reference from WooCommerce CSV
Soups with swallow: 5,000 Ft | Fried rice with protein: 4,000 Ft | Fried Plantain: 2,500 Ft | Grilled Chicken Thigh: 2,000 Ft | Kuli kuli: 2,000 Ft | Fried Yam: 3,500 Ft | Suya sticks: 1,500 Ft | Fried beef: 1,500 Ft | Meat Pie: 1,500 Ft | Coconut peanut: 1,500 Ft | Poundo Swallow: 1,200 Ft | Eba: 1,200 Ft | Malt: 1,500 Ft | Zobo: 1,500 Ft | Fanta: 1,000 Ft | Coca-Cola: 1,000 Ft

---

## Design System Reference
Use this in all v0 and Stitch prompts.

| Token | Value |
|-------|-------|
| `palm` | #C44D2B (warm terracotta — primary, CTAs) |
| `gold` | #E8A838 (warm gold — accents) |
| `leaf` | #2D5016 (deep green — secondary brand) |
| `cream` | #FDF6EC (default background — never white) |
| `cocoa` | #2A1A12 (near-black — body text) |
| Body font | DM Sans (300, 400, 500, 600, 700) |
| Display font | Playfair Display (400, 500, 600, 700) — headlines only |
| Border radius | lg (cards), 2xl (sections), full (buttons) |
| CTA button | `btn-primary`: rounded-full, bg-palm, text-cream |
| Ghost button | `btn-ghost`: rounded-full, border cocoa/20, text-cocoa |
| Header accent | Ankara-pattern stripe: repeating-linear-gradient 135deg — #C44D2B / #E8A838 / #2D5016 each 14px |
| Container | max-w-6xl, px-5 sm:px-8, mx-auto |

---

## Google Stitch — Full Site Design Brief

Paste this into Google Stitch to generate the visual design system.

```
Design a restaurant website for Oliviks Nigerian Kitchen, a homestyle Nigerian food kitchen in Budapest, Hungary.

BRAND IDENTITY
Name: Oliviks Kitchen
Tagline: Real Nigerian Food. Made in Budapest.
Vibe: warm, homestyle, authentic, welcoming — not fancy, not fast food. A real Nigerian kitchen that feels like home.
Founded by: two Nigerian women (Cynthia and Aese) who came to Hungary for their Masters degrees
Reviews: 4.8 stars from 491 Google reviews
Featured in: Origo, We Love Budapest, WMN

COLOR PALETTE
Primary: #C44D2B (warm terracotta)
Accent: #E8A838 (warm gold)
Dark green: #2D5016
Background: #FDF6EC (warm ivory — never pure white)
Text: #2A1A12 (near-black, warm undertone)

TYPOGRAPHY
Headlines: Playfair Display, bold, warm serif
Body: DM Sans, clean, readable
Style: mix of warm serif headlines with clean sans-serif body creates premium-but-approachable feel

DESIGN ELEMENTS
- Ankara-inspired decorative stripe in the header (diagonal pattern, terracotta / gold / green bands)
- Warm food photography placeholders (rich, warm-toned Nigerian dishes)
- Rounded cards and buttons (no sharp corners)
- Subtle depth through shadows on cards, not heavy borders
- Cream background sections alternate with white cards for visual rhythm

PAGES TO DESIGN
1. Homepage: Hero with food photo + headline + two CTAs (WhatsApp order + View Menu). Trust strip with press logos. "Guest favourites" dish cards grid. Final CTA block.
2. Menu: Category navigation tabs. Dish card grid (photo, name, description, price). Order CTA fixed or inline.
3. About: Founders story with photo. Values grid (4 cards). Closing CTA.
4. Catering: Hero with catering focus. What is included section. How to book section. Inquiry form.
5. Gallery: Masonry photo grid with category filter. Food, kitchen, restaurant.
6. Contact: Info cards (address, hours, phone, email). WhatsApp CTA button. Embedded Google Map. Contact form.
7. FAQ: Clean accordion. Questions about ordering, pickup, allergens, opening hours.

FEEL
Not a typical Hungarian restaurant website. Not a delivery-app style food site. A warm, human, story-led kitchen with real Nigerian character. Nigerian guests should feel seen. First-time visitors should feel welcomed and curious.
```

---

## v0 Prompts

### Prompt 1 — /catering page

```
Create a Next.js 15 App Router page for the /catering route of Oliviks Nigerian Kitchen, a homestyle Nigerian food kitchen in Budapest.

DESIGN SYSTEM (already set up in the project — use these class names and values)
- Background: bg-[#FDF6EC] (cream, default)
- Primary color: #C44D2B (terracotta — class: text-palm / bg-palm)
- Dark text: #2A1A12 (class: text-cocoa)
- Display font: font-display (Playfair Display)
- Body font: font-sans (DM Sans)
- Eyebrow label: className="text-sm font-semibold uppercase tracking-[0.18em] text-palm"
- Primary button: className="inline-flex items-center justify-center gap-2 rounded-full bg-[#C44D2B] px-6 py-3 font-medium text-[#FDF6EC] shadow-sm transition-all hover:bg-[#a83d20] active:scale-95"
- Ghost button: className="inline-flex items-center justify-center gap-2 rounded-full border border-[#2A1A12]/20 px-6 py-3 font-medium text-[#2A1A12] transition-all hover:border-[#C44D2B] hover:text-[#C44D2B] active:scale-95"
- Container: className="mx-auto w-full max-w-6xl px-5 sm:px-8"

PAGE CONTENT

Section 1 — Hero
Eyebrow: "Catering"
Headline (Playfair Display, bold): "Feed your guests with real Nigerian food"
Body: Oliviks Kitchen provides catering for corporate events, private celebrations, university gatherings, and community occasions across Budapest. Minimum 15 guests. Contact us 7 days in advance.
Two CTAs: "Get a quote on WhatsApp" (primary, links to wa.me/36705673070) | "Call us" (ghost, links to tel:+36705673070)

Section 2 — What we offer (3-column card grid on desktop, stacked on mobile)
Card 1 — Corporate Events: Platters of jollof rice, fried rice, soups with swallow, proteins, and sides. Setup included. Minimum 20 guests.
Card 2 — Private Parties: Birthday celebrations, family gatherings, community events. We work around your menu preferences and guest count.
Card 3 — University & Community: Special rates for student events and cultural occasions. Contact us to discuss.

Section 3 — How it works (numbered steps, horizontal on desktop)
1. Contact us — WhatsApp or email at least 7 days before your event
2. We confirm your menu, guest count, and logistics
3. We deliver and set up fresh food on the day

Section 4 — Inquiry form
Fields: Name, Email, Phone, Event date (date picker), Number of guests, Event type (select: Corporate / Private / University / Other), Message
Submit button: "Send catering inquiry" (primary color)
Note below form: "We usually reply within 24 hours."

Contact fallback: "Prefer to call or message directly? +36 70 567 3070 | olivikskitchen@gmail.com"

TECHNICAL NOTES
- Export as a single page.tsx file
- No external dependencies beyond what is standard in Next.js 15 + Tailwind CSS
- Form should use a standard HTML form with action pointing to /api/contact or use a controlled React form with console.log for now — do not wire up any backend
- Use Metadata export for SEO: title "Catering", description "Oliviks Kitchen provides Nigerian food catering for events in Budapest. Minimum 15 guests. Contact us to book."
- Mobile-first responsive layout
- No images needed — use colored placeholder divs or leave image slots empty
```

---

### Prompt 2 — /gallery page

```
Create a Next.js 15 App Router page for the /gallery route of Oliviks Nigerian Kitchen, a homestyle Nigerian food kitchen in Budapest.

DESIGN SYSTEM (same as above — use inline Tailwind values)
Background: #FDF6EC | Primary: #C44D2B | Text: #2A1A12 | Display font: Playfair Display | Body font: DM Sans
Container: mx-auto w-full max-w-6xl px-5 sm:px-8

PAGE CONTENT

Hero section
Eyebrow: "Gallery"
Headline: "A look inside Oliviks Kitchen"
Body: From jollof rice to suya, from the kitchen to the table. Real food, made fresh every day.

Category filter tabs (state-managed with useState)
Options: All | Food | Kitchen | Events
Default active tab: All
Active tab style: bg-[#C44D2B] text-[#FDF6EC] rounded-full px-4 py-2
Inactive tab: border border-[#2A1A12]/20 rounded-full px-4 py-2

Photo grid
- Masonry or CSS grid (3 columns desktop, 2 columns tablet, 1 column mobile)
- 12 placeholder image slots total
- Use a simple placeholder div for each: bg-[#2A1A12]/10 rounded-2xl with a centered label showing what the image is (e.g. "Jollof Rice", "Kitchen prep", "Suya sticks")
- Assign categories to placeholders: 6 Food, 3 Kitchen, 3 Events
- Filter updates which cards are visible using the active category

Closing CTA
"Hungry? Order for pickup."
WhatsApp link button (primary style): "Order on WhatsApp"

TECHNICAL NOTES
- Export as page.tsx with 'use client' directive (needed for useState)
- No lightbox required for now — static grid only
- Metadata: title "Gallery", description "See inside Oliviks Kitchen — authentic Nigerian food made fresh daily in Budapest."
- Image placeholders must be clearly labelled so real photos can be dropped in later
- All placeholder heights: aspect-[4/3] for uniform grid
```

---

### Prompt 3 — /faq page

```
Create a Next.js 15 App Router page for the /faq route of Oliviks Nigerian Kitchen, a homestyle Nigerian food kitchen in Budapest.

DESIGN SYSTEM
Background: #FDF6EC | Primary: #C44D2B | Text: #2A1A12 | Display font: Playfair Display | Body font: DM Sans
Container: mx-auto w-full max-w-6xl px-5 sm:px-8

PAGE CONTENT

Hero
Eyebrow: "FAQ"
Headline: "Common questions"
Body: Everything you need to know about ordering, pickup, and what we serve.

Accordion FAQ (12 questions — one open at a time using useState, smooth height animation)

ORDERING
Q: How do I order?
A: The easiest way is WhatsApp. Send us a message at +36 70 567 3070, tell us what you want, and we will confirm your order and pickup time. You can also call us directly on the same number.

Q: Can I order online?
A: Yes. You can order directly through our website or via WooCommerce. For quick orders, WhatsApp is fastest.

Q: Do you take walk-in orders?
A: Yes. Come to Rákóczi tér 9, 1084 Budapest during opening hours and order at the counter.

PICKUP & DELIVERY
Q: Do you deliver?
A: We are a pickup kitchen. Orders are collected from Rákóczi tér 9, 1084 Budapest. We do not currently offer delivery for regular orders. For catering and large orders, contact us to discuss logistics.

Q: How far in advance do I need to order?
A: For regular orders, same day is usually fine during opening hours. For catering, we ask for at least 7 days' notice.

Q: What are your opening hours?
A: Monday to Saturday, 11:00 to 20:00. We are closed on Sundays.

FOOD & ALLERGENS
Q: Is the food halal?
A: Yes. All our meat is halal.

Q: Do you cater for vegetarians?
A: Some of our dishes are vegetarian or can be made without meat — including eba, pounded yam, fried plantain, and some soups. Ask us when ordering and we will advise.

Q: Do your dishes contain nuts?
A: Some dishes — including suya — contain peanuts. Please inform us of any allergies when placing your order and we will advise on suitable options.

Q: Are the dishes spicy?
A: Nigerian food is bold and well-seasoned. Most dishes have moderate heat. If you prefer less spice, let us know when ordering and we can adjust.

ABOUT THE KITCHEN
Q: Is this a restaurant or a takeaway?
A: We are primarily a pickup kitchen. You can eat here, but most guests order for takeaway. Either works.

Q: Do you do catering for events?
A: Yes. We cater for corporate events, private parties, university occasions, and community gatherings. Minimum 15 guests. See our catering page or contact us directly.

CLOSING CTA (below accordion)
"Still have a question?"
Button (primary): "Message us on WhatsApp" → links to wa.me/36705673070

TECHNICAL NOTES
- 'use client' directive for useState accordion
- Accordion: clicking a question opens its answer, clicking again or another question closes it (only one open at a time)
- Smooth height transition on open/close
- Chevron icon rotates 180 degrees when open (use lucide-react ChevronDown)
- Metadata: title "FAQ", description "Answers to common questions about ordering, pickup, allergens, and catering at Oliviks Nigerian Kitchen in Budapest."
```

---

## Notes for Codex stage
After v0 generates the three pages, bring them into the existing `/website/src/app/` folder and:
1. Replace generic Tailwind hex values with the named color tokens from `tailwind.config.ts` (palm, cocoa, cream, gold, leaf)
2. Wire up the `Reveal` animation wrapper from `@/components/Reveal` on section headers
3. Use `OrderCTA` component from `@/components/OrderCTA` for all WhatsApp CTAs
4. Use `waLink()` from `@/data/site` for the WhatsApp links
5. Wire up the catering form to `ContactForm.tsx` pattern or create a new `CateringForm.tsx`
6. Add each page to the header nav in `Header.tsx` if not already there
7. Run `npm run build` and resolve any type errors
