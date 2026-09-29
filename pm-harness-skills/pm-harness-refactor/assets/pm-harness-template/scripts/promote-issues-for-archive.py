#!/usr/bin/env python3
"""Promote REQ/BUG directories to archive/ after OpenSpec change(s) are archived.

Used by /opsx-archive and /sprint-archive after workflow-sync updates trace status.

See rules/issues-lifecycle.md §4.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_sync.collect import (  # noqa: E402
    IssueRecord,
    find_archived_change_dir,
    load_all_issues,
    load_sprint,
    resolve_issue_dir,
    resolve_sprint_dir,
)
from workflow_sync.issue_status_residuals import (  # noqa: E402
    IssueStatusResidual,
    scan_issue_status_residuals,
)

ROOT = SCRIPTS_DIR.parent
PROMOTE_SCRIPT = SCRIPTS_DIR / "promote-issue-stage.py"
DONE_STATUSES = frozenset({"done", "archived", "resolved", "closed", "completed"})
PROMOTABLE_STAGES = frozenset({"review", "legacy"})


@dataclass
class PromotionCandidate:
    issue_id: str
    kind: str
    stage: str
    status: str | None
    change_ids: list[str]
    pending_changes: list[str]
    reason: str


def change_is_archived(change_id: str) -> bool:
    if find_archived_change_dir(change_id) is not None:
        return True
    return not (ROOT / "openspec/changes" / change_id).exists()


def collect_issue_change_ids(issue: IssueRecord) -> list[str]:
    ids: list[str] = []
    for oc in issue.openspec_changes:
        cid = oc.get("change_id")
        if isinstance(cid, str) and cid.strip():
            ids.append(cid.strip())
    if issue.kind == "req":
        for cid in issue.related_changes:
            if cid not in ids:
                ids.append(cid)
    if issue.kind == "bug" and issue.related_change:
        cid = str(issue.related_change).strip()
        if cid and cid not in ids:
            ids.append(cid)
    return ids


def issue_stage(issue: IssueRecord) -> str:
    base_rel = f"issues/{'requirements' if issue.kind == 'req' else 'bugs'}"
    resolved = resolve_issue_dir(base_rel, issue.issue_id)
    if resolved is None:
        return "unknown"
    rel = resolved.relative_to(ROOT / "issues" / ("requirements" if issue.kind == "req" else "bugs"))
    if len(rel.parts) == 1:
        return "legacy"
    stage = rel.parts[0]
    return stage if stage in {"plan", "review", "archive"} else "unknown"


def pending_change_ids(issue: IssueRecord) -> list[str]:
    return [cid for cid in collect_issue_change_ids(issue) if not change_is_archived(cid)]


def issue_ready_for_archive(issue: IssueRecord) -> tuple[bool, str]:
    stage = issue_stage(issue)
    if stage == "archive":
        return False, "already in archive/"
    if stage not in PROMOTABLE_STAGES:
        return False, f"stage `{stage}` is not promotable (need review/legacy)"

    pending = pending_change_ids(issue)
    if pending:
        return False, f"pending active change(s): {', '.join(pending)}"

    change_ids = collect_issue_change_ids(issue)
    if not change_ids:
        status = (issue.trace_status or "").lower()
        if status in DONE_STATUSES:
            return True, "status done (no linked change)"
        return False, "no linked change and status not done"

    status = (issue.trace_status or "").lower()
    if status not in DONE_STATUSES:
        return False, f"status `{issue.trace_status}` not done (sync first?)"

    return True, "all linked changes archived and status done"


def issues_linked_to_change(change_id: str, issues: dict[str, IssueRecord]) -> list[IssueRecord]:
    matched: list[IssueRecord] = []
    for issue in issues.values():
        linked = any(oc.get("change_id") == change_id for oc in issue.openspec_changes)
        if issue.kind == "bug" and issue.related_change == change_id:
            linked = True
        if linked:
            matched.append(issue)
    return matched


def build_candidates(
    issue_ids: list[str],
    issues: dict[str, IssueRecord],
) -> list[PromotionCandidate]:
    candidates: list[PromotionCandidate] = []
    for issue_id in issue_ids:
        issue = issues.get(issue_id)
        if not issue:
            continue
        ready, reason = issue_ready_for_archive(issue)
        if not ready:
            continue
        candidates.append(
            PromotionCandidate(
                issue_id=issue.issue_id,
                kind=issue.kind,
                stage=issue_stage(issue),
                status=issue.trace_status,
                change_ids=collect_issue_change_ids(issue),
                pending_changes=pending_change_ids(issue),
                reason=reason,
            )
        )
    return candidates


def unique_issue_ids(*groups: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for group in groups:
        for item in group:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
    return ordered


def resolve_sprint_issue_ids(sprint_id: str) -> list[str]:
    sprint_dir = resolve_sprint_dir(sprint_id)
    if sprint_dir is None:
        raise FileNotFoundError(f"sprint not found: {sprint_id}")
    sprint = load_sprint(sprint_id)
    if not sprint:
        raise FileNotFoundError(f"sprint.yaml missing for: {sprint_id}")
    return unique_issue_ids(sprint.requirements, sprint.bugs)


def collect_candidates_for_change(change_id: str, issues: dict[str, IssueRecord]) -> list[PromotionCandidate]:
    linked = issues_linked_to_change(change_id, issues)
    issue_ids = [issue.issue_id for issue in linked]
    return build_candidates(issue_ids, issues)


def collect_candidates_for_sprint(sprint_id: str, issues: dict[str, IssueRecord]) -> list[PromotionCandidate]:
    issue_ids = resolve_sprint_issue_ids(sprint_id)
    return build_candidates(issue_ids, issues)


def print_report(candidates: list[PromotionCandidate], *, dry_run: bool, context: str) -> None:
    print(f"## Promote Issues For Archive ({context})\n")
    if not candidates:
        print("No issues eligible for `review/` → `archive/` promotion.")
        return
    print("| Issue | Kind | From | Changes |")
    print("|-------|------|------|---------|")
    for item in candidates:
        changes = ", ".join(item.change_ids) if item.change_ids else "—"
        print(f"| {item.issue_id} | {item.kind} | {item.stage}/ | {changes} |")
    if dry_run:
        print("\nDry-run only. Re-run without `--dry-run` to apply promotions.")
    print()


def collect_residual_blockers(candidates: list[PromotionCandidate], issues: dict[str, IssueRecord]) -> list[IssueStatusResidual]:
    blockers: list[IssueStatusResidual] = []
    for item in candidates:
        issue = issues.get(item.issue_id)
        if issue is None:
            continue
        blockers.extend(scan_issue_status_residuals(issue.path, issue_id=item.issue_id))
    return blockers


def print_residual_blockers(blockers: list[IssueStatusResidual]) -> None:
    if not blockers:
        return
    print("## Issue Subdocument Status Gate\n")
    print("BLOCKED: issue archive promotion found non-closed status values in issue subdocuments.\n")
    print("| Issue | File | Source | Status | Suggestion |")
    print("|-------|------|--------|--------|------------|")
    for blocker in blockers:
        try:
            file_path = blocker.file.relative_to(ROOT)
        except ValueError:
            file_path = blocker.file
        issue_flag = "--req" if blocker.issue_id.startswith("REQ-") else "--bug"
        event = "req.archive" if issue_flag == "--req" else "bug.archive"
        dry_run_cmd = (
            f"python scripts/sync-workflow-status.py --event {event} {issue_flag} {blocker.issue_id} "
            "--sprint auto --reconcile-issue-status-residuals --dry-run"
        )
        write_cmd = (
            f"python scripts/sync-workflow-status.py --event {event} {issue_flag} {blocker.issue_id} "
            "--sprint auto --reconcile-issue-status-residuals --apply-reconcile"
        )
        print(
            f"| {blocker.issue_id} | `{file_path}` | {blocker.source} | `{blocker.status}` | "
            f"先运行 `{dry_run_cmd}`，确认后运行 `{write_cmd}`；若被阻断，先完成报告中的上游命令。 |"
        )
    print()


def run_promotions(candidates: list[PromotionCandidate], *, dry_run: bool, reason: str) -> int:
    exit_code = 0
    for item in candidates:
        flag = "--req" if item.kind == "req" else "--bug"
        cmd = [
            sys.executable,
            str(PROMOTE_SCRIPT),
            flag,
            item.issue_id,
            "--to",
            "archive",
            "--reason",
            reason,
        ]
        if dry_run:
            cmd.append("--dry-run")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            exit_code = result.returncode
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote REQ/BUG issue directories to archive/ when linked changes are archived.",
    )
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--change", metavar="change-id", help="OpenSpec change id just archived")
    scope.add_argument("--sprint", metavar="sprint-id", help="Sprint id (promote eligible sprint issues)")
    parser.add_argument(
        "--reason",
        default="",
        help="Changelog reason (default: /opsx-archive or /sprint-archive)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report eligible issues without moving")
    args = parser.parse_args()

    issues = load_all_issues()
    if args.change:
        candidates = collect_candidates_for_change(args.change, issues)
        context = f"change `{args.change}`"
        default_reason = f"/opsx-archive {args.change}"
    else:
        candidates = collect_candidates_for_sprint(args.sprint, issues)
        context = f"sprint `{args.sprint}`"
        default_reason = f"/sprint-archive {args.sprint}"

    reason = args.reason.strip() or default_reason
    print_report(candidates, dry_run=args.dry_run, context=context)
    blockers = collect_residual_blockers(candidates, issues)
    if blockers:
        print_residual_blockers(blockers)
        return 1
    sys.stdout.flush()
    return run_promotions(candidates, dry_run=args.dry_run, reason=reason)


if __name__ == "__main__":
    raise SystemExit(main())
