#!/usr/bin/env python3
"""Promote REQ/BUG directories between lifecycle stage folders.

The archive promotion is intentionally conservative: an issue can move to
archive only when every referenced OpenSpec change is already archived.
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path


ISSUE_TYPES = {
    "req": ("issues/requirements", "REQ"),
    "bug": ("issues/bugs", "BUG"),
}

STAGES = ("plan", "review", "archive")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


@dataclass
class IssueCandidate:
    kind: str
    issue_id: str
    path: Path
    trace_path: Path
    change_ids: list[str] = field(default_factory=list)


@dataclass
class Promotion:
    issue: IssueCandidate
    target: Path
    trace_before: str
    trace_after: str
    reason: str


@dataclass
class Report:
    promoted: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    drift: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", choices=["archive"], default="archive")
    parser.add_argument("--req", action="append", default=[])
    parser.add_argument("--bug", action="append", default=[])
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--sprint")
    parser.add_argument("--reason", default="workflow archive promotion")
    parser.add_argument("--check", action="store_true", help="Fail if promotions would be made")
    parser.add_argument("--dry-run", action="store_true", help="Show promotions without moving files")
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


def clean_scalar(value: str) -> str:
    return value.split("#", 1)[0].strip().strip("'\"")


def list_item_ids(lines: list[str], key: str) -> list[str]:
    values: list[str] = []
    in_list = False
    key_indent = 0

    for line in lines:
        stripped = line.strip()
        if in_list and stripped.startswith("#"):
            break
        if not stripped or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if re.match(rf"^{re.escape(key)}\s*:", stripped):
            in_list = True
            key_indent = indent
            inline = stripped.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                raw_items = inline[1:-1].strip()
                if raw_items:
                    values.extend(clean_scalar(item) for item in raw_items.split(",") if clean_scalar(item))
            continue
        if in_list and indent <= key_indent and not stripped.startswith("-"):
            break
        if not in_list or not stripped.startswith("- "):
            continue
        item = stripped[2:].strip()
        if not item:
            continue
        if ":" in item:
            item_key, item_value = item.split(":", 1)
            if item_key.strip() in {"id", "change_id"}:
                values.append(clean_scalar(item_value))
        else:
            values.append(clean_scalar(item))
    return [value for value in values if value]


def sprint_issue_ids(root: Path, sprint_id: str) -> tuple[list[str], list[str], list[str]]:
    matches = sorted((root / "iterations").glob(f"**/{sprint_id}/sprint.yaml"))
    if not matches:
        raise SystemExit(f"Unknown sprint: {sprint_id}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple sprint.yaml files found for {sprint_id}")
    lines = read_text(matches[0]).splitlines()
    return (
        list_item_ids(lines, "requirements"),
        list_item_ids(lines, "bugs"),
        list_item_ids(lines, "changes"),
    )


def issue_id_from_path(path: Path, kind: str) -> str:
    prefix = ISSUE_TYPES[kind][1]
    match = re.match(rf"({prefix}-\d+[^/]*)", path.name)
    return match.group(1) if match else path.name


def find_issue_dir(root: Path, kind: str, issue_id: str) -> Path | None:
    base = root / ISSUE_TYPES[kind][0]
    for stage in STAGES:
        for path in sorted((base / stage).glob(f"{issue_id}*")):
            if path.is_dir():
                return path
    return None


def change_refs_from_trace(text: str) -> list[str]:
    lines = text.splitlines()
    refs: list[str] = []
    patterns = [
        r"(?m)^\s*change_id:\s*['\"]?([A-Za-z0-9_.-]+)",
        r"(?m)^\s*-\s*change_id:\s*['\"]?([A-Za-z0-9_.-]+)",
        r"openspec/changes/(?:archive/[^/`|)\s]+/)?([^/`|)\s]+)/",
    ]
    for pattern in patterns:
        refs.extend(clean_scalar(ref) for ref in re.findall(pattern, text))
    refs.extend(list_item_ids(lines, "related_changes"))
    refs.extend(list_item_ids(lines, "openspec_changes"))
    ignored = {"archive", "changes", "待确认", "null", "none", "无"}
    return list(dict.fromkeys(ref for ref in refs if ref not in ignored and not ref.startswith(("REQ-", "BUG-"))))


def candidate_from_dir(kind: str, path: Path) -> IssueCandidate | None:
    trace_path = path / "trace.md"
    if not trace_path.exists():
        return None
    text = read_text(trace_path)
    return IssueCandidate(
        kind=kind,
        issue_id=issue_id_from_path(path, kind),
        path=path,
        trace_path=trace_path,
        change_ids=change_refs_from_trace(text),
    )


def candidates_for_changes(root: Path, change_ids: list[str]) -> list[IssueCandidate]:
    candidates: list[IssueCandidate] = []
    if not change_ids:
        return candidates
    for kind, (base_name, _) in ISSUE_TYPES.items():
        for trace_path in sorted((root / base_name).glob("**/trace.md")):
            text = read_text(trace_path)
            if any(change_id in text for change_id in change_ids):
                candidate = candidate_from_dir(kind, trace_path.parent)
                if candidate:
                    candidates.append(candidate)
    return candidates


def collect_candidates(root: Path, args: argparse.Namespace) -> list[IssueCandidate]:
    req_ids = list(dict.fromkeys(args.req))
    bug_ids = list(dict.fromkeys(args.bug))
    change_ids = list(dict.fromkeys(args.change))

    if args.sprint:
        sprint_reqs, sprint_bugs, sprint_changes = sprint_issue_ids(root, args.sprint)
        req_ids = list(dict.fromkeys([*req_ids, *sprint_reqs]))
        bug_ids = list(dict.fromkeys([*bug_ids, *sprint_bugs]))
        change_ids = list(dict.fromkeys([*change_ids, *sprint_changes]))

    candidates: list[IssueCandidate] = []
    for kind, ids in (("req", req_ids), ("bug", bug_ids)):
        for issue_id in ids:
            issue_dir = find_issue_dir(root, kind, issue_id)
            if not issue_dir:
                continue
            candidate = candidate_from_dir(kind, issue_dir)
            if candidate:
                candidates.append(candidate)

    candidates.extend(candidates_for_changes(root, change_ids))
    unique: dict[Path, IssueCandidate] = {}
    for candidate in candidates:
        unique[candidate.path] = candidate
    return sorted(unique.values(), key=lambda item: item.path.as_posix())


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


def all_changes_archived(root: Path, issue: IssueCandidate) -> tuple[bool, list[str]]:
    if not issue.change_ids:
        return False, ["no referenced OpenSpec changes found"]
    missing = [
        change_id
        for change_id in issue.change_ids
        if not find_archived_change(root, change_id)
    ]
    return not missing, missing


def replace_yaml_scalar(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^({re.escape(key)}:\s*).*$")
    replacement = rf"\g<1>{value}"
    new_text, count = pattern.subn(replacement, text, count=1)
    return new_text if count else text


def rewrite_trace_for_archive(text: str, reason: str) -> str:
    after = replace_yaml_scalar(text, "status", "done")
    after = replace_yaml_scalar(after, "lifecycle_stage", "archive")
    if after == text:
        return after
    note = f"\n- 归档同步：{reason}\n"
    if "## 变更记录" in after and note.strip() not in after:
        after = after.rstrip() + note
    return after


def build_promotions(root: Path, candidates: list[IssueCandidate], args: argparse.Namespace, report: Report) -> list[Promotion]:
    promotions: list[Promotion] = []
    for issue in candidates:
        rel = issue.path.relative_to(root).as_posix()
        base = root / ISSUE_TYPES[issue.kind][0]
        current_stage = issue.path.parent.name if issue.path.parent.name in STAGES else "legacy"
        if issue.path.parent.name == "archive":
            report.skipped.append(f"{rel} (already in archive)")
            continue
        if current_stage not in {"review", "legacy"} or issue.path.parent not in {base, base / "review"}:
            report.blocked.append(f"{rel} (stage is {current_stage}, expected review)")
            continue
        ok, missing = all_changes_archived(root, issue)
        if not ok:
            report.blocked.append(f"{rel} (unarchived changes: {', '.join(missing)})")
            continue
        target = root / ISSUE_TYPES[issue.kind][0] / "archive" / issue.path.name
        if target.exists():
            report.blocked.append(f"{rel} (target exists: {target.relative_to(root).as_posix()})")
            continue
        before = read_text(issue.trace_path)
        after = rewrite_trace_for_archive(before, args.reason)
        promotions.append(Promotion(issue, target, before, after, args.reason))
    return promotions


def diff_trace(promotion: Promotion, root: Path) -> str:
    rel = promotion.issue.trace_path.relative_to(root).as_posix()
    return "".join(
        difflib.unified_diff(
            promotion.trace_before.splitlines(True),
            promotion.trace_after.splitlines(True),
            fromfile=f"a/{rel}",
            tofile=f"b/{rel}",
        )
    )


def apply_promotions(root: Path, promotions: list[Promotion], args: argparse.Namespace, report: Report) -> int:
    if not promotions:
        return 0

    if args.check:
        for promotion in promotions:
            report.drift.append(f"{promotion.issue.path.relative_to(root)} -> {promotion.target.relative_to(root)}")
            print(diff_trace(promotion, root))
        return 1

    if args.dry_run:
        for promotion in promotions:
            print(f"Would promote {promotion.issue.path.relative_to(root)} -> {promotion.target.relative_to(root)}")
            print(diff_trace(promotion, root))
        return 0

    for promotion in promotions:
        if promotion.trace_before != promotion.trace_after:
            write_text(promotion.issue.trace_path, promotion.trace_after)
        promotion.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(promotion.issue.path), str(promotion.target))
        report.promoted.append(f"{promotion.issue.path.relative_to(root)} -> {promotion.target.relative_to(root)}")
    return 0


def print_report(args: argparse.Namespace, report: Report) -> None:
    print("## Issue Stage Promotion")
    print(f"Target: {args.to}")
    if report.promoted:
        print("Promoted:")
        for item in report.promoted:
            print(f"- {item}")
    else:
        print("Promoted: none")
    if report.drift:
        print("Drift:")
        for item in report.drift:
            print(f"- {item}")
    if report.blocked:
        print("Blocked:")
        for item in report.blocked:
            print(f"- {item}")
    if report.skipped:
        print("Skipped:")
        for item in report.skipped:
            print(f"- {item}")


def main() -> int:
    args = parse_args()
    root = find_root(Path.cwd())
    report = Report()
    candidates = collect_candidates(root, args)
    if not candidates:
        report.skipped.append("no issue candidates discovered")
        print_report(args, report)
        return 0
    promotions = build_promotions(root, candidates, args, report)
    exit_code = apply_promotions(root, promotions, args, report)
    print_report(args, report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
