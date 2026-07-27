from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "configure_hermes_profile.py"
SPEC = importlib.util.spec_from_file_location("configure_hermes_profile", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load profile renderer from {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TravelBotConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.overlay = yaml.safe_load(
            (ROOT / "config/hermes/travel-bot.overlay.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.source = {
            "_config_version": 9,
            "custom_providers": [
                {"name": "other", "api_key": "do-not-copy"},
                {
                    "name": "omni",
                    "api_key": "local-test-secret",
                    "base_url": "http://127.0.0.1:20128/v1",
                    "model": "hermes",
                    "models": {
                        "hermes": {},
                        "quick": {},
                        "travel-fast": {},
                        "codex-review": {},
                    },
                },
            ],
            "mcp_servers": {
                "context7": {"url": "https://mcp.context7.com/mcp"},
                "lightpanda": {"url": "http://127.0.0.1:9223/mcp"},
                "playwright": {"command": "npx", "args": ["@playwright/mcp"]},
                "unrelated": {"command": "never-copy"},
            },
        }

    def test_renderer_selects_minimal_provider_and_mcps(self) -> None:
        rendered = MODULE.render(self.source, self.overlay)
        self.assertEqual(
            [provider["name"] for provider in rendered["custom_providers"]],
            ["omni"],
        )
        self.assertEqual(
            set(rendered["mcp_servers"]),
            {"context7", "lightpanda", "playwright"},
        )
        self.assertNotIn("unrelated", rendered["mcp_servers"])
        self.assertEqual(rendered["model"]["default"], "travel-fast")
        self.assertEqual(
            rendered["custom_providers"][0]["model"], "travel-fast"
        )

    def test_renderer_rejects_unadvertised_default_model(self) -> None:
        self.source["custom_providers"][1]["models"].pop("travel-fast")
        with self.assertRaisesRegex(ValueError, "does not advertise"):
            MODULE.render(self.source, self.overlay)

    def test_owner_only_and_project_scope(self) -> None:
        rendered = MODULE.render(self.source, self.overlay)
        self.assertEqual(
            rendered["terminal"]["cwd"], "/opt/project_llm/projects/Travel"
        )
        self.assertEqual(rendered["telegram"]["allow_from"], ["5842551033"])
        self.assertTrue(rendered["gateway"]["strict"])
        self.assertFalse(rendered["security"]["allow_lazy_installs"])
        self.assertTrue(rendered["security"]["redact_secrets"])
        self.assertEqual(rendered["approvals"]["mode"], "smart")
        self.assertEqual(rendered["approvals"]["cron_mode"], "deny")
        self.assertTrue(rendered["sessions"]["auto_prune"])
        self.assertEqual(rendered["sessions"]["retention_days"], 30)
        self.assertEqual(
            rendered["skills"]["external_dirs"],
            [
                "/opt/project_llm/.agents/skills/travel-agent-skill",
                "/opt/project_llm/.agents/skills/travel-concierge",
                "/opt/project_llm/.agents/skills/travel-day-optimizer",
                "/opt/project_llm/.agents/skills/china-travel-operations",
                "/opt/project_llm/.agents/skills/web-agent-navigation",
                "/opt/project_llm/.agents/skills/augmented-advisory",
                "/opt/project_llm/.agents/skills/bash-defensive-patterns",
            ],
        )
        playwright_args = rendered["mcp_servers"]["playwright"]["args"]
        self.assertIn("@playwright/mcp@0.0.78", playwright_args)
        self.assertIn("--isolated", playwright_args)
        self.assertNotIn("--no-sandbox", playwright_args)
        self.assertNotIn("@playwright/mcp@latest", playwright_args)

    def test_prompt_contains_required_approval_gates(self) -> None:
        prompt = (ROOT / "prompts/TRAVEL_TELEGRAM_AGENT.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "покупка",
            "бронирование",
            "персональных",
            "Git push/release",
            "Confirmed",
            "Context7",
            "Lightpanda",
            "Playwright",
            "days[].deadline",
        ):
            self.assertIn(required, prompt)

    def test_installer_scrubs_inherited_telegram_token(self) -> None:
        installer = (ROOT / "scripts/install_travel_bot.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn('$1 != "TELEGRAM_BOT_TOKEN"', installer)
        self.assertIn('profile_created=true', installer)
        self.assertIn('readonly TRAVEL_DEFAULT_MODEL="travel-fast"', installer)
        self.assertIn(
            'set_env_key "HERMES_MODEL" "${TRAVEL_DEFAULT_MODEL}"', installer
        )
        self.assertIn('systemctl --user restart "${UNIT_NAME}"', installer)

    def test_systemd_unit_has_resource_guardrails(self) -> None:
        unit = (
            ROOT / "deploy/systemd/hermes-gateway-travel.service"
        ).read_text(encoding="utf-8")
        for required in (
            "MemoryHigh=1G",
            "MemoryMax=2G",
            "MemorySwapMax=512M",
            "TasksMax=256",
            "NoNewPrivileges=true",
        ):
            self.assertIn(required, unit)

    def test_resource_helper_is_bounded_and_dry_run_first(self) -> None:
        helper = (ROOT / "scripts/ensure_travel_resources.sh").read_text(
            encoding="utf-8"
        )
        swap_unit = (
            ROOT / "deploy/systemd/travel-swapfile.swap"
        ).read_text(encoding="utf-8")
        self.assertIn('readonly SWAP_DIR="/opt/travel-swap"', helper)
        self.assertIn('"${SWAP_DIR}/swap-primary.img"', helper)
        self.assertIn('"${SWAP_DIR}/swap-reserve.img"', helper)
        self.assertIn('"${SWAP_DIR}/swap-emergency.img"', helper)
        self.assertIn('$((4 * 1024 * 1024 * 1024))', helper)
        self.assertIn('$((8 * 1024 * 1024 * 1024))', helper)
        self.assertIn("APPLY=false", helper)
        self.assertIn('if [[ "${APPLY}" != true ]]', helper)
        self.assertIn("npm cache clean --force", helper)
        self.assertNotIn("rm -rf /home", helper)
        self.assertIn('sudo -n test -L "${swap_file}"', helper)
        self.assertIn('swap_type="$(sudo -n blkid', helper)
        self.assertIn("What=/opt/travel-swap/swap-primary.img", swap_unit)
        self.assertIn("RequiresMountsFor=/opt", swap_unit)
        self.assertIn("Priority=0", swap_unit)
        self.assertIn("WantedBy=swap.target", swap_unit)
        reserve_unit = (
            ROOT / "deploy/systemd/travel-swap-reserve.swap"
        ).read_text(encoding="utf-8")
        self.assertIn("What=/opt/travel-swap/swap-reserve.img", reserve_unit)
        self.assertIn("RequiresMountsFor=/opt", reserve_unit)
        self.assertIn("Priority=0", reserve_unit)
        self.assertIn("WantedBy=swap.target", reserve_unit)
        emergency_unit = (
            ROOT / "deploy/systemd/travel-swap-emergency.swap"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "What=/opt/travel-swap/swap-emergency.img", emergency_unit
        )
        self.assertIn("RequiresMountsFor=/opt", emergency_unit)
        self.assertIn("Priority=-1", emergency_unit)
        self.assertIn("WantedBy=swap.target", emergency_unit)
        preflight = (
            ROOT / "scripts/preflight_travel_bot.sh"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "SWAP_FALLBACK_MEM_AVAILABLE_KIB=$((12 * 1024 * 1024))",
            preflight,
        )
        self.assertIn(
            "mem_available_kib >= SWAP_FALLBACK_MEM_AVAILABLE_KIB",
            preflight,
        )


if __name__ == "__main__":
    unittest.main()
