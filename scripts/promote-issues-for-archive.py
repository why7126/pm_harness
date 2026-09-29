#!/usr/bin/env python3
"""Minimal root issue promotion guard for governance-only archive commands."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def issue_traces_linking_change(change: str) -> list[Path]:
    issue_root = ROOT / "issues"
    if not issue_root.exists():
        return []
    matches: list[Path] = []
    for trace in issue_root.glob("**/trace.md"):
        try:
            text = trace.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if change in text:
            matches.append(trace)
    return matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--change")
    parser.add_argument("--sprint")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()

    if not args.change and not args.sprint:
        print("--change or --sprint is required")
        return 1

    if args.change:
        linked = issue_traces_linking_change(args.change)
        print(f"Promote Issues For Archive: change={args.change}")
        if linked:
            print("Linked issue traces found; root minimal promoter cannot safely move issue packages:")
            for path in linked:
                print(f"- {path.relative_to(ROOT)}")
            print("Use the full Harness issue promotion tool before completing archive.")
            return 1
        print("Promoted issues: 0")
        print("Reason: governance change has no linked REQ/BUG issue traces")
        print("Errors: 0")
        return 0

    print(f"Promote Issues For Archive: sprint={args.sprint}")
    print("Promoted issues: 0")
    print("Reason: root governance sprint promotion is not issue-scoped")
    print("Errors: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
