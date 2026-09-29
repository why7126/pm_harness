from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from workflow_sync import collect
from workflow_sync.derive import derive_change_state, derive_issue


ROOT = Path(__file__).resolve().parents[1]
SPRINT_FILES = ("sprint.yaml", "sprint.md", "release-note.md", "acceptance-report.md")
CLOSED_CHANGE_STATES = frozenset({"applied", "archived"})
ARCHIVED_CHANGE_STATE = "archived"
LEGACY_ARCHIVE_PATH = "openspec/changes/archive/"


@dataclass(frozen=True)
class StaleHit:
    severity: str
    kind: str
    target: str
    file: str
    line: int
    context: str
    reason: str
    suggestion: str


@dataclass(frozen=True)
class SprintCloseStaleReport:
    sprint_id: str
    sprint_path: str
    checked_files: int
    blocker_count: int
    warning_count: int
    allowed_legacy_count: int
    hits: list[StaleHit]

    @property
    def ok(self) -> bool:
        return self.blocker_count == 0


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _with_collect_root(root: Path, fn, *args):
    previous_root = collect.ROOT
    collect.ROOT = root
    try:
        return fn(*args)
    finally:
        collect.ROOT = previous_root


def load_sprint_record(root: Path, sprint_id: str) -> collect.SprintRecord:
    sprint = _with_collect_root(root, collect.load_sprint, sprint_id)
    if sprint is None:
        raise FileNotFoundError(f"sprint.yaml not found for: {sprint_id}")
    return sprint


def resolve_auto_sprint(root: Path) -> str:
    sprint_ids = _with_collect_root(root, collect.list_sprint_ids)
    in_progress = [
        sprint_id
        for sprint_id in sprint_ids
        if (record := _with_collect_root(root, collect.load_sprint, sprint_id))
        and record.status == "in_progress"
    ]
    if len(in_progress) == 1:
        return in_progress[0]
    if not in_progress:
        raise ValueError("cannot resolve --sprint auto: no in_progress sprint; pass --sprint sprint-xxx")
    raise ValueError(
        "cannot resolve --sprint auto: multiple in_progress sprints "
        f"({', '.join(in_progress)}); pass --sprint sprint-xxx"
    )


def load_issues(root: Path) -> dict[str, collect.IssueRecord]:
    return _with_collect_root(root, collect.load_all_issues)


def load_change_records(
    root: Path,
    sprint: collect.SprintRecord,
    issues: dict[str, collect.IssueRecord],
) -> dict[str, Any]:
    openspec_data = _with_collect_root(root, collect.run_openspec_list)
    records: dict[str, Any] = {}
    for change_id in sprint.changes:
        records[change_id] = _with_collect_root(
            root,
            collect.load_change_record,
            change_id,
            issues,
            openspec_data,
        )
    return records


def sprint_files(sprint: collect.SprintRecord) -> list[Path]:
    return sorted(path for name in SPRINT_FILES if (path := sprint.path / name).exists())


def issue_files(sprint: collect.SprintRecord, issues: dict[str, collect.IssueRecord]) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for issue_id in [*sprint.requirements, *sprint.bugs]:
        issue = issues.get(issue_id)
        if not issue or not issue.path.is_dir():
            continue
        for path in sorted(issue.path.glob("*.md")):
            files.append((issue_id, path))
    return files


def _line_has_legacy_archive_path(line: str) -> bool:
    return LEGACY_ARCHIVE_PATH in line


def _line_mentions_target(line: str, target: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_-]){re.escape(target)}(?![A-Za-z0-9_-])", line) is not None


def _line_has_wait_opsx(line: str, command: str) -> bool:
    command_text = re.escape(command)
    return re.search(rf"待\s*`?/{command_text}`?", line) is not None


def _line_has_apply_wait(line: str) -> bool:
    return _line_has_wait_opsx(line, "opsx-apply") or re.search(r"待.*(?:开发|实现)", line) is not None


def _line_has_archive_wait(line: str) -> bool:
    return _line_has_wait_opsx(line, "opsx-archive") or re.search(r"待\s*archive", line, re.IGNORECASE) is not None


def _line_has_stale_state_word(line: str) -> bool:
    return re.search(r"(?<![A-Za-z0-9_-])(?:proposed|applied)(?![A-Za-z0-9_-])", line) is not None


def _line_has_issue_intermediate_word(line: str) -> bool:
    return re.search(
        r"(?<![A-Za-z0-9_-])(?:planned|pending|proposed|applied|in_sprint|待验收|待实现|待归档)(?![A-Za-z0-9_-])",
        line,
        re.IGNORECASE,
    ) is not None


def _manual_fix_suggestion(sprint_id: str) -> str:
    return (
        f"先运行 `python scripts/sync-workflow-status.py --event sprint.archive --sprint {sprint_id} --dry-run` "
        "或对应 Workflow Sync/reconcile；若命中位于人工说明区，手工修正文案。"
        "禁止手工编辑 `sprint.md` workflow-sync marker 派生块。"
    )


def scan_line(
    *,
    line: str,
    line_no: int,
    file_path: Path,
    root: Path,
    sprint: collect.SprintRecord,
    issues: dict[str, collect.IssueRecord],
    derived_issues: dict[str, Any],
    derived_changes: dict[str, Any],
) -> list[StaleHit]:
    hits: list[StaleHit] = []
    context = line.strip()
    file_rel = rel(file_path, root)

    if _line_has_legacy_archive_path(line):
        hits.append(
            StaleHit(
                severity="blocker",
                kind="legacy-change-archive-path",
                target=sprint.sprint_id,
                file=file_rel,
                line=line_no,
                context=context,
                reason="Sprint 四件套不得将 openspec/changes/archive/ 作为 canonical archive path。",
                suggestion="改用 `openspec/archive/YYYY-MM-DD-<change-id>/`，然后重跑 stale scan。",
            )
        )

    for issue_id in [*sprint.requirements, *sprint.bugs]:
        derived = derived_issues.get(issue_id)
        linked_change = derived.linked_change if derived else None
        if not linked_change or not _line_mentions_target(line, issue_id):
            continue
        if issues.get(issue_id, None) and issues[issue_id].kind == "req" and _line_has_wait_opsx(line, "req-opsx"):
            hits.append(
                StaleHit(
                    severity="blocker",
                    kind="stale-issue-open-change",
                    target=issue_id,
                    file=file_rel,
                    line=line_no,
                    context=context,
                    reason=f"{issue_id} 已关联 Change `{linked_change}`，不应继续提示待 `/req-opsx`。",
                    suggestion=_manual_fix_suggestion(sprint.sprint_id),
                )
            )
        if issues.get(issue_id, None) and issues[issue_id].kind == "bug" and _line_has_wait_opsx(line, "bug-opsx"):
            hits.append(
                StaleHit(
                    severity="blocker",
                    kind="stale-issue-open-change",
                    target=issue_id,
                    file=file_rel,
                    line=line_no,
                    context=context,
                    reason=f"{issue_id} 已关联 Change `{linked_change}`，不应继续提示待 `/bug-opsx`。",
                    suggestion=_manual_fix_suggestion(sprint.sprint_id),
                )
            )

    for change_id, change in derived_changes.items():
        if not _line_mentions_target(line, change_id):
            continue
        if change.state in CLOSED_CHANGE_STATES and _line_has_apply_wait(line):
            hits.append(
                StaleHit(
                    severity="blocker",
                    kind="stale-change-apply",
                    target=change_id,
                    file=file_rel,
                    line=line_no,
                    context=context,
                    reason=f"Change `{change_id}` 当前为 {change.state}，不应继续提示待 `/opsx-apply` 或待实现。",
                    suggestion=_manual_fix_suggestion(sprint.sprint_id),
                )
            )
        if change.state == ARCHIVED_CHANGE_STATE and (_line_has_archive_wait(line) or _line_has_stale_state_word(line)):
            hits.append(
                StaleHit(
                    severity="blocker",
                    kind="stale-change-archived",
                    target=change_id,
                    file=file_rel,
                    line=line_no,
                    context=context,
                    reason=f"Change `{change_id}` 已 archived，不应继续显示 proposed/applied 或待 archive 语义。",
                    suggestion=_manual_fix_suggestion(sprint.sprint_id),
                )
            )

    return hits


def scan_issue_line(
    *,
    issue_id: str,
    line: str,
    line_no: int,
    file_path: Path,
    root: Path,
    derived_issues: dict[str, Any],
    derived_changes: dict[str, Any],
) -> list[StaleHit]:
    hits: list[StaleHit] = []
    derived = derived_issues.get(issue_id)
    if not derived or derived.display_status != "done":
        return hits
    linked_change = derived.linked_change
    change = derived_changes.get(linked_change) if linked_change else None
    if not change or change.state != ARCHIVED_CHANGE_STATE:
        return hits

    context = line.strip()
    file_rel = rel(file_path, root)
    if _line_has_issue_intermediate_word(line):
        hits.append(
            StaleHit(
                severity="blocker",
                kind="issue-subdocument-stale-state",
                target=issue_id,
                file=file_rel,
                line=line_no,
                context=context,
                reason=f"{issue_id} 已 done 且 Change `{linked_change}` 已 archived，不应继续保留中间态文案。",
                suggestion="先运行 Workflow Sync/reconcile 回填 Issue 子文档状态和验收结果；若为人工说明区，记录明确豁免语义。",
            )
        )
    if linked_change and f"openspec/changes/{linked_change}" in line:
        hits.append(
            StaleHit(
                severity="blocker",
                kind="issue-subdocument-active-change-path",
                target=issue_id,
                file=file_rel,
                line=line_no,
                context=context,
                reason=f"Change `{linked_change}` 已 archived，Issue 子文档不应继续引用 active change 路径。",
                suggestion="改用 `openspec/archive/YYYY-MM-DD-<change-id>/` 或归档 trace 证据路径。",
            )
        )
    return hits


def build_report(sprint_id: str, *, root: Path = ROOT) -> SprintCloseStaleReport:
    root = root.resolve()
    if sprint_id == "auto":
        sprint_id = resolve_auto_sprint(root)
    sprint = load_sprint_record(root, sprint_id)
    issues = load_issues(root)
    change_records = load_change_records(root, sprint, issues)
    derived_changes = {
        change_id: derive_change_state(record) for change_id, record in change_records.items()
    }
    derived_issues = {
        issue_id: derive_issue(issue, derived_changes, sprint)
        for issue_id, issue in issues.items()
        if issue_id in sprint.requirements or issue_id in sprint.bugs
    }
    files = sprint_files(sprint)
    scoped_issue_files = issue_files(sprint, issues)

    hits: list[StaleHit] = []
    legacy_dir = root / "openspec" / "changes" / "archive"
    if legacy_dir.exists():
        hits.append(
            StaleHit(
                severity="blocker",
                kind="legacy-change-archive-directory",
                target=sprint.sprint_id,
                file=rel(legacy_dir, root),
                line=0,
                context=rel(legacy_dir, root),
                reason="真实 legacy archive 目录不得存在。",
                suggestion="迁移其子目录到 `openspec/archive/`，删除空 legacy 目录，并运行 `python scripts/validate-directory-structure.py`。",
            )
        )

    for path in files:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            hits.extend(
                scan_line(
                    line=line,
                    line_no=line_no,
                    file_path=path,
                    root=root,
                    sprint=sprint,
                    issues=issues,
                    derived_issues=derived_issues,
                    derived_changes=derived_changes,
                )
            )
    for issue_id, path in scoped_issue_files:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            hits.extend(
                scan_issue_line(
                    issue_id=issue_id,
                    line=line,
                    line_no=line_no,
                    file_path=path,
                    root=root,
                    derived_issues=derived_issues,
                    derived_changes=derived_changes,
                )
            )

    return SprintCloseStaleReport(
        sprint_id=sprint.sprint_id,
        sprint_path=rel(sprint.path, root),
        checked_files=len(files) + len(scoped_issue_files),
        blocker_count=sum(1 for hit in hits if hit.severity == "blocker"),
        warning_count=sum(1 for hit in hits if hit.severity == "warning"),
        allowed_legacy_count=sum(1 for hit in hits if hit.severity == "allowed_legacy"),
        hits=hits,
    )


def report_to_dict(report: SprintCloseStaleReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["ok"] = report.ok
    return payload


def render_markdown(report: SprintCloseStaleReport) -> str:
    lines = [
        "## Sprint Close Stale Scan Report",
        "",
        f"**Sprint:** {report.sprint_id}",
        f"**Sprint Path:** `{report.sprint_path}`",
        f"**Checked Files:** {report.checked_files}",
        f"**Blockers:** {report.blocker_count}",
        f"**Warnings:** {report.warning_count}",
        f"**Allowed Legacy:** {report.allowed_legacy_count}",
        f"**Verdict:** {'PASS' if report.ok else 'BLOCKED'}",
    ]
    if report.hits:
        lines.extend(
            [
                "",
                "| Severity | Kind | Target | File | Line | Reason | Suggestion |",
                "|---|---|---|---|---:|---|---|",
            ]
        )
        for hit in report.hits:
            lines.append(
                f"| {hit.severity} | {hit.kind} | `{hit.target}` | `{hit.file}` | {hit.line} | "
                f"{hit.reason} | {hit.suggestion} |"
            )
        lines.extend(
            [
                "",
                "Fix the stale Sprint close facts above, then rerun:",
                f"`python scripts/check-sprint-close-stale-scan.py --sprint {report.sprint_id}`",
            ]
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Sprint close four-piece for stale intermediate wording.")
    parser.add_argument("--sprint", required=True, help="Sprint id, e.g. sprint-005, or auto")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_report(args.sprint, root=args.root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", flush=True)
        return 2
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
