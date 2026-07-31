# ✨ Shareable Codex Skills

面向个人与团队的可公开安装 Codex skills：把重复、易遗漏的内容生产流程变成有边界、有检查点的工作流。

> 🔒 **隐私优先**：仓库不包含账号、凭证、真实短信、客户资料、私有文章、品牌素材或本机路径。安装后，账号配置始终留在你自己的工作区。

## 🧰 当前可用 Skills

| Skill | 适合什么场景 | 交付或保护点 | 版本 |
| --- | --- | --- | --- |
| 🏃 `running-wechat-article` | 调研并撰写跑步、赛事、训练类公众号文章 | 事实分层、图片授权、双 Markdown 文件 | `0.1.0` |
| 💬 `wechat-article-flow` | 选择文章与样式、生成预览、上传公众号草稿 | 适配器信任门禁、预览与上传分离确认 | `0.1.0` |
| 📱 `sms-template-review` | 审核中文短信模板或最终待发送文案 | 变量、链接、隐私、事实与发送风险检查 | `0.1.1` |
| 📊 `pptx-production-suite` | 制作、改版或验收可编辑 PPTX | 路线选择、依赖自检、交付验证 | `0.1.0` |

## 🚀 安装到 Codex

先查看仓库中可安装的 skill：

```bash
npx skills add kimplwjf/shareable-codex-skills --list
```

安装一个 skill 到本机 Codex（全局可用）：

```bash
npx skills add kimplwjf/shareable-codex-skills \
  --skill running-wechat-article \
  --global --agent codex
```

安装全部四个：

```bash
npx skills add kimplwjf/shareable-codex-skills \
  --skill '*' \
  --global --agent codex
```

安装后新开一个 Codex 对话，直接使用 `$running-wechat-article`、`$wechat-article-flow`、`$sms-template-review` 或 `$pptx-production-suite`。

> 💡 不使用 Codex？`skills` CLI 也支持 Claude Code、Cursor 等多种 agent；将 `--agent codex` 替换为你的目标 agent 即可。详见 [skills CLI](https://github.com/vercel-labs/skills)。

## 🗺️ 选择哪一个？

| 你的目标 | 从这里开始 |
| --- | --- |
| 写一篇可信、可发布的跑步公众号文章 | `running-wechat-article` |
| 已有 Markdown，想选择样式、预览或安全上传草稿 | `wechat-article-flow` |
| 在发送前检查一条赛事、通知或营销短信 | `sms-template-review` |
| 想要一份可编辑、可验收的 PPTX，而不是图片式幻灯片 | `pptx-production-suite` |

## 🔐 公众号：你的账号，你的配置

文章调研和写作不需要微信凭证；**本地预览与上传草稿需要你自己的适配器**。完成以下四步即可：

1. 将 [`账号适配器模板`](skills/wechat-article-flow/references/account-profile.template.md) 复制到私有工作区，例如 `.wechat-article/profile.md`。
2. 使用你自己的上传适配器，把 AppID、Secret、Cookie、Token 等放在受保护的环境变量或私有 `.env` 文件中。
3. 在画像中只填写你确认信任的**绝对适配器可执行文件路径**与固定 argv 协议；不要写 shell 命令、插值参数或任何凭证值。
4. 先确认本地预览，再逐次明确确认上传草稿与最终发布。

`wechat-article-flow` 不会自动搜索或执行工作区中的配置，也不会绕过上传确认。

## 📊 PPTX：依赖不会被偷偷打包

`pptx-production-suite` 是制作总控，不是把所有工具塞进一个 skill：

- 创建或修改可编辑 PPTX 时，需要单独安装 `ppt-master` 或你认可的等效作者工具。
- 原生动画、转场验收优先使用 PowerPoint。
- 图片、浏览器、HTML、Figma、Notion 等只会在所选路线需要时才提示使用。
- 缺少必需能力时，skill 会说明原因并停止在制作前；不会自动安装第三方依赖或静默降级。

查看完整的 [`PPTX 依赖矩阵`](skills/pptx-production-suite/references/toolchain.md)。

## 📱 短信审核：一条命令的机械预检

`sms-template-review` 会把可发送性拆成语言、事实、变量、链接和隐私检查。对含个人信息的正文，使用 `--stdin`，避免内容进入 shell 历史；skill 会给出已安装脚本的绝对路径调用方式。

它只做机械预检，**不替代**对日期、地点、受众、政策和最终链接的权威核验。

## 🔄 更新与版本

更新全部已安装 skill：

```bash
npx skills update --global
```

只更新一个：

```bash
npx skills update pptx-production-suite --global
```

每个 skill 的 `VERSION` 独立遵循语义化版本；[`skill-versions.json`](skill-versions.json) 用于快速查看整套版本。Git tag 表示整个仓库的可复现快照，并不要求所有 skill 同步升级。

## 🤝 维护与安全

维护者修改后，请至少运行：

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s skills/sms-template-review/scripts -p 'test_*.py'
```

提交前检查公开 diff，确保没有密钥、Cookie、真实联系人、内部链接、私有路径、未授权素材或客户数据。完整维护约束请见 [AGENTS.md](AGENTS.md)，发布记录请见 [CHANGELOG.md](CHANGELOG.md)。

---

MIT License · 欢迎 issue、改进建议与可复用 skill 贡献
