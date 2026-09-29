---
created_at: 2026-08-21 13:20:25
updated_at: 2026-08-21 13:20:25
---

# Governance Log: default review approve

## 迭代目标

将 `/req-review` 与 `/bug-review` 的高频通过路径调整为无 flag 默认 approve，减少日常治理命令输入负担，同时保留显式非通过结论的安全边界。

## 变更摘要

- `/req-review <REQ-id>` 默认等同 approved；`--approve` 继续作为兼容写法。
- `/bug-review <BUG-id>` 默认等同 approved；`--approve` 继续作为兼容写法。
- `--reject`、`--defer`、BUG 的 `--wont-fix` 仍必须显式提供。
- 下游命令示例改为推荐无 `--approve` 写法。
- 生命周期规则中的评审通过示例同步调整为默认 approve 语义。

## 影响范围

- 根项目 `.agents/skills/` 中的 review 命令与相关下一步示例。
- `pm-harness/` 新项目模板中的技能与生命周期规则。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
- `pm-harness-skills/pm-harness-refactor/assets/pm-harness-template/` 存量接入模板资产。
- OpenSpec Change `default-review-approve` 与 `sprint-001` 范围。

## 更新文件

- `.agents/skills/req-review/SKILL.md`
- `.agents/skills/bug-review/SKILL.md`
- `.agents/skills/{req-complete,bug-complete,req-opsx,sprint-propose,explore,initialize-project,build-design-system}/SKILL.md`
- `pm-harness/.agents/skills/**`
- `pm-harness/rules/{issues-lifecycle,requirement-management,bug-management}.md`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/**`
- `pm-harness-skills/pm-harness-refactor/assets/pm-harness-template/**`
- `openspec/changes/default-review-approve/**`
- `iterations/change/sprint-001/{sprint.md,sprint.yaml}`

## 验证结果

已通过：

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate default-review-approve`
- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`
- `python scripts/sync-workflow-status.py --event opsx.apply --change default-review-approve --sprint auto`
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change default-review-approve --sprint sprint-001 --json`

## API/DB/Web/小程序/管理端/Orval/Docker 影响

无影响。本次仅修改治理命令说明、规则文档、模板资产和 OpenSpec Change 文档，不触碰业务实现、接口、数据库、前端、小程序、管理端、Orval 或 Docker 配置。

## 后续建议

后续若发现用户仍频繁显式输入 `--approve`，可以保留兼容但继续在 Next 示例中只推荐无 flag 写法。
