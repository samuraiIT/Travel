#!/usr/bin/env python3
"""Render a minimal Travel Hermes profile without exposing donor secrets."""

from __future__ import annotations

import argparse
import copy
import os
import tempfile
from pathlib import Path

import yaml


ALLOWED_MCPS = ("context7", "lightpanda", "playwright")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def deep_merge(base: dict, overlay: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def select_omni_provider(source: dict) -> list[dict]:
    providers = source.get("custom_providers", [])
    if not isinstance(providers, list):
        raise ValueError("source custom_providers must be a list")
    for provider in providers:
        if isinstance(provider, dict) and provider.get("name") == "omni":
            return [copy.deepcopy(provider)]
    raise ValueError("source profile has no custom provider named 'omni'")


def select_mcps(source: dict) -> dict:
    available = source.get("mcp_servers", {})
    if not isinstance(available, dict):
        raise ValueError("source mcp_servers must be a mapping")
    missing = [name for name in ALLOWED_MCPS if name not in available]
    if missing:
        raise ValueError(f"source profile misses required MCPs: {', '.join(missing)}")
    return {name: copy.deepcopy(available[name]) for name in ALLOWED_MCPS}


def render(source: dict, overlay: dict) -> dict:
    base = {
        "_config_version": source.get("_config_version", 6),
        "custom_providers": select_omni_provider(source),
        "mcp_servers": select_mcps(source),
    }
    rendered = deep_merge(base, overlay)
    if Path(rendered["terminal"]["cwd"]).resolve() != Path(
        "/opt/project_llm/projects/Travel"
    ):
        raise ValueError("terminal.cwd must remain the Travel project root")
    return rendered


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rendered = render(load_yaml(args.source), load_yaml(args.overlay))
    atomic_write(
        args.output,
        yaml.safe_dump(rendered, sort_keys=False, allow_unicode=True),
    )
    print(f"Rendered Travel Hermes config: {args.output}")
    print(f"Enabled MCPs: {', '.join(ALLOWED_MCPS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
