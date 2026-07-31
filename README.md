# Shareable Codex Skills

可公开安装、可独立升级的 Codex Skill 集合。每个目录都是可单独安装的 skill；它们不会携带账号、凭证、私有文章、客户数据或本机路径。

## 当前 Skills

| Skill | 当前版本 | 用途 |
| --- | --- | --- |
| `running-wechat-article` | 0.1.0 | 调研并撰写跑步/赛事/训练类微信公众号文章。 |
| `wechat-article-flow` | 0.1.0 | 在对话中编排文章选择、本地预览和明确确认后的草稿上传。 |
| `sms-template-review` | 0.1.0 | 审核中文短信模板或成品，含隐私保护的机械检查。 |
| `pptx-production-suite` | 0.1.0 | 为可编辑 PPTX 制作选择工具路线、准备材料并执行验证门禁。 |

每个 skill 的 `VERSION` 是其独立版本权威；根目录的 `skill-versions.json` 方便批量查看。后续只改动一个 skill 时，只递增该 skill 的语义化版本（例如 `0.1.0` -> `0.1.1`），并在根 `CHANGELOG.md` 记录原因。仓库 tag 表示整套 skills 的可复现快照，不要求所有 skill 同步升版。

## 安装

发布到 GitHub 后，使用你环境中的 Skills 安装工具选择对应目录安装；常见入口为：

```bash
npx skills add <owner>/shareable-codex-skills
```

也可以在 Codex 中请求“从 `<owner>/shareable-codex-skills` 安装 `skills/<skill-name>`”。安装完成后，在新对话中使用 `$<skill-name>`。

离线或受限环境可将某个 `skills/<skill-name>/` 目录复制到：

```text
~/.codex/skills/<skill-name>/
```

复制后必须保留 `SKILL.md`、`VERSION`、`agents/` 与该 skill 引用的资源目录。

更新已安装的 skills：

```bash
npx skills update
```

如使用手工复制安装，则以新的 `skills/<skill-name>/` 目录完整替换本地安装副本；替换前保留自己的私有账号画像和 `.env` 文件在工作区，不要放进 skill 目录。

## 微信公众号配置

`running-wechat-article` 和 `wechat-article-flow` 可在没有任何账号配置时完成调研、写作与本地预览。上传草稿前，安装者必须在自己的工作区配置自己的公众号信息，且不得把真实值写进本仓库或 skill 安装目录：

1. 从 `skills/wechat-article-flow/references/account-profile.template.md` 复制账号画像到项目私有目录，例如 `.wechat-article/profile.md`。
2. 使用自己的上传工具或适配器，并把凭证放入本地受保护环境变量/`.env` 文件。
3. 在账号画像中只填写经本人确认的绝对适配器可执行文件路径及固定 argv 协议；不要填写 shell 命令、插值参数或凭证变量值，也不要在聊天、日志、提交或 issue 中粘贴 Secret。
4. 先生成本地预览。上传草稿和正式发布都必须逐次获得明确确认。

本仓库不包含微信公众号 AppID、Secret、Cookie、账号名、品牌水印、私有文章、预览文件或上传结果。

## 依赖边界

每个 skill 的 `SKILL.md` 说明必需与可选依赖。核心原则：

- 文章研究需要可用的联网检索；图片、浏览器、OCR 与特定编辑器按任务启用。
- 微信上传适配器和凭证只在“上传草稿”步骤需要，预览和写作不依赖它们。
- 安装 `pptx-production-suite` 不会自动安装 `ppt-master` 或其他依赖；它会先自检并提示安装者从可信上游单独安装所需导出引擎（默认路线为 `ppt-master`）和必要验证工具。
- 不把第三方 skill、浏览器插件、PowerPoint、Figma 或 Notion 视为默认已安装能力。

## 维护与发布

1. 在对应 `skills/<skill-name>/` 修改；不要直接维护 `~/.codex/skills/` 的安装副本。
2. 运行不依赖第三方 Python 包的结构校验和相关脚本测试：

   ```bash
   python3 scripts/validate_skills.py
   python3 -m unittest discover -s skills/sms-template-review/scripts -p 'test_*.py'
   ```
3. 复查公开 diff：不得包含密钥、Cookie、真实联系人、内部链接、私有路径、未授权素材或客户数据。
4. 递增被修改 skill 的 `VERSION`，更新 `skill-versions.json` 与 `CHANGELOG.md`。
5. 创建 Git commit 和发布 tag/Release；接收者按 Release 说明更新。

详见 [AGENTS.md](AGENTS.md) 的贡献与安全约束。
