#!/usr/bin/env python3
from pathlib import Path
import sys

FILES = [
"00-总览.md","01-MVP目标与核心假设.md","02-最小业务闭环.md","03-目标用户与用户任务链路.md",
"04-功能范围与优先级.md","05-MVP递进版本路线.md","06-交付验收标准.md","07-验证方案与指标.md",
"08-数据采集与分析方案.md","09-范围边界.md","10-依赖与风险.md","11-人工替代与技术债务.md",
"12-责任与协作建议.md","13-全链路追踪矩阵.md","14-决策记录.md","15-版本差异记录.md","16-设计交接说明.md"]

def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: validate_mvp_baseline.py <基线目录>")
    root = Path(sys.argv[1])
    errors = []
    for name in FILES:
        p = root / name
        if not p.is_file(): errors.append(f"缺少文件: {name}"); continue
        text = p.read_text(encoding="utf-8")
        if len(text.strip()) < 80: errors.append(f"内容过少: {name}")
        if "{{" in text or "}}" in text: errors.append(f"存在未替换占位符: {name}")
    if errors:
        print("校验失败\n" + "\n".join(f"- {e}" for e in errors)); return 1
    print(f"校验通过：{len(FILES)} 个标准文件完整")
    return 0
if __name__ == "__main__": raise SystemExit(main())
