# CEEFM Missing Fields Workflow

Built: 2026-05-15

## Goal

Turn the `Missing Fields` tab into sendable rows without wasting enrichment credits.

## What Counts As Filled

A row is complete enough for written outreach when it has:

- A verified decision maker or credible named operator
- A LinkedIn URL for that person or a verified direct email
- Bilingual copy reviewed
- No `Research before outreach` flag
- No phone-only dependency

## Enrichment Priority

### Priority 1: Named DM missing

Work these first. Do not spend Hunter, Tomba, or Apollo credits before finding a name.

Search patterns:

- `site:linkedin.com/in "[Company]" Budapest operations`
- `site:linkedin.com/in "[Company]" general manager`
- `site:linkedin.com/in "[Company]" property manager`
- `"[Company]" "General Manager" Budapest`
- `"[Company]" "Operations Director"`
- `"[Company]" "Managing Director"`

Acceptable roles:

- Owner
- Managing Director
- General Manager
- Operations Director
- Property Management Director
- Head of Operations
- Country Director

Reject:

- Reception
- Front desk
- Reservation desk
- Marketing intern
- Generic company page only

### Priority 2: LinkedIn missing

Once a name exists, find the personal LinkedIn URL.

Search patterns:

- `site:linkedin.com/in "[Full Name]" "[Company]"`
- `site:linkedin.com/in "[Full Name]" Budapest hospitality`
- `site:linkedin.com/in "[Full Name]" property management Budapest`

If only a company LinkedIn page is found, mark:

- `DM Verification`: Role only / unverified
- `Automation Stage`: Enrichment needed

### Priority 3: Direct email missing

Only after the name and role are credible:

1. Check company website contact/team pages.
2. Check press releases and PDFs.
3. Try Hunter/Tomba/Apollo.
4. If only a pattern is guessed, mark it unverified.

Accepted email verification statuses:

- `Direct - confirmed`
- `Direct - website confirmed`
- `Generic - confirmed`
- `Generic only`
- `Unverified direct-looking`
- `Missing`

Only the first two are auto-email eligible.

## Credit Use Rule

Use enrichment credits in this order:

1. Tier 1 aparthotel / hospitality operators with 20+ units or multi-property scale
2. Tier 2 property managers with 100+ units or clear investor portfolio
3. Referral partners with High referral potential
4. Everything else

Do not spend credits on:

- Cold / Q4
- Research first
- Parked rows
- Company pages with no named person

## Phone Rule

Phone is not a first-touch channel for Emmanuel unless:

- English speaker is verified, or
- Hungarian-speaking helper is available, or
- The call is only to ask for an email/name and has a short script.

Phone rows stay out of automation.

## Daily Workflow

1. Open `Missing Fields`.
2. Filter `Automation Blocker` contains `missing verified decision maker`.
3. Fill 5 names and LinkedIn URLs.
4. Move to email verification only after names are found.
5. Regenerate the packet.
6. Work from `Text Ready Queue` or `Send Control`.

## Regenerate Command

From the workspace root:

```powershell
& 'C:\Users\ELITEX21012G2\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\ceefm\build_outreach_packet.py
```
