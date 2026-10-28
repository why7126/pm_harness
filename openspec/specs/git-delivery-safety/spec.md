# git-delivery-safety Specification

## Purpose
定义 Git 暂存与历史内容检查、脱敏诊断、环境文件隔离和按交付范围同步的安全要求。
## Requirements
### Requirement: Git 内容快照覆盖
系统 MUST 分别检查暂存快照、受跟踪工作区和显式选择的待推送历史，不能将覆盖缺口报告为通过。

#### Scenario: 暂存后工作区已清理
- **WHEN** 暂存含敏感内容而工作区已替换为安全文本
- **THEN** 暂存 blob 仍产生阻断，index 保持不变

#### Scenario: 中间提交已删除敏感内容
- **WHEN** 待推送历史中曾提交随后删除敏感文件
- **THEN** 历史扫描仍阻断

### Requirement: 安全诊断与精确例外
系统 MUST 不输出命中行和敏感值；占位符必须完整匹配，不豁免整行或测试目录。

#### Scenario: 同行多个值
- **WHEN** 一行含多个敏感值及 example 子串
- **THEN** 检出风险且报告不含任何原始值

### Requirement: 环境文件隔离
系统 MUST 校验真实 env 忽略和示例可跟踪，默认及深度扫描不读取被忽略且未跟踪的真实 env。

#### Scenario: 示例误被忽略
- **WHEN** 忽略规则覆盖环境示例
- **THEN** 输出路径级诊断并阻断，不读取真实 env

### Requirement: 范围化 Git 同步
git-sync MUST 保护既有 staged 内容，精确暂存，复核安全与历史后按明确目标快进推送；正式 tag 绑定发布事实，禁止覆盖标签或强制推送。

#### Scenario: 混合暂存区
- **WHEN** 已暂存文件包含本次范围之外的用户改动
- **THEN** 保留暂存区并解决范围决策，不批量暂存或提交
