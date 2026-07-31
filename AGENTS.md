# Shareable Codex Skills Agent Contract

此仓库发布可被陌生安装者使用的通用 Codex skills。目标是可移植、可验证、无私有数据；README 面向安装者，本文约束仓库维护与发布。

## 范围与权威

- 每个 `skills/<name>/SKILL.md` 是该 skill 的执行权威；`references/` 仅存 SKILL.md 明确链接的按需细节。
- 根 `README.md` 负责安装、配置、版本与仓库导航；`skill-versions.json` 和各 skill 的 `VERSION` 共同记录版本。
- 不把原项目账号规则、私有样稿、运行日志或本机工作流当作公开 skill 的权威来源。

## 公开与隐私边界

- 禁止提交密钥、Token、Cookie、AppID/Secret、Webhook、手机号、姓名、客户数据、内部链接、真实草稿、上传结果、日志、缓存、私有截图和绝对本机路径。
- 账号名、品牌水印、作者偏好、内容画像、历史文章和上传适配器配置属于安装者私有层。只提供无真实值的模板，并明确要求安装者在自己工作区配置。
- 不将搜索结果、社交媒体素材或无水印图片视为可发布授权。对图片、短信和 PPTX 保留来源、事实、隐私与人工确认门禁。

## Skill 设计

- 每个 skill 必须独立安装和理解：具备 `SKILL.md`、`VERSION`、`agents/openai.yaml`，以及仅在确有必要时添加 `scripts/`、`references/` 或 `assets/`。
- YAML frontmatter 只使用 `name` 和 `description`；名称采用小写 hyphen-case。触发条件写在 description，正文保持流程与边界。
- 不硬编码 `$HOME`、开发者用户名、当前仓库路径、账号名或第三方凭证。把外部系统写为可选适配器，缺少时给出配置说明而不是伪装为已可用。
- 上传、发布、付费、删除、覆盖和浏览器登录都是外部副作用；默认停在本地预览或待确认状态，只有明确用户确认后才执行。

## 版本、测试与发布

- 每个 skill 独立采用语义化版本。仅修改一个 skill 时只升级该 skill；同时更新根 manifest 与 changelog。
- 修改前检查 `git status --short`，保留无关改动。修改后至少运行 `python3 scripts/validate_skills.py`、相关脚本测试、`git diff --check` 和敏感词/路径扫描。
- 修改公共流程后，用无凭证、合成输入做一次新安装者视角验证。不得用真实账号、真实短信、私有文章或生产发布验证。
- 提交、push、Release、上传和公开发布均需维护者明确授权。推送前检查完整 staged diff 与远端目标；不得 force push 或覆盖接收者配置。

## 交付

完成时报告修改的 skill、版本变化、验证结果、未验证项、依赖前提及剩余风险。不得将计划或未运行的外部操作表述为已完成。
