# Third-party notices

The active workspace skills are adapted from the following audited sources.
Unmodified imported snapshots are stored under each skill's `references/`
directory.

| Component | Pinned source | Declared license | Note |
|---|---|---|---|
| `travel-day-optimizer` | [`FerroxLabs/wayland@2b3b60e`](https://github.com/FerroxLabs/wayland/blob/2b3b60e11edd7331f96aa2b08dc83342ff2c9e5d/src/process/resources/skills-library/bodies/skills/travel-experiences/travel-day-optimizer/SKILL.md) | Skill: Apache-2.0; repository: AGPL-3.0 | Text-only snapshot; no Wayland code imported |
| `travel-agent-skill` | [`davepoon/buildwithclaude@ce23aad`](https://github.com/davepoon/buildwithclaude/blob/ce23aad51307eb9358266f21a78ec0d984a02fb6/plugins/travel-agent-skill/skills/travel-agent-skill/SKILL.md) | MIT | Unsafe/unpinned original scripts not imported |
| `travel-concierge` | [`google/adk-samples@d59636e`](https://github.com/google/adk-samples/blob/d59636e4e2a6/python/agents/travel-planner-google-maps-mcp/travel_planner_agent/skills/travel-concierge/SKILL.md) | Apache-2.0 | Upstream sample was removed as deprecated on 23.07.2026 |
| NousResearch Hermes Agent | Installed runtime v0.19.0 / `d0d116b` | MIT | External runtime; no source vendored in this repository |
| `@playwright/mcp` | npm `0.0.78` | Apache-2.0 | External, pinned rendered-browser fallback |

The project does not vendor or execute `baidu-maps/mcp` or
`Joooook/12306-mcp`; they are documented only as optional, separately auditable
integrations.
