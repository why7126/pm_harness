---
purpose: iOS 端兼容适配说明
content: iOS 系统版本、设备范围、权限、网络、存储、媒体、推送、打包发布、测试矩阵和初始化生成规则
source: Harness compatibility/devices/ios.md 抽象模板
update_method: iOS 技术栈、最低系统版本、权限能力、打包方式或发布渠道变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {IOS_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/devices/ios.md 模块
---

# iOS 端兼容说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在产品形态包含 iOS 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` iOS 端的系统版本、设备范围、权限、网络、存储、媒体、App Store 发布和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{IOS_STACK}` | 技术栈 | SwiftUI / UIKit / React Native / Flutter |
| `{IOS_MIN_VERSION}` | 最低 iOS 版本 | 待确认 |
| `{IOS_DEVICE_MATRIX}` | 设备矩阵 | iPhone / iPad |
| `{IOS_PERMISSIONS}` | 权限清单 | 相册 / 摄像头 / 麦克风 / 定位 |
| `{IOS_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用 + 个性化]`

- 权限说明必须与 Info.plist、隐私协议和实际功能一致。
- 安全区、键盘、横竖屏、深色模式、动态字体和低电量/弱网必须验证。
- 上传下载、媒体播放、文件选择、扫码和定位必须真机验证。
- App Store 审核、证书、签名和 TestFlight 流程必须记录。

## 3. 测试矩阵 `[通用]`

| 测试域 | iPhone | iPad | 模拟器 | 状态 |
|---|---|---|---|---|
| 安装启动 | 必测 | 条件启用 | 必测 | 待确认 |
| 登录授权 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 上传媒体 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 安全区键盘 | 必测 | 条件启用 | 条件启用 | 待确认 |

## 4. 初始化生成规则 `[通用]`

产品形态包含 iOS 时保留本文；否则删除或标记为不适用。不得伪造真机测试、TestFlight 或 App Store 审核结果。
