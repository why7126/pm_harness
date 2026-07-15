---
purpose: 产品总览
content: 产品定位、目标用户、核心场景、能力边界和文档导航
source: Harness docs Token 优化模板，初始化时基于用户输入生成
update_method: 产品定位、目标用户、产品形态、核心能力或范围边界变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 适用于 {PRODUCT_NAME} 项目
---

# 产品总览

## 1. 产品目标

`{PRODUCT_NAME}` 面向 `{TARGET_USERS}`，用于解决 `{BUSINESS_PROBLEM}`。

产品定位：

```text
{PRODUCT_DESCRIPTION}
```

产品形态：

```text
{PRODUCT_FORMS}
```

## 2. 核心场景

| 场景 | 用户 | 目标 | 状态 |
|---|---|---|---|
| `{SCENARIO_1}` | `{USER_1}` | `{GOAL_1}` | 待确认 |
| `{SCENARIO_2}` | `{USER_2}` | `{GOAL_2}` | 待确认 |
| `{SCENARIO_3}` | `{USER_3}` | `{GOAL_3}` | 待确认 |

## 3. 核心能力

```text
{CORE_CAPABILITIES}
```

能力详情以 `openspec/specs/` 为事实源；待开发能力以 `openspec/changes/`、`issues/` 和 `iterations/` 为事实源。

## 4. 范围边界

| 类型 | 内容 |
|---|---|
| 当前范围 | `{IN_SCOPE}` |
| 暂不包含 | `{OUT_OF_SCOPE}` |
| 依赖条件 | `{DEPENDENCIES}` |
| 人工确认项 | `{CONFIRMATION_REQUIRED}` |

## 5. 文档导航

完整索引见 [docs/README.md](README.md)。主文档按 `00`-`08` 阅读；API、测试、认证、上传等治理细则见 [docs/standards/](standards/)。
