#!/usr/bin/env python3
"""Validate the product data collection and observability standard."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = "docs/standards/product-data-collection-observability.md"

REQUIRED_TERMS = [
    "usage_events",
    "request_logs",
    "task_traces",
    "task_trace_spans",
    "behavior_trace_id",
    "behavior_event_id",
    "parent_behavior_event_id",
    "request_id",
    "client_request_id",
    "parent_request_id",
    "Task Trace",
    "标准数据结构",
    "可空与关联规则",
    "产品扩展",
    "Authorization",
    "Cookie",
    "Token",
    "完整请求体",
    "完整响应体",
    "本机绝对路径",
    "真实客户敏感数据",
    "product_data_collection_observability",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    standard_path = ROOT / STANDARD
    if not standard_path.exists():
        errors.append(f"缺少必需文件: {STANDARD}")
    else:
        text = read(standard_path)
        for term in REQUIRED_TERMS:
            if term not in text:
                errors.append(f"{STANDARD} 缺少关键内容: {term}")

    docs_readme = ROOT / "docs/README.md"
    if docs_readme.exists() and STANDARD not in read(docs_readme):
        errors.append("docs/README.md 缺少采集规范引用")

    api_governance = ROOT / "docs/standards/api-governance.md"
    if api_governance.exists() and STANDARD not in read(api_governance):
        errors.append("docs/standards/api-governance.md 缺少采集规范引用")

    if errors:
        print("通用产品数据采集与链路观测规范校验失败：")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("通用产品数据采集与链路观测规范校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
