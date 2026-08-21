# Wedding site

Private, password protected wedding website. Next.js App Router, Tailwind, Resend
for RSVP notifications, Supabase for the stored guest list.

## Fill in the content

Everything a guest reads lives in `src/data/wedding.ts`. Edit that one file.
Any value still starting with `TODO:` shows on the page inside a marked box, so
placeholder text can never be mistaken for real copy.

Photos go in `public/photos/`, then get listed in `wedding.gallery.photos` with
alt text for each one. Resize them to roughly 1600px on the long edge first.
They are served straight from `public/` behind the passphrase gate rather than
through Next's image optimizer, because the optimizer's internal fetch carries
no cookie and the gate turns it away. Keeping the gate is worth more here than
automatic resizing.

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
| `NEXT_PUBLIC_PREVIEW_SAMPLE` | Preview only. `1` renders invented sample content. Never set it on a live deploy |

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

## Seeing the design before the content exists

```
NEXT_PUBLIC_PREVIEW_SAMPLE=1 npm run dev
```

That swaps in `src/data/wedding.sample.ts`, an invented couple with full length
copy, and puts a preview ribbon across the top. The real data file is untouched,
and sample content never renders unless the flag is set.

`node scripts/make-preview.mjs` turns a running preview into a single self
contained HTML file at `preview/index.html`, which can be opened from disk or
shared as a link. The form in that snapshot is visual only.

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

## The guest photo drop

After the wedding, guests can send their own photographs and videos straight
into a folder in your Drive. They never sign in to anything.

How it works: the browser asks `/api/upload/session` for one resumable upload
session per file, the server mints that session with your Google credentials,
and then the phone sends the bytes **directly to Google**. Nothing large passes
through the site, which matters because a serverless request body is capped at a
few megabytes and a guest's video is not.

The section opens at midnight on the wedding date in `src/data/wedding.ts` and
closes thirty days later. Both the page and the API check the clock, so it
cannot be reopened from a guest's phone.

### One-time setup

1. In the Google Cloud console, create a project and an OAuth client of type
   **Web application**. Add `http://localhost:5411/callback` as an authorised
   redirect URI.
2. On the OAuth consent screen, add the scope
   `https://www.googleapis.com/auth/drive.file` and **publish the app**. It is a
   non sensitive scope, so no Google review is needed. Leaving the app in
   testing mode makes the refresh token expire after seven days, which would
   break the drop mid wedding.
3. Run the helper, sign in as yourselves, and paste the four values it prints
   into `.env.local` and into the Vercel project settings:

```
node scripts/google-drive-setup.mjs --client-id XXX --client-secret YYY
```

It creates the Drive folder for you and prints its id.

4. Set `NEXT_PUBLIC_SITE_ORIGIN` to the deployed URL. Google will only return an
   upload session the browser may use if the origin matches.

Until those are set the section shows an honest message rather than a form that
silently fails. Limits are 30 files per batch and 500MB per file, both in
`src/lib/photoDrop.ts`.

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
