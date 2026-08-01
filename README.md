# Shareable Codex Skills

把内容生产中容易遗漏的事实、授权与交付检查，做成可公开安装的 Codex Skills。

四个可独立安装的工作流，覆盖跑步内容写作、公众号本地预览与草稿上传、中文短信发送前审核，以及可编辑 PPTX 交付。账号、凭证、真实素材和私有配置始终留在安装者自己的工作区。

```bash
npx skills add kimplwjf/shareable-codex-skills \
  --skill '*' \
  --global --agent codex
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

## 安装

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

安装后新开一个 Codex 对话，直接使用 `$running-wechat-article`、`$wechat-article-flow`、`$sms-template-review` 或 `$pptx-production-suite`。

`skills` CLI 也支持 Claude Code、Cursor 等 Agent；将 `--agent codex` 替换为目标 Agent 即可。详见 [skills CLI](https://github.com/vercel-labs/skills)。

## 账号、隐私与依赖

- 公众号写作不需要微信凭证；本地预览与草稿上传使用安装者自己的受信任适配器。复制 [`账号适配器模板`](skills/wechat-article-flow/references/account-profile.template.md) 到私有工作区，凭证只放受保护的环境变量或私有 `.env`。
- 预览、上传草稿和正式发布是独立步骤；`wechat-article-flow` 不会自行发现配置，也不会绕过确认。
- `sms-template-review` 的机械检查不替代日期、地点、受众、政策和最终链接的权威核验。含个人信息的正文使用 `--stdin`，避免进入 shell 历史。
- `pptx-production-suite` 是制作与交付门禁，不会自动安装 `ppt-master`、PowerPoint、浏览器或其他依赖。缺少可编辑 PPTX 作者工具时，它会在制作前说明缺口并停止。

## 更新与维护

更新全部已安装 skill：

```bash
npx skills update --global
```

只更新一个：

```bash
npx skills update pptx-production-suite --global
```

每个 skill 的 `VERSION` 独立遵循语义化版本；[`skill-versions.json`](skill-versions.json) 汇总当前版本。维护者修改后至少运行：

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s skills/sms-template-review/scripts -p 'test_*.py'
```

提交前检查公开 diff，确保没有密钥、Cookie、真实联系人、内部链接、私有路径、未授权素材或客户数据。完整维护约束见 [AGENTS.md](AGENTS.md)，变更记录见 [CHANGELOG.md](CHANGELOG.md)。

MIT License · 欢迎 issue、改进建议与可复用 skill 贡献。
