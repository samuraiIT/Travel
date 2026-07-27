#!/usr/bin/env python3
"""Project entry point for the shared China travel validator."""

from __future__ import annotations

import runpy
from pathlib import Path


validator = (
    Path(__file__).resolve().parents[3]
    / ".agents"
    / "skills"
    / "china-travel-operations"
    / "scripts"
    / "validate_china_2026.py"
)
runpy.run_path(str(validator), run_name="__main__")
