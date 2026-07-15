#!/usr/bin/env bash
set -euo pipefail
python scripts/generate-baseline.py
python scripts/validate-directory-structure.py
if [[ "${PM_HARNESS_DELIVERY_VALIDATE:-0}" == "1" ]]; then
  python scripts/validate-generated-docs.py --strict
else
  python scripts/validate-generated-docs.py
fi
printf '\n项目基线已生成，请人工Review README.md、openspec/project.md 和 docs/*。\n'
