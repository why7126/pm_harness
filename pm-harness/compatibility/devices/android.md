---
purpose: Android 端兼容适配说明
content: Android 系统版本、设备范围、权限、网络、存储、媒体、推送、打包发布、测试矩阵和初始化生成规则
source: Harness compatibility/devices/android.md 抽象模板
update_method: Android 技术栈、最低系统版本、权限能力、打包方式或发布渠道变化时更新
owner: {ANDROID_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/devices/android.md 模块
---

# Android 端兼容说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在产品形态包含 Android 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` Android 端的系统版本、设备性能、权限、网络、存储、媒体、发布和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{ANDROID_STACK}` | 技术栈 | Native / React Native / Flutter |
| `{ANDROID_MIN_VERSION}` | 最低系统版本 | 待确认 |
| `{ANDROID_TARGET_SDK}` | Target SDK | 待确认 |
| `{ANDROID_PERMISSIONS}` | 权限清单 | 相册 / 摄像头 / 定位 |
| `{ANDROID_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用 + 个性化]`

- 权限必须按需申请，并处理拒绝授权。
- 低端设备、弱网、后台切换、系统杀进程、存储空间不足必须验证。
- 上传下载、媒体播放、文件选择、扫码和定位不得只按模拟器验证。
- 发布渠道、签名、隐私合规和 Target SDK 变更必须同步文档。

## 3. 测试矩阵 `[通用]`

| 测试域 | 主流 Android | 低端 Android | 模拟器 | 状态 |
|---|---|---|---|---|
| 安装启动 | 必测 | 条件启用 | 必测 | 待确认 |
| 登录授权 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 上传媒体 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 弱网后台 | 必测 | 条件启用 | 条件启用 | 待确认 |

## 4. 初始化生成规则 `[通用]`

产品形态包含 Android 时保留本文；否则删除或标记为不适用。不得伪造真机测试或应用商店审核结果。
