---
purpose: 安全治理规范
content: 敏感信息、真实环境文件、运行时数据、Git 安全检测和公开输出边界
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# 安全治理规范

## Git 安全门禁

提交或推送前 SHOULD 运行：

```bash
python scripts/git-check.py
```

深度复核可运行：

```bash
python scripts/git-check.py --all
```

`/git-check` 默认扫描 staged + tracked 文件，发现下列内容时 MUST 阻断：

- 真实 `.env`、部署 env、构建 env。
- 运行时数据库、对象存储数据、临时目录和构建产物。
- 密钥、Token、Authorization、Cookie、数据库连接串、对象存储凭据。
- 本机绝对路径和疑似隐私路径。
- 超过阈值的大型二进制产物。

`.env.example`、占位符、localhost、示例域名和 `change-me` 类值不得仅因关键词命中而阻断。

## 输出边界

安全扫描和治理日志 MUST 脱敏输出，不得贴出真实密钥、连接串、Authorization header、Cookie、真实客户数据或本机绝对路径原文。

## AI 禁止行为

AI 不得自动删除本地文件、自动 unstage、自动修改 `.gitignore` 来掩盖风险，也不得把真实 env 内容写入 OpenSpec、Sprint、release、学习报告或最终回复。
