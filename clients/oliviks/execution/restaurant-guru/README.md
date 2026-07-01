# Restaurant Guru 2026 award assets

HOW TO USE:
- `badge-1.png` is the chosen design (gold laurel). Its live embed is already on the
  website footer. The other badge PNGs are the alternative designs for reference.
- `certificate-2026-preview.png` is the printable certificate for the shop wall.
- `badges.json` holds the raw embed HTML for all six designs (from the award page).

Source: Restaurant Guru email 2026-06-30 to olivikskitchen@gmail.com, captured with
Playwright from https://restaurantguru.com/widget-awards (Oliviks award page).

Award: Certificate of Excellence 2026, "top 100 restaurants with banquet room in
Budapest". Public profile: https://restaurantguru.com/Oliviks-Kitchen-Budapest

## Promo activation (do AFTER the domain flip)
The award page has a form: enter the URL of the page carrying the badge plus
olivikskitchen@gmail.com, click "Activate promo". Their crawler verifies the badge
and activates promotional placement on their Budapest list. Submit oliviks.com
(footer badge is site-wide) once the domain points at Vercel, so the promo is tied
to the final domain, not the temporary vercel.app URL.
