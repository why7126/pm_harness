---
purpose: 生产部署矩阵
content: 生产外部依赖环境、启动方式和安全边界
source: deploy prod matrix template
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 00:00:00
---

# 生产部署矩阵

默认生产环境 ID：

```text
prod-external
```

该环境适用于生产服务使用外部数据库、对象存储或托管云服务的部署方式。生产 Compose 文件由具体项目提供；如尚未建立生产 Compose，`up.sh prod external` 会阻断并提示补齐。

前置条件：

- 生产数据库、账号和最小权限已创建。
- 对象存储 bucket、region、endpoint、访问密钥和权限策略已创建。
- `APP_SECRET_KEY`、管理员初始密码、数据库连接串和对象存储密钥必须来自生产密钥系统或受控 env 文件。
- 生产不得使用 SQLite、示例密钥、默认密码或本地对象存储占位配置。

配置：

```bash
cp deploy/prod/external.env.example deploy/prod/external.env
# 编辑 deploy/prod/external.env，替换所有生产占位值
./deploy/scripts/up.sh prod external
```

停止：

```bash
./deploy/scripts/down.sh prod
```

生产 env、日志和维护任务输出不得包含密钥、数据库连接串、Authorization header、Cookie、真实客户数据、本机绝对路径或不可公开域名。

校验提交的示例文件结构时可允许占位值：

```bash
python deploy/scripts/validate-env.py --domain prod --environment external --env-file deploy/prod/external.env.example --allow-example-values
```

真实生产 env 校验不得使用 `--allow-example-values`。
