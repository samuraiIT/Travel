# Travel Agents delivery roadmap

## Release 1.0.0 — dedicated owner bot

- [x] Read workspace and project canon; preserve immutable tickets.
- [x] Audit live Hermes profiles, gateways, service pattern, and OmniRoute.
- [x] Query current Hermes documentation through Context7.
- [x] Research official Hermes, browser MCP, China rail/map MCP, and skills.
- [x] Define roles, Travel SOUL, tool order, trust boundaries, and approvals.
- [x] Build idempotent profile renderer, installer, unit, verifier, and rollback.
- [x] Add minimal MCP policy and owner-only Telegram allowlist.
- [x] Add tests, secret scan, itinerary validator, and monitoring hooks.
- [x] Stage the dedicated profile and disabled/inactive user unit.
- [ ] Rotate the token disclosed in chat and provision it by hidden TTY input.
- [ ] Restore the host resource gate: at least 8 GiB MemAvailable, 2 GiB free
      swap, and 4 GiB free under `/home`.
- [ ] Complete owner `/start` and real question smoke after rotation.

The final two checks are deliberately impossible to automate safely from the
disclosed chat credential. Run:

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
