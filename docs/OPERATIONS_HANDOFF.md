# Travel bot operations handoff

Date: 2026-07-27. Release: 1.0.1.

## Current live state

- Project: `/opt/project_llm/projects/Travel`, branch `master`.
- Hermes profile: `/home/samurai/.hermes/profiles/travel-bot`.
- Unit: `hermes-gateway-travel.service`.
- Unit state: installed, disabled, inactive.
- Telegram token in Travel profile: absent by design.
- Resource units: `opt-travel\x2dswap-swap\x2dprimary.img.swap` and
  `opt-travel\x2dswap-swap\x2dreserve.img.swap`, enabled and active.
- Resource preflight: passed after `/home` cache cleanup, 8 GiB `/opt` swap
  provisioning and a final bounded cgroup-v2 reclaim of about 3 GiB.
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
reused. The resource gate is green at the latest verification, but it is a
live safety check and must pass again immediately before token entry. The unit
remains disabled and inactive until a newly rotated credential is supplied
through the hidden interactive prompt.

## Activation

1. Revoke/regenerate the bot token in BotFather.
2. Verify RAM, swap and `/home` headroom. The bounded helper uses dry-run by
   default; with `--apply` it removes only the regenerable npm content cache
   when `/home` is below the gate and adds two persistent 4 GiB swapfiles under
   the root-owned `0700` directory `/opt/travel-swap`:

```bash
cd /opt/project_llm/projects/Travel
./scripts/ensure_travel_resources.sh
./scripts/ensure_travel_resources.sh --apply
```

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
- 6 profile/unit/prompt/resource unit tests;
- live resource preflight after bounded remediation;
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

Resource-helper rollback:

```bash
(
  set -Eeuo pipefail
  travel_swap_unit='opt-travel\x2dswap-swap\x2dprimary.img.swap'
  travel_reserve_unit='opt-travel\x2dswap-swap\x2dreserve.img.swap'
  travel_rollback_stamp="$(date -u +%Y%m%dT%H%M%SZ)"

  sudo systemctl disable --now \
    "${travel_swap_unit}" "${travel_reserve_unit}"
  active_swap_names="$(sudo swapon --show=NAME --noheadings)"
  if grep -Fxq /opt/travel-swap/swap-primary.img <<<"${active_swap_names}" ||
    grep -Fxq /opt/travel-swap/swap-reserve.img <<<"${active_swap_names}"; then
    printf 'ERROR: a Travel swapfile is still active; rollback stopped.\n' >&2
    exit 1
  fi

  sudo mv "/etc/systemd/system/${travel_swap_unit}" \
    "/etc/systemd/system/${travel_swap_unit}.${travel_rollback_stamp}.disabled"
  sudo mv "/etc/systemd/system/${travel_reserve_unit}" \
    "/etc/systemd/system/${travel_reserve_unit}.${travel_rollback_stamp}.disabled"
  sudo mv /opt/travel-swap \
    "/opt/travel-swap.${travel_rollback_stamp}.disabled"
  sudo systemctl daemon-reload
)
```

The npm content cache is intentionally not restored; npm recreates it on
demand. The bounded cgroup reclaim has no persistent setting to roll back;
pages return to RAM naturally when referenced.
