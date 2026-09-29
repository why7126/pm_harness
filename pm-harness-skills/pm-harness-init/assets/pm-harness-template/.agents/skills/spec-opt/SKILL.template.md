---
name: spec-opt
description: 规范优化 - 新增或修改项目治理规范、技能命令、文档索引与治理脚本
---

# spec-opt

Use this skill when the user asks to run `/spec-opt ...` or requests optimization of project governance specifications, including `.agents/skills` commands, `rules/`, `docs/`, and governance scripts.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`。
- 已在同一会话读取过且无变更的规则和 Skill 文件，用摘要承接或摘要复用，不重复全量读取。
- 先用 `rg -l`、`rg --files`、`git diff --stat`、`git diff --name-only` 或 OpenSpec CLI `contextFiles` 定位，再分段读取必要片段。
- 禁止默认宽泛读取 `cat rules/*.md`、`cat docs/**`、`cat issues/**`、`cat iterations/**` 或 `ls -R`。
- 默认排除 generated、node_modules、coverage、dist、archive 大目录。
- 命令输出优先 `max_output_tokens <= 8000`；成功路径只报告摘要、影响范围、校验结果和下一步。

## Input

- `/spec-opt <自然语言治理优化目标>`：新增或修改命令、规则、文档规范、治理脚本。
- `/spec-opt update-command <command> <目标>`：新增或调整 `.agents/skills/<command>/SKILL.md`。
- `/spec-opt update-rules <目标>`：新增或调整 `rules/` 规范。
- `/spec-opt update-docs <目标>`：新增或调整 `docs/` 索引、standards 或长期治理文档。
- `/spec-opt update-script <script> <目标>`：新增或调整 `scripts/` 下治理脚本。
- 可接受明确的 `<change-id>`；未提供时，创建或复用与本次治理优化匹配的 OpenSpec Change。

## Scope

`/spec-opt` 是可落盘的项目治理规范优化命令，不是只读探索命令。

允许修改：

- `.agents/skills/<command>/SKILL.md`
- `AGENTS.md`
- `rules/*.md`
- `docs/**/*.md`
- `scripts/` 下治理脚本、校验脚本和脚本说明
- 当前 active OpenSpec Change 下的 proposal、design、tasks、delta spec、trace、acceptance、test-plan

禁止修改：

- `src/` 下业务运行时代码
- 后端 API、数据库 schema、Web、小程序、管理端业务实现
- `openspec/specs/` 正式规格（归档命令除外）
- `.env`、真实密钥、真实客户数据、运行时数据库文件或构建产物

若用户请求包含业务实现或产品行为变更，MUST 停止业务实现部分，并引导改用 `/capture`、`/req-*`、`/bug-*`、`/opsx-propose` 或对应业务流程。

## OpenSpec Change Rules

- 新增命令、治理扩展、目录边界变化或脚本校验行为变化 MUST 有 OpenSpec Change。
- `/spec-opt` MAY 直接创建或复用 OpenSpec Change，但 MUST 通过 OpenSpec CLI 创建 active Change。
- 不得绕过 active Change 直接修改 `openspec/specs/`。
- 若仅为文档错别字、链接修复或非行为性小修，可说明豁免原因；否则按 Change 流程执行。
- 纯治理 Change 无 REQ/BUG 来源时，仍 MUST 先纳入某个 Sprint 的 `changes[]` 后才能 `/opsx-apply`；不得因“不关联 REQ/BUG”或“未触碰业务 src”豁免 Sprint Inclusion Gate。
- 当项目无 active Sprint 且 `/spec-opt` 需要为纯治理 Change 创建 Sprint 时，MUST 按现有 `iterations/archive/` 与 `iterations/change/` 中的 `sprint-[0-9]{3}` 最大编号自动递增；不得用日期、主题或混合格式命名 Sprint。

## Documentation Sync Matrix（MUST）

| 变更类型 | 必须同步 |
|---|---|
| 新增/修改命令 | `.agents/skills/<command>/SKILL.md`、`AGENTS.md` 命令入口和速查、`rules/agent-context-budget.md`、相关 OpenSpec Change |
| 新增/修改文档规范 | `rules/*.md`、`docs/README.md` 或相关 `docs/standards/*.md`、`rules/document-governance.md`（按需）、`AGENTS.md` 读取路由或红线（按需） |
| 新增/修改脚本 | `scripts/<name>`、脚本帮助文本或 README、相关规则、相关 Skill 引用、最小验证或测试 |
| 命令输出契约调整 | 受影响 `.agents/skills/*/SKILL.md`、`AGENTS.md`、`rules/agent-context-budget.md`、`scripts/validate-agent-context-budget.py` |
| 目录边界调整 | `AGENTS.md`、`rules/directory-structure.md`、目录校验脚本、相关 docs 索引 |
| 下一步命令参数规范调整 | 受影响 Skill、`AGENTS.md`、`rules/requirement-management.md`、`rules/bug-management.md`、`rules/agent-context-budget.md`、`docs/README.md`、校验脚本 |

同步文档时 MUST 更新 Markdown frontmatter `updated_at`，不得修改既有 `created_at`。

## Spec Logs（MUST）

`/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代后，MUST 在 `docs/spec-logs/` 写入治理迭代日志；不得把实际项目日志写入脚手架模板目录。

命名规则：

```text
YYYYMMDDhhmmss-governance-xxx.md
```

- `YYYYMMDDhhmmss` MUST 使用日志生成时刻的 `Asia/Shanghai` 日期时间，精确到秒。
- `governance` 用于区分本项目规范工程迭代日志，与 `/spec-study` 生成的 `YYYYMMDDhhmmss-study-xxx.md` 学习报告区分。
- `xxx` MUST 使用小写 kebab-case 表达治理主题，例如 `skill-output-contract`、`api-governance-rules`、`spec-logs`。

治理迭代日志 MUST 包含：迭代目标、变更摘要、影响范围、更新文件、验证结果、API/DB/Web/小程序/管理端/Orval/Docker 影响和后续建议。

治理迭代日志 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码。涉及隐私风险时，只能使用脱敏占位符或聚合描述。

## Implementation Loop

1. 识别治理优化目标和禁止业务实现的边界。
2. 查找或创建 OpenSpec Change；读取 `openspec instructions apply --json` 返回的 `contextFiles`。
3. 判断影响范围：skills / rules / docs / scripts / AGENTS / OpenSpec。
4. 按文档同步矩阵做最小范围修改。
5. 修改脚本时补充或运行脚本级最小验证。
6. 写入或更新 `docs/spec-logs/YYYYMMDDhhmmss-governance-xxx.md` 治理迭代日志。
7. 每完成一组 task，立即把 `tasks.md` 对应 `- [ ]` 标记为 `- [x]`。
8. 使用聚焦 diff 复核没有修改 `src/` 业务代码。

## Validation（MUST）

完成前按影响范围运行：

```bash
python scripts/validate-agent-context-budget.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
openspec validate <change-id>
```

如修改脚本，MUST 至少运行被修改脚本本身或对应测试；如仅修改 Markdown 规范，可说明业务测试不适用。

## Final Step — Workflow Sync

若 `/spec-opt` 通过 `/opsx-apply` 落地 active Change，完成前运行：

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- 对无 REQ/BUG 来源的纯治理 Change，Sprint skipped/unresolved MUST 视为阻塞；必须先通过 `/sprint-propose` 或 `scripts/add-sprint-scope-item.py --sprint <sprint-id> --change <change-id> --rationale "<why this governance change is in scope>"` 纳入 Sprint。
- 若 Change 关联 REQ/BUG，MUST 遵守 `/opsx-apply` 的 Sprint Inclusion Gate。

随后运行 AI Usage Post-command Hook；MUST 使用 Workflow Sync 解析到的 Sprint，不得传入 `auto` 或虚构 Sprint。

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
