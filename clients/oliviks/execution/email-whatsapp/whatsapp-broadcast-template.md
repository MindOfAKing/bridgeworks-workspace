# Oliviks — WhatsApp Broadcast (Foundation A3, deliverable #7)

The WhatsApp side of the retention system. Open rates on WhatsApp run 70–90% vs
20–30% on email, so for weekly specials this is the strongest channel.

**Business WhatsApp number (confirmed 2026-07-14):** +36 70 567 3070 — the same number
used across the website. Join link: https://wa.me/36705673070?text=Join%20the%20Oliviks%20specials%20list

Still needs from Aese: create the broadcast list inside the WhatsApp Business app on
that number's phone, and add opted-in contacts to it (this is a manual in-app step).

---

## Opt-in message (reply to send when someone asks to join via the counter QR or the site)

Hi, and welcome to Oliviks 🎉
You are on our specials list. Once a week we will send you what is good at the kitchen,
nothing more. Reply STOP anytime to leave.
Your free puff puff is waiting on your first pickup at Rákóczi tér 9.

---

## Weekly broadcast text (paste, swap the [brackets], attach one photo)

**Oliviks this week 🍛**
[Dish name] — [price] Ft. [One line: what it is / why it is good this week.]

Order pickup at Rákóczi tér 9 → shop.oliviks.com
Or find us on Wolt and Marwa.
Come hungry. Reply STOP to leave the list.

---

## Counter QR code (deliverable #7) — DONE, ready to print

Print-ready assets are in `print-assets/`:
- `oliviks-whatsapp-counter-card.png` — full branded counter card (barn red, QR, offer).
  Print at A5/A4 and stand it at the pickup counter.
- `oliviks-whatsapp-qr.png` — the bare QR (barn red on chalk) if you want to place it
  in your own layout.

Both encode: `https://wa.me/36705673070?text=Join%20the%20Oliviks%20specials%20list`
Scanning opens WhatsApp to the Oliviks number with "Join the Oliviks specials list"
pre-filled. Aese replies with the opt-in message below and adds them to the broadcast
list.

---

## GDPR
Only broadcast to people who opted in (QR, counter, or website). Honor STOP replies
immediately. Keep the list in WhatsApp Business, not a personal number.
