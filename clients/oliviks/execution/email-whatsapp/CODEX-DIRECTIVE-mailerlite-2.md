# CODEX DIRECTIVE 2 — Fix the live MailerLite welcome emails (offer removal + new links)

Date issued: 2026-07-24. You (Codex) built the "Oliviks welcome sequence" in MailerLite
earlier and verified it delivers. Since then, three things changed and the LIVE emails
are now wrong. This is a MailerLite-UI-only job. Do not touch any code, the website
form, Supabase, the API key, or the integration.

## Why this is urgent
The client removed the "free puff puff with your first order" offer on 2026-07-15.
The website no longer promises it, but welcome Emails 1 and 2 still do. Every new
subscriber is currently promised a free item that no longer exists. Fix today.

## What changed since you built the emails
1. **Offer removed.** No free puff puff, no replacement offer. The list promises
   weekly specials only. (The "[BACKUP - INACTIVE] Oliviks welcome - 500 HUF off"
   automation is NOT to be activated; it is also obsolete now. Leave it inactive.)
2. **Domain is live.** oliviks.com now serves the new site (cutover 2026-07-24).
   All email links should use https://oliviks.com/... instead of
   https://oliviks-kitchen.vercel.app/...
3. **New opening hours.** Mon, Tue, Fri, Sat 11:00–20:00; Wed, Thu 11:00–18:00;
   Sun closed. Any hours line in the emails must match.

## Access
MailerLite in Chrome, Google SSO as olivikskitchen@gmail.com (same as before).
Automation: "Oliviks welcome sequence" (trigger: joins group "Oliviks subscribers",
id 192830261953562583). Keep the trigger, the delays (Email 1 immediate, +2d, +5d),
and the Active status exactly as they are. Edit only the email contents.

## Replacement copy (paste-ready; keep your existing formatting style — headings,
## paragraphs, spacing — which was already verified to render well)

### Email 1 — replace entirely
Subject: Welcome to Oliviks
Body:
Hi there,
Welcome to Oliviks. You are on the list for our weekly specials: what is good at the
kitchen each week, new dishes, and the occasional treat. No spam, and you can leave
any time.
If you have never ordered before, start with jollof rice, fried plantain, and puff
puff. That trio explains the whole menu.
Order for pickup: https://shop.oliviks.com
See the full menu: https://oliviks.com/menu
Come hungry.
Cynthia and Aese, Oliviks Kitchen
Rákóczi tér 9, 1084 Budapest. Mon, Tue, Fri, Sat 11:00 to 20:00. Wed, Thu 11:00 to 18:00.

### Email 2 — two edits only
1. Remove the line "If you have not claimed your free puff puff yet, it is still
   waiting." entirely (no replacement).
2. If any link points to oliviks-kitchen.vercel.app, change it to oliviks.com.
Everything else in Email 2 (the founders' story) stays as is.

### Email 3 — check only
No offer is mentioned, so likely fine. Just update any
oliviks-kitchen.vercel.app link to oliviks.com. Otherwise leave unchanged.

## VERIFY when done
1. Submit one real test signup at https://oliviks.com (scroll to the "Get the weekly
   specials first" band) with a Gmail +alias inbox you control.
2. Confirm the double opt-in confirmation arrives, click it, and confirm Email 1
   arrives with the NEW copy: no puff puff anywhere, links go to oliviks.com and
   shop.oliviks.com, hours line correct.
3. Open Emails 2 and 3 in the editor and visually confirm no "puff puff offer"
   wording and no vercel.app links remain anywhere in the sequence.
4. Delete your test subscriber from MailerLite afterwards so the real list stays clean.

## GUARDRAILS
- Edit email CONTENT only. Do not change the trigger, group, delays, or Active state.
- Do not activate, edit, or delete the 500 HUF backup automation. Leave it inactive.
- Do not touch route.ts, the website, Supabase, or the API key. Do not print the key.
- Do not create new automations or groups.
- If MailerLite login (Google 2FA) blocks you, stop and report; never make a new account.
