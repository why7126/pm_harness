---
name: "usage-docs-update"
description: "更新或跳过当前版本产品使用文档，并维护 release usage_docs 状态"
---

# usage-docs-update

Use this skill when the user asks `/usage-docs-update <version>` or wants to update, regenerate, project, or skip product usage docs.

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
releases/<version>/release.json
scripts/generate-usage-docs.py
scripts/validate-usage-docs.py
```

```bash
python scripts/generate-usage-docs.py <version>
python scripts/generate-usage-docs.py <version> --force
python scripts/generate-usage-docs.py <version> --skip --confirmed-by <name> --rationale "<reason>"
```

Old-version content corrections require explicit authorization and must be limited to public-safety fixes or approved corrections.
