#!/usr/bin/env python3
"""Validate a pm-prd-plan Markdown baseline directory."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "00-规划总览.md",
    "01-产品架构.md",
    "02-产品里程碑.md",
    "03-产品功能清单.md",
    "04-范围与边界.md",
    "05-依赖与风险.md",
    "06-规划决策记录.md",
    "07-版本差异.md",
    "08-产品设计交接说明.md",
]

FORBIDDEN_PLACEHOLDERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"待填写",
    r"示例内容",
    r"<product>",
    r"<version>",
]

REQUIRED_TERMS = {
    "00-规划总览.md": ["规划目标", "完整性检查"],
    "01-产品架构.md": ["mermaid", "产品域", "边界", "依赖"],
    "02-产品里程碑.md": ["业务目标", "最小必要范围", "退出标准"],
    "03-产品功能清单.md": ["功能 ID", "优先级", "里程碑", "依赖", "边界"],
    "04-范围与边界.md": ["产品内", "产品外"],
    "05-依赖与风险.md": ["业务", "数据", "技术", "组织", "外部", "责任建议"],
    "06-规划决策记录.md": ["决策 ID", "推荐", "最终结论"],
    "07-版本差异.md": ["版本", "变更"],
    "08-产品设计交接说明.md": ["设计目标", "规划边界"],
}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"目录不存在：{root}"]

    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            errors.append(f"缺少文件：{name}")
            continue
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 120:
            errors.append(f"内容过少：{name}")
        for pattern in FORBIDDEN_PLACEHOLDERS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(f"存在模板占位符：{name} / {pattern}")
        lower = text.lower()
        for term in REQUIRED_TERMS[name]:
            if term.lower() not in lower:
                errors.append(f"缺少必需内容：{name} / {term}")

    markdown_files = {p.name for p in root.glob("*.md")}
    extras = sorted(markdown_files - set(REQUIRED_FILES))
    if extras:
        errors.append("存在非标准 Markdown 文件：" + ", ".join(extras))
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：validate_baseline.py <规划基线目录>", file=sys.stderr)
        return 2
    errors = validate(Path(sys.argv[1]).resolve())
    if errors:
        print("规划基线校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("规划基线校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

