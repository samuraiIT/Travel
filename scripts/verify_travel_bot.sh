#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly PROJECT_ROOT="/opt/project_llm/projects/Travel"
readonly PROFILE_DIR="${HOME}/.hermes/profiles/travel-bot"
readonly UNIT_NAME="hermes-gateway-travel.service"
readonly UNIT_FILE="${HOME}/.config/systemd/user/${UNIT_NAME}"
readonly HERMES_BIN="${HOME}/.local/bin/hermes"

ALLOW_PENDING_SECRET=false
if [[ "${1:-}" == "--allow-pending-secret" ]]; then
  ALLOW_PENDING_SECRET=true
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--allow-pending-secret]\n' "$0" >&2
  exit 64
fi

failures=0
pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; failures=$((failures + 1)); }

if python3 "${PROJECT_ROOT}/scripts/validate_itinerary.py"; then
  pass "China itinerary validator"
else
  fail "China itinerary validator"
fi

if python3 -m unittest discover -s "${PROJECT_ROOT}/tests" -v; then
  pass "Travel bot unit tests"
else
  fail "Travel bot unit tests"
fi

if "${PROJECT_ROOT}/scripts/preflight_travel_bot.sh"; then
  pass "runtime resource preflight"
elif [[ "${ALLOW_PENDING_SECRET}" == true ]]; then
  printf 'PENDING: runtime resource gate is not green; live start is blocked.\n'
else
  fail "runtime resource preflight"
fi

if git -C "${PROJECT_ROOT}" grep -En \
  '[0-9]{8,12}:[A-Za-z0-9_-]{30,}' -- . \
  ':(exclude)tests/*' >/dev/null; then
  fail "repository contains a Telegram-token-shaped string"
else
  pass "repository contains no Telegram token"
fi

for required in config.yaml SOUL.md .env; do
  if [[ -f "${PROFILE_DIR}/${required}" ]]; then
    pass "profile contains ${required}"
  else
    fail "profile misses ${required}"
  fi
done

if [[ -f "${PROFILE_DIR}/config.yaml" ]] &&
  env -u TELEGRAM_BOT_TOKEN \
    "${HERMES_BIN}" -p travel-bot config check >/dev/null; then
  pass "Hermes configuration check"
else
  fail "Hermes configuration check"
fi

if [[ -f "${PROFILE_DIR}/config.yaml" ]] &&
  [[ "$("${HERMES_BIN}" -p travel-bot config get terminal.cwd 2>/dev/null)" == \
    "${PROJECT_ROOT}" ]]; then
  pass "terminal cwd is restricted to Travel"
else
  fail "terminal cwd is not the Travel project"
fi

if [[ -f "${UNIT_FILE}" ]] &&
  systemd-analyze --user verify "${UNIT_FILE}" >/dev/null; then
  pass "systemd unit syntax"
else
  fail "systemd unit syntax"
fi

token_ready=false
if [[ -f "${PROFILE_DIR}/.env" ]] &&
  grep -Eq '^TELEGRAM_BOT_TOKEN=.+$' "${PROFILE_DIR}/.env"; then
  token_ready=true
  pass "Telegram token is provisioned outside Git"
elif [[ "${ALLOW_PENDING_SECRET}" == true ]]; then
  printf 'PENDING: rotate and provision Telegram token before live activation.\n'
else
  fail "Telegram token is not provisioned"
fi

if [[ "${token_ready}" == true ]]; then
  if systemctl --user is-active --quiet "${UNIT_NAME}"; then
    pass "Travel gateway is active"
  else
    fail "Travel gateway is not active"
  fi
  if journalctl --user -u "${UNIT_NAME}" -n 100 --no-pager |
    grep -Eq '409|Conflict: terminated by other getUpdates request'; then
    fail "Telegram polling conflict found"
  else
    pass "no Telegram polling conflict in recent logs"
  fi
fi

for neighbor in hermes-gateway-trading.service hermes-gateway-terra.service \
  hermes-gateway-ipregion.service; do
  if systemctl --user is-active --quiet "${neighbor}"; then
    pass "neighbor remains active: ${neighbor}"
  else
    fail "neighbor is not active: ${neighbor}"
  fi
done

if [[ "${failures}" -ne 0 ]]; then
  printf 'Verification failed: %d check(s).\n' "${failures}" >&2
  exit 1
fi
printf 'Verification complete: all applicable checks passed.\n'
