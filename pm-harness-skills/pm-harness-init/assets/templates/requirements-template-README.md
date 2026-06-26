---
purpose: 需求模板说明
content: 说明如何使用本模板创建规范的需求文档
source: pm-harness 项目模板
update_method: 模板规范变化时更新
note: 适用于所有 pm-harness 项目
---

# 需求模板使用说明

## 如何使用

1. 复制本 `template/` 目录到 `issues/requirements/REQ-xxxx-需求名称/`
2. 按照每个文件的说明填写对应内容
3. 执行 `/req-opsx REQ-xxxx-需求名称` 生成 OpenSpec Change
4. 当需求关联 Bug 时，在 `trace.md` 的「关联缺陷」中补充索引级关联，不复制 Bug 全文

## 命名规范

```
REQ-0001-user-login/         ✅ 正确：序号 + 英文简述
REQ-0002-product-list/       ✅ 正确
requirements-login/          ❌ 错误：缺少序号前缀
```

## 目录结构

```
REQ-xxxx-name/
├── requirement.md        # 需求主文档（背景、目标、用户故事、功能范围）
├── acceptance.md         # 验收标准（功能、接口、数据、UI、异常）
├── user-stories.md       # 用户故事列表
├── business-flow.md      # 业务流程图（文字描述）
├── trace.md              # 需求追溯（关联 OpenSpec Change、迭代、Bug）
├── attachments/          # 附件目录（产品文档、参考截图等）
└── prototype/            # 原型目录
    ├── web/              # Web 端原型
    │   ├── *.html        # HTML 原型（AI 开发优先参考）
    │   ├── *.png         # 可选视觉稿；提供时作为 Golden Reference，缺失不阻塞需求或开发
    │   └── *-context.md  # 原型说明
    └── wechat-miniapp/          # 微信小程序端原型（如有）
```

## trace.md 关联缺陷

需求与 Bug 存在关联时，在需求 `trace.md` 中增加或维护以下章节：

```markdown
## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0003-brand-image-display-layout-shift | high | done | fix-brand-image-display-layout-shift | 品牌 Logo 展示与提示布局修复 |
```

规则：

- 只记录索引级关联，详细复现、根因、截图、日志和回归记录以 `issues/bugs/{BUG-ID}/` 为准。
- 当 Bug 状态、严重等级或关联 Change 变化时，同步更新需求 `trace.md`。
- 多个 Bug 可按一行一个 BUG 记录，不在需求 trace 中粘贴 BUG 全文。

## 开发流程

```
1. 创建需求目录 issues/requirements/REQ-xxxx-name/
2. 填写 requirement.md 和 acceptance.md（必须）
3. 执行 /req-opsx REQ-xxxx-name 生成 OpenSpec Change
4. 执行 /opsx-apply change-name 实现功能
5. 执行 /opsx-archive change-name 归档
```
