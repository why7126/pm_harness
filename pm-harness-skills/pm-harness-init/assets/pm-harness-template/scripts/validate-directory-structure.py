#!/usr/bin/env python3
"""
文档用途：校验项目目录结构
文档内容：检查禁止的根目录文件、必需目录、Docker部署文件是否存在
内容来源：AI自动生成，项目团队确认
更新方式：目录规范变化时同步更新
备注：该脚本可纳入CI，防止AI或开发人员随意破坏目录结构
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "rules/directory-structure.md",
    "openspec/project.md",
    "src/backend/app/main.py",
    "src/web/package.json",
    "src/miniapp/app.json",
    "docker-compose.yml",
    "src/backend/Dockerfile",
    "src/web/Dockerfile",
    "src/web/nginx.conf",
]

ALLOWED_ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".dockerignore",
    "docker-compose.yml",
    "project.yaml",
    "DOCUMENT_METADATA_INDEX.md",
}

ALLOWED_ROOT_DIRS = {
    "rules",
    "docs",
    "openspec",
    "issues",
    "iterations",
    "compatibility",
    ".claude",
    "src",
    "tests",
    "scripts",
    "data",
}

errors = []

for item in REQUIRED_PATHS:
    if not (ROOT / item).exists():
        errors.append(f"缺少必需路径: {item}")

for child in ROOT.iterdir():
    if child.name.startswith(".git"):
        continue
    if child.is_file() and child.name not in ALLOWED_ROOT_FILES:
        errors.append(f"根目录存在未登记文件: {child.name}")
    if child.is_dir() and child.name not in ALLOWED_ROOT_DIRS:
        errors.append(f"根目录存在未登记目录: {child.name}")

if errors:
    print("目录结构校验失败：")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("目录结构校验通过。")
