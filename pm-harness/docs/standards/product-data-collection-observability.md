---
purpose: 通用产品数据采集与链路观测规范
content: 行为事件、API 请求日志、任务链路、流程节点、保留周期、脱敏边界和新产品接入清单
source: /spec-study apply TilesFST product-data-collection-observability-standard
update_method: 数据采集、链路观测、日志审计、Task Trace 或保留周期规范变化时同步更新
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# 通用产品数据采集与链路观测规范

## 1. 目标

本规范用于指导新产品、新端和新模块从设计阶段接入产品数据采集与链路观测能力，确保用户行为、后端请求、任务链路和流程节点具备统一事实源、字段语义、脱敏边界和验收口径。

覆盖范围：

| 层 | 覆盖要求 |
|---|---|
| Web / 管理端 | 采集页面访问、业务点击、表单提交、查询筛选和请求链路透传。 |
| 小程序 / App | 采集页面、组件曝光、点击、搜索、收藏、分享和业务 API 请求链路。 |
| 后端 API | 业务 API 默认记录请求日志；任务类请求按分级策略记录任务链路和流程节点。 |
| DB / 日志审计 | 明确表结构、索引、保留周期、脱敏和查询路径。 |

如某产品、端或模块确实不适用其中某一层采集，需求、设计或 Change 验收必须记录 N/A 原因。

## 2. 四层链路模型

```text
usage_events
  -> request_logs
      -> task_traces
          -> task_trace_spans
```

| 层级 | 事实源 | 说明 |
|---|---|---|
| 行为事件 | `usage_events` | 记录页面访问、业务点击、搜索筛选、表单提交、保存、删除、上传、分享、收藏等可命名业务行为。 |
| 请求日志 | `request_logs` | 记录后端业务 API 请求摘要和服务端可信 `request_id`。 |
| 任务链路 | `task_traces` | 记录长耗时、多步骤、批量、异步、外部依赖或高风险操作的总体追踪。 |
| 流程节点 | `task_trace_spans` | 记录任务内部关键阶段；面向中文产品、管理端和验收表达统一称为“流程节点”。 |

## 3. 两类入口

界面触发入口：

```text
用户访问页面 / 点击业务按钮 / 搜索筛选 / 保存上传
  -> 客户端生成 behavior_trace_id
  -> 客户端生成 behavior_event_id
  -> 上报 usage_events
  -> 行为触发 API 请求携带 behavior_trace_id / behavior_event_id
  -> 后端 request_logs 保存 behavior_trace_id / parent_behavior_event_id
  -> 任务类请求进入 task_traces / task_trace_spans
```

直接 API 调用入口：

```text
外部系统 / 脚本 / API 客户端 / 后台服务调用业务 API
  -> 不伪造 usage_events
  -> request_logs 记录服务端 request_id
  -> behavior_trace_id 允许为空
  -> 任务类请求从 request_id 进入任务链路
```

## 4. 字段语义与可信边界

| 字段 | 生成方 | 语义 | 可信边界 |
|---|---|---|---|
| `behavior_trace_id` | 客户端 helper / SDK | 一次用户行为链路，可关联同一行为触发的一个或多个 API 请求。 | 客户端字段，仅用于链路归因和排障；不得作为认证、授权、审计身份或租户隔离依据。 |
| `behavior_event_id` | 客户端 helper / SDK | 单条行为事件 ID。 | 客户端字段，必须校验长度、字符集和格式。 |
| `parent_behavior_event_id` | 后端从请求头或上下文提取 | 请求来源行为事件 ID。 | 仅用于回指行为事件；缺失时允许为空。 |
| `request_id` | 后端 | 服务端可信单次 HTTP 请求 ID。 | 可信请求日志主追踪 ID；客户端传入值不得覆盖。 |
| `client_request_id` | 客户端 | 客户端侧请求标识，用于跨端排障辅助。 | 不得作为认证、授权、审计身份或租户隔离依据。 |
| `task_trace_id` | 后端 Task Trace helper | 任务链路 ID，串联任务摘要和流程节点。 | 后端生成或由后端校验后接受；不得信任未校验客户端值。 |

所有客户端传入链路字段必须做长度、字符集和格式校验。非法、超长或含敏感值的字段应被忽略或返回文档化错误。

## 5. 标准数据结构

具体产品可以扩展字段，但不得改变字段语义、关联关系、脱敏边界和保留周期。

| 事实源 | 最小标准字段 |
|---|---|
| `usage_events` | `id`、`behavior_trace_id`、`behavior_event_id`、`event_name`、`event_category`、`client_type`、`page_path`、`page_code`、`session_id`、`actor_user_id`、`actor_role`、`properties`、`result`、`created_at` |
| `request_logs` | `id`、`request_id`、`behavior_trace_id`、`parent_behavior_event_id`、`client_request_id`、`method`、`path`、`route_template`、`status_code`、`result`、`duration_ms`、`client_type`、`actor_user_id`、`actor_role`、`resource_type`、`resource_id`、`metadata`、`created_at` |
| `task_traces` | `id`、`task_trace_id`、`parent_request_id`、`task_type`、`task_name`、`status`、`started_at`、`finished_at`、`duration_ms`、`actor_user_id`、`client_type`、`metadata`、`error_code`、`error_message`、`created_at` |
| `task_trace_spans` | `id`、`task_trace_id`、`span_id`、`parent_span_id`、`span_name`、`node_label`、`sequence`、`status`、`started_at`、`finished_at`、`duration_ms`、`metadata`、`error_code`、`error_message`、`created_at` |

建议索引应覆盖链路 ID、事件 / 路由模板、状态、操作者和时间维度。物理类型、分区、归档表和索引名称由产品对应 schema、迁移和数据库设计文档落地。

## 6. 可空与关联规则

| 场景 | 必须满足 |
|---|---|
| 界面触发 API | `usage_events.behavior_trace_id` 与 `request_logs.behavior_trace_id` 保持一致；能识别来源事件时，`request_logs.parent_behavior_event_id` 等于 `usage_events.behavior_event_id`。 |
| 一次行为触发多个 API | 多条 `request_logs` 共享同一个 `behavior_trace_id`，并可共享同一个 `parent_behavior_event_id`。 |
| 直接 API 调用 | 不伪造 `usage_events`；`request_logs.behavior_trace_id` 和 `request_logs.parent_behavior_event_id` 允许为空。 |
| 任务类请求 | `task_traces.parent_request_id` 优先记录来源 `request_logs.request_id`。 |
| 后台定时任务 | 若无来源 HTTP 请求，`task_traces.parent_request_id` 允许为空，但必须保留 `task_trace_id`、`task_type`、`task_name` 和节点信息。 |
| 流程节点 | `task_trace_spans.task_trace_id` 必须指向 `task_traces.task_trace_id`；复杂任务可使用 `parent_span_id` 表达嵌套节点。 |

## 7. 采集覆盖策略

行为事件应采集页面、查询、表单、媒体和互动类可命名业务行为。纯视觉 hover、tooltip 关闭、无业务含义布局点击、重复无状态点击等 UI 噪音可排除。

所有业务 API 请求必须记录 `request_logs`。健康检查、静态资源、OpenAPI / Swagger / Redoc 文档资源、预检 OPTIONS 和内部探活可排除，排除项必须写入规范或产品实现文档。请求日志写入失败必须降级处理，不得阻断主业务响应。

Task Trace 按分级覆盖。满足长耗时、多步骤、批量 / 异步、外部依赖、失败需定位节点或高风险写操作任一条件的接口或任务必须接入 `task_traces` 和 `task_trace_spans`。普通简单写操作可以只保留 `request_logs`，但需求、设计或实现文档必须说明不接入 Task Trace 的理由。

## 8. 数据保留周期

| 数据 | 默认周期 | 处理方式 |
|---|---:|---|
| `request_logs` 明细 | 90 天 | 超期删除或匿名化。 |
| `usage_events` 明细 | 180 天 | 超期删除或匿名化。 |
| `task_traces` / `task_trace_spans` 明细 | 90 天 | 超期删除或匿名化。 |
| 聚合数据 | 1 年 | 可用于长期趋势分析。 |

调整保留周期时，必须记录调整原因、影响范围、审批依据、明细数据与聚合数据差异，以及对存储成本、排障窗口、隐私和合规的影响。

## 9. 安全与脱敏

禁止采集或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO AccessKey / SecretKey、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 或真实客户敏感数据。

前端脱敏只能作为展示优化。后端在持久化前执行敏感字段过滤、长度截断和安全 JSON 序列化，才是安全边界。采集字段不得放宽管理端、小程序、App 或后端 API 的权限边界。

## 10. 新产品接入清单

| 项 | 要求 |
|---|---|
| 行为事件字典 | 定义事件名、分类、必填属性、可选属性、禁止属性和 N/A 项。 |
| 前端 helper / SDK | 统一生成 `behavior_trace_id`、`behavior_event_id`，并在行为触发请求中透传。 |
| 后端 request log middleware | 统一生成 `request_id`，记录请求摘要、耗时、状态、客户端和脱敏 metadata。 |
| Task Trace helper | 通过封装写 `task_traces` 和 `task_trace_spans`，避免路由层直接拼 SQL。 |
| 标准数据结构 | 对照四类事实源最小标准字段，记录产品扩展字段、N/A 项和索引取舍。 |
| 直接 API 兼容 | `behavior_trace_id` 可空，不伪造 `usage_events`，从 `request_id` 进入任务链路。 |
| 脱敏 helper | 后端统一过滤敏感字段、截断长字段、安全序列化 JSON。 |
| DB / migration | 字段和索引变化同步 schema、迁移、数据库设计文档和测试。 |
| API / Orval | 请求头、查询参数、响应字段或错误码变化同步 OpenAPI、Orval、API 文档和前后端测试。 |
| 保留周期 | 记录默认周期、超期删除或匿名化方式、周期调整审批依据。 |
| 验收 | 覆盖行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期和旧数据兼容。 |

## 11. 后续 Change 引用规则

以下类型需求、BUG 或 Change 应引用本规范：观测类、日志审计类、行为埋点类、上传 / 导入导出 / 批量处理类、跨端请求封装类、Task Trace 或流程节点扩展类。

引用时必须说明：

- 哪些层级适用。
- 是否遵守标准数据结构最小字段、可空规则和索引建议。
- 哪些层级 N/A 及原因。
- 是否影响 API、DB、OpenAPI、Orval、Web、小程序、App 或测试。
- 是否需要新增或修改保留周期。
- 是否涉及敏感字段和脱敏验证。

## 12. 适用性声明格式

触发范围内的需求、BUG、Change 或 Sprint 摘要必须记录：

```yaml
product_data_collection_observability:
  status: applicable | not_applicable
  affected_layers:
    - api
    - database
    - request_logs
    - usage_events
    - task_trace
    - web_request_wrapper
    - miniapp_request_wrapper
    - app_request_wrapper
    - workflow_governance
  reason: <说明适用原因或可审计 N/A 原因>
  validation: <验证计划、验收摘要或 N/A 依据>
```

N/A 原因不得只写“无”“不涉及”“none”或等价空泛说明。

## 13. 验证命令

```bash
python scripts/validate-product-data-observability-standard.py
python scripts/validate-product-data-observability-gates.py --change <change-id>
```
