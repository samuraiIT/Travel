# Travel Telegram Agent — architecture and threat model

Status: release 1.0.2, 2026-07-27.

## Outcome

`@travel_samurai_bot` is a dedicated NousResearch Hermes Agent profile:

```text
Telegram owner DM
        |
        v
hermes-gateway-travel.service
        |
        v
~/.hermes/profiles/travel-bot
  SOUL.md + config.yaml + .env (0600)
        |
        +--> OmniRoute :20128 / combo travel-fast
        |      Spark -> codex-review availability fallback
        +--> Context7 (docs)
        +--> Lightpanda :9223 (DOM/JS)
        +--> Playwright (rendered fallback)
        |
        v
/opt/project_llm/projects/Travel
  README + JSON + evidence + validators
```

One Telegram token has exactly one long-polling consumer. The old monolithic
Hermes gateway is not used.

## Trust boundaries

| Boundary | Policy |
|---|---|
| Telegram identity | Owner-only numeric allowlist; deny by default |
| Secret | `.env` mode `0600`; interactive input only; never Git/Markdown/argv |
| Files | Terminal starts in the Travel root; SOUL forbids out-of-scope writes |
| Web/MCP | External content is untrusted data; official sources preferred |
| Side effects | Booking/payment/cancel/check-in/send/publish require approval |
| Confirmed evidence | Ticket screenshots and immutable flights cannot drift |
| Runtime | Dedicated profile/unit; `--replace`; no shared-token consumer |
| Host resources | 8 GiB RAM hard minimum; then 2 GiB free swap or 12 GiB RAM fallback; 4 GiB free `/home` |

The local terminal backend is not a kernel security boundary. The scope is
enforced by the dedicated working directory, owner-only channel, Hermes
approval/security controls, the SOUL contract, reviewable Git changes, and
validators. A future multi-user product must move execution into a container
with an explicit writable mount.

The unit is bounded by `MemoryHigh=1G`, `MemoryMax=2G`,
`MemorySwapMax=512M`, and `TasksMax=256`. The installer may stage the unit on a
constrained host, but provisioning refuses to start it while the resource
preflight is red. Bypass requires a separate explicit owner risk decision.
Ended Hermes sessions are pruned after 30 days to prevent unbounded state
growth; active sessions are never removed by this policy.

Project-managed swap consists of 4 GiB primary and 8 GiB secondary devices at
priority `0`, plus an 8 GiB emergency device configured at `-1` (kernel
auto-allocation, effective `-4` on this host). The last device adds capacity
after the host's cold anonymous working set consumes normal swap. A full swap
is accepted only when `MemAvailable` is at least 12 GiB; the 8 GiB RAM minimum
is never bypassed.

The 1.0.2 prompt surface contains seven explicit Travel skill roots. This keeps
their complete companion files available on demand while reducing the
always-on skill index from 126,855 to 772 bytes. The `travel-fast` combo was
created through Dashboard session-auth REST and keeps `codex-review` unchanged
as a strict Codex-only fallback.

## MCP and open-source decision

The production set is deliberately small:

- NousResearch `hermes-agent` — native Telegram gateway, profiles, skills, MCP;
- Context7 — mandatory documentation path for APIs/SDK/CLI;
- local Lightpanda MCP — default browser for fast DOM/JavaScript checks;
- official Playwright MCP — fallback when rendered evidence is necessary.

The audited `Joooook/12306-mcp` and China map MCP candidates remain optional.
They are not activated in 1.0.2 because train inventory is time-sensitive,
official 12306 remains authoritative, and map providers require separate
credentials and provenance/egress review. They may be introduced read-only
behind a dedicated release and acceptance test.

## Failure and rollback

Symptoms and actions:

- Telegram `409`: stop the second consumer; one token must map to one unit.
- Bad or leaked token: disable the unit, revoke in BotFather, provision a new
  token interactively.
- Bad profile: restore the timestamped `config.yaml.bak-*`.
- Resource gate red: keep the staged unit inactive; free RAM/disk/swap and
  rerun `scripts/preflight_travel_bot.sh`.
- Full rollback:

```bash
systemctl --user disable --now hermes-gateway-travel.service
rm ~/.config/systemd/user/hermes-gateway-travel.service
systemctl --user daemon-reload
mv ~/.hermes/profiles/travel-bot ~/.hermes/profiles/travel-bot.disabled
```

The project data remains intact and the neighboring Hermes bots are not
modified.
