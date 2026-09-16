# Shareable Codex Skills

面向中文写作与内容交付的开源 Codex Skills：润滑口吻、跑步公众号写作、文章预览与草稿上传、短信审核、可编辑 PPTX 制作与验收。

五个可独立安装的工作流，覆盖跑步内容写作、公众号本地预览与草稿上传、中文短信发送前审核、可编辑 PPTX 交付，以及中文圆融协调口吻写作。账号、凭证、真实素材和私有配置始终留在安装者自己的工作区。

每个 skill 都有独立的使用说明和版本。安装会向 Agent 添加工作指引及附带资源；模型、账号、发布适配器与 PPTX 制作工具需要按场景另行准备。

[快速安装](#快速安装) · [选择 Skill](#选择合适的-skill) · [使用与产物](#使用与产物) · [更新与卸载](#更新与卸载) · [常见问题](#常见问题)

## 快速安装

准备好 [Codex](https://developers.openai.com/codex/)、[Node.js LTS（含 npm / npx）](https://nodejs.org/)、Git，以及可访问 npm 和 GitHub 的网络。在终端执行以下命令。

**只安装「润滑」：**

```bash
npx --yes skills add kimplwjf/shareable-codex-skills --skill runhua --global --agent codex --yes
```

**安装全部五个 skill：**

```bash
npx --yes skills add kimplwjf/shareable-codex-skills --skill '*' --global --agent codex --yes
```

第一个 `--yes` 用于确认运行 npm 包，末尾的 `--yes` 跳过 skill 安装交互；希望逐项确认时可去掉这两个参数。安装前请阅读对应 `SKILL.md`，本地有自定义改动时先备份。

安装完成后，新开 Codex 对话输入：

```text
$runhua 帮我润滑一下：方案周五前给我，有困难及时说。
```

## 效果预览

<p align="center">
  <img src="preview/running-wechat-article-preview.jpg" alt="合成跑步内容创作示意：跑者、研究卡片与内容路线" width="32%" />
  <img src="preview/sms-template-review-preview.jpg" alt="合成短信审核示意：消息经由隐私与规则检查后输出" width="32%" />
  <img src="preview/pptx-production-suite-preview.jpg" alt="合成 PPTX 制作示意：幻灯片布局、内容卡片与交付检查" width="32%" />
</p>

| 可信内容与公众号流程 | 发送前审核 | 可编辑演示文稿 |
| --- | --- | --- |
| 从可核验事实和图片授权，到读者正文与内部选题稿；本地预览和草稿上传分阶段确认。 | 将变量、链接、隐私和事实拆开检查；机械通过不等于业务事实已确认。 | 选择合适的作者工具、准备材料、验证成品；不以截图冒充可编辑 PPTX。 |

以上均为原创合成示意图，不包含真实账号、客户、赛事、短信或演示文稿内容；详情见 [`preview/README.md`](preview/README.md)。

## 选择合适的 Skill

| 你的目标 | Skill | 示例请求 | 版本 |
| --- | --- | --- | --- |
| 写可信、可发布的跑步内容 | [`running-wechat-article`](skills/running-wechat-article/SKILL.md) | “分析这场马拉松的报名规则，并生成两份 Markdown 成稿。” | `0.1.0` |
| 将已确认文章本地预览并上传草稿 | [`wechat-article-flow`](skills/wechat-article-flow/SKILL.md) | “用我的受信任适配器预览这篇 Markdown。” | `0.1.0` |
| 判断一条短信是否可以发送 | [`sms-template-review`](skills/sms-template-review/SKILL.md) | “这条通知短信能发吗？请指出阻塞项并给出可用版本。” | `0.1.1` |
| 制作或验收可编辑演示文稿 | [`pptx-production-suite`](skills/pptx-production-suite/SKILL.md) | “根据这份大纲制作可编辑 PPTX，并说明需要的工具和验收项。” | `0.1.0` |
| 把话说得圆融顺口、便于协调 | [润滑 `runhua`](skills/runhua/SKILL.md) | “润滑一下：方案周五前给我，有困难及时说。” | `0.1.0` |

### 润滑：把话说顺，把配合接起来

适合群聊协调、提意见、催进度、谈合作和婉拒。默认带一点熟络的业务协调口吻：说清具体问题，接上共同推进的动作，再落到眼前的服务或配合上。内置融合自 ra-人话 的去 AI 味原则，避免模板对比、训话开头和空泛口号，同时保留期限、责任、拒绝和不确定性。

**合成示例**

原话：这个版本的报名入口不好找，需要调整。

> 这个版本的报名入口还得再磨一下，现在找起来有点费劲。咱们把这段操作理顺，用户少找两遍，服务也就做到位了。

安装「润滑」：

```bash
npx skills add kimplwjf/shareable-codex-skills \
  --skill runhua \
  --global --agent codex
```

安装后新开对话，例如：

```text
$runhua 润滑一下：方案周五前给我，有困难及时说。
```

想加强口吻可以说“再润一点”，需要收短可以说“保留这个味道，缩成两句”。默认直接输出中文成稿，无需额外安装 ra-人话，也不需要账号、API 或其他工具；写稿不会自动发送消息。

## 使用与产物

| Skill | 提供什么 | 得到什么 | 运行前提与边界 |
| --- | --- | --- | --- |
| `runhua` | 原话、收件对象、希望保留的条件 | 圆融顺口的中文成稿，可调浓度和长度 | 无额外工具依赖；保留事实、期限与拒绝，不自动发消息 |
| `running-wechat-article` | 选题、目标读者、权威来源与可用素材 | 内部选题稿和读者正文两份 Markdown | 时效事实需要检索核验；图片需要使用授权，默认只交付本地文件 |
| `wechat-article-flow` | 已确认文章、私有账号配置、受信任适配器 | 本地预览；确认后可上传公众号草稿 | 不附带上传器或微信凭证；选择、预览、打开浏览器与上传分步确认 |
| `sms-template-review` | 短信原文或截图、受众、发送时间、事实来源 | 审核结论、阻塞项、待核验项和可安全改写的版本 | 附带检查脚本需要 Python 3；格式检查不能证明业务事实正确 |
| `pptx-production-suite` | 内容来源、现有 PPTX 或模板、交付要求 | 工具路线、制作与验收；依赖齐备时交付可编辑 PPTX | 需要作者工具及独立审查能力；原生动画需相应播放器验证 |

以下请求使用合成场景和示例文件名，按自己的材料替换：

```text
$running-wechat-article 根据我提供的赛事官方公告，写一篇报名指南，分别输出选题与成稿、公众号正文。

$wechat-article-flow 我有一篇 article.md，请先说明账号适配器需要哪些配置，配置确认后只做本地预览。

$sms-template-review 审核这条模板：“您的报名已通过，请于{日期}前确认。” 缺少事实依据时请列出待核验项。

$pptx-production-suite 根据 outline.md 制作一份可编辑演示文稿，先检查工具和素材是否齐备。
```

## 安装选项

查看仓库中可安装的 skill：

```bash
npx skills add kimplwjf/shareable-codex-skills --list
```

只安装一个 skill 到本机 Codex：

```bash
npx skills add kimplwjf/shareable-codex-skills \
  --skill running-wechat-article \
  --global --agent codex
```

安装后新开一个 Codex 对话，直接使用 `$running-wechat-article`、`$wechat-article-flow`、`$sms-template-review`、`$pptx-production-suite` 或 `$runhua`（润滑）。

`skills` CLI 也支持 Claude Code、Cursor 等 Agent；将 `--agent codex` 替换为目标 Agent 即可。详见 [skills CLI](https://github.com/vercel-labs/skills)。

`--global` 表示用户级安装；只想在当前项目使用时，在项目目录执行并省略 `--global`。其他 Agent 可分别使用 `--agent claude-code` 或 `--agent cursor`；识别与调用方式以对应 Agent 为准。

检查 Codex 的全局安装结果：

```bash
npx skills list --global --agent codex
```

## 账号、隐私与依赖

- 公众号写作不需要微信凭证；本地预览与草稿上传使用安装者自己的受信任适配器。复制 [`账号适配器模板`](skills/wechat-article-flow/references/account-profile.template.md) 到私有工作区，凭证只放受保护的环境变量或私有 `.env`。
- 预览、上传草稿和正式发布是独立步骤；`wechat-article-flow` 不会自行发现配置，也不会绕过确认。
- `sms-template-review` 的机械检查不替代日期、地点、受众、政策和最终链接的权威核验。含个人信息的正文使用 `--stdin`，避免进入 shell 历史。
- `pptx-production-suite` 是制作与交付门禁，不会自动安装 `ppt-master`、PowerPoint、浏览器或其他依赖。缺少可编辑 PPTX 作者工具时，它会在制作前说明缺口并停止。

## 更新与卸载

更新全部已安装 skill：

```bash
npx skills update --global
```

只更新一个：

```bash
npx skills update runhua --global
```

更新会获取上游版本；有本地定制时先备份。各 skill 独立版本化，不要求一起升级。

卸载 Codex 的全局「润滑」安装：

```bash
npx skills remove runhua --global --agent codex
```

## 常见问题

**安装后没有识别到 skill？** 先用 `npx skills list --global --agent codex` 核对，再新开对话并显式输入 `$runhua` 等标识。项目级安装需在对应项目中使用。

**只有中文名字能调用吗？** 「润滑」是显示名，安装与显式调用标识为 `runhua` / `$runhua`。普通对话也可以说“帮我润滑一下”，是否自动选中由 Agent 决定。

**安装成功就能上传公众号或制作 PPTX 吗？** 还需要对应适配器、凭证或作者工具。Skill 会检查缺口；安装本仓库不会替你配置账号或安装这些依赖。

**联网安装失败怎么办？** 检查 Node.js、Git、npm registry 和 GitHub 的可达性，按报错定位下载或克隆阶段。不要把访问令牌、Cookie 或私有配置贴到公开 Issue。

**可以直接使用生成的文章、短信或图片吗？** 需要先核实事实、隐私、素材授权和目标渠道要求。短信“机械检查通过”、文章“本地预览完成”、公众号“草稿上传成功”是不同阶段，不能相互替代。

## 仓库导航与贡献

| 入口 | 内容 |
| --- | --- |
| [`skills/`](skills/) | 各 skill 的执行说明、版本及可选脚本、参考资料 |
| [`skill-versions.json`](skill-versions.json) | 全部 skill 的当前版本清单 |
| [`CHANGELOG.md`](CHANGELOG.md) | 版本和文档变更记录 |
| [`AGENTS.md`](AGENTS.md) | 仓库维护、隐私、验证与发布约定 |
| [`preview/README.md`](preview/README.md) | 能力示意图来源与使用边界 |
| [`LICENSE`](LICENSE) | MIT 许可证 |

欢迎通过 [Issues](https://github.com/kimplwjf/shareable-codex-skills/issues) 提交需求或问题，通过 [Pull requests](https://github.com/kimplwjf/shareable-codex-skills/pulls) 贡献改进。问题描述请注明 skill 名称、版本、Agent、预期行为与实际行为；复现材料使用合成或已脱敏输入。

贡献前阅读维护约定。通用规则放入 skill，私人账号、品牌偏好和上传配置留在安装者工作区；不要提交真实草稿、客户数据、凭证或运行日志。

每个 skill 的 `VERSION` 独立遵循语义化版本；[`skill-versions.json`](skill-versions.json) 汇总当前版本。维护者修改后至少运行：

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s skills/sms-template-review/scripts -p 'test_*.py'
```

提交前检查公开 diff，确保没有密钥、Cookie、真实联系人、内部链接、私有路径、未授权素材或客户数据。完整维护约束见 [AGENTS.md](AGENTS.md)，变更记录见 [CHANGELOG.md](CHANGELOG.md)。

MIT License · 欢迎 issue、改进建议与可复用 skill 贡献。
