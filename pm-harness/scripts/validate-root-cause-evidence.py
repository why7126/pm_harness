#!/usr/bin/env python3
"""Validate lightweight root-cause evidence contracts for BUGs and changes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VALID_STATUSES = {"unknown", "hypothesis", "probable", "confirmed"}
EVIDENCE_WORDS = ("证据", "evidence", "复现", "日志", "截图", "测试", "trace", "pytest", "vitest")


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def find_bug_dir(bug_id: str) -> Path | None:
    for stage in ("plan", "review", "archive"):
        candidate = ROOT / "issues" / "bugs" / stage / bug_id
        if candidate.exists():
            return candidate
    matches = list((ROOT / "issues" / "bugs").glob(f"*/{bug_id}"))
    return matches[0] if matches else None


def extract_status(text: str) -> str | None:
    patterns = [
        r"root_cause_status\s*:\s*([A-Za-z_-]+)",
        r"根因状态\s*[:：]\s*`?([A-Za-z_-]+)`?",
        r"cause_status\s*:\s*([A-Za-z_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().lower()
    return None


def has_evidence(text: str) -> bool:
    lowered = text.lower()
    return any(word.lower() in lowered for word in EVIDENCE_WORDS)


def validate_root_cause_file(path: Path, *, require_confirmed: bool = False) -> list[dict[str, str]]:
    if not path.exists():
        level = "blocker" if require_confirmed else "warning"
        return [{"level": level, "path": relative(path), "message": "root-cause.md 不存在，无法校验根因证据。"}]

    text = path.read_text(encoding="utf-8")
    status = extract_status(text)
    if not status:
        level = "blocker" if require_confirmed else "warning"
        return [{"level": level, "path": relative(path), "message": "缺少 root_cause_status 或“根因状态”。"}]
    if status not in VALID_STATUSES:
        return [{"level": "blocker", "path": relative(path), "message": f"根因状态 `{status}` 不在允许集合中。"}]

    findings: list[dict[str, str]] = []
    if require_confirmed and status != "confirmed":
        findings.append({
            "level": "blocker",
            "path": relative(path),
            "message": f"BUG review approve 要求 root_cause_status 为 `confirmed`，当前为 `{status}`。",
        })
    if status == "confirmed" and not has_evidence(text):
        findings.append({"level": "blocker", "path": relative(path), "message": "confirmed 根因缺少可定位证据链。"})
    if status in {"unknown", "hypothesis", "probable"} and "补证" not in text and "验证" not in text:
        findings.append({"level": "warning", "path": relative(path), "message": f"{status} 根因应记录补证或验证步骤。"})
    return findings


def validate_bug(bug_id: str, *, require_confirmed: bool = False) -> list[dict[str, str]]:
    bug_dir = find_bug_dir(bug_id)
    if bug_dir is None:
        return [{"level": "blocker", "path": bug_id, "message": "未找到 BUG 目录。"}]
    return validate_root_cause_file(bug_dir / "root-cause.md", require_confirmed=require_confirmed)


def bugs_linked_from_change(change_id: str) -> list[str]:
    change_dir = ROOT / "openspec" / "changes" / change_id
    if not change_dir.exists():
        return []
    text_parts = []
    for name in ("proposal.md", "design.md", "tasks.md", "trace.md", "acceptance.md"):
        path = change_dir / name
        if path.exists():
            text_parts.append(path.read_text(encoding="utf-8"))
    return sorted(set(re.findall(r"BUG-\d{4}[A-Za-z0-9_-]*", "\n".join(text_parts))))


def active_bug_ids() -> list[str]:
    bugs_root = ROOT / "issues" / "bugs"
    result: list[str] = []
    for stage in ("plan", "review"):
        stage_dir = bugs_root / stage
        if stage_dir.exists():
            result.extend(path.name for path in stage_dir.iterdir() if path.is_dir() and path.name.startswith("BUG-"))
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bug")
    parser.add_argument("--change")
    parser.add_argument("--all-active", action="store_true")
    parser.add_argument(
        "--require-confirmed",
        action="store_true",
        help="Require root_cause_status: confirmed; intended for /bug-review approve gate.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    if args.bug:
        findings.extend(validate_bug(args.bug, require_confirmed=args.require_confirmed))
    if args.change:
        linked = bugs_linked_from_change(args.change)
        if linked:
            for bug_id in linked:
                findings.extend(validate_bug(bug_id, require_confirmed=args.require_confirmed))
        else:
            findings.append({"level": "info", "path": f"openspec/changes/{args.change}", "message": "未发现 linked BUG，根因证据校验不适用。"})
    if args.all_active:
        for bug_id in active_bug_ids():
            findings.extend(validate_bug(bug_id, require_confirmed=args.require_confirmed))
    if not (args.bug or args.change or args.all_active):
        parser.error("one of --bug, --change, or --all-active is required")

    blockers = [item for item in findings if item["level"] == "blocker"]
    warnings = [item for item in findings if item["level"] == "warning"]
    payload = {
        "status": "failed" if blockers else "passed",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "findings": findings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"root-cause evidence: {payload['status']} blockers={len(blockers)} warnings={len(warnings)}")
        for finding in findings:
            print(f"- {finding['level']}: {finding['path']} - {finding['message']}")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
