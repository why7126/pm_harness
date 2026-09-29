#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


CHANGE_DOCS = {
    "proposal.md",
    "design.md",
    "tasks.md",
    "trace.md",
    "acceptance.md",
    "test-plan.md",
}

ENGLISH_SCAFFOLD_WORDS = {
    "bug analysis report",
    "capabilities",
    "context",
    "data and api",
    "documentation",
    "implementation",
    "impact",
    "knowledge base decision",
    "non-goals",
    "proposed design",
    "proposed fix",
    "risks",
    "rollback plan",
    "root cause",
    "test strategy",
    "testing",
    "validation",
    "what",
    "what changes",
    "why",
}

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
ALPHA_RE = re.compile(r"[A-Za-z]")
CHECKBOX_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def is_english_scaffold_heading(text: str) -> bool:
    title = strip_inline_code(text).strip().strip("#").strip()
    if has_cjk(title) or not ALPHA_RE.search(title):
        return False
    normalized = re.sub(r"[^a-zA-Z -]", "", title).strip().lower()
    return normalized in ENGLISH_SCAFFOLD_WORDS


def is_english_task(text: str) -> bool:
    if not CHECKBOX_RE.match(text):
        return False
    task_text = strip_inline_code(CHECKBOX_RE.sub("", text).strip())
    return bool(ALPHA_RE.search(task_text)) and not has_cjk(task_text)


def iter_change_docs(root: Path, include_archive: bool) -> list[Path]:
    paths: list[Path] = []
    change_root = root / "openspec" / "changes"
    if change_root.exists():
        for path in change_root.glob("*/*.md"):
            if path.name in CHANGE_DOCS:
                paths.append(path)

    if include_archive:
        archive_root = root / "openspec" / "archive"
        if archive_root.exists():
            for path in archive_root.glob("*/*.md"):
                if path.name in CHANGE_DOCS:
                    paths.append(path)

    return sorted(paths)


def validate_file(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    in_fence = False

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        heading = HEADING_RE.match(line)
        if heading and is_english_scaffold_heading(heading.group(1)):
            errors.append(
                f"{path.relative_to(root)}:{line_no}: OpenSpec 文档标题必须中文优先，避免英文脚手架标题：{stripped}"
            )
            continue

        if is_english_task(line):
            errors.append(
                f"{path.relative_to(root)}:{line_no}: tasks.md 任务项必须中文优先，命令/路径可保留英文：{stripped}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chinese-first OpenSpec change documents.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--include-archive", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    errors: list[str] = []
    for path in iter_change_docs(root, args.include_archive):
        errors.extend(validate_file(path, root))

    if errors:
        print("OpenSpec 文档语言校验失败：")
        for error in errors:
            print(f"- {error}")
        print("\n修复建议：标题和任务描述使用中文优先；OpenSpec 关键字、命令、路径、代码标识符可保留英文。")
        return 1

    print("OpenSpec 文档语言校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
