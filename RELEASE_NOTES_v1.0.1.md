# Travel v1.0.1

Patch release for safe host-resource remediation before Telegram activation.

## Added

- Dry-run-first `scripts/ensure_travel_resources.sh`.
- Two persistent 4 GiB `/opt` swapfiles managed by escaped systemd swap units.
- Root-owned `0700` swap directory; symlink/non-regular targets are rejected.
- Exact checks for swapfile size, ownership, mode and active state.
- Swap signatures are verified before activation.
- Both Travel swap units use an explicit deterministic priority of `0`.
- `/home` cleanup limited to npm's regenerable content cache and only when the
  4 GiB availability gate is red.
- Reproducible rollback and resource-helper regression coverage.

## Live verification

- `/home` and swap gates restored without stopping OmniRoute, Lightpanda or
  neighboring Hermes gateways.
- Bounded cgroup-v2 reclaim moved about 3 GiB of cold current-session memory
  to swap without terminating processes.
- `scripts/preflight_travel_bot.sh` passed all resource/runtime checks.

## Activation boundary

The Travel Telegram unit remains disabled and inactive. The token previously
shared in chat is treated as compromised and was never provisioned. Activate
only with a freshly rotated token through:

```bash
cd /opt/project_llm/projects/Travel
./scripts/provision_travel_bot.sh
```

The script reads the token from a hidden TTY prompt, validates
`@travel_samurai_bot` through Telegram `getMe`, stores it outside Git with mode
`0600`, and runs the full verifier.
