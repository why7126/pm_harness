---
name: pm-harness-init
description: 初始化 AI Coding 项目的 harness 工程结构。凡用户要创建、生成、优化或打包 pm-harness / OpenSpec + AI Agent 规范编程项目骨架时必须使用；输出前必须执行项目化渲染、能力裁剪、模板痕迹清理和交付质量校验，避免把 `[通用]`、`[个性化]`、`[条件启用]`、生成参数、初始化说明或散落的 `待确认` 交付给实际项目。
---

# PM Harness 工程初始化技能

## 目标

基于 `assets/pm-harness-template/` 生成一个可直接进入开发协作的 harness 工程，而不是交付一份半成品模板。生成结果应该让人和 AI 都能快速理解：

- 项目是什么，面向谁，核心能力是什么。
- 当前实际启用了哪些端、服务、数据库、对象存储、算法、Agent 工具和治理流程。
- 任务开始前读哪些文件，改完后如何验证。
- 哪些信息确实还未决策，以及这些未决策项集中在哪里。

## 资产

执行时必须使用这些资产，不得从零捏造核心结构：

| 路径 | 用途 |
|---|---|
| `assets/pm-harness-template/` | 工程模板、文档、规则、脚本、Agent 命令事实源 |
| `assets/templates/` | 需求和 Bug 记录模板 |
| `references/user-input-schema.md` | 顺序化输入、默认值、冲突处理和派生规则 |
| `references/agent-tool-mapping.md` | Agent 工具目录和命令同步规则 |
| `references/default-command-catalog.md` | 默认命令族和条件启用规则 |

## 必读引用

在收集输入或生成工程前，完整读取：

1. `references/user-input-schema.md`
2. `references/agent-tool-mapping.md`
3. `references/default-command-catalog.md`

## 执行流程

### 1. 收集输入

严格按 `user-input-schema.md` 的 16 个输入步骤收集或确认用户输入。用户一次性提供的信息可以复用，但不得跳过仍缺失的必填项。

完成输入后，先输出推导配置摘要，覆盖产品定位、产品范围、技术方案、Agent 工具、UI 设计来源、自动派生项和关键未决策项。用户未回复时，可按已收集信息和派生默认继续生成。

### 2. 派生变量

按 schema 派生所有内部变量。固定目录、默认治理流程、Docker Compose、本地测试命令、OpenSpec、需求/Bug/Sprint 治理等由 Skill 自动派生，不再追问用户。

未知信息按以下规则处理：

- 阻塞运行、治理或安全的未知项进入 `docs/pending-decisions.md`。
- 不阻塞初始化的细节不写入正文占位，后续有信息再补充。
- 不得在 README、AGENTS、`project.yaml`、`openspec/config.yaml` 中批量散落 `待确认`。
- 不得用 `待确认` 作为 YAML 布尔值、路径、命令、端口或必需配置。

### 3. 构建工程目录

1. 复制 `assets/pm-harness-template/` 到输出目录 `{PRODUCT_CODE}/`。
2. 根据产品形态、对象存储、本地模型、数据库、Agent 工具等能力裁剪目录和文件。
3. 根据 `agent-tool-mapping.md` 只生成用户启用的 Agent 工具目录；未启用的 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 不得保留。
4. 创建必要空目录并用 `.gitkeep` 保留。
5. 渲染模板中的产品名、项目编号、技术栈、命令、目录、服务、文档索引和规则入口。

### 4. 生成项目化文档

生成文档时遵守交付层规则：

- 删除所有模板模块标记：`[通用]`、`[个性化]`、`[条件启用]`、`【通用】`、`【个性化】`、`【条件启用】`。
- 删除模板说明章节：模块标记说明、生成参数、初始化参数、初始化占位符、初始化生成建议、生成与维护原则、模板模块构成。
- 删除 `template_scope`、`抽象模板`、`Token 优化模板`、`可作为工程初始化` 等模板元信息。
- 删除全行或整表都是 `待确认` 的内容。
- 删除未启用能力的章节、表格行、目录、测试矩阵和强制规则。
- 将确实需要后续确认的少量事项集中到 `docs/pending-decisions.md`，并标明影响范围、建议默认值和何时必须决策。

关键文件的职责：

- `AGENTS.md`：只保留 AI 执行入口、读取路由、红线、目录边界、验证和回复要求；不得保留占位符表或模板生成说明。
- `README.md`：只保留项目简介、快速启动、目录导航、常用命令和文档入口；不得保留生成参数表。
- `project.yaml`：作为结构化事实源，布尔值必须是 true/false，未启用能力应为 `enabled: false` 或删除强制字段。
- `openspec/config.yaml`：必须是可解析 YAML，路径和命令应来自实际目录/脚本；未知命令删除或集中记录，不写 `"待确认"`。
- `docs/` 和 `rules/`：面向实际项目维护，不写模板自述。

### 5. 交付质量校验

打包前必须在输出项目根目录运行：

```bash
python scripts/validate-directory-structure.py
python scripts/validate-generated-docs.py --strict
```

`validate-generated-docs.py --strict` 必须通过后才能打包。失败时按错误修正文档和配置，不要把错误解释为“可后续人工处理”。

### 6. 打包输出

```bash
cd /home/claude/output
zip -r {PRODUCT_CODE}-harness.zip {PRODUCT_CODE}/ \
  --exclude "*/.DS_Store" \
  --exclude "*/__pycache__/*" \
  --exclude "*/.pytest_cache/*"
cp {PRODUCT_CODE}-harness.zip /mnt/user-data/outputs/
```

然后用 `present_files` 展示 zip。

## 输出检查清单

打包前确认：

```text
□ README.md 不含生成参数、模块标记或散落待确认
□ AGENTS.md 不含模板说明、占位符表或模块构成表
□ project.yaml / openspec/config.yaml 中无待确认布尔值、路径、命令
□ docs/ 与 rules/ 不含 [通用] / [个性化] / [条件启用]
□ 未启用端、服务、对象存储、算法、Agent 工具已裁剪
□ 关键未决策项集中到 docs/pending-decisions.md
□ validate-directory-structure.py 通过
□ validate-generated-docs.py --strict 通过
```
