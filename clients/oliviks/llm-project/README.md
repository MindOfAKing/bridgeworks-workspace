# Oliviks LLM Project Folder

Purpose: keep every AI tool working from the same facts while giving each tool its own sandbox.

This folder is the shared coordination layer for the Oliviks Kitchen rebuild. It is not the production site. It is where prompts, outputs, source briefs, copy, design notes, and build handoffs live before they move into implementation.

## Project Rule

Manus is a teaser/prototype only. The final build starts from the Foundation scope, confirmed facts, and direct-order priority.

## Confirmed Facts

- Client: Oliviks Nigerian Kitchen / Oliviks KFT
- Location: Rakoczi ter 9, 1084 Budapest, Hungary
- Founders: Cynthia and Aese
- Founder story: Nigerian couple, studied for their Masters in Debrecen, then created Oliviks Kitchen
- Proof: 4.8 stars from 160+ Google reviews
- Press: Origo, We Love Budapest, WMN
- Platforms: Wolt and Foodora exist, but should be secondary
- Commercial priority: direct ordering first
- Foundation fee: 272,611 HUF
- First invoice: EO-2026-11, 136,306 HUF

## Pipeline

1. ChatGPT: voice and competitor research brief
2. NotebookLM: source-grounded proof, quotes, and founder details
3. Claude: final website copy
4. Nano Banana: campaign food visuals
5. Google Stitch: mobile-first page layouts
6. v0: frontend build
7. Codex: integration, verification, local files, final handoff

## Folder Map

- `00-shared/`: canonical facts, rules, source list, and access checklist
- `01-chatgpt/`: strategy prompt and output
- `02-notebooklm/`: source-grounded extraction prompt and output
- `03-claude/`: copywriting prompt and output
- `04-nano-banana/`: image generation prompt and outputs
- `05-google-stitch/`: layout prompt and exported layout notes
- `06-v0/`: build prompt and generated code handoff
- `07-codex/`: implementation notes, QA, decisions, and final delivery logs

## What Every Tool Must Preserve

- Cynthia and Aese, not Olivia
- Debrecen origin story
- Nigerian food first
- Direct order first
- Wolt/Foodora secondary
- No organic/pesticide-free/wellness positioning
- No fake testimonials
- No invented prices, hours, awards, or quotes
- No production claims unless verified

