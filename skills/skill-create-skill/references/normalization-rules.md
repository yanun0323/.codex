# Skill Normalization Rules

Apply these rules to all skills under `skills/`.

## Prefix Rules

- For skills with folder names starting with `agents-`:
  - Rename folder prefix to `rule-`
  - Rename `SKILL.md` frontmatter `name` to the new `rule-*` name
  - Use `rule-small.svg` in `assets/`
  - Set `interface.display_name` to `Rule - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/rule-small.svg`

- For skills with folder names starting with `command-`:
  - Keep `command-` prefix (or rename to `command-` if inconsistent)
  - Rename `SKILL.md` frontmatter `name` to the folder name
  - Use `command-small.svg` in `assets/`
  - Set `interface.display_name` to `Command - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/command-small.svg`

- For all other skill folders:
  - Rename folder prefix to `skill-`
  - Rename `SKILL.md` frontmatter `name` to the new `skill-*` name
  - Use `skill-small.svg` in `assets/`
  - Set `interface.display_name` to `Skill - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/skill-small.svg`

## Original Request (verbatim)

```text
幫我把 skills/ 底下的所有 skills 做以下修改：
- 所有 agents- 資料夾開頭的 skill：
    1. folder 以及 SKILL.md 的 name 改名為 rule- 前綴
    1. assets/ 使用 rule-small.svg 
    1. openai.yaml display name 使用 Rule - Xxx Xxx 命名方式，icon_small 使用 rule-small.svg

- 所有 command- 資料夾開頭的 skill：
    1. folder 以及 SKILL.md 的 name 改名為 command- 前綴
    1. assets/ 使用 command-small.svg 
    1. openai.yaml display name 使用 Command - Xxx Xxx 命名方式，icon_small 使用 command-small.svg

- 其他資料夾的 skill：
    1. folder 以及 SKILL.md 的 name 改名為 skill- 前綴
    1. assets/ 使用 skill-small.svg 
    1. openai.yaml display name 使用 Skill - Xxx Xxx 命名方式，icon_small 使用 skill-small.svg
```
