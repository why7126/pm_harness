#!/usr/bin/env python3
"""Validate product data collection and observability governance gates."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = "docs/standards/product-data-collection-observability.md"
DECLARATION = "product_data_collection_observability"

ENTRY_FILES = [
    "AGENTS.md",
    "rules/api.md",
    "rules/database.md",
    "rules/testing.md",
    "rules/document-governance.md",
    "rules/requirement-management.md",
    "rules/iterations-lifecycle.md",
]
SKILL_FILES = [
    ".agents/skills/req-generate/SKILL.md",
    ".agents/skills/req-complete/SKILL.md",
    ".agents/skills/req-review/SKILL.md",
    ".agents/skills/req-opsx/SKILL.md",
    ".agents/skills/opsx-propose/SKILL.md",
    ".agents/skills/opsx-apply/SKILL.md",
    ".agents/skills/opsx-modify/SKILL.md",
    ".agents/skills/opsx-archive/SKILL.md",
    ".agents/skills/sprint-propose/SKILL.md",
    ".agents/skills/sprint-apply/SKILL.md",
    ".agents/skills/sprint-archive/SKILL.md",
]
ENTRY_TERM_GROUPS = [
    [STANDARD],
    [DECLARATION],
    ["affected_layers", "适用层级"],
    ["reason", "原因"],
    ["validation", "验证", "验收"],
    ["N/A", "not_applicable", "不适用"],
]
PATH_TRIGGERS = [
    "src/backend/app/api/",
    "src/backend/app/schemas/",
    "src/backend/app/repositories/",
    "src/backend/app/services/",
    "src/backend/app/db/",
    "src/web/src/services/",
    "src/web/src/shared/api/",
    "src/miniapp/services/",
]
TEXT_TRIGGERS = [
    "API",
    "DB",
    "数据库",
    "日志审计",
    "行为埋点",
    "请求封装",
    "链路 ID",
    "Task Trace",
    "request_logs",
    "usage_events",
    "task_traces",
    "task_trace_spans",
    "behavior_trace_id",
    "behavior_event_id",
    "client_request_id",
    "request_id",
    "保留周期",
    "脱敏",
    "OpenAPI",
    "Orval",
]
BAD_NA_REASONS = {"无", "不涉及", "none", "n/a", "na", "N/A"}


class TargetScan:
    def __init__(self, label: str, files: list[Path], trigger_hits: list[str], text: str) -> None:
        self.label = label
        self.files = files
        self.trigger_hits = trigger_hits
        self.text = text


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.md") if "__pycache__" not in path.parts)


def validate_entry_files() -> list[str]:
    errors: list[str] = []
    checked = 0
    for item in ENTRY_FILES + SKILL_FILES:
        path = ROOT / item
        if not path.exists():
            continue
        checked += 1
        text = read(path)
        missing = ["/".join(group) for group in ENTRY_TERM_GROUPS if not any(term in text for term in group)]
        if missing:
            errors.append(f"{item}: 缺少采集规范门禁关键内容: {', '.join(missing)}")
    if checked == 0:
        errors.append("未找到可校验的入口或技能文件")
    return errors


def scan_target(label: str, files: list[Path]) -> TargetScan:
    chunks: list[str] = []
    trigger_hits: list[str] = []
    for path in sorted(set(files)):
        if not path.exists() or not path.is_file():
            continue
        relative = rel(path)
        path_hits = [trigger for trigger in PATH_TRIGGERS if trigger in relative]
        if path_hits:
            trigger_hits.append(f"{relative}:path:{'|'.join(path_hits)}")
        text = read(path)
        chunks.append(text)
        for trigger in TEXT_TRIGGERS:
            if trigger in text:
                trigger_hits.append(f"{relative}:text:{trigger}")
    return TargetScan(label=label, files=files, trigger_hits=sorted(set(trigger_hits)), text="\n".join(chunks))


def collect_change(change_id: str) -> TargetScan:
    return scan_target(f"change:{change_id}", markdown_files(ROOT / "openspec" / "changes" / change_id))


def collect_req(req_id: str) -> TargetScan:
    files: list[Path] = []
    for candidate in sorted((ROOT / "issues" / "requirements").glob(f"*/{req_id}*")):
        if candidate.is_dir():
            files.extend(markdown_files(candidate))
    return scan_target(f"req:{req_id}", files)


def collect_sprint(sprint_id: str) -> TargetScan:
    files: list[Path] = []
    for stage in ("change", "archive"):
        base = ROOT / "iterations" / stage / sprint_id
        if base.exists():
            files.extend(markdown_files(base))
            yaml_path = base / "sprint.yaml"
            if yaml_path.exists():
                files.append(yaml_path)
    return scan_target(f"sprint:{sprint_id}", files)


def collect_diff() -> TargetScan:
    result = subprocess.run(["git", "diff", "--name-only"], cwd=ROOT, text=True, capture_output=True, check=False)
    files: list[Path] = []
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            path = ROOT / line.strip()
            if path.exists() and path.is_file() and path.suffix in {".md", ".py", ".ts", ".tsx", ".js", ".json", ".yaml", ".yml"}:
                files.append(path)
    return scan_target("diff:working-tree", sorted(files))


def validate_target(scan: TargetScan) -> list[str]:
    errors: list[str] = []
    if not scan.files:
        errors.append(f"{scan.label}: 未找到可校验目标文件")
        return errors
    if not scan.trigger_hits:
        return errors
    if DECLARATION not in scan.text:
        errors.append(f"{scan.label}: 命中采集规范触发范围但缺少 `{DECLARATION}` 声明")
        return errors
    for term in ("affected_layers", "reason", "validation"):
        if term not in scan.text:
            errors.append(f"{scan.label}: `{DECLARATION}` 声明缺少 `{term}`")
    errors.extend(validate_na_reason(scan))
    return errors


def validate_na_reason(scan: TargetScan) -> list[str]:
    errors: list[str] = []
    lines = scan.text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if "status:" not in stripped or "not_applicable" not in stripped:
            continue
        reason = ""
        for follow in lines[index + 1:index + 8]:
            if follow.strip().startswith("reason:"):
                reason = follow.split(":", 1)[1].strip().strip("\"'")
                break
        if not reason or reason in BAD_NA_REASONS or len(reason) < 8:
            errors.append(f"{scan.label}: N/A 声明缺少可审计 reason")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change")
    parser.add_argument("--req")
    parser.add_argument("--sprint")
    parser.add_argument("--diff", action="store_true")
    args = parser.parse_args()

    errors = validate_entry_files()
    scans: list[TargetScan] = []
    if args.change:
        scans.append(collect_change(args.change))
    if args.req:
        scans.append(collect_req(args.req))
    if args.sprint:
        scans.append(collect_sprint(args.sprint))
    if args.diff:
        scans.append(collect_diff())
    for scan in scans:
        errors.extend(validate_target(scan))

    if errors:
        print("产品数据采集与链路观测门禁校验失败：")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("产品数据采集与链路观测门禁校验通过。")
    if scans:
        for scan in scans:
            print(f"- {scan.label}: files={len(scan.files)}, trigger_hits={len(scan.trigger_hits)}, declaration={'yes' if DECLARATION in scan.text else 'no'}")
    else:
        print("- focused_target: skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
