---
name: git-sync
description: 按交付范围安全暂存、提交、检查历史并同步 Git 远程与正式发布标签
created_at: 2026-10-28 11:24:48
updated_at: 2026-10-28 11:24:48
---

# git-sync

用于用户明确要求按交付范围暂存、提交或同步远程；只检查时使用 /git-check。本技能不代替验收、发布或归档，不因同步请求自动获得发布标签授权。

## 读取与范围

遵守 AGENTS.md、rules/security.md、rules/agent-context-budget.md、docs/standards/git-delivery-safety.md；读取相关 Change trace、Sprint 与发布事实源。已读内容摘要承接，定位后读取。已有授权持续有效，不重复确认。

1. 检查分支、upstream 与工作区分类，脱敏展示 staged/unstaged/untracked 摘要。远端 URL 可能含凭证，禁止原样输出。
2. 依据交付范围形成文件/hunk 清单。保护调用前 staged 内容；范围外 staged 内容不混入提交，不自动 unstage。归属不清时给出 2–3 个范围选项及推荐项，等待用户决定。
3. 混合工作区禁止 git add . 或 git add -A。逐路径或 hunk 暂存，复核实际 cached diff、name-status、stat 与 diff --cached --check；不将凭证 diff 原文写入报告。

## 提交前门禁

- 运行 python scripts/validate-env-ignore-policy.py 和 python scripts/git-check.py，覆盖实际 index blob。检查后 index 变化必须重跑。
- 核对交付验证。warning 逐项记录规则、位置、原因与处置；error 或覆盖不完整阻断，不能批量豁免测试目录、正则源码或证据。
- .gitignore 仅控制未跟踪文件；按最小范围调整新类型时保留示例和长期证据。已跟踪风险须评估索引及历史，明确授权后才精确 git rm --cached --，保留本地文件。不删除数据或用忽略规则掩盖风险。
- 提交信息基于实际 staged diff，不编造验收。已授权且范围清晰时报告摘要后提交；不自动 amend、squash、reset 或改写历史。
- 核对新 commit 的文件清单与 SHA，避免并发暂存引入额外范围。

## 远程同步

1. 按授权目标 fetch 后固定远端 commit SHA，比较 ahead/behind。远端领先或分叉按项目策略整合并保护无关改动；冲突核对双方意图，不明确时保留现场并给出具体决策。
2. 已有远端运行 python scripts/git-check.py --base 已核对的远端提交SHA；首次推送运行 python scripts/git-check.py --history。检查提交树与提交消息，包含中间提交后删除的内容，--all 不能替代历史扫描。
3. 浅克隆、缺失对象或范围无法完整证明时先补齐历史。真实凭证或客户数据进入待推送历史则停止，报告清理与轮换需求，不自动重写历史。
4. 整合或新增提交后重跑相关测试、diff --check、安全与历史检查。确认 HEAD 与扫描版本一致，指定分支快进推送；禁止 --force、--force-with-lease 或删除远端引用。
5. 推送后只读核对远端 SHA。认证/网络失败准确报告停留阶段，不输出 helper 凭据或 Token，不伪称同步完成。

## 正式版本标签

只有用户已授权正式标签且发布事实、验证和负责人确认满足项目规则时，才创建 annotated tag；普通提交和镜像 tag 不触发 Git tag。检查本地与远端同名 tag，以 peeled commit 比较：指向目标则复用，其他指向则阻断，不移动或覆盖。单独复核标签注释无敏感内容，再单独推送该 tag 并核对远端。

## 输出与复盘

报告交付范围、排除项、检查、warning 处置、commit、分支、远端、tag、阻断阶段和恢复动作。不得输出命中行、凭证、真实 env 或原始 Git 错误。执行链路复盘包含链路状态、问题证据、规范优化建议与 follow-up 状态。force-proceed 不跳过 error；未经明确授权不自动创建 Issue/Change。Git 同步不改变业务阶段，不虚构 Workflow Sync 事件。

## Final Output Contract

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
