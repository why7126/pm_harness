---
purpose: issues 需求/BUG 生命周期阶段与当前态索引规范
content: plan/review/archive 阶段目录、CHANGELOG 当前态索引和事实源边界
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# Issues 生命周期规范

## 阶段目录

REQ 与 BUG SHOULD 使用三阶段目录：

```text
issues/requirements/{plan,review,archive}/REQ-xxxx-slug/
issues/bugs/{plan,review,archive}/BUG-xxxx-slug/
```

`_registry.yaml` 与 `CHANGELOG.md` 保留在 `issues/requirements/` 和 `issues/bugs/` 根目录，不进入单条 Issue 目录。

## 当前态 CHANGELOG

`issues/requirements/CHANGELOG.md` 与 `issues/bugs/CHANGELOG.md` 是目录级当前态看板索引。每个 Issue SHOULD 维护一行，至少包含：

```text
编号 | 标题 | 当前状态 | 阶段 | Sprint | Change | 最近更新时间 | 下一步 | 事实源
```

当前态索引只用于快速定位和人工扫描，不替代以下事实源：

- `_registry.yaml`
- 单条 Issue `trace.md`
- Sprint 四件套
- OpenSpec Change

新增、评审、纳入 Sprint、创建 Change、apply、archive、状态同步或历史漂移修复后 SHOULD 更新对应当前态行。

## 安全边界

CHANGELOG 不得记录真实客户数据、密钥、未脱敏日志、本机绝对路径或聊天原文。需要引用证据时使用仓库相对路径或脱敏说明。
