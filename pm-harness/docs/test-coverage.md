---
purpose: 测试覆盖率标准
content: 后端与核心模块覆盖率门槛
source: build-test-framework
update_method: 覆盖率目标调整时同步更新
---

# 测试覆盖率

## 目标

| 范围 | 最低覆盖率 |
|------|------------|
| Backend 整体 | 80% |
| Core 模块（`app/core`、`app/services`） | 90% |

## 配置

`.coveragerc` — 省略 `tests/`、生成代码、迁移占位。

## 测量

```bash
cd src/backend && uv run pytest --cov=app --cov-report=term-missing
```

## CI

`.github/workflows/test.yml` 在 PR 时运行单元与集成测试；覆盖率门禁待团队启用。
