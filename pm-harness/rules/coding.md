---
purpose: 编码规范
content: FastAPI后端、React19前端、微信小程序、共享类型、模块边界与代码质量规则
source: AI自动生成初稿，项目团队确认
update_method: 技术栈、代码风格、模块边界或质量门禁变化时更新
note: AI生成代码必须遵守本规范
---

# 编码规范

## 1. 后端 Python/FastAPI

- Python版本固定为 3.12。
- 包管理器使用 `uv`。
- API框架使用 FastAPI。
- 数据验证与序列化使用 Pydantic。
- 每个业务模块放在 `src/backend/app/modules/<module>/`。
- API路由、Schema、Service、Repository 分层清晰。
- 不允许在路由层直接写复杂业务逻辑。
- SQLite访问必须通过Repository或统一数据访问层。
- MinIO访问必须通过对象存储适配层。

推荐模块结构：

```text
src/backend/app/modules/tile/
├── router.py
├── schemas.py
├── service.py
├── repository.py
└── models.py
```

## 2. 前端 React19/TypeScript

- 使用 React19 + TypeScript。
- 样式使用 Tailwind。
- 组件库使用 shadcn/ui。
- HTTP请求使用 Axios。
- API类型与客户端通过 Orval 从 OpenAPI 生成。
- 不允许手写与后端重复的接口类型，除非有明确原因。
- 店主展示端与企业管理端必须区分路由、权限和组件边界。

## 3. 微信小程序

- 小程序目录仅承载小程序端代码。
- 不允许直接复用Web浏览器专属API。
- 上传、视频播放、图片预览必须考虑小程序平台限制。

## 4. 媒体相关代码

图片、视频、文档上传相关代码必须集中在 media 模块，不允许散落在 tile、admin 等模块中。

## 5. AI修改规则

AI修改代码时必须说明：

- 修改了哪些文件。
- 是否影响API。
- 是否影响数据库。
- 是否影响媒体上传/视频处理。
- 是否需要更新OpenSpec、docs、tests。
