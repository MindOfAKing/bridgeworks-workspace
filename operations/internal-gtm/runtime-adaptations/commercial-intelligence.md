---
name: bridgeworks-commercial-intelligence
description: "Collect public evidence for the commercial_fit and execution_readiness qualification dimensions: company scale, budget-capacity proxies, growth state, probable value of the identified problem, procurement complexity and fit with BridgeWorks engagement size. Use when qualification-v1 reports commercial_fit as missing research. Never invents a contract value."
---

# Commercial Intelligence

A bounded research capability. It answers one question: is there plausibly enough
commercial substance here to justify further GTM effort.

It does not qualify. It does not route. It collects evidence and hands it to the
Evidence Auditor, which decides what is approved, and then to qualification-v1,
which scores.

## When it runs

`qualification-v1` reports `commercial_fit` with `research_status: required`, or
`execution_readiness` with `research_status: required`.

It does not run when either dimension already has fresh approved evidence. Check
`qualification_coverage.by_dimension` before starting. Re-researching a dimension
that is already `complete` is waste.

## Tool order, free first

1. Public web and browser research. The company's own site, About, Careers,
   Locations, Investors, press page.
2. Public registries. Companies House, cegjegyzek, CAC where applicable.
3. Free search. SerpApi and Firecrawl free tiers, Google, Bing.
4. Public directories with visible data. Crunchbase public pages, PitchBook public
   profiles, LinkedIn public company pages.
5. Paid enrichment only after Emmanuel approves the spend. Apollo credits are spend.

Record which tool produced each fact. A fact without a tool and a URL is not a fact.

## What to establish

| Question | Acceptable evidence |
|---|---|
| Plausible company scale | employee count on an owned page or registry filing, office count, named team size |
| Budget-capacity proxies | published pricing, published contract wins, funding announcement, registry turnover band, paid advertising presence |
| Locations, employees, customers | only where the company publishes them or a registry holds them |
| Growth or expansion state | dated hiring, a new location, a funding round, a product launch, an export-finance record |
| Probable value of the identified problem | the observed problem multiplied by a published volume, never by an assumed one |
| Procurement complexity | tender history, a published procurement policy, an enterprise security page, a named legal or compliance contact |
| Fit with BridgeWorks engagement size | compare the above against the engagement sizes BridgeWorks has actually delivered |

## Hard rule on value

**Never fabricate a contract value.** Not a range, not an estimate, not an
"order of magnitude". If the evidence supports a band, give the band and the
arithmetic. If it does not, say `commercial_value_band: null` and list what would
be needed to establish one.

A published price times a published volume is a supportable band. Anything times an
assumption is a fabrication with a number attached, which is worse than silence.

## Output

```json
{
  "capability": "bridgeworks-commercial-intelligence",
  "prospect_id": "<id>",
  "as_of": "<YYYY-MM-DD>",
  "findings": [
    {
      "id": "ci-<n>",
      "category": "commercial_fit | execution_readiness",
      "claim_key": "<exact proposition, e.g. employee_count>",
      "claim": "<one factual sentence>",
      "value": "<machine-readable value>",
      "severity": "none",
      "source": "<exact URL fetched>",
      "observed_at": "<YYYY-MM-DD>",
      "status": "verified | observed | inferred",
      "tool": "<public_web | registry | serpapi | firecrawl | directory>"
    }
  ],
  "commercial_value_band": {
    "low": null, "high": null, "currency": null,
    "basis": "<the exact arithmetic, or null>",
    "confidence": "high | medium | low | none"
  },
  "procurement_complexity": "low | medium | high | unknown",
  "engagement_size_fit": "below_floor | plausible | above_ceiling | unknown",
  "unresolved_questions": ["<what would need to be found next>"],
  "external_action_authorized": false
}
```

## Guardrails

- Never send, publish, enrich for credits, or contact anyone.
- A directory omission is not proof of absence. Say what you could not find.
- An inferred finding is labelled `inferred` and will not score. That is correct.
- Do not classify the service route. That is the Prospect Router's job.
- If the evidence shows the prospect is below the BridgeWorks engagement floor, say
  so plainly. A verified negative is a useful result and it scores zero honestly.
