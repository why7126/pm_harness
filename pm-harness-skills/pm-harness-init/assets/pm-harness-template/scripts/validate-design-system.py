#!/usr/bin/env python3
"""
文档用途：校验 Design System 合规性
文档内容：检查 Hex 硬编码、裸原生控件、绕过 shared/ui 等问题
内容来源：build-design-system / initialize-project
更新方式：DS 规则变化时同步更新
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_DIRS = [
    ROOT / "src" / "web" / "src",
    ROOT / "src" / "shared",
]

EXTENSIONS = {".tsx", ".ts", ".css"}

# 允许出现 Hex 的路径（Token 定义与生成文件）
ALLOWED_HEX_PATHS = {
    "globals.css",
    "tokens.generated.css",
    "colors.ts",
    "css.ts",
    "tailwind.config.ts",
    "DesignSystemPage.tsx",
    "design-system.test.tsx",
}

HEX_PATTERN = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
ARBITRARY_BG_PATTERN = re.compile(r"bg-\[#[0-9A-Fa-f]+\]")
NATIVE_CONTROL_PATTERN = re.compile(
    r"<(button|input|select|textarea)\b",
)
NATIVE_SKIP_DIRS = ("components/ui/", "shared/ui/")

violations: list[str] = []


def should_skip_hex(path: Path) -> bool:
    return path.name in ALLOWED_HEX_PATHS or "tokens/" in str(path)


def scan_file(path: Path) -> None:
    rel = path.relative_to(ROOT)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return

    for i, line in enumerate(text.splitlines(), start=1):
        if not should_skip_hex(path):
            if HEX_PATTERN.search(line) and "var(--" not in line:
                violations.append(f"{rel}:{i} — 硬编码 Hex 颜色")
            if ARBITRARY_BG_PATTERN.search(line):
                violations.append(f"{rel}:{i} — 使用 bg-[#...] 任意值")

        if path.suffix in {".tsx", ".ts"} and "pages/dev/" not in str(path):
            if any(skip in str(path) for skip in NATIVE_SKIP_DIRS):
                continue
            if NATIVE_CONTROL_PATTERN.search(line) and "// ds-ok" not in line:
                violations.append(
                    f"{rel}:{i} — 直接使用原生 HTML 控件，应使用 shadcn/shared/ui（可加 // ds-ok 豁免）"
                )


def main() -> int:
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix in EXTENSIONS and path.is_file():
                scan_file(path)

    if violations:
        print("Design System 校验失败：")
        for v in violations:
            print(f"  - {v}")
        print(f"\n共 {len(violations)} 项违规。修复建议：使用 semantic token class，复用 shared/ui。")
        return 1

    print("Design System 校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
