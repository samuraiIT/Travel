# Travel v1.0.3

Resource-stability patch following the `travel-fast` rollout.

## Outcome

- Added `/opt/travel-swap/swap-emergency.img`, 8 GiB.
- Added persistent unit
  `opt-travel\x2dswap-swap\x2demergency.img.swap`.
- Set unit priority to `-1` (kernel auto-allocation; effective `-4` on this
  host), below the normal Travel devices (`0`), so the file acts as emergency
  capacity rather than preferred paging capacity.
- Kept 8 GiB `MemAvailable` and 4 GiB free under `/home` as hard
  requirements. The swap condition is now either 2 GiB `SwapFree` or a
  stricter 12 GiB `MemAvailable` fallback.
- No model, combo, Telegram credential, or neighboring gateway changed.

## Why

The host has about 60 GiB of anonymous working set across long-lived services.
Up to 37 GiB remains cold in swap even while about 20 GiB RAM is available.
The 1.0.2 primary + secondary Travel swap and the new emergency device were
therefore consumed as working capacity rather than remaining empty headroom.

The low-priority emergency file increases capacity. The adaptive gate measures
actual reclaimable headroom: it never permits less than 8 GiB RAM, and when
swap is full it requires 12 GiB RAM instead. This avoids killing unrelated
processes, changing global swappiness, or cycling an in-use swap device.

## Verification

- unit and helper regression tests;
- systemd unit syntax;
- exact file owner/mode/size/type validation;
- active swap-device verification;
- full Travel preflight and bot verifier;
- neighboring trading, terra, and ipregion gateways remain active.

## Rollback

Only after confirming the emergency file is unused or can be safely swapped
off:

```bash
sudo systemctl disable --now \
  'opt-travel\x2dswap-swap\x2demergency.img.swap'
```

Move the unit and swap file to timestamped `.disabled` paths; do not delete
them while active.
