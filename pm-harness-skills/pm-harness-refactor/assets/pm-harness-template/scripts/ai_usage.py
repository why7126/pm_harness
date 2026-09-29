"""Extract redacted AI command usage facts from local Codex session JSONL."""

from __future__ import annotations

import argparse
import os
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from workflow_sync import collect as workflow_collect
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from workflow_sync import collect as workflow_collect


TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)
COUNT_FIELDS = (
    "command_run_count",
    "model_call_count",
    "tool_call_count",
    "retry_count",
)
SPRINT_MATRIX_COMMAND_COLUMNS = (
    ("capture", "Capture"),
    ("bug.capture", "BUG-Capture"),
    ("req.capture", "REQ-Capture"),
    ("bug.explore", "BUG-Explore"),
    ("req.explore", "REQ-Explore"),
    ("req.generate", "REQ-Generate"),
    ("bug.generate", "BUG-Generate"),
    ("req.complete", "REQ-Complete"),
    ("bug.complete", "BUG-Complete"),
    ("req.review", "REQ-Review"),
    ("bug.review", "BUG-Review"),
    ("req.opsx", "REQ-Opsx"),
    ("bug.opsx", "BUG-Opsx"),
    ("opsx.explore", "Opsx-Explore"),
    ("opsx.propose", "Opsx-Propose"),
    ("opsx.apply", "Opsx-Apply"),
    ("opsx.modify", "Opsx-Modify"),
    ("opsx.archive", "Opsx-Archive"),
    ("sprint.propose", "Sprint-Propose"),
    ("sprint.explore", "Sprint-Explore"),
    ("sprint.apply", "Sprint-Apply"),
    ("sprint.archive", "Sprint-Archive"),
)
SPRINT_MATRIX_METRICS = (
    "total_tokens",
    "input_tokens",
    "output_tokens",
    "model_call_count",
)

USAGE_MODE_ACTUAL = "actual"
USAGE_MODE_ESTIMATED = "estimated_fallback"
USAGE_MODE_UNAVAILABLE = "unavailable"

REQ_RE = re.compile(r"\bREQ-\d{4,}[A-Za-z0-9_-]*\b")
BUG_RE = re.compile(r"\bBUG-\d{4,}[A-Za-z0-9_-]*\b")
ISSUE_SHORT_RE = re.compile(r"\b((?:REQ|BUG)-\d{4,})")
SPRINT_RE = re.compile(r"\bsprint-\d{3,}\b")
RELEASE_RE = re.compile(r"\bv\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?\b")
EVENT_RE = re.compile(
    r"(?:^|\s)--event\s+(?P<event>[a-z][a-z0-9_.-]*)"
    r"|(?:^|\s)/(?P<slash_family>req|bug|opsx|sprint|release|image)-(?P<slash_action>[a-z0-9-]+)"
    r"|(?:^|\s)\[\$(?P<link_family>req|bug|opsx|sprint|release|image)-(?P<link_action>[a-z0-9-]+)\]"
)
SECRET_RE = re.compile(
    r"(\bauthorization\b|\bbearer\s+[A-Za-z0-9._-]+|\bcookie\b|\.env\b"
    r"|(?:secret|password|api[_-]?key|access[_-]?key|token)\s*[:=]"
    r"|\b[A-Z0-9_]*(?:SECRET|PASSWORD|TOKEN|API_KEY|ACCESS_KEY)[A-Z0-9_]*\s*[:=])",
    re.IGNORECASE,
)
ABS_PATH_RE = re.compile(r"(/Users/|/home/|/private/|[A-Za-z]:\\)")
CHANGE_RE = re.compile(r"\b(?:add|update|fix|build|archive|refine|implement|create)-[a-z0-9][a-z0-9-]{2,}\b")
UNSAFE_PERSISTED_KEYS = {
    "prompt",
    "system_prompt",
    "system_instruction",
    "developer_instruction",
    "developer_message",
    "session_jsonl",
    "raw_session",
    "tool_output_body",
    "tool_output_text",
}

AUTO_SESSION_SCAN_LIMIT = 300
_ISSUE_CANONICAL_CACHE: dict[Path, dict[str, str]] = {}
_CHANGE_ISSUE_LINK_CACHE: dict[Path, dict[str, dict[str, set[str]]]] = {}


def issue_short_id(value: str) -> str | None:
    match = ISSUE_SHORT_RE.search(value)
    return match.group(1) if match else None


def issue_canonical_map(root: Path | None = None) -> dict[str, str]:
    """Map unique short issue IDs to their full directory-backed canonical IDs."""

    base = (root or Path.cwd()).resolve()
    cached = _ISSUE_CANONICAL_CACHE.get(base)
    if cached is not None:
        return cached

    candidates: dict[str, set[str]] = {}
    for issue_root in (base / "issues" / "requirements", base / "issues" / "bugs"):
        if not issue_root.exists():
            continue
        for path in issue_root.glob("*/*"):
            if not path.is_dir():
                continue
            short = issue_short_id(path.name)
            if short:
                candidates.setdefault(short, set()).add(path.name)

    canonical = {
        short: next(iter(values))
        for short, values in candidates.items()
        if len(values) == 1 and next(iter(values)) != short
    }
    _ISSUE_CANONICAL_CACHE[base] = canonical
    return canonical


def canonicalize_issue_ids(values: list[str] | set[str], canonical_map: dict[str, str] | None = None) -> list[str]:
    canonical_map = canonical_map if canonical_map is not None else issue_canonical_map()
    grouped: dict[str, set[str]] = {}
    passthrough: set[str] = set()
    for value in values:
        text = str(value)
        short = issue_short_id(text)
        if not short:
            passthrough.add(text)
            continue
        grouped.setdefault(short, set()).add(canonical_map.get(short, text))

    normalized = set(passthrough)
    for short, aliases in grouped.items():
        preferred = canonical_map.get(short)
        if preferred:
            normalized.add(preferred)
            continue
        full_aliases = [alias for alias in aliases if alias != short]
        normalized.add(sorted(full_aliases or aliases, key=lambda item: (len(item), item))[-1])
    return sorted(normalized)


def _read_text_safely(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _extract_change_links_from_text(text: str) -> tuple[set[str], set[str]]:
    requirements = {
        match.group(2)
        for match in re.finditer(r"^\s*source_requirement:\s*(`?)(REQ-\d{4,}[A-Za-z0-9_-]*)\1\s*$", text, re.MULTILINE)
    }
    bugs = {
        match.group(2)
        for match in re.finditer(r"^\s*source_bug:\s*(`?)(BUG-\d{4,}[A-Za-z0-9_-]*)\1\s*$", text, re.MULTILINE)
    }
    return set(canonicalize_issue_ids(requirements)), set(canonicalize_issue_ids(bugs))


def _change_text_paths(base: Path, change_id: str) -> list[Path]:
    paths = [
        base / "openspec" / "changes" / change_id / "trace.md",
        base / "openspec" / "changes" / change_id / "proposal.md",
    ]
    for archive_root in (
        base / "openspec" / "archive",
        base / "openspec" / "changes" / "archive",
    ):
        if archive_root.exists():
            for archived in sorted(archive_root.glob(f"*-{change_id}")):
                paths.extend([archived / "trace.md", archived / "proposal.md"])
    return paths


def _known_change_dirs(base: Path) -> list[tuple[str, Path]]:
    changes_root = base / "openspec" / "changes"
    if not changes_root.exists():
        return []

    items: list[tuple[str, Path]] = []
    for change_dir in changes_root.glob("*"):
        if change_dir.is_dir() and change_dir.name != "archive":
            items.append((change_dir.name, change_dir))

    for archive_root in (
        base / "openspec" / "archive",
        changes_root / "archive",
    ):
        if archive_root.exists():
            for change_dir in archive_root.glob("*"):
                if not change_dir.is_dir():
                    continue
                change_id = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", change_dir.name)
                items.append((change_id, change_dir))

    return sorted(items, key=lambda item: (item[0], str(item[1])))


def change_issue_links(root: Path | None = None) -> dict[str, dict[str, set[str]]]:
    base = (root or Path.cwd()).resolve()
    cached = _CHANGE_ISSUE_LINK_CACHE.get(base)
    if cached is not None:
        return cached

    links: dict[str, dict[str, set[str]]] = {}

    for issue_root, key in (
        (base / "issues" / "requirements", "requirements"),
        (base / "issues" / "bugs", "bugs"),
    ):
        if not issue_root.exists():
            continue
        for trace in issue_root.glob("*/*/trace.md"):
            issue_id = canonicalize_issue_ids({trace.parent.name})[0]
            text = _read_text_safely(trace)
            change_ids = {
                match.group(1)
                for match in re.finditer(r"^\s*(?:-\s*)?(?:change_id|related_change):\s*([a-z0-9][a-z0-9-]{2,})\s*$", text, re.MULTILINE)
            }
            for change_id in change_ids:
                bucket = links.setdefault(change_id, {"requirements": set(), "bugs": set()})
                bucket[key].add(issue_id)

    for change_id, change_dir in _known_change_dirs(base):
        text = "\n".join(
            [
                _read_text_safely(change_dir / "trace.md"),
                _read_text_safely(change_dir / "proposal.md"),
                *(_read_text_safely(path) for path in _change_text_paths(base, change_id)),
            ]
        )
        requirements, bugs = _extract_change_links_from_text(text)
        if requirements or bugs:
            bucket = links.setdefault(change_id, {"requirements": set(), "bugs": set()})
            bucket["requirements"].update(requirements)
            bucket["bugs"].update(bugs)

    _CHANGE_ISSUE_LINK_CACHE[base] = links
    return links


def enrich_opsx_issue_links(record: dict[str, Any]) -> dict[str, Any]:
    workflow_event = str(record.get("workflow_event") or record.get("command") or "")
    if not workflow_event.startswith("opsx."):
        return record
    changes = [str(item) for item in record.get("changes", []) if str(item).strip()]
    if not changes:
        return record

    links = change_issue_links()
    requirements = set(str(item) for item in record.get("requirements", []))
    bugs = set(str(item) for item in record.get("bugs", []))
    for change_id in changes:
        linked = links.get(change_id)
        if not linked:
            continue
        requirements.update(linked.get("requirements", set()))
        bugs.update(linked.get("bugs", set()))
    record["requirements"] = sorted(requirements)
    record["bugs"] = sorted(bugs)
    return record


def normalize_record_issues(record: dict[str, Any]) -> dict[str, Any]:
    enrich_opsx_issue_links(record)
    for key in ("requirements", "bugs"):
        if isinstance(record.get(key), list):
            record[key] = canonicalize_issue_ids(record[key])
    return record


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_record_issues(record) for record in records]


def model_speed_tier(model_name: str | None = None, rate_limit_name: str | None = None) -> str | None:
    text = (model_name or "").lower()
    if "spark" in text:
        return "ultra_fast"
    if "luna" in text or "mini" in text:
        return "fast"
    if "terra" in text:
        return "balanced"
    if "sol" in text or "gpt-5.5" in text:
        return "frontier"
    text = (rate_limit_name or "").lower()
    if "spark" in text:
        return "ultra_fast"
    if "luna" in text or "mini" in text:
        return "fast"
    if "terra" in text:
        return "balanced"
    if "sol" in text or "gpt-5.5" in text:
        return "frontier"
    return None


def extract_model_metadata(row: dict[str, Any]) -> dict[str, str | int]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    settings = payload.get("thread_settings") if isinstance(payload.get("thread_settings"), dict) else {}
    collaboration = payload.get("collaboration_mode") if isinstance(payload.get("collaboration_mode"), dict) else {}
    collaboration_settings = collaboration.get("settings") if isinstance(collaboration.get("settings"), dict) else {}
    rate_limits = payload.get("rate_limits") if isinstance(payload.get("rate_limits"), dict) else {}
    if not rate_limits and isinstance(row.get("rate_limits"), dict):
        rate_limits = row["rate_limits"]
    info = payload.get("info") if isinstance(payload.get("info"), dict) else {}

    metadata: dict[str, str | int] = {}
    for output_key, candidates in {
        "model_name": (payload.get("model"), settings.get("model"), collaboration_settings.get("model")),
        "model_provider": (payload.get("model_provider"), settings.get("model_provider_id")),
        "service_tier": (payload.get("service_tier"), settings.get("service_tier")),
        "reasoning_effort": (payload.get("reasoning_effort"), payload.get("effort"), settings.get("reasoning_effort"), collaboration_settings.get("reasoning_effort")),
        "reasoning_summary": (payload.get("reasoning_summary"), payload.get("summary"), settings.get("reasoning_summary")),
        "model_rate_limit_name": (rate_limits.get("limit_name"),),
        "model_rate_limit_id": (rate_limits.get("limit_id"),),
        "model_context_window": (payload.get("model_context_window"), info.get("model_context_window")),
    }.items():
        for value in candidates:
            if isinstance(value, (str, int)) and value != "":
                metadata[output_key] = value
                break

    speed = model_speed_tier(
        str(metadata.get("model_name")) if metadata.get("model_name") else None,
        str(metadata.get("model_rate_limit_name")) if metadata.get("model_rate_limit_name") else None,
    )
    if speed:
        metadata["model_speed_tier"] = speed
    return metadata


def apply_model_metadata(run: "CommandRun", metadata: dict[str, str | int]) -> None:
    for key, value in metadata.items():
        if key != "model_speed_tier" and hasattr(run, key) and value not in ("", None):
            setattr(run, key, value)
    speed = model_speed_tier(run.model_name, run.model_rate_limit_name)
    if speed:
        run.model_speed_tier = speed


def display_source_data_file(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return "~/" + str(resolved.relative_to(Path.home().resolve()))
    except ValueError:
        return path.name


@dataclass
class CommandRun:
    source_session_hash: str
    source_data_file: str
    source_line_start: int
    source_line_end: int
    turn_hash: str
    started_at: str | None = None
    ended_at: str | None = None
    command: str = "unknown"
    workflow_event: str | None = None
    requirements: set[str] = field(default_factory=set)
    bugs: set[str] = field(default_factory=set)
    changes: set[str] = field(default_factory=set)
    sprint_id: str | None = None
    release_sprints: set[str] = field(default_factory=set)
    release_version: str | None = None
    attribution_confidence: str = "low"
    model_name: str | None = None
    model_provider: str | None = None
    service_tier: str | None = None
    reasoning_effort: str | None = None
    reasoning_summary: str | None = None
    model_speed_tier: str | None = None
    model_rate_limit_name: str | None = None
    model_rate_limit_id: str | None = None
    model_context_window: int | None = None
    model_call_count: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_output_tokens: int = 0
    total_tokens: int = 0
    tool_call_count: int = 0
    tool_output_chars: int = 0
    retry_count: int = 0
    retry_count_method: str = "tool_result_error_count"
    warnings: list[str] = field(default_factory=list)
    _tool_errors: int = 0

    def to_record(self) -> dict[str, Any]:
        return {
            "source_session_hash": self.source_session_hash,
            "source_data_file": self.source_data_file,
            "source_line_start": self.source_line_start,
            "source_line_end": self.source_line_end,
            "turn_hash": self.turn_hash,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "command": self.command,
            "workflow_event": self.workflow_event,
            "requirements": sorted(self.requirements),
            "bugs": sorted(self.bugs),
            "changes": sorted(self.changes),
            "sprint_id": self.sprint_id,
            "release_sprints": sorted(self.release_sprints),
            "release_version": self.release_version,
            "attribution_confidence": self.attribution_confidence,
            "model_name": self.model_name,
            "model_provider": self.model_provider,
            "service_tier": self.service_tier,
            "reasoning_effort": self.reasoning_effort,
            "reasoning_summary": self.reasoning_summary,
            "model_speed_tier": self.model_speed_tier,
            "model_rate_limit_name": self.model_rate_limit_name,
            "model_rate_limit_id": self.model_rate_limit_id,
            "model_context_window": self.model_context_window,
            "model_call_count": self.model_call_count,
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_output_tokens": self.reasoning_output_tokens,
            "total_tokens": self.total_tokens,
            "tool_call_count": self.tool_call_count,
            "tool_output_chars": self.tool_output_chars,
            "retry_count": self.retry_count,
            "retry_count_method": self.retry_count_method,
        }


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def source_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def session_source_hash(path: Path, raw: bytes) -> str:
    first_line = raw.splitlines()[0] if raw.splitlines() else b""
    material = path.name.encode("utf-8") + b"\n" + first_line
    return hashlib.sha256(material).hexdigest()


def event_type(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    value = payload.get("type") or row.get("type") or row.get("event")
    return str(value or "unknown")


def timestamp(row: dict[str, Any]) -> str | None:
    for key in ("timestamp", "ts", "created_at", "time"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    value = payload.get("timestamp")
    return value if isinstance(value, str) and value else None


def safe_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "content", "message", "cmd", "command"):
            if isinstance(value.get(key), str):
                return value[key]
    return ""


def user_text(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    message = row.get("message") if isinstance(row.get("message"), dict) else {}
    if row.get("role") == "user" or payload.get("role") == "user" or message.get("role") == "user":
        return safe_text(row) or safe_text(payload) or safe_text(message)
    if event_type(row) in {"user_message", "user_turn", "input"}:
        return safe_text(row) or safe_text(payload)
    return ""


def is_token_event(row: dict[str, Any]) -> bool:
    return event_type(row) == "token_count"


def token_usage(row: dict[str, Any]) -> dict[str, int]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    info = payload.get("info") if isinstance(payload.get("info"), dict) else {}
    usage = (
        payload.get("last_token_usage")
        or row.get("last_token_usage")
        or info.get("last_token_usage")
        or payload.get("usage")
        or {}
    )
    if not isinstance(usage, dict):
        return {field: 0 for field in TOKEN_FIELDS}
    return {field: int(usage.get(field) or 0) for field in TOKEN_FIELDS}


def is_tool_call(row: dict[str, Any]) -> bool:
    kind = event_type(row)
    if kind in {"tool_call", "function_call", "exec_command", "tool_use"}:
        return True
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return bool(payload.get("tool_name") or row.get("tool_name"))


def is_tool_result(row: dict[str, Any]) -> bool:
    return event_type(row) in {"tool_result", "function_result", "exec_result", "tool_output"}


def tool_output_length(row: dict[str, Any]) -> int:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    for key in ("output", "result", "stdout", "stderr", "content"):
        value = payload.get(key, row.get(key))
        if isinstance(value, str):
            return len(value)
    return 0


def tool_failed(row: dict[str, Any]) -> bool:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    status = payload.get("status") or row.get("status")
    if str(status).lower() in {"failed", "error", "timeout"}:
        return True
    exit_code = payload.get("exit_code", row.get("exit_code"))
    return isinstance(exit_code, int) and exit_code != 0


def classify_text(text: str) -> dict[str, Any]:
    reqs = set(REQ_RE.findall(text))
    bugs = set(BUG_RE.findall(text))
    sprints = set(SPRINT_RE.findall(text))
    releases = set(RELEASE_RE.findall(text))
    changes = set(CHANGE_RE.findall(text))
    workflow_event = None
    event_match = EVENT_RE.search(text)
    if event_match:
        workflow_event = event_match.group("event")
        if not workflow_event:
            family = event_match.group("slash_family") or event_match.group("link_family")
            action = event_match.group("slash_action") or event_match.group("link_action")
            workflow_event = f"{family}.{action}" if family and action else None
    command = workflow_event or ("multi-issue" if len(reqs | bugs) > 1 else "command")
    confidence = "high" if any((reqs, bugs, sprints, changes, workflow_event)) else "low"
    return {
        "requirements": reqs,
        "bugs": bugs,
        "changes": changes,
        "sprint_id": sorted(sprints)[0] if sprints else None,
        "release_version": sorted(releases)[0] if releases else None,
        "workflow_event": workflow_event,
        "command": command,
        "attribution_confidence": confidence,
    }


def redaction_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    if ABS_PATH_RE.search(text):
        warnings.append("redacted-local-absolute-path")
    if SECRET_RE.search(text):
        warnings.append("redacted-sensitive-text")
    return warnings


def apply_attribution(run: CommandRun, text: str) -> None:
    details = classify_text(text)
    run.requirements.update(details["requirements"])
    run.bugs.update(details["bugs"])
    run.changes.update(details["changes"])
    run.sprint_id = run.sprint_id or details["sprint_id"]
    if details["sprint_id"]:
        run.release_sprints.add(details["sprint_id"])
    run.release_version = run.release_version or details["release_version"]
    run.workflow_event = run.workflow_event or details["workflow_event"]
    run.command = details["command"]
    run.attribution_confidence = details["attribution_confidence"]
    run.warnings.extend(redaction_warnings(text))


def parse_session_jsonl(path: Path, manual_map: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    raw = path.read_bytes()
    session_hash = session_source_hash(path, raw)
    source_data_file = display_source_data_file(path)
    runs: list[CommandRun] = []
    current: CommandRun | None = None
    current_model: dict[str, str | int] = {}
    warnings: list[str] = []

    for line_number, raw_line in enumerate(raw.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            row = json.loads(raw_line)
        except json.JSONDecodeError:
            warnings.append(f"line-{line_number}: malformed-json")
            if current:
                current.warnings.append("malformed-json-row-skipped")
            continue
        if not isinstance(row, dict):
            warnings.append(f"line-{line_number}: non-object-row")
            continue

        model_metadata = extract_model_metadata(row)
        if model_metadata:
            current_model.update(model_metadata)
            if current:
                apply_model_metadata(current, model_metadata)

        text = user_text(row)
        if text:
            if current:
                current.retry_count = current._tool_errors
                runs.append(current)
            current = CommandRun(
                source_session_hash=session_hash,
                source_data_file=source_data_file,
                source_line_start=line_number,
                source_line_end=line_number,
                turn_hash=stable_hash(f"{session_hash}:{line_number}:{text}"),
                started_at=timestamp(row),
                ended_at=timestamp(row),
            )
            apply_model_metadata(current, current_model)
            apply_attribution(current, text)
            continue

        if current is None:
            continue
        current.source_line_end = line_number
        current.ended_at = timestamp(row) or current.ended_at
        kind = event_type(row)
        if is_token_event(row):
            current.model_call_count += 1
            usage = token_usage(row)
            for field in TOKEN_FIELDS:
                setattr(current, field, getattr(current, field) + usage[field])
            continue
        if is_tool_call(row):
            current.tool_call_count += 1
            continue
        if is_tool_result(row):
            current.tool_output_chars += tool_output_length(row)
            if tool_failed(row):
                current._tool_errors += 1
            continue
        if kind not in {"assistant_message", "message", "unknown"}:
            current.warnings.append(f"unknown-event:{kind}")

    if current:
        current.retry_count = current._tool_errors
        runs.append(current)

    records = normalize_records([run.to_record() for run in runs])
    if manual_map:
        records = apply_manual_mapping(records, manual_map)
    return records, warnings


def apply_manual_mapping(records: list[dict[str, Any]], manual_map: dict[str, Any]) -> list[dict[str, Any]]:
    for record in records:
        mapping = manual_map.get(record["turn_hash"]) or manual_map.get(record["source_session_hash"])
        if not isinstance(mapping, dict):
            continue
        for key in ("requirements", "bugs", "changes"):
            if isinstance(mapping.get(key), list):
                record[key] = sorted(set(record[key]) | set(str(item) for item in mapping[key]))
        if isinstance(mapping.get("sprint_id"), str):
            record["sprint_id"] = mapping["sprint_id"]
        if isinstance(mapping.get("release_sprints"), list):
            record["release_sprints"] = sorted(set(str(item) for item in mapping["release_sprints"]))
        if isinstance(mapping.get("release_version"), str):
            record["release_version"] = mapping["release_version"]
        if isinstance(mapping.get("workflow_event"), str):
            record["workflow_event"] = mapping["workflow_event"]
        if mapping.get("post_command_target") is True:
            record["_post_command_target"] = True
        record["attribution_confidence"] = mapping.get("attribution_confidence", "medium")
        normalize_record_issues(record)
    return records


def _record_context_score(
    record: dict[str, Any],
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_version: str | None = None,
) -> int:
    score = 0
    record_event = record.get("workflow_event") or record.get("command")
    if workflow_event and record_event == workflow_event:
        score += 6
    if sprint_id and record.get("sprint_id") == sprint_id:
        score += 3
    if release_version and record.get("release_version") == release_version:
        score += 3
    for key, values in (
        ("requirements", requirements or []),
        ("bugs", bugs or []),
        ("changes", changes or []),
    ):
        existing = set(str(item) for item in record.get(key, []))
        score += len(existing & set(values)) * 2
    return score


def select_workflow_context_record(
    records: list[dict[str, Any]],
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_version: str | None = None,
) -> dict[str, Any] | None:
    if not records:
        return None
    manual_targets = [record for record in records if record.get("_post_command_target") is True]
    if manual_targets:
        return manual_targets[-1]
    scored = [
        (
            _record_context_score(
                record,
                workflow_event=workflow_event,
                requirements=requirements,
                bugs=bugs,
                changes=changes,
                sprint_id=sprint_id,
                release_version=release_version,
            ),
            index,
            record,
        )
        for index, record in enumerate(records)
    ]
    best_score, _, target = max(scored, key=lambda item: (item[0], item[1]))
    return target if best_score > 0 else records[-1]


def apply_workflow_context(
    records: list[dict[str, Any]],
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_sprints: list[str] | None = None,
    release_version: str | None = None,
) -> list[dict[str, Any]]:
    """Apply explicit workflow attribution to the best matching parsed command run."""

    if not records:
        return records
    target = select_workflow_context_record(
        records,
        workflow_event=workflow_event,
        requirements=requirements,
        bugs=bugs,
        changes=changes,
        sprint_id=sprint_id,
        release_version=release_version,
    )
    if target is None:
        return records
    target["_post_command_target"] = True
    for key, values in (
        ("requirements", requirements or []),
        ("bugs", bugs or []),
        ("changes", changes or []),
    ):
        target[key] = sorted(set(str(item) for item in target.get(key, [])) | set(values))
    normalize_record_issues(target)
    if workflow_event:
        target["workflow_event"] = workflow_event
        target["command"] = workflow_event
    if sprint_id:
        target["sprint_id"] = sprint_id
    if release_sprints:
        existing = set(str(item) for item in target.get("release_sprints", []))
        target["release_sprints"] = sorted(existing | set(release_sprints))
    if release_version:
        target["release_version"] = release_version
    if any((workflow_event, requirements, bugs, changes, sprint_id, release_sprints, release_version)):
        target["attribution_confidence"] = "high"
    return records


MODEL_FIELDS = (
    "model_name",
    "model_provider",
    "service_tier",
    "reasoning_effort",
    "reasoning_summary",
    "model_speed_tier",
    "model_rate_limit_name",
    "model_context_window",
)


def model_identity(row: dict[str, Any]) -> dict[str, Any]:
    return {field: row.get(field) for field in MODEL_FIELDS if row.get(field) not in (None, "")}


def resolve_sprint_yaml_path(sprint_id: str, root: Path | None = None) -> Path | None:
    base = root or Path.cwd()
    for candidate in (
        base / "iterations" / "change" / sprint_id / "sprint.yaml",
        base / "iterations" / "archive" / sprint_id / "sprint.yaml",
        base / "iterations" / sprint_id / "sprint.yaml",
    ):
        if candidate.exists():
            return candidate
    return None


def sprint_scope_for_usage(sprint_id: str, root: Path | None = None) -> dict[str, list[str]]:
    path = resolve_sprint_yaml_path(sprint_id, root=root)
    if path is None:
        return {"requirements": [], "bugs": [], "changes": []}
    data = workflow_collect.parse_simple_yaml(path.read_text(encoding="utf-8"))
    return {
        "requirements": [str(item) for item in data.get("requirements") or []],
        "bugs": [str(item) for item in data.get("bugs") or []],
        "changes": [str(item) for item in data.get("changes") or []],
    }


def record_matches_sprint_scope(record: dict[str, Any], sprint_id: str, scope: dict[str, list[str]]) -> bool:
    if record.get("sprint_id") == sprint_id:
        return True
    record_requirements = set(str(item) for item in record.get("requirements", []))
    record_bugs = set(str(item) for item in record.get("bugs", []))
    record_changes = set(str(item) for item in record.get("changes", []))
    return bool(
        record_requirements & set(scope.get("requirements") or [])
        or record_bugs & set(scope.get("bugs") or [])
        or record_changes & set(scope.get("changes") or [])
    )


def sprint_issue_alias_map(rows: list[dict[str, Any]], scope: dict[str, list[str]]) -> dict[str, str]:
    grouped: dict[str, set[str]] = {}
    for value in [
        *(scope.get("requirements") or []),
        *(scope.get("bugs") or []),
        *[item for row in rows for item in row.get("requirements", [])],
        *[item for row in rows for item in row.get("bugs", [])],
    ]:
        text = str(value)
        short = issue_short_id(text)
        if short and text != short:
            grouped.setdefault(short, set()).add(text)
    return {short: next(iter(values)) for short, values in grouped.items() if len(values) == 1}


def normalize_sprint_issue_aliases(rows: list[dict[str, Any]], scope: dict[str, list[str]]) -> list[dict[str, Any]]:
    alias_map = sprint_issue_alias_map(rows, scope)
    if not alias_map:
        return rows
    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        normalized = dict(row)
        for key in ("requirements", "bugs"):
            normalized[key] = canonicalize_issue_ids(set(row.get(key, [])), canonical_map=alias_map)
        normalized_rows.append(normalized)
    return normalized_rows


def empty_sprint_usage_matrix_cells() -> dict[str, dict[str, int]]:
    return {
        metric: {label: 0 for _, label in SPRINT_MATRIX_COMMAND_COLUMNS}
        for metric in SPRINT_MATRIX_METRICS
    }


def add_sprint_usage_matrix_values(cells: dict[str, dict[str, int]], record: dict[str, Any]) -> None:
    event = record.get("workflow_event") or record.get("command") or "unknown"
    label_by_event = dict(SPRINT_MATRIX_COMMAND_COLUMNS)
    label = label_by_event.get(str(event))
    if label is None:
        return
    for metric in SPRINT_MATRIX_METRICS:
        cells[metric][label] += int(record.get(metric) or 0)


def build_sprint_usage_matrices(
    rows: list[dict[str, Any]],
    sprint_id: str,
    scope: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    scope = scope or {}
    ordered_row_keys: list[tuple[str, str]] = [
        ("total", "Total"),
        ("sprint", sprint_id),
    ]
    scope_requirements = [str(item) for item in scope.get("requirements") or []]
    scope_bugs = [str(item) for item in scope.get("bugs") or []]
    row_requirements = sorted({item for row in rows for item in row.get("requirements", [])})
    row_bugs = sorted({item for row in rows for item in row.get("bugs", [])})
    ordered_row_keys.extend(
        ("requirement", issue_id)
        for issue_id in [*scope_requirements, *[item for item in row_requirements if item not in scope_requirements]]
    )
    ordered_row_keys.extend(
        ("bug", issue_id)
        for issue_id in [*scope_bugs, *[item for item in row_bugs if item not in scope_bugs]]
    )

    row_cells = {
        row_id: {
            "object_type": object_type,
            "object_id": row_id,
            "metrics": empty_sprint_usage_matrix_cells(),
        }
        for object_type, row_id in ordered_row_keys
    }
    for record in rows:
        add_sprint_usage_matrix_values(row_cells["Total"]["metrics"], record)
        add_sprint_usage_matrix_values(row_cells[sprint_id]["metrics"], record)
        for issue_id in record.get("requirements", []):
            if issue_id in row_cells:
                add_sprint_usage_matrix_values(row_cells[issue_id]["metrics"], record)
        for issue_id in record.get("bugs", []):
            if issue_id in row_cells:
                add_sprint_usage_matrix_values(row_cells[issue_id]["metrics"], record)

    return {
        "source": "data/ai-usage command-runs",
        "metrics": list(SPRINT_MATRIX_METRICS),
        "columns": [
            {"workflow_event": event, "label": label}
            for event, label in SPRINT_MATRIX_COMMAND_COLUMNS
        ],
        "rows": [row_cells[row_id] for _, row_id in ordered_row_keys],
        "note": (
            "Total and sprint rows aggregate unique command runs. Requirement and bug rows "
            "are attribution views; a multi-issue command run may be counted in multiple object rows."
        ),
    }


def aggregate_sprint(records: list[dict[str, Any]], sprint_id: str) -> dict[str, Any]:
    records = normalize_records(records)
    scope = sprint_scope_for_usage(sprint_id)
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        if record_matches_sprint_scope(record, sprint_id, scope):
            unique[record["turn_hash"]] = record
    rows = normalize_sprint_issue_aliases(list(unique.values()), scope)
    totals = {field: sum(int(row.get(field) or 0) for row in rows) for field in TOKEN_FIELDS}
    totals.update(
        {
            "command_run_count": len(rows),
            "model_call_count": sum(int(row.get("model_call_count") or 0) for row in rows),
            "tool_call_count": sum(int(row.get("tool_call_count") or 0) for row in rows),
            "tool_output_chars": sum(int(row.get("tool_output_chars") or 0) for row in rows),
            "retry_count": sum(int(row.get("retry_count") or 0) for row in rows),
        }
    )
    by_event: dict[str, Counter[str]] = {}
    by_model: dict[str, Counter[str]] = {}
    models: dict[str, dict[str, Any]] = {}
    for row in rows:
        event = row.get("workflow_event") or row.get("command") or "unknown"
        bucket = by_event.setdefault(event, Counter())
        bucket["command_run_count"] += 1
        bucket["model_call_count"] += int(row.get("model_call_count") or 0)
        bucket["tool_call_count"] += int(row.get("tool_call_count") or 0)
        bucket["retry_count"] += int(row.get("retry_count") or 0)
        for field in TOKEN_FIELDS:
            bucket[field] += int(row.get(field) or 0)

        identity = model_identity(row)
        model_key = "|".join(str(identity.get(field) or "") for field in ("model_name", "reasoning_effort", "model_speed_tier"))
        model_key = model_key or "unknown"
        models.setdefault(model_key, identity)
        model_bucket = by_model.setdefault(model_key, Counter())
        model_bucket["command_run_count"] += 1
        model_bucket["model_call_count"] += int(row.get("model_call_count") or 0)
        for field in TOKEN_FIELDS:
            model_bucket[field] += int(row.get(field) or 0)
    coverage = {
        "requirements": sorted({item for row in rows for item in row.get("requirements", [])}),
        "bugs": sorted({item for row in rows for item in row.get("bugs", [])}),
        "changes": sorted({item for row in rows for item in row.get("changes", [])}),
    }
    source_data_files = sorted({str(row.get("source_data_file")) for row in rows if row.get("source_data_file")})
    return {
        "sprint_id": sprint_id,
        "source": "data/ai-usage command-runs",
        "source_data_files": source_data_files,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "estimated": not bool(rows),
        "coverage": coverage,
        "models": sorted(models.values(), key=lambda item: (str(item.get("model_name") or ""), str(item.get("reasoning_effort") or ""))),
        "totals": totals,
        "by_workflow_event": {key: dict(value) for key, value in sorted(by_event.items())},
        "by_model": {key: dict(value) for key, value in sorted(by_model.items())},
        "usage_matrices": build_sprint_usage_matrices(rows, sprint_id, scope=scope),
    }


def aggregate_release(records: list[dict[str, Any]], release_version: str, workflow_event: str | None = None) -> dict[str, Any]:
    records = normalize_records(records)
    rows = [
        record
        for record in records
        if record.get("release_version") == release_version
        and (workflow_event is None or record.get("workflow_event") == workflow_event)
    ]
    totals = {field: sum(int(row.get(field) or 0) for row in rows) for field in TOKEN_FIELDS}
    totals.update(
        {
            "command_run_count": len(rows),
            "model_call_count": sum(int(row.get("model_call_count") or 0) for row in rows),
            "tool_call_count": sum(int(row.get("tool_call_count") or 0) for row in rows),
            "tool_output_chars": sum(int(row.get("tool_output_chars") or 0) for row in rows),
            "retry_count": sum(int(row.get("retry_count") or 0) for row in rows),
        }
    )
    coverage = {
        "requirements": sorted({item for row in rows for item in row.get("requirements", [])}),
        "bugs": sorted({item for row in rows for item in row.get("bugs", [])}),
        "changes": sorted({item for row in rows for item in row.get("changes", [])}),
        "sprints": sorted(
            {
                *{str(row.get("sprint_id")) for row in rows if row.get("sprint_id")},
                *{str(item) for row in rows for item in row.get("release_sprints", [])},
            }
        ),
    }
    source_data_files = sorted({str(row.get("source_data_file")) for row in rows if row.get("source_data_file")})
    return {
        "release_version": release_version,
        "workflow_event": workflow_event,
        "source": "data/ai-usage release command-runs",
        "source_data_files": source_data_files,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "estimated": not bool(rows),
        "coverage": coverage,
        "totals": totals,
        "command_runs": rows,
    }


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _status_payload(
    *,
    path: Path,
    status: str,
    warnings: list[str] | None = None,
    generated_at: str | None = None,
    coverage: dict[str, Any] | None = None,
    totals: dict[str, Any] | None = None,
    usage_matrices: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "snapshot_status": status,
        "snapshot_path": str(path),
        "present": status not in {"missing"},
        "usage_mode": "actual" if status == "present" else "estimated_fallback",
        "generated_at": generated_at,
        "coverage": coverage or {"requirements": "unknown", "bugs": "unknown", "changes": "unknown"},
        "warnings": warnings or [],
        "warning_count": len(warnings or []),
        "totals": totals or {},
        "usage_matrices": usage_matrices or {},
        "recommended_action": None
        if status == "present"
        else f"Run `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint <sprint-id>` and re-check {path.name}.",
    }


def check_sprint_snapshot(
    path: Path,
    sprint_id: str,
    *,
    expected_scope: dict[str, list[str]] | None = None,
    min_generated_at: str | None = None,
) -> dict[str, Any]:
    """Return a compact safety/status summary for one Sprint AI usage snapshot."""

    if not path.exists():
        return _status_payload(path=path, status="missing", warnings=["snapshot-missing"])

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return _status_payload(path=path, status="failed", warnings=["invalid-ai-usage-json"])
    if not isinstance(data, dict):
        return _status_payload(path=path, status="failed", warnings=["invalid-ai-usage-json"])

    warnings: list[str] = []
    generated_at = data.get("generated_at") if isinstance(data.get("generated_at"), str) else None
    totals = data.get("totals") if isinstance(data.get("totals"), dict) else {}
    usage_matrices = data.get("usage_matrices") if isinstance(data.get("usage_matrices"), dict) else {}
    coverage_data = data.get("coverage") if isinstance(data.get("coverage"), dict) else {}
    coverage: dict[str, Any] = {}

    if data.get("sprint_id") != sprint_id:
        warnings.append("sprint-id-mismatch")
    if data.get("estimated") is True:
        warnings.append("snapshot-estimated")
    if not generated_at:
        warnings.append("generated-at-missing")
    elif min_generated_at:
        generated = parse_datetime(generated_at)
        minimum = parse_datetime(min_generated_at)
        if generated is None:
            warnings.append("generated-at-invalid")
        elif minimum and generated < minimum:
            warnings.append("snapshot-stale")

    metric_values = [int(totals.get(field) or 0) for field in (*COUNT_FIELDS, *TOKEN_FIELDS)]
    if not totals or not any(metric_values):
        warnings.append("required-metrics-empty")
    if not usage_matrices:
        warnings.append("usage-matrices-missing")

    expected_scope = expected_scope or {}
    for key in ("requirements", "bugs", "changes"):
        expected = sorted(set(expected_scope.get(key) or []))
        actual = sorted(set(str(item) for item in coverage_data.get(key) or []))
        missing = sorted(set(expected) - set(actual))
        coverage[key] = {
            "expected": expected,
            "actual": actual,
            "missing": missing,
            "status": "pass" if not missing else "missing",
        }
        if expected and not actual:
            warnings.append(f"{key}-coverage-unknown")
        elif missing:
            warnings.append(f"{key}-coverage-missing")

    if any(warning in warnings for warning in ("sprint-id-mismatch", "snapshot-estimated", "required-metrics-empty")):
        status = "failed"
    elif any(
        "stale" in warning
        or "coverage-" in warning
        or warning in {"generated-at-missing", "usage-matrices-missing"}
        for warning in warnings
    ):
        status = "stale"
    else:
        status = "present"

    return _status_payload(
        path=path,
        status=status,
        warnings=sorted(set(warnings)),
        generated_at=generated_at,
        coverage=coverage,
        totals=totals,
        usage_matrices=usage_matrices,
    )


def assert_record_safe(record: dict[str, Any]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).lower() in UNSAFE_PERSISTED_KEYS:
                    raise ValueError("unsafe key detected in usage record")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(record)
    text = json.dumps(record, ensure_ascii=False)
    if ABS_PATH_RE.search(text) or SECRET_RE.search(text):
        raise ValueError("unsafe text detected in usage record")


def safe_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    safe: list[dict[str, Any]] = []
    skipped = 0
    for record in records:
        try:
            assert_record_safe(record)
        except ValueError:
            skipped += 1
            continue
        safe.append(record)
    return safe, skipped


def load_command_run_records(out_dir: Path) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((out_dir / "command-runs").rglob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        for record in payload.get("command_runs", []) if isinstance(payload, dict) else []:
            if not isinstance(record, dict) or not isinstance(record.get("turn_hash"), str):
                continue
            try:
                assert_record_safe(record)
            except ValueError:
                continue
            else:
                records[record["turn_hash"]] = record
    return normalize_records(list(records.values()))


def merge_command_run_file(path: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    try:
        payload = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, json.JSONDecodeError):
        payload = {}
    for record in payload.get("command_runs", []) if isinstance(payload, dict) else []:
        if isinstance(record, dict) and isinstance(record.get("turn_hash"), str):
            merged[record["turn_hash"]] = record
    for record in records:
        merged[record["turn_hash"]] = record
    return normalize_records(list(merged.values()))


def slug_part(value: str | None, fallback: str) -> str:
    text = str(value or fallback)
    text = re.sub(r"[^A-Za-z0-9_.-]+", "-", text).strip("-")
    return text or fallback


def command_run_scope_dir(records: list[dict[str, Any]]) -> Path:
    release_versions = sorted(
        {
            str(record.get("release_version"))
            for record in records
            if record.get("release_version")
            and str(record.get("workflow_event") or "").startswith(("release.", "image."))
        }
    )
    requirements = sorted({str(item) for record in records for item in record.get("requirements", [])})
    bugs = sorted({str(item) for record in records for item in record.get("bugs", [])})
    changes = sorted({str(item) for record in records for item in record.get("changes", [])})
    sprints = sorted({str(record.get("sprint_id")) for record in records if record.get("sprint_id")})
    if release_versions:
        return Path("releases") / slug_part(release_versions[0], "unknown-release")
    if requirements:
        return Path("issues") / slug_part(requirements[0], "unknown-requirement")
    if bugs:
        return Path("issues") / slug_part(bugs[0], "unknown-bug")
    if changes:
        return Path("opsxs") / slug_part(changes[0], "unknown-change")
    if sprints:
        return Path("sprints") / slug_part(sprints[0], "unknown-sprint")
    return Path("_unscoped")


def command_run_file_name(records: list[dict[str, Any]]) -> str:
    first = records[0]
    started_at = str(first.get("started_at") or "")
    date = started_at[:10] if re.match(r"\d{4}-\d{2}-\d{2}", started_at) else "unknown-date"
    events = sorted({str(record.get("workflow_event") or record.get("command") or "command") for record in records})
    event = events[0] if len(events) == 1 else "session"
    session_hash = str(first.get("source_session_hash") or "unknown")[:16]
    return f"{slug_part(date, 'unknown-date')}--{slug_part(event, 'session')}--{session_hash}.json"


def command_run_path(command_dir: Path, records: list[dict[str, Any]]) -> Path:
    return command_dir / command_run_scope_dir(records) / command_run_file_name(records)


def legacy_command_run_path(command_dir: Path, records: list[dict[str, Any]]) -> Path:
    return command_dir / f"{records[0]['source_session_hash'][:16]}.json"


def existing_command_run_paths(command_dir: Path, records: list[dict[str, Any]]) -> list[Path]:
    session_hash = str(records[0]["source_session_hash"])[:16]
    paths = {legacy_command_run_path(command_dir, records)}
    paths.update(command_dir.glob(f"*--{session_hash}.json"))
    paths.update(command_dir.rglob(f"*--{session_hash}.json"))
    return sorted(paths)


def release_event_file_name(workflow_event: str | None) -> str:
    return f"{slug_part(workflow_event or 'release.command', 'release.command')}.json"


def write_outputs(
    records: list[dict[str, Any]],
    out_dir: Path,
    sprint_id: str | None,
    release_version: str | None = None,
    workflow_event: str | None = None,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    command_dir = out_dir / "command-runs"
    sprint_dir = out_dir / "sprints"
    release_dir = command_dir / "releases"
    command_dir.mkdir(parents=True, exist_ok=True)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)
    records = normalize_records(records)
    records, _ = safe_records(records)
    output_paths: dict[str, Path] = {}
    if records:
        for existing_path in existing_command_run_paths(command_dir, records):
            records = merge_command_run_file(existing_path, records)
        records, _ = safe_records(records)
        command_path = command_run_path(command_dir, records)
        command_path.parent.mkdir(parents=True, exist_ok=True)
        command_path.write_text(json.dumps({"command_runs": records}, ensure_ascii=False, indent=2) + "\n")
        for existing_path in existing_command_run_paths(command_dir, records):
            if existing_path != command_path and existing_path.exists():
                existing_path.unlink()
        output_paths["command_runs"] = command_path
    if sprint_id:
        snapshot_records = load_command_run_records(out_dir) if records else []
        snapshot = aggregate_sprint(snapshot_records or records, sprint_id)
        assert_record_safe(snapshot)
        sprint_path = sprint_dir / f"{sprint_id}.json"
        sprint_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        output_paths["sprint"] = sprint_path
    if release_version and records:
        release_snapshot = aggregate_release(records, release_version, workflow_event)
        assert_record_safe(release_snapshot)
        release_path = release_dir / slug_part(release_version, "unknown-release") / release_event_file_name(workflow_event)
        release_path.parent.mkdir(parents=True, exist_ok=True)
        release_path.write_text(json.dumps(release_snapshot, ensure_ascii=False, indent=2) + "\n")
        output_paths["release"] = release_path
    return output_paths


def relative_path(path: Path, root: Path | None = None) -> str:
    root = (root or Path.cwd()).resolve()
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return path.name


def workflow_search_terms(
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_sprints: list[str] | None = None,
    release_version: str | None = None,
) -> list[str]:
    terms: set[str] = set()
    if workflow_event:
        terms.add(workflow_event)
        if "." in workflow_event:
            family, action = workflow_event.split(".", 1)
            terms.add(f"{family}-{action}")
            terms.add(f"/{family}-{action}")
    for values in (requirements or [], bugs or []):
        for value in values:
            text = str(value)
            terms.add(text)
            short_match = re.match(r"\b((?:REQ|BUG)-\d{4,})", text)
            if short_match:
                terms.add(short_match.group(1))
    for value in changes or []:
        terms.add(str(value))
    if sprint_id:
        terms.add(sprint_id)
    for value in release_sprints or []:
        terms.add(str(value))
    if release_version:
        terms.add(release_version)
    return sorted(term.lower() for term in terms if term)


def discover_session_jsonl(search_terms: list[str]) -> Path | None:
    if not search_terms:
        return None
    root = Path(os.environ.get("AI_USAGE_SESSIONS_DIR") or Path.home() / ".codex" / "sessions")
    if not root.exists():
        return None
    try:
        paths = sorted(
            root.glob("**/*.jsonl"),
            key=lambda candidate: candidate.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return None
    best: tuple[int, float, Path] | None = None
    for path in paths[:AUTO_SESSION_SCAN_LIMIT]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            mtime = path.stat().st_mtime
        except OSError:
            continue
        score = sum(1 for term in search_terms if term in text)
        if score <= 0:
            continue
        candidate = (score, mtime, path)
        if best is None or candidate > best:
            best = candidate
    return best[2] if best else None


def resolve_session_jsonl(
    path: Path | None,
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_sprints: list[str] | None = None,
    release_version: str | None = None,
) -> tuple[Path | None, str | None, str]:
    if path:
        return path, None, "explicit"
    for env_name in ("AI_USAGE_SESSION_JSONL", "CODEX_SESSION_JSONL"):
        value = os.environ.get(env_name)
        if value:
            return Path(value), None, "env"
    discovered = discover_session_jsonl(
        workflow_search_terms(
            workflow_event=workflow_event,
            requirements=requirements,
            bugs=bugs,
            changes=changes,
            sprint_id=sprint_id,
            release_sprints=release_sprints,
            release_version=release_version,
        )
    )
    if discovered:
        return discovered, None, "auto"
    return None, "session-jsonl-missing", "unavailable"


def warning_usage_mode(records: list[dict[str, Any]], warnings: list[str]) -> str:
    if not records:
        return USAGE_MODE_UNAVAILABLE
    if warnings:
        return USAGE_MODE_ESTIMATED
    has_real_usage = any(
        int(record.get("model_call_count") or 0) > 0 or int(record.get("total_tokens") or 0) > 0
        for record in records
    )
    return USAGE_MODE_ACTUAL if has_real_usage else USAGE_MODE_ESTIMATED


def post_command_hook(
    *,
    session_jsonl: Path | None,
    out_dir: Path,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
    release_sprints: list[str] | None = None,
    release_version: str | None = None,
    manual_map: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Build a compact post-command AI usage fact source summary."""

    resolved_session, missing_reason, session_input = resolve_session_jsonl(
        session_jsonl,
        workflow_event=workflow_event,
        requirements=requirements,
        bugs=bugs,
        changes=changes,
        sprint_id=sprint_id,
        release_sprints=release_sprints,
        release_version=release_version,
    )
    if missing_reason or resolved_session is None:
        warning = missing_reason or "session-jsonl-missing"
        return {
            "status": "skipped",
            "usage_mode": USAGE_MODE_UNAVAILABLE,
            "command_run_count": 0,
            "session_input": session_input,
            "outputs": {},
            "sprint_snapshot": {
                "status": "skipped",
                "path": None,
                "reason": "no-sprint" if not sprint_id else warning,
            },
            "warnings": [warning],
            "warning_count": 1,
            "recommended_action": "Provide --session-jsonl or set AI_USAGE_SESSION_JSONL to build a redacted usage fact source.",
        }
    if not resolved_session.exists():
        return {
            "status": "skipped",
            "usage_mode": USAGE_MODE_UNAVAILABLE,
            "command_run_count": 0,
            "session_input": session_input,
            "outputs": {},
            "sprint_snapshot": {
                "status": "skipped",
                "path": None,
                "reason": "session-jsonl-not-found",
            },
            "warnings": ["session-jsonl-not-found"],
            "warning_count": 1,
            "recommended_action": "Check the local Codex session path and rerun the hook with --session-jsonl.",
        }

    records, parse_warnings = parse_session_jsonl(resolved_session, manual_map)
    records = apply_workflow_context(
        records,
        workflow_event=workflow_event,
        requirements=requirements,
        bugs=bugs,
        changes=changes,
        sprint_id=sprint_id,
        release_sprints=release_sprints,
        release_version=release_version,
    )
    if any((workflow_event, requirements, bugs, changes, sprint_id, release_sprints, release_version)):
        records = [record for record in records if record.pop("_post_command_target", False)]
    warnings = list(parse_warnings)
    if not records:
        warnings.append("no-command-runs")
    if records and not any(int(record.get("model_call_count") or 0) > 0 for record in records):
        warnings.append("token-count-missing")
    if records:
        records, skipped_unsafe = safe_records(records)
        if skipped_unsafe:
            warnings.append(f"unsafe-records-skipped:{skipped_unsafe}")
        if skipped_unsafe and not records:
            warnings.append("no-safe-command-runs")

    usage_mode = warning_usage_mode(records, warnings)
    outputs: dict[str, str] = {}
    output_paths: dict[str, Path] = {}
    if records and not dry_run:
        output_paths = write_outputs(records, out_dir, sprint_id, release_version, workflow_event)
        outputs = {key: relative_path(value) for key, value in output_paths.items()}

    if sprint_id:
        sprint_snapshot = {
            "status": "dry-run" if dry_run else ("refreshed" if "sprint" in output_paths else "skipped"),
            "path": relative_path(out_dir / "sprints" / f"{sprint_id}.json"),
            "reason": None if (dry_run or "sprint" in output_paths) else "no-command-runs",
        }
    else:
        sprint_snapshot = {
            "status": "skipped",
            "path": None,
            "reason": "no-sprint",
        }
    if release_version:
        release_artifact = {
            "status": "dry-run" if dry_run else ("refreshed" if "release" in output_paths else "skipped"),
            "path": relative_path(out_dir / "command-runs" / "releases" / slug_part(release_version, "unknown-release") / release_event_file_name(workflow_event)),
            "reason": None if (dry_run or "release" in output_paths) else "no-command-runs",
        }
    else:
        release_artifact = {
            "status": "skipped",
            "path": None,
            "reason": "no-release",
        }

    status = "ok" if usage_mode == USAGE_MODE_ACTUAL else "warning"
    recommended_action = None
    if usage_mode != USAGE_MODE_ACTUAL:
        recommended_action = "Inspect warnings and rerun with a session containing token_count events if actual usage is required."
    return {
        "status": status,
        "usage_mode": usage_mode,
        "command_run_count": len(records),
        "session_input": session_input,
        "outputs": outputs,
        "sprint_snapshot": sprint_snapshot,
        "release_artifact": release_artifact,
        "warnings": sorted(set(warnings)),
        "warning_count": len(set(warnings)),
        "recommended_action": recommended_action,
    }


def compact_post_command_summary(
    payload: dict[str, Any],
    *,
    include_release: bool = False,
) -> dict[str, Any]:
    """Return the user-facing compact post-command hook summary."""

    summary = {
        "status": payload.get("status"),
        "usage_mode": payload.get("usage_mode"),
        "command_run_count": payload.get("command_run_count", 0),
        "sprint_snapshot": payload.get("sprint_snapshot"),
        "warning_count": payload.get("warning_count", 0),
        "recommended_action": payload.get("recommended_action"),
    }
    if include_release:
        summary["session_input"] = payload.get("session_input")
        summary["release_artifact"] = payload.get("release_artifact")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-jsonl", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("data/ai-usage"))
    parser.add_argument("--sprint")
    parser.add_argument("--release-sprint", action="append", default=[])
    parser.add_argument("--release")
    parser.add_argument("--manual-map", type=Path)
    parser.add_argument("--post-command-hook", action="store_true")
    parser.add_argument("--workflow-event")
    parser.add_argument("--req", action="append", default=[])
    parser.add_argument("--bug", action="append", default=[])
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check-snapshot", action="store_true")
    parser.add_argument("--expected-requirement", action="append", default=[])
    parser.add_argument("--expected-bug", action="append", default=[])
    parser.add_argument("--expected-change", action="append", default=[])
    parser.add_argument("--min-generated-at")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manual = json.loads(args.manual_map.read_text()) if args.manual_map else None
    if args.post_command_hook:
        payload = post_command_hook(
            session_jsonl=args.session_jsonl,
            out_dir=args.out_dir,
            workflow_event=args.workflow_event,
            requirements=args.req,
            bugs=args.bug,
            changes=args.change,
            sprint_id=args.sprint,
            release_sprints=args.release_sprint,
            release_version=args.release,
            manual_map=manual,
            dry_run=args.dry_run,
        )
        payload = compact_post_command_summary(payload, include_release=bool(args.release))
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
        return 0
    if args.check_snapshot:
        if not args.sprint:
            raise SystemExit("--check-snapshot requires --sprint")
        path = args.out_dir / "sprints" / f"{args.sprint}.json"
        payload = check_sprint_snapshot(
            path,
            args.sprint,
            expected_scope={
                "requirements": args.expected_requirement,
                "bugs": args.expected_bug,
                "changes": args.expected_change,
            },
            min_generated_at=args.min_generated_at,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
        return 0
    if not args.session_jsonl:
        raise SystemExit("--session-jsonl is required unless --check-snapshot is used")
    records, warnings = parse_session_jsonl(args.session_jsonl, manual)
    paths = write_outputs(records, args.out_dir, args.sprint, args.release, args.workflow_event)
    payload = {"command_run_count": len(records), "warnings": warnings, "outputs": {k: str(v) for k, v in paths.items()}}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
    return 0
