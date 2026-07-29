---
purpose: 对象存储使用规范
content: 桶、对象 Key、目录前缀、权限、生命周期与 AI 更新要求
source: Harness Token 优化模板
update_method: 对象存储策略变化时由技术负责人确认后更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: 默认推荐一个项目一个 Bucket，桶内使用目录前缀区分业务资源
---

# 对象存储规范

## 1. 总原则

对象存储栈由 `{OBJECT_STORAGE_STACK}` 决定。默认推荐：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

项目初始化后必须在 `.env.example` 中明确 Bucket、Endpoint、访问方式和安全边界。

## 2. 标准对象前缀

```text
images/
videos/
audios/
files/
thumbnails/
processed/
tmp/
imports/
exports/
videos/covers/
videos/transcoded/
```

## 3. Object Key 形态

推荐形态：

```text
{prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

MUST NOT 使用用户原始文件名、真实身份信息或未经校验的路径片段。

## 4. AI 必须遵守

AI 在新增文件上传、视频上传、图片处理、导入导出能力时：

```text
□ 不新增多个业务 Bucket，除非 OpenSpec 明确要求
□ 复用 .env.example 中的对象存储变量
□ 使用标准前缀或在 OpenSpec 中说明例外
□ 更新媒体资源相关 OpenSpec 和文档
□ 补充对象 Key 生成逻辑和测试
```
