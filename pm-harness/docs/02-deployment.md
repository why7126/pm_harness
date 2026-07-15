---
purpose: 部署说明
content: 部署组件、环境变量、Docker Compose、生产部署、数据持久化和运维校验
source: Harness docs Token 优化模板，初始化时基于部署栈生成
update_method: 部署拓扑、镜像、环境变量、端口、数据卷或生产运维流程变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 真实生产密钥、域名和连接串不得写入本文档
---

# 部署说明

## 1. 部署组件

| 组件 | 技术栈 | 说明 |
|---|---|---|
| Backend | `{BACKEND_STACK}` | API、鉴权、业务服务 |
| Web / Client | `{FRONTEND_STACK}` | 静态资源或客户端应用 |
| Database | `{DATABASE_STACK}` | 结构化数据 |
| Object Storage | `{OBJECT_STORAGE_STACK}` | 文件、图片、视频、附件 |
| Async / Jobs | `{ASYNC_TASK_STACK}` | 后台任务（如启用） |

## 2. 配置入口

| 文件 | 作用 |
|---|---|
| `.env.example` | 可提交的环境变量示例 |
| `docker-compose.yml` | 本地开发 / demo 编排 |
| `docker-compose.prod.yml` | 生产编排（如启用） |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/web/Dockerfile` | Web 镜像构建 |
| `deploy/` | 目标环境部署配置 |

环境变量新增或变更时，必须同步 `.env.example`、邻近注释和 `rules/environment.md`。

## 3. 本地启动

```bash
cp .env.example .env
./scripts/docker-up.sh
```

停止：

```bash
./scripts/docker-down.sh
```

如项目不使用 Docker Compose，应在初始化后替换为真实启动命令。

## 4. 数据持久化

| 路径 | 职责 | 提交边界 |
|---|---|---|
| `data/runtime/` | 运行时数据 | 不提交真实数据 |
| `data/tmp/` | 临时处理文件 | 不提交 |
| `data/object-storage/` | 本地对象存储卷 | 不提交真实客户数据 |
| `data/fixtures/` | 测试样例 | 仅脱敏样例 |

实际路径以 `.env.example`、`docker-compose*.yml` 和 `data/README.md` 为准。

## 5. 生产部署

生产部署必须确认：

```text
□ APP_ENV / DEBUG 等环境标识正确
□ DATABASE_URL 指向生产数据库且不使用 demo 默认值
□ 对象存储 bucket / endpoint / 凭据已由安全渠道注入
□ 管理员初始密码和应用密钥不是示例值
□ 端口、域名、HTTPS、反向代理已确认
□ 数据卷、备份、日志、监控和回滚策略已确认
```

生产镜像包、离线交付或云服务器部署流程见 [08-production-image-release.md](08-production-image-release.md)。

## 6. 冒烟校验

部署后至少验证：

```text
□ Web / Client 可访问
□ Backend health endpoint 可访问
□ 登录 / 鉴权链路可用（如启用）
□ 核心 API 可读写
□ 文件上传与受控读取可用（如启用）
□ 重启后数据库与对象存储数据仍可访问
```

## 7. 安全要求

- `.env.example` 只能包含示例值。
- 文档、Issue、截图、日志不得暴露真实密钥、连接串、客户数据或内部域名。
- 生产部署变更必须同步 `rules/release.md`、`rules/security.md` 和相关 OpenSpec / release 记录。
