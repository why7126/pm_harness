---
name: "miniapp-env"
description: "切换微信小程序 API 环境策略：dev、prod、auto"
---

# miniapp-env

Use this skill when the user asks `/miniapp-env <dev|prod|auto>` or wants to switch the WeChat miniapp API environment.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；先定位再分段读取，避免全量展开无关目录。
- 只读取小程序环境相关文件、脚本和必要规则；不要默认读取全部 docs、issues、iterations 或 archive。

## Input

- `dev`：开发版使用本地 API。
- `prod`：体验版、提审或正式发布前使用生产 API。
- `auto`：开发版使用本地，体验版和正式版使用生产。

DevTools URL 校验随策略同步：

- `dev` / `auto` SHOULD 将小程序 `project.private.config.json` 的 `setting.urlCheck` 设为 `false`，避免本地 HTTP API 被微信开发者工具拦截。
- `prod` SHOULD 将 `setting.urlCheck` 设为 `true`，用于体验版、提审和正式发布前验证生产合法域名。

## Must Read

```text
rules/coding.md
rules/testing.md
rules/directory-structure.md
rules/agent-context-budget.md
```

按实际目录读取存在的文件：

```text
src/wechat-miniapp/README.md
src/wechat-miniapp/project.private.config.json
src/miniapp/README.md
src/miniapp/project.private.config.json
scripts/miniapp-env.py
```

## Steps

1. 确认参数为 `dev`、`prod` 或 `auto`；缺失时询问用户目标策略。
2. 若 `scripts/miniapp-env.py` 存在，执行：

```bash
python scripts/miniapp-env.py set <strategy>
```

3. 若脚本不存在，按项目实际小程序目录检查并报告需要接入的环境切换脚本，不手写散落配置。
4. 若小程序静态测试存在，执行项目已有测试命令，例如：

```bash
uv run pytest tests/test_miniapp_static.py
```

5. 输出当前策略、`project.private.config.json setting.urlCheck`、修改文件、测试结果和下一步建议。

## Output

说明是否影响 API、数据库、Web、小程序、管理端；是否需要客户端生成；是否需要 Docker Compose 验证；是否补充或更新测试；遵循了哪些 `rules/` 文件。
