# Oliviks Kitchen — Digital Systems Handover

**Prepared for:** Aese Agaigbe and Cynthia Chia, Oliviks Kitchen
**Prepared by:** Emmanuel Ehigbai, BridgeWorks
**Date:** 14 July 2026
**Engagement:** Foundation package (contract 29 April 2026)

This document is yours to keep. It lists everything that was built, every account you
own, and how to run each system day to day. No technical background is needed. Where a
password or key is involved, it is not written here. Passwords are shared privately.

**Verification note, 14 July 2026:** the new site is live on the Vercel preview, not
yet on `oliviks.com`. Supabase and MailerLite are connected. The live signup path still
needs an approved end-to-end test, and the WhatsApp broadcast list remains an owner
action. This note controls where older wording below sounds fully final.

---

## 1. What you now have

Four systems, working together:

1. **A new website** that tells your story and sends customers to your shop.
2. **Your existing WooCommerce shop**, restyled to match, secure again, and now carrying
   every dish on the menu.
3. **A customer list of your own** (email + WhatsApp), with automatic welcome emails.
4. **A stronger Google presence**: optimized profile, the Restaurant Guru award, and
   review handling.

How they connect: a customer finds you on Google → lands on the website → orders on the
shop → gets a branded receipt → joins your list → gets your weekly specials → orders
again. That last loop is the point of all of it.

---

## 2. Your accounts — what you own

| System | Where | Login |
|---|---|---|
| Website (marketing site) | oliviks-kitchen.vercel.app (soon oliviks.com) | Managed by BridgeWorks; content editable by you at /admin |
| Shop + orders (WooCommerce) | shop.oliviks.com/wp-admin | Your existing WordPress account (user: bridgeworks account also exists for us) |
| Email list (MailerLite) | dashboard.mailerlite.com | Sign in with Google as olivikskitchen@gmail.com |
| Customer list backup (Supabase) | supabase.com, project "oliviks-kitchen" | Your Supabase account |
| Domain + hosting + business email | namecheap.com | Your Namecheap account |
| Google Business Profile | business.google.com | Your Google account |
| WhatsApp Business | The phone with +36 70 567 3070 | Your phone |

Everything above belongs to Oliviks. BridgeWorks holds working access to deliver and
support, nothing more.

---

## 3. How to do the common things

### Change a menu item, price, photo, or availability
1. Go to **oliviks-kitchen.vercel.app/admin** (after the domain move: oliviks.com/admin).
2. Pick the dish from the list.
3. Edit the name, description, price, image, or switch it available/unavailable.
4. Paste the **admin access code** (shared privately) and press Save.
5. The public menu updates within about a minute.
Note: this edits the menu on the website. Prices on the shop are separate; change those
in WooCommerce (Products) because that is what customers actually pay.

### Send the weekly specials email (5 minutes)
1. Open MailerLite → Campaigns → Create.
2. Use the weekly specials template (in the "Email and WhatsApp pack" we handed over):
   fill in the dish, the price, one photo.
3. Send to the group **Oliviks subscribers**. Best time: Thursday or Friday, late morning.

### Send the same special on WhatsApp
1. On the +36 70 567 3070 phone, open WhatsApp Business → your broadcast list.
2. Paste the same text and photo. Each person receives it as a private message.
3. Anyone who replies STOP: remove them from the list.

### The sign-up offer
The website offer is **"Free puff puff with your first pickup order."** MailerLite has
an enabled, valid five-step welcome automation and an inactive 500 HUF-off backup.
The complete signup, confirmation, and welcome-email path still needs one approved
live test before it can be described as accepted. Once verified, customers show the
email at the counter to claim the offer.

### Respond to a Google review
Reply to every negative review, and to positive ones when you have something specific
to say. Short, warm, never copy-paste. From the Google Business app or
business.google.com → Reviews.

### The counter QR card
A print-ready card ("Get weekly specials first," with a QR that opens WhatsApp) is in
your handover pack. Print it A5 or A4 and stand it at the pickup counter.

---

## 4. Still open, and whose move it is

| Item | Whose move |
|---|---|
| Look at the new site and approve it (or send changes) | You |
| Point oliviks.com at the new site (15 min, after your approval) | BridgeWorks |
| Create the WhatsApp broadcast list on the business phone | You (we guide) |
| Print the counter QR card | You |
| Balance invoice EO-2026-13 (136,305 HUF, due 19 July) | You |
| Review online prices for the 9 newly added shop products | You (tell us the markups, we set them) |

One note on prices: the website shows your in-store menu prices, and says clearly that
online/delivery prices include a small markup. The shop charges the online price. If any
online price looks wrong, tell us the right number and we change it the same day.

---

## 5. Looking after it going forward

Everything handed over runs on free tiers today: hosting, the database, and the email
tool (free up to 1,000 subscribers). Two dates to know:

- **9 October 2026** — the oliviks.com certificate renews. It is set up to be handled;
  we flag it here for completeness.
- **MailerLite** becomes paid only if your list grows past 1,000 subscribers. A good
  problem.

Running these systems weekly (specials emails, WhatsApp broadcasts, Google posts,
review replies, listing updates, the blog) is exactly what the optional Growth Retainer
in your proposal covers. The Foundation built the machine. The retainer drives it. If
you want that, say so; if you prefer to run it yourselves, this document plus the
Email and WhatsApp pack is everything you need.

For anything at all: office@bridgeworks.agency.

---

## Appendix — for any future technician

- Marketing site: Next.js 15, hosted on Vercel (project oliviks-kitchen). Code managed
  by BridgeWorks. Menu content: Supabase project toltnysainnkpxfxibff (tables
  menu_categories, menu_items, menu_option_groups, menu_options, subscribers), public
  reads via anon key with row-level security, writes server-side only.
- Shop: WordPress + WooCommerce on Namecheap shared hosting (server72.web-hosting.com),
  shop.oliviks.com as an add-on domain with its own SSL (PositiveSSL, renews via
  Namecheap). Order emails send as "Oliviks Kitchen" <olivikskitchen@gmail.com>.
- Sign-up flow: website form → /api/subscribe → Supabase insert (consent required) →
  MailerLite group "Oliviks subscribers" (double opt-in on).
- DNS: managed on Namecheap hosting nameservers. Mail (MX jellyfish.systems) and the
  shop A record must never be touched during website changes.
- Domain flip runbook, brand CSS for the shop, and all templates live in the BridgeWorks
  engagement records and can be re-shared on request.

*Oliviks Kitchen · Rákóczi tér 9, 1084 Budapest · Come hungry.*
