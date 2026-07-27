# Travel v1.0.4

Conversation UX release for `@travel_samurai_bot`.

## Outcome

The bot now answers like a calm, attentive travel partner in a private
Telegram conversation instead of emitting an audit report by default.

The change is behavioral, not a model swap:

- model remains OmniRoute `travel-fast`;
- served primary remains `codex/gpt-5.3-codex-spark`;
- strict `codex-review` remains availability fallback;
- owner-only Telegram, seven-skill allowlist, MCP allowlist, credentials,
  project scope, and approval policy are unchanged.

The assistant is intentionally conversational but never pretends to be human.
Warmth cannot change facts, confidence, privacy boundaries, or confirmation
requirements.

## Root cause and fix

The previous SOUL contained an unconditional instruction to start with a
`verdict` and next action. On a three-record JSON read this produced:

- canned «Сразу по факту» openings;
- `deadline/date/booking/status` field dumps;
- the same information repeated in separate status sections;
- automatic completion emoji and internal method narration.

Harness diagnosis: D3/D6. The route was accurate and fast enough; the
generation/output contract was wrong.

Release 1.0.4:

- defines a compact durable persona in `SOUL.md`;
- uses ordinary Russian prose for simple questions;
- allows compact status groups only when the owner asks for separation;
- hides internal roles, tools, JSON schema, sorting, and reasoning;
- uses first person only for work actually performed;
- keeps serious exact formatting for approval-gated actions;
- adds a short per-owner Telegram reinforcement without duplicating the SOUL.

## Roles and executed prompt

The release used these lenses:

- Conversation Designer & UX Writer;
- Prompt & Persona Engineer;
- Travel Operations Lead;
- Safety & Trust Reviewer;
- Conversation QA Engineer;
- Release & Observability Engineer.

The reusable and executed workflow is
[`prompts/TRAVEL_CONVERSATION_DESIGN_RELEASE.md`](prompts/TRAVEL_CONVERSATION_DESIGN_RELEASE.md).

## Research and skill decision

Context7 was mandatory and confirmed the Hermes split:

- stable persona in `SOUL.md`;
- project rules in project context;
- per-chat policy in `telegram.channel_prompts`;
- skills loaded through progressive disclosure.

Google, Microsoft, and OpenAI guidance supported concise, relevant, contextual,
truthful conversation. External UX-writing and humanizer skills were reviewed.
None was installed into the live profile: a new always-on skill would increase
prompt weight, and impersonation/auto-install patterns conflict with
transparent AI identity and `allow_lazy_installs: false`.

Firecrawl returned HTTP 401. Research continued through Exa and primary
sources. Lightpanda/Playwright were unnecessary because all selected evidence
was available as static documentation.

Full source matrix:
[`docs/RESEARCH_AND_SELECTION.md`](docs/RESEARCH_AND_SELECTION.md).

## Verification

- 20 unit tests passed;
- itinerary validator passed: 18 days, 16 China nights, 5 immutable flights;
- deterministic evaluator rejects the old robotic field dump, swapped
  date/status associations, contradictions, repetition, and human-identity
  claims;
- generated deadline reply passed semantic and conversational style gates;
- greeting smoke: 15.0 seconds wall-clock;
- Badaling short-advice smoke: 26.5 seconds wall-clock;
- successful golden-set calls: HTTP 200, `gpt-5.3-codex-spark`, no fallback;
- SOUL: 12,941 bytes / 7,818 characters;
- full runtime verifier passed;
- Telegram gateway active; no polling conflict;
- trading, terra, and ipregion gateways remained active;
- repository secret scan passed.

Representative accepted deadline answer:

> Сверил по `data/china-2026.json` — ближайшие три дедлайна такие:
> `Confirmed`: 31 июля — Shanghai и Chongqing.
> `Book`: 20 августа — официальный билет 12306.
> Ничего не бронировал, только посмотрел сроки по данным файла.

Exact wording may vary; dates, records, statuses, source, and no-booking fact
must not.

## Rollback

The installer created timestamped runtime config backups before every render.
To roll back only the voice:

1. restore the previous `SOUL.md` from Git tag `v1.0.3`;
2. restore the latest pre-1.0.4 `config.yaml.bak-*` only if the overlay must
   also be reverted;
3. restart only `hermes-gateway-travel.service`;
4. run `scripts/verify_travel_bot.sh`.

Do not alter the Telegram token or OmniRoute combo for this rollback.
