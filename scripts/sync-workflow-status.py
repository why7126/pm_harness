#!/usr/bin/env python3
"""
Sync REQ / BUG / Sprint / OpenSpec workflow status across derived documents.

Usage:
  python scripts/sync-workflow-status.py --sprint sprint-002
  python scripts/sync-workflow-status.py --event opsx.archive --change add-example-capability --sprint auto
  python scripts/sync-workflow-status.py --sprint auto --check
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_sync.engine import main

if __name__ == "__main__":
    raise SystemExit(main())
