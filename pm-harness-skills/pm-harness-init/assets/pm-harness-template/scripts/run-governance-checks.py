#!/usr/bin/env python3
"""Run PM Harness governance checks as a read-only aggregate."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "context-budget": ["scripts/validate-agent-context-budget.py"],
    "openspec-language": ["scripts/validate-openspec-language.py"],
    "directory-structure": ["scripts/validate-directory-structure.py"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "checks",
        nargs="*",
        choices=sorted(CHECKS),
        help="Optional subset of checks to run. Defaults to all checks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = args.checks or sorted(CHECKS)
    failures: list[str] = []

    for check in selected:
        command = [sys.executable, *CHECKS[check]]
        print(f"==> {check}: {' '.join(command)}")
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            failures.append(check)

    if failures:
        print("governance checks failed:")
        for check in failures:
            print(f"- {check}")
        return 1

    print("governance checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
