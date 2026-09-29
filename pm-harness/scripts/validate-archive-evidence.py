#!/usr/bin/env python3
"""Validate archived OpenSpec Change evidence for a single Change."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from archive_evidence import validate_archive_evidence


ROOT = Path(__file__).resolve().parents[1]


def render_markdown(result) -> str:
    lines = [
        "## Archive Evidence Report",
        "",
        f"**Change:** `{result.change_id}`",
        f"**Archive Path:** `{result.archive_path}`",
        f"**Evidence Status:** {result.status}",
        f"**Trace:** {'present' if result.trace_exists else 'missing'}",
    ]
    if result.fallback_summary_file:
        lines.append(f"**Fallback Summary:** `{result.fallback_summary_file}`")
    if result.generated_trace_file:
        lines.append(f"**Generated Trace:** `{result.generated_trace_file}`")
    if result.structured_fallback_summary:
        lines.extend(
            [
                "",
                "**Structured Fallback Summary:**",
                "```json",
                json.dumps(result.structured_fallback_summary, ensure_ascii=False, indent=2),
                "```",
            ]
        )
    lines.extend(
        [
            "",
            "**Checked Files:**",
            *[f"- `{path}`" for path in result.checked_files],
        ]
    )
    if result.missing_items:
        lines.extend(["", f"**Missing Items:** {', '.join(result.missing_items)}"])
    lines.extend(["", f"**Verdict:** {'PASS' if result.ok else 'BLOCKED'}"])
    if result.blocker:
        lines.extend(["", result.blocker])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change", required=True, help="Change id")
    parser.add_argument("--archive-path", type=Path, required=True, help="Archived Change directory")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--no-write-minimal-trace",
        action="store_true",
        help="Do not write trace.md; emit structured fallback when possible",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    archive_path = args.archive_path
    if not archive_path.is_absolute():
        archive_path = root / archive_path
    if not archive_path.is_dir():
        print(f"ERROR: archive path not found: {archive_path}", file=sys.stderr)
        return 2

    result = validate_archive_evidence(
        archive_path,
        root,
        change_id=args.change,
        write_minimal_trace=not args.no_write_minimal_trace,
    )
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
