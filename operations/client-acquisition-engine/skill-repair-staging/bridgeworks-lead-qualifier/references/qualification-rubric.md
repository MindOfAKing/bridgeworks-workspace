# Qualification rubric pointer

Canonical model: `qualification-v1` in
`operations/internal-gtm/scripts/qualification_v1.py`, backed by the single
arithmetic and gate implementation in `operations/internal-gtm/scripts/gtm_core.py`.

Dimensions: problem evidence 25, commercial fit 20, buyer accessibility 15,
trigger urgency 15, proof fit 15 and execution readiness 10.

Tiers: HOT 85+, STRONG 70+, QUALIFIED 55+, WATCH 40+ and DO_NOT_PURSUE below 40.

Every positive component must cite evidence. The scorer returns numeric score and
actionability separately. Routing and diagnostic-family selection are not
qualification dimensions.

The former fit/change/problem/capacity/access rubric is retained only inside the
compatibility CLI for reading historical records. Its status must never advance
canonical GTM lifecycle state.
