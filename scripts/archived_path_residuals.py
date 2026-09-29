from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from workflow_sync import collect


ROOT = Path(__file__).resolve().parents[1]
SPRINT_FILES = ("sprint.yaml", "sprint.md", "release-note.md", "acceptance-report.md")


@dataclass(frozen=True)
class ExpectedPath:
    kind: str
    target: str
    old_path: str
    new_path: str | None


@dataclass(frozen=True)
class ResidualHit:
    kind: str
    target: str
    file: str
    line: int
    old_path: str
    new_path: str | None
    context: str


@dataclass(frozen=True)
class ResidualReport:
    sprint_id: str
    sprint_path: str
    checked_files: int
    residual_count: int
    expected_paths: list[ExpectedPath]
    residuals: list[ResidualHit]

    @property
    def ok(self) -> bool:
        return self.residual_count == 0


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def iter_markdown_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix == ".md" else []
    if not path.is_dir():
        return []
    return sorted(item for item in path.rglob("*.md") if item.is_file())


def active_change_path(change_id: str) -> str:
    return f"openspec/changes/{change_id}/"


def archived_change_dir(root: Path, change_id: str) -> Path | None:
    for archive_root in (
        root / "openspec" / "archive",
        root / "openspec" / "changes" / "archive",
    ):
        if not archive_root.exists():
            continue
        matches = sorted(archive_root.glob(f"*-{change_id}"))
        if matches:
            return matches[-1]
    return None


def load_sprint_record(root: Path, sprint_id: str) -> collect.SprintRecord:
    previous_root = collect.ROOT
    collect.ROOT = root
    try:
        sprint = collect.load_sprint(sprint_id)
    finally:
        collect.ROOT = previous_root
    if sprint is None:
        raise FileNotFoundError(f"sprint.yaml not found for: {sprint_id}")
    return sprint


def load_issues(root: Path) -> dict[str, collect.IssueRecord]:
    previous_root = collect.ROOT
    collect.ROOT = root
    try:
        return collect.load_all_issues()
    finally:
        collect.ROOT = previous_root


def issue_paths(issues: dict[str, collect.IssueRecord], issue_ids: list[str]) -> list[Path]:
    paths: list[Path] = []
    for issue_id in issue_ids:
        issue = issues.get(issue_id)
        if issue:
            paths.append(issue.path)
    return paths


def change_paths(root: Path, change_ids: list[str]) -> list[Path]:
    paths: list[Path] = []
    for change_id in change_ids:
        active = root / "openspec" / "changes" / change_id
        archived = archived_change_dir(root, change_id)
        if active.exists():
            paths.append(active)
        if archived and archived.exists():
            paths.append(archived)
    return paths


def collect_files(root: Path, sprint: collect.SprintRecord, issues: dict[str, collect.IssueRecord]) -> list[Path]:
    files: set[Path] = set()
    for name in SPRINT_FILES:
        path = sprint.path / name
        if path.exists():
            files.add(path)
    for path in issue_paths(issues, [*sprint.requirements, *sprint.bugs]):
        files.update(iter_markdown_files(path))
    for path in change_paths(root, sprint.changes):
        files.update(iter_markdown_files(path))
    return sorted(files)


def expected_paths(root: Path, sprint: collect.SprintRecord) -> list[ExpectedPath]:
    expectations = [
        ExpectedPath(
            kind="sprint-change-path",
            target=sprint.sprint_id,
            old_path=f"iterations/change/{sprint.sprint_id}/",
            new_path=f"iterations/archive/{sprint.sprint_id}/",
        )
    ]
    for change_id in sprint.changes:
        archived = archived_change_dir(root, change_id)
        expectations.append(
            ExpectedPath(
                kind="active-change-path",
                target=change_id,
                old_path=active_change_path(change_id),
                new_path=f"{rel(archived, root)}/" if archived else None,
            )
        )
        if archived and "openspec/changes/archive" not in rel(archived, root):
            legacy_old_path = f"openspec/changes/archive/{archived.name}/"
            expectations.append(
                ExpectedPath(
                    kind="legacy-change-archive-path",
                    target=change_id,
                    old_path=legacy_old_path,
                    new_path=f"{rel(archived, root)}/",
                )
            )
    return expectations


def line_has_path(line: str, path: str) -> bool:
    return re.search(rf"(?<![\w./-]){re.escape(path)}", line) is not None


def scan_file(path: Path, root: Path, expectations: list[ExpectedPath]) -> list[ResidualHit]:
    hits: list[ResidualHit] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for expected in expectations:
            if line_has_path(raw, expected.old_path):
                hits.append(
                    ResidualHit(
                        kind=expected.kind,
                        target=expected.target,
                        file=rel(path, root),
                        line=line_no,
                        old_path=expected.old_path,
                        new_path=expected.new_path,
                        context=raw.strip(),
                    )
                )
    return hits


def build_report(sprint_id: str, *, root: Path = ROOT) -> ResidualReport:
    root = root.resolve()
    sprint = load_sprint_record(root, sprint_id)
    issues = load_issues(root)
    expectations = expected_paths(root, sprint)
    files = collect_files(root, sprint, issues)
    residuals: list[ResidualHit] = []
    for path in files:
        residuals.extend(scan_file(path, root, expectations))
    return ResidualReport(
        sprint_id=sprint.sprint_id,
        sprint_path=rel(sprint.path, root),
        checked_files=len(files),
        residual_count=len(residuals),
        expected_paths=expectations,
        residuals=residuals,
    )


def report_to_dict(report: ResidualReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["ok"] = report.ok
    return payload


def render_markdown(report: ResidualReport) -> str:
    lines = [
        "## Archived Path Residual Report",
        "",
        f"**Sprint:** {report.sprint_id}",
        f"**Sprint Path:** `{report.sprint_path}`",
        f"**Checked Files:** {report.checked_files}",
        f"**Residuals:** {report.residual_count}",
        f"**Verdict:** {'PASS' if report.ok else 'BLOCKED'}",
    ]
    if report.residuals:
        lines.extend(
            [
                "",
                "| Kind | Target | File | Line | Old Path | Suggested Path |",
                "|---|---|---|---:|---|---|",
            ]
        )
        for hit in report.residuals:
            lines.append(
                f"| {hit.kind} | {hit.target} | `{hit.file}` | {hit.line} | "
                f"`{hit.old_path}` | `{hit.new_path or 'unresolved'}` |"
            )
        lines.extend(
            [
                "",
                "Fix the stale links above, then rerun:",
                f"`python scripts/check-archived-path-residuals.py --sprint {report.sprint_id}`",
            ]
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check archived Sprint documents for stale change-path links.")
    parser.add_argument("--sprint", required=True, help="Sprint id, e.g. sprint-005")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_report(args.sprint, root=args.root)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", flush=True)
        return 2
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
