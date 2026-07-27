# Hermes profile configuration

`travel-bot.overlay.yaml` contains only non-secret project policy. The renderer
selectively imports the live `omni` custom provider and the approved MCP
definitions from an existing local Hermes profile. It never prints their
credentials and never copies another Telegram token.

Approved MCP set for release 1.0.2:

- `context7` — required for library/API/SDK/CLI documentation;
- `lightpanda` — low-cost DOM/JavaScript browser at the local MCP service;
- `playwright` — rendered-page fallback.

The profile intentionally excludes unrelated GitLab, PostgreSQL, trading,
Qdrant, media, and unaudited China ticket/map MCPs. Native Hermes file and
terminal tools are rooted at `/opt/project_llm/projects/Travel`; the SOUL and
systemd policy forbid work outside that scope.

The default model is the OmniRoute `travel-fast` combo. The profile indexes
only seven external Travel/operations skill roots rather than both complete
workspace registries. Each root still exposes its complete `SKILL.md`,
scripts, references, templates, and assets through progressive disclosure.

Secrets live only in
`~/.hermes/profiles/travel-bot/.env` and the generated runtime config, both
mode `0600`. They are not release artifacts.
