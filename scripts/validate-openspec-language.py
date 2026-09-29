#!/usr/bin/env python3
"""Lightweight OpenSpec language validation for root governance changes."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
bad = []
for path in (ROOT / "openspec/changes").glob("*/**/*.md"):
    text = path.read_text(encoding="utf-8")
    if "[TODO]" in text or "待确认" in text:
        bad.append(path.relative_to(ROOT).as_posix())

if bad:
    print("OpenSpec documents contain unresolved placeholders:")
    for path in bad:
        print(f"- {path}")
    sys.exit(1)

print("openspec language validation passed")
