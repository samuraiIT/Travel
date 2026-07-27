#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly MIN_MEM_AVAILABLE_KIB=$((8 * 1024 * 1024))
readonly SWAP_FALLBACK_MEM_AVAILABLE_KIB=$((12 * 1024 * 1024))
readonly MIN_HOME_AVAILABLE_KIB=$((4 * 1024 * 1024))
readonly RECOMMENDED_SWAP_FREE_KIB=$((2 * 1024 * 1024))

failures=0
pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; failures=$((failures + 1)); }

mem_available_kib="$(
  awk '$1 == "MemAvailable:" { print $2 }' /proc/meminfo
)"
swap_free_kib="$(
  awk '$1 == "SwapFree:" { print $2 }' /proc/meminfo
)"
home_available_kib="$(df -Pk "${HOME}" | awk 'NR == 2 { print $4 }')"

if (( mem_available_kib >= MIN_MEM_AVAILABLE_KIB )); then
  pass "MemAvailable is at least 8 GiB"
else
  fail "MemAvailable is below 8 GiB (${mem_available_kib} KiB)"
fi

if (( home_available_kib >= MIN_HOME_AVAILABLE_KIB )); then
  pass "/home has at least 4 GiB available"
else
  fail "/home has below 4 GiB available (${home_available_kib} KiB)"
fi

if (( swap_free_kib >= RECOMMENDED_SWAP_FREE_KIB )); then
  pass "SwapFree is at least 2 GiB"
elif (( mem_available_kib >= SWAP_FALLBACK_MEM_AVAILABLE_KIB )); then
  pass "SwapFree is below 2 GiB but MemAvailable is at least 12 GiB"
else
  fail "SwapFree is below 2 GiB and MemAvailable is below 12 GiB"
fi

if systemctl --user is-active --quiet omniroute.service ||
  systemctl is-active --quiet omniroute.service; then
  pass "OmniRoute service is active"
else
  fail "OmniRoute service is not active"
fi

if systemctl --user is-active --quiet lightpanda-mcp.service ||
  systemctl is-active --quiet lightpanda-mcp.service; then
  pass "Lightpanda MCP service is active"
else
  fail "Lightpanda MCP service is not active"
fi

for neighbor in hermes-gateway-trading.service hermes-gateway-terra.service \
  hermes-gateway-ipregion.service; do
  if systemctl --user is-active --quiet "${neighbor}"; then
    pass "neighbor is active: ${neighbor}"
  else
    fail "neighbor is not active: ${neighbor}"
  fi
done

printf 'Preflight summary: failures=%d\n' "${failures}"
if (( failures > 0 )); then
  exit 1
fi
