---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# Test Plan

## 必跑校验

```bash
python scripts/validate-root-cause-evidence.py --all-active --json
python scripts/validate-agent-context-budget.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
openspec validate apply-projectmoonbox-governance-increments
python pm-harness/scripts/validate-template-sync.py
python pm-harness/scripts/validate-directory-structure.py
python pm-harness/scripts/validate-skill-package.py
python pm-harness/scripts/validate-agent-context-budget.py
python scripts/sync-workflow-status.py --event opsx.apply --change apply-projectmoonbox-governance-increments --sprint auto
python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-projectmoonbox-governance-increments --sprint sprint-001 --json
```

## 不适用项

- API、数据库、Web、小程序、管理端、Orval、Docker Compose 不涉及运行时变更，不跑业务测试。
