# Travel v1.0.2

Performance and correctness release for `@travel_samurai_bot`.

## Outcome

- Live model: OmniRoute combo `travel-fast`.
- Priority path: `codex/gpt-5.3-codex-spark`.
- Availability fallback: existing strict Codex-only combo `codex-review`.
- Travel gateway: enabled and active; neighboring Hermes gateways were not
  restarted.
- Telegram credential remains outside Git in the profile `.env`.

The existing `quick`, `free`, `hermes`, and `codex-review` combos were not
modified. `travel-fast` was created through the authenticated Dashboard
session + CSRF REST path; OmniRoute SQLite was not written directly.

## Why this model

The old `hermes` route actually served `codex/gpt-5.5`. Eleven production
calls took about 184 seconds in total, with a 10.4-second median LLM call and
a 60-second worst case. The Travel profile also injected a 126,855-byte skill
index, producing observed prompts around 81–89K input tokens.

Release acceptance used the real project question, not only `PONG`:

```text
Find the three earliest non-empty days[].deadline values, keep duplicate dates,
and return deadline | status | booking.
```

`quick` and free candidates were rejected when they returned wrong deadlines,
lost a duplicate date, hit quota/credential failures, or produced a 47-second
tail. `codex-review` was correct but slower in the full Hermes smoke.
`travel-fast` passed direct text, native tool-use, deadline accuracy, and the
full default-profile smoke.

Measured after rollout:

- direct combo text: 1.68 seconds;
- direct native tool call: 2.06 seconds;
- direct deadline test: 5.89 seconds;
- cold full Hermes file-reading smoke: 24.7 seconds, exact answer;
- system prompt: 145,226 → 19,353 bytes;
- skill index: 126,855 → 772 bytes.

Telegram latency depends on session/tool state, but the dominant prompt bloat
and the 60-second old route were removed.

## Resource note

The host filled all existing swap with cold pages during rollout while the
Travel service itself stayed below 0.7 GiB. The secondary `/opt` Travel reserve
was expanded from 4 to 8 GiB; together with the 4 GiB primary reserve this
provides 12 GiB of project-managed swap. The original preflight thresholds were
not weakened or bypassed.

## Verification

- 7 unit tests;
- itinerary validator;
- Bash syntax and `git diff --check`;
- authenticated Dashboard inventory before and after combo creation;
- direct combo text/native-tool/semantic gates;
- live default-profile semantic smoke;
- Hermes config check and prompt-size inspection;
- full `scripts/verify_travel_bot.sh`;
- no Telegram `401`, `409`, polling conflict, or recent traceback;
- all neighboring Hermes gateways remained active.

## Rollback

Restore the latest `config.yaml.pre-quick-*` and `.env.pre-quick-*` backups in
`~/.hermes/profiles/travel-bot`, or set both the generated config and
`HERMES_MODEL` back to the previous model and restart only:

```bash
systemctl --user restart hermes-gateway-travel.service
```

Do not delete or broaden `codex-review`; it remains a strict Codex-only lane.
