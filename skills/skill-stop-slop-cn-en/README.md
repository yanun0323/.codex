# Stop Slop CN-EN for Hermes Agent

[简体中文](README.zh-CN.md) | English

A bilingual anti-AI-slop writing skill for Hermes Agent.

This repository is **not an original project from scratch**. It is adapted from Hardik Pandya's open-source project [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop). The upstream project focuses on removing AI tells from English prose. This version reorganizes the idea into a Hermes-compatible Agent Skill and adds Chinese, Chinese-English mixed writing, finance/research writing, WeChat-style prose, and Hermes tool-use guidance.

## Cross-agent compatibility and installation

This repository now uses a dual-layout skill structure:

```text
repo/
├── SKILL.md                                      # canonical cross-agent instructions
├── AGENTS.md                                    # Codex/OpenAI project instructions
├── CLAUDE.md                                    # Claude Code project instructions
├── agents/openai.yaml                           # optional OpenAI agent metadata
└── skills/creative/stop-slop-cn-en/SKILL.md  # Hermes/OpenClaw packaged skill copy
```

The root `SKILL.md` and the packaged `skills/creative/stop-slop-cn-en/SKILL.md` are intentionally byte-identical. Supporting files, when present, are available next to both copies.

### Install as a reusable skill

- **Claude Code**: copy `skills/creative/stop-slop-cn-en/` to `~/.claude/skills/creative/stop-slop-cn-en/`.
- **OpenAI Codex / OpenAI agents**: keep `AGENTS.md` when working in this repository, or copy `skills/creative/stop-slop-cn-en/` to `~/.agents/skills/creative/stop-slop-cn-en/` for a reusable skill.
- **OpenClaw**: copy `skills/creative/stop-slop-cn-en/` to either `<workspace>/skills/creative/stop-slop-cn-en/`, `<workspace>/.agents/skills/creative/stop-slop-cn-en/`, or `~/.openclaw/skills/creative/stop-slop-cn-en/`.
- **Hermes Agent**: copy `skills/creative/stop-slop-cn-en/` to `~/.hermes/skills/creative/stop-slop-cn-en/`, then start a new Hermes session.
- **Generic AgentSkills loaders**: use the directory that contains `SKILL.md`; the skill name is `stop-slop-cn-en`.


## What changed from upstream

Compared with the original `stop-slop`, this version:

- Uses the Hermes / Agent Skills tap structure: `skills/creative/stop-slop-cn-en/SKILL.md`.
- Extends English anti-AI-slop rules to Chinese and bilingual writing.
- Adds Chinese AI-slop phrase lists, including terms such as “赋能”, “助力”, “生态”, “闭环”, “高质量发展”, and “未来可期”.
- Adds Chinese structural pattern checks, including PPT-like sections, mechanical three-part structure, pseudo-depth phrasing, generic endings, and over-formatting.
- Adds Hermes-specific workflow guidance: use `read_file` + `patch` for file edits, and use `write_file` only for large rewrites.
- Adds finance, macro, and listed-company research safeguards: do not invent data, distinguish disclosed facts from analytical inference, and write “not disclosed” / “未披露” when data is missing.
- Adds platform-aware guidance for Telegram replies, WeChat public articles, GitHub READMEs, and technical documentation.

## Use cases

Use this skill to rewrite Chinese, English, or mixed Chinese-English text so it sounds less like generated AI prose and more like natural human writing.

It is especially useful for:

- Chinese WeChat public account articles
- Macro-finance commentary
- Listed-company research notes
- Light de-AI editing for academic paragraphs
- AI tool evaluations
- GitHub README and technical documentation
- Telegram or social-media long replies
- Naturalizing bilingual Chinese-English prose

## Repository structure

```text
skills/creative/stop-slop-cn-en/
├── SKILL.md
└── references/
    ├── phrases-cn.md
    ├── structures-cn.md
    ├── examples-cn.md
    └── checklist-cn.md
```

## Install in Hermes

### Option 1: Local copy

Copy `skills/stop-slop-cn-en` to:

```bash
~/.hermes/skills/creative/stop-slop-cn-en
```

Then start a new Hermes session, or load it in chat:

```text
/skill stop-slop-cn-en
```

### Option 2: GitHub skill tap

```bash
hermes skills tap add yanyintingyou/stop-slop-cn-en
hermes skills install yanyintingyou/stop-slop-cn-en/stop-slop-cn-en --force
```

## Example prompt

```text
/skill stop-slop-cn-en

Rewrite the following Chinese finance paragraph so it sounds natural and less AI-written. Keep factual boundaries, do not invent data, and avoid generic conclusions.
```

## Attribution

Original project: [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)

Original author: Hardik Pandya

Original license: MIT

This adapted version keeps the MIT license and adds Hermes Agent compatibility plus Chinese/English bilingual writing guidance.

## License

MIT. The upstream project is MIT licensed, and this adapted version is also released under MIT.
