# pm-prd-design

企业级 AI 产品经理 PRD 需求文档与产品原型设计工程化生成 Skill。

把"需求 → 交互 → 可点击原型 → 版本化交付包"这条链路变成一套可重复、可校验、可增量演进的工程流程，而不是一次性的自由发挥。核心解决的问题：迭代/打补丁时容易"顺手"改动未被授权的区域，导致产品设计风格漂移、无法追溯改动范围。

## 三种模式

- **CREATE_PRD_DESIGN** — 从零创建产品需求与设计原型
- **ITERATE_PRD_DESIGN** — 在已有产品设计基础上整体性改进/新增
- **PATCH_PRD_DESIGN** — 范围明确的小版本补丁，默认拒绝改动，只做明确授权的项

完整工作流程、原则与质量门禁见 [`SKILL.md`](./SKILL.md)。

### 快速指定模式（可选）

不指定时会根据你的描述自动识别模式，拿不准会反问。想跳过识别、直接指定，在消息开头加显式触发词即可：

```
CREATE: 帮我做一个任务管理产品的 PRD 和原型...
ITERATE: 在上一版基础上给任务列表页加筛选功能...
PATCH: 只把设置页的通知开关默认值改成开启，其他不动...
```

## 目录结构

```
pm-prd-design-skill/
├── SKILL.md                  # 主入口：原则/工作流/模式说明/质量门禁
├── README.md
├── VERSION
├── prompts/                  # 各模式的角色设定与执行步骤
│   ├── create-mode-prompt.md
│   ├── iteration-mode-prompt.md
│   ├── patch-mode-prompt.md
│   └── validator-prompt.md
├── templates/                 # 输入/输出文件模板
│   ├── product-context-template.md
│   ├── ui-design-template.md
│   ├── page-request-template.md
│   ├── change-request-template.md
│   ├── patch-request-template.md
│   └── version-manifest-template.md
├── schemas/                   # 结构化字段定义
│   ├── input-schema.yaml
│   ├── output-schema.yaml
│   └── version-manifest-schema.yaml
└── validators/                 # 质量门禁校验清单
    ├── package-validator.md
    ├── regression-validator.md
    └── patch-scope-validator.md
```

## 输出交付物

`requirement.md`、`interaction.md`、`prototype.html`（可点击高保真原型）、`prototype-context.md`、`prototype.png`、`version-manifest.md`，ITERATE/PATCH 模式额外产出 `change-log.md`、`diff-report.md`、`regression-report.md`，最终打包为 `package.zip`。完整定义见 `schemas/output-schema.yaml`。

## 版本号规则

CREATE 起版 `1.0.0`；ITERATE 次版本号 +1；PATCH 修订号 +1。每次产出都会更新 `version-manifest.md`，记录本版本的稳定区（未改动）与变更区（本次改动），作为下一次迭代/打补丁的判断依据。
