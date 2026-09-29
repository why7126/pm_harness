#!/usr/bin/env python3
from pathlib import Path
import sys

REQUIRED = [
    "00-方案总览.md", "01-问题目标与范围.md", "02-角色与核心场景.md",
    "03-端到端业务流程.md", "04-核心业务对象与关系.md", "05-功能机制与业务规则.md",
    "06-权限与责任.md", "07-状态与生命周期.md", "08-异常与边界场景.md",
    "09-备选方案与取舍.md", "10-影响依赖与风险.md", "11-验收意图.md",
    "12-决策与未决问题.md", "13-全链路追踪矩阵.md", "14-版本差异记录.md",
    "15-产品设计交接说明.md",
]

def main() -> int:
    if len(sys.argv) != 2:
        print("用法: validate_solution_baseline.py <方案基线目录>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    errors = []
    if not root.is_dir():
        errors.append(f"目录不存在: {root}")
    else:
        for name in REQUIRED:
            path = root / name
            if not path.is_file():
                errors.append(f"缺少文件: {name}")
            elif not path.read_text(encoding="utf-8").strip():
                errors.append(f"空文件: {name}")
        all_text = "\n".join(
            p.read_text(encoding="utf-8") for p in root.glob("*.md") if p.is_file()
        )
        for marker in ("{{", "TODO", "待填写"):
            if marker in all_text:
                errors.append(f"存在未完成占位符: {marker}")
    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"校验通过: {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
