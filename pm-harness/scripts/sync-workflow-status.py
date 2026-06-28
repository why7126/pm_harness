#!/usr/bin/env python3
"""Synchronize workflow status across OpenSpec, issues, and sprint docs.

This script intentionally starts conservative: it updates machine-maintained
marker blocks and safe OpenSpec status references, and reports drift where the
current document shape is not safe to rewrite automatically.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SYNC_MARKERS = {
    "sprint_goals": (
        "<!-- workflow-sync:sprint-goals:start -->",
        "<!-- workflow-sync:sprint-goals:end -->",
    ),
    "scope_changes": (
        "<!-- workflow-sync:scope-changes:start -->",
        "<!-- workflow-sync:scope-changes:end -->",
    ),
    "scope_requirements": (
        "<!-- workflow-sync:scope-requirements:start -->",
        "<!-- workflow-sync:scope-requirements:end -->",
    ),
    "scope_bugs": (
        "<!-- workflow-sync:scope-bugs:start -->",
        "<!-- workflow-sync:scope-bugs:end -->",
    ),
    "acceptance_tasks": (
        "<!-- workflow-sync:openspec-tasks:start -->",
        "<!-- workflow-sync:openspec-tasks:end -->",
    ),
    "release_changes": (
        "<!-- workflow-sync:release-changes:start -->",
        "<!-- workflow-sync:release-changes:end -->",
    ),
    "milestones": (
        "<!-- workflow-sync:milestones:start -->",
        "<!-- workflow-sync:milestones:end -->",
    ),
}


DATETIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class SprintItem:
    item_id: str
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class SprintMilestone:
    milestone_id: str
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class ChangeState:
    change_id: str
    status: str
    path: str
    tasks_done: int = 0
    tasks_total: int = 0


@dataclass
class SprintState:
    sprint_id: str
    path: Path
    status: str = "unknown"
    requirements: list[SprintItem] = field(default_factory=list)
    bugs: list[SprintItem] = field(default_factory=list)
    changes: list[SprintItem] = field(default_factory=list)
    milestones: list[SprintMilestone] = field(default_factory=list)

    @property
    def requirement_ids(self) -> list[str]:
        return [item.item_id for item in self.requirements]

    @property
    def bug_ids(self) -> list[str]:
        return [item.item_id for item in self.bugs]

    @property
    def change_ids(self) -> list[str]:
        return [item.item_id for item in self.changes]


@dataclass
class Patch:
    path: Path
    before: str
    after: str
    reason: str


@dataclass
class Report:
    updated: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    drift: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", default="manual.sync")
    parser.add_argument("--sprint", help="Sprint id, path name, or auto")
    parser.add_argument("--req", action="append", default=[])
    parser.add_argument("--bug", action="append", default=[])
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--check", action="store_true", help="Fail if changes would be made")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing")
    return parser.parse_args()


def find_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "openspec").exists() and (path / "issues").exists():
            return path
    return start


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def scalar_from_yaml_line(line: str) -> str:
    value = line.split(":", 1)[1].strip()
    return value.strip("'\"")


def parse_yaml_item_list(lines: list[str], key: str) -> list[SprintItem]:
    values: list[SprintItem] = []
    in_list = False
    key_indent = 0
    current_fields: dict[str, str] | None = None

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if re.match(rf"^{re.escape(key)}\s*:", stripped):
            in_list = True
            key_indent = indent
            inline = stripped.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                raw_items = inline[1:-1].strip()
                if raw_items:
                    values.extend(
                        SprintItem(item.strip().strip("'\""))
                        for item in raw_items.split(",")
                        if item.strip()
                    )
            continue
        if in_list and indent <= key_indent and not stripped.startswith("-"):
            break
        if not in_list:
            continue
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            current_fields = None
            if not item:
                continue
            if ":" in item:
                item_key, item_value = item.split(":", 1)
                current_fields = {item_key.strip(): item_value.strip().strip("'\"")}
                item_id = current_fields.get("id") or current_fields.get(f"{key[:-1]}_id") or current_fields.get("change_id")
                values.append(SprintItem(item_id or "", current_fields))
            else:
                values.append(SprintItem(item.strip("'\"")))
        elif current_fields is not None and ":" in stripped:
            item_key, item_value = stripped.split(":", 1)
            current_fields[item_key.strip()] = item_value.strip().strip("'\"")
            if values[-1].item_id == "":
                item_id = (
                    current_fields.get("id")
                    or current_fields.get(f"{key[:-1]}_id")
                    or current_fields.get("change_id")
                    or ""
                )
                values[-1].item_id = item_id
    return [value for value in values if value.item_id]


def parse_yaml_milestones(lines: list[str]) -> list[SprintMilestone]:
    return [
        SprintMilestone(item.item_id, item.fields)
        for item in parse_yaml_item_list(lines, "milestones")
    ]


def item_value(item, keys: list[str], default: str = "待确认") -> str:
    for key in keys:
        value = item.fields.get(key)
        if value:
            return value
    return default


def full_datetime_or_unknown(value: str) -> str:
    if value == "待确认":
        return value
    if DATETIME_PATTERN.match(value):
        return value
    if DATE_ONLY_PATTERN.match(value):
        return "待确认"
    return value


def parse_sprint_yaml(path: Path) -> SprintState:
    lines = read_text(path).splitlines()
    sprint_id = path.parent.name
    status = "unknown"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("sprint_id:"):
            sprint_id = scalar_from_yaml_line(stripped)
        elif stripped.startswith("status:"):
            status = scalar_from_yaml_line(stripped)
    return SprintState(
        sprint_id=sprint_id,
        path=path.parent,
        status=status,
        requirements=parse_yaml_item_list(lines, "requirements"),
        bugs=parse_yaml_item_list(lines, "bugs"),
        changes=parse_yaml_item_list(lines, "changes"),
        milestones=parse_yaml_milestones(lines),
    )


def all_sprints(root: Path) -> list[SprintState]:
    return [
        parse_sprint_yaml(path)
        for path in sorted((root / "iterations").glob("**/sprint.yaml"))
    ]


def id_matches(needle: str, haystack: str) -> bool:
    return haystack == needle or haystack.startswith(f"{needle}-")


def any_id_matches(needles: Iterable[str], haystack_values: Iterable[str]) -> bool:
    return any(id_matches(needle, haystack) for needle in needles for haystack in haystack_values)


def any_exact_matches(needles: Iterable[str], haystack_values: Iterable[str]) -> bool:
    return bool(set(needles).intersection(haystack_values))


def active_sprint(sprints: list[SprintState]) -> SprintState | None:
    active = [sprint for sprint in sprints if sprint.status == "in_progress"]
    if len(active) == 1:
        return active[0]
    if len(active) > 1:
        raise SystemExit("Multiple in_progress sprints found; pass --sprint explicitly.")
    return None


def resolve_sprint(root: Path, args: argparse.Namespace) -> SprintState | None:
    sprints = all_sprints(root)
    event = args.event or ""

    if event.startswith("bug.") and args.bug:
        for sprint in sprints:
            if any_id_matches(args.bug, sprint.bug_ids):
                return sprint
        return None

    if event.startswith("req.") and args.req:
        for sprint in sprints:
            if any_id_matches(args.req, sprint.requirement_ids):
                return sprint
        return None

    if event.startswith("opsx.") and args.change:
        for sprint in sprints:
            if any_exact_matches(args.change, sprint.change_ids):
                return sprint
        return None

    if args.sprint and args.sprint != "auto":
        for sprint in sprints:
            if sprint.sprint_id == args.sprint or sprint.path.name == args.sprint:
                return sprint
        raise SystemExit(f"Unknown sprint: {args.sprint}")

    if args.sprint == "auto" or event.startswith("sprint.") or not [*args.req, *args.bug, *args.change]:
        return active_sprint(sprints)

    for sprint in sprints:
        if (
            any_id_matches([*args.req, *args.bug], sprint.requirement_ids + sprint.bug_ids)
            or any_exact_matches(args.change, sprint.change_ids)
        ):
            return sprint
    return None


def count_tasks(tasks_path: Path) -> tuple[int, int]:
    if not tasks_path.exists():
        return (0, 0)
    text = read_text(tasks_path)
    done = len(re.findall(r"(?m)^\s*-\s*\[[xX]\]", text))
    open_count = len(re.findall(r"(?m)^\s*-\s*\[\s\]", text))
    return done, done + open_count


def find_archived_change(root: Path, change_id: str) -> Path | None:
    archive_root = root / "openspec" / "changes" / "archive"
    if not archive_root.exists():
        return None
    for path in archive_root.rglob("*"):
        if not path.is_dir():
            continue
        if path.name == change_id or path.name.endswith(f"-{change_id}"):
            if (path / "tasks.md").exists() or (path / "proposal.md").exists() or (path / "trace.md").exists():
                return path
    return None


def derive_change(root: Path, change_id: str) -> ChangeState:
    active = root / "openspec" / "changes" / change_id
    archived = find_archived_change(root, change_id)
    if archived:
        done, total = count_tasks(archived / "tasks.md")
        return ChangeState(change_id, "archived", archived.relative_to(root).as_posix() + "/", done, total)
    if active.exists():
        done, total = count_tasks(active / "tasks.md")
        status = "applied" if total and done == total else "in_progress" if done else "proposed"
        return ChangeState(change_id, status, active.relative_to(root).as_posix() + "/", done, total)
    return ChangeState(change_id, "missing", f"openspec/changes/{change_id}/")


def replace_marker_block(text: str, start: str, end: str, body: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"{re.escape(start)}\n.*?\n{re.escape(end)}",
        flags=re.DOTALL,
    )
    replacement = f"{start}\n{body.rstrip()}\n{end}"
    new_text, count = pattern.subn(replacement, text)
    return new_text, count > 0


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def sprint_goals_body(sprint: SprintState, change_states: dict[str, ChangeState]) -> str:
    lines = [
        f"- 本 Sprint 当前包含 {len(sprint.requirements)} 个需求、{len(sprint.bugs)} 个 BUG、{len(sprint.changes)} 个 OpenSpec Change。",
    ]
    if sprint.requirements:
        lines.append("- 需求目标：" + "、".join(f"`{req}`" for req in sprint.requirement_ids))
    if sprint.bugs:
        lines.append("- 缺陷目标：" + "、".join(f"`{bug}`" for bug in sprint.bug_ids))
    if sprint.changes:
        archived = sum(1 for state in change_states.values() if state.status == "archived")
        applied = sum(1 for state in change_states.values() if state.status == "applied")
        active = len(sprint.changes) - archived - applied
        lines.append(f"- 交付目标：推进 {len(sprint.changes)} 个 Change（archived {archived}，applied {applied}，active/proposed {active}）。")
    lines.append("- 时间记录：本模块由 workflow-sync 根据 sprint.yaml 刷新；目标日期字段统一使用 `YYYY-MM-DD hh:mm:ss`，缺少时分秒时写 `待确认`。")
    return "\n".join(lines)


def patch_sprint_md(root: Path, sprint: SprintState, change_states: dict[str, ChangeState], report: Report) -> list[Patch]:
    path = sprint.path / "sprint.md"
    if not path.exists():
        report.skipped.append(f"{path.relative_to(root)} (missing)")
        return []

    before = read_text(path)
    after = before
    changed_any = False

    req_rows = [
        [
            req.item_id,
            item_value(req, ["name", "title"], req.item_id),
            item_value(req, ["priority"], "-"),
            item_value(req, ["status"], "in_sprint"),
            item_value(req, ["description", "说明"]),
            full_datetime_or_unknown(item_value(req, ["included_at", "created_at", "updated_at", "纳入时间"])),
        ]
        for req in sprint.requirements
    ]
    bug_rows = [
        [
            bug.item_id,
            item_value(bug, ["severity", "严重等级"], "-"),
            item_value(bug, ["status"], "in_sprint"),
            item_value(bug, ["description", "说明"]),
            full_datetime_or_unknown(item_value(bug, ["included_at", "created_at", "updated_at", "纳入时间"])),
        ]
        for bug in sprint.bugs
    ]
    change_rows = [
        [
            f"`{state.change_id}`",
            item_value(change, ["requirement", "req", "关联需求"], "-"),
            state.status,
            item_value(change, ["sprint_goal", "Sprint目标", "Sprint 目标"]),
            full_datetime_or_unknown(item_value(change, ["target_date", "目标日期", "updated_at"])),
            f"{state.tasks_done}/{state.tasks_total}" if state.tasks_total else "-",
            state.path,
        ]
        for change in sprint.changes
        if (state := change_states.get(change.item_id))
    ]
    milestone_rows = [
        [
            item_value(milestone, ["stage", "阶段"], milestone.milestone_id),
            item_value(milestone, ["deliverable", "交付"], "-"),
            item_value(milestone, ["status"], "待确认"),
            full_datetime_or_unknown(item_value(milestone, ["target_date", "目标日期"])),
        ]
        for milestone in sprint.milestones
    ]

    replacements = {
        "sprint_goals": sprint_goals_body(sprint, change_states),
        "scope_requirements": table(["REQ ID", "名称", "优先级", "状态", "说明", "纳入时间"], req_rows),
        "scope_bugs": table(["BUG ID", "严重等级", "状态", "说明", "纳入时间"], bug_rows),
        "scope_changes": table(["Change ID", "关联需求", "状态", "Sprint 目标", "目标日期", "Tasks", "路径"], change_rows),
        "milestones": table(["阶段", "交付", "状态", "目标日期"], milestone_rows),
    }
    for marker, body in replacements.items():
        start, end = SYNC_MARKERS[marker]
        after, changed = replace_marker_block(after, start, end, body)
        changed_any = changed_any or changed

    if not changed_any:
        report.skipped.append(f"{path.relative_to(root)} (no workflow-sync markers)")
        return []
    if before != after:
        return [Patch(path, before, after, "sprint marker refresh")]
    report.skipped.append(f"{path.relative_to(root)} (no delta)")
    return []


def patch_acceptance_report(root: Path, sprint: SprintState, change_states: dict[str, ChangeState], report: Report) -> list[Patch]:
    path = sprint.path / "acceptance-report.md"
    if not path.exists():
        report.skipped.append(f"{path.relative_to(root)} (missing)")
        return []

    before = read_text(path)
    rows = [
        [
            f"`{state.change_id}`",
            state.status,
            f"{state.tasks_done}/{state.tasks_total}" if state.tasks_total else "-",
            state.path,
        ]
        for state in change_states.values()
    ]
    body = table(["Change ID", "状态", "Tasks", "OpenSpec 路径"], rows)
    start, end = SYNC_MARKERS["acceptance_tasks"]
    after, changed = replace_marker_block(before, start, end, body)
    if not changed:
        report.skipped.append(f"{path.relative_to(root)} (no workflow-sync markers)")
        return []
    if before != after:
        return [Patch(path, before, after, "acceptance OpenSpec tasks refresh")]
    report.skipped.append(f"{path.relative_to(root)} (no delta)")
    return []


def patch_release_note(root: Path, sprint: SprintState, change_states: dict[str, ChangeState], report: Report) -> list[Patch]:
    path = sprint.path / "release-note.md"
    if not path.exists():
        report.skipped.append(f"{path.relative_to(root)} (missing)")
        return []

    before = read_text(path)
    rows = [
        [f"`{state.change_id}`", state.status, state.path]
        for state in change_states.values()
    ]
    body = table(["Change ID", "发布状态", "OpenSpec 路径"], rows)
    start, end = SYNC_MARKERS["release_changes"]
    after, changed = replace_marker_block(before, start, end, body)
    if not changed:
        report.skipped.append(f"{path.relative_to(root)} (no workflow-sync markers)")
        return []
    if before != after:
        return [Patch(path, before, after, "release note change status refresh")]
    report.skipped.append(f"{path.relative_to(root)} (no delta)")
    return []


def status_label(status: str) -> str:
    return {
        "archived": "已归档",
        "applied": "已应用",
        "in_progress": "进行中",
        "proposed": "已提案",
        "missing": "缺失",
    }.get(status, status)


def patch_issue_trace(root: Path, trace_path: Path, change_states: dict[str, ChangeState], report: Report) -> list[Patch]:
    before = read_text(trace_path)
    after = before
    touched = False

    for change_id, state in change_states.items():
        if change_id not in after:
            continue
        touched = True
        path_pattern = re.compile(rf"openspec/changes/(?:archive/[^`|)\s]+/)?{re.escape(change_id)}/")
        after = path_pattern.sub(state.path, after)

    if not touched:
        report.skipped.append(f"{trace_path.relative_to(root)} (no referenced change)")
        return []
    if before != after:
        return [Patch(trace_path, before, after, "issue trace OpenSpec status refresh")]
    report.skipped.append(f"{trace_path.relative_to(root)} (no delta)")
    return []


def candidate_trace_files(root: Path, reqs: list[str], bugs: list[str], change_ids: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for req in reqs:
        paths.update((root / "issues" / "requirements").glob(f"**/{req}*/trace.md"))
    for bug in bugs:
        paths.update((root / "issues" / "bugs").glob(f"**/{bug}*/trace.md"))
    if change_ids:
        for trace in (root / "issues").glob("**/trace.md"):
            try:
                text = read_text(trace)
            except UnicodeDecodeError:
                continue
            if any(change_id in text for change_id in change_ids):
                paths.add(trace)
    return sorted(paths)


def diff_patch(patch: Patch, root: Path) -> str:
    rel = patch.path.relative_to(root).as_posix()
    return "".join(
        difflib.unified_diff(
            patch.before.splitlines(True),
            patch.after.splitlines(True),
            fromfile=f"a/{rel}",
            tofile=f"b/{rel}",
        )
    )


def apply_patches(root: Path, patches: list[Patch], args: argparse.Namespace, report: Report) -> int:
    if not patches:
        return 0

    if args.check:
        for patch in patches:
            report.drift.append(f"{patch.path.relative_to(root)} ({patch.reason})")
            print(diff_patch(patch, root))
        return 1

    if args.dry_run:
        for patch in patches:
            print(diff_patch(patch, root))
        return 0

    for patch in patches:
        write_text(patch.path, patch.after)
        report.updated.append(f"{patch.path.relative_to(root)} ({patch.reason})")
    return 0


def print_report(args: argparse.Namespace, sprint: SprintState | None, report: Report) -> None:
    print("## Workflow Sync")
    print(f"Event: {args.event}")
    if sprint:
        print(f"Sprint: {sprint.sprint_id}")
    if report.updated:
        print("Updated:")
        for item in report.updated:
            print(f"- {item}")
    else:
        print("Updated: none")
    if report.drift:
        print("Drift:")
        for item in report.drift:
            print(f"- {item}")
    if report.skipped:
        print("Skipped:")
        for item in report.skipped:
            print(f"- {item}")


def main() -> int:
    args = parse_args()
    root = find_root(Path.cwd())
    report = Report()
    sprint = resolve_sprint(root, args)

    change_ids = list(dict.fromkeys(args.change))
    if sprint:
        change_ids = list(dict.fromkeys([*change_ids, *sprint.change_ids]))
    change_states = {change_id: derive_change(root, change_id) for change_id in change_ids}

    patches: list[Patch] = []
    if sprint:
        patches.extend(patch_sprint_md(root, sprint, change_states, report))
        patches.extend(patch_acceptance_report(root, sprint, change_states, report))
        patches.extend(patch_release_note(root, sprint, change_states, report))

    trace_paths = candidate_trace_files(root, args.req, args.bug, change_ids)
    for trace_path in trace_paths:
        patches.extend(patch_issue_trace(root, trace_path, change_states, report))

    if args.check and not patches and not report.skipped:
        report.skipped.append("no sync targets discovered")

    exit_code = apply_patches(root, patches, args, report)
    print_report(args, sprint, report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
