#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

readonly PROJECT_ROOT="/opt/project_llm/projects/Travel"
readonly PROFILE_NAME="travel-bot"
readonly PROFILE_DIR="${HOME}/.hermes/profiles/${PROFILE_NAME}"
readonly DONOR_PROFILE="${HERMES_DONOR_PROFILE:-trading-bot}"
readonly DONOR_CONFIG="${HOME}/.hermes/profiles/${DONOR_PROFILE}/config.yaml"
readonly HERMES_BIN="${HOME}/.local/bin/hermes"
readonly UNIT_NAME="hermes-gateway-travel.service"
readonly UNIT_SOURCE="${PROJECT_ROOT}/deploy/systemd/${UNIT_NAME}"
readonly UNIT_TARGET="${HOME}/.config/systemd/user/${UNIT_NAME}"
readonly OWNER_ID="5842551033"
readonly TRAVEL_DEFAULT_MODEL="travel-fast"

START_NOW=false
if [[ "${1:-}" == "--start" ]]; then
  START_NOW=true
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--start]\n' "$0" >&2
  exit 64
fi

for required in "${HERMES_BIN}" "${DONOR_CONFIG}" \
  "${PROJECT_ROOT}/config/hermes/travel-bot.overlay.yaml" \
  "${PROJECT_ROOT}/prompts/TRAVEL_TELEGRAM_AGENT.md" "${UNIT_SOURCE}"; do
  if [[ ! -e "${required}" ]]; then
    printf 'ERROR: required path missing: %s\n' "${required}" >&2
    exit 1
  fi
done

profile_created=false
if [[ ! -d "${PROFILE_DIR}" ]]; then
  "${HERMES_BIN}" profile create "${PROFILE_NAME}" \
    --no-alias \
    --no-skills \
    --description "Owner-only Travel Operations Agent for the Travel project"
  profile_created=true
fi

install -d -m 700 "${PROFILE_DIR}" "${HOME}/.config/systemd/user"

if [[ -f "${PROFILE_DIR}/config.yaml" ]]; then
  backup="${PROFILE_DIR}/config.yaml.bak-$(date -u +%Y%m%dT%H%M%SZ)"
  install -m 600 "${PROFILE_DIR}/config.yaml" "${backup}"
fi

python3 "${PROJECT_ROOT}/scripts/configure_hermes_profile.py" \
  --source "${DONOR_CONFIG}" \
  --overlay "${PROJECT_ROOT}/config/hermes/travel-bot.overlay.yaml" \
  --output "${PROFILE_DIR}/config.yaml"
"${HERMES_BIN}" -p "${PROFILE_NAME}" config migrate >/dev/null

install -m 600 \
  "${PROJECT_ROOT}/prompts/TRAVEL_TELEGRAM_AGENT.md" \
  "${PROFILE_DIR}/SOUL.md"

env_file="${PROFILE_DIR}/.env"
if [[ ! -f "${env_file}" ]]; then
  install -m 600 /dev/null "${env_file}"
fi

# Hermes profile creation can inherit a channel token from the current
# environment. A new domain profile must never retain that token.
if [[ "${profile_created}" == true ]]; then
  scrubbed_env="$(mktemp "${PROFILE_DIR}/.env.scrub.XXXXXX")"
  chmod 600 "${scrubbed_env}"
  awk -F= '$1 != "TELEGRAM_BOT_TOKEN" { print }' \
    "${env_file}" > "${scrubbed_env}"
  mv -f "${scrubbed_env}" "${env_file}"
fi

set_env_key() {
  local key="$1"
  local value="$2"
  local temp_file
  temp_file="$(mktemp "${PROFILE_DIR}/.env.XXXXXX")"
  chmod 600 "${temp_file}"
  awk -F= -v wanted="${key}" '$1 != wanted { print }' "${env_file}" > "${temp_file}"
  printf '%s=%s\n' "${key}" "${value}" >> "${temp_file}"
  mv -f "${temp_file}" "${env_file}"
}

set_env_key "HERMES_MODEL" "${TRAVEL_DEFAULT_MODEL}"
set_env_key "HERMES_PROVIDER" "custom:omni"
set_env_key "OPENAI_API_BASE" "http://127.0.0.1:20128/v1"
set_env_key "TELEGRAM_ALLOWED_USERS" "${OWNER_ID}"
set_env_key "GATEWAY_ALLOW_ALL_USERS" "false"

chmod 600 "${PROFILE_DIR}/config.yaml" "${PROFILE_DIR}/SOUL.md" "${env_file}"
install -m 644 "${UNIT_SOURCE}" "${UNIT_TARGET}"
systemctl --user daemon-reload

env -u TELEGRAM_BOT_TOKEN \
  "${HERMES_BIN}" -p "${PROFILE_NAME}" config check >/dev/null
printf 'Hermes configuration check passed.\n'

if [[ "${START_NOW}" == true ]]; then
  if ! grep -Eq '^TELEGRAM_BOT_TOKEN=.+$' "${env_file}"; then
    printf '%s\n' \
      "ERROR: rotated Telegram token is not provisioned." \
      "Run scripts/provision_travel_bot.sh from an interactive terminal." >&2
    exit 2
  fi
  "${PROJECT_ROOT}/scripts/preflight_travel_bot.sh"
  systemctl --user enable "${UNIT_NAME}"
  if systemctl --user is-active --quiet "${UNIT_NAME}"; then
    systemctl --user restart "${UNIT_NAME}"
  else
    systemctl --user start "${UNIT_NAME}"
  fi
else
  if ! grep -Eq '^TELEGRAM_BOT_TOKEN=.+$' "${env_file}"; then
    # Enabled units are discovered by the shared healthcheck and can be
    # started automatically. Keep a secretless staged unit disabled.
    systemctl --user disable --now "${UNIT_NAME}" >/dev/null 2>&1 || true
    systemctl --user reset-failed "${UNIT_NAME}" >/dev/null 2>&1 || true
  fi
  printf '%s\n' \
    "Profile and unit installed. Secretless service is disabled and stopped." \
    "Rotate the exposed token in BotFather, then run:" \
    "  ${PROJECT_ROOT}/scripts/provision_travel_bot.sh"
fi
