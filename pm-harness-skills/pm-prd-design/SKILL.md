---
name: pm-prd-design
description: 面向企业级产品的 PRD 需求文档与产品原型设计工程化生成技能。当用户要求"写 PRD"、"出需求文档"、"做产品原型"、"设计交互稿"、"迭代/优化现有产品设计"、"给已有原型打补丁/小改一个点"、"生成设计交付包"，或提供 product-context / ui-design / page-request / iteration-request / patch-request 等材料并希望得到 requirement.md、interaction.md、prototype.html 等交付物时，必须触发此 Skill。同样适用于"在不改动整体布局和设计系统的前提下只改某个字段/按钮/文案"这类小版本补丁请求，以及"帮我看看这版原型和上一版比改了哪些地方"这类回归/差异校验请求。即使用户没有直接说"PRD"或"Skill"这两个词，只要诉求是产出可交付的产品需求 + 交互原型工程包，就应使用本技能。
---

# PM PRD & Design Engineering Skill

一名资深企业产品经理 + 交互设计师的工作流封装：把"需求 → 交互 → 可点击原型 → 版本化交付包"这条链路，变成一套可重复执行、可校验、可增量演进的工程流程，而不是一次性的自由发挥。

## 为什么要工程化

产品设计交付物最容易出的问题不是"不够漂亮"，而是**不稳定**：同一个产品迭代两次，风格全变了；改一个按钮文案,整个页面布局跟着重排；这一版和上一版之间说不清改了什么。本技能的核心价值就是对抗这种不稳定性，用显式的原则、模板和校验器，把"这次改动是否在授权范围内"这件事变成可以检查的事实，而不是靠印象判断。

## 四条核心原则（贯穿所有模式）

1. **设计资产优先（Design Asset First）**：任何输出都必须先有依据——已确认的设计系统（色板/字体/间距/组件库）、既有页面结构、明确的信息架构，而不是临场发挥出一套新风格。没有 `ui-design.md` 或可复用的既有原型时，先向用户确认设计基调，不要自行假设。
2. **先保留、后改进（Preserve Before Improve）**：迭代或打补丁时，默认"能不动就不动"。改动必须能追溯到用户的明确诉求；顺手做的"优化"是被禁止的，即使它看起来更好——参见下方 PATCH 模式的强约束。
3. **工程可交付（Engineering Deliverable）**：输出不是聊天里的一段描述，而是一组结构化文件（见下方"输出文件清单"），每个文件都有固定用途，缺一不可,并且要打包为 `package.zip`。
4. **版本受控演进（Version Controlled Evolution）**：每一次 CREATE / ITERATE / PATCH 都要落地为一份 `version-manifest.md`，明确记录本版本相对上一版的稳定区（stable area）和变更区（modified area），为下一次迭代提供依据。

## 工作流程总览

```
识别模式 → 收集必需输入 → 加载对应 prompt → 生成交付物 → 跑质量门禁校验 → 打包 package.zip → 交付
```

### 第一步：识别模式

先检查用户消息里是否包含下面的**显式触发词**（不区分大小写，允许出现在消息开头或独立一行，后面可以直接跟具体诉求）：

| 触发词 | 直接进入模式 |
|---|---|
| `CREATE:` / `CREATE_PRD_DESIGN:` | `CREATE_PRD_DESIGN` |
| `ITERATE:` / `ITERATE_PRD_DESIGN:` | `ITERATE_PRD_DESIGN` |
| `PATCH:` / `PATCH_PRD_DESIGN:` | `PATCH_PRD_DESIGN` |

**命中显式触发词 → 跳过下面的意图识别，直接按该模式走**，不再反问"这是新建还是迭代"。触发词只决定"走哪个模式"，不能替代必需输入——该模式要求的材料（见第二步）缺失时仍要照常引导用户补齐，不能因为用户显式指定了模式就放松材料校验。

若显式触发词与随后描述的诉求明显矛盾（例如打了 `PATCH:` 但诉求其实是"整体重新设计"），不要生硬地按字面模式执行，向用户确认一下更合适：*"你标了 PATCH，但这个改动看起来影响面比较大，要不要按 ITERATE 来做？"*——确认后再继续。

**没有显式触发词时**，走意图识别：根据用户诉求和已提供的材料判断进入哪个模式，三选一：

| 信号 | 模式 |
|---|---|
| 从零开始做一个新产品/新页面的需求与原型 | `CREATE_PRD_DESIGN` |
| 已有产品设计资产，想整体优化、加功能、调整交互 | `ITERATE_PRD_DESIGN` |
| 已有版本，只想改一两个明确的点，其余必须原样保留 | `PATCH_PRD_DESIGN` |

拿不准时，直接问用户："这是全新设计，还是在现有版本上迭代/打补丁？"——不要替用户假设成影响范围最大的那个模式。

### 第二步：收集必需输入

三个模式各自要求不同的输入文件，见下表。用户没有提供某项时，主动追问或引导其用对应模板（`templates/`）补齐；**不要在缺少必填项的情况下强行生成**，这会导致产出没有依据。

| 模式 | 必需输入 | 对应模板 |
|---|---|---|
| CREATE_PRD_DESIGN | `product-context.md`（产品定位/目标用户/核心场景）、`ui-design.md`（设计系统：色板/字体/间距/组件规范）、`page-request.md`（要做哪些页面及其功能点） | `templates/product-context-template.md`、`templates/ui-design-template.md`、`templates/page-request-template.md`。用户若无 `ui-design.md`，可先用 `/mnt/skills/public/frontend-design/SKILL.md` 的方法帮其确立设计基调，再落成文档 |
| ITERATE_PRD_DESIGN | `source.zip`（上一版完整交付包）或既有设计文件、`iteration-request.md`（本次要改进/新增什么） | `templates/change-request-template.md` |
| PATCH_PRD_DESIGN | `source.zip`（上一版完整交付包）、`patch-request.md`（仅列出要改的点） | `templates/patch-request-template.md` |

### 第三步：加载对应 prompt 并生成交付物

打开对应的 prompt 文件，按其中的角色设定和步骤执行：

- CREATE 模式 → 读 `prompts/create-mode-prompt.md`
- ITERATE 模式 → 读 `prompts/iteration-mode-prompt.md`
- PATCH 模式 → 读 `prompts/patch-mode-prompt.md`

生成 `prototype.html` 时，这是一个**可以在浏览器中直接打开、可点击交互的高保真原型**，不是静态效果图描述。写 HTML/CSS 时应用 `/mnt/skills/public/frontend-design/SKILL.md` 的设计原则（避免模板化默认风格、有意识的字体和配色决策），但前提是不能违反本技能的"先保留、后改进"原则——ITERATE/PATCH 模式下，设计系统以 `ui-design.md` 或既有原型为准，不能借口"更美观"重新发挥。

`prototype.png` 是 `prototype.html` 在标准视口下的静态截图，用于快速预览和存档，不能与 html 内容不一致。

### 第四步：质量门禁校验

生成完毕后，必须过一遍质量门禁，不要跳过：读 `prompts/validator-prompt.md`，依次执行：

1. `validators/package-validator.md` — 检查交付包文件是否齐全
2. `validators/regression-validator.md` — 检查布局/组件/设计系统/关键流程是否有非预期改动（ITERATE/PATCH 模式必跑）
3. `validators/patch-scope-validator.md` — 检查是否只改了 `patch-request.md` 里明确列出的项（仅 PATCH 模式）

任一校验不通过，回到第三步修正，不要带着已知问题打包交付。校验结果写入 `regression-report.md`（ITERATE/PATCH）与/或在交付说明中简要汇报。

### 第五步：打包并交付

将本轮所有产出文件打包为 `package.zip`，并同步更新 `version-manifest.md`（用 `templates/version-manifest-template.md`，字段定义见 `schemas/version-manifest-schema.yaml`）。CREATE 模式从 v1.0.0 起版；ITERATE 模式次版本号 +1（如 1.0.0 → 1.1.0）；PATCH 模式修订号 +1（如 1.1.0 → 1.1.1）。

## 输出文件清单

| 文件 | 说明 | 何时产出 |
|---|---|---|
| `requirement.md` | PRD 需求文档：背景、目标用户、用户故事、功能清单、验收标准 | 全部模式（ITERATE/PATCH 为更新版） |
| `interaction.md` | 交互说明：页面流程、状态、交互细节、异常态/空态处理 | 全部模式 |
| `prototype.html` | 可点击高保真原型，单文件（CSS/JS 内联） | 全部模式 |
| `prototype-context.md` | 原型使用的组件、数据字段、跳转关系说明，供工程团队参照实现 | 全部模式 |
| `prototype.png` | 原型静态截图 | 全部模式 |
| `version-manifest.md` | 版本清单：版本号、设计系统版本、页面/组件清单、稳定区/变更区 | 全部模式 |
| `change-log.md` | 本版本相对上一版的变更说明（人类可读） | ITERATE / PATCH |
| `diff-report.md` | 逐项差异清单（结构化，便于比对） | ITERATE / PATCH |
| `regression-report.md` | 回归校验结果 | ITERATE / PATCH |
| `package.zip` | 以上全部文件的打包压缩包 | 全部模式 |

对应结构化定义见 `schemas/output-schema.yaml`；三种模式的输入结构化定义见 `schemas/input-schema.yaml`。

## PATCH 模式的强约束（最容易出错的地方）

PATCH 是三种模式里唯一"默认拒绝改动"的模式。收到 patch 请求后：

- **只做** `patch-request.md` 中"Only Modify"列出的项。
- **禁止**：重排布局、调整信息架构、更换或新增设计系统 token（颜色/字体/间距）、替换或新增组件、顺带"优化"未提及的区域——哪怕你认为它有问题。
- 如果发现未被要求修改的地方存在明显缺陷，**在交付说明里指出并询问用户是否需要另开一次 ITERATE**，而不是自己动手改掉。
- 生成后必须跑 `validators/patch-scope-validator.md`，逐条核对 diff 是否越界。

## 边界情况

- **用户只给了零散截图/文字描述，没有走模板**：仍然可以工作，但要主动把这些信息归纳进对应模板结构里（在回复中或生成的 `.md` 文件中），避免关键信息（目标用户、验收标准、设计系统)缺失。
- **用户要求的改动会明显破坏既有设计系统一致性**（比如在 PATCH 模式里要求换整体配色）：如实告知这已超出 PATCH 范围，建议走 ITERATE，或在用户坚持的情况下确认后再执行并如实记录进 `change-log.md`。
- **source.zip 缺失但用户说"在之前生成的基础上改"**：先尝试从当前对话上下文中找回此前生成的文件；找不到时明确告知用户需要重新提供，不要凭空杜撰"上一版"的内容。
