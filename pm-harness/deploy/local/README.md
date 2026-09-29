---
purpose: 本地部署矩阵
content: 本地开发部署环境、前置条件和启动方式
source: deploy local matrix template
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 00:00:00
---

# 本地部署矩阵

默认本地环境 ID：

```text
local-default
```

该环境复用根目录 `docker-compose.yml`。如项目包含自建对象存储、文档站、worker 或本地数据库 profile，可在 `deploy/scripts/up.sh` 中增加对应 profile，并在 env 示例中写清变量用途和安全边界。

启动：

```bash
./deploy/scripts/up.sh local default
```

停止：

```bash
./deploy/scripts/down.sh local
```

真实本地 env 可复制为：

```bash
cp deploy/local/default.env.example deploy/local/default.env
```

真实 env 文件禁止提交。变更本地部署后至少校验：

```bash
python deploy/scripts/validate-env.py --domain local --environment default --env-file deploy/local/default.env.example
docker compose --env-file deploy/local/default.env.example config --quiet
```
