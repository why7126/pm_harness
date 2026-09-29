---
name: "spec-study"
description: "跨项目 Harness 学习应用 - 学习其他项目治理工程，并经用户确认后应用到本项目治理资产"
created_at: 2026-08-07 09:06:21
updated_at: 2026-08-07 10:41:52
---

# spec-study

Use this skill when the user asks to run `/spec-study ...`, or asks to learn another project's Harness / OpenSpec / Agent governance setup and apply selected learnings to this project.

`/spec-study` 是两阶段治理学习命令：先学习并提出候选内容，再等待用户确认；确认后才更新本项目治理资产。它不是复制目录命令，也不是业务开发命令；它对学习对象永远只读，绝不允许改动学习对象的任何代码、文档、配置或仓库状态。

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 检索先定位再分段读取；对学习对象先输出文件清单和命中摘要，再按主题读取必要片段。
- 大范围 `rg/find` 默认排除 generated、node_modules、dist、coverage、archive、运行时数据和构建产物；只有学习 Harness/Agent 目录时 MAY 放开 `.agents/`、`.cursor/`、`.codex/`、`.kiro/`、`.opencode/`、`.claude/` 等目录排除。
- 命令输出优先 `max_output_tokens <= 8000`；长文档、长脚本、大 diff、Workflow Sync 输出先给摘要、命中数或关键片段。
- MUST NOT 把学习对象的长脚本、长规范、模板资产全文复制进最终回复或技能文件；应用时应改写为适配本项目的简洁规则、脚本或引用。
- MUST NOT 对学习对象运行任何写入、格式化、安装、生成、迁移、测试修复、提交、分支、清理或重置命令；不得在学习对象路径下使用会产生文件变更的脚本或工具。

## Input

- `/spec-study <学习对象>`：默认自动学习。
- `/spec-study <学习对象> --mode auto`：自动学习 Harness 工程。
- `/spec-study <学习对象> --focus <内容>`：指定学习内容，例如 `技能`、`UI设计系统`、`API治理`、`测试治理`、`部署治理`、`文档索引`。
- `/spec-study apply <学习报告或候选项>`：用户确认后应用指定学习内容。

学习对象可以是本地项目路径或 GitHub 项目 URL。

## Scope

允许在应用阶段修改：

- `.agents/skills/<command>/SKILL.md`
- `AGENTS.md`
- `rules/*.md`
- `docs/**/*.md`
- `scripts/` 下治理脚本、校验脚本和脚本说明
- `deploy/`、`docker-compose*.yml`、`.env.example` 中的治理说明或示例边界
- 当前 active OpenSpec Change 下的 proposal、design、tasks、delta spec、trace、acceptance、test-plan
- `iterations/change|archive/<sprint>/` 中与本次治理同步相关的 Sprint 四件套

禁止修改：

- 学习对象中的任何文件、目录、Git 状态、依赖锁文件、缓存、生成物或运行时数据
- `src/` 下任何业务运行时代码
- 后端 API、数据库 schema、Web、小程序、管理端业务实现
- `openspec/specs/` 正式规格（归档命令除外）
- `.env`、真实密钥、真实客户数据、运行时数据库文件、依赖目录、构建产物

如果候选学习内容需要修改业务实现，MUST 停止业务实现部分，并引导改用 `/capture`、`/req-*`、`/bug-*`、`/opsx-propose` 或对应业务流程。

## Learning Matrix（MUST）

学习任何主题时，都 MUST 横向检查相关模块，避免只看单一目录：

| 模块 | 重点 |
|---|---|
| 项目入口 | `AGENTS.md`、`project.yaml`、`DOCUMENT_METADATA_INDEX.md` |
| 全局规范 | `rules/`、`docs/`、`docs/standards/`、`docs/knowledge-base/` |
| Agent 能力 | `.agents/`、`.cursor/`、`.codex/`、`.kiro/`、`.opencode/`、`.claude/` 等 |
| 脚本 | `scripts/` 下治理、校验、同步、生成脚本 |
| 部署 | `docker-compose*.yml`、`.env.example`、`deploy/` |

本项目当前唯一 AI 工具入口是 `.agents/skills/`。学习对象中即使存在 `.cursor/`、`.codex/`、`.kiro/`、`.opencode/`、`.claude/`，应用到本项目时也 MUST 优先转写为 `.agents/skills/`、`rules/`、`docs/` 或 `scripts/`；不得直接恢复这些目录，除非先通过 OpenSpec Change 更新目录边界、校验脚本和 `AGENTS.md`。

## Phase 1 — 学习与候选清单

1. 解析学习对象和学习模式；未指定模式时使用 `auto`。
2. 本地路径必须先确认存在并只读扫描；GitHub URL 必须先说明需要远端只读快照，如需网络或 clone，按当前权限策略请求批准。
   - 学习对象 MUST 被视为外部只读输入，禁止在该路径内写入文件、安装依赖、运行格式化、执行迁移、修复测试、修改 Git 状态或清理目录。
   - 如需临时克隆 GitHub 项目，只能克隆到受控临时目录并作为只读快照读取；不得 push、commit、checkout 覆盖、reset、clean 或修改远端仓库。
3. 用 `find -maxdepth`、`rg --files` 或等价方式列出候选治理文件，默认排除依赖、构建产物、运行时数据和历史归档。
4. 如果学习对象存在 `docs/spec-logs/CHANGELOG.md`，MUST 先读该日志索引，再读取相关单次 `study` / `governance` 日志；日志只作为入口地图和历史背景，不能替代当前资产事实源。
5. 按 Learning Matrix 横向校验当前真实治理资产，必要时读取脚本或配置片段，并记录来源路径、主题、可迁移价值、适配成本和风险。
6. 输出候选学习内容，必须包含学习对象与模式、已学习模块摘要、建议应用项、不建议应用项和等待用户确认的选项。

Phase 1 默认 MUST NOT 修改本项目文件；除非用户在同一命令中明确授权“学习并应用全部建议”。

## Phase 2 — 用户确认后应用

1. 确认用户选择的学习项和应用范围。
2. 若变更属于新增命令、治理扩展、目录边界、脚本校验行为变化，MUST 有 active OpenSpec Change，并且该 Change MUST 已纳入 Sprint scope。
3. 按本项目现有规范重写学习内容，不做原样大段复制。
4. 更新必要的 `.agents/skills/`、`AGENTS.md`、`rules/`、`docs/`、`scripts/`、部署治理文件和 active Change 文档。
5. 每完成一组 active Change task，立即把 `tasks.md` 对应 `- [ ]` 标记为 `- [x]`。
6. 使用聚焦 diff 复核没有修改 `src/`。
7. 使用学习对象的 `git status --short`、文件清单对比或等价方式复核学习对象未发生变更；若学习对象不是 Git 仓库，MUST 说明采用了只读命令且未对其路径执行写入操作。
8. 输出学习报告。报告 MUST 统一写入 `docs/spec-logs/`，文件名 MUST 使用 `YYYYMMDDhhmmss-study-xxx.md` 格式，例如 `20260807103045-study-design-system.md`；同一次学习应用流程只生成一份正式 `study` 报告，不得同时生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md` 治理日志；若同一流程已有报告，MUST 更新该报告。不得写入脚手架模板目录、active Change 的 `implementation/` 或 `docs/knowledge-base/` 作为正式学习报告位置。

## Learning Report（MUST）

应用完成后的学习报告 MUST 包含：

- 学习对象、学习模式、执行时间。
- 学习到的治理能力。
- 已采纳内容和采纳原因。
- 未采纳内容和未采纳原因。
- 更新文件清单和每个文件的修改原因。
- API、数据库、Web、小程序、管理端、Orval、Docker Compose、测试影响。
- 校验命令和结果。
- 学习对象只读保护结果。
- 后续建议。

学习报告落盘规则：

- 目录：`docs/spec-logs/`
- 文件名：`YYYYMMDDhhmmss-study-xxx.md`
- `YYYYMMDDhhmmss` MUST 使用报告生成时刻的 `Asia/Shanghai` 日期时间，精确到秒。
- `study` 用于区分跨项目学习报告，与 `/spec-opt` 生成的 `YYYYMMDDhhmmss-governance-xxx.md` 治理迭代日志区分。
- `xxx` MUST 使用小写 kebab-case，表达学习对象或主题，例如 `pm-harness`、`design-system`、`api-governance`。
- Markdown Frontmatter MUST 包含 `created_at` 与 `updated_at`，时间格式遵守 `rules/document-governance.md`。
- 学习报告 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、本机绝对路径、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码；涉及隐私风险或本地路径时，只能使用仓库相对路径、脱敏占位符或聚合描述，例如 `<local-project>/rules/global.md`、`rules/global.md`、`<user-home>`。
- 同一次学习应用流程 MUST 只生成一份正式 `study` 报告。学习阶段候选内容 SHOULD 保留在最终回复、active Change 文档或同一报告的阶段章节中，不得另起第二份 `YYYYMMDDhhmmss-study-xxx.md`。
- `/spec-study` 触发的治理资产应用结果 MUST 汇总到同一份 `study` 报告，不得再额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`。若同一学习对象、学习主题和用户确认批次已存在本流程报告，后续应用结果、验证结果或修正 MUST 更新同一文件。

## Validation（MUST）

完成应用阶段前按影响范围运行：

```bash
python scripts/validate-agent-context-budget.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
openspec validate <change-id>
```

如修改脚本，MUST 至少运行被修改脚本本身或对应测试；如仅修改 Markdown 规范，可说明业务测试不适用。

## Final Step — Workflow Sync

若 `/spec-study apply` 通过 active Change 落地治理变更，完成前运行：

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- 对无 REQ/BUG 来源的纯治理 Change，Sprint skipped/unresolved MUST 视为阻塞；必须先通过 `/sprint-propose` 或 `scripts/add-sprint-scope-item.py --sprint <sprint-id> --change <change-id> --rationale "<why this governance change is in scope>"` 纳入 Sprint。
- Workflow Sync 成功后运行 AI Usage Post-command Hook；MUST 使用 Workflow Sync 解析到的 Sprint，不得传入 `auto` 或虚构 Sprint。

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
