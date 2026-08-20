# Wedding site

Private, password protected wedding website. Next.js App Router, Tailwind, Resend
for RSVP notifications, Supabase for the stored guest list.

## Fill in the content

Everything a guest reads lives in `src/data/wedding.ts`. Edit that one file.
Any value still starting with `TODO:` shows on the page inside a marked box, so
placeholder text can never be mistaken for real copy.

Photos go in `public/photos/`, then get listed in `wedding.gallery.photos` with
alt text for each one.

## Environment

Copy `.env.example` to `.env.local` and fill it in.

| Variable | What it is |
|---|---|
| `SITE_PASSWORD` | The shared word printed on the invitations |
| `SESSION_SECRET` | Any long random string, used to hash the unlock cookie |
| `RESEND_API_KEY` | From resend.com, sends the RSVP notification |
| `RSVP_TO` | The family inbox that receives every RSVP |
| `RSVP_FROM` | Verified sender address in Resend |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Server only key, never exposed to the browser |

Generate a session secret:

```
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## Run it

```
npm install
npm run dev
```

Without `SITE_PASSWORD` and `SESSION_SECRET` every route redirects to `/unlock`,
which says what is missing. That is deliberate: a half configured deploy stays
shut rather than quietly going public.

## The guest list

Run `supabase/schema.sql` once in the Supabase SQL editor. The table has row
level security on with no policies, so only the server, using the service role
key, can read or write it.

RSVPs are also emailed to `RSVP_TO`. The two paths are independent. If only one
is configured, replies still land. If neither is configured, the form tells the
guest the truth instead of faking a success.

Resubmissions are stored as new rows rather than overwriting, so a change of
plan stays visible. The schema file carries a query for counting the latest
reply per guest.

## How the lock works

A shared passphrase, checked by `src/middleware.ts` in front of every route and
API call except the unlock endpoint. The cookie holds a SHA-256 digest of the
passphrase plus `SESSION_SECRET`, never the passphrase itself.

This is invite-level privacy. It keeps the site out of search results and out of
casual hands. It is not a vault: anyone with the word can share it with anyone
else, so treat the link and the word the way you would treat a paper invitation.

## Deploying

Vercel, with the root directory set to `personal/wedding-site`. Add every
variable above to the project settings before the first deploy, otherwise the
site opens locked and stays that way.
