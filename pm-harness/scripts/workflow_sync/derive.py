from __future__ import annotations

from dataclasses import dataclass

from .collect import ChangeRecord, IssueRecord, SprintRecord
from .timefmt import normalize_datetime


@dataclass
class DerivedChange:
    change_id: str
    state: str
    display_status: str
    note: str
    tasks_done: int
    tasks_total: int
    linked_req: str | None
    linked_bug: str | None
    archive_date: str | None


@dataclass
class DerivedIssue:
    issue_id: str
    kind: str
    display_status: str
    linked_change: str | None
    note: str


def derive_change_state(record: ChangeRecord) -> DerivedChange:
    if record.location == "archived":
        state = "archived"
        display = "archived"
        date = normalize_datetime(record.archive_date) or "archived"
        note = f"archived `{record.change_id}`（{date}）"
    elif record.location == "active":
        done, total = record.tasks.done, record.tasks.total
        if total > 0 and done >= total:
            state = "applied"
            display = "applied"
            note = f"apply {done}/{total}；待 archive `{record.change_id}`"
        elif done > 0:
            state = "in_progress"
            display = "in_progress"
            note = f"in_progress {done}/{total}；`{record.change_id}`"
        else:
            state = "proposed"
            display = "proposed"
            note = f"proposed `{record.change_id}`"
    else:
        state = "missing"
        display = "missing"
        note = f"change `{record.change_id}` 未找到"

    return DerivedChange(
        change_id=record.change_id,
        state=state,
        display_status=display,
        note=note,
        tasks_done=record.tasks.done,
        tasks_total=record.tasks.total,
        linked_req=record.linked_req,
        linked_bug=record.linked_bug,
        archive_date=record.archive_date,
    )


def issue_status_from_change(change: DerivedChange | None, trace_status: str | None) -> str:
    if change:
        if change.state == "archived":
            return "done"
        if change.state in {"applied", "in_progress", "proposed"}:
            return "in_sprint" if trace_status in {None, "approved", "in_sprint", "applied"} else str(trace_status)
        if change.state == "missing":
            pass
    if trace_status in {"done", "archived", "resolved"}:
        return "done"
    if trace_status:
        return trace_status
    return "approved"


def derive_issue(
    issue: IssueRecord,
    changes: dict[str, DerivedChange],
    sprint: SprintRecord | None,
) -> DerivedIssue:
    linked_change = None
    for oc in issue.openspec_changes:
        cid = oc.get("change_id")
        if isinstance(cid, str):
            linked_change = cid
            break
    if not linked_change and issue.related_changes:
        linked_change = issue.related_changes[0]
    if not linked_change and issue.kind == "bug" and issue.related_change:
        linked_change = issue.related_change

    change = changes.get(linked_change) if linked_change else None
    display = issue_status_from_change(change, issue.trace_status)

    if sprint and (issue.issue_id in sprint.requirements or issue.issue_id in sprint.bugs):
        if display == "approved":
            display = "in_sprint"

    if change and change.state == "archived":
        display = "done"
        note = change.note
    elif change and change.state == "applied":
        note = f"apply 完成；待 archive `{change.change_id}`"
        if display not in {"done", "in_sprint"}:
            display = "in_sprint"
    elif change:
        note = change.note
    else:
        note = f"status `{display}`"

    return DerivedIssue(
        issue_id=issue.issue_id,
        kind=issue.kind,
        display_status=display,
        linked_change=linked_change,
        note=note,
    )


def openspec_change_status(change: DerivedChange | None) -> str:
    if not change:
        return "proposed"
    if change.state == "archived":
        return "archived"
    if change.state == "applied":
        return "applied"
    if change.state == "in_progress":
        return "in_progress"
    return "proposed"


def sprint_summary_note(sprint: SprintRecord, changes: dict[str, DerivedChange]) -> str:
    total = len(sprint.changes)
    archived = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "archived")
    applied = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "applied")
    pending = total - archived - applied
    return (
        f"workflow-sync 自动同步 — {archived}/{total} Change archived"
        f"；{applied} applied"
        f"{f'；{pending} 进行中' if pending else ''}"
        f"；Sprint `{sprint.status}`"
    )


def release_status_line(sprint: SprintRecord, changes: dict[str, DerivedChange]) -> str:
    total = len(sprint.changes)
    archived = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "archived")
    applied = sum(1 for cid in sprint.changes if changes.get(cid) and changes[cid].state == "applied")
    if sprint.status == "completed":
        return "**已发布（Published）**"
    if archived == total and total > 0:
        return "**实现完成，待 sign-off（Ready for sign-off）**"
    if applied > 0 or archived > 0:
        return "**实现进行中（In progress）**"
    return "**规划中（Draft）**"
