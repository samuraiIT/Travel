# Travel bot operations handoff

Date: 2026-07-27. Release: 1.0.4.

## Current live state

- Project: `/opt/project_llm/projects/Travel`, branch `master`.
- Hermes profile: `/home/samurai/.hermes/profiles/travel-bot`.
- Unit: `hermes-gateway-travel.service`.
- Unit state: enabled, active, dedicated long-polling consumer.
- Telegram token: provisioned outside Git in profile `.env` mode `0600`;
  value is never printed or documented.
- Default model: `travel-fast` through `custom:omni`.
- Combo: `codex/gpt-5.3-codex-spark` first, strict `codex-review` fallback.
- Resource units: `opt-travel\x2dswap-swap\x2dprimary.img.swap`,
  `opt-travel\x2dswap-swap\x2dreserve.img.swap`, and
  `opt-travel\x2dswap-swap\x2demergency.img.swap`, enabled and active at
  4 GiB, 8 GiB, and 8 GiB respectively. Emergency unit priority is `-1`;
  the kernel assigned effective priority `-4` on this host.
- Resource preflight: passed without bypass after bounded cgroup-v2 reclaim;
  the secondary reserve was expanded when the host exhausted the original
  4 GiB reserve. Hard minimum is 8 GiB RAM; the swap condition is 2 GiB free
  swap or a stricter 12 GiB available-RAM fallback.
- Profile permissions: directory `0700`; config, SOUL and `.env` `0600`.
- SOUL: 12,941 bytes / 7,818 characters; skill index remains 772 bytes.
- Conversation contract: natural concise Russian, transparent AI identity,
  contextual structure, no internal method narration or duplicated summaries.
- Model smokes: grounded deadline answer passed the semantic/style evaluator;
  greeting and Badaling recommendation were concise and conversational.
- MCP allowlist: `context7`, `lightpanda`, `playwright`.
- External skill allowlist: seven complete Travel/operations skill roots.
- Approval policy: `smart`, 300 seconds, cron dangerous commands denied.
- Neighboring trading, terra and ipregion gateways remained active.

`travel-fast` was created through the authenticated Dashboard + CSRF REST path.
No direct OmniRoute SQLite write was used. Receiver model pickers/configs were
synchronized without globally restarting Hermes; only the Travel gateway was
restarted for the live switch.

Release 1.0.4 did not mutate OmniRoute. It used the existing combo and restarted
only `hermes-gateway-travel.service` through the backup-producing installer.
All observed successful golden-set calls were HTTP 200 and served
`gpt-5.3-codex-spark`; `codex-review` was not needed.

## Model decision

The old `hermes` combo served `codex/gpt-5.5`; 11 observed production calls
took about 184 seconds, with a 10.4-second median and a 60-second maximum.
`quick` was fast in synthetic probes but returned wrong project deadlines.
Free/cheap alternatives were rejected for semantic error, quota exhaustion,
missing credentials, or long tails. `travel-fast` passed direct text, native
tool-use, a duplicate-deadline accuracy gate, and the full profile smoke.

Full evidence: [`../RELEASE_NOTES_v1.0.2.md`](../RELEASE_NOTES_v1.0.2.md).

## Operations and future token rotation

1. Verify RAM, swap and `/home` headroom. The bounded helper uses dry-run by
   default; with `--apply` it removes only the regenerable npm content cache
   when `/home` is below the gate and maintains 4 GiB primary, 8 GiB
   secondary, and 8 GiB low-priority emergency swapfiles under the root-owned
   `0700` directory `/opt/travel-swap`:

```bash
cd /opt/project_llm/projects/Travel
./scripts/ensure_travel_resources.sh
./scripts/ensure_travel_resources.sh --apply
```

2. Normal config/SOUL/model update with the existing credential:

```bash
cd /opt/project_llm/projects/Travel
./scripts/preflight_travel_bot.sh
./scripts/install_travel_bot.sh --start
./scripts/verify_travel_bot.sh
```

3. For a future token rotation, regenerate it in BotFather and run from an
   interactive terminal:

```bash
cd /opt/project_llm/projects/Travel
./scripts/provision_travel_bot.sh
```

Provisioning:

- reads the rotated token without echo or argv exposure;
- validates token format;
- calls Telegram `getMe` and requires username `travel_samurai_bot`;
- writes `.env` atomically with mode `0600`;
- enables/starts only the dedicated Travel unit;
- executes the full verifier.

4. Post-release owner smoke:

```text
/start
Покажи ближайшие три дедлайна бронирования по data/china-2026.json,
отдели Confirmed от Book и ничего не бронируй.
```

5. Confirm that the answer includes both 31 July hotel rows followed by the
20 August `Book` item, changes nothing, and sounds like a short Telegram reply:
no JSON field dump, sorting narration, duplicated status recap, or automatic
`✅`. A dangerous command must still produce an inline approval prompt.

## Verification evidence

Green:

- itinerary validator: 18 days, 16 China nights, 5 immutable flights;
- 20 profile/unit/prompt/resource/model/conversation unit tests;
- live resource preflight after bounded remediation;
- direct `travel-fast` text/native-tool/deadline gates;
- live deadline response passed `scripts/evaluate_travel_reply.py`;
- greeting smoke: 15.0 seconds wall-clock;
- Badaling short-advice smoke: 26.5 seconds wall-clock;
- all successful golden calls served Codex Spark with HTTP 200 and no fallback;
- SOUL: 12,941 bytes / 7,818 characters, below the Hermes character cap;
- prompt remains far below the pre-1.0.2 145,226-byte baseline;
- Hermes config v33 and doctor: no active security advisories;
- MCP security: no suspicious stdio commands;
- Bandit/Semgrep/Gitleaks security scans after the one low test-only assert was
  removed;
- systemd unit syntax and central monitoring YAML parse;
- no Telegram-token-shaped value in the project;
- active owner-only Telegram gateway with no recent `401`, `409`, traceback,
  or polling conflict;
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
  travel_emergency_unit='opt-travel\x2dswap-swap\x2demergency.img.swap'
  travel_rollback_stamp="$(date -u +%Y%m%dT%H%M%SZ)"

  sudo systemctl disable --now \
    "${travel_swap_unit}" "${travel_reserve_unit}" "${travel_emergency_unit}"
  active_swap_names="$(sudo swapon --show=NAME --noheadings)"
  if grep -Fxq /opt/travel-swap/swap-primary.img <<<"${active_swap_names}" ||
    grep -Fxq /opt/travel-swap/swap-reserve.img <<<"${active_swap_names}" ||
    grep -Fxq /opt/travel-swap/swap-emergency.img <<<"${active_swap_names}"; then
    printf 'ERROR: a Travel swapfile is still active; rollback stopped.\n' >&2
    exit 1
  fi

  sudo mv "/etc/systemd/system/${travel_swap_unit}" \
    "/etc/systemd/system/${travel_swap_unit}.${travel_rollback_stamp}.disabled"
  sudo mv "/etc/systemd/system/${travel_reserve_unit}" \
    "/etc/systemd/system/${travel_reserve_unit}.${travel_rollback_stamp}.disabled"
  sudo mv "/etc/systemd/system/${travel_emergency_unit}" \
    "/etc/systemd/system/${travel_emergency_unit}.${travel_rollback_stamp}.disabled"
  sudo mv /opt/travel-swap \
    "/opt/travel-swap.${travel_rollback_stamp}.disabled"
  sudo systemctl daemon-reload
)
```

The npm content cache is intentionally not restored; npm recreates it on
demand. The bounded cgroup reclaim has no persistent setting to roll back;
pages return to RAM naturally when referenced.
