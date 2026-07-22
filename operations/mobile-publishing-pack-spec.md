# Mobile Publishing Pack Specification

Version: 1.0 (proposed)
Created: 2026-07-22
Owner: Emmanuel Ehigbai
Status: Specification only. This file defines the structure; it does not create the pack, write to Drive, or publish anything. Codex assembles the pack in the canonical Drive system after content is drafted and approved.

The Mobile Publishing Pack is cloud-first and phone-accessible. No required publishing step may depend only on a local laptop file. The pack lives in the canonical Drive Content Studio, one folder per week.

## Weekly pack structure

`YYYY-MM-DD Weekly Pack`

- `00 Weekly Overview`
- `01 Approval Sheet`
- `02 Personal LinkedIn`
- `03 BridgeWorks LinkedIn`
- `04 Personal Instagram`
- `05 BridgeWorks Instagram`
- `06 Personal Facebook`
- `07 BridgeWorks Facebook`
- `08 Nigerian WhatsApp Status`
- `09 X`
- `10 TikTok`
- `11 Analytics and Receipts`

## Per-item fields

Every content item in the pack includes:

- Content ID
- Master thesis ID
- Origin channel
- Amplification channels
- Channel-specific copy
- Asset filename
- Dimensions
- Editable-source link
- Preview link
- Hook
- CTA
- First comment where relevant
- Alt text
- Link destination
- Proposed date and time
- Approval status
- Publishing owner
- Rights status
- Evidence source
- Unresolved issues
- Posted URL
- Measurement fields

## Rules

- Cloud-first: the pack must be openable and approvable from a phone.
- Nothing publishes automatically. Publishing is approval-gated per the runbook.
- The Nigerian WhatsApp Status item carries the 9:16 asset and caption only; posting is manual and the number is never stored.
- Codex owns pack assembly, Content ID registration, and the approval queue. Claude Code builds the templates and validation, not the approvals.
