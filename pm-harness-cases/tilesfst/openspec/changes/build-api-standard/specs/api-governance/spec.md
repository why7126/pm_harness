# api-governance Specification

## Purpose

API 治理：统一路径、返回、错误码、OpenAPI 与 Orval。

## Requirements

### Requirement: Unified response envelope

All public JSON APIs MUST return `{ code, message, data }`.

### Requirement: Error code registry

Business and auth errors MUST use codes documented in `docs/error-codes.md`.

### Requirement: OpenAPI metadata

Public routes MUST declare `response_model`, `summary`, `tags`.
