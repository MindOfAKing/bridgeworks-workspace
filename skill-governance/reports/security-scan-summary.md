# Security scan summary

Date: 2026-07-25  
Scanner: NVIDIA SkillSpector 2.4.4  
Pinned scanner source: `fd25398d7aa99353d86237b9c260759351f0e644`  
Mode: static only, isolated virtual environment  
OSV status: network lookup was unavailable in the sandbox, so SkillSpector used its static fallback

## Whole-repository scans

| Repository | Score | Severity | Issues | Interpretation |
|---|---:|---|---:|---|
| NVIDIA SkillSpector | 100 | CRITICAL | 816 | Repository-wide scan includes security rules, malicious test fixtures, credential-pattern tests, subprocess code, and provider code. Manual review is required |
| Microsoft MarkItDown | 100 | CRITICAL | 69 | Flags include hidden-instruction patterns, environment access, subprocess calls, scope, and incomplete OSV checks. The isolated pilot used only local conversion with plugins and LLM features disabled |
| Marketing Skills | 100 | CRITICAL | 122 | Full bundle contains many unrelated skills and example assets. Six critical matches came from harmful-content terms in an ad-creative example, not the five candidate procedures |
| Agent Reach | 100 | CRITICAL | 179 | Material credential, cookie, browser-data, subprocess, remote bootstrap, tool-install, and persistent configuration surface |
| Last30Days | 100 | CRITICAL | 682 | Large credential, cookie, browser, subprocess, network, state, and publishing surface across a large research engine |

These scores do not prove malicious intent. They do prove that full-repository installation is not acceptable under the current gate.

## Component scans

| Component | Score | Severity | Findings |
|---|---:|---|---|
| Revenue operations | 8 | LOW | One autonomous-decision warning |
| Churn prevention | 0 | LOW | None |
| Marketing loops | 0 | LOW | None |
| Programmatic SEO | 0 | LOW | None |
| App-store optimisation | 8 | LOW | Three context-window size warnings |

Low component scores do not approve installation. Capability, permission, isolated functional testing, pilot, and rollback review still apply.

## Manual permission findings

### Agent Reach

- Installs and routes several upstream command-line tools.
- Core dependencies include network clients and `yt-dlp`.
- Optional dependencies include Playwright and browser-cookie extraction.
- Stores configuration and tokens under `~/.agent-reach/`.
- Can read explicitly selected browser cookie databases.
- Installation guidance includes remote repositories, external binaries, MCP configuration, proxies, and authenticated platforms.
- Decision: reject installation in this batch. A future pilot may use only a separately adapted public-source procedure with no package install, cookies, proxy, browser session, or persistent credentials.

### Last30Days

- Bundles a large Python research engine and a vendored Node client.
- Supports many API keys and optional browser-cookie access.
- Writes Markdown, JSON, HTML, SQLite, queues, configuration, and library state.
- Can publish HTML only when explicitly requested, but publishing code exists.
- Public-only sources are possible, but the default skill includes setup paths that encourage browser-cookie scanning.
- Decision: reject installation in this batch. Reference its source-quality, date, deduplication, and prior-findings fields only.

## Scanner limitations

- Static matching produced clear false positives in test fixtures and example content.
- OSV live checks were unavailable.
- Repository-wide scores overstate the risk of a small Markdown-only component.
- A low score can miss logic, permission, necessity, or operational conflicts.
- A scanner cannot decide whether a capability belongs in BridgeWorks.

> A security scan can identify known suspicious patterns, but it does not prove that a skill is safe, necessary, correct, or appropriate.
