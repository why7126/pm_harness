# REQ-0000 建设测试标准

## 1. 背景

OpenSpec + AI 开发需要可重复的测试目录、Pytest 基线、治理文档与 CI，确保 Requirement → Implementation → Test 闭环。

## 2. 目标

- 根目录 `tests/` 金字塔结构（unit / integration / e2e）
- `pytest.ini`、`tests/conftest.py`、覆盖率与治理文档
- 校验脚本与 GitHub Actions 基线

## 3. 状态

`completed` — Sprint-00 建立基线；业务测试随各 Change 扩展。
