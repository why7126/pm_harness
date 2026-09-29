#!/usr/bin/env python3
"""Validate versioned product usage docs for a release."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MINTLIFY_DIR = ROOT / "mintlify"
TIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"\bpassword\s*=", re.I),
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path} must contain a JSON object")
        return {}
    return data


def scan_public_safety(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                errors.append(f"public usage docs contain sensitive pattern {pattern.pattern}: {path}")


def validate_generated(release_path: Path, release_data: dict[str, Any], usage_docs: dict[str, Any], errors: list[str]) -> None:
    rdir = release_path.parent
    version = str(release_data.get("version", ""))
    root_name = str(usage_docs.get("root") or "usage-docs")
    manifest_name = str(usage_docs.get("manifest") or f"{root_name}/manifest.json")
    usage_dir = rdir / root_name
    manifest_path = rdir / manifest_name
    if not usage_dir.exists():
        errors.append(f"usage_docs.status generated requires directory: {usage_dir}")
        return
    manifest = load_json(manifest_path, errors)
    pages = manifest.get("pages")
    if manifest.get("version") != version:
        errors.append("manifest.version must match release version")
    if not TIME_PATTERN.fullmatch(str(manifest.get("generated_at", ""))):
        errors.append("manifest.generated_at must be YYYY-MM-DD HH:mm:ss")
    if not isinstance(pages, list) or not pages:
        errors.append("manifest.pages must be a non-empty list")
        pages = []
    actual_pages = sorted(str(path.relative_to(usage_dir)).replace("\\", "/") for path in usage_dir.rglob("*.mdx"))
    if sorted(str(page) for page in pages) != actual_pages:
        errors.append("manifest.pages must match actual usage-docs .mdx files")
    projection = manifest.get("site_projection")
    if isinstance(projection, dict):
        for key in ("target_site_root", "latest_target", "synced_at", "content_hashes"):
            if key not in projection:
                errors.append(f"manifest.site_projection.{key} is required")
        if not TIME_PATTERN.fullmatch(str(projection.get("synced_at", ""))):
            errors.append("manifest.site_projection.synced_at must be YYYY-MM-DD HH:mm:ss")
    files_to_scan = [release_path, manifest_path, rdir / str(release_data.get("announcement", "announcement.mdx"))]
    files_to_scan.extend(usage_dir.rglob("*.mdx"))
    if MINTLIFY_DIR.exists():
        files_to_scan.extend(MINTLIFY_DIR.rglob("*.mdx"))
        files_to_scan.extend([MINTLIFY_DIR / "mint.json", MINTLIFY_DIR / "site-manifest.json"])
    scan_public_safety(files_to_scan, errors)


def validate_skipped(release_path: Path, usage_docs: dict[str, Any], errors: list[str]) -> None:
    rdir = release_path.parent
    root_name = str(usage_docs.get("root") or "usage-docs")
    if (rdir / root_name).exists():
        errors.append("usage_docs.status skipped must not create usage-docs directory")
    decision = usage_docs.get("generation_decision")
    if not isinstance(decision, dict):
        errors.append("usage_docs.generation_decision is required when skipped")
        return
    if decision.get("required") is not False:
        errors.append("usage_docs.generation_decision.required must be false when skipped")
    for key in ("confirmed_at", "confirmed_by", "rationale"):
        if not decision.get(key):
            errors.append(f"usage_docs.generation_decision.{key} is required when skipped")


def validate_release_usage_docs(release_path: Path) -> list[str]:
    errors: list[str] = []
    release_data = load_json(release_path, errors)
    if errors:
        return errors
    usage_docs = release_data.get("usage_docs")
    if not isinstance(usage_docs, dict):
        return ["usage_docs object is required for usage-docs governed releases"]
    status = str(usage_docs.get("status", "")).lower()
    gates = release_data.get("gates")
    gate = gates.get("usage_docs_preview") if isinstance(gates, dict) else None
    if not isinstance(gate, dict):
        errors.append("gate usage_docs_preview is required")
    if status == "generated":
        validate_generated(release_path, release_data, usage_docs, errors)
    elif status == "skipped":
        validate_skipped(release_path, usage_docs, errors)
    elif status == "pending_confirmation":
        errors.append("usage_docs.status pending_confirmation blocks release readiness")
    else:
        errors.append("usage_docs.status must be generated, skipped, or pending_confirmation")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", required=True)
    args = parser.parse_args()
    release_path = Path(args.release_dir).resolve() / "release.json"
    errors = validate_release_usage_docs(release_path)
    if errors:
        print("Usage docs validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Usage docs validation passed: {release_path.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
