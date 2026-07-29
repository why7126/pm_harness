#!/usr/bin/env python3
"""Validate generated PM Harness docs do not leak template-only content."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_EXTENSIONS = {".md", ".yaml", ".yml"}

DEFAULT_EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}

TEMPLATE_ALLOWED_PARTS = {
    "issues",
}

PENDING_ALLOWED_FILES = {
    Path("docs/pending-decisions.md"),
    Path("issues/requirements/template/requirement.md"),
    Path("issues/requirements/template/trace.md"),
    Path("issues/bugs/template/bug.md"),
    Path("issues/bugs/template/trace.md"),
}

CRITICAL_NO_PENDING = {
    Path("AGENTS.md"),
    Path("README.md"),
    Path("project.yaml"),
    Path("openspec/config.yaml"),
}

TEMPLATE_MARKER_RE = re.compile(
    r"(\[(?:通用|个性化|条件启用)(?:\s*\+\s*(?:通用|个性化|条件启用))*\]|"
    r"【(?:通用|个性化|条件启用)】)"
)

TEMPLATE_SECTION_RE = re.compile(
    r"(模块标记说明|生成参数|初始化参数|初始化占位符|初始化生成建议|"
    r"生成与维护原则|AGENTS\.md 模块构成|模板模块构成)"
)

TEMPLATE_META_RE = re.compile(
    r"(template_scope|抽象模板|Token 优化模板|可作为工程初始化|"
    r"初始化时基于用户输入生成|初始化工具生成)"
)

YAML_PENDING_SCALAR_RE = re.compile(r":\s*[\"']?待确认(?:（[^\"']*）)?[\"']?\s*(?:#.*)?$")


@dataclass
class Finding:
    severity: str
    path: Path
    line: int
    message: str
    text: str


def iter_docs(root: Path) -> list[Path]:
    docs: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in DOC_EXTENSIONS:
            continue
        rel_parts = set(path.relative_to(root).parts)
        if rel_parts & DEFAULT_EXCLUDED_PARTS:
            continue
        docs.append(path)
    return sorted(docs)


def is_issue_template(rel: Path) -> bool:
    return len(rel.parts) >= 3 and rel.parts[0] == "issues" and "template" in rel.parts


def allow_pending(rel: Path) -> bool:
    return rel in PENDING_ALLOWED_FILES or is_issue_template(rel)


def scan_file(root: Path, path: Path) -> list[Finding]:
    rel = path.relative_to(root)
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="ignore")

    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if TEMPLATE_MARKER_RE.search(line) and not is_issue_template(rel):
            findings.append(Finding("error", rel, index, "交付文档残留模板模块标记", stripped))
        if TEMPLATE_SECTION_RE.search(line) and not is_issue_template(rel):
            findings.append(Finding("error", rel, index, "交付文档残留模板生成说明章节", stripped))
        if TEMPLATE_META_RE.search(line) and not is_issue_template(rel):
            findings.append(Finding("error", rel, index, "交付文档残留模板元信息", stripped))
        if "待确认" in line and rel in CRITICAL_NO_PENDING:
            findings.append(Finding("error", rel, index, "关键入口文件不得残留待确认", stripped))
        if path.suffix in {".yaml", ".yml"} and not stripped.startswith("#") and YAML_PENDING_SCALAR_RE.search(line):
            findings.append(Finding("error", rel, index, "YAML 配置不得使用待确认作为标量值", stripped))

    return findings


def count_pending(root: Path, docs: list[Path]) -> tuple[int, list[tuple[Path, int]]]:
    total = 0
    per_file: list[tuple[Path, int]] = []
    for path in docs:
        rel = path.relative_to(root)
        if allow_pending(rel):
            continue
        count = path.read_text(encoding="utf-8", errors="ignore").count("待确认")
        if count:
            total += count
            per_file.append((rel, count))
    return total, sorted(per_file, key=lambda item: item[1], reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT, help="Generated project root")
    parser.add_argument("--strict", action="store_true", help="Fail on excessive scattered pending items")
    parser.add_argument("--max-pending", type=int, default=20, help="Allowed scattered pending count outside pending-decisions and issue templates")
    args = parser.parse_args()

    root = args.root.resolve()
    docs = iter_docs(root)
    findings: list[Finding] = []
    for path in docs:
        findings.extend(scan_file(root, path))

    pending_total, pending_files = count_pending(root, docs)
    if args.strict and pending_total > args.max_pending:
        for rel, count in pending_files[:20]:
            findings.append(
                Finding(
                    "error",
                    rel,
                    0,
                    f"散落待确认过多：{count} 处；请删除低价值占位或集中到 docs/pending-decisions.md",
                    "",
                )
            )

    if findings:
        title = "生成文档质量校验失败：" if args.strict else "生成文档质量校验发现问题："
        print(title)
        for finding in findings:
            location = str(finding.path)
            if finding.line:
                location = f"{location}:{finding.line}"
            print(f"- [{finding.severity}] {location} {finding.message}")
            if finding.text:
                print(f"  {finding.text}")
        print(f"\n散落待确认总数：{pending_total}")
        if pending_files:
            print("待确认最多的文件：")
            for rel, count in pending_files[:10]:
                print(f"- {rel}: {count}")
        if args.strict:
            return 1
        print("\n当前为非严格模式，仅报告问题；打包交付前请使用 --strict。")
        return 0

    print("生成文档质量校验通过。")
    print(f"扫描文档：{len(docs)} 个；散落待确认：{pending_total} 个。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
