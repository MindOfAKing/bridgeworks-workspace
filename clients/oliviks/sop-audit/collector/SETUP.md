# Collector: deployed and verified

Set up 2026-08-11. Nothing outstanding. This file is the record, not a to-do list.

## What is live

| Piece | Where |
|---|---|
| Forms | <https://oliviks-ops-review.vercel.app> (Vercel project `oliviks-ops-review`) |
| Owners' audit | <https://oliviks-ops-review.vercel.app/audit> |
| Staff form | <https://oliviks-ops-review.vercel.app/team> |
| Collector script | Apps Script project `16LhMjq_OkYyuxS9USOA7dT-k0WeP6OAUpgtn3L7lkp5m1ZmxAAi9et60` |
| Endpoint | `https://script.google.com/macros/s/AKfycbxrTPTpwgDtHKys64UjQFyf_vuJhIsMJMLFzgla1XTDggnFfKY1VVNJ-MU1ArKTH2oD/exec` |
| Responses | [Oliviks SOP audit responses](https://docs.google.com/spreadsheets/d/1qQI3lp9TL4t6ykUoALdKOkVIvSCxD--QVvVQtWWdNss/edit), tabs `Owners` and `Staff` |

Deployment: Version 3, web app, execute as `emmanuelehigbai@gmail.com`, access `Anyone`.
"Anyone" exposes the script URL only. The spreadsheet stays private. All the script can
do is append a row.

The spreadsheet is created and owned by the script itself, and its id is stored in script
properties under `SHEET_ID`. An earlier hand-made sheet
(`10Tbn--gIb11Sg-Z5vQl-XWmX2gRJZ241bpn_2VFIcBk`, "Untitled spreadsheet") could not be
opened by the script and is now orphaned. Safe to delete.

## Verified 2026-08-11

- `GET /exec` returns `{"ok":true,...}` with the sheet name and URL.
- Owners submission from the live origin landed in `Owners`, stamped `2026-08-11 19:43`.
- Staff submission landed in `Staff`, stamped `2026-08-11`, **date only, no time**.
- Both tabs got a formatted header row on first write.
- `/`, `/audit` and `/team` all return 200, with `X-Robots-Tag: noindex, nofollow`.

## Test rows to clear before sending

Three test rows are in the sheet. Delete them before the real thing starts:

- `Owners` row 2, name "TEST SUBMISSION, ignore".
- `Staff` rows 2 and 3. The second one carries "LIVE ORIGIN TEST, delete this row" in the
  final free-text answer. Neither is labelled in an obvious column, so clear both.

## Rules this setup depends on

- **Never share the responses spreadsheet with anyone at Oliviks.** The staff form tells
  people only BridgeWorks can open it. That promise is why the answers will be honest.
- The `Staff` tab stores a date, not a time. A timestamp plus a shift rota identifies a
  person. Do not add a time column later.
- Report staff findings to the owners as themes across everyone, never as individual
  responses, and never quote a line only one person could have written.

## If the endpoint ever changes

Editing `Code.gs` alone does nothing to the live URL. Apps Script serves the version that
was published, so you must run **Deploy > New deployment** again and paste the new `/exec`
URL into `SUBMIT_URL` at the top of `site/audit.html` and `site/team.html`, then redeploy
the site with `vercel deploy --prod` from `sop-audit/site`.

If `SUBMIT_URL` is ever blanked, the Send button says sending is not switched on and the
forms fall back to Download, Copy and Print. They stay usable, collection just goes manual.
