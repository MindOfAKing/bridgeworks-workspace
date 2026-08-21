# Adapters

An adapter is a read or write bridge to something outside the GTM architecture.
No business truth lives here. If deleting an adapter would lose a fact about a
prospect, it is not an adapter.

## Present

| Adapter | Direction | What it does |
|---|---|---|
| `acquisition_engine.py` | read | Turns a client-acquisition-engine research record into a slice input. Blocks and returns a classification call rather than guessing a gap category. |
| `engine_snapshot.py` | read | Builds the daily snapshot the objective selector consumes. Emits null, never zero, for anything it could not read. |
| `classifications/` | data | One file per prospect recording the gap-category classification and the quoted rationale behind it. |

## Free and public tools

Firecrawl, SerpAPI, the public web, browser research, Google Search and Places, ODS
local search and future free APIs are **tool adapters**. They are not capabilities
and they are not sources of truth.

The distinction that matters:

- A **capability** is registered in `skill-governance/capability-registry.yaml`, has
  a role permitted to call it, and produces a judgment.
- A **tool adapter** fetches bytes. It has no opinion.

Three rules follow.

**Register on demonstrated need, not on availability.** A tool adapter gets wired in
when a role or capability has a use for it that is written down. `geo-audit` needed
public web fetching on 2026-08-11, so it used it. Nothing needed SerpAPI, so nothing
was configured.

**Low historical usage is not a reason to remove an integration.** `TOMBA_API_KEY`,
`HUNTER_API_KEY` and `APIFY_API_KEY` exist in `Projects/.env` and are barely used.
That is evidence about the workflows built so far, not about the tools. Removing
them costs a re-setup later and saves nothing now. Leave them. The open loop about
picking one of Hunter, Tomba and Apollo is a spend decision, and it is Emmanuel's.

**An unverified key is not a working integration.** `ROUTING.md` marks Tomba and
Hunter as set but unverified, and n8n as having no server. A capability call must
not assume any of them works. `capability_call_request` records the runtime the
routing policy assigns; it does not assert that runtime is currently reachable.

## Wanted

| Adapter | Direction | Why |
|---|---|---|
| Gmail evidence | read | `outreach_engine.py` already does this inside the engine. It belongs here. |
| HubSpot | read | Duplicate checks before enrichment. Writes stay blocked until the connector is reauthorized. |
| Review packet | write | So an internal-GTM packet lands in the existing approval surface instead of creating a second one. |
| ODS or Qwen | read | The routing policy sends `simple_stage_classification` to `ods_qwen`. ODS was not verified running on 2026-08-11, so Claude did that classification and the substitution is recorded in the classification file. |
