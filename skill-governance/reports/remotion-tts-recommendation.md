# Remotion and local TTS recommendation

## Existing capability

Do not build a new video system.

Two working Remotion 4 setups already exist:

- `clients/ceefm/brand-visuals/remotion-video` with 15-second and 30-second EN/HU renders in three aspect ratios.
- `BridgeWorks-Content-Studio/06_Production/Remotion/bridgeworks-content-engine-v2` with pinned Remotion 4.0.489, typecheck, pilot render, representative render, and render-matrix scripts.

The content engine already states that rendered masters are silent and that voice/audio needs approved direction and usage rights.

## Recommended reusable template

Extend the existing BridgeWorks content engine with one BridgeWorks AI Visibility explainer.

Architecture:

Verified source evidence  
to approved script  
to structured scene data  
to existing Remotion render  
to optional manual finishing  
to approval queue  
to manual publishing

Required scene-data fields:

- Claim.
- Source path or URL.
- Evidence date.
- Display text.
- Visual treatment.
- Duration.
- Required disclaimer.
- Approval status.

Success criterion: one 30-second silent master renders in 16:9, 1:1, and 9:16 from the same scene data, passes typecheck and visual QA, and contains no unsupported claim.

## Local TTS

Use local TTS only for timing, pronunciation, and draft pacing.

Do not replace a licensed client-facing voice service until voice quality, speaker consent, attribution, model licence, and commercial-use rights are documented. Keep generated audio out of final client work until manual approval.
