# Oliviks — Email & WhatsApp Handover (Foundation A3, deliverable #9)

How the retention system works and how to run it. Written for Aese and Cynthia.
No technical background needed.

---

## What you now have

A way to turn one-time and delivery customers into regulars who order direct.
When someone joins your list on the website, their email (and optional WhatsApp
number) is saved to your own private list, with their consent recorded. You can then
send them weekly specials.

- **Sign-up form:** on the website homepage ("Free puff puff with your first pickup
  order"). Live now.
- **Your list:** stored securely in your own database. Only you can see it. It exports
  to an email tool (MailerLite) when you are ready to send.
- **The offer:** free puff puff on a first pickup order. Change the wording anytime.

---

## What is done vs. what needs you

**Done and live:**
- Website sign-up form (email + WhatsApp + consent)
- Private subscriber list (you own it)
- Privacy policy page
- MailerLite group `Oliviks subscribers` connected to the website configuration
- Enabled and valid five-step `Oliviks welcome sequence` automation
- Welcome emails written (3), weekly specials template (EN + HU)

**Still needs proof or an owner action:**
1. **End-to-end signup test.** On 2026-07-14 MailerLite contained one unconfirmed
   subscriber, the automation had qualified zero subscribers, and Supabase contained
   zero subscriber rows. The form-to-database-to-double-opt-in-to-welcome-email path
   is not yet proven.
2. **WhatsApp broadcast list.** Create the list on the business phone using
   +36 70 567 3070. BridgeWorks can guide this but cannot complete the in-app step.
3. **Counter card.** Print and place the prepared QR card.
4. **Offer acceptance.** Confirm the free-puff-puff wording and counter redemption
   method in writing.

---

## How to send a weekly specials email (5 minutes)

1. Open MailerLite → Campaigns → New.
2. Open the weekly-specials template. Fill in the dish, price, and one photo.
3. Send to "All subscribers." Best time: Thursday or Friday, late morning.
4. Paste the same text into your WhatsApp broadcast (see below).

## How to send a WhatsApp broadcast

1. In WhatsApp Business, open your Oliviks broadcast list.
2. Paste the weekly special text and one photo. Send.
3. Each person receives it as a private message, not a group.
   (Open rates on WhatsApp are far higher than email — this is your best channel.)

## How to add a subscriber by hand

Someone gives you their email at the counter? Add them in MailerLite →
Subscribers → Add. Only add people who agreed to be emailed (GDPR).

---

## The rules that keep you legal (GDPR)

- Only email people who ticked the consent box or clearly agreed. The website form
  does this automatically.
- Every email must have an unsubscribe link. MailerLite adds this for you.
- If someone asks to be removed, remove them.

---

## Files in this folder
- `welcome-sequence.md` — the 3 welcome emails
- `weekly-specials-template.md` — the fill-in weekly email (EN + HU)
- `whatsapp-broadcast-template.md` — WhatsApp opt-in + weekly message text
- This handover
