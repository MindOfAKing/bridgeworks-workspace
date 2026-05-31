# Misi's Gin: Engagement Task List

**Client:** Misi's Gin (Kenyeres Mihály E.V.), Budapest
**Owner:** Emmanuel / BridgeWorks
**Prepared:** 2026-05-31
**Scope:** GEO Foundation Fix (one-time) + optional Visibility Care (retainer)
**Source audits:** GEO-AUDIT-misisgin.md, MARKETING-AUDIT-misisgin.md

This is your execution checklist if the engagement is approved. Tasks are sequenced so each phase unblocks the next. Every task says what to do, where, and how to confirm it is done. The site is WordPress (Brando theme, WPBakery page builder, TranslatePress for the 6 languages). No coding required. Most work is done through plugins and the page builder.

---

## Phase 0: Access and Setup (Day 1 to 3)

Get these before any work starts. Without them you are blocked.

- [ ] **WordPress admin login** from Misi (admin-level user, not editor)
- [ ] **Hosting/cPanel access** at Aruba (needed for the crawler unblock and security headers)
- [ ] **Wordfence access** (it is the likely cause of the GPTBot/ClaudeBot block). Confirm the plugin is installed and you can reach its settings
- [ ] **Domain registrar / DNS access** (only if Google Business Profile verification or email needs it)
- [ ] **Confirm the product facts in writing from Misi:** exact ABV (retailers say 40%, one award body says 40.5% - confirm), bottle size (0.5L), full botanical list, the yuzu/kaffir lime story, batch size (~70 bottles), direct price, and whether he wants to sell direct online
- [ ] **Confirm the 2022 World Gin Awards Country Winner Hungary detail** and get the official tasting note text
- [ ] **Get the 19 partner venues as a list with links** (websites or Google Maps), split into "buy online here" vs "drink here"
- [ ] **Get founder photo(s)** and permission to use the personal story and name (Mihály Kenyeres)
- [ ] **Full WordPress backup before touching anything** (UpdraftPlus or host snapshot). Verify the backup downloads and opens
- [ ] **Set up a staging copy if the host allows it**, so changes are tested before going live

---

## Phase 1: Critical Fixes (Week 1)

These clear the issues that make the brand invisible and legally exposed. Highest priority.

### 1.1 Unblock the AI crawlers
- [ ] In Wordfence, find the rule blocking GPTBot and ClaudeBot (Tools > Live Traffic / Blocking). Whitelist both user agents
- [ ] If Wordfence is not the cause, ask Aruba support to remove GPTBot and ClaudeBot from any proxy bot-blocking rules
- [ ] **Verify:** run `curl -A "GPTBot/1.0" https://www.misisgin.com/` and `curl -A "ClaudeBot" https://www.misisgin.com/` and confirm both return HTTP 200, not 404. Re-test both the HU and EN homepages

### 1.2 Install the SEO foundation
- [ ] Install and activate **Rank Math** (or Yoast) SEO plugin
- [ ] Run its setup wizard, connect Google Search Console
- [ ] Set a unique, keyworded **title and meta description per language**. Example EN title: "Misi's Gin: Award-Winning Hungarian Craft Gin from Budapest". Example HU title: "Misi's Gin: Díjnyertes magyar kézműves gin | Budapest"
- [ ] **Verify:** view page source, confirm the title is no longer the duplicate "Misi's Gin – Misi's Gin" and a meta description is present

### 1.3 Add structured data (schema)
- [ ] Add **LocalBusiness/Distillery schema** with name, address (1141 Budapest, Paskál-malom utca 3), phone, email, founding date, awards, and sameAs links to Facebook, Instagram, TikTok. JSON-LD is ready in GEO-AUDIT-misisgin.md Appendix B
- [ ] Add **Person schema** for Mihály Kenyeres (founder/distiller) with the confirmed bio
- [ ] Add **Product schema** for the gin (name, ABV, size, image, awards as `award` properties)
- [ ] Add the JSON-LD via Rank Math's custom schema field or the theme header, server-rendered, not via a JavaScript widget
- [ ] **Verify:** test both pages in Google Rich Results Test and schema.org validator, confirm no errors

### 1.4 Fix the sitemap and robots.txt
- [ ] Let Rank Math regenerate a clean sitemap that includes all 6 language home pages with correct lastmod dates
- [ ] Remove or fix the stale 2015 `/blog/` entry
- [ ] Add a `Sitemap:` directive line to robots.txt pointing at the new sitemap
- [ ] Submit the sitemap in Google Search Console
- [ ] **Verify:** open the sitemap URL, confirm all language versions are listed; confirm Search Console accepts it

### 1.5 Show price and product spec (the biggest conversion unblock)
- [ ] Add a clear product block to the page: bottle size, ABV, botanical list, tasting notes, and price (or "from X HUF")
- [ ] **Verify:** price, size, and ABV are visible without contacting anyone

### 1.6 Legal and compliance layer
- [ ] Add an **age-verification gate** (18+) before content loads, localized per language. Use a lightweight plugin (e.g. Age Gate)
- [ ] Publish a **privacy policy** (GDPR) and an **impressum** (Hungarian requirement for an EV), link both in the footer
- [ ] Surface the ÁSZF/terms clearly in the footer
- [ ] **Verify:** the age gate appears on first visit; privacy policy and impressum are reachable from every page

---

## Phase 2: Conversion and Content (Week 2)

Turn the brochure into something that sells.

### 2.1 Build the purchase path
- [ ] Add a **"Buy / Pour it here" block**: the partner retailers as clickable cards (lead with online sellers: ginshop.hu, iDrinks, totaldrinks.hu), and the bars as a separate "As served at" list
- [ ] Add a **direct order option**: at minimum a clean order form (name, product, quantity, email/phone) plus a `mailto:` button pre-filled with subject "Order: Misi's Gin". Add a tap-to-call button and a WhatsApp or Messenger link for mobile
- [ ] (If Misi wants full direct sales) scope a simple **WooCommerce** setup: one product, flat-rate Hungarian shipping, bank transfer or SimplePay/Stripe. Only after the form proves demand
- [ ] **Verify:** a visitor can reach at least one working purchase path in one click on both desktop and mobile

### 2.2 Rewrite the homepage messaging
- [ ] Replace the bare "Misi's Gin" headline with an informative one, for example "Gold-medal Hungarian craft gin from Budapest, with a Japanese citrus character". Keep the friendship tagline as a supporting line
- [ ] Add a **value-proposition block** directly under the headline (story + proof + origin + personal service in about four sentences)
- [ ] Add the **2022 Country Winner Hungary award** and link all awards to the awarding bodies
- [ ] Fix the **"occured" typo** in the EN founder story
- [ ] **Verify:** a first-time visitor understands what the product is and why it matters within 5 seconds

### 2.3 Build the trust wall
- [ ] Awards as **badges linked to the award bodies**
- [ ] Add **3 to 5 short testimonials/quotes**: one partner bartender, one retailer, one customer (collect these from Misi)
- [ ] Show the **"as served at" venue logos** as social proof
- [ ] **Verify:** the page now carries proof beyond the 2021 medals

### 2.4 Finish the cocktail content
- [ ] Add **method steps** (2 to 3 lines) and a "why this works with Misi's" line to each of the three cocktails
- [ ] Add **Recipe schema** to each cocktail (JSON-LD ready in the GEO audit appendix for the Negroni)
- [ ] **Verify:** cocktails validate as Recipe schema and read as usable recipes

### 2.5 Email capture
- [ ] Add a **newsletter signup** (one field) with an incentive: "Get the next batch and Christmas gift sets first". Connect to a simple tool (MailerLite or Mailchimp free tier)
- [ ] **Verify:** a test signup lands in the list

---

## Phase 3: SEO Structure (Weeks 3 to 4)

The real fix for losing the brand's own search results to retailers.

- [ ] **Split the single page into real pages** with their own URLs: Home, The Gin (product), Awards, Cocktails, Order/Shop, Gift, Story/About
- [ ] Give each page its own **title, meta description, one H1, and proper H2/H3 hierarchy** (current headings are styling-only H5/H6)
- [ ] Target one keyword cluster per page: The Gin = "magyar kézműves gin / craft gin Budapest"; Awards = "díjnyertes magyar gin"; Gift = "gin ajándék"; Order = "Misi's gin rendelés / ár"
- [ ] Add **internal links** between the new pages
- [ ] Add **Open Graph and Twitter card tags** (Rank Math handles this) so shared links and press coverage pull a proper card
- [ ] Build a **"Press / As seen in" page** linking existing coverage (szeretlekmagyarorszag.hu, Roadster, Székely Konyha) for ranking authority
- [ ] Re-submit the updated sitemap to Search Console
- [ ] **Verify:** each new page has a unique title, one H1, and validates schema; Search Console indexes the new URLs

---

## Phase 4: Performance and Hardening (Week 4)

- [ ] Add a **caching/optimization plugin** (e.g. LiteSpeed Cache or WP Rocket): combine/defer the 30 stylesheets and 59 scripts, defer jQuery
- [ ] Serve **WebP/AVIF images** for the galleries (the optimization plugin or a converter plugin handles this)
- [ ] Add **security headers** via the host or a plugin: Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and a basic CSP
- [ ] Publish an **llms.txt** at the root summarizing the brand, product, awards, and key URLs
- [ ] **Verify:** run PageSpeed Insights and confirm LCP/INP improved; confirm security headers present via a header checker; confirm llms.txt loads

---

## Foundation Fix: Definition of Done

The one-time engagement is complete when all of the following are true:

- [ ] GPTBot and ClaudeBot both return 200
- [ ] LocalBusiness, Person, Product, and Recipe schema present and validating
- [ ] Price, ABV, size, and botanicals visible on-site
- [ ] At least one working purchase path in one click
- [ ] Age gate, privacy policy, and impressum live
- [ ] Unique titles and meta descriptions per language
- [ ] Sitemap complete with all languages and submitted to Search Console
- [ ] Trust wall (linked awards + testimonials + venue logos) live
- [ ] Email capture working
- [ ] Re-run the GEO audit and confirm a materially higher score

---

## Optional: Visibility Care (Monthly Retainer)

Ongoing work that compounds. Only if Misi takes the retainer.

**Each month:**
- [ ] One AI-visibility check (is the site readable and being cited) plus a short progress note to Misi
- [ ] 1 to 2 new content pieces or cocktail recipes with proper schema
- [ ] Monitor Search Console for new rankings on the target keywords

**Across the first 90 days:**
- [ ] Prepare and submit a **Wikidata entry** for the brand and founder (acceptance is the platform's call, not guaranteed)
- [ ] Set up and optimize a **Google Business Profile** (service-area distillery, Budapest) with full NAP, category, and photos
- [ ] Authentic participation in **Reddit (r/gin, r/cocktails) and Hungarian spirits communities**, within each platform's rules

**Growth initiatives to plan and ship (this quarter):**
- [ ] **Christmas/seasonal gift set** (numbered bottle, glass, tasting card) for Q4, tied to the email list
- [ ] **Paid Budapest distillery tasting/experience**, sold via the site and tourism channels (GetYourGuide, hotel concierge)
- [ ] **HoReCa-to-direct bridge**: QR table cards at partner venues ("Enjoyed Misi's here? Order a bottle")
- [ ] **B2B/export/wholesale page** (distributor enquiry, MOQ, trade contact) to convert the multilingual export ambition
- [ ] Consolidate the 6 thin language versions into deep EN and HU first, add languages back only with full content

---

## Notes and Risks

- The age gate, privacy policy, and impressum are a legal requirement, not optional polish. Do these in Week 1 even if other items slip.
- Confirm ABV before publishing schema: retailers list 40%, one award body lists 40.5%. Use whatever Misi confirms is on the current label.
- Wikidata and Wikipedia inclusion cannot be promised. Treat as best-effort groundwork.
- Back up before each phase. The site uses a page builder, so test structural changes on staging where possible.
- Keep all client-facing copy in Misi's voice and bilingual where it faces customers.

---

*office@bridgeworks.agency · bridgeworks.agency*
