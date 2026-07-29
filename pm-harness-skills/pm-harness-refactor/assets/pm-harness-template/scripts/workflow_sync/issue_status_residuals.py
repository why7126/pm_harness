from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import collect
from .timefmt import now_shanghai, touch_frontmatter

CLOSED_STATUSES = frozenset({"done", "archived", "resolved", "closed", "completed"})
BLOCKING_STATUSES = frozenset(
    {
        "captured",
        "exploring",
        "draft",
        "enriching",
        "pending_review",
        "approved",
        "in_sprint",
        "applied",
        "proposed",
        "todo",
        "open",
    }
)


@dataclass(frozen=True)
class IssueStatusResidual:
    issue_id: str
    file: Path
    source: str
    status: str


@dataclass(frozen=True)
class IssueStatusReconcilePlan:
    residual: IssueStatusResidual
    target_status: str
    updated_at: str


@dataclass(frozen=True)
class IssueStatusReconcileResult:
    issue_id: str
    changed_files: int
    changed_fields: int
    planned: list[IssueStatusReconcilePlan]
    blockers: list[str]
    dry_run: bool


def _status_value(value: object) -> str | None:
    status = str(value).strip() if value is not None else ""
    return status or None


def _iter_yaml_blocks(text: str) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    for match in re.finditer(r"```yaml\n(.*?)```", text, re.DOTALL):
        blocks.append(collect.parse_simple_yaml(match.group(1)))
    return blocks


def _is_blocking_status(status: str) -> bool:
    normalized = status.strip().lower()
    if normalized in CLOSED_STATUSES:
        return False
    return normalized in BLOCKING_STATUSES


def _is_closed_status(status: str | None) -> bool:
    return (status or "").strip().lower() in CLOSED_STATUSES


def _replace_mapping_value(text: str, key: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"^(\s*{re.escape(key)}\s*:\s*).*$", re.MULTILINE)
    new_text, count = pattern.subn(rf"\g<1>{value}", text, count=1)
    return new_text, bool(count)


def _replace_frontmatter_status(text: str, target_status: str) -> tuple[str, bool]:
    if not text.startswith("---"):
        return text, False
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return text, False
    fm_text = match.group(1)
    new_fm, changed = _replace_mapping_value(fm_text, "status", target_status)
    if not changed:
        return text, False
    return f"---\n{new_fm}\n---{text[match.end():]}", True


def _replace_yaml_block_status(text: str, target_status: str) -> tuple[str, bool]:
    changed = False

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        block = match.group(1)
        parsed = collect.parse_simple_yaml(block)
        status = _status_value(parsed.get("status"))
        if not status or not _is_blocking_status(status):
            return match.group(0)
        new_block, block_changed = _replace_mapping_value(block, "status", target_status)
        if not block_changed:
            return match.group(0)
        changed = True
        return f"```yaml\n{new_block}```"

    return re.sub(r"```yaml\n(.*?)```", replace, text, flags=re.DOTALL), changed


def scan_issue_status_residuals(issue_dir: Path, *, issue_id: str | None = None) -> list[IssueStatusResidual]:
    """Return non-closed status values in top-level issue Markdown documents."""

    resolved_issue_id = issue_id or issue_dir.name
    residuals: list[IssueStatusResidual] = []
    if not issue_dir.is_dir():
        return residuals

    for path in sorted(issue_dir.glob("*.md")):
        text = collect.read_text(path)
        frontmatter_status = _status_value(collect.parse_frontmatter(text).get("status"))
        if frontmatter_status and _is_blocking_status(frontmatter_status):
            residuals.append(
                IssueStatusResidual(
                    issue_id=resolved_issue_id,
                    file=path,
                    source="frontmatter",
                    status=frontmatter_status,
                )
            )

        for block in _iter_yaml_blocks(text):
            block_status = _status_value(block.get("status"))
            if block_status and _is_blocking_status(block_status):
                residuals.append(
                    IssueStatusResidual(
                        issue_id=resolved_issue_id,
                        file=path,
                        source="yaml_block",
                        status=block_status,
                    )
                )

    return residuals


def issue_target_closed_status(issue: collect.IssueRecord) -> str:
    status = (issue.trace_status or "").strip().lower()
    return status if status in CLOSED_STATUSES else "done"


def issue_reconcile_blockers(issue: collect.IssueRecord) -> list[str]:
    blockers: list[str] = []
    if not _is_closed_status(issue.trace_status):
        blockers.append(f"issue trace status `{issue.trace_status or 'unknown'}` is not closed")

    change_ids: list[str] = []
    for oc in issue.openspec_changes:
        cid = oc.get("change_id")
        if isinstance(cid, str) and cid.strip():
            change_ids.append(cid.strip())
    if issue.kind == "req":
        for cid in issue.related_changes:
            if cid not in change_ids:
                change_ids.append(cid)
    if issue.kind == "bug" and issue.related_change:
        cid = str(issue.related_change).strip()
        if cid and cid not in change_ids:
            change_ids.append(cid)

    pending_changes = [
        cid
        for cid in change_ids
        if collect.find_archived_change_dir(cid) is None and (collect.ROOT / "openspec/changes" / cid).exists()
    ]
    if pending_changes:
        blockers.append(f"linked change(s) not archived: {', '.join(pending_changes)}")

    incomplete_sprints = [
        sprint_id
        for sprint_id in collect.find_sprints_for_issue(issue.issue_id)
        if (sprint := collect.load_sprint(sprint_id)) and sprint.status != "completed"
    ]
    if incomplete_sprints:
        blockers.append(f"linked sprint(s) not completed: {', '.join(incomplete_sprints)}")
    return blockers


def plan_issue_status_reconcile(issue: collect.IssueRecord) -> tuple[list[IssueStatusReconcilePlan], list[str]]:
    blockers = issue_reconcile_blockers(issue)
    target_status = issue_target_closed_status(issue)
    updated_at = now_shanghai()
    planned = [
        IssueStatusReconcilePlan(residual=residual, target_status=target_status, updated_at=updated_at)
        for residual in scan_issue_status_residuals(issue.path, issue_id=issue.issue_id)
    ]
    return planned, blockers


def reconcile_issue_status_residuals(
    issue: collect.IssueRecord,
    *,
    write: bool,
) -> IssueStatusReconcileResult:
    planned, blockers = plan_issue_status_reconcile(issue)
    if blockers or not planned or not write:
        return IssueStatusReconcileResult(
            issue_id=issue.issue_id,
            changed_files=0,
            changed_fields=0,
            planned=planned,
            blockers=blockers,
            dry_run=not write,
        )

    changed_files = 0
    changed_fields = 0
    for path in sorted({plan.residual.file for plan in planned}):
        text = collect.read_text(path)
        text, fm_changed = _replace_frontmatter_status(text, issue_target_closed_status(issue))
        text, block_changed = _replace_yaml_block_status(text, issue_target_closed_status(issue))
        if fm_changed or block_changed:
            text, _ = touch_frontmatter(text, bump_updated=True)
            path.write_text(text, encoding="utf-8")
            changed_files += 1
            changed_fields += int(fm_changed) + int(block_changed)

    return IssueStatusReconcileResult(
        issue_id=issue.issue_id,
        changed_files=changed_files,
        changed_fields=changed_fields,
        planned=planned,
        blockers=blockers,
        dry_run=False,
    )
