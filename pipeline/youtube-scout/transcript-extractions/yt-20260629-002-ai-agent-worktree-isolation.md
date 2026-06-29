# YouTube Extraction - AI Agent Worktree Isolation SOP

Date: 2026-06-29  
Source: `Run Multiple AI Agents in Parallel (Claude Code Tutorial)`  
URL: https://www.youtube.com/watch?v=n35KalqEwJc  
Transcript: `pipeline/youtube-scout/runtime-transcripts/n35KalqEwJc.txt`  
Decision: Adapt  
BridgeWorks area: AI Delivery Verification, Website Production System, Agency Operations

## Core extraction

Parallel AI coding only works when each agent has a separate working directory and a separate branch.

The useful pattern is git worktrees:

1. Keep one repo as the source of truth.
2. Create one worktree per task or feature.
3. Run one Codex or Claude Code session inside each worktree.
4. Only parallelize tasks that do not touch the same files.
5. Verify each output before commit or merge.
6. Use comparison mode when two agents should solve the same task in different ways.
7. Keep project-level `AGENTS.md` or `CLAUDE.md` context available in every worktree.

## Evidence

- 00:15 to 00:28: multiple agents in the same directory create file collisions because they read and write the same files.
- 01:33 to 02:19: git worktrees decouple one repo from multiple working directories. Each worktree has separate files and a separate branch.
- 04:22 to 04:58: naming worktrees by project and feature helps avoid confusion and overlap.
- 08:26 to 12:30: the example runs backend and UI work in separate worktrees because the tasks do not overlap.
- 13:20 to 14:59: each branch still needs status checks, testing, commit, PR, merge, and conflict awareness.
- 15:43 to 16:22: shared agent context can live in the project-level MD file. Worktree-specific context can be added when needed.
- 16:27 to 17:07: the most useful worktree pattern can be agent-versus-agent comparison for architecture choices.
- 19:08 to 19:39: use worktrees when tasks do not share the same file, or when a risky task needs two approaches. Avoid worktrees for whole-codebase or exploratory tasks.

## BridgeWorks adaptation

Create a guarded SOP for Codex / Claude Code delivery:

- Use one worktree per non-overlapping implementation task.
- Keep the main workspace clean.
- Do not run two agents against the same files.
- Add a short task brief in each worktree if the task needs extra context.
- Verify with tests, screenshots, rendered output, or app behavior before accepting.
- Merge only after review.
- Do not commit or push without Emmanuel approval.

## Guardrails

- This is for AI tools to execute, not for Emmanuel to manually debug.
- No parallel agents on client work without a clear rollback path.
- No broad refactors in parallel.
- No commit or push from this routine.

## One BridgeWorks action

Add an `AI Agent Worktree Isolation` row to the AI Delivery Verification Checklist and Website Production System.
