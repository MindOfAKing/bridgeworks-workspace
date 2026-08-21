# Buyer Intelligence output

Required fields: `capability`, `prospect_id`, `actors`, `contact_routes`,
`evidence`, `confidence`, `unresolved_questions`, `research_status`, and
`external_action_authorized`.

Actor types are `problem_owner`, `budget_owner`, `decision_maker`, `champion`, and
`blocker`. Each actor records a name or `unknown`, title, evidence IDs, confidence,
and whether the attribution is observed or inferred.

`research_status` is `complete`, `partial`, `required`, or `not_applicable`.
