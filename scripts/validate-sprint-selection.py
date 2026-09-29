#!/usr/bin/env python3
"""Validate Sprint selection and sequential creation rules."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRINT_RE = re.compile(r"^sprint-(\d{3})$")


@dataclass(frozen=True)
class SprintInventory:
    active: list[str]
    known: list[str]
    next_id: str


def read_sprint_id(path: Path) -> str | None:
    yaml_path = path / "sprint.yaml"
    if not yaml_path.exists():
        return None
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("sprint_id:"):
            return line.split(":", 1)[1].strip()
    return None


def collect_sprints(root: Path = ROOT) -> SprintInventory:
    known: set[str] = set()
    active: set[str] = set()
    for stage in ("change", "archive"):
        stage_dir = root / "iterations" / stage
        if not stage_dir.exists():
            continue
        for path in stage_dir.iterdir():
            if not path.is_dir():
                continue
            if SPRINT_RE.match(path.name):
                known.add(path.name)
                if stage == "change":
                    active.add(path.name)
            yaml_id = read_sprint_id(path)
            if yaml_id and SPRINT_RE.match(yaml_id):
                known.add(yaml_id)
                if stage == "change":
                    active.add(yaml_id)
    max_number = max((int(SPRINT_RE.match(item).group(1)) for item in known if SPRINT_RE.match(item)), default=-1)
    return SprintInventory(active=sorted(active), known=sorted(known), next_id=f"sprint-{max_number + 1:03d}")


def validate_selection(requested: str | None, inventory: SprintInventory) -> tuple[bool, str]:
    active_count = len(inventory.active)
    if requested is None:
        if active_count == 0:
            return True, f"未指定 Sprint，当前无 active Sprint；默认创建 {inventory.next_id}。"
        if active_count == 1:
            return True, f"未指定 Sprint，默认使用当前 Sprint {inventory.active[0]}。"
        return False, "未指定 Sprint，但当前存在多个 active Sprint：" + ", ".join(inventory.active) + "。请使用 /sprint-propose --sprint <sprint-id> 明确指定当前 Sprint。"

    if not SPRINT_RE.match(requested):
        return False, f"Sprint ID 必须使用 sprint-xxx 三位数字格式：{requested}"
    if requested in inventory.active:
        return True, f"指定 Sprint {requested} 为 active Sprint，可继续。"
    if active_count >= 2:
        return False, "当前已存在两个 active Sprint：" + ", ".join(inventory.active) + "。不得创建第三个 Sprint，请指定其中一个当前 Sprint。"
    if requested != inventory.next_id:
        return False, f"新建 Sprint 必须按顺序创建，当前下一个允许编号为 {inventory.next_id}，不得跳号创建 {requested}。"
    if active_count == 1:
        return True, f"指定 {requested} 为下一个连续 Sprint；仅应在当前 Sprint 容量超过 120% 并已阻断后继续。"
    return True, f"指定 {requested} 为下一个连续 Sprint，可创建。"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sprint", help="Requested sprint id. Omit to validate default selection.")
    parser.add_argument("--json", action="store_true", help="Emit compact key lines.")
    args = parser.parse_args()

    inventory = collect_sprints()
    ok, message = validate_selection(args.sprint, inventory)
    if args.json:
        print(f"status={'pass' if ok else 'fail'}")
        print(f"active={','.join(inventory.active)}")
        print(f"next_id={inventory.next_id}")
        print(f"message={message}")
    else:
        print("## Sprint Selection Gate")
        print()
        print(f"Status: {'PASS' if ok else 'FAIL'}")
        print(f"Active Sprints: {', '.join(inventory.active) if inventory.active else 'none'}")
        print(f"Next Sprint: {inventory.next_id}")
        print(f"Message: {message}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
