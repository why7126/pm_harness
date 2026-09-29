from __future__ import annotations

from typing import Any


LARGE_SPRINT_CHANGE_THRESHOLD = 10
DEFAULT_CHANGE_BATCH_SIZE = 5


def _task_value(change: dict[str, Any], key: str) -> int:
    tasks = change.get("tasks") or {}
    value = tasks.get(key, 0)
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _warning_label_counts(warnings: list[dict[str, Any]]) -> dict[str, int]:
    labels: dict[str, int] = {}
    for warning in warnings:
        kind = str(warning.get("kind") or "unknown")
        labels[kind] = labels.get(kind, 0) + 1
    return labels


def _warnings_for_change(warnings: list[dict[str, Any]], change_id: str) -> list[dict[str, Any]]:
    return [warning for warning in warnings if warning.get("target") == change_id]


def _hints_for_change(evidence_hints: list[dict[str, Any]], change_id: str) -> list[dict[str, str]]:
    hints: list[dict[str, str]] = []
    for hint in evidence_hints:
        reason = str(hint.get("reason") or "")
        path = str(hint.get("path") or "")
        if change_id not in reason and change_id not in path:
            continue
        hints.append(
            {
                "reason": reason,
                "path": path,
            }
        )
    return hints


def build_change_batches(
    changes: list[dict[str, Any]],
    *,
    warnings: list[dict[str, Any]] | None = None,
    evidence_hints: list[dict[str, Any]] | None = None,
    ordering: str,
    batch_size: int = DEFAULT_CHANGE_BATCH_SIZE,
    threshold: int = LARGE_SPRINT_CHANGE_THRESHOLD,
) -> dict[str, Any]:
    """Build compact, machine-readable batches for large Sprint change scopes."""

    total_changes = len(changes)
    applicable = total_changes >= threshold
    warning_rows = warnings or []
    hint_rows = evidence_hints or []
    summary: dict[str, Any] = {
        "applicable": applicable,
        "reason": "large-sprint" if applicable else "not_applicable",
        "threshold": threshold,
        "batch_size": batch_size,
        "total_changes": total_changes,
        "batch_count": 0,
        "ordering": ordering,
        "batches": [],
    }
    if not applicable:
        return summary

    batches: list[dict[str, Any]] = []
    for batch_index, start in enumerate(range(0, total_changes, batch_size), start=1):
        batch_changes = changes[start : start + batch_size]
        change_ids = [str(change.get("change_id")) for change in batch_changes]
        batch_warnings = [
            warning
            for change_id in change_ids
            for warning in _warnings_for_change(warning_rows, change_id)
        ]
        batch_hints = [
            hint for change_id in change_ids for hint in _hints_for_change(hint_rows, change_id)
        ]
        blockers = [
            {
                "change_id": str(change.get("change_id")),
                "detail": str(change.get("blocker")),
            }
            for change in batch_changes
            if change.get("blocker")
        ]
        trace_present = sum(1 for change in batch_changes if change.get("trace_exists") is True)
        trace_missing = sum(1 for change in batch_changes if change.get("trace_exists") is False)

        batches.append(
            {
                "batch_id": f"batch-{batch_index:03d}",
                "change_ids": change_ids,
                "ordering": ordering,
                "range": {
                    "start": start + 1,
                    "end": start + len(batch_changes),
                },
                "counts": {
                    "changes": len(batch_changes),
                    "tasks_done": sum(_task_value(change, "done") for change in batch_changes),
                    "tasks_total": sum(_task_value(change, "total") for change in batch_changes),
                    "trace_present": trace_present,
                    "trace_missing": trace_missing,
                    "blockers": len(blockers),
                    "warnings": len(batch_warnings),
                    "evidence_hints": len(batch_hints),
                },
                "blockers": blockers,
                "warning_labels": _warning_label_counts(batch_warnings),
                "evidence_hints": batch_hints,
                "recommended_next_read": "batch_evidence_hints" if blockers or batch_warnings else "none",
            }
        )

    summary["batch_count"] = len(batches)
    summary["batches"] = batches
    return summary
