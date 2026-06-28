# Handoff: Oliviks Kitchen — Menu page update

## Overview
This package documents an updated **menu / "What We Cook"** page for Oliviks Kitchen (a Nigerian restaurant in Budapest). The live site is a Next.js app at `oliviks-kitchen.vercel.app`. The goal of this handoff is to bring a set of **content, link, and visual changes** into that existing codebase.

The bundled files were built as **design references in HTML** — prototypes that show the intended look, content, and behavior. They are **not** meant to be dropped into the site as-is. Recreate them inside the existing Next.js + React environment, using its established component, styling, and image patterns (e.g. `next/image`, the existing menu data source, the existing layout/header/footer components).

## Fidelity
**High-fidelity.** Colors, typography, spacing, copy, and interactions are final. Recreate the UI faithfully using the codebase's existing libraries/components. Exact token values are listed in **Design Tokens** below; the prototype references them as CSS variables (e.g. `var(--barn-red)`), which map to the brand's design system (also in this project under `tokens/` and `styles.css`).

---

## What changed (the actual work to port)

These are the concrete diffs to apply to the live site. If the menu is driven by a data file/CMS, most of this is data edits; the rest are component/markup edits.

### 1. Menu items, prices & options (reconciled to the printed in-store menu)
Full current menu is in **Menu Data** below. Key changes from the previous version:
- **Rice** switched from "with protein" bundles to **plain plates + protein add-on** model:
  - Jollof rice — **2,500 Ft** (was "from/2,500–4,000")
  - Fried rice — **2,500 Ft**
  - Pilau rice — **3,500 Ft** (previously "Beef Pilau 5,500")
  - Each Rice item shows an options note: *"Add a protein from Sides — grilled chicken, turkey, mackerel, or beef"*
- **Soups** all priced **4,700 Ft** with one swallow (was 5,000). Pepper soup **5,000 Ft** (now has a real price; was "Price soon").
- **New soups added:** Okro soup (4,700), Groundnut soup (4,700, note "Contains peanuts").
- **New sides added:** Fried mackerel (half cut) 2,000, Grilled turkey 1,500, Moi Moi 1,500.
- **Price corrections:** Grilled Chicken Thigh 1,000, Suya sticks 1,000, Poundo/Eba swallows 500 each, Meat Pie 1,000, Puff Puff 2,000, Chin Chin 1,000, Zobo/Malt/V-soy 1,000.
- **Fried Yam** 2,500 (now has photo).
- **Fish roll** description corrected — it is a fish roll (baked dough around deboned mackerel), **not** meat pie.

### 2. Vegetable soup — dried-fish variant
"Vegetable soup with one swallow" has a secondary thumbnail (a small circular sub-image, bottom-right of the main photo) plus the note: *"Dried fish variant on request, subject to availability."* Source images: `assets/dish-vegetable-soup.png` (main) and `assets/dish-vegetable-soup-fish.jpg` (variant).

### 3. Delivery links
- **Removed Foodora** everywhere (Oliviks is not active on Foodora).
- **Added Marwa:** `https://www.marwa.hu/store/113/oliviks-kitchen`
- Footer "Order & Delivery" list is now: Order Online (pickup) · Wolt · Marwa · WhatsApp.

### 4. Google rating block (hero card)
- Shows **`4.8★`** with the **official multicolor Google "G"** icon (inline SVG, in a white circle) and the label **"Rated on Google"**.
- **Review count removed** (previously "from 491 Google reviews"). Footer blurb also changed to "4.8★ rated on Google" (no count).

### 5. Header nav links activated
Previously `href="#"`. Now:
- **Menu** → `#menu` (anchors to the sticky category bar)
- **Catering** → `https://oliviks-kitchen.vercel.app/catering`
- **About** → `https://oliviks-kitchen.vercel.app/about`
- **Contact** → `https://oliviks-kitchen.vercel.app/contact`

(In the real Next.js app, use `next/link` with internal routes `/catering`, `/about`, `/contact` rather than absolute URLs.)

### 6. Visual elevation + animation (see Interactions section)
A warm top accent bar, hero glow, lighter card borders, section-title accent rule, plus entrance + scroll-reveal + hover animations.

---

## Screens / Views

### Menu page (single page)
**Purpose:** Let customers browse the full menu by category and jump out to order (pickup / Wolt / Marwa / WhatsApp).

**Layout (desktop, max content width 1180px, centered):**
1. **Sticky header** (`z-index:30`): 3px gradient accent strip on top (barn-red → papaya-orange → papaya-400), then a row: logo (height 46px) · nav (Menu/Catering/About/Contact) · right side: "Questions? WhatsApp" text link + "Order Online" pill button. Background `rgba(247,249,244,0.9)` with `backdrop-filter: blur(10px)`.
2. **Hero** (`padding:52px 28px 30px`): two-column grid `1.3fr 0.7fr`, gap 36px.
   - Left: eyebrow "Our dishes" (uppercase, barn-red, 12px, letter-spacing 0.16em) · H1 "What We Cook" (800, 60px, line-height 1.02, letter-spacing -0.025em) · intro paragraph (18px, line-height 1.6, max-width 560px) · a papaya "First time here?" pill · two CTAs (papaya "Order Online" solid + outlined barn-red "See the Menu").
   - Right: **barn-red info card** (`border-radius: var(--radius-xl)`=28px, `box-shadow: var(--shadow-lg)`): 4.8★ + Google G + "Rated on Google" · italic quote "Honest food with soul." · divider · Pickup address + Mon–Sat 11:00–20:00. A faint decorative `sparkle-mark.png` top-right.
   - Behind the hero, a soft radial papaya glow (`radial-gradient(closest-side, rgba(250,183,58,0.16), transparent)`).
3. **Press strip** (dark, `--surface-ink`): "As featured in — Origo · We Love Budapest · WMN".
4. **Category chips** (sticky, `top:74px`, `z-index:20`): All · Rice · Soups · Sides · Snacks · Drinks. Active chip = barn-red fill + white text; inactive = white fill, subtle border. Clicking filters which groups show.
5. **Menu groups** (`<main>`): for each visible category — H2 title (800, 32px) + blurb (16px, muted) + a 46×3px gradient accent rule, then a **3-column card grid** (gap 22px).
6. **"How ordering works"** note card (papaya-tinted) + Order Online / WhatsApp buttons.
7. **Footer** (dark `--neutral-900`): 4 columns — brand blurb · Visit (address/phone/email) · Hours · Order & Delivery links · bottom bar with copyright.

**Dish card component:**
- Container: `flex column`, `background: var(--surface-card)`, `border: 1px solid rgba(225,227,219,0.6)`, `border-radius: var(--radius-lg)` (20px), `box-shadow: var(--shadow-sm)`, `overflow:hidden`.
- **Media** (height 172px, `overflow:hidden`): the dish image, `object-fit:cover`, `width/height:100%`. Optional **"Popular"** badge (papaya pill, top-left) and **heat** badge (dark translucent pill, top-right, e.g. "Mild", "Warming", "Peppery", "Our hottest"). For the vegetable-soup variant, a 58px circular sub-image sits bottom-right with a small "Dried fish variant" label pill.
- **Body** (`padding:18px 20px`, gap 8px): title (700, 18px) + price (700, 15px, barn-red, right-aligned, `white-space:nowrap`) on one baseline row · description (13.5px, line-height 1.5, muted) · optional **options note** (12px, barn-red on `--red-50`, e.g. the protein/swallow note) · an "Order" / "Ask about this" pill button (papaya).

**Responsive:** card grid → 2 columns ≤860px, → 1 column ≤560px; hero → single column ≤860px; footer → 2 columns ≤860px.

---

## Interactions & Behavior

- **Category filter:** clicking a chip sets active category; "All" shows every group, otherwise only the matching group renders. Active chip styled barn-red.
- **Entrance animation (hero):** the 6 hero blocks fade + rise (`translateY(22px)→0`, opacity 0→1) over **0.72s**, easing `cubic-bezier(0.16, 1, 0.3, 1)` (`--ease-out`), staggered via `animation-delay` (40/110/190/240/270/350ms).
- **Scroll reveal (menu):** section titles, blurbs, accent rules, and each card fade + rise (`translateY(20px)→0`) over **0.6s** as they enter the viewport, via IntersectionObserver (threshold 0.12, `rootMargin: 0px 0px -6% 0px`). Cards in a row stagger ~55ms each.
- **Card hover:** lift `translateY(-7px)`, deepen to `--shadow-lg`, border → `--papaya-200`; the image inside zooms to `scale(1.06)` over 0.6s.
- **Button hover/press:** hover `translateY(-2px)` + raise shadow; active settles to `translateY(0)`.
- **Chip / nav / footer-link hover:** chips lift 1px; nav links get papaya-50 bg + barn-red text; footer links → papaya-orange.
- **Accessibility / robustness (important):**
  - Wrap all `opacity:0` entrance/reveal styles behind a JS-added `.om-ready` class on the page root, added on mount — so if JS fails, **content is never invisible**.
  - A **safety timeout (2.2s)** force-reveals everything (adds `.in` to reveal elements, clears `.om-anim` opacity/transform) in case IntersectionObserver never fires (background tab, reduced perf, SSR snapshot, etc.).
  - `@media (prefers-reduced-motion: reduce)` disables all animation/transition and forces final visible state.
  In React/Next this maps cleanly to: gate hidden state behind a `mounted` flag (`useEffect`), use an IntersectionObserver hook, and respect `prefers-reduced-motion`. SSR should render content visible by default.

## State Management
- `activeCategory` — `'All' | 'Rice' | 'Soups' | 'Sides' | 'Snacks' | 'Drinks'`. Controls chip styling + which groups render.
- `mounted` / reveal flags — for the animation guard described above.
- Menu data is static (see below); no data fetching required. In the real site, prefer sourcing it from the existing menu data module/CMS rather than hardcoding.

## Design Tokens
All tokens live in `tokens/` (colors.css, fonts.css, spacing.css) and are aggregated by `styles.css`. Key values used on this page:

**Colors**
- Barn Red (primary): `--barn-red`
- Papaya Orange (accent): `--papaya-orange` / ramp `--papaya-50 … --papaya-600` (e.g. `--papaya-400: #fcc865`, `--papaya-500: #fab73a`)
- Chalk White (page bg): `--chalk-white`; hero page bg uses a subtle `linear-gradient(180deg,#fffaf1 0,var(--chalk-white) 380px)`
- Surfaces: `--surface-card`, `--surface-sunken`, `--surface-accent`, `--surface-ink`, `--red-50`
- Neutrals: `--neutral-300 / -400 / -900`, `--text-strong / -body / -muted`, `--border-subtle`
- Google G icon colors (literal): `#4285F4 #34A853 #FBBC05 #EA4335`

**Typography**
- Primary (headings/labels/buttons): **Rubik** (`--font-primary`), weights 600/700/800
- Secondary (body): **Manrope** (`--font-secondary`)
- Notable sizes: H1 60px/800, section H2 32px/800, card title 18px/700, body 18px (hero) / 13.5–16px (content)

**Radius:** `--radius-sm`, `--radius-lg` (20px), `--radius-xl` (28px), pill `999px`
**Shadow:** `--shadow-xs / -sm / -md / -lg`, `--shadow-accent` (papaya glow `0 10px 28px rgba(250,183,58,0.35)`) — warm red-brown tinted, not black
**Motion:** `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`; entrance 720ms, reveal 600ms, hover 200–400ms

## Assets
All dish/brand images are in `assets/`. **New / changed photos** the live site likely needs added to its `/images` (or equivalent) folder:
- `dish-grilled-chicken.png`, `dish-grilled-turkey.png`, `dish-fried-mackerel.png`, `dish-fried-yam.png`, `dish-moi-moi.png`, `dish-okro-soup.png`, `dish-groundnut-soup.png`, `dish-coconut-peanut.png`, `dish-malta`→`drink-malta.png`, `dish-vegetable-soup-fish.jpg` (variant thumb), corrected `drink-zobo.jpg` (was swapped with the soup photo).
- Brand: `oliviks-logo-horizontal.png`, `sparkle-mark.png`.

In the prototype, images are resolved by a small `img(path)` helper: paths starting with `assets/` are used directly; anything else falls back to `https://oliviks-kitchen.vercel.app/_next/image?url=/images/<name>&w=1200&q=75`. **In the live app, just use `next/image` with the real `/images/...` sources** — ignore the prototype's blob/`__resources` indirection (that exists only for the offline standalone build).

## Files in this bundle
- `Oliviks Menu.dc.html` — the editable design prototype (single self-contained component; markup is the `<x-dc>` block, logic is the `<script data-dc-script>` class). **Primary reference.**
- `Oliviks Menu (standalone-offline).html` — fully inlined, offline-openable version (all images embedded). Handy for viewing the design without the project. Do not port code from this file — it's a compiled artifact.
- `assets/` — all images used.
- `tokens/` + `styles.css` — the Oliviks design-system token definitions referenced throughout.

## Menu Data
Categories in display order: **Rice, Soups, Sides, Snacks, Drinks.** Fields: name · price · description · options note (if any) · heat label (if any) · popular flag · image.

### Rice — "add a protein from Sides to build your plate"
| Item | Price | Heat | Options note | Image |
|---|---|---|---|---|
| Jollof rice *(Popular)* | 2,500 Ft | Warming | Add a protein from Sides — grilled chicken, turkey, mackerel, or beef | dish-jollof.png |
| Fried rice | 2,500 Ft | Mild | (same protein note) | dish-fried-rice.png |
| Pilau rice | 3,500 Ft | Warming | (same protein note) | dish-pilau-rice.png |

### Soups — "served with one swallow (pounded yam or eba)"
| Item | Price | Heat | Note | Image |
|---|---|---|---|---|
| Egusi soup with one swallow *(Popular)* | 4,700 Ft | Warming | Served with a swallow | dish-egusi.jpg |
| Oha soup with one swallow | 4,700 Ft | Warming | Served with a swallow | dish-oha-soup.png |
| Ogbono soup with one swallow | 4,700 Ft | Warming | Served with a swallow | dish-ogbono.png |
| Vegetable soup with one swallow | 4,700 Ft | Mild | Served with a swallow · **Dried fish variant on request, subject to availability** (sub-image: dish-vegetable-soup-fish.jpg) | dish-vegetable-soup.png |
| Bitter leaf soup with one swallow | 4,700 Ft | Warming | Served with a swallow | dish-soup.jpg |
| Okro soup with one swallow | 4,700 Ft | Mild | Served with a swallow | dish-okro-soup.png |
| Groundnut soup with one swallow | 4,700 Ft | Warming | Served with a swallow · **Contains peanuts** | dish-groundnut-soup.png |
| Pepper soup | 5,000 Ft | Peppery | — | dish-pepper-soup.png |

### Sides
| Item | Price | Heat | Image |
|---|---|---|---|
| Fried Yam | 2,500 Ft | Mild | dish-fried-yam.png |
| Moi Moi | 1,500 Ft | Mild | dish-moi-moi.png |
| Fried beef | 1,500 Ft | Warming | dish-suya-platter.jpg |
| Fried mackerel (half cut) | 2,000 Ft | Mild | dish-fried-mackerel.png |
| Grilled turkey | 1,500 Ft | Mild | dish-grilled-turkey.png |
| Grilled Chicken Thigh | 1,000 Ft | Mild | dish-grilled-chicken.png |
| Suya sticks *(Popular)* | 1,000 Ft | Our hottest | dish-suya-sticks.jpg |
| Poundo Swallow | 500 Ft | Mild | dish-poundo.jpg |
| Eba | 500 Ft | Mild | dish-eba.png |

### Snacks
| Item | Price | Heat | Image |
|---|---|---|---|
| Meat Pie | 1,000 Ft | Mild | dish-meat-pie.png |
| Coconut peanut | 1,500 Ft | Mild | dish-coconut-peanut.png |
| Spicy kuli kuli (one pack) | 2,000 Ft | Peppery | dish-kuli-kuli.png |
| Fried Plantain *(Popular)* | 2,500 Ft | Mild | dish-fried-plantain.jpg |
| Puff Puff *(Popular)* | 2,000 Ft | Mild | dish-puff-puff-fresh.jpg |
| Plantain chips | 1,000 Ft | Mild | dish-plantain-chips.png |
| Chin Chin | 1,000 Ft | Mild | (no photo) |
| Fish roll | 1,500 Ft | Mild | dish-fish-roll.jpg |

### Drinks
| Item | Price | Image |
|---|---|---|
| Chilled Zobo Drink | 1,000 Ft | drink-zobo.jpg |
| Chilled Malt 330 ml | 1,000 Ft | drink-malta.png |
| V-soy multi grain drink | 1,000 Ft | drink-vsoy.png |
| Fanta 330 ml | 1,000 Ft | drink-fanta.png |
| Coca-Cola Cherry Coke 330 ml | 1,000 Ft | drink-coke.png |

### Outbound links / constants
- Order Online (pickup): the site's existing order/checkout flow
- WhatsApp: existing WhatsApp contact link (used for "Questions?", "Ask about this", and the ordering note)
- Wolt: `https://wolt.com/en/hun/budapest/restaurant/oliviks-nigerian-kitchen`
- **Marwa: `https://www.marwa.hu/store/113/oliviks-kitchen`**
- Address: Rákóczi tér 9, 1084 Budapest · Phone +36 70 567 3070 · olivikskitchen@gmail.com · Mon–Sat 11:00–20:00, Sun closed
