---
name: "usage-docs-validate"
description: "校验版本化产品使用文档、manifest、Mintlify 投影和公开安全"
---

# usage-docs-validate

Use this skill when the user asks `/usage-docs-validate <version>` or wants to validate product usage docs for a release.

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
releases/<version>/release.json
scripts/validate-usage-docs.py
scripts/validate-mintlify-site.py
```

If `usage_docs.status=generated`, also read `releases/<version>/usage-docs/manifest.json`, `mintlify/mint.json` or `mintlify/docs.json`, and `mintlify/site-manifest.json`.

```bash
python scripts/validate-usage-docs.py --release-dir releases/<version>
python scripts/validate-mintlify-site.py
python scripts/validate-release.py --release-dir releases/<version>
```
