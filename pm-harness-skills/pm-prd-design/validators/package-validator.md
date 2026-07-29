# Package Validator

检查交付包的文件是否齐全、是否有效。适用于全部三种模式，具体必需文件因模式而异。

## 必需文件（按模式）

### CREATE_PRD_DESIGN
- [ ] `requirement.md`
- [ ] `interaction.md`
- [ ] `prototype.html`
- [ ] `prototype-context.md`
- [ ] `prototype.png`
- [ ] `version-manifest.md`

### ITERATE_PRD_DESIGN（在上面基础上新增）
- [ ] `change-log.md`
- [ ] `diff-report.md`
- [ ] `regression-report.md`

### PATCH_PRD_DESIGN（同 ITERATE，文件清单一致，内容颗粒度更小）
- [ ] `change-log.md`
- [ ] `diff-report.md`
- [ ] `regression-report.md`

全部模式最终都要有：
- [ ] `package.zip`（包含以上全部文件）

## 内容有效性检查（不只是"文件存在"，还要"内容合格"）

- [ ] 没有空文件，没有只有模板占位符没填内容的文件
- [ ] `requirement.md` 中出现的每个功能点，在 `interaction.md` 里都能找到对应的交互说明
- [ ] `interaction.md` 中描述的每个交互，在 `prototype.html` 里都能实际点到/触发
- [ ] `prototype-context.md` 中列出的组件/字段，在 `prototype.html` 的实际 DOM 中确实存在
- [ ] `prototype.png` 与当前版本的 `prototype.html` 视觉一致（不是旧版本截图）
- [ ] `version-manifest.md` 的版本号符合本次操作的递增规则（CREATE 起 1.0.0；ITERATE 次版本号+1；PATCH 修订号+1）
- [ ] （ITERATE/PATCH）`diff-report.md` 中列出的改动项，在实际文件对比中都能验证到；没有列出的地方没有意外改动

## 判定

以上任一项未通过，视为本次校验不通过，需返回生成步骤修正，修正后重新执行本清单，直到全部通过再打包。
