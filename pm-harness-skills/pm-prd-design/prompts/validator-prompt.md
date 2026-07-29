# Validator Prompt

在打包 `package.zip` 交付之前，按顺序执行以下校验。这是生成流程的最后一道关卡，目的是把"我觉得应该没问题"变成"我逐项核对过"。任一项不通过，回到生成步骤修正后重新校验，不要带着已知问题交付。

## 执行顺序

### 1. 包完整性校验（全部模式必跑）

读 `validators/package-validator.md`，核对本次应产出的文件是否齐全、是否为空文件、内容是否互相引用一致（例如 `prototype-context.md` 提到的组件在 `prototype.html` 里确实存在）。

### 2. 回归校验（ITERATE / PATCH 模式必跑，CREATE 模式跳过）

读 `validators/regression-validator.md`，对比本版本与上一版本（来自 `source.zip`），确认未被本次请求覆盖的区域——布局、组件、设计系统 token、关键交互流程——没有发生非预期变化。把结果写入 `regression-report.md`：每一项标注"未变化 / 已按要求变化 / 意外变化"，如有"意外变化"必须回去修正，不能带着交付。

### 3. 补丁范围校验（仅 PATCH 模式必跑）

读 `validators/patch-scope-validator.md`，把最终 diff 与 `patch-request.md` 的"Only Modify"清单逐条比对，确认二者完全对应——没有遗漏，也没有越界。

## 校验结论怎么用

- 三项校验（或适用的子集）全部通过后，才能生成/更新 `package.zip`
- 校验发现的问题，修正后必须重新跑一遍相关校验，不能只修正不复查
- 在最终交付说明中，用一两句话向用户汇报校验结果（例如："已完成回归校验，除本次要求的两处改动外，其余页面与上一版本一致"），让用户对改动范围有明确认知
