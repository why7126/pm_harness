#!/usr/bin/env python3
"""Validate core Agent context-budget and final-output contract guidance."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "rules/agent-context-budget.md",
    ".agents/skills/spec-study/SKILL.md",
]
SKILLS_DIR = ROOT / ".agents" / "skills"
FINAL_CONTRACT_HEADING = "## Final Output Contract"
REQUIRED_FINAL_OUTPUT_CONTRACT_SNIPPETS = (
    "不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例",
    "输出判定",
    "暂无可推进下一步",
)
FORBIDDEN_FINAL_OUTPUT_CONTRACT_SNIPPETS = (
    "下一步：<可直接执行的命令",
    "- <需要用户选择",
    "命令结束前，最终回复 MUST 明确包含",
    "MUST 给出可复制执行的命令，例如",
    "例如 `/bug-review BUG-0122`",
    "确认是否立即执行 /req-opsx",
    "确认是否立即执行 /bug-opsx",
)
NORMATIVE_LEAK_RE = re.compile(r"```text[\s\S]*?(?:MUST|SHOULD|Final Output Contract)[\s\S]*?```")


def extract_section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    next_heading = re.search(r"\n## (?!#)", text[start + len(heading):])
    if not next_heading:
        return text[start:]
    return text[start:start + len(heading) + next_heading.start()]


def validate_final_output_hygiene(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    if FINAL_CONTRACT_HEADING not in text:
        return []

    errors: list[str] = []
    section = extract_section(text, FINAL_CONTRACT_HEADING)
    for snippet in REQUIRED_FINAL_OUTPUT_CONTRACT_SNIPPETS:
        if snippet not in section:
            errors.append(f"{rel}: Final Output Contract 缺少输出卫生约束 `{snippet}`")
    for snippet in FORBIDDEN_FINAL_OUTPUT_CONTRACT_SNIPPETS:
        if snippet in section:
            errors.append(f"{rel}: Final Output Contract 残留易被原样输出的旧模板或通用示例 `{snippet}`")
    if NORMATIVE_LEAK_RE.search(section):
        errors.append(f"{rel}: Final Output Contract 示例泄漏 MUST/SHOULD/Final Output Contract 规范语气")
    if "待用户决策/处理" in section and "不得重复" not in section and "只列命令之外" not in section:
        errors.append(f"{rel}: Final Output Contract 缺少下一步与待用户决策/处理去重约束")
    return errors

missing = [path for path in REQUIRED if not (ROOT / path).exists()]
if missing:
    print("Missing required context-budget files:")
    for path in missing:
        print(f"- {path}")
    sys.exit(1)

skill = (ROOT / ".agents/skills/spec-study/SKILL.md").read_text(encoding="utf-8")
if "日志索引" not in skill or "docs/spec-logs/CHANGELOG.md" not in skill:
    print("spec-study skill does not mention log-first learning.")
    sys.exit(1)

budget = (ROOT / "rules/agent-context-budget.md").read_text(encoding="utf-8")
workflow = (ROOT / ".agents/skills/workflow-sync/SKILL.md").read_text(encoding="utf-8")
if "执行链路复盘" not in budget or "执行链路复盘" not in workflow:
    print("command execution review hook is not documented in budget rule and workflow-sync skill.")
    sys.exit(1)

errors: list[str] = []
if SKILLS_DIR.exists():
    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        errors.extend(validate_final_output_hygiene(path))

if errors:
    print("agent context budget validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("agent context budget validation passed")
