# Public-source research pilot readiness

## The Next New Thing AI

The existing `youtube-intelligence` workflow remains the single YouTube system. Channel ID `UCNZEktrsM5oJZ-MK4jKPMOQ` was added to `youtube-watchlist.json` with a no-auto-install label.

The source skill now records video title, publication date, named tool or repository, verified repository URL, claimed benefit, actual BridgeWorks use case, overlap, security, permissions, maintenance health, recommendation, and pilot status.

Any mentioned repository must enter quarantine at an exact commit. A video claim is not security evidence or a capability decision.

## Agent Reach

Pinned commit: `b4d52c46c9113cb0f653d6df4cf71ebadf4930ac`.

Readiness: not ready to install. Ready only for a future adapted public-source procedure.

Allowed future sources:

- Public YouTube pages and captions.
- Public GitHub repositories, issues, and releases.
- Public Reddit pages where ordinary logged-out access works.
- RSS and Atom feeds.
- Public webpages.

Prohibited:

- Browser cookies or cookie databases.
- LinkedIn, X, Google, Meta, or other authenticated sessions.
- Primary-account access.
- Proxy or anti-bot circumvention.
- Package auto-install, remote bootstrap, or system-tool installation.
- Persistent secrets in the repository.

Repository behaviour to isolate:

- Network requests to public and optional authenticated platforms.
- Subprocess calls to upstream tools.
- Optional Playwright and browser-cookie packages.
- Configuration and tokens under `~/.agent-reach/`.
- Upstream tools under `~/.agent-reach/tools/`.

Pilot success criterion: one public-source query returns traceable URLs and dates from YouTube, GitHub, RSS, and a public webpage, with zero cookie access, zero credential reads, zero writes outside an isolated pilot directory, and no installed upstream tools.

## Last30Days

Pinned commit: `a4e7eca51637123f92086d50b2525eecdf24abbe`.

Readiness: not ready to install. Reference-only procedure review is ready.

Important behaviour:

- Public Reddit, Hacker News, Polymarket, GitHub, YouTube, and web modes exist.
- Optional configuration supports many API keys and browser-cookie paths.
- State may be written as Markdown, JSON, HTML, SQLite, queues, configuration, and library files.
- Default saved research may go to `~/Documents/Last30Days` unless redirected.
- Publishing code exists behind explicit flags.

Any pilot must set an isolated save directory, disable browser cookies, disable publishing, avoid setup wizards, and use public sources only.

### Bounded use case 1: BridgeWorks AI Visibility Radar

Question: Which public changes in AI search, answer engines, schema, citation behaviour, and major platform documentation have operational impact?

Output fields:

- New evidence.
- Publication date.
- Event date.
- Source quality.
- Operational implication.
- Required action.
- Previously assessed finding.
- Uncertainty.

Success: at least five dated primary or high-quality sources, no repeated stale finding presented as new, and one concrete action or an explicit no-action decision.

### Bounded use case 2: Prospect Trigger Radar

Question: Which public business events indicate a likely website, visibility, workflow, or growth-system need?

Use only public company websites, public job posts, public press releases, and public news. Do not contact anyone.

Success: three traceable triggers with separate publication and event dates, a source-quality score, a specific BridgeWorks hypothesis, and no invented contact or intent.

### Bounded use case 3: GitHub Efficiency Scout

Question: Which recently maintained repositories could remove a measured BridgeWorks bottleneck?

Success: three pinned repositories with licence, recent maintenance evidence, permission surface, internal overlap, security review status, and one recommended quarantine candidate at most.

## Recommendation

Use the existing YouTube, web, GitHub, NotebookLM, and file-based research stack for the first pilots. Borrow the date, source-quality, deduplication, and prior-finding schema from Last30Days. Do not install Agent Reach or Last30Days until a public-only isolated pilot proves a capability gap.
