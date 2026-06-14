# 业务流程

```text
rules/ui-design.md（规范）
        ↓
src/shared/design-system/tokens（TS）
        ↓
globals.css + tailwind.config.ts（Web）
        ↓
shadcn/ui + shared/ui + business + templates
        ↓
/design-system 预览 + validate-design-system.py
        ↓
业务 Change 消费（如 refactor-login-ui）
```
