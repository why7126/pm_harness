#!/usr/bin/env python3
"""Validate the PM Harness template directory structure."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "project.yaml",
    "DOCUMENT_METADATA_INDEX.md",
    ".gitignore",
    ".dockerignore",
    ".env.example",
    "pytest.ini",
    "rules/directory-structure.md",
    "rules/issues-lifecycle.md",
    "rules/iterations-lifecycle.md",
    "rules/global.md",
    "rules/testing.md",
    "issues/requirements/_registry.yaml",
    "issues/bugs/_registry.yaml",
    "docs/README.md",
    "docs/00-product-overview.md",
    "docs/01-architecture.md",
    "docs/02-deployment.md",
    "docs/03-api-index.md",
    "docs/04-database-design.md",
    "docs/05-compatibility-matrix.md",
    "docs/knowledge-base/README.md",
    "openspec/project.md",
    "openspec/config.yaml",
    "openspec/testing-mapping.md",
    "docker-compose.yml",
    "scripts/promote-issue-stage.py",
    "scripts/validate-directory-structure.py",
]

REQUIRED_DIRS = [
    ".agents",
    ".claude",
    ".codex",
    ".cursor",
    ".kiro",
    ".opencode",
    "rules",
    "docs",
    "docs/standards",
    "docs/knowledge-base",
    "docs/knowledge-base/best-practices",
    "docs/knowledge-base/incidents",
    "docs/knowledge-base/sprints",
    "compatibility",
    "compatibility/database",
    "compatibility/devices",
    "compatibility/object-storage",
    "openspec",
    "openspec/specs",
    "openspec/changes",
    "openspec/archive",
    "issues",
    "issues/requirements",
    "issues/requirements/plan",
    "issues/requirements/review",
    "issues/requirements/archive",
    "issues/bugs",
    "issues/bugs/plan",
    "issues/bugs/review",
    "issues/bugs/archive",
    "iterations",
    "iterations/change",
    "iterations/archive",
    "scripts",
    "src",
    "src/backend",
    "src/web",
    "src/wechat-miniapp",
    "src/shared",
    "src/sdk",
    "src/infrastructure",
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/integration/api",
    "tests/e2e",
    "tests/compatibility",
    "data",
    "models",
    "deploy",
]

ALLOWED_ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".dockerignore",
    ".env.example",
    "docker-compose.yml",
    "project.yaml",
    "DOCUMENT_METADATA_INDEX.md",
    "pytest.ini",
}

ALLOWED_ROOT_DIRS = {
    "rules",
    "docs",
    "openspec",
    "issues",
    "iterations",
    "compatibility",
    ".agents",
    ".claude",
    ".codex",
    ".cursor",
    ".kiro",
    ".opencode",
    "src",
    "tests",
    "scripts",
    "data",
    "models",
    "deploy",
}

errors = []

for item in REQUIRED_PATHS:
    if not (ROOT / item).exists():
        errors.append(f"缺少必需路径: {item}")

for item in REQUIRED_DIRS:
    if not (ROOT / item).is_dir():
        errors.append(f"缺少必需目录: {item}")

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
