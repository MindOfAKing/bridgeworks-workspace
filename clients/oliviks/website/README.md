# Oliviks Nigerian Kitchen — Website

The real Website Upgrade for Oliviks Kitchen (BridgeWorks Foundation engagement).
Next.js 15 (App Router) + TypeScript + Tailwind + framer-motion. Deploys to Vercel.

This replaces the Manus teaser. You own this code.

## HOW TO USE (non-technical)

1. **See it locally:** open a terminal in this folder and run `npm install` then `npm run dev`. Visit http://localhost:3000.
2. **Change business info** (address, phone, hours, reviews): edit `src/data/site.ts`. One file, plain text.
3. **Change the menu / add prices:** edit `src/data/menu.ts`. Each dish has a `price` (set it like `'2,500 Ft'`) and an `image`.
4. **Add real photos:** drop files in `public/` and set the `image` path on a dish, e.g. `image: '/jollof.jpg'`. Until then a branded placeholder shows automatically.
5. **Publish:** push to GitHub and connect to Vercel, or run `vercel`. See Deploy below.

## What's built

- Pages: Home, Menu (filterable, all 23 dishes), About (Cynthia & Aese story), Contact (map + working form), 404.
- Restaurant JSON-LD schema (`src/lib/schema.ts`) for Google + AI search.
- Meta + Open Graph tags on every page.
- Scroll animations, mobile menu, animated transitions.
- Working contact form via Resend (see Env below). No fake "message sent".

## Before going live (client confirmations needed)

- [ ] **Prices** — fill every `price` in `src/data/menu.ts` from the WooCommerce / current menu. Contract requires visible prices.
- [ ] **Photos** — 30–50 real photos from the client (per agreement section 6).
- [ ] **Exact address geo** — confirm map pin location in `src/data/site.ts`.
- [ ] **Ordering method** — owners deciding direct-order flow. Currently WhatsApp + Call. See `src/components/OrderCTA.tsx`.
- [ ] **Foodora/Wolt** — kept OFF (`site.ordering.showPlatforms = false`) per client. Flip in `site.ts` if they change their mind.

## Environment variables (for the contact form)

Set these in Vercel (Project → Settings → Environment Variables):

| Variable | Purpose |
|---|---|
| `RESEND_API_KEY` | API key from resend.com. Without it the form returns an honest error and points users to WhatsApp. |
| `CONTACT_TO` | Inbox that receives enquiries (defaults to olivikskitchen@gmail.com). |
| `CONTACT_FROM` | Verified sender, e.g. `Oliviks <hello@oliviks.com>`. For testing, `onboarding@resend.dev` works to the Resend account owner. |

## Deploy to Vercel

```
npm install -g vercel   # if needed
vercel                  # first deploy (link / create project)
# add env vars in the Vercel dashboard, then:
vercel --prod
```

Point `oliviks.com` at the Vercel project (Domains tab) once the client approves the content.

---
BridgeWorks · office@bridgeworks.agency
