# YouTube Extraction: n8n Prospect Research Intake Guardrail

Source: Tito Space, `How To Build an AI Lead Generator with n8n Step by Step`  
URL: https://www.youtube.com/watch?v=ZX3A9QubE2M  
Date extracted: 2026-07-15  
BridgeWorks pillar: Outreach Infrastructure, Competitive Intelligence, AI Growth Systems

## Useful Ideas

- A prospect research workflow can start from a simple form: business type, city, and state.
- The workflow pulls Google business data, loops through each business, formats fields, waits between requests, and writes results to a sheet.
- The useful BridgeWorks pattern is research intake and structured enrichment, not automated outreach.
- Scheduled runs are possible, but they must remain local or approval-gated until the data, source quality, and contact policy are verified.

## Evidence

- 00:01 to 00:27: workflow trigger is a form, then Python scripts split businesses and loop through results.
- 03:06 to 04:00: form captures business type, city, and state, then a Python script scrapes Google API data.
- 05:27 to 06:18: fields include location, phone number, name, rating, Google Maps URL, user rating total, website, address, latitude, and longitude.
- 06:53 to 07:04: columns can be mapped automatically into the sheet.
- 08:34 to 09:03: a scheduler can run the process at a set time, but it is described as process automation rather than a true AI agent.
- 10:04 to 10:18: the result is around 20 businesses pulled from Google into the lead sheet.
- 10:57 to 11:55: workflow flow is form, script, split businesses, loop each business, format, wait, and save to sheet.

## What This Changes For BridgeWorks

BridgeWorks already has a 45-row prospect queue from the current acquisition workstream. This source supports a cleaner intake pattern for future batches, but the active manual evidence checks remain safer than blind automation.

## Action To Take

Create a `Prospect Research Intake Guardrail` before any automated list-building:

1. Approved niche.
2. Approved city.
3. Source used.
4. Fields allowed.
5. Manual verification required.
6. Duplicate check.
7. No outreach flag.
8. No CRM or Google Sheet write without approval.

## SOP / Template Update

Any n8n prospect automation must be read-only or local-file-only until Emmanuel approves the exact workflow by name.

## Content Or Proof Angle

Internal only for now. This is an infrastructure pattern, not public content.

## Decision

Adapt later. Do not activate or import a workflow from this run.
