# CEEFM conversion action mismatch — 2026-08-21

**Engagement status: still closed.** This is diagnosis only, follow-on to the unpaid ad-hoc support recorded in `WEBSITE-UPDATE-2026-08-11.md`. Not a reactivation. Do not schedule delivery off this file.

**Prompted by:** Victor ran Google Ads "Troubleshoot conversion action" and got "This conversion action wasn't detected" for **Contact (Form submission www.ceefm.eu/)**, conversion ID `18378779634`, label `8ze4CP2Tyt4cEPLX17tE`.

---

## Blocker found first: GitHub is behind production

`MindOfAKing/ceefm-astro` has one branch, `main`, at `8356255` (2026-05-19). **None of the 2026-08-11 work is pushed.** Verified missing from the repo: the `AW-18378779634` config, the Consent Mode grant fix, the conversion event and its ref guard, the Web3Forms success-parsing fix, `/privacy`, `/hu/adatvedelem`, the `Nav.astro` `altEn`/`altHu` props, the BridgeWorks footer credit, and `deploy-ftp.py`. `ContactForm.tsx` line 30 in the repo is still the buggy `setFormStatus(response.ok ? 'success' : 'error')`.

Commits `ca44ded`, `f5e7a37`, `eba63b2`, `35da0ae`, `9a9bc35` exist only at `C:/Users/User/ceefm-astro` and as built output on Hostinger.

**Consequence:** any patch applied to GitHub main and deployed would revert the entire August release, including legal text published under CEEFM Kft's name. Push the local commits before touching anything.

---

## The banner is not sufficient evidence of breakage

Google's troubleshooter loads the URL and watches for the tag. It cannot fill in and submit the contact form. A conversion that fires only on genuine submit success can never be detected this way. `ads_conversion_Contact_Us_1`, which fires on page load, *would* show as detected. Detection in this tool is not a quality signal.

## But there is a real mismatch

Deminified from the live bundle `/_astro/ContactForm.Bu9U6aps.js` on 2026-08-21:

```js
const k = "ads_conversion_Contact_Us_2";
const fired = useRef(false);
const fireConversion = () => {
  if (!fired.current) {
    fired.current = true;
    try {
      const g = window.gtag;
      if (typeof g === "function") g("event", k);   // no params, no send_to
    } catch {}
  }
};
```

Verified across `/contact/`, the www copy, and the bundle:

| Check | Result |
|---|---|
| Label `8ze4CP2Tyt4cEPLX17tE` anywhere on site | Zero occurrences |
| `send_to` anywhere on site | Zero occurrences |
| Ads events fired | Exactly one, by event name only |
| Ref guard against double-count | Present and correct |

The action in the screenshot is named "Contact (Form submission www.ceefm.eu/)", Google's naming for the form-submission / URL goal flow rather than the Google-tag flow that generates `ads_conversion_*` event names. If that is what it is, nothing on the site will ever fire it.

## What the 2026-08-11 wire test actually proved

The 200 from `googleads.g.doubleclick.net/pagead/viewthroughconversion/18378779634/?en=ads_conversion_Contact_Us_2` means Google **accepted** the hit against conversion ID 18378779634. It does not mean the hit was **attributed** to a conversion action. If no action is bound to that event name, the hit lands and counts toward nothing. The tag works. The binding is the open question.

---

## Decision gate for Victor (Ads → Goals → Conversions → Summary)

1. Is there an action whose **event name** is `ads_conversion_Contact_Us_2`? If yes, the code is correct and the banner is the false alarm described above. Stop here.
2. What is the screenshot's "Contact" action bound to: an event name, the label, or Google's automatic form detection?
3. Is `ads_conversion_Contact_Us_1` a primary conversion? It fires on page load of `/contact/` and will skew Smart Bidding toward page views. Demote or remove.
4. Are these type Website rather than GA4 imports, with Count set to "One"?

Do not apply the patch below until 1 and 2 are answered.

---

## Option A patch, if Victor keeps the screenshot's action

One change in `C:/Users/User/ceefm-astro/src/components/ContactForm.tsx`. Bind by label instead of event name.

Replace the event-name constant and call:

```tsx
// was:
const ADS_CONVERSION_EVENT = 'ads_conversion_Contact_Us_2';
// ...
if (typeof g === 'function') g('event', ADS_CONVERSION_EVENT);
```

with:

```tsx
const ADS_CONVERSION_SEND_TO = 'AW-18378779634/8ze4CP2Tyt4cEPLX17tE';
// ...
if (typeof g === 'function') {
  g('event', 'conversion', { send_to: ADS_CONVERSION_SEND_TO });
}
```

Keep unchanged: the `useRef` guard, the `try`/`catch`, and firing only on genuine submit success after the response body is parsed.

**Caution.** If that action was auto-created by Google's automatic form detection, Google may also fire it independently and double count. Confirm its origin before choosing this. Count = "One" mitigates but does not remove the problem.

**Option B, no deploy:** edit the action in Ads so its event name is `ads_conversion_Contact_Us_2`. Cheaper if the action is editable.

This patch is a specification, not a compiled and tested change, because the tree it applies to is not on GitHub. It must be built and verified locally before deploy via `python deploy-ftp.py`.

## How to actually verify a submit conversion

Tag Assistant connected to the site, then submit the form for real or reuse the stubbed POST from 2026-08-11. The troubleshooter will never confirm it.

---

## Side finding

`www.ceefm.eu` returns 200 directly instead of redirecting to the apex. Both hosts serve the full site with the tag, and every canonical points to `https://ceefm.eu/`, so search is unaffected. Worth a 301 www to apex eventually. Not the cause here, but it explains why the conversion action was registered against the www URL while the canonical site is apex.

## Still open from 2026-08-11

No reply from Victor since the Hostinger collaborator invite on 2026-08-11 (checked Gmail through 2026-08-21). Policy still unreviewed by him, remarketing still undisclosed either way, and the Hostinger collaborator access covering domain, hosting and email appears never revoked.
