# Changelog

All notable changes to this project are documented here.

## [1.0.4] - 2026-07-27

### Added

- Human-centered Telegram voice contract in the Travel SOUL with transparent
  AI identity, context-sensitive warmth, compact formatting, and grounded
  first-person language.
- Executable conversation-design release prompt with selected roles, research
  order, golden prompts, safety constraints, and acceptance gates.
- Deterministic deadline-reply evaluator plus regression fixtures for exact
  date/item/status associations, contradictions, repetition, AI identity,
  robotic field dumps, method narration, and justified compact status grouping.

### Changed

- Replaced the unconditional `verdict`/report response rule with a
  task-proportional conversation contract.
- Simple local fact reads now avoid unnecessary multi-step travel workflows
  and hide internal sorting, JSON fields, roles, and tool narration.
- Telegram owner overlay now reinforces natural concise Russian while
  preserving explicit AI identity and every existing approval gate.

### Security

- No new runtime MCP or third-party humanizer skill was installed. The live
  allowlists, owner boundary, model route, credentials, and external-action
  approvals are unchanged.

## [1.0.3] - 2026-07-27

### Added

- Persistent 8 GiB low-priority emergency swap reserve on `/opt`.

### Fixed

- Made the restart gate pressure-aware after the host's roughly 60 GiB
  anonymous working set consumed all swap despite 20 GiB `MemAvailable`:
  require 2 GiB `SwapFree` or a stricter 12 GiB RAM fallback.

## [1.0.2] - 2026-07-27

### Changed

- Switched the live Travel agent from the overloaded `hermes` lane to the
  dedicated `travel-fast` OmniRoute combo: Codex Spark first and the strict
  Codex-only `codex-review` combo as availability fallback.
- Reduced the always-on Hermes skill index from all workspace skills to seven
  Travel-relevant skill roots while preserving every skill's companion files.
- Added a deterministic `days[].deadline` rule and synchronized the generated
  provider default with `model.default`.
- Expanded the secondary Travel swap reserve from 4 GiB to 8 GiB after the
  host exhausted the original reserve during the rollout.

### Fixed

- The installer now restarts an already-running Travel gateway after a
  configuration change instead of treating `enable --now` as a reload.
- The verifier now fails unless both the runtime config and environment pin
  `travel-fast`.
- A semantically wrong but superficially fast model can no longer pass release
  acceptance: the live smoke must preserve duplicate deadlines and statuses.

## [1.0.1] - 2026-07-27

### Added

- Defensive host-resource remediation helper with dry-run/apply modes.
- Two persistent 4 GiB `/opt` swap units and documented rollback.
- Regenerable npm content-cache cleanup to restore `/home` headroom.
- Root-owned swap directory plus regular-file and swap-signature validation.

## [1.0.0] - 2026-07-27

### Added

- Production-ready Hermes Agent profile design for `@travel_samurai_bot`.
- Owner-only Telegram gateway deployment, secret provisioning, verification,
  systemd lifecycle, rollback, and monitoring integration.
- Travel Agent SOUL prompt with grounded research, booking approval gates,
  immutable-ticket protection, and the project skill pipeline.
- Reproducible profile renderer with a minimal MCP set: Context7,
  Lightpanda, and Playwright fallback.
- Unit tests, release notes, architecture/threat model, and delivery roadmap.
- China 2026 human and machine-readable operations canon with validation.

### Security

- Telegram tokens are intentionally absent from Git and documentation.
- A token disclosed in a chat or log must be revoked before activation.
- External side effects such as booking, payment, cancellation, check-in,
  publication, and sharing personal data require explicit human approval.
