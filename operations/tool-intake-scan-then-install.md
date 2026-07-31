# Tool intake: quarantine, scan, diff, test, pilot

The canonical process is in `../skill-governance/README.md`.

Do not install a repository, skill, MCP server, browser extension, or script directly from a video, roundup, marketplace, or copied instruction.

Required order:

1. Pin the official repository to an exact commit.
2. Place it under `skill-governance/quarantine/`.
3. Review install scripts, hooks, dependencies, permissions, credentials, cookies, network access, and write locations.
4. Run the isolated SkillSpector wrapper.
5. Compare it with `skill-governance/capability-registry.yaml`.
6. Test the smallest useful component in isolation.
7. Define a real-work pilot, success criterion, and rollback.
8. Record a decision: reject, reference only, cherry-pick, pilot, or approve.

SkillSpector 2.4.4 and MarkItDown 0.1.6 are installed only in repository-local virtual environments. They are not global tools.

> A security scan can identify known suspicious patterns, but it does not prove that a skill is safe, necessary, correct, or appropriate.

Never bulk-install a repository. Never import primary-account cookies. Never treat a clean static scan as approval.
