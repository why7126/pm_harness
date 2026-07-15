from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constants import ROOT

# issues/requirements 与 issues/bugs 下的生命周期阶段子目录（见 rules/issues-lifecycle.md）
ISSUE_STAGE_DIRS = frozenset({"plan", "review", "archive"})
ISSUE_DIR_PREFIXES = ("REQ-", "BUG-")


def is_issue_stage_dir(name: str) -> bool:
    return name in ISSUE_STAGE_DIRS


def is_issue_id_dir(name: str) -> bool:
    return name.startswith(ISSUE_DIR_PREFIXES)


def iter_issue_dirs(base: Path):
    """Yield REQ/BUG issue directories (legacy flat or plan/review/archive)."""
    if not base.is_dir():
        return
    for path in sorted(base.iterdir()):
        if not path.is_dir() or path.name.startswith("_"):
            continue
        if is_issue_stage_dir(path.name):
            for staged in sorted(path.iterdir()):
                if staged.is_dir() and is_issue_id_dir(staged.name):
                    yield staged
        elif is_issue_id_dir(path.name):
            yield path


def resolve_issue_dir(base_rel: str, issue_id: str) -> Path | None:
    """Resolve issue directory across legacy flat and staged layouts."""
    base = ROOT / base_rel
    for candidate in (
        base / issue_id,
        base / "plan" / issue_id,
        base / "review" / issue_id,
        base / "archive" / issue_id,
    ):
        if candidate.is_dir():
            return candidate
    matches = [
        p
        for p in iter_issue_dirs(base)
        if p.name == issue_id or p.name.startswith(f"{issue_id}-") or issue_id in p.name
    ]
    if len(matches) == 1:
        return matches[0]
    return None


@dataclass
class TaskProgress:
    done: int = 0
    total: int = 0


@dataclass
class ChangeRecord:
    change_id: str
    location: str  # active | archived | missing
    archive_dir: str | None = None
    archive_date: str | None = None
    tasks: TaskProgress = field(default_factory=TaskProgress)
    openspec_status: str | None = None
    linked_req: str | None = None
    linked_bug: str | None = None


@dataclass
class IssueRecord:
    issue_id: str
    kind: str  # req | bug
    path: Path
    title: str = ""
    priority: str = "P1"
    trace_status: str | None = None
    openspec_changes: list[dict[str, Any]] = field(default_factory=list)
    related_changes: list[str] = field(default_factory=list)
    related_requirement: str | None = None
    related_change: str | None = None


@dataclass
class SprintRecord:
    sprint_id: str
    path: Path
    status: str
    requirements: list[str] = field(default_factory=list)
    bugs: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def parse_frontmatter_yaml(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    return parse_simple_yaml(match.group(1))


def parse_yaml_block(text: str) -> dict[str, Any] | None:
    match = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
    if not match:
        return None
    return parse_simple_yaml(match.group(1))


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    """Minimal YAML parser for trace.md blocks (no external deps)."""

    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    current_key: str | None = None
    list_item: dict[str, Any] | None = None

    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
            list_item = None

        container = stack[-1][1]

        if content.startswith("- "):
            item_text = content[2:]
            if not isinstance(container, list):
                continue
            if ":" in item_text:
                item: dict[str, Any] = {}
                key, value = item_text.split(":", 1)
                item[key.strip()] = coerce_scalar(value.strip())
                container.append(item)
                list_item = item
                stack.append((indent, item))
            else:
                container.append(coerce_scalar(item_text))
            continue

        if ":" not in content:
            continue
        key, value = content.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            new_list: list[Any] = []
            if isinstance(container, dict):
                container[key] = new_list
            stack.append((indent, new_list))
            current_key = key
            continue

        if value == "[]":
            if isinstance(container, dict):
                container[key] = []
            continue

        scalar = coerce_scalar(value)
        if isinstance(container, dict):
            container[key] = scalar

    return root


def coerce_scalar(value: str) -> Any:
    if value in {"null", "~", ""}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def count_tasks(tasks_path: Path) -> TaskProgress:
    if not tasks_path.exists():
        return TaskProgress()
    text = read_text(tasks_path)
    done = len(re.findall(r"^- \[x\]", text, re.MULTILINE))
    total = len(re.findall(r"^- \[[ x]\]", text, re.MULTILINE))
    return TaskProgress(done=done, total=total)


def run_openspec_list() -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["openspec", "list", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return {"changes": []}
    if proc.returncode != 0:
        return {"changes": []}
    return json.loads(proc.stdout or '{"changes": []}')


def find_archived_change_dir(change_id: str) -> Path | None:
    archive_root = ROOT / "openspec/changes/archive"
    if not archive_root.exists():
        return None
    matches = sorted(archive_root.glob(f"*-{change_id}"))
    return matches[-1] if matches else None


def extract_archive_date(archive_dir: Path) -> str | None:
    name = archive_dir.name
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-", name)
    return match.group(1) if match else None


LIFECYCLE_ARCHIVE_KEYS = ("archived", "opsx_archived")
LIFECYCLE_FALLBACK_KEYS = ("completed", "reviewed", "approved")
TRACE_DONE_STATUSES = frozenset({"archived", "done", "resolved", "closed"})


def _lifecycle_timestamp(lifecycle: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = lifecycle.get(key)
        if value and str(value).strip().lower() not in {"null", "none"}:
            return str(value).strip()
    return None


def _latest_changelog_timestamp(text: str) -> str | None:
    latest: str | None = None
    for match in re.finditer(
        r"^\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        text,
        re.MULTILINE,
    ):
        candidate = match.group(1)
        if latest is None or candidate > latest:
            latest = candidate
    return latest


def extract_trace_timestamp(
    trace_path: Path,
    *,
    include_frontmatter_updated_at: bool = True,
) -> str | None:
    """Resolve the best available timestamp from a trace.md (issue or change)."""

    if not trace_path.exists():
        return None
    text = read_text(trace_path)
    fm = parse_frontmatter(text)
    block = parse_yaml_block(text)
    if block:
        lifecycle = block.get("lifecycle")
        if isinstance(lifecycle, dict):
            explicit = _lifecycle_timestamp(lifecycle, LIFECYCLE_ARCHIVE_KEYS)
            if explicit:
                return explicit
            fallback = _lifecycle_timestamp(lifecycle, LIFECYCLE_FALLBACK_KEYS)
            if fallback:
                return fallback
        for key in (*LIFECYCLE_ARCHIVE_KEYS, *LIFECYCLE_FALLBACK_KEYS):
            value = block.get(key)
            if value and str(value).strip().lower() not in {"null", "none"}:
                return str(value).strip()

    for key in LIFECYCLE_ARCHIVE_KEYS:
        match = re.search(
            rf"^\s*{re.escape(key)}:\s*(\d{{4}}-\d{{2}}-\d{{2}}(?:\s+\d{{2}}:\d{{2}}:\d{{2}})?)\s*$",
            text,
            re.MULTILINE,
        )
        if match:
            return match.group(1).strip()

    changelog_timestamp = _latest_changelog_timestamp(text)
    if changelog_timestamp:
        return changelog_timestamp

    status = (block or {}).get("status") or fm.get("status") or ""
    if include_frontmatter_updated_at and str(status).strip().lower() in TRACE_DONE_STATUSES:
        updated_at = fm.get("updated_at")
        if updated_at:
            return updated_at.strip()

    return None


def lifecycle_archived_from_trace(trace_path: Path) -> str | None:
    return extract_trace_timestamp(trace_path)


def resolve_archive_timestamp(
    archived_path: Path,
    change_id: str,
    linked_req: str | None,
    linked_bug: str | None,
    issues: dict[str, IssueRecord],
) -> str | None:
    from .timefmt import ARCHIVE_DATE_ONLY_FALLBACK, normalize_datetime

    change_trace = archived_path / "trace.md"
    candidates: list[str | None] = [
        extract_trace_timestamp(change_trace, include_frontmatter_updated_at=False),
    ]
    if linked_bug and linked_bug in issues:
        candidates.append(
            extract_trace_timestamp(
                issues[linked_bug].path / "trace.md",
                include_frontmatter_updated_at=False,
            )
        )
    if linked_req and linked_req in issues:
        candidates.append(
            extract_trace_timestamp(
                issues[linked_req].path / "trace.md",
                include_frontmatter_updated_at=False,
            )
        )
    for issue in issues.values():
        linked = any(oc.get("change_id") == change_id for oc in issue.openspec_changes)
        if not linked and change_id in issue.related_changes:
            linked = True
        if not linked and issue.related_change == change_id:
            linked = True
        if linked:
            candidates.append(
                extract_trace_timestamp(
                    issue.path / "trace.md",
                    include_frontmatter_updated_at=False,
                )
            )

    dir_date = extract_archive_date(archived_path)
    if dir_date:
        candidates.append(dir_date)

    for raw in candidates:
        if not raw:
            continue
        normalized = normalize_datetime(raw, default_time=ARCHIVE_DATE_ONLY_FALLBACK)
        if normalized:
            return normalized
    return None


def load_issue_record(path: Path, kind: str) -> IssueRecord | None:
    if not path.is_dir():
        return None
    issue_id = path.name
    title = issue_id
    priority = "P1"
    req_md = path / "requirement.md"
    bug_md = path / "bug.md"
    capture_md = path / "capture.md"
    for candidate in (req_md, bug_md, capture_md):
        if candidate.exists():
            fm = parse_frontmatter(read_text(candidate))
            if fm.get("title"):
                title = fm["title"]
            if fm.get("priority"):
                priority = fm["priority"]
            if kind == "bug" and fm.get("severity"):
                priority = fm["severity"]
            break

    trace_path = path / "trace.md"
    trace_status = None
    openspec_changes: list[dict[str, Any]] = []
    related_requirement = None
    related_change = None
    related_changes: list[str] = []
    if trace_path.exists():
        trace_text = read_text(trace_path)
        fm = parse_frontmatter(trace_text)
        fm_block = parse_frontmatter_yaml(trace_text)
        trace_status = fm.get("status")
        raw_changes = fm_block.get("openspec_changes") or []
        if isinstance(raw_changes, list):
            openspec_changes = [c for c in raw_changes if isinstance(c, dict)]
        raw_related_changes = fm_block.get("related_changes") or []
        if isinstance(raw_related_changes, list):
            related_changes = [str(item).strip() for item in raw_related_changes if str(item).strip()]
        related_requirement = fm_block.get("related_requirement")
        related_change = fm_block.get("related_change")
        block = parse_yaml_block(trace_text)
        if block:
            trace_status = block.get("status") or trace_status
            raw_changes = block.get("openspec_changes") or []
            if isinstance(raw_changes, list):
                openspec_changes = [c for c in raw_changes if isinstance(c, dict)]
            raw_related_changes = block.get("related_changes") or []
            if isinstance(raw_related_changes, list):
                related_changes = [str(item).strip() for item in raw_related_changes if str(item).strip()]
            related_requirement = block.get("related_requirement")
            related_change = block.get("related_change")

    return IssueRecord(
        issue_id=issue_id,
        kind=kind,
        path=path,
        title=title,
        priority=str(priority),
        trace_status=trace_status,
        openspec_changes=openspec_changes,
        related_changes=related_changes if kind == "req" else [],
        related_requirement=related_requirement if kind == "bug" else None,
        related_change=related_change if kind == "bug" else None,
    )


def load_all_issues() -> dict[str, IssueRecord]:
    records: dict[str, IssueRecord] = {}
    for base, kind in (
        (ROOT / "issues/requirements", "req"),
        (ROOT / "issues/bugs", "bug"),
    ):
        for path in iter_issue_dirs(base):
            record = load_issue_record(path, kind)
            if record:
                records[record.issue_id] = record
    return records


def infer_change_links(change_id: str, issues: dict[str, IssueRecord]) -> tuple[str | None, str | None]:
    linked_req: str | None = None
    linked_bug: str | None = None
    for issue in issues.values():
        for oc in issue.openspec_changes:
            if oc.get("change_id") == change_id:
                if issue.kind == "req":
                    linked_req = issue.issue_id
                else:
                    linked_bug = issue.issue_id
        if issue.kind == "bug" and issue.related_change == change_id:
            linked_bug = issue.issue_id
            if issue.related_requirement:
                linked_req = str(issue.related_requirement)
    if linked_req or linked_bug:
        return linked_req, linked_bug

    active = ROOT / "openspec/changes" / change_id / "proposal.md"
    archived = find_archived_change_dir(change_id)
    proposal = active if active.exists() else (
        archived / "proposal.md" if archived and (archived / "proposal.md").exists() else None
    )
    if proposal and proposal.exists():
        text = read_text(proposal)
        req_match = re.search(r"(REQ-\d{4}(?:-[a-z0-9-]+)?)", text)
        bug_match = re.search(r"(BUG-\d{4}(?:-[a-z0-9-]+)?)", text)
        if req_match:
            linked_req = normalize_issue_id(req_match.group(1), "issues/requirements")
        if bug_match:
            linked_bug = normalize_issue_id(bug_match.group(1), "issues/bugs")
    return linked_req, linked_bug


def normalize_issue_id(short_or_full: str, base_rel: str) -> str:
    resolved = resolve_issue_dir(base_rel, short_or_full)
    if resolved is not None:
        return resolved.name
    base = ROOT / base_rel
    if (base / short_or_full).exists():
        return short_or_full
    prefix = short_or_full if short_or_full.count("-") >= 2 else None
    if not prefix:
        return short_or_full
    for path in iter_issue_dirs(base):
        if path.name.startswith(short_or_full.split("-")[0] + "-"):
            if path.name.startswith(short_or_full) or short_or_full in path.name:
                return path.name
    matches = [p.name for p in iter_issue_dirs(base) if short_or_full.split("-")[1] in p.name]
    return matches[0] if len(matches) == 1 else short_or_full


def load_change_record(change_id: str, issues: dict[str, IssueRecord], openspec_data: dict[str, Any]) -> ChangeRecord:
    active_path = ROOT / "openspec/changes" / change_id
    archived_path = find_archived_change_dir(change_id)
    openspec_entry = next(
        (c for c in openspec_data.get("changes", []) if c.get("name") == change_id),
        None,
    )
    linked_req, linked_bug = infer_change_links(change_id, issues)

    if archived_path:
        tasks = count_tasks(archived_path / "tasks.md")
        return ChangeRecord(
            change_id=change_id,
            location="archived",
            archive_dir=archived_path.name,
            archive_date=resolve_archive_timestamp(
                archived_path, change_id, linked_req, linked_bug, issues
            ),
            tasks=tasks,
            openspec_status="archived",
            linked_req=linked_req,
            linked_bug=linked_bug,
        )

    if active_path.exists():
        tasks = count_tasks(active_path / "tasks.md")
        if openspec_entry:
            tasks = TaskProgress(
                done=int(openspec_entry.get("completedTasks") or tasks.done),
                total=int(openspec_entry.get("totalTasks") or tasks.total),
            )
        return ChangeRecord(
            change_id=change_id,
            location="active",
            tasks=tasks,
            openspec_status=openspec_entry.get("status") if openspec_entry else "active",
            linked_req=linked_req,
            linked_bug=linked_bug,
        )

    return ChangeRecord(
        change_id=change_id,
        location="missing",
        tasks=TaskProgress(),
        openspec_status=None,
        linked_req=linked_req,
        linked_bug=linked_bug,
    )


def resolve_sprint_dir(sprint_id: str) -> Path | None:
    """Resolve sprint directory under change/archive or legacy flat path."""
    iterations = ROOT / "iterations"
    for stage in ("change", "archive"):
        candidate = iterations / stage / sprint_id
        if (candidate / "sprint.yaml").exists():
            return candidate
    legacy = iterations / sprint_id
    if (legacy / "sprint.yaml").exists():
        return legacy
    return None


def list_sprint_ids() -> list[str]:
    iterations = ROOT / "iterations"
    if not iterations.exists():
        return []
    ids: set[str] = set()
    for stage in ("change", "archive"):
        for path in iterations.glob(f"{stage}/sprint-*/sprint.yaml"):
            ids.add(path.parent.name)
    for path in iterations.glob("sprint-*/sprint.yaml"):
        ids.add(path.parent.name)
    return sorted(ids)


def find_sprints_for_issue(issue_id: str) -> list[str]:
    matches: list[str] = []
    for sprint_id in list_sprint_ids():
        sprint = load_sprint(sprint_id)
        if not sprint:
            continue
        if issue_id in sprint.requirements or issue_id in sprint.bugs:
            matches.append(sprint_id)
    return matches


def find_sprints_for_change(change_id: str) -> list[str]:
    matches: list[str] = []
    for sprint_id in list_sprint_ids():
        sprint = load_sprint(sprint_id)
        if sprint and change_id in sprint.changes:
            matches.append(sprint_id)
    return matches


def _pick_preferred_sprint(candidates: list[str]) -> str | None:
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    in_progress = [
        sprint_id
        for sprint_id in candidates
        if (record := load_sprint(sprint_id)) and record.status == "in_progress"
    ]
    if len(in_progress) == 1:
        return in_progress[0]
    return candidates[-1]


def resolve_in_progress_sprint_id() -> str | None:
    in_progress: list[str] = []
    for sprint_id in list_sprint_ids():
        sprint = load_sprint(sprint_id)
        if sprint and sprint.status == "in_progress":
            in_progress.append(sprint_id)
    if len(in_progress) == 1:
        return in_progress[0]
    if len(in_progress) > 1:
        return in_progress[-1]
    sprint_ids = list_sprint_ids()
    return sprint_ids[-1] if sprint_ids else None


def resolve_sprint_id(
    sprint_id: str | None,
    *,
    event: str | None = None,
    req_id: str | None = None,
    bug_id: str | None = None,
    change_id: str | None = None,
) -> tuple[str | None, str | None]:
    """Return (sprint_id, skip_reason). skip_reason is set when sprint sync is intentionally skipped."""

    from .constants import CHANGE_SCOPED_EVENTS, ISSUE_SCOPED_EVENTS

    if sprint_id and sprint_id not in {"auto", "none"}:
        return sprint_id, None

    if sprint_id == "none":
        return None, "explicitly skipped (`--sprint none`)"

    issue_id = req_id or bug_id
    if event in ISSUE_SCOPED_EVENTS and issue_id:
        matches = find_sprints_for_issue(issue_id)
        if not matches:
            parts = issue_id.split("-", 2)
            short = f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else issue_id
            return None, f"skipped — {short} not in sprint scope"
        return _pick_preferred_sprint(matches), None

    if event in CHANGE_SCOPED_EVENTS and change_id:
        matches = find_sprints_for_change(change_id)
        if not matches:
            return None, f"skipped — change `{change_id}` not in sprint scope"
        return _pick_preferred_sprint(matches), None

    return resolve_in_progress_sprint_id(), None


def load_sprint(sprint_id: str) -> SprintRecord | None:
    sprint_path = resolve_sprint_dir(sprint_id)
    if sprint_path is None:
        return None
    yaml_path = sprint_path / "sprint.yaml"
    block = parse_simple_yaml(read_text(yaml_path))
    return SprintRecord(
        sprint_id=sprint_id,
        path=sprint_path,
        status=str(block.get("status") or "planning"),
        requirements=list(block.get("requirements") or []),
        bugs=list(block.get("bugs") or []),
        changes=list(block.get("changes") or []),
    )


def load_registry(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not path.exists():
        return {"next_id": 1, "entries": []}, []
    block = parse_simple_yaml(read_text(path))
    entries = block.get("entries") or []
    if not isinstance(entries, list):
        entries = []
    return block, entries
