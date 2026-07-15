#!/usr/bin/env python3
"""Validate that key pm-harness template files are mirrored in the init skill asset."""

from pathlib import Path
import filecmp
import sys

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "pm-harness"
ASSET = ROOT / "pm-harness-skills" / "pm-harness-init" / "assets" / "pm-harness-template"

SYNC_PATHS = [
    ".gitignore",
    ".dockerignore",
    ".env.example",
    "AGENTS.md",
    "README.md",
    "DOCUMENT_METADATA_INDEX.md",
    "project.yaml",
    "docker-compose.yml",
    "pytest.ini",
    ".agents",
    "rules",
    "docs",
    "compatibility",
    "data",
    "deploy",
    "issues",
    "iterations",
    "models",
    "openspec/config.yaml",
    "openspec/project.md",
    "openspec/testing-mapping.md",
    "scripts",
    "tests",
]

errors = []

for rel in SYNC_PATHS:
    left = MAIN / rel
    right = ASSET / rel
    if not left.exists():
        errors.append(f"主模板缺少: {rel}")
        continue
    if not right.exists():
        errors.append(f"Skill 资产缺少: {rel}")
        continue
    if left.is_file():
        if not filecmp.cmp(left, right, shallow=False):
            errors.append(f"文件不同步: {rel}")
        continue
    for item in left.rglob("*"):
        if item.is_dir():
            continue
        rel_item = item.relative_to(left)
        other = right / rel_item
        if item.name == ".DS_Store" or "__pycache__" in item.parts or item.suffix == ".pyc":
            errors.append(f"主模板包含缓存文件: {rel}/{rel_item}")
            continue
        if not other.exists():
            errors.append(f"Skill 资产缺少: {rel}/{rel_item}")
            continue
        if not filecmp.cmp(item, other, shallow=False):
            errors.append(f"文件不同步: {rel}/{rel_item}")

if errors:
    print("模板同步校验失败：")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("模板同步校验通过。")
