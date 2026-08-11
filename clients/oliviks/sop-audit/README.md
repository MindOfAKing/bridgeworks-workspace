# Oliviks SOP audit, August 2026

Discovery instruments for the SOP engagement, which is separate from the Foundation.
Two audiences: the owners, and the people on shift. Built to find out which parts of the
operation need standardising first, before any SOP writing starts.

```
sop-audit/
  diagnostic/           what happens when responses land
    README.md           internal method, scoring model, sizing
    OLIVIKS-OPS-DIAGNOSTIC-TEMPLATE.md   the client deliverable
    FOLLOW-UP-GUIDE.md  interview and observation guide
  site/                 the deployable forms
    index.html          landing page with both links
    audit.html          owners, about 20 minutes, scores itself
    team.html           staff, about 10 minutes, anonymous
    vercel.json         clean URLs, noindex
  collector/
    Code.gs             Apps Script that appends submissions to the sheet
    SETUP.md            the four manual steps, about two minutes
  OLIVIKS-SOP-AUDIT-2026-08-11.md   paper version of the owners' questions
  README.md
```

## Status

Live and verified end to end, 2026-08-11.

| | |
|---|---|
| Owners' audit | <https://oliviks-ops-review.vercel.app/audit> |
| Staff form | <https://oliviks-ops-review.vercel.app/team> |
| Both, with descriptions | <https://oliviks-ops-review.vercel.app> |
| Responses | [Oliviks SOP audit responses](https://docs.google.com/spreadsheets/d/1qQI3lp9TL4t6ykUoALdKOkVIvSCxD--QVvVQtWWdNss/edit) |

Submissions from the live site land in the sheet within a second. Details, deployment ids
and the operating rules are in `collector/SETUP.md`.

**Before sending anything to the client:** delete the three test rows listed in
`collector/SETUP.md`, and delete the orphaned "Untitled spreadsheet"
(`10Tbn--gIb11Sg-Z5vQl-XWmX2gRJZ241bpn_2VFIcBk`).

## The surveys are not the deliverable

They are evidence collection. The first deliverable is the diagnostic in `diagnostic/`:
process inventory, gap map, scored priority register. It ends at a review with Aese and
Cynthia, before any SOP gets written, because that review is where they see why a document
is needed and where you learn how many you are actually writing.

Survey, then gap analysis, then targeted follow-up, then drafting. Going straight from
survey to manual produces confident documents full of assumptions.

## Send both at the same time

The two instruments are worth more together than in sequence. The owners describe the
system they believe exists. Staff describe the system they actually experience. The gap
between the two is the finding, and it only stays clean if both sides answer without
having seen the other set.

Sequencing them loses that. By the time staff answer, the questions have been discussed,
and people answer with what they think the owner wants to hear.

**Aese distributes the staff link. BridgeWorks never approaches staff directly.** That
keeps consent with the owner and independence in the answers. Ask her not to talk the team
through the questions first, and say why.

## Privacy rules the staff form depends on

The staff form makes three promises. All three are now load-bearing:

1. **No name is collected.** Verified: zero text inputs in the file.
2. **Only BridgeWorks can open the responses.** Never share the spreadsheet with anyone
   at Oliviks.
3. **Date only, never a time.** A timestamp plus a shift rota identifies a person. The
   Apps Script writes a date for staff submissions and a full stamp for owner ones. Do not
   add a time column later.

Report staff findings to the owners as themes across everyone. Never as individual
responses, and never quote a line only one person could have written.

## What the owners' audit covers

Part 0 sets the shape of the business, then thirteen areas:

1. Opening and closing the kitchen
2. Buying and stock
3. Cooking and portion consistency
4. Food safety and hygiene
5. Taking orders
6. Packing and handing over
7. Menu and prices across channels
8. Money and admin
9. Catering and events
10. Customers, complaints and reviews
11. Marketing routines
12. People and training
13. Accounts, access and keys

Each area asks four to six statements on a four-point scale (written and followed, written
and ignored, in our heads, not happening), plus who owns it, what goes wrong, and how much
it hurts right now. 68 columns land in the sheet, including a full text transcript.

## What the staff version covers

No name field, no score, deliberately. A score would read as marking them.

1. When you started here (were you shown, told once, or left to work it out)
2. A normal shift (do you know what to do without asking)
3. When something goes wrong
4. Where the time goes
5. Teaching somebody else
6. Anything else

The three questions that usually produce the most usable material are at the end: what you
would tell a new person in their first hour, what nobody writes down but everybody has to
know, and what mistake every new person makes. Those answers are close to being SOP drafts
already. 36 columns land in the sheet.

## How to read the results

The score is not the point. The prioritisation is.

An area scoring 20% that Aese marked "fine, leave it alone" is not urgent. An area scoring
40% that she marked "this costs us money" is where the first SOP goes. The results screen
ranks the three areas with the worst combination of the two, and the audit separately asks
her to pick her own top three. Where those two lists disagree is the most useful
conversation on the follow-up call.

## Why these areas

Drawn from the Foundation engagement, April to August 2026:

- Menu and prices across channels is already a known problem. The same dish carries three
  prices across in store, shop.oliviks.com and Wolt, Wolt has carried a wrong address, and
  dish names and spellings differ between the website and Wolt. Documented in
  `../reports/WOLT-VS-WEBSITE-COMPARISON-2026-07-15.md`.
- Order intake is spread across walk in, phone, WhatsApp, the shop, Wolt and Foodora.
- Marketing routines exist as systems now (MailerLite weekly specials, WhatsApp broadcast,
  Google Business Profile) but were handed over with no owner and no schedule. See
  `../OLIVIKS-HANDOVER-2026-07-14.md`.
- Accounts and access matters because every account is in the owners' names and several
  sit on one phone.
- The 4.8 rating from 160+ reviews is the business's biggest asset and has no written rules
  protecting it.

## Language

The staff form is in English and tells people to answer in Hungarian if that is easier, but
the questions themselves are not translated. If any of the team read Hungarian more
comfortably, translate before distribution rather than after.

## Not covered on purpose

Legal and employment compliance beyond a plain question about written agreements, kitchen
equipment maintenance, and anything requiring an on-site visit. Those come after the audit
identifies whether they matter.
