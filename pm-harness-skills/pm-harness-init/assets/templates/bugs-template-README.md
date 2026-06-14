---
purpose: Bug 模板说明
content: 说明如何使用本模板创建规范的 Bug 记录
source: pm-harness 项目模板
update_method: 模板规范变化时更新
note: 适用于所有 pm-harness 项目
---

# Bug 模板使用说明

## 如何使用

1. 复制本 `template/` 目录到 `issues/bugs/BUG-xxxx-bug描述/`
2. 按照每个文件说明填写内容
3. 执行 `/bug-to-change BUG-xxxx` 生成 OpenSpec Fix Change

## 命名规范

```
BUG-0001-login-crash/        ✅ 正确：序号 + 英文简述
BUG-0002-upload-failed/      ✅ 正确
bug-login/                   ❌ 错误：缺少序号前缀
```

## 目录结构

```
BUG-xxxx-name/
├── bug.md            # Bug 描述（现象、复现步骤、期望行为）
├── root-cause.md     # 根因分析
├── workaround.md     # 临时解决方案
├── acceptance.md     # 修复验收标准
├── trace.md          # 关联 OpenSpec Fix Change、迭代
├── logs/             # 相关日志（.gitkeep 占位）
└── screenshots/      # 截图（.gitkeep 占位）
```

## 处理流程

```
1. 创建 issues/bugs/BUG-xxxx-name/
2. 填写 bug.md（必须）
3. 执行 /bug-to-change BUG-xxxx 生成 fix-* change
4. 执行 /opsx-apply fix-xxxx 修复
5. 执行 /opsx-archive fix-xxxx 归档
6. 如有知识沉淀价值，更新 docs/knowledge-base/incidents/
```
