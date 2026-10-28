---
name: git-check
description: 检查 Git 暂存快照、工作区、环境忽略与待推送历史的安全边界
created_at: 2026-08-10 23:19:03
updated_at: 2026-10-28 11:24:48
---

# git-check

用于提交或推送前只读安全检查。先读 AGENTS.md、rules/security.md、rules/agent-context-budget.md、docs/standards/git-delivery-safety.md，沿用已读摘要。

## 命令与范围

- 默认：python scripts/git-check.py，分别检查 index blob 与受跟踪工作区，接入 env 忽略校验。
- 深度当前文件：python scripts/git-check.py --all，增加未忽略的未跟踪文件；不读取被忽略且未跟踪的真实 env，不扫描历史。
- 待推送历史：python scripts/git-check.py --base 已核对的远端提交SHA，检查 base..HEAD 的全部提交树与消息。
- 首次推送：python scripts/git-check.py --history，检查 HEAD 可达历史。
- 回归：PYTHONDONTWRITEBYTECODE=1 python scripts/test_git_check.py。

## 门禁与输出

error、不可读对象、冲突 index、覆盖不完整或策略读取失败均阻断。warning 逐项复核，不用清零代替核验。报告范围、错误数、警告数、规则与位置，不输出命中行、Git stderr 或部分凭证。二进制只检查路径与大小；文本为 UTF-8 且最多 1 MiB。LFS 内容、标签注释、子模块内容或未选择的历史需单独审查，不宣称全仓无秘密。

占位符必须完整匹配；URL host 和查询参数不能豁免凭证。路径正则只排除语法，不豁免整行或测试目录。细则见 docs/standards/git-delivery-safety.md。

## 只读边界

不自动修改 .gitignore、不 unstage、不删除数据、不执行学习对象脚本。提交推送由用户授权的 /git-sync 承接。force-proceed 不跳过 error，不自动创建 Issue；失败仅报告证据与建议。

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
