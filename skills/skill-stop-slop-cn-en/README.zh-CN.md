# Stop Slop CN-EN for Hermes Agent

简体中文 | [English](README.md)

这是一个面向 Hermes Agent 的中英双语去 AI 腔写作 skill。

本项目**不是从零原创**，而是基于 Hardik Pandya 的开源项目 [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) 修改、重组和适配而来。原项目主要用于移除英文 AI 写作痕迹；本版本在保留其核心思想的基础上，改造成 Hermes 可加载的 Agent Skill，并加入中文写作、中英混合文本、中文财经/研究文章、微信公众号风格和 Hermes 工具使用规则。

## 跨 Agent 兼容结构与安装

本仓库现在使用双布局 skill 结构：

```text
repo/
├── SKILL.md                                      # 跨 Agent 通用的权威说明
├── AGENTS.md                                    # Codex / OpenAI 项目指令
├── CLAUDE.md                                    # Claude Code 项目指令
├── agents/openai.yaml                           # 可选 OpenAI agent 元数据
└── skills/creative/stop-slop-cn-en/SKILL.md  # Hermes / OpenClaw 打包版 skill
```

根目录 `SKILL.md` 与 `skills/creative/stop-slop-cn-en/SKILL.md` 会保持字节级一致。若有脚本、参考文档或依赖文件，它们也会同时出现在两个可安装位置旁边。

### 作为可复用 skill 安装

- **Claude Code**：复制 `skills/creative/stop-slop-cn-en/` 到 `~/.claude/skills/creative/stop-slop-cn-en/`。
- **OpenAI Codex / OpenAI agents**：在本仓库工作时保留 `AGENTS.md`；如需作为可复用 skill，复制 `skills/creative/stop-slop-cn-en/` 到 `~/.agents/skills/creative/stop-slop-cn-en/`。
- **OpenClaw**：复制 `skills/creative/stop-slop-cn-en/` 到 `<workspace>/skills/creative/stop-slop-cn-en/`、`<workspace>/.agents/skills/creative/stop-slop-cn-en/` 或 `~/.openclaw/skills/creative/stop-slop-cn-en/`。
- **Hermes Agent**：复制 `skills/creative/stop-slop-cn-en/` 到 `~/.hermes/skills/creative/stop-slop-cn-en/`，然后开启新的 Hermes 会话。
- **通用 AgentSkills 加载器**：使用包含 `SKILL.md` 的目录；skill 名称为 `stop-slop-cn-en`。


## 相比原项目做了什么改造

相较原版 `stop-slop`，本版本主要做了以下调整：

- 改为 Hermes / Agent Skills 可识别的标准 skill tap 结构：`skills/creative/stop-slop-cn-en/SKILL.md`。
- 将原本偏英文的 AI 写作痕迹规则扩展为中文和中英混合文本可用的规则。
- 增加中文 AI 腔高频短语清单，例如“赋能”“助力”“生态”“闭环”“高质量发展”“未来可期”等。
- 增加中文结构问题识别，例如 PPT 式分层、机械三段式、伪深度句式、万能结尾和过度格式化。
- 加入 Hermes 工具使用说明：文件改写时优先 `read_file` + `patch`，大段重写才用 `write_file`。
- 加入金融、宏观、上市公司研究场景下的事实边界要求：不编造数据，不混淆披露事实和分析推断，缺数据时写“未披露”。
- 加入 Telegram、微信公众号、GitHub README/技术文档等不同输出场景的格式差异说明。

## 用途

用于改写中文、英文或中英混合文本，减少 AI 写作痕迹，让输出更自然、更像真人写作。

特别适合：

- 中文公众号文章
- 宏观金融短评
- 上市公司研究笔记
- 学术段落轻度去 AI 腔
- AI 工具评测
- GitHub README/技术文档
- Telegram 或社媒长回复
- 中英混合文本的自然化改写

## 仓库结构

```text
skills/creative/stop-slop-cn-en/
├── SKILL.md
└── references/
    ├── phrases-cn.md
    ├── structures-cn.md
    ├── examples-cn.md
    └── checklist-cn.md
```

## 安装到 Hermes

### 方式一：本地复制

把 `skills/stop-slop-cn-en` 复制到：

```bash
~/.hermes/skills/creative/stop-slop-cn-en
```

然后新开一个 Hermes 会话，或在对话中加载：

```text
/skill stop-slop-cn-en
```

### 方式二：作为 GitHub skill tap 安装

```bash
hermes skills tap add yanyintingyou/stop-slop-cn-en
hermes skills install yanyintingyou/stop-slop-cn-en/stop-slop-cn-en --force
```

## 使用示例

```text
/skill stop-slop-cn-en

把下面这段中文财经评论改得自然一点，少点 AI 腔。保留事实边界，不要编造数据，不要写万能总结。
```

## 来源说明

原始项目：[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)

原作者：Hardik Pandya

原始许可证：MIT

本版本保留 MIT 许可，并在原项目基础上增加 Hermes Agent 兼容、中英双语写作规则和中文研究/财经文本适配。

## 许可

MIT。原始项目为 MIT，本改造版同样使用 MIT。
