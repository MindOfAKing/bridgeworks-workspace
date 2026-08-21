# Phase 3 migration plan

Written 2026-08-11 at the end of Phase 2. Nothing here has been executed.

Phase 2 changed no live schedule or external behaviour. It added a deterministic
spine, mapped 199 stable meaningful files and 34 logical components, marked only migration-
conditional supersession, and tested Appinio plus a deliberately blocked partial
GEO run for Tilz Prosperitas.

Phase 3 is where things actually move. Every step below names its owner, its
verification, and what it does not touch.

## Sequencing rule

Steps 1 to 4 are prerequisites. Nothing in 5 onward is safe until they pass,
because each of them depends on the registry being current, the packet surface
being shared, and the objective selector having run in shadow.

---

## Step 1: Regenerate the canonical capability registry

**Owner:** Claude Code. **Blocks:** everything.

The registry was generated 2026-07-25 and does not represent the current native
Codex estate (64 skill directories observed on 2026-08-11). Every skill
authored on 2026-08-01 is invisible to it, including `bridgeworks-lead-qualifier`,
`bridgeworks-prospect-router`, `bridgeworks-geo-prospect-scan`,
`bridgeworks-revenue-system-scan` and `bridgeworks-ai-workflow-scan`.

The same audit must reconcile registered aggregate `geo-audit` with the five
native `agent-geo-*` Codex installations. The aggregate contract may remain owned
by Claude Code, but Codex routing must be able to resolve and invoke its native
subordinates without consulting a staged prose registry.

That gap is why a second registry got written inside the router skill.

```bash
python skill-governance/scripts/registry_tool.py generate
python skill-governance/scripts/registry_tool.py validate
python -m unittest discover -s skill-governance/tests
python operations/internal-gtm/scripts/capability_loader.py
```

**Verify:** the five 2026-08-01 skills and five native GEO specialists resolve by
id, `geo-audit` retains one aggregate owner, and `dangling references: 0` still
holds.

**Then:** add the five to the roles that should be permitted them in
`role-registry.yaml`. `lead-qualifier` gains `bridgeworks-lead-qualifier`.
`prospect-router` gains `bridgeworks-prospect-router` and the three bounded scans.

**Do not:** hand-edit the registry. It is generated. Editing it by hand is how it
drifts.

**Risk:** regeneration rewrites 5,371 lines and could drop metadata that was
hand-corrected since 25 July. Diff the generated file against the current one
before committing and check that no `security.result` or `last_reviewed` value is
silently reset.

---

## Step 2: Retire the second capability registry

**Owner:** Claude Code. **Depends on:** step 1.

`skill-repair-staging/bridgeworks-prospect-router/references/capability-registry.md`
carries a `SUPERSEDED_AFTER_MIGRATION` banner. Once step 1 makes the canonical
registry complete, replace its body with a pointer to
`skill-governance/capability-registry.yaml` and keep the work-pass routing table,
which has no equivalent anywhere else.

**Verify:** `capability_loader.assert_single_registry()` passes, and the router
skill still runs its own forward test.

---

## Step 3: Decide and implement one qualification contract

**Owner:** Claude Code. **Depends on:** step 1.

Two rubrics currently score the same prospects on different scales.
`score_prospect.py` uses fit 25 / active_change 25 / problem_evidence 20 /
capacity 15 / buyer_access 15 with a 65-point gate.
`gtm_core.RUBRIC` uses route fit 30 / trigger 20 / evidence 20 / reachability 15 /
gap severity 15 with HOT at 75.

First present both rubrics, their gates, and replay results to Emmanuel. Record the
canonical decision. Then make the non-canonical entry point a thin wrapper or an
explicitly versioned translator while keeping the native Codex skill's CLI and
output contract stable.

**Verify:** replay all three live-test runs (`appinio`, `silver-lining`,
`bridgeworks-dogfood`) through the wrapper. The dogfood run scored
`discovery-ready` at 100/100 with eight verified signals. If the unified rubric
does not also clear the gate on that run, the mapping is wrong, not the run.

**Do not:** silently declare the migration rubric canonical or change thresholds
during the plumbing step. Decide first, unify second, tune later.

---

## Step 4: Shadow-run the daily objective selector

**Owner:** Codex to schedule, Claude Code owns the code. **Depends on:** nothing.

Ten weekdays. The live 09:10 job runs unchanged. `engine_snapshot.py --select`
runs alongside and writes to `runs/daily-objective/`.

**Ready when all four hold:**

1. it never selected `generate_new_companies` on a day when a ready and uncontacted
   prospect existed;
2. every `blocked_unverified` result matched a real connector or file failure;
3. the objectives chosen were ones Emmanuel agreed were correct;
4. no run wrote to the acquisition engine, confirmed by mtime comparison.

**Also fix during the shadow period:** `engine_snapshot.CAPACITY` currently hardcodes
a coverage target of 4 and an approval cap of 3. Set them from Emmanuel's real
weekly capacity before the cutover, not after.

**Do not:** change the cron entry. That is step 9.

---

## Step 5: Score the backlog with the real rubric

**Owner:** Claude Code, with Emmanuel reviewing the classifications.

39 of 41 researched prospects carry a provisional tier derived from engine
readiness. Two have a real score.

For each of the 9 ready prospects: run the adapter, produce a classification file
with quoted rationale, run the slice, and store the run record. Nine classifications
is roughly an hour of review, and it replaces every provisional tier that matters.

**Verify:** `route_depth` in the snapshot becomes real, so
`investigate_new_market_need` and the supply gate start working on measured
coverage instead of an empty dictionary.

**Expect disagreement.** Some of the nine will not clear HOT or WARM under the real
rubric. That is the point of running it. Record which ones and why.

---

## Step 6: Write internal-GTM packets into the existing approval surface

**Owner:** Claude Code builds the adapter, Codex wires the run.

Today an internal-GTM packet stops at `awaiting_approval` inside
`runs/geo/`. The engine's approval surface is
`research/prospect-operations/review/` with a durable state file and an append-only
event log holding 20 waiting external tasks.

Two approval surfaces is the exact duplication this whole exercise exists to avoid.

Build `adapters/review_packet.py` writing an internal-GTM packet into the engine's
review state as an external task, carrying the `approval_payload_digest` so approval
binds to exact copy.

**Verify:** a packet appears in `prospect-review-state.json`, an event appears in
`prospect-review-events.jsonl`, and `prospect_review_queue.py` reads it without
modification.

**Do not:** create a second approval queue in internal-gtm. If the adapter cannot
write to the engine's surface, stop and reopen the design.

---

## Step 7: Measure the three prospect lists before merging them

**Owner:** Claude Code.

Three acquisition-engine lists exist and their overlap has never been measured:

| List | Rows |
|---|---:|
| `research/prospect-operations/prospect-source-current.csv` | 100 |
| `research/prospect-operations/operating-output/canonical-prospect-register.csv` | 60 |
| `SERVICE-LINE-PROSPECT-LIST-2026-08-01.csv` | 26 |

Plus two more outside the engine: `operations/lead-engine-v1/01-prospects/prospect-batch-2026-07-14.csv`
(45) and `pipeline/prospecting/prospect-tracker.csv` (27).

`gtm_core.dedupe` is the tool. It merges on exact domain or normalized company,
reports every merge with a reason, and is order-independent by test.

**Deliverable:** a merge report, not a merge. Counts of unique entities, exact
duplicates, and rows that produce no key at all. Emmanuel decides what becomes
canonical after seeing the numbers.

**Do not:** write a merged file in this step.

---

## Step 8: Port the production ceilings

**Owner:** Claude Code.

`validate_route.py` enforces limits internal-GTM has no equivalent for: at most four
work passes, a 1 to 20 minute asset production ceiling, an overproduction check that
rejects a plan mentioning proposal, full audit, ROI estimate or CRM migration
architecture at initial contact, and mandatory stop conditions and approval gates.

These are the rules that stop a first touch turning into a free consulting project.
They belong in `gtm_core`, enforced on the packet, not in a validator that only runs
when someone hands it a plan.

**Verify:** a packet that names a proposal or an ROI estimate raises, the same way
citing unapproved evidence raises today.

---

## Step 9: Cut over the 09:10 schedule

**Owner:** Codex. **Depends on:** steps 4, 5 and 6. **Requires Emmanuel's explicit approval.**

Change `orchestrator-schedule.json` entry `prospect-evidence-weekday` to run the
objective selector, and have `generate_new_companies` be the only objective that
calls `prospect_research_queue.py prepare`.

`prospect_research_queue.py` is not deleted. It becomes one of nine possible actions
instead of the only one.

**Rollback:** revert the schedule entry. The old job is unchanged and still works.

---

## Step 10: Decide the three retirements

**Owner:** Emmanuel decides, Codex executes. **Depends on:** step 7.

Only after the merge report exists:

| Surface | Question |
|---|---|
| `operations/lead-engine-v1/` | Migrate the 3 real Gmail send records and the 10 lead-leak reviews, then archive read-only? |
| `pipeline/prospecting/` | Anything here not already in the engine's 100-row source? |
| Duplicate prospect Sheets | Which single list is canonical? |

The preserve inventory at `receipts/2026-08-11-preserve-inventory.md` lists the
irreplaceable state, including three Gmail message and thread IDs that exist nowhere
else in the repository.

**Nothing is shut down, revoked or archived without Emmanuel's approval per surface.**

---

## What Phase 3 does not do

- No outreach. The last stage code can reach stays `awaiting_approval`.
- No CRM writes. HubSpot writes stay blocked until the connector is reauthorized.
- No deletion of anything in the acquisition engine.
- No Hermes changes. Those jobs are outside this repository and uninventoried.
- No change to `operations/client-acquisition-engine/` beyond the markers already
  placed, until the step that names the file.

## Effort estimate

| Step | Rough effort | Can run unattended |
|---|---|---|
| 1 Registry regeneration | 30 min plus diff review | No, the diff needs eyes |
| 2 Retire second registry | 20 min | Yes |
| 3 One rubric | 2 hours with replay tests | Yes |
| 4 Shadow run | 10 weekdays, 5 min a day | Yes |
| 5 Score the backlog | 1 hour of classification review | No, Emmanuel reviews |
| 6 Approval adapter | 2 hours | Yes |
| 7 Merge report | 1 hour | Yes |
| 8 Production ceilings | 1 hour | Yes |
| 9 Schedule cutover | 15 min | No, needs approval |
| 10 Retirement decisions | Emmanuel's time | No |

Steps 2, 3, 6, 7 and 8 can run in parallel with the step 4 shadow period.
