#!/usr/bin/env python3
"""Compare schema.mysql.sql with a target MySQL database without mutating data."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_FILE = ROOT / "src" / "backend" / "app" / "db" / "schema.mysql.sql"

CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+`?([A-Za-z0-9_]+)`?\s*\((.*?)\)\s*ENGINE\s*=",
    re.IGNORECASE | re.DOTALL,
)

TABLE_ITEM_PREFIXES = (
    "PRIMARY ",
    "UNIQUE ",
    "KEY ",
    "INDEX ",
    "CONSTRAINT ",
    "CHECK ",
    "FOREIGN ",
    "FULLTEXT ",
    "SPATIAL ",
)


def split_top_level_csv(text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    quote: str | None = None
    index = 0
    while index < len(text):
        char = text[index]
        current.append(char)
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"', "`"):
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            current.pop()
            parts.append("".join(current).strip())
            current = []
        index += 1
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def parse_expected_schema(schema_sql: str) -> dict[str, set[str]]:
    expected: dict[str, set[str]] = {}
    for match in CREATE_TABLE_RE.finditer(schema_sql):
        table_name = match.group(1)
        columns: set[str] = set()
        for item in split_top_level_csv(match.group(2)):
            normalized = item.strip()
            upper = normalized.upper()
            if not normalized or upper.startswith(TABLE_ITEM_PREFIXES):
                continue
            column_match = re.match(r"`?([A-Za-z0-9_]+)`?\s+", normalized)
            if column_match:
                columns.add(column_match.group(1))
        expected[table_name] = columns
    return expected


def fetch_actual_schema(database_url: str) -> dict[str, set[str]]:
    try:
        from sqlalchemy import create_engine, text
    except ImportError as exc:
        raise RuntimeError("sqlalchemy is required; run with the backend uv environment") from exc

    engine = create_engine(database_url, pool_pre_ping=True)
    query = text(
        """
        SELECT TABLE_NAME, COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
    )
    actual: dict[str, set[str]] = {}
    with engine.connect() as connection:
        for row in connection.execute(query):
            actual.setdefault(str(row.TABLE_NAME), set()).add(str(row.COLUMN_NAME))
    return actual


def compare_schema(expected: dict[str, set[str]], actual: dict[str, set[str]]) -> dict[str, Any]:
    expected_tables = set(expected)
    actual_tables = set(actual)
    common_tables = expected_tables & actual_tables
    missing_columns = {
        table: sorted(expected[table] - actual[table])
        for table in sorted(common_tables)
        if expected[table] - actual[table]
    }
    extra_columns = {
        table: sorted(actual[table] - expected[table])
        for table in sorted(common_tables)
        if actual[table] - expected[table]
    }
    return {
        "missing_tables": sorted(expected_tables - actual_tables),
        "extra_tables": sorted(actual_tables - expected_tables),
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "expected_table_count": len(expected_tables),
        "actual_table_count": len(actual_tables),
    }


def has_blocking_drift(report: dict[str, Any]) -> bool:
    return bool(report["missing_tables"] or report["missing_columns"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Check target MySQL schema drift against schema.mysql.sql.")
    parser.add_argument("--schema-file", default=str(DEFAULT_SCHEMA_FILE), help="Path to schema.mysql.sql")
    parser.add_argument("--database-url", default=os.environ.get("DATABASE_URL"), help="MySQL DATABASE_URL; defaults to env")
    parser.add_argument("--schema-only", action="store_true", help="Parse schema file only and skip database connection")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    schema_file = Path(args.schema_file).resolve()
    if not schema_file.exists():
        print(
            f"schema file not found: {schema_file}; pass --schema-file when this project uses a different location",
            file=sys.stderr,
        )
        return 2
    schema_sql = schema_file.read_text(encoding="utf-8")
    expected = parse_expected_schema(schema_sql)
    if args.schema_only:
        payload: dict[str, Any] = {
            "schema_file": str(schema_file),
            "expected_table_count": len(expected),
            "expected_tables": sorted(expected),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"Parsed {len(expected)} table(s) from {schema_file}")
        return 0

    if not args.database_url:
        print("DATABASE_URL is required; pass --database-url or set DATABASE_URL", file=sys.stderr)
        return 2
    if not re.match(r"^mysql(?:\+\w+)?://", args.database_url, re.IGNORECASE):
        print("DATABASE_URL must be a MySQL URL", file=sys.stderr)
        return 2

    actual = fetch_actual_schema(args.database_url)
    report = compare_schema(expected, actual)
    payload = {"schema_file": str(schema_file), **report}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"MySQL schema drift check: expected {report['expected_table_count']} table(s), actual {report['actual_table_count']} table(s)")
        if report["missing_tables"]:
            print("Missing tables: " + ", ".join(report["missing_tables"]))
        if report["missing_columns"]:
            for table, columns in report["missing_columns"].items():
                print(f"Missing columns in {table}: {', '.join(columns)}")
        if not has_blocking_drift(report):
            print("No blocking schema drift detected.")
    return 1 if has_blocking_drift(report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
