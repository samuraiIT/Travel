#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly PROJECT_ROOT="/opt/project_llm/projects/Travel"
readonly SWAP_DIR="/opt/travel-swap"
readonly MIN_HOME_AVAILABLE_KIB=$((4 * 1024 * 1024))
readonly -a SWAP_FILES=(
  "${SWAP_DIR}/swap-primary.img"
  "${SWAP_DIR}/swap-reserve.img"
  "${SWAP_DIR}/swap-emergency.img"
)
readonly -a SWAP_SIZE_BYTES=(
  $((4 * 1024 * 1024 * 1024))
  $((8 * 1024 * 1024 * 1024))
  $((8 * 1024 * 1024 * 1024))
)
readonly -a SWAP_SIZE_LABELS=(
  "4 GiB"
  "8 GiB"
  "8 GiB"
)
readonly -a UNIT_TEMPLATES=(
  "${PROJECT_ROOT}/deploy/systemd/travel-swapfile.swap"
  "${PROJECT_ROOT}/deploy/systemd/travel-swap-reserve.swap"
  "${PROJECT_ROOT}/deploy/systemd/travel-swap-emergency.swap"
)

APPLY=false
if [[ "${1:-}" == "--apply" ]]; then
  APPLY=true
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--apply]\n' "$0" >&2
  exit 64
fi

for dependency in awk blkid df du fallocate grep install mktemp mkswap \
  npm rm stat sudo swapon systemctl systemd-analyze systemd-escape; do
  if ! command -v "${dependency}" >/dev/null 2>&1; then
    printf 'ERROR: required command is missing: %s\n' "${dependency}" >&2
    exit 1
  fi
done
validation_dir="$(mktemp -d)"
trap 'rm -rf -- "${validation_dir}"' EXIT
for index in "${!SWAP_FILES[@]}"; do
  swap_file="${SWAP_FILES[${index}]}"
  unit_template="${UNIT_TEMPLATES[${index}]}"
  if [[ ! -f "${unit_template}" ]]; then
    printf 'ERROR: unit template is missing: %s\n' "${unit_template}" >&2
    exit 1
  fi
  unit_name="$(systemd-escape --path --suffix=swap "${swap_file}")"
  install -m 644 "${unit_template}" "${validation_dir}/${unit_name}"
  systemd-analyze verify "${validation_dir}/${unit_name}"
done

home_available_kib="$(df -Pk "${HOME}" | awk 'NR == 2 { print $4 }')"
swap_free_kib="$(awk '$1 == "SwapFree:" { print $2 }' /proc/meminfo)"
printf 'Current: home_available=%s KiB swap_free=%s KiB\n' \
  "${home_available_kib}" "${swap_free_kib}"

if [[ "${APPLY}" != true ]]; then
  if (( home_available_kib < MIN_HOME_AVAILABLE_KIB )); then
    printf '%s\n' \
      "DRY RUN: would clear only the regenerable npm content cache."
  else
    printf '%s\n' \
      "DRY RUN: would preserve npm cache because /home satisfies the gate."
  fi
  printf 'DRY RUN: would ensure %s is root:root 0700.\n' "${SWAP_DIR}"
  for index in "${!SWAP_FILES[@]}"; do
    swap_file="${SWAP_FILES[${index}]}"
    swap_size_label="${SWAP_SIZE_LABELS[${index}]}"
    unit_name="$(systemd-escape --path --suffix=swap "${swap_file}")"
    printf '%s\n' \
      "DRY RUN: would ensure ${swap_file} is ${swap_size_label} and valid." \
      "DRY RUN: would install and enable /etc/systemd/system/${unit_name}."
  done
  printf 'Re-run with --apply to execute.\n'
  exit 0
fi

if ! sudo -n true; then
  printf 'ERROR: passwordless sudo is required for swap provisioning.\n' >&2
  exit 1
fi

if sudo -n test -L "${SWAP_DIR}"; then
  printf 'ERROR: swap directory must not be a symlink: %s\n' \
    "${SWAP_DIR}" >&2
  exit 1
elif sudo -n test -e "${SWAP_DIR}"; then
  if ! sudo -n test -d "${SWAP_DIR}"; then
    printf 'ERROR: swap directory is not a real directory: %s\n' \
      "${SWAP_DIR}" >&2
    exit 1
  fi
else
  sudo -n install -d -o root -g root -m 700 "${SWAP_DIR}"
fi
if sudo -n test -L "${SWAP_DIR}"; then
  printf 'ERROR: swap directory became a symlink: %s\n' "${SWAP_DIR}" >&2
  exit 1
fi
swap_dir_owner_mode="$(sudo -n stat -c '%U:%G %a' "${SWAP_DIR}")"
if [[ "${swap_dir_owner_mode}" != "root:root 700" ]]; then
  printf 'ERROR: swap directory has unexpected owner/mode: %s\n' \
    "${swap_dir_owner_mode}" >&2
  exit 1
fi

if (( home_available_kib < MIN_HOME_AVAILABLE_KIB )); then
  # This removes only npm's re-downloadable content-addressed cache. Installed
  # global packages and the _npx execution cache are not removed.
  npm cache clean --force
else
  printf 'SKIP: /home already satisfies the 4 GiB availability gate.\n'
fi

for index in "${!SWAP_FILES[@]}"; do
  swap_file="${SWAP_FILES[${index}]}"
  swap_size_bytes="${SWAP_SIZE_BYTES[${index}]}"
  unit_template="${UNIT_TEMPLATES[${index}]}"
  unit_name="$(systemd-escape --path --suffix=swap "${swap_file}")"
  unit_target="/etc/systemd/system/${unit_name}"

  if sudo -n test -L "${swap_file}"; then
    printf 'ERROR: swap target must not be a symlink: %s\n' \
      "${swap_file}" >&2
    exit 1
  elif ! sudo -n test -e "${swap_file}"; then
    sudo -n install -o root -g root -m 600 /dev/null "${swap_file}"
    if ! sudo -n fallocate -l "${swap_size_bytes}" "${swap_file}"; then
      sudo -n rm -f -- "${swap_file}"
      exit 1
    fi
    allocated_bytes="$(sudo -n du -B1 "${swap_file}" | awk '{ print $1 }')"
    if (( allocated_bytes < swap_size_bytes )); then
      printf 'ERROR: swapfile is sparse (%s of %s bytes allocated).\n' \
        "${allocated_bytes}" "${swap_size_bytes}" >&2
      sudo -n rm -f -- "${swap_file}"
      exit 1
    fi
    if ! sudo -n mkswap "${swap_file}"; then
      sudo -n rm -f -- "${swap_file}"
      exit 1
    fi
  else
    if ! sudo -n test -f "${swap_file}"; then
      printf 'ERROR: existing swap target is not a regular file: %s\n' \
        "${swap_file}" >&2
      exit 1
    fi
    owner_mode="$(sudo -n stat -c '%U:%G %a' "${swap_file}")"
    size_bytes="$(sudo -n stat -c '%s' "${swap_file}")"
    swap_type="$(sudo -n blkid -p -s TYPE -o value "${swap_file}" || true)"
    if [[ "${owner_mode}" != "root:root 600" ]] ||
      [[ "${swap_type}" != "swap" ]] ||
      (( size_bytes != swap_size_bytes )); then
      printf '%s\n' \
        "ERROR: existing swap target has unexpected owner/mode/size/type:" \
        "${swap_file}" >&2
      exit 1
    fi
  fi

  if [[ "$(sudo -n blkid -p -s TYPE -o value "${swap_file}" || true)" != \
    "swap" ]]; then
    printf 'ERROR: swap signature verification failed: %s\n' \
      "${swap_file}" >&2
    exit 1
  fi

  sudo -n install -m 644 "${unit_template}" "${unit_target}"
  sudo -n systemctl daemon-reload
  sudo -n systemctl enable --now "${unit_name}"

  if ! sudo -n swapon --show=NAME --noheadings |
    awk '{$1=$1};1' | grep -Fxq "${swap_file}"; then
    printf 'ERROR: swapfile is not active after unit start: %s\n' \
      "${swap_file}" >&2
    exit 1
  fi
done

"${PROJECT_ROOT}/scripts/preflight_travel_bot.sh"
