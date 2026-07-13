# CODEX DIRECTIVE — Finish Oliviks A3 (MailerLite UI + WooCommerce email)

You are finishing the last UI steps of the Oliviks "Email & WhatsApp Infrastructure"
(Foundation deliverable A3). The API connection is already built and live. Your job is
the browser-UI work that the API cannot do. Do NOT rebuild the integration.

## Brand voice (apply to anything you write/edit)
No em dashes. No AI slop (world-class, seamless, elevate, etc.). Short sentences.
Warm, specific. From name: "Oliviks Kitchen".

## Repo + key paths
- Repo root: `C:\Users\User\Projects\bridgeworks-workspace\clients\oliviks`
- Site code: `clients/oliviks/website` (Next.js on Vercel, project `oliviks-kitchen`, live at https://oliviks-kitchen.vercel.app)
- Subscribe API (already wired, DO NOT CHANGE logic): `clients/oliviks/website/src/app/api/subscribe/route.ts`
- Drafted copy: `clients/oliviks/execution/email-whatsapp/` (welcome-sequence.md, weekly-specials-template.md, whatsapp-broadcast-template.md, HANDOVER.md)

## What is ALREADY DONE (do not redo)
- Live sign-up form on the homepage (email + optional WhatsApp + GDPR consent), stores to Supabase AND pushes to MailerLite. Verified end-to-end 2026-07-13.
- MailerLite group **"Oliviks subscribers"**, id **192830261953562583**, already receiving signups.
- `MAILERLITE_API_KEY` and `MAILERLITE_GROUP_ID` are set in `clients/oliviks/website/.env.local` (gitignored) and in Vercel production env. Do not print or commit the key.
- `/privacy` page live. Consent is captured + timestamped in Supabase, so the list is already GDPR-lawful on single opt-in.

## MailerLite access
Account was created by the client, login via **"Sign in with Google"** as
**olivikskitchen@gmail.com**. There may be Google 2FA (phone). If you cannot complete
login, stop and tell Emmanuel; do not create a second account.
Dashboard: https://dashboard.mailerlite.com

---

## TASK 1 — Enable double opt-in (2 min)
MailerLite: Settings → (Subscribe settings / Security & privacy) → enable
**"Enable double opt-in"**. Save. This makes new API subscribers receive a
confirmation email before they get campaigns. Optional for compliance (consent is
already logged) but recommended for deliverability.

## TASK 2 — Build the 3-email Welcome automation (main task)
MailerLite → Automations → Create workflow.
- Trigger: **"When subscriber joins a group"** → group **Oliviks subscribers**.
- Add 3 emails with delays. Full copy below (also in welcome-sequence.md). Incentive
  wording: **"Free puff puff with your first pickup order"** (redeemed by showing the
  email at the counter — confirm with Aese if she wants a code instead).

**Email 1 — sends immediately**
Subject: Your free puff puff is waiting
Body:
Hi there,
Welcome to Oliviks. You just earned free puff puff with your first pickup order.
Here is how to claim it: order for pickup at Rákóczi tér 9, show this email at the counter, and the puff puff is on us.
If you have never had ours: it is lightly sweet, golden, and hard to stop at one.
Order for pickup: https://shop.oliviks.com
See the full menu: https://oliviks-kitchen.vercel.app/menu
Come hungry.
Cynthia and Aese, Oliviks Kitchen
Rákóczi tér 9, 1084 Budapest. Mon to Sat, 11:00 to 20:00.

**Email 2 — 2 days after Email 1**
Subject: Why we opened a Nigerian kitchen in Budapest
Body:
Hi again,
A quick story about why Oliviks exists.
We came to Hungary to study. Both of us did our Masters in Debrecen, far from Lagos and far from the food we grew up on. Real Nigerian cooking was not on the menu anywhere.
So we cooked it ourselves. Oliviks is a Nigerian kitchen, not an African-themed one. The recipes come from Cynthia's family table, made from scratch.
Budapest answered. Nigerians looking for home, Hungarians trying egusi for the first time, students, regulars who never left the menu. Most order again.
If you have not claimed your free puff puff yet, it is still waiting.
Order for pickup: https://shop.oliviks.com
Cynthia and Aese

**Email 3 — 5 days after Email 2**
Subject: What is good this week at Oliviks
Body:
Hi,
From now on we will send the occasional note about what is good that week: specials, new dishes, the odd treat for people on this list. No spam. Leave any time.
First time deciding what to order? Start here:
- Jollof rice, the dish our parties are built around
- Fried plantain, soft, sweet, the easy balance to anything peppery
- Suya sticks, smoky, our hottest, hard to stop eating
Order for pickup: https://shop.oliviks.com
See you soon,
Cynthia and Aese, Oliviks Kitchen

Set the automation status to **Active** when built.

## TASK 3 — WooCommerce order-receipt email — DONE 2026-07-14 (do not redo)
Rebranded via the WooCommerce REST API: from name "Oliviks Kitchen", from address
olivikskitchen@gmail.com (was the previous dev's personal gmail), base color barn red
#761212, chalk background, ink text, Oliviks footer.
Two optional enhancements left for whoever has the WP UI + a proper asset:
1. Upload a WHITE/inverted Oliviks logo as the email header image (a dark logo would
   clash on the barn-red header, so none was set).
2. Deliverability: from-address is a gmail on a non-gmail server, so SPF/DKIM won't
   cover it and receipts may land in spam. Better long-term: a domain address like
   no-reply@oliviks.com (needs that mailbox created on Namecheap Private Email).

## TASK 1 + 2 STATUS (done 2026-07-14, verified by Claude)
Double opt-in enabled, welcome automation built and Active (trigger: joins group
"Oliviks subscribers"; Email 1 immediate, +2 days Email 2, +5 days Email 3).
Integration verified end-to-end: a live signup lands in Supabase + MailerLite and now
arrives as **unconfirmed** (proving double opt-in works). Group + automation correct.

## TASK 4 — Verify the MailerLite SENDER so emails actually send (THE LAST STEP)
Problem found during verification: no confirmation email is delivered yet, because a
brand-new MailerLite account cannot send anything until a sender identity is verified
(and the account may need a one-time sending approval). Until this is done, signups are
captured but no confirmation/welcome/specials emails go out.

Do the QUICK path (no DNS):
1. MailerLite (logged in, Google SSO as olivikskitchen@gmail.com) → Settings →
   Domains / "Sender" / "Verify email".
2. Add sender email **olivikskitchen@gmail.com** (matches the WooCommerce from-address).
3. MailerLite emails a verification link to olivikskitchen@gmail.com. Open that inbox
   (Emmanuel has client email access) and click the link to verify.
4. If MailerLite shows an account-approval / "request sending access" form for the new
   account, complete it honestly (restaurant sending weekly specials + order-related
   updates to opted-in customers).

OPTIONAL later upgrade (better inbox delivery, needs DNS): verify the whole domain
oliviks.com — MailerLite gives SPF/DKIM/CNAME records to add in cPanel DNS Zone Editor.
This is NOT the domain flip; it only adds email records and changes nothing about the
website. Leave for later unless asked.

After verifying, re-run the VERIFY steps below. Emails should then deliver.

---

## VERIFY when done
1. Turn double opt-in behaviour on, then submit a real test signup on
   https://oliviks-kitchen.vercel.app (scroll to "Free puff puff" band). Use an inbox
   you control.
2. Confirm you receive the confirmation email (if double opt-in on), then Email 1 of
   the welcome sequence.
3. In MailerLite, confirm the subscriber is in "Oliviks subscribers" and entered the
   automation.
4. Delete your test subscriber from MailerLite afterwards so the real list stays clean.

## OUT OF SCOPE (needs the client, do not attempt)
- WhatsApp broadcast list + counter QR: needs the business WhatsApp number from Aese.
  Templates ready in whatsapp-broadcast-template.md.
- Final incentive wording / redemption method: confirm with Aese.

## GUARDRAILS
- Do not modify `route.ts` or the MailerLite/Supabase integration; it is verified.
- Do not change the group id or create new groups.
- Do not print, paste, or commit `MAILERLITE_API_KEY`.
- If MailerLite login (Google 2FA) blocks you, stop and report; do not make a new account.
