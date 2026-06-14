# testing Specification

## Purpose

测试治理：目录、Pytest 基线、覆盖率与 Requirement 映射。

## Requirements

### Requirement: Pytest baseline

Backend tests MUST be runnable from repository root via `./scripts/run-tests.sh`.

### Requirement: Test mapping

Each REQ-0000 infrastructure requirement MUST map to at least one automated test or validation script in `openspec/testing-mapping.md`.

### Requirement: Change tests

New Services and Routers in OpenSpec Changes MUST include corresponding tests.
