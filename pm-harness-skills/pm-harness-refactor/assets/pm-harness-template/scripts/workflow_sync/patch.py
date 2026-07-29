from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .collect import IssueRecord, SprintRecord, parse_frontmatter, read_text
from .constants import ROOT, SCOPE_MARKERS
from .derive import DerivedChange, DerivedIssue
from .timefmt import normalize_datetime, normalize_milestone_datetime, now_shanghai, touch_frontmatter


@dataclass
class PatchResult:
    path: str
    changed: bool
    detail: str = ""


def persist_markdown(path: Path, text: str, original: str, write: bool) -> bool:
    changed = text != original
    if write:
        text, ts_changed = touch_frontmatter(text, bump_updated=changed)
        changed = changed or ts_changed
        if changed:
            path.write_text(text, encoding="utf-8")
    return changed


def replace_marker_block(text: str, marker: str, new_body: str) -> tuple[str, bool]:
    start = f"<!-- {marker}:start -->"
    end = f"<!-- {marker}:end -->"
    block = f"{start}\n{new_body.rstrip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(block, text, count=1)
        return updated, updated != text
    return text, False


def ensure_marker_block(text: str, marker: str, new_body: str, insert_after: str) -> tuple[str, bool]:
    start = f"<!-- {marker}:start -->"
    if start in text:
        return replace_marker_block(text, marker, new_body)
    anchor_idx = text.find(insert_after)
    if anchor_idx == -1:
        return text, False
    line_end = text.find("\n", anchor_idx)
    if line_end == -1:
        line_end = len(text)
    insertion = (
        text[: line_end + 1]
        + f"\n<!-- {marker}:start -->\n{new_body.rstrip()}\n<!-- {marker}:end -->\n"
        + text[line_end + 1 :]
    )
    return insertion, True


def short_issue_label(issue_id: str) -> str:
    parts = issue_id.split("-", 2)
    if len(parts) >= 3:
        return f"{parts[0]}-{parts[1]}-{parts[2]}"
    return issue_id


def short_issue_code(issue_id: str) -> str:
    match = re.match(r"^(REQ-\d{4}|BUG-\d{4})", issue_id)
    return match.group(1) if match else issue_id


def issue_display_name(issue: IssueRecord) -> str:
    if issue.title and issue.title != issue.issue_id:
        return issue.title
    slug = issue.issue_id.split("-", 2)
    if len(slug) >= 3:
        return slug[2].replace("-", " ")
    return issue.issue_id


def render_requirements_table(
    sprint: SprintRecord,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
) -> str:
    lines = [
        "| 编号 | 名称 | 优先级 | 状态 | 说明 |",
        "|---|---|---|---|---|",
    ]
    for req_id in sprint.requirements:
        issue = issues.get(req_id)
        derived = derived_issues.get(req_id)
        if not issue or not derived:
            lines.append(f"| {short_issue_code(req_id)} | {req_id} | P1 | unknown | 未找到 trace |")
            continue
        linked_change = derived.linked_change
        change = changes.get(linked_change) if linked_change else None
        note = change.note if change else derived.note
        lines.append(
            f"| {short_issue_code(req_id)} | {issue_display_name(issue)} | {issue.priority} | "
            f"{derived.display_status} | {note} |"
        )
    return "\n".join(lines)


def render_bugs_table(
    sprint: SprintRecord,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
) -> str:
    lines = [
        "| 编号 | 名称 | 优先级 | 状态 | 说明 |",
        "|---|---|---|---|---|",
    ]
    for bug_id in sprint.bugs:
        issue = issues.get(bug_id)
        derived = derived_issues.get(bug_id)
        if not issue or not derived:
            lines.append(f"| {short_issue_code(bug_id)} | {bug_id} | P1 | unknown | 未找到 trace |")
            continue
        linked_change = derived.linked_change or issue.related_change
        change = changes.get(linked_change) if linked_change else None
        note = change.note if change else derived.note
        lines.append(
            f"| {short_issue_code(bug_id)} | {issue_display_name(issue)} | {issue.priority} | "
            f"{derived.display_status} | {note} |"
        )
    return "\n".join(lines)


def normalize_milestone_table_dates(text: str) -> tuple[str, bool]:
    """Normalize 目标日期 cells under ## 里程碑 to YYYY-MM-DD HH:mm:ss with non-zero time."""

    section_match = re.search(r"(^## 里程碑\s*\n)(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not section_match:
        return text, False

    section = section_match.group(2)
    changed = False
    new_lines: list[str] = []

    for line in section.splitlines():
        if not line.strip().startswith("|") or line.count("|") < 4 or "---" in line:
            new_lines.append(line)
            continue
        parts = line.split("|")
        if len(parts) < 5:
            new_lines.append(line)
            continue
        date_cell = parts[-2].strip()
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2}:\d{2})?)(.*)$", date_cell)
        if not date_match:
            new_lines.append(line)
            continue
        normalized = normalize_milestone_datetime(date_match.group(1))
        if not normalized:
            new_lines.append(line)
            continue
        suffix = date_match.group(2) or ""
        new_cell = f"{normalized}{suffix}"
        if new_cell != date_cell:
            changed = True
            parts[-2] = f" {new_cell} "
            line = "|".join(parts)
        new_lines.append(line)

    if not changed:
        return text, False
    new_section = "\n".join(new_lines)
    return text[: section_match.start(2)] + new_section + text[section_match.end(2) :], True


def render_changes_table(
    sprint: SprintRecord,
    changes: dict[str, DerivedChange],
) -> str:
    lines = [
        "| Change ID | 关联需求 | 状态 | Sprint 目标 |",
        "|---|---|---|---|",
    ]
    for change_id in sprint.changes:
        change = changes.get(change_id)
        if not change:
            lines.append(f"| `{change_id}` | — | missing | — |")
            continue
        link = change.linked_req or change.linked_bug or "—"
        if change.linked_req:
            link = short_issue_label(change.linked_req)
        elif change.linked_bug:
            link = short_issue_label(change.linked_bug)
        goal = change.note
        lines.append(
            f"| `{change.change_id}` | {link} | {change.display_status} | {goal} |"
        )
    return "\n".join(lines)


def patch_sprint_md(
    sprint: SprintRecord,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
    summary_note: str,
    write: bool = True,
) -> PatchResult:
    path = sprint.path / "sprint.md"
    text = read_text(path)
    original = text

    req_table = render_requirements_table(sprint, issues, derived_issues, changes)
    bug_table = render_bugs_table(sprint, issues, derived_issues, changes)
    change_table = render_changes_table(sprint, changes)

    text, _ = ensure_marker_block(
        text,
        SCOPE_MARKERS["requirements"],
        req_table,
        "### 包含需求",
    )
    text, _ = replace_marker_block(text, SCOPE_MARKERS["requirements"], req_table)

    text, _ = ensure_marker_block(
        text,
        SCOPE_MARKERS["bugs"],
        bug_table,
        "### 包含 BUG",
    )
    text, _ = replace_marker_block(text, SCOPE_MARKERS["bugs"], bug_table)

    text, _ = ensure_marker_block(
        text,
        SCOPE_MARKERS["changes"],
        change_table,
        "### 包含 Change",
    )
    text, _ = replace_marker_block(text, SCOPE_MARKERS["changes"], change_table)

    text, milestone_changed = normalize_milestone_table_dates(text)

    note_line = f"note: workflow-sync — {summary_note}"
    if re.search(r"^note:\s*.+$", text, re.MULTILINE):
        text = re.sub(r"^note:\s*.+$", note_line, text, count=1, flags=re.MULTILINE)
    else:
        text = text.replace("---\n", f"---\n{note_line}\n", 1)

    changed = persist_markdown(path, text, original, write)
    detail = "Scope tables + note"
    if milestone_changed:
        detail += " + milestone dates"
    return PatchResult(str(path.relative_to(ROOT)), changed, detail)


def patch_release_note(sprint: SprintRecord, release_line: str, write: bool = True) -> PatchResult:
    path = sprint.path / "release-note.md"
    if not path.exists():
        return PatchResult(str(path.relative_to(ROOT)), False, "missing file")
    text = read_text(path)
    original = text
    body = f"| 发布状态 | {release_line} |"
    text, marker_changed = replace_marker_block(text, SCOPE_MARKERS["release_status"], body)
    if not marker_changed:
        text, _ = ensure_marker_block(
            text,
            SCOPE_MARKERS["release_status"],
            body,
            "| 计划周期 |",
        )
        text, _ = replace_marker_block(text, SCOPE_MARKERS["release_status"], body)
    if re.search(r"^\| 发布状态 \|", text, re.MULTILINE) and SCOPE_MARKERS["release_status"] + ":start" not in text:
        text = re.sub(
            r"^\| 发布状态 \|.*\|$",
            f"| 发布状态 | {release_line} |",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    changed = persist_markdown(path, text, original, write)
    return PatchResult(str(path.relative_to(ROOT)), changed, "release status")


def change_status_text(change: DerivedChange | None, fallback_status: str) -> str:
    if change and change.state == "archived":
        archive_date = ""
        if change.archive_date:
            normalized = normalize_datetime(change.archive_date)
            archive_date = f" {normalized}" if normalized else ""
        return f"done，已归档（`{change.change_id}` archived{archive_date}）"
    if change and change.state == "applied":
        return f"applied，待归档（`{change.change_id}` {change.tasks_done}/{change.tasks_total}）"
    if change and change.state == "in_progress":
        return f"in_progress（`{change.change_id}` {change.tasks_done}/{change.tasks_total}）"
    if change and change.state == "proposed":
        return f"in_sprint，待实现（`{change.change_id}` proposed）"
    return fallback_status


def patch_acceptance_report(
    sprint: SprintRecord,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
    write: bool = True,
) -> PatchResult:
    path = sprint.path / "acceptance-report.md"
    if not path.exists():
        return PatchResult(str(path.relative_to(ROOT)), False, "missing file")
    text = read_text(path)
    original = text

    for issue_id, derived in derived_issues.items():
        issue = issues.get(issue_id)
        if not issue:
            continue
        change_id = derived.linked_change or issue.related_change
        change = changes.get(change_id) if change_id else None
        status_text = change_status_text(change, derived.display_status)
        source_pattern = re.escape(f"`{issue.path.relative_to(ROOT)}/acceptance.md`")
        pattern = re.compile(
            rf"(> 来源：{source_pattern}\s*\n)> 状态：\*\*.*?\*\*.*?$",
            re.MULTILINE,
        )
        text = pattern.sub(rf"\1> 状态：**{status_text}**", text, count=1)
        table_pattern = re.compile(
            rf"^(\| (?:REQ|BUG) \| {re.escape(issue_id)} \| [^|]+ \| )[^|]*( \| .+\|)$",
            re.MULTILINE,
        )
        text = table_pattern.sub(rf"\1{status_text}\2", text, count=1)

    summary = sprint_summary_for_acceptance(sprint, changes)
    note_line = f"note: workflow-sync — {summary}"
    if re.search(r"^note:\s*.+$", text, re.MULTILINE):
        text = re.sub(r"^note:\s*.+$", note_line, text, count=1, flags=re.MULTILINE)
    else:
        text = text.replace("---\n", f"---\n{note_line}\n", 1)

    changed = persist_markdown(path, text, original, write)
    return PatchResult(str(path.relative_to(ROOT)), changed, "issue status lines + note")


def sprint_summary_for_acceptance(sprint: SprintRecord, changes: dict[str, DerivedChange]) -> str:
    total = len(sprint.changes)
    archived = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "archived")
    applied = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "applied")
    return f"{archived}/{total} Change 已 archive；{applied} applied；待人工 sign-off"


def bug_summary_text(issue: IssueRecord) -> str:
    if issue.title and issue.title != issue.issue_id:
        return issue.title
    return issue_display_name(issue)


def render_parent_bug_index(
    parent_req_id: str,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
) -> str:
    rows = [
        "| BUG | 严重等级 | 状态 | 关联 Change | 说明 |",
        "|---|---|---|---|---|",
    ]
    related_bugs = sorted(
        (
            issue
            for issue in issues.values()
            if issue.kind == "bug" and issue.related_requirement == parent_req_id
        ),
        key=lambda issue: issue.issue_id,
    )
    for bug in related_bugs:
        derived = derived_issues.get(bug.issue_id)
        status = derived.display_status if derived else (bug.trace_status or "captured")
        change_id = (
            derived.linked_change
            if derived and derived.linked_change
            else bug.related_change
        )
        change = changes.get(change_id) if change_id else None
        if change and change.state == "archived":
            status = "done"
        severity = bug.priority
        rows.append(
            f"| {bug.issue_id} | {severity} | {status} | {change_id or '—'} | {bug_summary_text(bug)} |"
        )
    return "\n".join(rows)


def patch_parent_requirement_bug_index(
    parent_req_id: str,
    issues: dict[str, IssueRecord],
    derived_issues: dict[str, DerivedIssue],
    changes: dict[str, DerivedChange],
    write: bool = True,
) -> PatchResult:
    parent = issues.get(parent_req_id)
    if not parent:
        return PatchResult(f"issues/requirements/{parent_req_id}/trace.md", False, "parent requirement not found")
    trace_path = parent.path / "trace.md"
    if not trace_path.exists():
        return PatchResult(str(trace_path.relative_to(ROOT)), False, "missing trace")

    text = read_text(trace_path)
    original = text
    table = render_parent_bug_index(parent_req_id, issues, derived_issues, changes)
    heading_pattern = re.compile(
        r"(##[ \t]+(?:\d+\.[ \t]*)?关联缺陷[ \t]*\n)(.*?)(?=\n##[ \t]+|\Z)",
        re.DOTALL,
    )
    if heading_pattern.search(text):
        text = heading_pattern.sub(lambda match: f"{match.group(1)}\n{table}\n", text, count=1)
    else:
        text = text.rstrip() + f"\n\n## 关联缺陷\n\n{table}\n"

    changed = persist_markdown(trace_path, text, original, write)
    return PatchResult(str(trace_path.relative_to(ROOT)), changed, "related bug index")


def update_yaml_scalar(block: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^({re.escape(key)}:\s*).*$", re.MULTILINE)
    if pattern.search(block):
        return pattern.sub(rf"\1{value}", block, count=1)
    return block.rstrip() + f"\n{key}: {value}\n"


def update_openspec_changes_in_block(block: str, change_id: str, status: str) -> str:
    lines = block.splitlines()
    out: list[str] = []
    in_target = False
    for line in lines:
        if re.match(rf"^\s*- change_id:\s*{re.escape(change_id)}\s*$", line):
            in_target = True
            out.append(line)
            continue
        if in_target and re.match(r"^\s*status:\s*", line):
            indent = line[: len(line) - len(line.lstrip(" "))]
            out.append(f"{indent}status: {status}")
            in_target = False
            continue
        if in_target and re.match(r"^\s*- change_id:", line):
            in_target = False
        out.append(line)
    return "\n".join(out)


def append_workflow_event_record(
    text: str,
    *,
    event: str | None,
    change_id: str | None,
    derived: DerivedIssue,
    change_status_map: dict[str, str],
) -> str:
    if "## 变更记录" not in text or not event or not change_id:
        return text
    if derived.linked_change != change_id:
        return text
    change_status = change_status_map.get(change_id)
    if event == "opsx.apply" and change_status == "applied":
        command = "/opsx-apply"
        description = f"Change `{change_id}` apply 完成，待 archive。"
    elif event == "opsx.archive" and change_status == "archived":
        command = "/opsx-archive"
        description = f"Change `{change_id}` 已归档，状态同步完成。"
    else:
        return text

    if command in text and change_id in text and description in text:
        return text

    stamp = now_shanghai()
    table_row = f"| {stamp} | {command} | {description} |\n"
    table_header = re.compile(r"(## 变更记录\n\n\|[^\n]*\|\n\|[^\n]*\|\n)", re.MULTILINE)
    if table_header.search(text):
        return table_header.sub(rf"\1{table_row}", text, count=1)
    return text.replace("## 变更记录\n\n", f"## 变更记录\n\n- {stamp} {command}：{description}\n", 1)


def normalize_change_record_table(text: str) -> str:
    section_pattern = re.compile(r"(## 变更记录\n\n)(.*?)(?=\n## |\Z)", re.DOTALL)
    match = section_pattern.search(text)
    if not match:
        return text

    body = match.group(2)
    lines = body.splitlines()
    header_index: int | None = None
    for index, line in enumerate(lines[:-1]):
        if re.match(r"^\|\s*(时间|日期)\s*\|", line) and re.match(r"^\|\s*-", lines[index + 1]):
            header_index = index
            break
    if header_index is None:
        return text

    header = lines[header_index]
    separator = lines[header_index + 1]
    rows: list[str] = []
    other_lines: list[str] = []
    for index, line in enumerate(lines):
        if index in {header_index, header_index + 1}:
            continue
        if line.startswith("|") and line.endswith("|"):
            rows.append(line)
        elif line.strip():
            other_lines.append(line)

    normalized_lines = [header, separator, *rows]
    if other_lines:
        normalized_lines.extend(["", *other_lines])
    normalized_body = "\n".join(normalized_lines).rstrip() + "\n"
    if normalized_body == body:
        return text
    return text[: match.start(2)] + normalized_body + text[match.end(2) :]


def update_current_status_section(text: str, issue: IssueRecord, derived: DerivedIssue) -> str:
    if "## 当前状态" not in text:
        return text
    stage = issue.path.parent.name if issue.path.parent.name in {"plan", "review", "archive"} else None
    if stage:
        text = re.sub(
            r"(?m)^- 阶段：.+$",
            f"- 阶段：{stage}",
            text,
            count=1,
        )
    return re.sub(
        r"(?m)^- 状态：.+$",
        f"- 状态：{derived.display_status}",
        text,
        count=1,
    )


def patch_issue_trace(
    issue: IssueRecord,
    derived: DerivedIssue,
    change_status_map: dict[str, str],
    event: str | None = None,
    focus_change: str | None = None,
    write: bool = True,
) -> PatchResult:
    trace_path = issue.path / "trace.md"
    if not trace_path.exists():
        return PatchResult(str(trace_path.relative_to(ROOT)), False, "missing trace")
    text = read_text(trace_path)
    original = text
    previous_status = issue.trace_status or parse_frontmatter(text).get("status")

    if (parse_frontmatter(text).get("status") or "") == derived.display_status:
        pass
    else:
        text = re.sub(
            r"^(status:\s*).+$",
            rf"\1{derived.display_status}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    frontmatter_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if frontmatter_match:
        block = frontmatter_match.group(1).rstrip("\n") + "\n"
        current_block = block
        for change_id, status in change_status_map.items():
            block = update_openspec_changes_in_block(block, change_id, status)
        if not block.endswith("\n"):
            block += "\n"
        if block != current_block:
            text = text[: frontmatter_match.start(1)] + block + text[frontmatter_match.end(1) :]

    yaml_match = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
    if yaml_match:
        block = yaml_match.group(1).rstrip("\n") + "\n"
        current_block = block
        block = update_yaml_scalar(block, "status", derived.display_status)
        for change_id, status in change_status_map.items():
            block = update_openspec_changes_in_block(block, change_id, status)
        if not block.endswith("\n"):
            block += "\n"
        if derived.display_status == "done" and re.search(r"^\s*archived:\s*null\s*$", block, re.MULTILINE):
            block = re.sub(
                r"^(\s*archived:\s*)null\s*$",
                rf"\g<1>{now_shanghai()}",
                block,
                count=1,
                flags=re.MULTILINE,
            )
        if block != current_block:
            text = text[: yaml_match.start(1)] + block + text[yaml_match.end(1) :]

    if (
        derived.display_status == "done"
        and previous_status not in {"done", "archived", "resolved", "closed", None}
        and "## 变更记录" in text
    ):
        stamp = now_shanghai()
        entry = f"- {stamp} workflow-sync：状态同步为 done（Change archived）"
        if entry not in text:
            text = text.rstrip() + f"\n{entry}\n"

    text = normalize_change_record_table(text)
    text = append_workflow_event_record(
        text,
        event=event,
        change_id=focus_change,
        derived=derived,
        change_status_map=change_status_map,
    )
    text = update_current_status_section(text, issue, derived)

    changed = persist_markdown(trace_path, text, original, write)
    return PatchResult(str(trace_path.relative_to(ROOT)), changed, derived.display_status)


def patch_registry_entry(
    registry_path: Path,
    issue_id: str,
    display_status: str,
    write: bool = True,
) -> PatchResult:
    if not registry_path.exists():
        return PatchResult(str(registry_path.relative_to(ROOT)), False, "missing registry")
    text = read_text(registry_path)
    original = text
    pattern = re.compile(
        rf"(?m)^(\s*- id:\s*{re.escape(issue_id)}\s*\n(?:.*\n)*?\s*status:\s*).+$"
    )
    if not pattern.search(text):
        return PatchResult(str(registry_path.relative_to(ROOT)), False, "entry not found")
    text = pattern.sub(rf"\1{display_status}", text, count=1)
    changed = text != original
    if changed and write:
        registry_path.write_text(text, encoding="utf-8")
    return PatchResult(str(registry_path.relative_to(ROOT)), changed, issue_id)
