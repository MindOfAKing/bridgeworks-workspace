# Secure skill governance and efficiency upgrade

Date: 2026-07-25  
Status: implementation complete, local validation complete, Git commit and push awaiting approval

## 1. Executive summary

BridgeWorks now has a local governance layer for discovering, comparing, scanning, piloting, and approving skills before installation. The work also adds a machine-readable design system, an evidence-controlled Engagement Architect skill, a bounded MarkItDown pilot, and explicit research and video recommendations.

No external candidate skill was installed. NVIDIA SkillSpector and Microsoft MarkItDown were installed only in repository-local virtual environments. Agent Reach, Last30Days, and the Marketing Skills bundle remain quarantined and inactive.

## 2. Workspace inspected

- `bridgeworks-workspace` instructions, memory, knowledge, operations, client records, automation layer, brand constants, existing Remotion projects, tracked artifacts, and Git state
- Live Claude and Codex skill directories
- Source mirrors in `claude-skills`
- SkillSpector, MarkItDown, Marketing Skills, Agent Reach, and Last30Days at pinned commits
- Existing YouTube scouting configuration

## 3. Capability inventory

The generated registry records 74 unique live capabilities across 76 installations. It stores purpose, triggers, inputs, outputs, tools, permission notes, security status, provenance, category, overlaps, and last-verified metadata.

Unknown fields remain explicitly `unknown`; the generator does not infer permissions or provenance that source instructions do not establish. The largest overlap clusters are the marketing and GEO suites. `bridgeworks-idea-to-content` exists in both Claude and Codex, while `daily-brief` has two Claude installations with the same declared identifier.

## 4. Governance implementation

Completed:

- Machine-readable registry and human-readable generated summary
- Intake template and candidate-specific intake records
- Quarantine boundary with ignored contents
- Scan wrapper, capability diff, registry generator and validator
- MarkItDown pilot runner and native sample inspector
- Automated governance failure-mode tests
- Canonical scan-before-install operating procedure

The scan wrapper blocks paths outside quarantine unless an explicit override is supplied, records repository and commit data, checks for installation and build hooks, defaults to static analysis, and returns non-zero for scanner failure or critical results.

## 5. Security findings

Whole-repository static scans rated all five external repositories critical because they contain broad code, fixtures, credential patterns, subprocesses, or browser and network surfaces. These ratings do not establish malicious intent, but they reject bundle-level installation under the current gate.

Selected Markdown-only Marketing Skills components scored low:

- Revenue operations: 8
- Churn prevention: 0
- Marketing loops: 0
- Programmatic SEO: 0
- App-store optimisation: 8

Agent Reach has material cookie, browser-data, proxy, credential, external-tool, and persistent-state scope. Last30Days has browser-cookie, API-key, subprocess, publishing, and persistent research-state scope. Neither was installed.

OSV network lookup was unavailable, so results rely on SkillSpector static analysis plus manual inspection. A scan does not prove that a skill is safe, necessary, correct, or appropriate.

## 6. Capability decisions

- Revenue operations: partial gap; reference only until a real proposal-to-invoice pilot
- Churn prevention: genuine gap without present BridgeWorks use; reject
- Marketing loops: conflicts with existing orchestration; reference its stopping-condition concept only
- Programmatic SEO: improvement candidate; reference only until a live client case exists
- App-store optimisation: genuine gap without present use; reject
- Agent Reach: reject installation; consider only a separately adapted public-source procedure
- Last30Days: reject installation; reuse only its source-quality, date, deduplication, and prior-findings schema

## 7. MarkItDown pilot

MarkItDown 0.1.6 was tested in an isolated local environment on a text-heavy PDF, structured DOCX, branded PPTX, meaningful XLSX, and visual PNG.

- PDF and DOCX produced useful text-first reductions
- PPTX preserved text but lost layout and brand meaning
- XLSX expanded the rough token footprint and lost native behaviour
- PNG produced no useful output without OCR or vision

Decision: optional first-pass preprocessing for selected digital, text-heavy PDF and DOCX files, plus small flat spreadsheets. Native or rendered review remains mandatory for visual documents, presentations, analytical workbooks, diagrams, images, and scanned files.

## 8. Design system

Completed a repository-level design system with:

- Verified colours and typography
- Machine-readable tokens
- Content style and prohibited patterns
- Accessibility and alt-text checks
- A validator with automated tests

Spacing, radius, grid, breakpoints, logo clearspace, and image style remain unresolved rather than invented. The system is derived from existing brand constants, knowledge files, messaging rules, and the live agency frontend.

## 9. Engagement Architect

Created and validated `engagement-architect` in the canonical `claude-skills` source and installed it in the live Claude skill directory after approval.

The skill converts discovery evidence into:

- A mobile-readable scope
- A full engagement specification
- Evidence labels
- Assumptions and unresolved questions
- Scope-creep controls
- Approval gates

It composes existing discovery, follow-up, qualification, audit, proposal, and market-proposal capabilities. It never invents prices, commitments, proof, or delivery terms. Four automated tests pass.

## 10. YouTube scouting

Added The Next New Thing AI to the watchlist with channel ID `UCNZEktrsM5oJZ-MK4jKPMOQ`. The source and live `youtube-intelligence` instructions now require:

- Provenance
- Claimed purpose
- Inputs and outputs
- Permission scope
- Security or privacy notes
- Overlaps
- Install hooks
- Suggested decision

Discovery never triggers automatic installation.

## 11. Research pilot designs

Three public-only, no-login pilot cases are defined for:

- Public skill and repository discovery
- Time-bounded public market research
- Public source triangulation for a BridgeWorks topic

The designs record source URL, publisher, publication date, discovery date, query, extract, claim, corroboration, contradiction, relevance, confidence, and prior-finding status. Cookies, authenticated accounts, private browser state, anti-bot workarounds, and persistent credentials are prohibited.

## 12. Remotion and TTS recommendation

Use the existing BridgeWorks Content Studio Remotion engine for one short AI Visibility explainer. Do not create another video stack.

Use local TTS only for draft timing and internal review. Final voice selection, publishing, paid services, client claims, and public release remain approval-gated.

## 13. Git hygiene

Expanded `.gitignore` for Python artifacts, local virtual environments, quarantine contents, scanner output, pilot samples and telemetry, test caches, logs, databases, build output, IDE metadata, and operating-system files.

No tracked secret-shaped value was found in the targeted scan. Existing `.env` examples were preserved. Several large tracked client and evidence files remain unresolved because removing or rewriting them would require a separate retention decision.

No user file was deleted. No commit or push was made.

## 14. Validation results

- Governance tests: 10 passed
- Design tests: 3 passed
- Engagement Architect tests: 4 passed
- Engagement Architect quick validation: passed
- Capability registry validation: passed
- Design-system validation: passed
- MarkItDown five-format pilot: completed

The failure-mode suite covers malformed registries, unknown metadata, duplicate capability scoring, quarantine escape, missing scanners, critical and warning results, install-hook detection, and missing converters.

## 15. Reproduction commands

Run from the `bridgeworks-workspace` root.

Validate the registry:

```powershell
python skill-governance\scripts\registry_tool.py validate
```

Regenerate the live registry:

```powershell
python skill-governance\scripts\registry_tool.py generate
```

Scan a quarantined repository or skill:

```powershell
python skill-governance\scripts\scan_skill.py skill-governance\quarantine\<candidate>
```

Compare a proposal with active capabilities:

```powershell
python skill-governance\scripts\capability_diff.py --proposal skill-governance\intake\<candidate>.yaml --output skill-governance\reports\capability-diff-<candidate>.md
```

Run the MarkItDown pilot:

```powershell
python skill-governance\scripts\markitdown_pilot.py --manifest skill-governance\markitdown-samples.json --cli skill-governance\.venv-markitdown\Scripts\markitdown.exe --output skill-governance\reports\markitdown-pilot-data.json
```

Run governance and design tests:

```powershell
python -m unittest discover -s skill-governance\tests -v
python -m unittest discover -s design-system\tests -v
python design-system\scripts\validate_design.py
```

Run Engagement Architect tests from `claude-skills`:

```powershell
python engagement-architect\scripts\test_engagement_architect.py
```

## 16. Rollback

- Governance and design-system rollback: remove the newly created repository directories and restore `.gitignore` and `youtube-watchlist.json` before commit.
- Local tool rollback: remove `skill-governance/.venv-skillspector`, `skill-governance/.venv-markitdown`, `.uv-cache`, quarantine contents, samples, and generated raw reports. These paths are ignored.
- Engagement Architect rollback: remove the live `~/.claude/skills/engagement-architect` directory and the source `claude-skills/engagement-architect` directory.
- YouTube instruction rollback: restore `claude-skills/youtube-intelligence/SKILL.md` and its live copy from the previous revision.

Do not run destructive rollback commands without resolving the exact targets and confirming approval.

## 17. Files created or modified

Main workspace:

- `.gitignore`
- `youtube-watchlist.json`
- `skill-governance/`
- `design-system/`
- `operations/tool-intake-scan-then-install.md`
- `sessions/2026-07-25-session.md`
- `03-automation-layer/codex-active-work.md`

Canonical Claude skill source:

- `claude-skills/engagement-architect/`
- `claude-skills/youtube-intelligence/SKILL.md`

Live Claude skills:

- `~/.claude/skills/engagement-architect/`
- `~/.claude/skills/youtube-intelligence/SKILL.md`

## 18. Unresolved items

- Git commit and push require explicit approval under workspace rules.
- Large tracked client and evidence files need a separate retention and history decision.
- OSV live vulnerability lookup should be repeated when approved network access is available.
- Design spacing, radius, grid, breakpoints, logo clearspace, and image style need verified source values.
- External candidate functional pilots should wait for a real use case and separate approval.

## 19. Recommended next pilot

Use the revenue-operations procedure as reference material during one real, approval-gated proposal-to-invoice handoff. Measure missing fields, manual handoffs, time saved, and conflicts with the existing BridgeWorks operating system. Do not install the full Marketing Skills bundle. Promote only a minimal BridgeWorks-native procedure if the measured gap persists.
