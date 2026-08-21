# Handoffs

A handoff is a proposal from implementation to operating state. It is not canonical.

Claude Code owns implementation writes and produces handoffs here. Codex owns
operating-state writes and decides whether to persist a handoff as a transition
receipt or canonical entity state.

Nothing in this folder is a lifecycle advancement, an approval, or an executable
artifact. A handoff that is never persisted simply expires as a proposal.

| Rule | Why |
|---|---|
| A handoff never advances a lifecycle stage | Advancement needs a receipt, and receipts are operating state |
| A handoff never becomes a competing batch truth | The canonical cohort receipt is the baseline |
| A handoff records its evidence provenance and any withdrawn source | So the reader can tell what was scored and what was not |
