---
purpose: 部署环境矩阵入口
content: deploy 目录职责、环境 ID、Compose/env/script 分工
source: deploy matrix template
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 00:00:00
---

# deploy 部署矩阵

`deploy/` 用于表达本地与生产部署环境矩阵。根目录 `docker-compose.yml` 可继续作为最小本地/demo 编排入口；新增环境优先在 `deploy/` 下表达。

原则：

- 一拓扑一 Compose：服务拓扑变化才新增 Compose 或 profile。
- 一环境一 env 示例：变量差异通过 `*.env.example` 表达。
- 脚本集中：`deploy/scripts/` 负责环境解析、校验、up/down。
- 安全优先：只提交 `.env.example`，不得提交真实 `.env`、密钥、数据库连接串、客户数据、运行时数据库、对象存储数据或镜像包。

## 环境矩阵

| 环境 ID | 域 | 用途 | Compose | env 示例 |
|---|---|---|---|---|
| `local-default` | local | 本地开发/demo | `docker-compose.yml` | `deploy/local/default.env.example` |
| `prod-external` | prod | 生产外部数据库/对象存储 | 项目生产 Compose | `deploy/prod/external.env.example` |

## 命令

```bash
./deploy/scripts/up.sh local default
./deploy/scripts/up.sh prod external
./deploy/scripts/down.sh local
./deploy/scripts/down.sh prod
```

项目可继续保留兼容入口：

```bash
./scripts/docker-up.sh
./scripts/docker-down.sh
```

新增部署环境时，必须同步：

- `deploy/README.md`
- 对应 `deploy/<domain>/README.md`
- 对应 `*.env.example`
- `deploy/scripts/up.sh` / `deploy/scripts/down.sh`
- `docs/02-deployment.md`
- `.env.example`
