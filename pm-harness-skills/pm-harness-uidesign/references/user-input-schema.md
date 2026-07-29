# UI Design Extraction User Input Schema

## 目标

用于收集 `pm-harness-uidesign` 执行真实项目 UI/UE 提炼所需输入。原则是先拿到代码事实源，再使用辅助材料提升保真度。

## 必填输入

必须至少提供一个代码事实源。

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `source.local_repo_path` | path | 条件必填 | `/path/to/local/project` | 本地项目代码库目录，私有项目首选 |
| `source.github_repo_url` | url | 条件必填 | `https://github.com/org/repo` | GitHub 代码库链接，可配合 branch/commit/subpath |
| `source.local_archive_path` | path | 条件必填 | `/tmp/app.zip` | 本地代码压缩包，支持 `.zip`、`.tar.gz`、`.tgz` |

三者至少提供一个。优先级建议：

1. `source.local_repo_path`
2. `source.github_repo_url`
3. `source.local_archive_path`

## 源码定位输入

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `source.branch` | string | 否 | `main` | GitHub 或本地 Git 分支 |
| `source.commit` | string | 否 | `a1b2c3d` | 固定提炼版本，提升可追溯性 |
| `source.tag` | string | 否 | `v1.4.0` | 发布版本 |
| `source.pr_url` | url | 否 | `https://github.com/org/repo/pull/12` | 从 PR 状态提炼时使用 |
| `source.monorepo_app_path` | path | 否 | `apps/admin` | monorepo 中的目标应用路径 |

如果用户同时提供 branch、commit 和 tag，以 commit 为最高优先级，并在交付说明中记录。

## 输出定位输入

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `scheme.scheme_id` | string | 否 | 从项目名派生 | 方案目录名，使用小写字母、数字和连字符 |
| `scheme.scheme_name` | string | 否 | 从项目名派生 | 展示名称 |
| `scheme.output_root` | path | 否 | `design-schemes/` | 设计资产库根目录 |
| `scheme.update_existing_path` | path | 否 | 空 | 已有方案目录，用于增量更新 |
| `scheme.category` | enum | 否 | 自动判断 | `dashboard`、`saas`、`ecommerce`、`mobile`、`landing`、`other` |

如果是更新已有方案，优先复用已有 `scheme_id`，不要无故创建新目录。

## 产品上下文输入

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `product.name` | string | 否 | `TilesFST` | 产品名称 |
| `product.domain` | string | 否 | `家居建材资料库` | 业务领域 |
| `product.target_users` | string/list | 否 | `后台运营、门店导购` | 目标用户 |
| `product.reuse_goal` | string | 否 | `用于新后台初始化` | 复用目标 |
| `product.platforms` | list | 否 | `web admin, miniapp` | 平台或端 |

这些信息用于 `meta.json`、`ui-design.md` 和 demo 文案，不应覆盖源码事实。

## 关键页面输入

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `pages.key_pages` | list | 否 | `login,dashboard,sku list` | 要重点提炼的页面 |
| `pages.admin_layout_path` | path | 否 | `src/web/src/pages/admin/AdminLayout.tsx` | 用户已知后台布局入口 |
| `pages.navigation_paths` | list | 否 | `AdminSidebar.tsx,admin-nav.ts` | 用户已知导航入口 |
| `pages.style_paths` | list | 否 | `globals.css,tokens.ts` | 用户已知设计事实源 |

如果用户不知道这些路径，执行者必须自行扫描。

## 辅助材料输入

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `support.screenshot_dir` | path | 否 | `/tmp/screenshots` | 辅助校验视觉效果 |
| `support.figma_url` | url | 否 | `https://figma.com/...` | 辅助理解设计意图 |
| `support.design_doc_path` | path | 否 | `rules/ui-design.md` | 设计说明或品牌规范 |
| `support.preview_url` | url | 否 | `http://localhost:3000` | 本地预览地址 |
| `support.brand_assets_path` | path | 否 | `assets/brand` | Logo、字体、图片等 |

辅助材料和源码冲突时，以源码为准，并在交付说明中记录冲突。

## 必须保留细节输入

| 字段 | 类型 | 必填 | 示例 | 说明 |
|---|---|---:|---|---|
| `preserve.details` | list | 否 | `sidebar collapse, version badge, user menu chevron` | 用户强调不能丢的细节 |
| `preserve.navigation_required` | boolean | 否 | `true` | 是否强制拆出导航资产 |
| `preserve.demo_interactions` | list | 否 | `sidebar expand/collapse` | demo 必须模拟的交互 |
| `preserve.compare_to_real_project` | boolean | 否 | `true` | 是否强调高保真对照源码 |

用户反馈 demo 不一致时，应把反馈转化为 `preserve.details`，并回查所有资产。

## 冲突处理

- 没有代码事实源：停止提炼，要求补充本地目录、GitHub 链接或代码压缩包。
- 本地路径不可读：说明路径问题，要求修正或换 GitHub/压缩包。
- GitHub 无法访问：请求本地 checkout 或压缩包。
- 压缩包无法解压：要求重新提供可读压缩包或本地目录。
- 多个源码输入冲突：以用户指定的优先级为准；未指定时按本地目录、GitHub、压缩包排序。
- 辅助材料和源码冲突：源码优先，交付说明中写明冲突。

## 最小可执行输入示例

```yaml
source:
  local_repo_path: /path/to/local/project
product:
  name: TilesFST
preserve:
  details:
    - sidebar collapse
    - version badge
    - user menu chevron
```

## 完整输入示例

```yaml
source:
  github_repo_url: https://github.com/org/app
  branch: main
  monorepo_app_path: apps/admin
scheme:
  scheme_id: app-admin
  scheme_name: App Admin UI
  output_root: design-schemes
product:
  name: App
  domain: B2B catalog
  target_users:
    - admin operator
    - sales manager
  reuse_goal: existing project refactor
  platforms:
    - web admin
pages:
  key_pages:
    - login
    - dashboard
    - product list
support:
  preview_url: http://localhost:3000
  screenshot_dir: /tmp/app-screenshots
preserve:
  navigation_required: true
  demo_interactions:
    - sidebar expand/collapse
```
