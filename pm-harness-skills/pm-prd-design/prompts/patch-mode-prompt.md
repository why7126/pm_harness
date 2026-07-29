# Patch Mode Prompt — PATCH_PRD_DESIGN

## 角色

你现在做的是**小版本补丁**，不是重新设计。类比工程里的 hotfix：改动面越小越好，任何"顺便"都是风险。这是三种模式里约束最强的一种——默认姿态是拒绝改动,只有 `patch-request.md` 白纸黑字写出来的项才能动。

## 输入前提

- `source.zip`：上一版完整交付包，必须以此为唯一基线
- `patch-request.md`：用 `templates/patch-request-template.md` 结构，明确列出：
  - `Version`：基于哪个版本打补丁
  - `Only Modify`：仅允许修改的项，逐条列出
  - `Forbidden Changes`：显式禁止的改动（可选，用户特别强调时填）
  - `Keep`：需要特别强调保留的部分（可选）

如果 `patch-request.md` 里的"Only Modify"条目描述模糊（比如"优化一下按钮"而没说清楚是哪个页面的哪个按钮、改什么），先向用户确认具体范围,不要自己扩大解释。

## 最高优先级：保留原版本

在开始任何修改之前，先明确一件事：**除了 `Only Modify` 里列出的项，其余一切原样保留**——包括但不限于：

- 布局结构（不重排、不调整栅格、不改页面区块顺序）
- 信息架构（不新增/删除/合并导航层级）
- 设计系统（不改配色、字体、间距、圆角、阴影等任何 token）
- 组件（不替换组件样式、不新增未被要求的组件、不删除现有组件）
- 未被提及区域的文案、交互、状态逻辑

## 执行步骤

1. 从 `source.zip` 取出上一版的 `requirement.md`、`interaction.md`、`prototype.html`、`prototype-context.md`、`version-manifest.md`，作为唯一基线，逐字理解现状。

2. 把 `patch-request.md` 的"Only Modify"逐条对照到具体文件、具体位置——明确"这一条对应 `prototype.html` 里的哪个 DOM 节点/哪个页面的哪个组件"。

3. 只对这些精确定位到的位置做最小化修改，其余内容**逐字节保持不变**（`prototype.html` 里没被要求改的部分，直接原样复制，不要因为"顺手重新生成"导致细微差异）。

4. 修改完成后，生成：
   - 更新后的完整文件集（`requirement.md` / `interaction.md` / `prototype.html` / `prototype-context.md`）
   - `change-log.md`：只记录本次 patch 的改动点，一条一句话
   - `diff-report.md`：逐项列出改动前后的对比（字段级/属性级颗粒度）
   - `version-manifest.md`：修订号 +1（如 `1.1.0` → `1.1.1`），稳定区填绝大部分内容（未改动的），变更区只填本次 patch 涉及的项

5. **跑范围校验**（不能跳过）：读 `validators/patch-scope-validator.md`，逐条核对最终 diff 是否精确等于 `patch-request.md` 里的"Only Modify"清单——多一条都不行,少一条说明遗漏了用户的诉求，也要修正。

## 禁止事项（重复强调，因为这是最容易破坏的约束）

不要：

- 重新设计布局
- 更换设计系统
- 新增本次未被要求的组件
- "顺便"优化未被提及的区域，即便你判断那里确实有问题

发现明显缺陷但不在本次授权范围内时，在交付说明里如实指出，并建议用户另开一次 `ITERATE_PRD_DESIGN`，把决定权交还给用户。
