---
purpose: 桌面端兼容适配说明
content: 桌面端支持范围、操作系统、CPU 架构、运行时、文件系统、更新、权限、安全、测试矩阵和初始化生成规则
source: Harness compatibility/devices/desktop.md 抽象模板
update_method: 桌面端技术栈、操作系统、打包方式、更新策略或权限能力变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {DESKTOP_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/devices/desktop.md 模块
---

# 桌面端兼容说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在产品形态包含桌面端时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 桌面端的系统、架构、运行时、安装更新、文件权限、本地数据、安全和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{DESKTOP_STACK}` | 桌面技术栈 | Electron / Tauri / Qt |
| `{OS_SUPPORT_MATRIX}` | 操作系统矩阵 | Windows / macOS / Linux |
| `{CPU_ARCH_SUPPORT}` | CPU 架构 | x64 / arm64 |
| `{DESKTOP_PACKAGE_COMMAND}` | 打包命令 | 待确认 |
| `{DESKTOP_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用 + 个性化]`

- 明确最低 OS 版本、CPU 架构、安装包格式和自动更新策略。
- 本地文件、数据库、模型、缓存和日志必须有固定目录与清理策略。
- 系统权限、证书、代理、离线、杀毒软件拦截和防火墙行为必须验证。
- 桌面端不得默认复用 Web 兼容结论。

## 3. 测试矩阵 `[通用]`

| 测试域 | Windows | macOS | Linux | 状态 |
|---|---|---|---|---|
| 安装启动 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 更新卸载 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 本地数据 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 权限安全 | 必测 | 条件启用 | 条件启用 | 待确认 |

## 4. 初始化生成规则 `[通用]`

产品形态包含桌面端时保留本文；否则删除或标记为不适用。不得编造 OS 认证或安装测试结果。
