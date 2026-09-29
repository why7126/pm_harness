---
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# project-governance Delta

## ADDED Requirements

### Requirement: 跨项目治理学习应用

ProjectPmHarness SHALL support applying confirmed governance patterns from a read-only peer project through an active OpenSpec Change and Sprint scope.

#### Scenario: 应用确认候选项

- GIVEN 用户已通过 `/spec-study <project>` 获取候选项
- WHEN 用户执行 `/spec-study apply <items>`
- THEN 系统 SHALL 通过 active Change 记录应用范围、模板同步、验证结果和学习对象只读保护结果

### Requirement: 推送前安全检测

ProjectPmHarness SHALL provide a Git safety check command for detecting committed secrets, real env files, runtime data, large local artifacts and local absolute paths.

#### Scenario: 发现阻断项

- GIVEN staged 或 tracked 文件包含禁止路径或敏感内容
- WHEN 执行 `/git-check`
- THEN 命令 SHALL 返回非零并输出脱敏后的 error 摘要和修复建议

### Requirement: 原型驱动 UI 验收

ProjectPmHarness SHALL provide a reusable UI acceptance standard for changes with prototype assets.

#### Scenario: UI Change 引用 prototype

- GIVEN Change 包含 prototype、UI Skeleton 或明确视觉参照
- WHEN 进入实现或归档阶段
- THEN Change SHALL 记录 UI Contract、视觉证据、computed style 或等价验收说明，以及 Mock/API 边界
