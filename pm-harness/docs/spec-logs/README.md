---
created_at: 2026-08-07 15:10:22
updated_at: 2026-08-07 15:10:22
---

# 规范工程日志

`docs/spec-logs/` 用于存放规范工程日志，包括 `/spec-study` 学习其他项目 Harness 工程后生成的学习报告，以及 `/spec-opt` 对本项目规范、技能、脚本、目录边界和校验规则的迭代更新日志。

## 命名规则

文件名 MUST 使用：

```text
YYYYMMDDhhmmss-study-xxx.md
YYYYMMDDhhmmss-governance-xxx.md
```

- `YYYYMMDDhhmmss`：报告生成时刻的 `Asia/Shanghai` 日期时间，精确到秒。
- `study`：`/spec-study` 跨项目学习报告。
- `governance`：`/spec-opt` 本项目规范、技能、脚本或校验规则迭代日志。
- `xxx`：小写 kebab-case 主题，例如 `pm-harness`、`design-system`、`api-governance`、`spec-logs`。

## 去重规则

- 同一次 `/spec-study` 学习应用流程只生成一份正式 `study` 报告。
- 学习阶段候选内容不得另行落盘为第二份正式 `study` 报告；可保留在最终回复、active Change 文档或同一报告的阶段章节中。
- `/spec-study` 触发的治理资产应用结果必须汇总到同一份 `study` 报告，不得再额外生成内容重复的 `governance` 日志。
- 若同一学习对象、学习主题和用户确认批次已存在本流程报告，后续应用结果、验证结果或修正 MUST 更新同一文件。
- `/spec-opt` 每次独立治理变更 MAY 生成一份 `governance` 日志；同一治理变更的补充修正 SHOULD 更新同一日志。

## 边界

- 本目录只承载 `/spec-study` 学习报告和 `/spec-opt` 治理迭代日志。
- 不存放需求、BUG、Sprint 四件套或 OpenSpec Change 事实源。
- 不存放学习对象源码、密钥、真实客户数据、用户隐私数据、本机绝对路径、运行时数据库、依赖目录或构建产物。
- 不得记录可识别个人或客户主体的信息，包括但不限于姓名、手机号、邮箱、地址、证件号、账号 ID、访问令牌、订单原文、聊天原文、工单原文、截图中的个人信息和未脱敏日志。
- 如确需说明隐私相关风险或本地路径，MUST 使用脱敏占位符、仓库相对路径或聚合描述，例如 `<user-email>`、`<customer-id>`、`<local-project>/rules/global.md`、`rules/global.md`、`某类用户标识`，不得写入原始值或本机绝对路径。
