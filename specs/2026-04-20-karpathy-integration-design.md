# Karpathy Rules + Token Efficiency — Workspace Integration

**Date:** 2026-04-20
**Owner:** Emmanuel Ehigbai
**Source:** [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)

## Goal

Integrate Andrej Karpathy's four behavioral principles plus a fifth "Token Efficiency" rule across all workspaces (local + GitHub + Drive) using a hybrid approach. Augment existing CLAUDE.md files without stripping content.

## Definition of Done

1. Global `~/.claude/CLAUDE.md` has a new **Behavioral Rules** section (5 rules) appended, no existing content removed.
2. Each per-repo CLAUDE.md (5 existing + 1 new for ceefm-astro) has a **Behavioral Rules** footer appended, no existing content removed.
3. Each git-tracked repo has a commit pushed to `main` with the change.
4. A Drive reference doc exists at `Work&Business / Claude Operating System / claude-behavioral-rules.md`.

## The Five Rules (canonical text)

### 1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs. State assumptions explicitly. If uncertain, ask. If multiple interpretations exist, present them. If simpler exists, say so. If unclear, stop and name what's confusing.

### 2. Simplicity First
Minimum code that solves the problem. Nothing speculative. No features beyond what was asked. No abstractions for single-use code. No configurability that wasn't requested. No error handling for impossible scenarios.

### 3. Surgical Changes
Touch only what you must. Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style. Every changed line must trace directly to the request.

### 4. Goal-Driven Execution
Transform tasks into verifiable goals. Strong success criteria let the agent loop independently. Weak criteria ("make it work") require constant clarification. State a brief plan for multi-step tasks.

### 5. Token Efficiency
Drop conversational fluff. Concise, direct answers. No restating of the question. No trailing summaries the user can read from the diff. Save context for work, not ceremony.

## Scope

### Global
- File: `C:\Users\ELITEX21012G2\.claude\CLAUDE.md`
- Action: **append** new section. Keep all existing content (identity, brand voice, session protocol, colors, typography).

### Per-repo (augment existing)
| Repo | Path | Git remote |
|---|---|---|
| bridgeworks-agency | `C:\Users\ELITEX21012G2\bridgeworks-agency` | MindOfAKing/bridgeworks-agency |
| bridgeworks-workspace | `C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace` | MindOfAKing/bridgeworks-workspace |
| mindofaking-workspace | `C:\Users\ELITEX21012G2\Projects\mindofaking-workspace` | MindOfAKing/mindofaking-workspace |
| personal-brand-workspace | `C:\Users\ELITEX21012G2\Projects\personal-brand-workspace` | MindOfAKing/personal-brand-workspace |
| business-brain | `C:\Users\ELITEX21012G2\Projects\business-brain` | local only |

### Per-repo (create new)
| Repo | Path | Git remote | Contents |
|---|---|---|---|
| ceefm-astro | `C:\Users\ELITEX21012G2\ceefm-astro` | MindOfAKing/ceefm-astro | Astro stack notes + CEEFM client context + Behavioral Rules footer |

### Drive
- Folder: `Work&Business / Claude Operating System /` (new subfolder)
- File: `claude-behavioral-rules.md`
- Content: the five rules as written above, plus source link

## Non-goals
- No refactoring of existing CLAUDE.md content
- No removal of any existing behavioral guidance
- No enforcement tooling (hooks, pre-commit checks)

## Commit policy
One commit per repo. Message: `docs: add Claude behavioral rules (Karpathy + token efficiency)`. Confirm before push on each.
