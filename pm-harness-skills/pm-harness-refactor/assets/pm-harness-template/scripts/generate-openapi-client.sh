#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

(cd "${ROOT_DIR}/src/backend" && uv run python -c "import json; from app.main import app; print(json.dumps(app.openapi()))") \
  > "${ROOT_DIR}/src/web/openapi.json"

(cd "${ROOT_DIR}/src/web" && ./node_modules/.bin/orval --config orval.config.ts)
