---
purpose: 系统架构
content: 系统模块、前后端分层、数据流、存储链路、集成边界和 AI 开发边界
source: Harness docs Token 优化模板，初始化时基于用户输入与技术栈生成
update_method: 架构、模块边界、技术栈、集成方式或运行链路变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
status: draft
note: 本文档是架构摘要，不替代 OpenSpec 能力规格
---

# 系统架构

## 1. 总体架构

```text
{CLIENTS}
    ↓
{BACKEND_STACK}
    ↓
{DATABASE_STACK}
    ↓
{OBJECT_STORAGE_STACK}
```

如启用异步任务、算法服务、第三方系统或消息队列，应在此补充：

```text
{OPTIONAL_RUNTIME_COMPONENTS}
```

## 2. 模块边界

| 模块 | 路径 | 职责 | 主要依赖 |
|---|---|---|---|
| 后端 | `src/backend/` | API、服务、数据访问、后台任务 | `{BACKEND_STACK}` |
| Web 前端 | `src/web/` | 页面、交互、状态、接口调用 | `{FRONTEND_STACK}` |
| 移动/小程序/桌面端 | `src/wechat-miniapp/`、`src/android/`、`src/ios/`、`src/desktop/` | 端能力与平台适配 | `{PRODUCT_FORMS}` |
| 共享层 | `src/shared/`、`src/sdk/` | 类型、常量、契约、SDK | OpenAPI / 生成物 |
| 基础设施 | `deploy/`、`docker-compose*.yml` | 部署、环境、端口、观测 | `{DEPLOYMENT_STACK}` |

## 3. 后端分层

推荐分层：

```text
api -> schemas -> services -> repositories -> models
```

复杂业务可增加 domain、jobs、events、adapters 等层，但必须同步 `rules/coding.md` 与目录说明。

## 4. 数据与媒体链路

结构化数据：

```text
Client -> API -> Service -> Repository -> Database
```

文件/媒体数据：

```text
Client -> Backend Upload API -> Validation -> Object Storage -> Metadata Database -> Controlled Read URL
```

前端不得绕过后端直接写入未授权对象存储。

## 5. AI 开发边界

- AI 必须基于 `issues/`、`openspec/changes/`、`rules/` 和相关 docs 开发。
- 不允许凭对话直接修改正式功能，除非变更被判定为轻量文档/注释/无行为变化。
- 改变架构、接口、数据、权限、部署或流程时，必须先更新 OpenSpec Change。
