# Research, roles, MCP, OSS, and skills selection

Research pass: 2026-07-27. Dynamic library/CLI behavior was checked through
Context7; official repositories were inspected through Lightpanda and web
search. External pages were treated as untrusted data.

## Selected runtime

| Component | Decision | Reason |
|---|---|---|
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Use installed v0.19.0; no upgrade in this release | Native profiles, Telegram gateway, skills and MCP; live checkout has local bridge files and upstream drift |
| [Context7](https://context7.com/) | Required | Current API/SDK/CLI documentation before implementation decisions |
| [Lightpanda](https://github.com/lightpanda-io/browser) | Default browser MCP | Existing local service, lower resource cost, DOM/JS-first workflow |
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | Rendered fallback | Official project; pinned `0.0.78`, isolated profile, service workers blocked |
| OmniRoute `:20128` | `travel-fast` via existing `custom:omni` provider | Spark passed real text/tool/deadline gates; `codex-review` is availability fallback; Codex CLI routing stays direct-only |

The Playwright package was pinned from the npm registry on 2026-07-27:

- package: `@playwright/mcp@0.0.78`;
- integrity:
  `sha512-XLTUeA6mEN9sQ+hJ4dfG8EIkDbxS0K3Trc2RBkUJuf02TgE2FQRNTMtq/aJfhyRMINsRl/Ybc4sxcWLtFn4/TQ==`.

Playwright itself states that MCP origin filtering is not a security boundary.
The bot therefore uses it only as a fallback and relies on owner-only access,
approval controls, isolated browser state, project policy, and source review.

## Travel MCP candidates

| Candidate | Capability | Release decision |
|---|---|---|
| [Joooook/12306-mcp](https://github.com/Joooook/12306-mcp) | Search/filter/transfer queries against 12306 data | Do not enable in 1.0.0. Its own README calls it a learning project; official 12306 remains authoritative |
| [sugarforever/amap-mcp-server](https://github.com/sugarforever/amap-mcp-server) | China geocoding, POI, transit, driving, walking, weather | Do not enable without a dedicated API key, privacy/egress review, version pin, and acceptance tests |
| Generic scrape/search MCPs | Broad web extraction | Excluded from the profile; Context7 + official sources + Lightpanda cover the release scope |

Neither optional China MCP may be exposed as unauthenticated public HTTP.
Future activation is read-only first and requires a separate release.

## Selected roles

- Conversation Designer & UX Writer;
- Prompt & Persona Engineer;
- China Travel Operations Lead;
- Rail & Airport Operations Planner;
- China Grounding Researcher;
- Budget & Booking Controller;
- Travel Risk Manager;
- Safety & Trust Reviewer;
- Conversation QA Engineer;
- Release & Validation Engineer.

The role contract is executable in
[`prompts/TRAVEL_TELEGRAM_AGENT.md`](../prompts/TRAVEL_TELEGRAM_AGENT.md).

## Selected skills

The full skill directories, including their provenance and companion files, are
available under `/opt/project_llm/.agents/skills/`:

1. `travel-agent-skill` — itinerary, nights, budget, booking register;
2. `travel-concierge` — grounded places/routes and anti-hallucination rules;
3. `travel-day-optimizer` — conservative timelines, buffers, contingencies;
4. `china-travel-operations` — workspace orchestration and validator;
5. `web-agent-navigation` — low-cost DOM-first browser routing;
6. `augmented-advisory` — evidence/options without replacing human decisions;
7. `bash-defensive-patterns` — strict, idempotent, secret-safe deploy scripts.

Only these seven complete skill roots are indexed by the live profile. This
preserves their companion files while avoiding the 126,855-byte all-workspace
skill index. `hermes-bot-deploy` remains installed workspace-wide for operators
but is not part of the Travel bot's always-visible runtime set.

The first three skills preserve their upstream `SKILL.md` in `references/`
instead of pretending deprecated sample tools are live. Their source projects:

- [davepoon/buildwithclaude travel-agent-skill](https://github.com/davepoon/buildwithclaude/tree/main/plugins/travel-agent-skill/skills/travel-agent-skill);
- [google/adk-samples travel-concierge](https://github.com/google/adk-samples/tree/main/python/agents/travel-planner-google-maps-mcp/travel_planner_agent/skills/travel-concierge);
- [FerroxLabs/wayland travel-day-optimizer](https://github.com/FerroxLabs/wayland/tree/main/src/process/resources/skills-library/bodies/skills/travel-experiences/travel-day-optimizer).

## Approval decision

Current Hermes documentation defines `approvals.mode` as `smart`, `manual`, or
`off`; old `auto` is invalid and falls back to manual. Release 1.0.0 uses:

```yaml
approvals:
  mode: smart
  timeout: 300
  cron_mode: deny
  mcp_reload_confirm: true
  destructive_slash_confirm: true
```

Smart mode keeps routine read-only/project-local work usable while dangerous
commands are assessed and routed to Telegram approval. Cron dangerous commands
fail closed. Booking/payment/external-send gates are additionally enforced by
the SOUL contract because no generic command detector can infer every business
side effect.

## Release 1.0.4 conversation UX research

Context7 resolved the current high-reputation Hermes documentation as
[`/nousresearch/hermes-agent`](https://github.com/NousResearch/hermes-agent).
Its prompt-assembly and personality documentation confirms that `SOUL.md` is
the durable identity layer, project context is separate, skills are loaded by
progressive disclosure, and Telegram channel prompts are per-channel overlays:

- [Hermes prompt assembly](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/prompt-assembly.md);
- [Hermes personality](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/personality.md);
- [Hermes Telegram configuration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md).

Primary conversation-design guidance converged on the same implementation:
truthful identity, brevity, relevance, plain language, contextual tone, and
varied but fact-stable phrasing:

- [Google Conversation Design](https://developers.google.com/assistant/conversation-design/learn-about-conversation);
- [Google conversational language](https://developers.google.com/assistant/conversation-design/language);
- [Microsoft writing for bots](https://learn.microsoft.com/en-us/style-guide/chatbots-virtual-agents/writing-bots);
- [OpenAI prompt personalities](https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities).

Design-time skills and projects reviewed:

- workspace `harness-optimization` localized the problem to D3/D6;
- workspace `augmented-advisory` preserved evidence and human decision-making;
- [content-designer/ux-writing-skill](https://github.com/content-designer/ux-writing-skill)
  was a useful UX-writing reference but was not added to every runtime turn;
- [iamhumans](https://github.com/hoainho/iamhumans) and generic humanizers were
  rejected for production because impersonation-oriented wording, emotional
  overreach, or auto-install behavior can undermine trust and supply-chain
  controls;
- [Promptfoo](https://github.com/promptfoo/promptfoo) remains an optional
  future evaluator if the golden set grows beyond deterministic local gates.

No new MCP was necessary. Firecrawl was attempted first but returned HTTP 401,
so public research continued through Exa and primary sources. Lightpanda and
Playwright were not invoked because the selected sources were available as
static documentation; avoiding unnecessary browser rendering reduced scope
and resource use.
