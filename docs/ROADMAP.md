# Travel Agents delivery roadmap

## Releases 1.0.0–1.0.1 — dedicated owner bot and resource gate

- [x] Read workspace and project canon; preserve immutable tickets.
- [x] Audit live Hermes profiles, gateways, service pattern, and OmniRoute.
- [x] Query current Hermes documentation through Context7.
- [x] Research official Hermes, browser MCP, China rail/map MCP, and skills.
- [x] Define roles, Travel SOUL, tool order, trust boundaries, and approvals.
- [x] Build idempotent profile renderer, installer, unit, verifier, and rollback.
- [x] Add minimal MCP policy and owner-only Telegram allowlist.
- [x] Add tests, secret scan, itinerary validator, and monitoring hooks.
- [x] Stage the dedicated profile and disabled/inactive user unit.
- [x] Add bounded `/home` cache cleanup and persistent `/opt` swap reserve.
- [x] Rotate the token disclosed in chat and provision it by hidden TTY input.
- [x] Restore the host resource gate: at least 8 GiB MemAvailable, 2 GiB free
      swap, and 4 GiB free under `/home`.
- [x] Complete owner `/start` and real-question use after rotation.

## Release 1.0.2 — latency and semantic quality

- [x] Measure the actual model served by `hermes` and production call latency.
- [x] Benchmark `quick`, `free`, Haiku, GitHub, Gemini, DeepSeek, Hermes,
      Codex Spark, and `codex-review` paths.
- [x] Reject fast candidates that fail the real duplicate-deadline test.
- [x] Create `travel-fast` through Dashboard session + CSRF REST only.
- [x] Keep `codex-review` strict Codex-only and use it only as fallback.
- [x] Reduce the skill index to seven complete Travel-relevant roots.
- [x] Pin runtime config, provider default, and `HERMES_MODEL` consistently.
- [x] Restart only the Travel gateway and pass the full verifier.
- [ ] Owner confirms post-release Telegram wall-clock latency from a fresh DM.

## Release 1.0.3 — durable restart headroom

- [x] Measure repeated swap exhaustion after the model rollout.
- [x] Preserve the existing RAM/swap/disk gate without a force bypass.
- [x] Add an 8 GiB low-priority emergency swap device on `/opt`.
- [x] Add a conservative 12 GiB RAM fallback when cold pages fill all swap.
- [x] Keep the model, combo, credentials, and neighboring gateways unchanged.
- [x] Confirm the adaptive gate after a 90-second settling interval.

## Release 1.0.4 — human conversation UX

- [x] Diagnose the robotic answer as harness D3/D6, not a model-routing issue.
- [x] Verify Hermes SOUL, channel-prompt, skills, and Telegram behavior through
      Context7 before editing.
- [x] Research primary conversation-design guidance and open-source skills;
      reject unsafe impersonation and auto-install patterns.
- [x] Add Conversation Designer, Prompt/Persona, Safety/Trust, Conversation QA,
      and Release/Observability roles to an executable release prompt.
- [x] Replace unconditional report formatting with a compact contextual voice.
- [x] Preserve transparent AI identity and every booking/payment/data approval.
- [x] Add semantic/style regression gates for the real duplicate-deadline case.
- [x] Deploy through the backup-producing installer and restart only Travel.
- [x] Pass 20 unit tests, itinerary validation, full runtime verifier, and live
      deadline/greeting/Badaling golden prompts.
- [x] Confirm successful calls use `travel-fast` → Codex Spark without fallback.

For reprovisioning after a future token rotation:

```bash
/opt/project_llm/projects/Travel/scripts/preflight_travel_bot.sh
/opt/project_llm/projects/Travel/scripts/provision_travel_bot.sh
```

It validates Telegram `getMe`, checks the expected username, starts the unit,
and executes the live verification suite.

## Release 1.1 — booking-window operations

- Re-verify hotel inventory and China rail sales windows from official sources.
- Add scheduled owner reminders for booking deadlines without auto-purchase.
- Evaluate read-only 12306 MCP in an isolated profile and pin an audited commit.
- Add source freshness metadata and stale-fact warnings.

## Release 1.2 — travel-day mode

- Mobile-friendly daily brief, local timezone, weather horizon, and abort rules.
- Read-only document wallet index; keep passport/payment data outside Git.
- Optional China map provider after API-key, privacy, license, and cost review.
- Containerized write boundary if the bot is ever opened beyond the owner.
