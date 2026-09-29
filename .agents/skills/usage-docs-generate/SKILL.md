---
name: "usage-docs-generate"
description: "确认需要后生成当前版本产品使用文档、manifest 并投影到 Mintlify"
---

# usage-docs-generate

Use this skill when the user asks `/usage-docs-generate <version>` or wants to generate product usage docs for a release version.

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
rules/document-governance.md
releases/<version>/release.json
releases/templates/usage-docs/
scripts/generate-usage-docs.py
scripts/validate-usage-docs.py
```

Before generation, `release.json` MUST explicitly confirm `usage_docs.generation_decision.required=true` with `confirmed_at`, `confirmed_by`, and `rationale`.

```bash
python scripts/generate-usage-docs.py <version>
python scripts/validate-usage-docs.py --release-dir releases/<version>
```

Do not include secrets, real `.env`, database URLs, Authorization headers, Cookies, object storage credentials, production private domains, local absolute paths, or real customer data.
