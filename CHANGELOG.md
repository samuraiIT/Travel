# Changelog

All notable changes to this project are documented here.

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
