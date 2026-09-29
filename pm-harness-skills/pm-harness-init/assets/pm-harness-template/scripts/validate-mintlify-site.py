#!/usr/bin/env python3
"""Validate the public Mintlify documentation site projection.

The validator is intentionally product-neutral: it checks public safety,
navigation links, version projection shape and forbidden local/build files
without requiring product-specific pages.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MINTLIFY_DIR = ROOT / "mintlify"
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
MDX_HREF_PATTERN = re.compile(r"\bhref=[\"']([^\"']+)[\"']")
TIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
FORBIDDEN_NAMES = {
    ".DS_Store",
    ".env",
    ".env.local",
    ".mintlify",
    "build",
    "dist",
    "node_modules",
}
SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\bMINIO_(?:ACCESS|SECRET)_KEY\s*=", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"\bpassword\s*=", re.I),
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return data


def site_page_ref(path: Path) -> str:
    return str(path.relative_to(MINTLIFY_DIR).with_suffix("")).replace("\\", "/")


def page_path_from_ref(ref: str) -> Path:
    return MINTLIFY_DIR / f"{ref.removeprefix('/').removesuffix('/')}.mdx"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_ref(raw_ref: str) -> str:
    ref = raw_ref.strip().split()[0].strip("<>")
    ref = ref.split("#", 1)[0]
    ref = ref.split("?", 1)[0]
    return ref


def collect_navigation_pages(value: Any) -> list[str]:
    pages: list[str] = []

    def visit(item: Any) -> None:
        if isinstance(item, str):
            if item.endswith(".mdx"):
                pages.append(item[:-4])
            elif "/" in item or item in {"index", "overview"}:
                pages.append(item)
            return
        if isinstance(item, dict):
            for key, nested in item.items():
                if key in {"page", "href"} and isinstance(nested, str) and not nested.startswith(("http://", "https://")):
                    pages.append(normalize_ref(nested).removesuffix(".mdx").removeprefix("/"))
                else:
                    visit(nested)
        elif isinstance(item, list):
            for nested in item:
                visit(nested)

    visit(value)
    return pages


def validate_config(errors: list[str]) -> tuple[dict[str, Any], set[str]]:
    docs_json = MINTLIFY_DIR / "docs.json"
    mint_json = MINTLIFY_DIR / "mint.json"
    if docs_json.exists():
        config_path = docs_json
        config = load_json(docs_json, errors)
        if config.get("$schema") != "https://mintlify.com/docs.json":
            errors.append('Mintlify docs.json $schema must be "https://mintlify.com/docs.json"')
    elif mint_json.exists():
        config_path = mint_json
        config = load_json(mint_json, errors)
        if "$schema" not in config:
            errors.append("Mintlify mint.json $schema is required")
    else:
        errors.append("missing Mintlify config: mintlify/docs.json or mintlify/mint.json")
        return {}, set()

    nav_pages = collect_navigation_pages(config.get("navigation", []))
    seen: set[str] = set()
    for page in nav_pages:
        if page in seen:
            errors.append(f"Mintlify navigation duplicates page: {page}")
        seen.add(page)
        if not page_path_from_ref(page).exists():
            errors.append(f"Mintlify navigation references missing page: {page}")

    if not nav_pages and any(MINTLIFY_DIR.rglob("*.mdx")):
        errors.append(f"{config_path.relative_to(ROOT)} navigation should mount at least one .mdx page")
    return config, seen


def validate_links_and_images(nav_pages: set[str], errors: list[str]) -> None:
    all_pages = {site_page_ref(path): path for path in MINTLIFY_DIR.rglob("*.mdx")}
    for ref, path in all_pages.items():
        if ref.startswith("docs/latest/") and nav_pages and ref not in nav_pages:
            errors.append(f"latest page is not mounted in navigation: {ref}")
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                errors.append(f"Mintlify public file contains sensitive pattern {pattern.pattern}: {path.relative_to(ROOT)}")
        refs = [*MARKDOWN_LINK_PATTERN.findall(text), *MARKDOWN_IMAGE_PATTERN.findall(text), *MDX_HREF_PATTERN.findall(text)]
        for raw_ref in refs:
            target = normalize_ref(raw_ref)
            if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            if target.startswith("/assets/"):
                asset = MINTLIFY_DIR / target.removeprefix("/")
                if not asset.exists() or asset.is_dir():
                    errors.append(f"Mintlify page references missing asset: {ref} -> {target}")
                continue
            target_path = page_path_from_ref(target) if target.startswith("/") else (path.parent / target).resolve()
            if target_path.suffix != ".mdx":
                target_path = target_path.with_suffix(".mdx")
            try:
                target_path.relative_to(MINTLIFY_DIR.resolve())
            except ValueError:
                errors.append(f"Mintlify page references outside site root: {ref} -> {raw_ref}")
                continue
            if not target_path.exists():
                errors.append(f"Mintlify page has broken link: {ref} -> {raw_ref}")


def validate_site_manifest(errors: list[str]) -> None:
    manifest_path = MINTLIFY_DIR / "site-manifest.json"
    if not manifest_path.exists():
        return
    manifest = load_json(manifest_path, errors)
    raw_latest_version = manifest.get("latest_version")
    latest_version = str(raw_latest_version).strip() if raw_latest_version is not None else ""
    if latest_version and not TIME_PATTERN.fullmatch(str(manifest.get("updated_at", ""))):
        errors.append("site-manifest.updated_at must be YYYY-MM-DD HH:mm:ss")
    versions = manifest.get("versions")
    if latest_version and isinstance(versions, list) and latest_version not in versions:
        errors.append("site-manifest.versions must include latest_version")
    latest_root = MINTLIFY_DIR / "docs" / "latest"
    version_root = MINTLIFY_DIR / "docs" / latest_version if latest_version else None
    if latest_version and latest_root.exists() and version_root and version_root.exists():
        latest_pages = sorted(path.relative_to(latest_root) for path in latest_root.rglob("*.mdx"))
        version_pages = sorted(path.relative_to(version_root) for path in version_root.rglob("*.mdx"))
        if latest_pages != version_pages:
            errors.append("docs/latest pages must match docs/<latest_version> pages")

    projections = manifest.get("projections")
    if not isinstance(projections, list):
        return
    for projection in projections:
        if not isinstance(projection, dict):
            continue
        target = projection.get("target_site_root")
        hashes = projection.get("content_hashes")
        if not isinstance(target, str) or not isinstance(hashes, dict):
            continue
        target_root = ROOT / target
        for page, expected in hashes.items():
            page_path = target_root / str(page)
            if not page_path.exists():
                errors.append(f"site-manifest content_hashes references missing page: {target}/{page}")
                continue
            if str(expected) != file_sha256(page_path):
                errors.append(f"site-manifest content_hashes drift for page: {target}/{page}")


def validate_forbidden_files(errors: list[str]) -> None:
    for path in MINTLIFY_DIR.rglob("*"):
        if path.name in FORBIDDEN_NAMES or (path.name.endswith(".env") and not path.name.endswith(".env.example")):
            errors.append(f"Mintlify contains forbidden file or build output: {path.relative_to(ROOT)}")


def validate_mintlify_site() -> list[str]:
    errors: list[str] = []
    if not MINTLIFY_DIR.exists():
        return ["missing directory: mintlify"]
    _, nav_page_set = validate_config(errors)
    validate_links_and_images(nav_page_set, errors)
    validate_site_manifest(errors)
    validate_forbidden_files(errors)
    return errors


def main() -> int:
    errors = validate_mintlify_site()
    if errors:
        print("Mintlify site validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Mintlify site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
