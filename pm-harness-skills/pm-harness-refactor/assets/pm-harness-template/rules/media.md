---
purpose: 媒体资产管理规范
content: 图片、视频、附件、封面、转码、上传、对象存储和前端展示限制
source: Harness Token 优化模板
update_method: 新增媒体类型、视频转码、封面生成、上传限制、对象存储策略时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: 涉及媒体上传、预览、处理或分发时读取
---

# 媒体资产管理规范

## 1. 媒体类型

项目可按需启用：

```text
images/
videos/
audios/
files/
thumbnails/
covers/
processed/
```

具体业务类型由 OpenSpec 和 `docs/06-video-asset-management.md` 确认。

## 2. 存储规则

- 媒体文件必须通过后端授权上传，不允许前端绕过后端直接写入未授权对象存储。
- 对象 Key 不得包含用户原始文件名、真实姓名、手机号、地址等敏感信息。
- 原始文件、缩略图、转码文件、临时文件必须有清晰前缀和清理策略。

## 3. 视频规范

- 视频格式、大小、封面、转码、多清晰度属于产品能力，必须经 OpenSpec 明确。
- 转码或封面生成不得执行用户可控命令。
- 临时文件必须写入 `data/tmp/` 或等价运行时目录，并在处理完成后清理。

## 4. AI 更新清单

AI 新增或修改媒体能力时，必须检查：

```text
□ .env.example
□ data/README.md
□ docs/06-video-asset-management.md
□ rules/object-storage.md
□ 后端 media 模块或对象存储适配层
□ 前端上传 / 预览组件
□ 集成测试与安全校验
```
