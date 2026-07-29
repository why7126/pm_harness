#!/usr/bin/env python3
"""
文档用途：校验测试框架基线
文档内容：检查 pytest 配置、治理文档、基线测试是否存在
内容来源：build-test-framework / initialize-project
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "pytest.ini",
    "tests/conftest.py",
    "docs/standards/testing-governance.md",
    "docs/standards/unit-test-standard.md",
    "docs/standards/frontend-test-standard.md",
    ".coveragerc",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
]

errors: list[str] = []


def has_python_tests(directory: Path) -> bool:
    if not directory.exists():
        return False
    return any(directory.rglob("test_*.py"))


def main() -> int:
    for item in REQUIRED:
        if not (ROOT / item).exists():
            errors.append(f"缺少: {item}")

    if not has_python_tests(ROOT / "tests" / "unit"):
        errors.append("tests/unit/ 下无 test_*.py")
    if not has_python_tests(ROOT / "tests" / "integration"):
        errors.append("tests/integration/ 下无 test_*.py")

    backend_tests = ROOT / "src" / "backend" / "tests"
    if not has_python_tests(backend_tests):
        errors.append("src/backend/tests/ 下无 test_*.py（建议保留认证等集成测试）")

    if errors:
        print("测试框架校验失败：")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("测试框架校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
