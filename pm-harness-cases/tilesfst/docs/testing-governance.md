---
purpose: 测试治理体系
content: 测试金字塔、目录职责、AI 补测与 CI 要求
source: rules/testing.md / build-test-framework
update_method: 测试规范变更时同步更新
---

# 测试治理体系

## 测试目标

验证：正确性、稳定性、兼容性、安全性、回归能力。

## 测试金字塔

```text
            E2E (10%)
         Integration (20%)
            Unit (70%)
```

## 目录职责

| 目录 | 职责 |
|------|------|
| `tests/unit/` | Service、Repository、工具、错误码 |
| `tests/integration/` | API、数据库、MinIO |
| `tests/e2e/` | Playwright 端到端 |
| `tests/compatibility/` | Web、小程序、SQLite、Docker |
| `tests/fixtures/` | 共享测试数据 |
| `src/backend/tests/` | 后端模块就近测试（兼容） |
| `src/web/src/**/*.test.tsx` | 前端 Vitest |

## AI 开发要求

任何 OpenSpec Change 新增代码 MUST 补充对应测试；禁止只改实现不补测试。

## 运行

```bash
./scripts/run-tests.sh
cd src/web && pnpm test
```

## 覆盖率

见 `docs/test-coverage.md`、`.coveragerc`

## 校验

```bash
python scripts/validate-test-framework.py
```

## 相关

- `docs/unit-test-standard.md`
- `docs/frontend-test-standard.md`
- `openspec/testing-mapping.md`
