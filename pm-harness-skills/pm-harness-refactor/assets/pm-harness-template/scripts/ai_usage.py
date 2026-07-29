"""Extract redacted AI command usage facts from local Codex session JSONL."""

from __future__ import annotations

import argparse
import os
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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

USAGE_MODE_ACTUAL = "actual"
USAGE_MODE_ESTIMATED = "estimated_fallback"
USAGE_MODE_UNAVAILABLE = "unavailable"

REQ_RE = re.compile(r"\bREQ-\d{4,}[A-Za-z0-9_-]*\b")
BUG_RE = re.compile(r"\bBUG-\d{4,}[A-Za-z0-9_-]*\b")
SPRINT_RE = re.compile(r"\bsprint-\d{3,}\b")
EVENT_RE = re.compile(r"--event\s+([a-z][a-z0-9_.-]*)|/(req|bug|opsx|sprint)-([a-z0-9-]+)")
SECRET_RE = re.compile(
    r"(authorization|bearer|cookie|secret|password|api[_-]?key|access[_-]?key|token\s*[:=]|\.env)",
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


@dataclass
class CommandRun:
    source_session_hash: str
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
    attribution_confidence: str = "low"
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
            "attribution_confidence": self.attribution_confidence,
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
            "warnings": self.warnings,
        }


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def source_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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
    usage = payload.get("last_token_usage") or row.get("last_token_usage") or payload.get("usage") or {}
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
    changes = set(CHANGE_RE.findall(text))
    workflow_event = None
    event_match = EVENT_RE.search(text)
    if event_match:
        workflow_event = event_match.group(1) or f"{event_match.group(2)}.{event_match.group(3)}"
    command = workflow_event or ("multi-issue" if len(reqs | bugs) > 1 else "command")
    confidence = "high" if any((reqs, bugs, sprints, changes, workflow_event)) else "low"
    return {
        "requirements": reqs,
        "bugs": bugs,
        "changes": changes,
        "sprint_id": sorted(sprints)[0] if sprints else None,
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
    run.workflow_event = run.workflow_event or details["workflow_event"]
    run.command = details["command"]
    run.attribution_confidence = details["attribution_confidence"]
    run.warnings.extend(redaction_warnings(text))


def parse_session_jsonl(path: Path, manual_map: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    raw = path.read_bytes()
    session_hash = source_hash(raw)
    runs: list[CommandRun] = []
    current: CommandRun | None = None
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

        text = user_text(row)
        if text:
            if current:
                current.retry_count = current._tool_errors
                runs.append(current)
            current = CommandRun(
                source_session_hash=session_hash,
                source_line_start=line_number,
                source_line_end=line_number,
                turn_hash=stable_hash(f"{session_hash}:{line_number}:{text}"),
                started_at=timestamp(row),
                ended_at=timestamp(row),
            )
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

    records = [run.to_record() for run in runs]
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
        if isinstance(mapping.get("workflow_event"), str):
            record["workflow_event"] = mapping["workflow_event"]
        record["attribution_confidence"] = mapping.get("attribution_confidence", "medium")
    return records


def apply_workflow_context(
    records: list[dict[str, Any]],
    *,
    workflow_event: str | None = None,
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    sprint_id: str | None = None,
) -> list[dict[str, Any]]:
    """Apply explicit workflow attribution to the latest parsed command run."""

    if not records:
        return records
    target = records[-1]
    for key, values in (
        ("requirements", requirements or []),
        ("bugs", bugs or []),
        ("changes", changes or []),
    ):
        target[key] = sorted(set(str(item) for item in target.get(key, [])) | set(values))
    if workflow_event:
        target["workflow_event"] = workflow_event
        target["command"] = workflow_event
    if sprint_id:
        target["sprint_id"] = sprint_id
    if any((workflow_event, requirements, bugs, changes, sprint_id)):
        target["attribution_confidence"] = "high"
    return records


def aggregate_sprint(records: list[dict[str, Any]], sprint_id: str) -> dict[str, Any]:
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        if record.get("sprint_id") == sprint_id or sprint_id in record.get("changes", []):
            unique[record["turn_hash"]] = record
    rows = list(unique.values())
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
    for row in rows:
        event = row.get("workflow_event") or row.get("command") or "unknown"
        bucket = by_event.setdefault(event, Counter())
        bucket["command_run_count"] += 1
        bucket["model_call_count"] += int(row.get("model_call_count") or 0)
        bucket["tool_call_count"] += int(row.get("tool_call_count") or 0)
        bucket["retry_count"] += int(row.get("retry_count") or 0)
        for field in TOKEN_FIELDS:
            bucket[field] += int(row.get(field) or 0)
    warnings = sorted({warning for row in rows for warning in row.get("warnings", [])})
    if not rows:
        warnings.append("no-real-usage-snapshot")
    coverage = {
        "requirements": sorted({item for row in rows for item in row.get("requirements", [])}),
        "bugs": sorted({item for row in rows for item in row.get("bugs", [])}),
        "changes": sorted({item for row in rows for item in row.get("changes", [])}),
    }
    return {
        "sprint_id": sprint_id,
        "source": "data/ai-usage command-runs",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "estimated": not bool(rows),
        "coverage": coverage,
        "totals": totals,
        "by_workflow_event": {key: dict(value) for key, value in sorted(by_event.items())},
        "warnings": warnings,
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
    elif any("stale" in warning or "coverage-" in warning or warning == "generated-at-missing" for warning in warnings):
        status = "stale"
    else:
        status = "present"

    return _status_payload(
        path=path,
        status=status,
        warnings=sorted(set(warnings + list(data.get("warnings") or []))),
        generated_at=generated_at,
        coverage=coverage,
        totals=totals,
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


def load_command_run_records(out_dir: Path) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((out_dir / "command-runs").glob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        for record in payload.get("command_runs", []) if isinstance(payload, dict) else []:
            if isinstance(record, dict) and isinstance(record.get("turn_hash"), str):
                records[record["turn_hash"]] = record
    return list(records.values())


def write_outputs(records: list[dict[str, Any]], out_dir: Path, sprint_id: str | None) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    command_dir = out_dir / "command-runs"
    sprint_dir = out_dir / "sprints"
    command_dir.mkdir(parents=True, exist_ok=True)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        assert_record_safe(record)
    output_paths: dict[str, Path] = {}
    if records:
        command_path = command_dir / f"{records[0]['source_session_hash'][:16]}.json"
        command_path.write_text(json.dumps({"command_runs": records}, ensure_ascii=False, indent=2) + "\n")
        output_paths["command_runs"] = command_path
    if sprint_id:
        snapshot_records = load_command_run_records(out_dir) if records else []
        snapshot = aggregate_sprint(snapshot_records or records, sprint_id)
        assert_record_safe(snapshot)
        sprint_path = sprint_dir / f"{sprint_id}.json"
        sprint_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        output_paths["sprint"] = sprint_path
    return output_paths


def relative_path(path: Path, root: Path | None = None) -> str:
    root = (root or Path.cwd()).resolve()
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return path.name


def resolve_session_jsonl(path: Path | None) -> tuple[Path | None, str | None]:
    if path:
        return path, None
    for env_name in ("AI_USAGE_SESSION_JSONL", "CODEX_SESSION_JSONL"):
        value = os.environ.get(env_name)
        if value:
            return Path(value), None
    return None, "session-jsonl-missing"


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
    manual_map: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Build a compact post-command AI usage fact source summary."""

    resolved_session, missing_reason = resolve_session_jsonl(session_jsonl)
    if missing_reason or resolved_session is None:
        warning = missing_reason or "session-jsonl-missing"
        return {
            "status": "skipped",
            "usage_mode": USAGE_MODE_UNAVAILABLE,
            "command_run_count": 0,
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
    )
    warnings = list(parse_warnings)
    if not records:
        warnings.append("no-command-runs")
    if records and not any(int(record.get("model_call_count") or 0) > 0 for record in records):
        warnings.append("token-count-missing")

    usage_mode = warning_usage_mode(records, warnings)
    outputs: dict[str, str] = {}
    output_paths: dict[str, Path] = {}
    if records and not dry_run:
        output_paths = write_outputs(records, out_dir, sprint_id)
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

    status = "ok" if usage_mode == USAGE_MODE_ACTUAL else "warning"
    recommended_action = None
    if usage_mode != USAGE_MODE_ACTUAL:
        recommended_action = "Inspect warnings and rerun with a session containing token_count events if actual usage is required."
    return {
        "status": status,
        "usage_mode": usage_mode,
        "command_run_count": len(records),
        "outputs": outputs,
        "sprint_snapshot": sprint_snapshot,
        "warnings": sorted(set(warnings)),
        "warning_count": len(set(warnings)),
        "recommended_action": recommended_action,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-jsonl", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("data/ai-usage"))
    parser.add_argument("--sprint")
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
            manual_map=manual,
            dry_run=args.dry_run,
        )
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
    paths = write_outputs(records, args.out_dir, args.sprint)
    payload = {"command_run_count": len(records), "warnings": warnings, "outputs": {k: str(v) for k, v in paths.items()}}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
    return 0
