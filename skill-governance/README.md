# Skill governance

## HOW TO USE

1. Put each external repository under `quarantine/<name>/` and pin its exact commit.
2. Run `python scripts/scan_skill.py quarantine/<name>`.
3. Complete `intake/INTAKE-TEMPLATE.yaml`.
4. Run `python scripts/capability_diff.py --proposal intake/<file>.yaml`.
5. Approve nothing until security, overlap, permissions, isolated testing, pilot, and success criteria are reviewed.

The live registry is `capability-registry.yaml`. It uses JSON syntax, which is valid YAML, so validation requires only Python's standard library.

## Governing gate

An external component may enter the active system only after:

1. Security review.
2. Capability-overlap review.
3. Permission review.
4. Isolated functional testing.
5. A defined real-work pilot.
6. A measurable success criterion.

Allowed decisions are `reject`, `reference_only`, `cherry_pick`, `pilot`, and `approve`.

> A security scan can identify known suspicious patterns, but it does not prove that a skill is safe, necessary, correct, or appropriate.

The scanner never installs a target. Quarantine contents, local virtual environments, raw scanner output, and converted documents are ignored by Git.

## Commands

```powershell
python skill-governance/scripts/registry_tool.py validate
python skill-governance/scripts/registry_tool.py generate
python skill-governance/scripts/scan_skill.py skill-governance/quarantine/NAME
python skill-governance/scripts/capability_diff.py --proposal skill-governance/intake/example.yaml
python skill-governance/scripts/markitdown_pilot.py --manifest skill-governance/markitdown-samples.json
python -m unittest discover -s skill-governance/tests -v
```

Use `--allow-outside-quarantine` on the scanner only for an explicit, reviewed exception. A clean scan is evidence, not approval.
