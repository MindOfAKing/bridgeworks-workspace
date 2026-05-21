# BridgeWorks API-backed prospecting

This folder wires BridgeWorks prospecting into the API keys already available in the local env files.

The engine reads keys from:

- `bridgeworks-workspace/.env`
- `bridgeworks-agency/.env.local`

It does not print secrets.

## Current API roles

- `GOOGLE_PLACES_API_KEY`: preferred key for prospect discovery through Google Places.
- `GOOGLE_API_KEY`: fallback key for Google Places if a dedicated Places key is not present.
- `FIRECRAWL_API_KEY`: prospect website extraction for conversion/GEO signals.
- `HUNTER_API_KEY`: email enrichment after a company is qualified.
- `TOMBA_API_KEY` + `TOMBA_SECRET_KEY`: fallback email enrichment.
- `APIFY_API_KEY`: reserved for bulk runs when we move beyond small daily batches.
- `SERPAPI_API_KEY`: optional future key for SERP/GEO checks.
- `APOLLO_API_KEY`: optional future key for decision-maker enrichment.

## Run

```powershell
python scripts\prospecting\daily_prospecting_engine.py --limit 10 --per-query 3
```

Dry run:

```powershell
python scripts\prospecting\daily_prospecting_engine.py --dry-run --limit 5
```

Outputs:

- Adds qualified prospects to `pipeline/prospecting/prospect-tracker.csv`.
- Adds A-priority research/draft items to `pipeline/prospecting/daily-outreach-queue.csv`.
- Saves a non-secret run summary in `pipeline/prospecting/runs/`.

## Google Places setup

The current local `GOOGLE_API_KEY` is present, but Google is returning access denied for Places. Use a dedicated Places key to avoid breaking other Google/Gemini usage.

In Google Cloud:

1. Open the project that owns your billing.
2. Enable **Places API (New)**.
3. Create or edit an API key.
4. Allow the key to use **Places API (New)**.
5. Add it locally as:

```text
GOOGLE_PLACES_API_KEY=...
```

The daily prospecting engine will automatically prefer `GOOGLE_PLACES_API_KEY` over the generic `GOOGLE_API_KEY`.
