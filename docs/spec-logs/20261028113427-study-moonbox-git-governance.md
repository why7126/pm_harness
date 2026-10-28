---
title: MoonBox Git 治理学习应用
created_at: 2026-10-28 11:34:27
updated_at: 2026-10-28 11:56:34
---

# MoonBox Git 治理学习应用

## 对象、模式与授权

学习对象 ProjectMoonBox；auto 模式，focus Git。用户确认 G1–G4、先扫描后同步技能，并同步脚手架模板。执行时间 2026-10-28 11:34:27（Asia/Shanghai）。Change `add-moonbox-git-governance`，Sprint `sprint-001`。本流程仅此一份 study 报告，不生成重复 governance 日志。

## 已采纳内容

- G1：按交付范围暂存和提交，保护已有 staged 内容，明确远端、历史与正式标签边界。
- G2：精确路径规则、正反例回归，不豁免整行或测试目录。
- G3：真实 env 忽略、示例可跟踪与 index 中真实 env 的双向门禁。
- G4：逐项告警复核和覆盖边界，不把退出零等同完全安全。

## 适配与补强

扫描 index blob 与 worktree 分开，--base/--history 检查提交树及消息并覆盖中间删除；浅克隆、冲突、链接、不可读与超限拒绝。诊断不输出内容行、部分凭证或 Git stderr。占位符完整匹配，URL 单独核验凭证，支持精确模板参数与安全默认值；Markdown 分隔符不成为值的一部分。

未采纳 MoonBox 自动优化授权、固定部署路径、广泛子串豁免、整行脱敏替换和无关浏览器长契约。未执行当前仓库提交、推送、打标签或改写历史。未修改学习对象。

## 文件与原因

- `.agents/skills/git-check/SKILL.md`：扫描范围、失败处理与脱敏契约。
- `.agents/skills/git-sync/SKILL.md`：授权范围内的提交同步契约。
- `.gitignore`：入口、规范、索引与模板生成说明同步。
- `AGENTS.md`：入口、规范、索引与模板生成说明同步。
- `README.md`：入口、规范、索引与模板生成说明同步。
- `docs/08-command-execution-order.md`：入口、规范、索引与模板生成说明同步。
- `docs/README.md`：入口、规范、索引与模板生成说明同步。
- `docs/standards/git-delivery-safety.md`：入口、规范、索引与模板生成说明同步。
- `iterations/change/sprint-001/acceptance-report.md`：纳入 sprint-001 并维护派生状态。
- `iterations/change/sprint-001/sprint.md`：纳入 sprint-001 并维护派生状态。
- `iterations/change/sprint-001/sprint.yaml`：纳入 sprint-001 并维护派生状态。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/.openspec.yaml`：治理 Change 的设计、任务、验收与追踪。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/design.md`：治理 Change 的设计、任务、验收与追踪。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/proposal.md`：治理 Change 的设计、任务、验收与追踪。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/specs/git-delivery-safety/spec.md`：治理 Change 的设计、任务、验收与追踪。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/tasks.md`：治理 Change 的设计、任务、验收与追踪。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/trace.md`：治理 Change 的设计、任务、验收与追踪。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/.agents/skills/git-check/SKILL.template.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/.agents/skills/git-sync/SKILL.template.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/.gitignore`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/AGENTS.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/README.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/docs/08-command-execution-order.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/docs/README.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/docs/standards/git-delivery-safety.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/project.yaml`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/rules/agent-context-budget.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/rules/security.md`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/scripts/git-check.py`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/scripts/test_git_check.py`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/scripts/validate-env-ignore-policy.py`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/scripts/validate-skill-package.py`：init 包镜像，与主模板一致。
- `pm-harness-skills/pm-harness-init/references/default-command-catalog.md`：入口、规范、索引与模板生成说明同步。
- `pm-harness/.agents/skills/git-check/SKILL.md`：可交付的新项目模板能力。
- `pm-harness/.agents/skills/git-sync/SKILL.md`：可交付的新项目模板能力。
- `pm-harness/.gitignore`：可交付的新项目模板能力。
- `pm-harness/AGENTS.md`：可交付的新项目模板能力。
- `pm-harness/README.md`：可交付的新项目模板能力。
- `pm-harness/docs/08-command-execution-order.md`：可交付的新项目模板能力。
- `pm-harness/docs/README.md`：可交付的新项目模板能力。
- `pm-harness/docs/standards/git-delivery-safety.md`：可交付的新项目模板能力。
- `pm-harness/project.yaml`：可交付的新项目模板能力。
- `pm-harness/rules/agent-context-budget.md`：可交付的新项目模板能力。
- `pm-harness/rules/security.md`：可交付的新项目模板能力。
- `pm-harness/scripts/git-check.py`：可交付的新项目模板能力。
- `pm-harness/scripts/test_git_check.py`：可交付的新项目模板能力。
- `pm-harness/scripts/validate-env-ignore-policy.py`：可交付的新项目模板能力。
- `pm-harness/scripts/validate-skill-package.py`：可交付的新项目模板能力。
- `rules/agent-context-budget.md`：入口、规范、索引与模板生成说明同步。
- `rules/security.md`：入口、规范、索引与模板生成说明同步。
- `scripts/git-check.py`：安全扫描、环境忽略或回归验证。
- `scripts/test_git_check.py`：安全扫描、环境忽略或回归验证。
- `scripts/validate-env-ignore-policy.py`：安全扫描、环境忽略或回归验证。

- `docs/spec-logs/20261028113427-study-moonbox-git-governance.md`：本次学习应用报告、验证映射或治理追踪补齐。
- `docs/spec-logs/CHANGELOG.md`：本次学习应用报告、验证映射或治理追踪补齐。
- `iterations/change/sprint-001/release-note.md`：本次学习应用报告、验证映射或治理追踪补齐。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/acceptance.md`：本次学习应用报告、验证映射或治理追踪补齐。
- `openspec/archive/2026-10-28-add-moonbox-git-governance/test-plan.md`：本次学习应用报告、验证映射或治理追踪补齐。
- `openspec/testing-mapping.md`：本次学习应用报告、验证映射或治理追踪补齐。

## 影响

API、DB schema、Web、小程序、管理端、Orval、Docker Compose 运行配置均无变更。测试仅在临时 Git 仓库执行。Git 检测依赖 Python 标准库和 Git，不引入外部依赖。包体上限由270调整为274，新增四份资产后实际271；保留唯一 SKILL.md 与缓存禁入门禁。

product_data_collection_observability: not_applicable
affected_layers: []
reason: 本地静态安全检查及命令契约，不新增产品采集或运行时观测。
validation: 临时 Git 回归与产品数据观测声明门禁。

## 验证

- `PYTHONDONTWRITEBYTECODE=1 python scripts/test_git_check.py`：15项通过，覆盖实际 index、worktree、历史删除、消息、浅克隆、冲突、占位符、无内容输出、env 双向策略、特殊文件名、链接、超限和解码失败。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过，271份文件。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- `openspec validate add-moonbox-git-governance`：通过。
- Sprint 选择、聚焦 scope、观测声明与文档卫生检查：通过。
- `git diff --check`：通过。
- 全仓 git-check：返回1，保留既有阻断。完整轮次后补充 Compose 引用语法回归并通过15项测试；最终受跟踪工作区复核仅余2处本机路径与3份 .env.docker 路径，旧 index 仍包含未暂存修正前快照。未执行真实待推送历史检查。

## 既有边界与安装状态

原有三份已跟踪 .env.docker 不因 ignore 自动解除风险；不自动移出索引或修改这些文件。主模板既存 Finder 缓存已完整移至仓库外受控临时目录，未删除，实际路径只保留在本机会话。根目录两份既存同步冲突缓存未动。未发现本机 pm-harness-init 安装版，已同步仓库源码和 init 内嵌资产，不创建猜测的个人目录。

## 学习对象只读保护

只使用文件读取及 git --no-optional-locks status；未运行对象脚本、安装、测试或 Git 写命令。起始状态231条，状态摘要为 6d833d9a6504a533246609c8e5f22d36eacbb8dc45cea5bb780a16c0169fa747；收尾核对仍为231条且摘要相同；未对学习对象路径执行写入。不将状态摘要当成所有文件内容哈希。

## 工作流与后续

Workflow Sync 已成功解析 sprint-001，opsx.apply 无错误；AI Usage Hook 已执行，usage_mode 为 unavailable，缺可归因 token 事件，不伪造用量，保留非阻断 warning。未自动创建 follow-up Issue/Change。Git 同步需另行用户授权，并先处理全仓安全门禁命中；本次交付仅新增能力，不替用户提交推送。

## 归档收尾

2026-10-28 11:46:43：用户授权归档，OpenSpec CLI 同步4条正式要求，目录已规范化到 `openspec/archive/2026-10-28-add-moonbox-git-governance`，未留下 legacy archive 目录。Workflow Sync 解析 sprint-001，0错误；Issue promote 为0项，纯治理变更。AI Usage Hook 已调用，缺实际用量时保留 unavailable，不影响归档完成。


## Git 阻断处置复核

用户授权处置默认扫描的 17 项阻断，保留本地 env，不提交或推送。root_cause_status: confirmed；证据为 index 与工作区逐项比对，以及默认扫描来源、规则与行号。

- 真实隐私风险：AGENTS.md 的 index 及观测治理 design.md 两个来源保留个人目录，共 3 项。改用用户目录占位符；AGENTS.md 只更新 index 的对应路径，保留其他未暂存变更。
- 可移植性问题而非个人凭证：init 技能打包命令的固定环境路径命中两个来源，共 2 项。改用显式输出目录变量并在缺失时停止命令。
- 扫描器源码的语义误报：三份旧 index 扫描器含固定环境示例白名单，共 3 项。工作区已有治理版本移除此白名单，更新三份 index 及 env 校验依赖、回归测试，不新增豁免或放宽规则。
- 环境文件跟踪风险：三份 backend/.env.docker 在 index、worktree、env-policy 重复命中，共 9 项。内容启发式未命中凭证，不据此证明不存在秘密；仅取消 Git 跟踪，保留本地字节，沿用现有 env 忽略规则和 .env.example。

本轮未改变扫描规则或业务行为，仅修正文档路径并将已有治理修复反映到 index，属于非行为性小修，不新建 Change，不修改正式 specs。沿用本报告记录补充修正，未创建 Issue。安装版 pm-harness-init 经实际路径检查未安装，不创建目录。

product_data_collection_observability: not_applicable；affected_layers: []；reason: 仅文档脱敏与 Git 跟踪处置，无产品采集链路变更；validation: 默认安全检查、env 保全核验和治理校验。API/DB/Web/小程序/管理端/Orval 无影响；Docker 本地 env 保留，示例文件保留。

验证：模板同步、模板目录、Skill 包、模板上下文预算、根目录结构、OpenSpec 语言校验通过；15 项扫描回归、根上下文预算、文档卫生、关联 Change 校验和 diff 空白检查通过；最终 git-check 扫描 2136 entries，Errors: 0，warnings: 0，退出码 0。三个 env 的修复前后 SHA-256 一致、已忽略且不再受跟踪，示例文件保留，HEAD 未变。历史和未跟踪文件不在本次默认扫描范围。后续建议：仅在另行授权同步时检查待推送历史，不将本次检查扩大解释为历史安全结论。
