---
purpose: 目录结构规范
content: 约束AI与开发人员遵循当前项目目录边界、文件归属和新增文件规则
source: AI自动生成初稿，项目团队确认
update_method: 目录结构调整时由架构负责人确认后更新；AI只能提出建议，不得擅自放宽规则
note: AGENTS.md 必须强制引用本文档；用于防止AI随意新增目录或把文件放错位置
---

# 目录结构规范

## 1. 目标

本文档用于约束 AI Agent 和开发人员在瓷砖信息管理平台中遵循统一目录结构，避免出现以下问题：

- AI 随意创建新目录。
- 后端、前端、小程序、文档、测试文件混放。
- 绕过 OpenSpec 直接新增业务模块。
- 接口变更后未同步前端 Orval 类型。
- Docker、部署、脚本文件分散在错误位置。

## 2. 顶层目录职责

| 目录 | 职责 | 是否允许随意新增同级目录 |
|---|---|---|
| `rules/` | 全局规范 | 否 |
| `docs/` | 产品与技术文档 | 否 |
| `openspec/` | OpenSpec需求与规格事实源 | 否 |
| `issues/` | 原始需求和BUG池 | 否 |
| `iterations/` | 迭代管理 | 否 |
| `compatibility/` | 兼容性说明 | 否 |
| `.claude/` | AI命令与技能 | 否 |
| `src/` | 源码 | 否 |
| `tests/` | 测试 | 否 |
| `scripts/` | 自动化脚本 | 否 |
| `data/` | 本地开发数据卷 | 是，仅本地环境 |

如需新增顶层目录，必须先创建 OpenSpec Change，并在 `rules/directory-structure.md` 中说明新增原因。

## 3. 源码归属规则

### 3.1 后端代码

后端代码必须放在：

```text
src/backend/app/
```

推荐归属：

```text
src/backend/app/api/              # FastAPI Router
src/backend/app/core/             # 配置、异常、日志、安全等核心能力
src/backend/app/db/               # SQLite连接、schema、迁移辅助
src/backend/app/models/           # 数据模型或ORM模型
src/backend/app/repositories/     # 数据访问层
src/backend/app/schemas/          # Pydantic Schema
src/backend/app/services/         # 应用服务与业务逻辑
src/backend/app/main.py           # 应用入口
```

禁止把后端业务代码放到 `scripts/`、`docs/` 或项目根目录。

### 3.2 Web前端代码

Web展示端与管理端代码必须放在：

```text
src/web/src/
```

推荐归属：

```text
src/web/src/app/                  # 应用入口、路由、布局
src/web/src/pages/                # 页面
src/web/src/features/             # 业务功能模块
src/web/src/components/           # 通用组件
src/web/src/services/             # Axios与API封装
src/web/src/generated/            # Orval生成代码，不允许手工修改
src/web/src/styles/               # 全局样式
```

`src/web/src/generated/` 只能由 Orval 生成，AI 不得直接手写。

### 3.3 微信小程序代码

微信小程序代码必须放在：

```text
src/miniapp/
```

推荐归属：

```text
src/miniapp/pages/                # 页面
src/miniapp/components/           # 组件
src/miniapp/services/             # API调用
src/miniapp/utils/                # 工具函数
```

### 3.4 共享代码

跨端共享类型、常量、错误码应放在：

```text
src/shared/
```

不得把共享定义复制到多个端中。

## 4. 文档归属规则

- 产品需求放入 `docs/prd/`。
- BUG分析放入 `docs/bugs/`。
- 迭代文档放入 `docs/iterations/` 或 `iterations/`。
- 正式系统能力放入 `openspec/specs/`。
- 开发中的变更放入 `openspec/changes/`。
- 已完成变更放入 `openspec/archive/`。

## 5. Docker与部署文件规则

- 根目录只允许存在项目级编排文件：`docker-compose.yml`。
- 后端镜像构建文件放入 `src/backend/Dockerfile`。
- Web镜像构建文件放入 `src/web/Dockerfile`。
- Web Nginx配置放入 `src/web/nginx.conf`。
- Docker启动停止脚本放入 `scripts/`。

## 6. AI新增文件前检查清单

AI 在新增文件前必须回答：

```text
□ 是否已有 OpenSpec Change？
□ 新文件是否属于已有目录职责？
□ 是否需要更新 rules/directory-structure.md？
□ 是否需要更新 AGENTS.md 的目录说明？
□ 是否需要更新 README.md？
□ 是否需要补充测试？
□ 是否需要同步 Orval 生成代码？
```

## 7. 禁止事项

- 禁止在根目录新增业务代码文件。
- 禁止将测试代码放入源码目录外的临时目录。
- 禁止手工修改 Orval 生成代码。
- 禁止在未更新 OpenSpec 的情况下新增业务能力。
- 禁止把 Docker 环境变量硬编码到代码中。
- 禁止用临时目录替代正式目录结构。
