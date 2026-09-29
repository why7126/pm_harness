#!/usr/bin/env python3
"""Validate ProjectPmHarness root governance directory boundaries."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required_dirs = [
    "docs/decision-notes",
    "docs/spec-logs",
    "issues/requirements",
    "issues/bugs",
    "iterations/change",
    "openspec/changes",
    ".agents/skills",
]
missing = [path for path in required_dirs if not (ROOT / path).is_dir()]
if missing:
    print("Missing required directories:")
    for path in missing:
        print(f"- {path}")
    sys.exit(1)

for forbidden in [".claude", ".cursor", ".kiro", ".opencode"]:
    if (ROOT / forbidden).exists():
        print(f"Forbidden multi-agent entry exists: {forbidden}")
        sys.exit(1)

print("directory structure validation passed")
