# Travel bot operations handoff

Date: 2026-07-27. Release: 1.0.0.

## Current live state

- Project: `/opt/project_llm/projects/Travel`, branch `master`.
- Hermes profile: `/home/samurai/.hermes/profiles/travel-bot`.
- Unit: `hermes-gateway-travel.service`.
- Unit state: installed, disabled, inactive.
- Telegram token in Travel profile: absent by design.
- Profile permissions: directory `0700`; config, SOUL and `.env` `0600`.
- Model smoke: `TRAVEL_MODEL_OK` through `custom:omni`.
- MCP allowlist: `context7`, `lightpanda`, `playwright`.
- Approval policy: `smart`, 300 seconds, cron dangerous commands denied.
- Neighboring trading, terra and ipregion gateways remained active.

The unit was briefly started once without a Telegram credential during staged
verification. It reported “No messaging platforms enabled”, made no Telegram
polling request, and was stopped. The installer was then hardened to keep a
secretless unit disabled and stopped.

## Why Telegram is not active

The credential supplied in chat is compromised by disclosure and must not be
reused. A second independent gate is also red:

- `MemAvailable` below the required 8 GiB;
- `SwapFree` below the required 2 GiB;
- free space under `/home` below the required 4 GiB.

Starting another always-on Hermes gateway in this state risks host pressure.
The unit has cgroup limits, but production activation still requires the
preflight to pass.

## Activation

1. Revoke/regenerate the bot token in BotFather.
2. Restore enough RAM, swap and `/home` headroom.
3. Run from an interactive terminal:

```bash
cd /opt/project_llm/projects/Travel
./scripts/preflight_travel_bot.sh
./scripts/provision_travel_bot.sh
```

Provisioning:

- reads the rotated token without echo or argv exposure;
- validates token format;
- calls Telegram `getMe` and requires username `travel_samurai_bot`;
- writes `.env` atomically with mode `0600`;
- enables/starts only the dedicated Travel unit;
- executes the full verifier.

4. From the owner Telegram account, send:

```text
/start
Покажи ближайшие три дедлайна бронирования по data/china-2026.json,
отдели Confirmed от Book и ничего не бронируй.
```

5. Confirm that the answer cites project facts, changes nothing, and that a
dangerous command produces an inline approval prompt.

## Verification evidence

Green:

- itinerary validator: 18 days, 16 China nights, 5 immutable flights;
- 5 profile/unit/prompt unit tests;
- model inference smoke;
- Hermes config v33 and doctor: no active security advisories;
- MCP security: no suspicious stdio commands;
- Bandit/Semgrep/Gitleaks security scans after the one low test-only assert was
  removed;
- systemd unit syntax and central monitoring YAML parse;
- no Telegram-token-shaped value in the project.
- ticket screenshot containing a booking reference is local-only and ignored.

Known upstream/runtime warnings not changed in this release:

- embedded SQLite 3.50.4 WAL-reset advisory; Hermes automatically uses
  `journal_mode=DELETE`;
- build-time npm advisories in the shared Hermes web/TUI workspaces;
- upstream Hermes is far ahead and the live checkout contains untracked bridge
  code, so an upgrade requires a separate backup/staged rollout.

## Rollback

```bash
systemctl --user disable --now hermes-gateway-travel.service
mv ~/.config/systemd/user/hermes-gateway-travel.service \
   ~/.config/systemd/user/hermes-gateway-travel.service.disabled
systemctl --user daemon-reload
mv ~/.hermes/profiles/travel-bot \
   ~/.hermes/profiles/travel-bot.disabled
```

To roll back project code, use the release tag/previous commit. Do not delete
the profile until its `.env` and state retention requirements have been
reviewed.
