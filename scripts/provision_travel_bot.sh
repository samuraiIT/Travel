#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

readonly PROJECT_ROOT="/opt/project_llm/projects/Travel"
readonly PROFILE_DIR="${HOME}/.hermes/profiles/travel-bot"
readonly ENV_FILE="${PROFILE_DIR}/.env"
readonly UNIT_NAME="hermes-gateway-travel.service"
readonly EXPECTED_USERNAME="travel_samurai_bot"
readonly DEFAULT_OWNER_ID="5842551033"

force_resource_gate=false
if [[ "${1:-}" == "--force-resource-gate" ]]; then
  force_resource_gate=true
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--force-resource-gate]\n' "$0" >&2
  exit 64
fi

if [[ ! -t 0 ]]; then
  printf '%s\n' \
    "ERROR: interactive TTY required; the token must not be passed as an argument." >&2
  exit 64
fi
if [[ ! -d "${PROFILE_DIR}" || ! -f "${ENV_FILE}" ]]; then
  printf 'ERROR: run %s/scripts/install_travel_bot.sh first.\n' \
    "${PROJECT_ROOT}" >&2
  exit 1
fi

if ! "${PROJECT_ROOT}/scripts/preflight_travel_bot.sh"; then
  if [[ "${force_resource_gate}" != true ]]; then
    printf '%s\n' \
      "ERROR: resource/runtime preflight failed; token was not requested." \
      "Free host resources and retry. Use --force-resource-gate only after" \
      "an explicit owner risk decision." >&2
    exit 1
  fi
  printf '%s\n' \
    "WARNING: owner explicitly bypassed the resource gate; cgroup limits remain active." >&2
fi

printf '%s\n' \
  "Use only a freshly rotated BotFather token for @${EXPECTED_USERNAME}." \
  "The token will not be echoed or stored in shell history."
IFS= read -r -s -p "Rotated Telegram bot token: " bot_token
printf '\n'
IFS= read -r -p "Owner Telegram numeric ID [${DEFAULT_OWNER_ID}]: " owner_id
owner_id="${owner_id:-${DEFAULT_OWNER_ID}}"

if [[ ! "${bot_token}" =~ ^[0-9]{8,12}:[A-Za-z0-9_-]{30,}$ ]]; then
  printf 'ERROR: token format is invalid.\n' >&2
  exit 1
fi
if [[ ! "${owner_id}" =~ ^[0-9]{5,20}$ ]]; then
  printf 'ERROR: owner ID must be numeric.\n' >&2
  exit 1
fi

temp_dir="$(mktemp -d)"
cleanup() {
  bot_token=""
  rm -rf "${temp_dir}"
}
trap cleanup EXIT
chmod 700 "${temp_dir}"

curl_config="${temp_dir}/curl.conf"
response_file="${temp_dir}/getme.json"
printf 'silent\nshow-error\nfail\nurl = "https://api.telegram.org/bot%s/getMe"\n' \
  "${bot_token}" > "${curl_config}"
chmod 600 "${curl_config}"
curl --config "${curl_config}" --output "${response_file}"

actual_username="$(
  python3 - "${response_file}" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if payload.get("ok") is not True:
    raise SystemExit("Telegram getMe did not return ok=true")
print(payload.get("result", {}).get("username", ""))
PY
)"
if [[ "${actual_username}" != "${EXPECTED_USERNAME}" ]]; then
  printf 'ERROR: token belongs to @%s, expected @%s.\n' \
    "${actual_username:-unknown}" "${EXPECTED_USERNAME}" >&2
  exit 1
fi

upsert_env_key() {
  local key="$1"
  local value="$2"
  local output="${temp_dir}/env.next"
  awk -F= -v wanted="${key}" '$1 != wanted { print }' "${ENV_FILE}" > "${output}"
  printf '%s=%s\n' "${key}" "${value}" >> "${output}"
  install -m 600 "${output}" "${ENV_FILE}"
}

upsert_env_key "TELEGRAM_BOT_TOKEN" "${bot_token}"
upsert_env_key "TELEGRAM_ALLOWED_USERS" "${owner_id}"
upsert_env_key "GATEWAY_ALLOW_ALL_USERS" "false"

systemctl --user enable --now "${UNIT_NAME}"
sleep 2
"${PROJECT_ROOT}/scripts/verify_travel_bot.sh"

printf 'Provisioned and started @%s for owner %s.\n' \
  "${EXPECTED_USERNAME}" "${owner_id}"
