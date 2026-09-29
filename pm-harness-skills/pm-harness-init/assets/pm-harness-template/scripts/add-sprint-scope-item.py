#!/usr/bin/env python3
"""Add a reviewed REQ/BUG and/or Change to a Sprint machine scope."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_sync.collect import ROOT, load_sprint, read_text


@contextlib.contextmanager
def sprint_scope_lock(path: Path):
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def section_bounds(lines: list[str], key: str) -> tuple[int, int] | None:
    start: int | None = None
    for index, line in enumerate(lines):
        if line == f"{key}:":
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith(" ") and re.match(r"^[A-Za-z0-9_]+:", line):
            end = index
            break
    return start, end


def ensure_list_item(lines: list[str], key: str, value: str, *, after_key: str | None = None) -> bool:
    bounds = section_bounds(lines, key)
    item = f"  - {value}"
    if bounds is not None:
        start, end = bounds
        if item in lines[start + 1 : end]:
            return False
        lines.insert(end, item)
        return True

    insert_at = len(lines)
    if after_key:
        after_bounds = section_bounds(lines, after_key)
        if after_bounds is not None:
            insert_at = after_bounds[1]
    lines.insert(insert_at, f"{key}:")
    lines.insert(insert_at + 1, item)
    return True


def set_scalar(lines: list[str], key: str, value: str) -> bool:
    line = f"{key}: {value}"
    for index, existing in enumerate(lines):
        if existing.startswith(f"{key}:"):
            if existing == line:
                return False
            lines[index] = line
            return True
    lines.append(line)
    return True


def scope_item_bounds(lines: list[str], item_id: str) -> tuple[int, int] | None:
    bounds = section_bounds(lines, "scope_estimates")
    if bounds is None:
        return None
    start, end = bounds
    index = start + 1
    while index < end:
        if lines[index].strip() != f"- id: {item_id}":
            index += 1
            continue
        item_end = end
        for next_index in range(index + 1, end):
            if lines[next_index].startswith("  - id: "):
                item_end = next_index
                break
        return index, item_end
    return None


def ensure_scope_estimate(
    lines: list[str],
    *,
    item_id: str,
    req_id: str | None,
    bug_id: str | None,
    change_id: str | None,
    size: str,
    story_points: str,
    person_days: str,
    rationale: str,
) -> bool:
    if scope_item_bounds(lines, item_id) is not None:
        return sync_scope_estimate_change(lines, item_id, change_id)

    bounds = section_bounds(lines, "scope_estimates")
    if bounds is None:
        lines.append("scope_estimates:")
        bounds = (len(lines) - 1, len(lines))
    _, end = bounds

    block = [f"  - id: {item_id}"]
    if req_id:
        block.append(f"    requirement: {req_id}")
    if bug_id:
        block.append(f"    bug: {bug_id}")
    if change_id:
        block.append(f"    change: {change_id}")
    block.extend(
        [
            f"    size: {size}",
            f"    story_points: {story_points}",
            f"    estimated_person_days: {person_days}",
            f"    rationale: {rationale}",
        ]
    )
    lines[end:end] = block
    return True


def sync_scope_estimate_change(lines: list[str], item_id: str, change_id: str | None) -> bool:
    if not change_id:
        return False
    bounds = scope_item_bounds(lines, item_id)
    if bounds is None:
        return False
    start, end = bounds
    for index in range(start + 1, end):
        if re.match(r"^\s+change:\s*", lines[index]):
            expected = f"    change: {change_id}"
            if lines[index] == expected:
                return False
            lines[index] = expected
            return True
    lines.insert(start + 1, f"    change: {change_id}")
    return True


def estimate_totals(lines: list[str]) -> tuple[float, float]:
    bounds = section_bounds(lines, "scope_estimates")
    if bounds is None:
        return 0.0, 0.0
    start, end = bounds
    story_points = 0.0
    person_days = 0.0
    for line in lines[start + 1 : end]:
        stripped = line.strip()
        if stripped.startswith("story_points:"):
            story_points += float(stripped.split(":", 1)[1].strip())
        if stripped.startswith("estimated_person_days:"):
            person_days += float(stripped.split(":", 1)[1].strip())
    return story_points, person_days


def scalar_from_capacity(lines: list[str], key: str) -> float | None:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            raw = stripped.split(":", 1)[1].strip()
            try:
                return float(raw)
            except ValueError:
                return None
    return None


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def update_capacity(lines: list[str]) -> bool:
    story_points, person_days = estimate_totals(lines)
    capacity = scalar_from_capacity(lines, "capacity_person_days")
    changed = False
    changed |= set_scalar(lines, "estimated_story_points", format_number(story_points))
    changed |= set_scalar(lines, "estimated_person_days", format_number(person_days))
    if capacity and capacity > 0:
        usage = person_days / capacity
        buffer_days = max(capacity - person_days, 0)
        buffer_ratio = buffer_days / capacity
        changed |= set_scalar(lines, "capacity_usage", f"{usage:.4f}".rstrip("0").rstrip("."))
        changed |= set_scalar(lines, "fix_buffer_person_days", format_number(buffer_days))
        changed |= set_scalar(lines, "fix_buffer_ratio", f"{buffer_ratio:.4f}".rstrip("0").rstrip("."))
        changed |= patch_capacity_gate(lines, person_days, usage, capacity)
    return changed


def patch_capacity_gate(lines: list[str], person_days: float, usage: float, capacity: float) -> bool:
    bounds = section_bounds(lines, "capacity_gate")
    if bounds is None:
        return False
    start, end = bounds
    changed = False
    replacements = {
        "estimated_person_days": format_number(person_days),
        "capacity_usage": f"{usage:.4f}".rstrip("0").rstrip("."),
    }
    for index in range(start + 1, end):
        stripped = lines[index].strip()
        for key, value in replacements.items():
            if stripped.startswith(f"{key}:"):
                expected = f"  {key}: {value}"
                if lines[index] != expected:
                    lines[index] = expected
                    changed = True
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sprint", required=True)
    parser.add_argument("--req")
    parser.add_argument("--bug")
    parser.add_argument("--change")
    parser.add_argument("--size", default="S")
    parser.add_argument("--story-points", default="1")
    parser.add_argument("--person-days", default="1")
    parser.add_argument("--rationale", required=True)
    args = parser.parse_args()

    if not args.req and not args.bug and not args.change:
        raise SystemExit("at least one of --req, --bug or --change is required")
    if args.req and args.bug:
        raise SystemExit("--req and --bug are mutually exclusive")

    sprint = load_sprint(args.sprint)
    if sprint is None:
        raise SystemExit(f"sprint not found: {args.sprint}")

    path = sprint.path / "sprint.yaml"
    with sprint_scope_lock(path):
        original = read_text(path)
        lines = original.splitlines()
        changed = False

        if args.req:
            changed |= ensure_list_item(lines, "requirements", args.req, after_key="capacity")
        if args.bug:
            changed |= ensure_list_item(lines, "bugs", args.bug, after_key="requirements")
        if args.change:
            changed |= ensure_list_item(lines, "changes", args.change, after_key="bugs")

        item_id = args.req or args.bug or args.change
        changed |= ensure_scope_estimate(
            lines,
            item_id=item_id,
            req_id=args.req,
            bug_id=args.bug,
            change_id=args.change,
            size=args.size,
            story_points=args.story_points,
            person_days=args.person_days,
            rationale=args.rationale,
        )
        changed |= update_capacity(lines)

        updated = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed = True

    print("## Sprint Scope Item")
    print()
    print(f"**Sprint:** {args.sprint}")
    if args.req:
        print(f"**REQ:** {args.req}")
    if args.bug:
        print(f"**BUG:** {args.bug}")
    if args.change:
        print(f"**Change:** {args.change}")
    print(f"**Updated:** {'yes' if changed else 'no'}")
    print(f"**Path:** `{path.relative_to(ROOT)}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
