---
name: "explore"
description: "通用探索模式 - 面向问题、需求或话题的只读分析与方案探讨，不改代码、不落盘"
created_at: 2026-08-06 00:00:00
updated_at: 2026-08-06 00:00:00
---

# explore

Use this skill when the user asks to run the workflow command `explore`, or wants to discuss an open-ended problem, requirement, idea, or topic before creating REQ / BUG / OpenSpec artifacts.

`/explore` 是通用探索入口，应用功能与 `/bug-explore`、`/req-explore`、`/opsx-explore` 相似，但不要求用户已拥有 BUG、REQ 或 Change ID。它负责把用户抛出的内容先分流为「问题 / 需求 / 话题 / 混合」，再提供根因分析、需求评估、方案设计或观点论证。

**默认：不写任何文件、不写代码、不改 `src/`、不改 `issues/`、不改 `openspec/`、不改 `iterations/`。**

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 检索先用 `rg -l` / `rg --files` 定位文件，再用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 读取必要片段。
- 大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。
- 不为探索目的读取整目录；只读取与当前问题、需求、话题直接相关的文档、代码、配置或 Change 片段。

## Command Template

**Input**：自然语言问题、需求、想法、话题；也可以包含 `REQ-xxxx`、`BUG-xxxx`、`sprint-xxx`、`openspec/changes/<change-id>` 或文件路径。

**默认行为**：

- 只读分析、搜索、定位、比较和讨论。
- 若用户输入已经明显属于某个专门命令，优先沿用该命令的思路：
  - BUG 或故障：对标 `/bug-explore`
  - 需求或产品想法：对标 `/req-explore`
  - OpenSpec Change 或技术变更：对标 `/opsx-explore`
  - Sprint 范围、排期、依赖：对标 `/sprint-explore`
- 若用户要求实现、修复、生成正式文档或创建 Change，提醒必须退出 explore，并按 `/capture`、`/req-*`、`/bug-*`、`/opsx-*` 或 `/sprint-*` 流程执行。

## Stance

- **好奇但有判断**：先理解语境，再给清晰结论；不把探索变成机械问卷。
- **证据优先**：涉及项目事实时，读取现有代码、文档、配置或 OpenSpec 片段作为依据。
- **多方案思维**：需求和设计问题优先给多个可行方案，再比较取舍。
- **明确决策点**：凡需要用户选择范围、优先级、成本、风险或路线时，必须显式列出。
- **可视化**：适合时使用 ASCII 图、流程图、依赖图、对比表帮助澄清。
- **不越界**：探索不是实现，不自动落盘，不假装已经修复。

## 输入分流

### 1. 问题 / 故障 / 异常

适用：用户描述「为什么」「报错」「不生效」「表现异常」「体验不对」「可能有 bug」。

输出 SHOULD 包含：

- 问题复述：用一句话确认理解。
- 现象与影响：影响范围、触发条件、严重程度倾向。
- 根因判断：区分已确认根因、强推测、待验证假设。
- 证据依据：引用只读调查到的代码、文档、配置、日志或用户描述。
- 解决方案：给出至少一个可执行修复路线；复杂问题可拆临时 workaround 与正式 fix。
- 验证建议：建议如何复现、如何验证修复、是否需要回归测试。
- 后续流程：若确认是 BUG，建议 `/bug-capture` 或 `/capture`；不得自动创建，除非用户明确授权。

### 2. 需求 / 产品想法 / 改进建议

适用：用户描述「想做」「能不能加」「是否合理」「怎么设计」「要不要支持」。

输出 SHOULD 包含：

- 需求理解：目标用户、场景、要解决的问题。
- 合理性评估：价值、频率、边界、与现有产品定位的一致性。
- 评估依据：用户价值、业务价值、实现成本、维护成本、风险、现有系统约束。
- 范围建议：In / Out、MVP 与后续增强。
- 设计方案：给出一个或多个方案；多个方案 MUST 提供对比表。
- 推荐方案：说明推荐理由、适用前提和放弃其他方案的原因。
- 决策点：明确需要用户决定的范围、优先级、体验、数据、权限、上线节奏等。
- 后续流程：若值得正式推进，建议 `/req-capture` 或 `/opsx-propose`；不得自动创建，除非用户明确授权。

### 3. 技术设计 / 架构取舍

适用：用户比较技术路线、模块边界、接口设计、数据模型、部署策略或实现方式。

输出 SHOULD 包含：

- 现状地图：当前相关模块、依赖、接口、数据流或文档约束。
- 约束条件：OpenSpec、API、DB、权限、安全、部署、测试、Orval、设计系统等影响。
- 候选方案：至少覆盖保守方案与演进方案；必要时给长期方案。
- 对比维度：复杂度、风险、迁移成本、可测试性、可维护性、上线影响。
- 推荐方案：给出明确推荐，并说明何时应选择其他方案。
- 决策点：需要用户拍板的 trade-off 必须列出。

### 4. 话题 / 观点 / 讨论

适用：用户抛出开放话题、原则问题、行业判断、流程理念或希望听看法。

输出 SHOULD 包含：

- 观点：先给一个清晰看法，允许保留不确定性。
- 论点与依据：分条说明判断来自哪些事实、经验、项目约束或逻辑推导。
- 反方或边界：说明该观点在哪些条件下可能不成立。
- 可延展话题：如果能引发新的讨论点，可以抛出 1-3 个高价值方向。
- 决策点：若话题背后隐含产品、流程或技术选择，明确指出。

### 5. 混合输入

如果用户输入同时包含问题、需求和话题：

- 先拆分主题。
- 标注每个主题的类型倾向。
- 逐项探索，或在信息量过大时先给主题地图并建议优先级。
- 不得把多主题混成一个含糊结论。

## 可读取内容

- 用户给出的文件、日志、截图或上下文。
- 与问题相关的 `src/`、`tests/`、`docs/`、`rules/`、`issues/`、`openspec/changes/`、`iterations/` 必要片段。
- 已存在的 REQ / BUG / Change / Sprint 文档片段，用于避免重复和确认上下文。

## 禁止

- 写代码、修复代码、格式化代码、改测试。
- 新建或修改 `issues/`、`openspec/`、`iterations/`、`docs/`、`releases/`、`src/` 文件。
- 勾选 `tasks.md`、推进 workflow status、运行 apply/archive 类命令。
- 自动创建 REQ / BUG / Change / Sprint。
- 为了探索读取大范围历史归档或生成物。

## 用户明确要求记录结论时

如果用户明确说「记录下来」「帮我创建需求/BUG」「写入 Change」「更新设计文档」：

- 先确认这已超出 `/explore` 的默认只读范围。
- 根据内容选择 `/capture`、`/req-capture`、`/bug-capture`、`/req-generate`、`/bug-generate`、`/opsx-propose`、`/opsx-explore` 或 `/sprint-explore`。
- 写入前必须读取对应 Skill 和 lifecycle 规则。
- 写入后必须按对应 Workflow Sync 规则执行，不得用 `/explore` 偷偷落盘。

## 建议输出形态

按输入类型自然组织，不强制所有章节都出现。常用结构：

```text
判断
依据
方案
对比
推荐
需要你决策
下一步
```

当用户只需要轻量观点时，可以短答；当涉及项目根因、需求推进或架构取舍时，必须给出足够证据和明确决策点。

## Next

- 确认是 BUG：`/bug-capture` → `/bug-generate` → `/bug-complete`
- 确认是需求：`/req-capture` → `/req-generate` → `/req-complete`
- 确认要进入 OpenSpec：`/opsx-propose`
- 已有 BUG / REQ / Change / Sprint：切换到对应专用 explore 命令继续深入

## Final Step — AI Usage Post-command Hook（SHOULD）

Because generic explore mode normally does not change workflow state, prefer running the hook in dry-run mode before ending when the script supports generic events:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event explore --dry-run --json
```

- If the script does not support `explore`, do not force status changes only to create usage data.
- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- Do not update REQ/BUG/Change/Sprint status only to create usage data.

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
