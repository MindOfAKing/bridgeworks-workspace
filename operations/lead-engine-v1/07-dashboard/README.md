# BridgeWorks Lead Engine Cockpit

Private local dashboard for the Lead Engine v1 acquisition workflow.

## Refresh

```bash
python refresh.py
```

## View locally

```bash
python -m http.server 8766
```

Open:

```text
http://localhost:8766/
```

## Sources

- `../01-prospects/prospect-tracker.csv`
- `../03-outreach-drafts/outreach-send-log-2026-06-23.json`
- `../02-lead-leak-reviews/batch-2/batch-2-summary.md`
- `../05-os-build-next/bridgeworks-os-next-steps-2026-06-23.md`

## Guardrail

Local/private only. Do not deploy publicly without removing sensitive prospect, email, and operational data.
