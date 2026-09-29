"""Shared archived OpenSpec Change evidence checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


FALLBACK_SUMMARY_FILES = ("proposal.md", "design.md", "tasks.md")
FALLBACK_SUMMARY_REQUIREMENTS = {
    "validation": ("验证命令", "验证结果", "测试命令", "test", "pytest", "validate"),
    "acceptance": ("验收结论", "验收结果", "acceptance", "verdict"),
    "issue_or_sprint_status": ("Issue", "Sprint", "REQ-", "BUG-", "状态"),
    "archive_evidence": ("归档路径", "归档时间", "openspec/archive", "archive"),
}


@dataclass(frozen=True)
class ArchiveEvidenceResult:
    change_id: str
    archive_path: str
    status: str
    trace_exists: bool
    checked_files: list[str]
    fallback_summary_file: str | None = None
    missing_items: list[str] | None = None
    blocker: str | None = None
    generated_trace_file: str | None = None
    structured_fallback_summary: dict[str, object] | None = None

    @property
    def ok(self) -> bool:
        return self.blocker is None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def extract_archive_summary(text: str) -> str | None:
    match = re.search(r"^## 归档验证摘要\s*\n(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def missing_fallback_summary_items(summary: str) -> list[str]:
    missing: list[str] = []
    lowered = summary.lower()
    for key, terms in FALLBACK_SUMMARY_REQUIREMENTS.items():
        if not any(term.lower() in lowered for term in terms):
            missing.append(key)
    return missing


def parse_task_counts(path: Path) -> tuple[int, int] | None:
    if not path.exists():
        return None
    text = read_text(path)
    done = len(re.findall(r"^- \[x\]", text, re.MULTILINE))
    total = len(re.findall(r"^- \[[ x]\]", text, re.MULTILINE))
    return done, total


def spec_delta_paths(change_dir: Path, root: Path) -> list[str]:
    specs_dir = change_dir / "specs"
    if not specs_dir.exists():
        return []
    return [rel(path, root) for path in sorted(specs_dir.rglob("*.md"))]


def archive_dir_date(change_dir: Path) -> str | None:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-", change_dir.name)
    return match.group(1) if match else None


def current_timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")


def build_structured_fallback_summary(
    change_dir: Path,
    root: Path,
    *,
    change_id: str,
    archive_path: str,
    evidence_status: str,
    warnings: list[str] | None = None,
) -> tuple[dict[str, object] | None, list[str]]:
    missing: list[str] = []
    tasks = parse_task_counts(change_dir / "tasks.md")
    if tasks is None:
        missing.append("tasks")
        tasks_done = 0
        tasks_total = 0
    else:
        tasks_done, tasks_total = tasks
        if tasks_total == 0:
            missing.append("tasks")
        elif tasks_done < tasks_total:
            missing.append("tasks_complete")

    archive_date = archive_dir_date(change_dir)
    archive_timestamp = "unknown"
    timestamp_source = "unknown"
    if archive_date:
        timestamp_source = "archive_dir_date"
        archive_timestamp = archive_date

    specs = spec_delta_paths(change_dir, root)

    summary: dict[str, object] = {
        "change_id": change_id,
        "archive_path": archive_path,
        "evidence_status": evidence_status,
        "archive_timestamp": archive_timestamp,
        "timestamp_source": timestamp_source,
        "tasks_done": tasks_done,
        "tasks_total": tasks_total,
        "spec_delta_paths": specs,
        "warnings": warnings or [],
        "recommended_action": None,
    }
    if missing:
        summary["recommended_action"] = "补齐 tasks.md 完成状态或手工补充归档证据后重跑校验。"
    return (None if missing else summary), missing


def render_minimal_trace(summary: dict[str, object]) -> str:
    now = current_timestamp()
    specs = summary.get("spec_delta_paths") or []
    spec_lines = "\n".join(f"  - {path}" for path in specs) if specs else "  - none"
    warnings = summary.get("warnings") or []
    warning_lines = "\n".join(f"  - {item}" for item in warnings) if warnings else "  - none"
    return f"""---
change_id: {summary["change_id"]}
status: archived
created_at: {now}
updated_at: {now}
source: auto_generated_minimal_archive_trace
archive_path: {summary["archive_path"]}
archive_timestamp: {summary["archive_timestamp"]}
timestamp_source: {summary["timestamp_source"]}
---

# {summary["change_id"]} Trace

```yaml
change_id: {summary["change_id"]}
status: archived
archive_path: {summary["archive_path"]}
archive_timestamp: {summary["archive_timestamp"]}
timestamp_source: {summary["timestamp_source"]}
source: auto_generated_minimal_archive_trace
tasks:
  done: {summary["tasks_done"]}
  total: {summary["tasks_total"]}
spec_delta_paths:
{spec_lines}
warnings:
{warning_lines}
```

## 归档验证摘要

- 证据状态：自动生成最小归档 trace。
- 归档路径：`{summary["archive_path"]}`。
- 归档时间来源：`{summary["timestamp_source"]}`，值：`{summary["archive_timestamp"]}`。
- 任务完成摘要：{summary["tasks_done"]}/{summary["tasks_total"]}。
- 说明：本文件由归档证据校验自动补齐，只记录可从归档目录和现有文件推断的最小事实，不代表额外人工验收结论。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| {now} | validate-archive-evidence | 自动生成最小归档 trace。 |
"""


def validate_archive_evidence(
    change_dir: Path,
    root: Path,
    *,
    change_id: str | None = None,
    write_minimal_trace: bool = True,
) -> ArchiveEvidenceResult:
    resolved_root = root.resolve()
    resolved_change_dir = change_dir.resolve()
    checked_files = [rel(resolved_change_dir / name, resolved_root) for name in FALLBACK_SUMMARY_FILES]
    resolved_change_id = change_id or resolved_change_dir.name.split("-", 3)[-1]
    archive_path = rel(resolved_change_dir, resolved_root)

    if (resolved_change_dir / "trace.md").exists():
        return ArchiveEvidenceResult(
            change_id=resolved_change_id,
            archive_path=archive_path,
            status="trace-present",
            trace_exists=True,
            checked_files=checked_files,
            missing_items=[],
        )

    structured_summary, structured_missing = build_structured_fallback_summary(
        resolved_change_dir,
        resolved_root,
        change_id=resolved_change_id,
        archive_path=archive_path,
        evidence_status="structured-fallback-summary",
    )

    if structured_summary is not None and write_minimal_trace:
        trace_path = resolved_change_dir / "trace.md"
        try:
            trace_path.write_text(render_minimal_trace(structured_summary), encoding="utf-8")
        except OSError as exc:
            structured_summary = {
                **structured_summary,
                "warnings": [
                    *list(structured_summary.get("warnings") or []),
                    f"trace_write_failed: {exc.__class__.__name__}",
                ],
                "recommended_action": "归档目录不可写；请保留结构化 fallback 摘要或修复权限后重跑校验。",
            }
        else:
            return ArchiveEvidenceResult(
                change_id=resolved_change_id,
                archive_path=archive_path,
                status="auto-generated-minimal-trace",
                trace_exists=True,
                checked_files=checked_files,
                missing_items=[],
                generated_trace_file=rel(trace_path, resolved_root),
                structured_fallback_summary=structured_summary,
            )

    if structured_summary is not None:
        return ArchiveEvidenceResult(
            change_id=resolved_change_id,
            archive_path=archive_path,
            status="fallback-summary-pass",
            trace_exists=False,
            checked_files=checked_files,
            missing_items=[],
            structured_fallback_summary=structured_summary,
        )

    best_missing = list(FALLBACK_SUMMARY_REQUIREMENTS)
    for name in FALLBACK_SUMMARY_FILES:
        path = resolved_change_dir / name
        if not path.exists():
            continue
        summary = extract_archive_summary(read_text(path))
        if summary is None:
            continue
        missing = missing_fallback_summary_items(summary)
        if not missing:
            return ArchiveEvidenceResult(
                change_id=resolved_change_id,
                archive_path=archive_path,
                status="fallback-summary-pass",
                trace_exists=False,
                checked_files=checked_files,
                fallback_summary_file=rel(path, resolved_root),
                missing_items=[],
            )
        if len(missing) < len(best_missing):
            best_missing = missing

    if structured_missing and len(structured_missing) < len(best_missing):
        best_missing = structured_missing

    blocker = (
        "archived change missing trace.md and complete fallback summary "
        f"(change: {resolved_change_id}; archive: {archive_path}; "
        f"checked: {', '.join(checked_files)}; missing: {', '.join(best_missing)})"
    )
    return ArchiveEvidenceResult(
        change_id=resolved_change_id,
        archive_path=archive_path,
        status="missing",
        trace_exists=False,
        checked_files=checked_files,
        missing_items=best_missing,
        blocker=blocker,
    )
