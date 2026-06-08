# Cross-Tool Sandbox Setup

Each tool should have its own sandbox but receive the same canonical facts.

## ChatGPT Sandbox Needs

Input:
- Canonical brief
- ChatGPT strategy prompt
- Any current competitor/source links

Output:
- Voice and competitor research brief
- Positioning map
- Voice principles

Save as:
- `01-chatgpt/STAGE-1-VOICE-COMPETITOR-BRIEF.md`

Rules:
- Browse if available
- Mark unverified claims
- Do not write final website copy

## NotebookLM Sandbox Needs

Input:
- Origo article
- We Love Budapest article
- WMN article
- Google review excerpts
- NotebookLM extraction prompt

Output:
- Source-grounded proof points
- Direct quotes
- Founder/source details
- Recurring praise themes

Save as:
- `02-notebooklm/STAGE-2-SOURCE-GROUNDED-BRIEF.md`

Rules:
- Use loaded sources only
- No outside facts
- Preserve conflicts

## Claude Sandbox Needs

Input:
- Canonical brief
- Stage 1 voice brief
- Stage 2 source brief
- Claude copy prompt

Output:
- Final copy for homepage, about, menu intro, contact page

Save as:
- `03-claude/STAGE-3-WEBSITE-COPY.md`

Rules:
- No em dashes
- No generic restaurant copy
- No unsupported claims
- Direct order first

## Nano Banana Sandbox Needs

Input:
- Canonical brief
- Visual prompt
- Any real food/founder photos if available

Output:
- Hero banner visual
- Rating feature card visual
- Pepper soup feature visual
- Suya feature visual

Save as:
- `04-nano-banana/outputs/`
- `04-nano-banana/STAGE-4-VISUAL-NOTES.md`

Rules:
- Prefer image without baked-in text if text rendering is weak
- Keep negative space for overlay text
- Avoid fake logos and distorted hands

## Google Stitch Sandbox Needs

Input:
- Canonical brief
- Stage 3 final copy
- Stage 4 visual direction or selected visuals
- Stitch layout prompt

Output:
- Mobile homepage layout
- Desktop homepage layout
- Mobile about layout
- Desktop about layout
- Responsive notes
- Component annotations

Save as:
- `05-google-stitch/STAGE-5-LAYOUT-BRIEF.md`
- screenshots/exports in `05-google-stitch/outputs/`

Rules:
- Mobile first
- Direct order primary
- Wolt/Foodora secondary
- Build-ready annotations

## v0 Sandbox Needs

Input:
- Canonical brief
- Stage 3 copy
- Stage 5 layout brief
- Approved image assets or placeholders
- v0 build prompt

Output:
- React components
- Pages: home, about, menu, contact
- Shared nav/footer/components

Save as:
- `06-v0/STAGE-6-V0-OUTPUT.md`
- code export in `06-v0/code/`

Rules:
- No fake form
- No invented prices/hours
- No unsupported claims
- Semantic, responsive, accessible

## Codex Sandbox Needs

Input:
- All stage outputs
- Approved assets
- Client access/materials

Output:
- Local implementation
- QA notes
- Production handoff
- Evidence log

Save as:
- `07-codex/IMPLEMENTATION-LOG.md`
- `07-codex/QA-CHECKLIST.md`
- `07-codex/HANDOFF.md`

Rules:
- Do not publish without approval
- Do not mutate client systems without access confirmation
- Keep source files and historical documents separate

