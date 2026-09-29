#!/usr/bin/env python3
"""Generate, skip, or project versioned product usage docs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = ROOT / "releases"
MINTLIFY_DIR = ROOT / "mintlify"
TEMPLATE_DIR = RELEASES_DIR / "templates" / "usage-docs"
TIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
VERSION_PATTERN = re.compile(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?")


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON {path}: {exc}") from None
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def release_dir(version: str) -> Path:
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"version must be SemVer-like, got {version}")
    return RELEASES_DIR / version


def ensure_generation_confirmed(data: dict[str, Any]) -> dict[str, Any]:
    usage_docs = data.get("usage_docs")
    if not isinstance(usage_docs, dict):
        raise ValueError("release.json usage_docs object is required before generating usage docs")
    decision = usage_docs.get("generation_decision")
    if not isinstance(decision, dict) or decision.get("required") is not True:
        raise ValueError("usage_docs.generation_decision.required must be true before generating usage docs")
    for key in ("confirmed_at", "confirmed_by", "rationale"):
        if not decision.get(key):
            raise ValueError(f"usage_docs.generation_decision.{key} is required before generating usage docs")
    if not TIME_PATTERN.fullmatch(str(decision.get("confirmed_at", ""))):
        raise ValueError("usage_docs.generation_decision.confirmed_at must be YYYY-MM-DD HH:mm:ss")
    return usage_docs


def render_template(text: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_templates(target_dir: Path, context: dict[str, str]) -> list[str]:
    if not TEMPLATE_DIR.exists():
        raise ValueError(f"missing usage docs template directory: {TEMPLATE_DIR}")
    pages: list[str] = []
    for src in sorted(TEMPLATE_DIR.rglob("*")):
        rel_path = src.relative_to(TEMPLATE_DIR)
        if src.is_dir():
            (target_dir / rel_path).mkdir(parents=True, exist_ok=True)
            continue
        target = target_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_template(src.read_text(encoding="utf-8"), context), encoding="utf-8")
        if target.suffix == ".mdx":
            pages.append(str(rel_path).replace("\\", "/"))
    return pages


def ensure_mintlify_base() -> None:
    for path in (MINTLIFY_DIR / "docs", MINTLIFY_DIR / "releases", MINTLIFY_DIR / "assets" / "screenshots"):
        path.mkdir(parents=True, exist_ok=True)
    mint_path = MINTLIFY_DIR / "mint.json"
    if not mint_path.exists():
        write_json(mint_path, {"$schema": "https://mintlify.com/schema.json", "name": "产品文档", "navigation": []})


def update_mintlify_navigation(version: str, pages: list[str]) -> None:
    write_json(
        MINTLIFY_DIR / "mint.json",
        {
            "$schema": "https://mintlify.com/schema.json",
            "name": "产品文档",
            "navigation": [
                {"group": "当前版本", "pages": ["docs/latest/overview"] if pages else []},
                {"group": version, "pages": [f"docs/{version}/{page.removesuffix('.mdx')}" for page in pages]},
            ],
        },
    )


def project_to_mintlify(version: str, rdir: Path, usage_dir: Path, manifest: dict[str, Any]) -> None:
    ensure_mintlify_base()
    pages = [str(page) for page in manifest.get("pages", []) if isinstance(page, str)]
    generated_at = now_text()
    target_root = MINTLIFY_DIR / "docs" / version
    latest_root = MINTLIFY_DIR / "docs" / "latest"
    for target in (target_root, latest_root):
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    for page in pages:
        source = usage_dir / page
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8")
        hashes[page] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        for target in (target_root / page, latest_root / page):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
    announcement = rdir / str(load_json(rdir / "release.json").get("announcement", "announcement.mdx"))
    if announcement.exists():
        target = MINTLIFY_DIR / "releases" / version / "announcement.mdx"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(announcement.read_text(encoding="utf-8"), encoding="utf-8")
    projection = {
        "status": "synced",
        "source_release": rel(rdir),
        "source_manifest": rel(usage_dir / "manifest.json"),
        "target_site_root": rel(target_root),
        "latest_target": rel(latest_root),
        "synced_at": generated_at,
        "mode": "copy",
        "content_hashes": hashes,
    }
    manifest["site_projection"] = projection
    write_json(usage_dir / "manifest.json", manifest)
    write_json(
        MINTLIFY_DIR / "site-manifest.json",
        {"updated_at": generated_at, "latest_version": version, "versions": [version], "projections": [projection]},
    )
    update_mintlify_navigation(version, pages)


def generate_usage_docs(version: str, *, force: bool = False) -> Path:
    rdir = release_dir(version)
    release_path = rdir / "release.json"
    data = load_json(release_path)
    usage_docs = ensure_generation_confirmed(data)
    target_dir = rdir / str(usage_docs.get("root") or "usage-docs")
    if target_dir.exists() and not force:
        raise ValueError(f"{target_dir} already exists; rerun with --force to overwrite current-version generated docs")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    generated_at = now_text()
    pages = copy_templates(target_dir, {"VERSION": version, "GENERATED_AT": generated_at, "SOURCE_VERSION": "null"})
    manifest = load_json(target_dir / "manifest.json")
    manifest.update(
        {
            "version": version,
            "generated_at": generated_at,
            "source_release": {"path": "release.json", "sha256": file_sha256(release_path)},
            "pages": pages,
        }
    )
    write_json(target_dir / "manifest.json", manifest)
    project_to_mintlify(version, rdir, target_dir, manifest)
    usage_docs.update({"status": "generated", "root": "usage-docs", "manifest": "usage-docs/manifest.json"})
    data["usage_docs"] = usage_docs
    gates = data.setdefault("gates", {})
    gates["usage_docs_preview"] = {
        "status": "blocked",
        "evidence": f"{generated_at}: generated usage docs under {rel(target_dir)} and projected to mintlify/. Run validate-usage-docs before publish.",
    }
    write_json(release_path, data)
    return target_dir


def mark_skipped(version: str, *, confirmed_by: str, rationale: str, confirmed_at: str | None = None) -> None:
    if not rationale.strip():
        raise ValueError("--rationale is required when marking usage docs skipped")
    rdir = release_dir(version)
    release_path = rdir / "release.json"
    data = load_json(release_path)
    confirmed_at = confirmed_at or now_text()
    if not TIME_PATTERN.fullmatch(confirmed_at):
        raise ValueError("--confirmed-at must be YYYY-MM-DD HH:mm:ss")
    data["usage_docs"] = {
        "status": "skipped",
        "root": "usage-docs",
        "manifest": "usage-docs/manifest.json",
        "generation_decision": {
            "required": False,
            "confirmed_at": confirmed_at,
            "confirmed_by": confirmed_by,
            "rationale": rationale,
        },
    }
    data.setdefault("gates", {})["usage_docs_preview"] = {
        "status": "na",
        "rationale": f"{confirmed_at}: usage docs skipped by {confirmed_by}; {rationale}",
    }
    write_json(release_path, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip", action="store_true")
    parser.add_argument("--confirmed-by", default="operator")
    parser.add_argument("--confirmed-at")
    parser.add_argument("--rationale", default="")
    args = parser.parse_args()
    try:
        if args.skip:
            mark_skipped(args.version, confirmed_by=args.confirmed_by, rationale=args.rationale, confirmed_at=args.confirmed_at)
            print(f"Usage docs skipped for {args.version}; release.json updated.")
        else:
            target = generate_usage_docs(args.version, force=args.force)
            print(f"Usage docs generated: {target}")
    except ValueError as exc:
        print(f"Usage docs generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
