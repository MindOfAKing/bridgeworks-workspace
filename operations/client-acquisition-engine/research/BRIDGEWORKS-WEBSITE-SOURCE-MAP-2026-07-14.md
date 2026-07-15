# BridgeWorks Production Website Source Map

Date: 2026-07-14
Run type: Read-only source and deployment audit
Status: Source identified. No website source, GitHub repository, Vercel project, or live page was changed.

## Production Identity

| Item | Verified value | Evidence |
|---|---|---|
| GitHub repository | `MindOfAKing/bridgeworks-agency` | Canonical `bridgeworks-dev` GitHub account, private repository metadata. |
| Remote URL | `https://github.com/MindOfAKing/bridgeworks-agency` | GitHub repository record. |
| Local clone | `C:\Users\User\Projects\bridgeworks-agency` | Local git remote points to the same repository. |
| Default branch | `main` | GitHub repository metadata and local branch. |
| Audited HEAD | `f3e40e98480415b562c61a4eeb21ee9a1955b34e` | GitHub tree, local HEAD, and latest production deployment record agree. |
| Hosting project | `bridgeworks-agency` | Local `.vercel/project.json`. |
| Vercel project ID | `prj_j1wwuoJ0GA18r9OsgZ4T3zKqXAFx` | Local `.vercel/project.json`. |
| Latest GitHub production deployment in the audit | 2026-06-23 18:22 UTC at audited HEAD | Vercel bot GitHub deployment record. |

The Composio Vercel toolkit has no active connection. This did not prevent source identification because GitHub deployment records and the local Vercel project link agree. It does prevent a direct Vercel account audit until the existing connection is deliberately restored.

## User Work Preservation

The local clone already contains uncommitted user changes in:

- `src/app/api/contact/route.ts`
- `src/messages/en.json`
- `src/messages/de.json`
- `src/messages/hu.json`
- `src/messages/ro.json`

The message-file edits update privacy wording from Web3Forms to the private Google Sheet intake path. They do not alter the reviewed claim strings. Any approved claim correction must preserve these changes. No source file was edited during this audit.

## Public And Source Findings

### English homepage

Direct current public evidence for `/en` shows:

- The homepage offer is the `48-Hour Lead Leak Review`.
- The testimonial says `Eight weeks later`.
- The proof row says `30+ Reviews delivered` and `4 platforms checked`.

The English source at the audited production commit matches those strings.

### Hungarian homepage

Direct current public evidence for `/hu` shows:

- The homepage still offers a free AI visibility scan.
- The testimonial still says sixteen weeks in Hungarian.
- The proof row still says 30-plus scans and four AI platforms.

### German and Romanian source

The deployed source for German and Romanian follows the same older offer and claim pattern as Hungarian:

- Free AI visibility scan on the homepage.
- Sixteen-week testimonial wording.
- 30-plus scans and four AI platforms.

This is source evidence tied to the production deployment commit. Direct live-page extraction for German and Romanian was not completed in this audit.

### About page

The English About page is publicly verified as claiming:

- Automated publishing across multiple LinkedIn channels.
- Real-time scoring and routing of every inbound enquiry.

Equivalent claims exist in all four locale files.

## Exact Source Locations

| Claim or offer | Translation path | Rendering source |
|---|---|---|
| CEEFM duration testimonial | `testimonials.items[0].quote` in all four `src/messages/*.json` files | `src/components/home/Testimonials.tsx:29` renders it inside quotation marks and a `blockquote`. |
| Homepage offer | `freeAudit.tag`, `headline`, `description`, and `cta` | `src/components/home/FreeAudit.tsx`. |
| Homepage 30-plus claim | `freeAudit.socialProof.auditsCount` and `auditsLabel` | `src/components/home/FreeAudit.tsx:44`. |
| Homepage four-platform claim | `freeAudit.socialProof.platformsCount` and `platformsLabel` | `src/components/home/FreeAudit.tsx:49`. |
| About automation claim | `about.part3.p2` | `src/app/[locale]/about/AboutClient.tsx:147`. |
| AI Visibility Scan 30-plus claim | `geoAudit.stats.auditsCount` and `auditsLabel` | `src/app/[locale]/ai-visibility-scan/GeoAuditClient.tsx:83`. |
| AI Visibility Scan four-platform claim | `geoAudit.stats.platformsCount` and `platformsLabel` | `src/app/[locale]/ai-visibility-scan/GeoAuditClient.tsx:90`. |

The relevant translation line anchors at the audited local HEAD are:

| Locale | Testimonial | Homepage stats | About claim | Scan stats |
|---|---:|---:|---:|---:|
| English | 74 | 125 and 127 | 330 | 981 and 983 |
| German | 74 | 121 and 123 | 375 | 1038 and 1040 |
| Hungarian | 74 | 121 and 123 | 375 | 1038 and 1040 |
| Romanian | 74 | 121 and 123 | 375 | 1038 and 1040 |

## Additional Locale Drift

The English `freeAudit` namespace has been repositioned to the Lead Leak Review. German, Hungarian, and Romanian still use the free AI Visibility Scan headline and CTA.

Those three non-English locale files also contain untranslated English copy in the `freeAudit.positioning` and `freeAudit.sprint` blocks. The paid sprint title and price exist alongside the older free-scan homepage copy, creating a mixed offer in one section.

## Minimum Controlled Patch

Implementation should remain one approval-gated multilingual patch:

1. Choose the single homepage offer for every locale: the Lead Leak Review or the defined-capacity Free AI Visibility Scan.
2. Replace the testimonial component with a factual CEEFM proof block, or obtain client-confirmed testimonial wording. Do not silently edit the quoted client statement.
3. Remove the 30-plus and four-platform counters unless matching evidence and platform scope are supplied.
4. Replace the About automation paragraph with the evidence-safe operating-system wording already proposed in the correction packet.
5. Translate the approved offer, proof, and About copy consistently into German, Hungarian, and Romanian.
6. Preserve the existing contact-route and privacy-copy worktree changes.
7. Validate all four JSON files, run lint and build, and visually check the homepage, About page, and AI Visibility Scan route in all four locales.
8. Deploy only after a separate production approval.

## Local Baseline Verification

- All four locale JSON files parsed successfully with PowerShell `ConvertFrom-Json`.
- `npm run build` passed against the existing local worktree and generated 74 static/dynamic routes across English, German, Hungarian, and Romanian.
- Type checking passed as part of the Next.js production build.
- `npm run lint` could not complete because `next lint` opened the first-time interactive ESLint configuration prompt. No lint configuration was generated or changed during the audit.
- The build left the same five source files modified as before the audit. No additional tracked source file entered the git diff.

## Approval Boundary

This source map authorizes nothing. No local source patch, GitHub write, commit, push, Vercel action, or live website change was performed.
