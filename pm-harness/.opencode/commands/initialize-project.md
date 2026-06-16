---
description: 根据 project.yaml 完成项目基础设施（DS / API / Test / Docker / Sprint-000）
---

根据 `project.yaml` 与 `rules/*` 完成**一次性**基础设施建设。与业务需求流分离：治理类能力登记为 `REQ-0000-*`，经 **`req-*` → `req-opsx` → `opsx-apply` → `sprint-archive`** 闭环。

**Input**：无，或 `--step design-system|api|test|docker|sprint` 只跑子步骤

**禁止**：跳过 OpenSpec CLI 手写 `openspec/changes/`；业务 REQ 不得用本命令代替 `/req-capture`。

---

## 必须读取

```text
AGENTS.md
openspec/project.md
project.yaml
rules/*
docs/02-deployment.md
```

---

## 前置关系

```text
/initialize-project
    ├─ /build-design-system      → REQ-0000-build-design-system
    ├─ /build-api-standard       → REQ-0000-build-api-standard
    ├─ /build-test-framework     → REQ-0000-build-test-standard
    ├─ Docker / .env.example
    └─ /sprint-propose sprint-000   （登记已交付治理迭代）
```

已归档能力见 `openspec/specs/`（`design-system`、`api-governance`、`testing`）。**扩展**治理规范须新建 REQ + `/req-opsx`，不得直接改本命令重复建仓。

---

## Step 1 — Design System

执行 **`/build-design-system`**（或 `--step design-system`）。

产出：`src/shared/design-system/`、`src/web` 样式与校验脚本、`/design-system` 预览。

---

## Step 2 — API Standard

执行 **`/build-api-standard`**（或 `--step api`）。

产出：`docs/standards/api-governance.md`、`error-codes`、FastAPI 分层模板、`validate-api-standard.py`。

---

## Step 3 — Database Standard

读 `rules/database.md`；生成/核对：

```text
src/backend/app/models/
src/backend/app/repositories/
src/backend/app/db/schema.sql
docs/04-database-design.md
```

（无独立 change；随业务 REQ 的 `req-opsx` 演进 schema。）

---

## Step 4 — Test Framework

执行 **`/build-test-framework`**（或 `--step test`）。

产出：`tests/`、`pytest.ini`、Vitest 基线、`validate-test-framework.py`、CI workflow。

---

## Step 5 — Docker 基线

读 `project.yaml`、`docs/02-deployment.md`；核对：

```text
docker-compose.yml
src/backend/Dockerfile
src/web/Dockerfile
.env.example
scripts/docker-up.sh
scripts/docker-down.sh
```

---

## Step 6 — Sprint-000 与 REQ-0000 登记

若 `iterations/sprint-000/` 不存在：

1. **`/sprint-propose sprint-000`** — 纳入（须已 **approved** 或治理 REQ 标记 `done`）：
   - `REQ-0000-build-design-system`
   - `REQ-0000-build-api-standard`
   - `REQ-0000-build-test-standard`
2. 各 REQ 若缺 `review.md`：补评审记录，`status: approved` 或 `done`
3. Change 已归档则 `sprint.yaml` 的 `changes[]` 指向 archive 状态；`sprint.md` 标 **completed**

若 REQ-0000 目录不存在：

```text
/req-capture → /req-generate → /req-complete → /req-review --approve
/req-opsx REQ-0000-build-* 
/opsx-apply → /opsx-archive
```

---

## 验收

```text
□ validate-design-system.py 可运行
□ validate-api-standard.py 可运行
□ validate-test-framework.py 可运行
□ docker compose config 通过
□ iterations/sprint-000 四件套存在
□ openspec/specs 含 design-system、api-governance、testing
```

## Next

业务需求走 **`/req-capture`** … **`/sprint-propose sprint-001`**，勿再调用本命令。
