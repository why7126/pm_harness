#!/usr/bin/env python3
"""Pre-push safety checks for ProjectPmHarness Git content."""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_FILE_SIZE_MB = 10
TEXT_READ_LIMIT_BYTES = 1024 * 1024

SAFE_PATH_PATTERNS = [
    ".env.example",
    "**/.env.example",
    "deploy/**/*.env.example",
    "scripts/*.env.example",
]

FORBIDDEN_PATH_PATTERNS = [
    ".env",
    ".env.*",
    "deploy/**/*.env",
    "scripts/*.env",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "data/runtime/**",
    "data/uploads/**",
    "data/tmp/**",
    "data/minio/**",
    "data/s3/**",
    "node_modules/**",
    "dist/**",
    "build/**",
    "coverage/**",
    ".pytest_cache/**",
    "__pycache__/**",
    "*.pyc",
    ".DS_Store",
    "*.zip",
]

BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tar", ".tgz", ".sqlite", ".sqlite3", ".db"}

PLACEHOLDERS = {
    "<access_token>",
    "<token>",
    "<secret>",
    "<password>",
    "<api_key>",
    "change-me",
    "change-me-in-local-env",
    "example",
    "example.com",
    "localhost",
    "127.0.0.1",
}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("authorization-header", re.compile(r"\bAuthorization\s*:\s*Bearer\s+([A-Za-z0-9._~+/=-]{16,})", re.I), "error"),
    ("cookie-header", re.compile(r"\bCookie\s*:\s*([^;\s=]+=[^;\s]{12,})", re.I), "error"),
    ("assigned-secret", re.compile(r"\b(api[_-]?key|access[_-]?key|secret[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']([^\"']{12,})[\"']", re.I), "error"),
    ("database-url", re.compile(r"\b(?:mysql|postgresql|postgres):\/\/[^\s\"']{12,}", re.I), "error"),
    ("local-absolute-path", re.compile(r"(?:/Users/[^/\s]+|/home/[^/\s]+|C:\\\\Users\\\\[^\\\\\s]+)"), "error"),
]

SAFE_LITERAL_SNIPPETS = [
    "/home/claude/output",
    "/mnt/user-data/outputs",
    're.compile(r"/Users/',
    're.compile(r"(/Users/',
    'ABS_PATH_RE = re.compile',
    're.search(r"/Users/',
]


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    path: str
    line: int | None
    message: str
    snippet: str | None = None


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def path_matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatch(path, pattern)


def is_forbidden_path(path: str) -> str | None:
    if any(path_matches(path, pattern) for pattern in SAFE_PATH_PATTERNS):
        return None
    for pattern in FORBIDDEN_PATH_PATTERNS:
        if path_matches(path, pattern):
            return pattern
    return None


def collect_files(scan_all: bool) -> tuple[str, set[str]]:
    if scan_all:
        files = set()
        for path in ROOT.rglob("*"):
            if path.is_file():
                rel = path.relative_to(ROOT).as_posix()
                if not rel.startswith(".git/") and "/.git/" not in rel:
                    files.add(rel)
        return "all", files
    staged = set(run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"]))
    tracked = set(run_git(["ls-files"]))
    return "staged+tracked", staged | tracked


def redact(value: str) -> str:
    text = re.sub(r"/Users/[^/\s]+", "<user-home>", value)
    text = re.sub(r"/home/[^/\s]+", "<user-home>", text)
    text = re.sub(r"C:\\\\Users\\\\[^\\\\\s]+", "<user-home>", text)
    if len(text) > 120:
        text = f"{text[:80]}..."
    return text


def is_placeholder(value: str) -> bool:
    normalized = value.strip().strip("\"'").lower()
    return normalized in PLACEHOLDERS or normalized.startswith("<") and normalized.endswith(">")


def is_safe_literal_line(line: str) -> bool:
    return any(snippet in line for snippet in SAFE_LITERAL_SNIPPETS)


def scan_paths(paths: set[str], max_file_size_mb: int) -> list[Finding]:
    findings: list[Finding] = []
    max_bytes = max_file_size_mb * 1024 * 1024
    for path in sorted(paths):
        forbidden = is_forbidden_path(path)
        if forbidden:
            findings.append(Finding("error", "forbidden-path", path, None, f"路径匹配禁止提交规则: {forbidden}"))
        full = ROOT / path
        if full.exists() and full.is_file():
            size = full.stat().st_size
            if size > max_bytes:
                severity = "error" if full.suffix.lower() in BINARY_EXTENSIONS else "warning"
                findings.append(Finding(severity, "large-file", path, None, f"文件超过阈值 {max_file_size_mb}MB"))
    return findings


def should_scan_text(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return suffix not in BINARY_EXTENSIONS


def scan_content(paths: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(paths):
        full = ROOT / path
        if not full.exists() or not full.is_file() or not should_scan_text(path):
            continue
        try:
            raw = full.read_bytes()[:TEXT_READ_LIMIT_BYTES]
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_safe_literal_line(line):
                continue
            for rule, pattern, severity in SECRET_PATTERNS:
                match = pattern.search(line)
                if not match:
                    continue
                candidate = match.group(match.lastindex or 0)
                if is_placeholder(candidate):
                    continue
                findings.append(Finding(severity, rule, path, lineno, "疑似敏感内容或本机路径", redact(line.strip())))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="scan all files under the repository")
    parser.add_argument("--max-file-size-mb", type=int, default=DEFAULT_MAX_FILE_SIZE_MB)
    args = parser.parse_args()

    scope, files = collect_files(args.all)
    findings = scan_paths(files, args.max_file_size_mb) + scan_content(files)
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    print(f"Git safety check scope: {scope}")
    print(f"Scanned files: {len(files)}")
    print(f"Errors: {len(errors)}")
    for item in errors:
        loc = f"{item.path}:{item.line}" if item.line else item.path
        print(f"- [error] {item.rule} {loc} - {item.message}")
        if item.snippet:
            print(f"  snippet: {item.snippet}")
    print(f"Warnings: {len(warnings)}")
    for item in warnings:
        loc = f"{item.path}:{item.line}" if item.line else item.path
        print(f"- [warning] {item.rule} {loc} - {item.message}")
    if errors:
        print("Suggestion: remove secrets/runtime artifacts from Git tracking or replace them with safe examples.")
        return 1
    print("Git safety check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
