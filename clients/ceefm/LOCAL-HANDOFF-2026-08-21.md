# CEEFM local handoff — 2026-08-21

Written by a Cowork session that could not reach `C:/Users/User/ceefm-astro`. Everything below is for a local Claude Code session running in that folder.

**Engagement status: closed since 2026-06-19.** This is unpaid ad-hoc support, follow-on to `WEBSITE-UPDATE-2026-08-11.md`. Not a reactivation. Do not schedule delivery, content, or reporting off this file.

---

## Get this to your machine

```
cd C:/Users/User/Projects/bridgeworks-workspace
git fetch origin claude/ceefm-google-tag-update-kv5kyl
git checkout claude/ceefm-google-tag-update-kv5kyl
git pull
```

Three files matter:

- `clients/ceefm/CONVERSION-ACTION-MISMATCH-2026-08-21.md` — full diagnosis and the patch spec
- `clients/ceefm/scripts/verify-dist.py` — pre-upload build check
- this file

---

## Kickoff prompt

Open Claude Code in `C:/Users/User/ceefm-astro` and paste:

> This repo deploys to Hostinger by FTPS: `python deploy-ftp.py` from this folder, with `CEEFM_FTP_PASS` set. GitHub is a backup remote only, never a deploy source.
>
> Two jobs, in this order.
>
> **1. Push the backlog.** `MindOfAKing/ceefm-astro` on GitHub is at `8356255` (2026-05-19). Five local commits from 2026-08-11 were never pushed: `ca44ded`, `f5e7a37`, `eba63b2`, `35da0ae`, `9a9bc35`. They are the only source copy of the Google Ads tag, the Consent Mode v2 fix, the bilingual privacy policy, the Web3Forms success-parsing fix, and the deploy script. Verify they are intact, then push to `main`. This gates nothing else, it is backup hygiene.
>
> **2. Read `deploy-ftp.py` and tell me three things** before anything is uploaded:
> - Does it upload `dist/`, or a stale `ceefm-deploy/` folder? (`.gitignore` still lists the latter from the old zip workflow.)
> - Does it send dotfiles? `.htaccess` carries HSTS and CSP, `.well-known/security.txt` is also a dotted path. Many FTP scripts skip hidden files by default.
> - Is it a mirror or additive? Additive means removed files stay live forever.
>
> Do not apply the conversion patch yet. It is gated on a Google Ads answer that has not come back. Details in `bridgeworks-workspace/clients/ceefm/CONVERSION-ACTION-MISMATCH-2026-08-21.md`.

---

## The gate

Victor ran the Ads troubleshooter and got "conversion action wasn't detected" for **Contact (Form submission www.ceefm.eu/)**, ID `18378779634`, label `8ze4CP2Tyt4cEPLX17tE`.

That banner is **not** proof of breakage. The troubleshooter loads the page and watches. It cannot submit a form, so a submit-only conversion can never be detected by it.

The real question, unanswered: **is any conversion action in the account bound to the event name `ads_conversion_Contact_Us_2`?**

- **Yes** → the deployed code is already correct. Change nothing. The banner is the false alarm above.
- **No** → apply Option A below.

Verified from the live bundle on 2026-08-21: the site fires that event name only. The label `8ze4CP2Tyt4cEPLX17tE` and `send_to` appear nowhere on the site. The 2026-08-11 wire test's 200 proves the hit was **accepted**, not **attributed**.

Do not apply the patch before this is answered. Applying it when the event-name binding is correct would break a working conversion.

---

## Option A patch, only once the gate clears

One change in `src/components/ContactForm.tsx`:

```tsx
// from:
const ADS_CONVERSION_EVENT = 'ads_conversion_Contact_Us_2';
if (typeof g === 'function') g('event', ADS_CONVERSION_EVENT);

// to:
const ADS_CONVERSION_SEND_TO = 'AW-18378779634/8ze4CP2Tyt4cEPLX17tE';
if (typeof g === 'function') {
  g('event', 'conversion', { send_to: ADS_CONVERSION_SEND_TO });
}
```

Keep the `useRef` guard, the `try`/`catch`, and firing only on genuine submit success after the response body is parsed.

Caution: if that action was auto-created by Google's form detection, Google may fire it independently and double count. Confirm its origin first.

**Option B, no deploy at all:** edit the action in Ads so its event name is `ads_conversion_Contact_Us_2`.

---

## Release sequence

```
cd C:/Users/User/ceefm-astro
git status                 # commit first, this is the only rollback path
npm ci
npm run build
python C:/Users/User/Projects/bridgeworks-workspace/clients/ceefm/scripts/verify-dist.py dist
# only if it exits 0:
set CEEFM_FTP_PASS=...
python deploy-ftp.py
```

`verify-dist.py` checks the build output: all 10 pages present and carrying both tags, consent defaults denying before `gtag.js` loads with a grant path present, which conversion binding the bundle actually uses, that the Web3Forms `response.ok` bug has not regressed, `.htaccess` present with HSTS and CSP, robots/llms/security.txt present, and 10 sitemap URLs. Exit 0 means the build is sound. It says nothing about the Ads account.

`public/.htaccess` is in the repo, so Astro copies it into `dist/` on every build. It is rebuilt and re-uploaded each release, not preserved on the server.

## Rollback

```
git log --oneline -5
git checkout <previous-commit>
npm run build
python deploy-ftp.py
git checkout main
```

About two minutes, and it is the whole safety net. Which is why you commit before building.

## Post-deploy verification

All 10 pages 200 with the AW tag, consent default denied, grant path present, policy links locale-correct, HSTS and CSP intact. Then **Tag Assistant with a real form submit**, or the stubbed POST used on 2026-08-11. The troubleshooter will never confirm a submit conversion.

---

## Still open, all Victor-side

No reply from him since the Hostinger collaborator invite on 2026-08-11 (Gmail checked through 2026-08-21).

1. `ads_conversion_Contact_Us_1` fires on **page load** of `/contact/`. Not ours. If primary, Smart Bidding optimises toward page views. Demote or remove.
2. Confirm the action's type is Website, not a GA4 import, Count = "One".
3. The privacy policy is unreviewed by him. It is legal text published under CEEFM Kft's name.
4. Remarketing is not disclosed either way in the policy.
5. Hostinger collaborator access covering domain, hosting and email appears never revoked.

## Side finding

`www.ceefm.eu` returns 200 directly rather than redirecting to apex. Both hosts serve the full site with the tag, and every canonical points to `https://ceefm.eu/`, so search is unaffected. Worth a 301 www to apex eventually. It explains why the Ads action was registered against the www URL while `astro.config.mjs` sets `site: 'https://ceefm.eu'`.
