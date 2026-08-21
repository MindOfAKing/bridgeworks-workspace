# Claude Design — capture and BridgeWorks adaptation

**Source:** HubSpot / Futurepedia, "Claude Design in Action: 7 Use Cases To Try Today"
`https://offers.hubspot.com/view/claude-design-use-cases-futurepedia`
**Captured:** 2026-08-09. Page is ungated, no form required.

**Accuracy note:** the page states Claude Design runs on "Claude Opus 4.7". That is stale. Current models are the Claude 5 family. Treat every model claim on that page as unverified. The workflow structure is still sound.

## HOW TO USE
1. Set up the design system once (block below) so every output is on-brand from the first draft.
2. Pick the workflow you need from the seven below.
3. Copy the prompt, fill the brackets, attach the prep files.
4. Ask Claude to review before exporting.

---

## One-time setup: BridgeWorks design system

Configure during Claude Design onboarding:

- Company: BridgeWorks
- Colors: Navy `#0F1A2E`, Gold `#B8860B`, Ivory `#F5F0E8` (default background, never white), Sage `#4A6741`, Charcoal `#1C2B3A`, Warm Gray `#6B6560`
- Body font: Inter (300, 400, 500, 600)
- Headline font: Playfair Display (400, 700) — headlines only
- Logo: `C:/Users/User/Projects/brand-assets/`
- Optional repo link for component reference: `C:/Users/User/Projects/bridgeworks-agency`

Voice rules to paste into every prompt: no em dashes, no AI slop words (world-class, seamless, transformative, leverage, robust, cutting-edge, game-changing, ecosystem, innovative, passionate about), short sentences, one idea per sentence, specific over general, real numbers and real timelines.

---

## The six-step framework

1. **Prep input.** Gather notes, docs, screenshots, brand assets. Upload for context.
2. **Start simple.** Write the prompt as a creative brief: goal, audience, constraints, format.
3. **Review draft.** Check structure, content, flow before touching visuals.
4. **Refine.** Global changes through chat, local changes through inline comments, then propagate across all screens.
5. **Ask Claude to review.** Readability, hierarchy, contrast, accessibility.
6. **Export.** PPTX, PDF, Canva, standalone HTML, or Claude Code handoff.

---

## The seven workflows

### 1. Discovery notes to pitch deck
**Use for:** BridgeWorks proposals after a discovery call. Pairs with `/discovery-call-prep` and `/new-proposal`.
**Prep:** call notes, design system, prior deck as PPTX, competitor screenshots.
**Export:** PPTX, Canva, internal URL.

> Create a 12-slide pitch deck for [PROSPECT COMPANY]. They're a [SIZE] company struggling with [PAIN POINT]. Their buying committee includes [ROLES]. Use our brand system. Structure: company overview (1), their problem (2), our solution mapped to their challenges (3), case study (2), pricing (1), implementation timeline (1), next steps (1), Q&A (1). Tone: confident but consultative.

**Check:** does the problem framing match what they actually said? Are solution slides specific to their case? Does it flow problem, solution, proof, action?

### 2. PRD to clickable wireframes
**Use for:** client website and platform scoping before build.
**Prep:** spec or PRD, existing product screenshots, user flows, design system.
**Export:** Claude Code handoff, Canva, internal URL.

> Create a clickable wireframe for [FEATURE NAME] based on the attached PRD. This is a [TYPE]. Primary user: [ROLE]. Key requirements: [LIST 3-5]. Use our design system. Start with main screen and 2-3 supporting screens showing core user flow. Keep functional, not polished, we're aligning on structure first.

### 3. Campaign brief to one-pager
**Use for:** service one-pagers, the audit entry offer sheet, client campaign collateral.
**Prep:** brief or bullets, logos, a prior one-pager as reference.
**Export:** PDF, Canva.

> Create a one-page marketing document for [PRODUCT/CAMPAIGN]. Audience: [TARGET]. Key message: [CORE VALUE PROP]. Include: headline, 3-4 key benefits with supporting details, one customer proof point or stat, and clear CTA. Use our brand system. Tone: [PROFESSIONAL/CONVERSATIONAL/BOLD]. Format: single-page PDF layout.

**Check:** scannable in ten seconds? Headline states the value without jargon?

### 4. Live meeting to prototype
**Use for:** client calls where a visual settles the argument faster than a follow-up email.
**Prep:** open Claude Design before the call, design system connected.
**Export:** internal URL, share on the spot.

> Create a quick prototype for [CONCEPT DISCUSSED]. It should show [KEY SCREENS/SECTIONS]. Primary user: [ROLE]. Keep it rough, we're capturing the idea, not polishing. Use our brand system.

Before wrapping: "Quick review: flag big issues only. We're wrapping up a meeting."

### 5. Competitor screenshots to landing page
**Use for:** client landing pages and BridgeWorks campaign pages. Feeds straight into Claude Code and the Next.js stack.
**Prep:** 2-4 reference screenshots, value prop, audience, design system.
**Export:** standalone HTML, Canva, Claude Code.

> Create a landing page for [PRODUCT NAME]. Target audience: [WHO]. Core value prop: [ONE SENTENCE]. Use attached competitor screenshots as visual inspiration for layout and structure, but use our brand system for colors, typography, components. Include: hero with headline and CTA, 3-4 feature/benefit sections, social proof (testimonials or logos), final CTA. Optimize for desktop and mobile.

**Check:** on-brand, not a competitor clone. Mobile-responsive. Ivory ground, not white.

### 6. Strategy doc to visual roadmap
**Use for:** client engagement roadmaps, the 16-week style delivery plan, internal quarterly plans.
**Prep:** strategy doc or OKRs, prior roadmap format, audience context.
**Export:** PDF, PPTX.

> Transform the attached strategy document into a visual roadmap. Audience: [BOARD/INVESTORS/TEAM]. Timeframe: [PERIOD]. Show: key initiatives grouped by [THEME/TEAM/QUARTER], milestones, dependencies between workstreams, current status. Use our brand system. Format: [SINGLE-PAGE/MULTI-SLIDE]. Tone: [EXECUTIVE/OPERATIONAL/STRATEGIC].

**Check:** strategy grasped in under 30 seconds? Dependencies obvious?

### 7. Social asset templates
**Use for:** the LinkedIn and Instagram cadence across BridgeWorks, Emmanuel Ehigbai, and MindOfAKing. Pairs with `/content-week` and `/generate-social-visual`.
**Prep:** best-performing post screenshots, brand guidelines, platform specs, content categories.
**Export:** Canva for sizing and scheduling, PDF for approval, HTML for embeds.

> Create a set of social media templates for [BRAND]. Platforms: [LINKEDIN, INSTAGRAM, X/TWITTER]. Templates for: [PRODUCT ANNOUNCEMENT, THOUGHT LEADERSHIP, CUSTOMER STORY, EVENT PROMO]. Each template: headline zone, body text zone, image/visual zone, CTA zone, branded footer. Use our brand system. Design so any team member can swap copy and images without breaking layout.

---

## Tool routing

| Job | Tool |
|---|---|
| Prompt to first visual | Claude Design |
| Pixel-perfect production design | Figma |
| Final asset polish and scheduling | Canva |
| Production code | Claude Code |
| Cross-app pipelines | n8n |

## Limits and caveats

- Inline comments sometimes vanish before Claude reads them. Paste feedback into chat instead.
- A 15-slide deck takes roughly 10 minutes to generate.
- Usage counts against the Claude plan quota. Heavy prototyping sessions burn through it.
- Requires Pro, Max, Team, or Enterprise and the top model selected.
- Treat output as exploration, not final production. Export to Canva, Figma, or Claude Code for the finish.
- Specify mobile, tablet, desktop requirements in the first prompt, not later.

## Notes for BridgeWorks

Highest value here is workflow 1 and 3. Proposal decks and one-pagers are the current bottleneck between a discovery call and a signed engagement, and both are pure design labour with no code involved. Workflow 5 overlaps with what Claude Code already does better for the Next.js stack, so use it only for concept exploration, not for shipping pages.
