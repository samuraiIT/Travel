# Travel Agents 1.0.0

Released: 2026-07-27.

This release turns the Travel repository into an owner-operated Hermes Agent
workspace for `@travel_samurai_bot`.

Highlights:

- dedicated `travel-bot` profile and systemd gateway;
- grounded China 2026 operations canon and immutable-ticket validator;
- Context7-first documentation workflow with Lightpanda/Playwright browsing;
- owner-only access and explicit approval gates for external side effects;
- reproducible deploy, secret provisioning, monitoring, verification, rollback;
- no Telegram token or provider credential in Git.

Activation safety note: any token pasted into a chat must be revoked. The
release intentionally stages the unit disabled and stopped until a newly
rotated token is entered through the interactive provisioning script and the
host resource preflight is green.
