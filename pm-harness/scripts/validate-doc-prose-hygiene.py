#!/usr/bin/env python3
"""Lightweight prose hygiene scan for durable governance documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ("AGENTS.md", "docs", "rules", ".agents/skills")
SKIP_DIRS = {".git", "node_modules", "dist", "coverage", "__pycache__", "archive"}
PATTERNS = (
    ("session_reasoning", re.compile(r"(我先|我会先|接下来我|本轮先|然后我会)")),
    ("review_conversation", re.compile(r"(reviewer|review 要求|按评论|审阅者)", re.I)),
    ("temporary_draft", re.compile(r"(草案|临时稿|第\s*\d+\s*版|audit\s+[A-Z]?\d+)", re.I)),
    ("local_absolute_path", re.compile(r"/Users/[^\s)`\"']+")),
    ("secret_like", re.compile(r"(Authorization\s*:|Bearer\s+[A-Za-z0-9._-]+|DATABASE_URL\s*=|SECRET_KEY\s*=)", re.I)),
)


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".mdx"}:
            files.append(path)
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                if child.is_file() and child.suffix.lower() in {".md", ".mdx"}:
                    files.append(child)
    return sorted(set(files))


def scan_file(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        for code, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "line": lineno,
                        "code": code,
                        "excerpt": line.strip()[:160],
                    }
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files or directories to scan")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    targets = [ROOT / path for path in (args.paths or DEFAULT_TARGETS)]
    findings: list[dict[str, object]] = []
    for path in iter_markdown(targets):
        findings.extend(scan_file(path))
    payload = {"status": "pass" if not findings else "warning", "finding_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"doc prose hygiene {payload['status']}: {len(findings)} finding(s)")
        for finding in findings:
            print(f"- {finding['path']}:{finding['line']} [{finding['code']}] {finding['excerpt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
