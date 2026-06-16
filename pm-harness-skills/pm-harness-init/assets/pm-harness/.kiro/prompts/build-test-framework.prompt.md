---
description: 建立 Testing Governance（pytest / vitest / E2E / CI / 映射）
---

将 `rules/testing.md` 落地为测试目录、基线配置、覆盖率规则与 `validate-test-framework.py`。

**关联 REQ**：`REQ-0000-build-test-standard`（`change_id: build-test-framework`，已归档见 `openspec/specs/testing/`）

**Input**：`--verify` 仅校验

---

## 必须读取

```text
AGENTS.md
rules/testing.md
rules/coding.md
rules/api.md
openspec/specs/testing/spec.md
openspec/testing-mapping.md
pytest.ini / src/backend/tests/
src/web vitest 配置
```

---

## 与 req / opsx 关系

```text
REQ acceptance.md  →  pytest / vitest / e2e
/req-opsx tasks.md   →  MUST 含测试任务
/opsx-apply          →  新增代码必须新增测试
/sprint-apply        →  跑 change 内测试任务
```

BUG 修复：`/bug-opsx` tasks **MUST** 含回归测试。

---

## Step 1 — 治理文档

```text
docs/standards/testing-governance.md
docs/standards/unit-test-standard.md
docs/standards/frontend-test-standard.md
docs/standards/test-coverage.md
openspec/testing-mapping.md
```

金字塔：Unit 70% / Integration 20% / E2E 10%。

---

## Step 2 — 目录与基线

```text
src/backend/tests/          # pytest（本项目主路径）
src/web/**/*.test.tsx       # vitest
tests/e2e/                  # Playwright（可选）
tests/fixtures/
pytest.ini
.coveragerc
.github/workflows/test.yml
```

`conftest.py`：TestClient、SQLite、MinIO fixture。

---

## Step 3 — 映射

`openspec/testing-mapping.md` 维护：

```yaml
REQ-xxxx:
  acceptance: [AC-001, …]
  tests: [test_…]
```

每个 **approved** REQ 在 `req-complete` 时应有关联测试计划（`test-plan.md` 或 acceptance 内）。

---

## Step 4 — 校验

```bash
python scripts/validate-test-framework.py
cd src/backend && uv run pytest
cd src/web && pnpm exec vitest run
```

---

## Step 5 — OpenSpec

已归档 **勿重建** `build-test-framework`。测试规范变更走新 REQ + `/req-opsx`。

---

## 验收

```text
□ validate-test-framework.py pass
□ CI workflow 存在
□ testing-mapping 含 REQ-0000 三项
□ Backend coverage 目标文档化（≥80%）
```
