---
purpose: 文档表达卫生与过程残留审计标准
content: 约束长期文档避免会话推理、临时草稿、review 对话、不可解析路径和敏感片段
source: /spec-study apply TilesFST upgrade-governance 文档卫生 最小相关验证矩阵
update_method: 文档治理、spec-logs、技能输出或审计脚本变化时更新
created_at: 2026-08-21 22:28:02
updated_at: 2026-08-21 22:28:02
---

# 文档表达卫生与过程残留审计标准

## 1. 目标

长期文档必须站在仓库当前事实视角描述规则、边界和验证方式，不写会话推理、临时草稿、review 对话或无法在仓库中解析的内部引用。

## 2. 禁止进入长期文档的内容

| 类型 | 说明 | 处理方式 |
|---|---|---|
| 会话推理残留 | “我先…然后…所以…”等只属于执行过程的叙述 | 删除推理过程，保留可验证结论 |
| 临时草稿引用 | `设计稿第 N 版`、`audit C2`、`草案 §4` 等未提交事实源 | 改为仓库相对路径或删除引用 |
| review 对话 | “reviewer 要求…”、“已按评论修改…” | 写成当前规则或移入治理日志 |
| 历史叙事 | “之前/现在/不再/本次新增”等非必要变化故事 | 写成当前行为；必要历史放 spec-log |
| 不可解析路径 | 本机绝对路径、会话路径、截图个人信息路径 | 使用仓库相对路径或脱敏占位符 |
| 敏感片段 | 密钥、Token、连接串、Cookie、Authorization header、真实客户数据 | 立即移除并改用安全摘要 |

## 3. 允许保留的内容

- OpenSpec Change、Issue、Sprint、release、spec-log 等仓库内可解析事实源引用。
- BUG、事故、复盘中的必要证据摘要，前提是脱敏且可定位。
- 当前规则的理由摘要，尤其是会影响后续实现、验证或归档判断的取舍。
- 明确的 TODO / FIXME / follow-up 命令，且有 owner 或来源对象。

## 4. 审计方法

优先运行轻量脚本：

```bash
python scripts/validate-doc-prose-hygiene.py
```

聚焦路径：

```bash
python scripts/validate-doc-prose-hygiene.py docs/standards rules AGENTS.md
```

脚本只提供启发式发现项，不自动删除内容。处理前必须判断该内容是否承载真实事实、验收证据、合规说明或必要历史。
