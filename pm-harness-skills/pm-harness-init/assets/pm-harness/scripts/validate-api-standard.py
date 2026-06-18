#!/usr/bin/env python3
"""
文档用途：校验 API 标准合规性
文档内容：检查路由 OpenAPI 元数据、错误码引用等
内容来源：build-api-standard / initialize-project
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "src" / "backend" / "app" / "api"

violations: list[str] = []


def check_router_file(path: Path) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # Heuristic: route handlers often have router decorator
        for dec in node.decorator_list:
            src = ast.get_source_segment(text, dec) or ""
            if "router." not in src and "app." not in src:
                continue
            if "get(" in src or "post(" in src or "put(" in src or "patch(" in src or "delete(" in src:
                body = ast.get_source_segment(text, node) or ""
                if "response_model" not in src and "response_model" not in body:
                    violations.append(
                        f"{rel}:{node.lineno} — 路由 {node.name} 缺少 response_model"
                    )
                if "tags=" not in src:
                    violations.append(f"{rel}:{node.lineno} — 路由 {node.name} 缺少 tags")
                if "summary=" not in src:
                    violations.append(f"{rel}:{node.lineno} — 路由 {node.name} 缺少 summary")
                break


def main() -> int:
    if not API_DIR.exists():
        print("API 目录不存在，跳过校验。")
        return 0

    for path in API_DIR.rglob("*.py"):
        if path.name.startswith("_"):
            continue
        try:
            check_router_file(path)
        except SyntaxError as e:
            violations.append(f"{path.relative_to(ROOT)} — 语法错误: {e}")

    required_docs = [
        "docs/standards/api-governance.md",
        "docs/standards/error-codes.md",
        "src/backend/app/core/error_codes.py",
        "src/backend/app/schemas/common.py",
    ]
    for doc in required_docs:
        if not (ROOT / doc).exists():
            violations.append(f"缺少必需文件: {doc}")

    if violations:
        print("API 标准校验失败：")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("API 标准校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
