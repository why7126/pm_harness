#!/usr/bin/env python3
"""Validate pm-harness-init skill package constraints."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "pm-harness-skills" / "pm-harness-init"
MAX_FILES = 200

files = [p for p in SKILL.rglob("*") if p.is_file()]
skill_files = [p for p in files if p.name == "SKILL.md"]
forbidden = [
    p
    for p in files
    if p.name == ".DS_Store"
    or "__pycache__" in p.parts
    or p.suffix == ".pyc"
    or p.suffix == ".zip"
]

errors = []
if len(files) > MAX_FILES:
    errors.append(f"文件数 {len(files)} 超过 Claude Skill 限制 {MAX_FILES}")
if len(skill_files) != 1:
    errors.append(f"必须只有一个 SKILL.md，当前为 {len(skill_files)}")
if forbidden:
    for item in forbidden:
        errors.append(f"包含禁止打包文件: {item.relative_to(SKILL)}")

if errors:
    print("Skill 包校验失败：")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Skill 包校验通过：{len(files)} files, exactly one SKILL.md.")
