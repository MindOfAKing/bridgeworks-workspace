# GEO specialist hand-back contract

The aggregate input must contain `run_id`, `completed_at`, and a `specialists`
object with exactly five keys:

- `agent-geo-ai-visibility`: scores `ai_citability`, `brand_authority`
- `agent-geo-content`: score `content_eeat`
- `agent-geo-technical`: score `technical_geo`
- `agent-geo-schema`: score `schema_structured_data`
- `agent-geo-platform-analysis`: score `platform_optimization`

Each specialist record contains:

- `scores`: integer category scores from 0 to 100
- `findings`: structured evidence findings compatible with
  `operations/internal-gtm/schemas/geo-diagnostic.schema.json`
- `confidence`: `low`, `medium`, or `high`
- `sources_checked`: public URLs or immutable local evidence paths
- `blocked_checks`: checks that could not be performed

No specialist chooses a service route, qualification tier, or offer. The
orchestrator preserves all findings and computes only the established weighted
GEO score.
