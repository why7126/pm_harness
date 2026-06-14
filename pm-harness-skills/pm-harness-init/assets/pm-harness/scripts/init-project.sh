#!/usr/bin/env bash
set -euo pipefail
python scripts/generate-baseline.py
python scripts/validate-directory-structure.py
printf '\n项目基线已生成，请人工Review README.md、openspec/project.md 和 docs/*。\n'
