# Patch Scope Validator

仅用于 `PATCH_PRD_DESIGN` 模式。核对最终产出的改动，与 `patch-request.md` 中"Only Modify"清单是否**完全对应**——既不能有遗漏，也不能有越界。这是 PATCH 模式独有的、比常规回归校验更严格的一道关卡。

## 校验方法

1. 把 `diff-report.md` 中列出的每一项改动，逐条对照到 `patch-request.md` 的"Only Modify"清单：
   - [ ] 每一条实际改动，都能在"Only Modify"清单里找到对应条目（没有越界改动）
   - [ ] "Only Modify"清单里的每一条，都能在实际改动中找到落地（没有遗漏用户的诉求）

2. 检查是否触碰了 `patch-request.md` 中"Forbidden Changes"（如有填写）列出的项：
   - [ ] 没有任何改动落在"Forbidden Changes"范围内

3. 检查"Keep"（如有填写）中特别强调要保留的部分：
   - [ ] 这些部分在最终产出中确实原样保留

4. 抽查未被列入"Only Modify"的相邻区域（例如同一页面的其他模块），确认没有被"顺带"改动：
   - [ ] 相邻但未授权的区域逐字节/逐属性对比与上一版一致

## 判定

- 存在越界改动（不在"Only Modify"里，也不在明确沟通后的补充授权里）→ 不通过，必须撤销该改动
- 存在遗漏（"Only Modify"里要求的项没有落地）→ 不通过，必须补齐
- 触碰了"Forbidden Changes"→ 不通过，必须撤销
- 全部对应且无越界 → 通过，可以进入打包环节
