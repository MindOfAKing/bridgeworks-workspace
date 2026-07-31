# Capability Diff

## Proposed component

skills/programmatic-seo

## Claimed function

Create SEO-driven pages at scale using templates and structured data while avoiding thin content.

## Classification

Improvement candidate

## Existing equivalents

- `geo-schema` (evidence score 130): `C:\Users\User\.claude\skills\geo-schema`
- `geo-content` (evidence score 125): `C:\Users\User\.claude\skills\geo-content`
- `geo-technical` (evidence score 120): `C:\Users\User\.claude\skills\geo-technical`
- `market-seo` (evidence score 105): `C:\Users\User\.claude\skills\market-seo`
- `market-landing` (evidence score 100): `C:\Users\User\.claude\skills\market-landing`
- `gsc-opportunity` (evidence score 62): `C:\Users\User\.claude\skills\gsc-opportunity`
- `generate-image` (evidence score 54): `C:\Users\User\.claude\skills\generate-image`
- `geo-report-pdf` (evidence score 54): `C:\Users\User\.claude\skills\geo-report-pdf`

## Genuine missing capability

Manual reviewer must confirm which deliverable or workflow stage is absent.

## Conflicts or duplication

Review the cited source files. Automated evidence is advisory and does not decide installation.

## Permission difference

Proposed: `{"network_access": "optional for research", "filesystem_access": "write only during an approved implementation", "credentials": false, "cookies": false, "external_executables": []}`

## Recommendation

- Reference only or cherry-pick procedure

## Evidence

### geo-schema (130)
Source: `C:\Users\User\.claude\skills\geo-schema/SKILL.md`
- purpose: shared terms data, structured
- proposal explicitly names this internal overlap

### geo-content (125)
Source: `C:\Users\User\.claude\skills\geo-content/SKILL.md`
- purpose: shared terms content
- workflow: shared terms assessment, quality
- proposal explicitly names this internal overlap

### geo-technical (120)
Source: `C:\Users\User\.claude\skills\geo-technical/SKILL.md`
- purpose: shared terms seo
- triggers: shared terms seo
- proposal explicitly names this internal overlap

### market-seo (105)
Source: `C:\Users\User\.claude\skills\market-seo/SKILL.md`
- workflow: shared terms quality
- proposal explicitly names this internal overlap

### market-landing (100)
Source: `C:\Users\User\.claude\skills\market-landing/SKILL.md`
- proposal explicitly names this internal overlap

### gsc-opportunity (62)
Source: `C:\Users\User\.claude\skills\gsc-opportunity/SKILL.md`
- purpose: shared terms data, pages, seo
- triggers: shared terms seo
- tools: shared terms filesystem
- workflow: shared terms data

### generate-image (54)
Source: `C:\Users\User\.claude\skills\generate-image/SKILL.md`
- purpose: shared terms create, using
- tools: shared terms filesystem

### geo-report-pdf (54)
Source: `C:\Users\User\.claude\skills\geo-report-pdf/SKILL.md`
- purpose: shared terms data, using
- tools: shared terms filesystem
- workflow: shared terms data
