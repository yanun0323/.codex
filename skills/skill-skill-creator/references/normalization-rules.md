# Skill Normalization Rules

Apply these rules to all skill folders discovered by scanning `skills/**/SKILL.md`.

## Prefix and Type Rules

- Folder names starting with `agents-`:
  - Rename prefix to `rule-`
  - Rename `SKILL.md` frontmatter `name` to the new `rule-*` name
  - Ensure `assets/rule-small.svg` exists
  - Set `interface.display_name` to `Rule - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/rule-small.svg`

- Folder names starting with `command-`:
  - Keep (or normalize to) `command-` prefix
  - Rename `SKILL.md` frontmatter `name` to the folder name
  - Ensure `assets/command-small.svg` exists
  - Set `interface.display_name` to `Command - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/command-small.svg`
  - Ensure `SKILL.md` frontmatter `description` contains:
    - `Use this skill only when the user explicitly asks to invoke`

- Folder names starting with `rule-`:
  - Keep `rule-` prefix
  - Rename `SKILL.md` frontmatter `name` to the folder name
  - Ensure `assets/rule-small.svg` exists
  - Set `interface.display_name` to `Rule - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/rule-small.svg`

- All other folder names:
  - Rename prefix to `skill-`
  - Rename `SKILL.md` frontmatter `name` to the new `skill-*` name
  - Ensure `assets/skill-small.svg` exists
  - Set `interface.display_name` to `Skill - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/skill-small.svg`

## Metadata Safety

- Keep existing `agents/openai.yaml` fields unless explicitly required to change.
- Update only the required fields when normalizing:
  - `interface.display_name`
  - `interface.icon_small`

## Validation

Use check mode to validate without edits:

```bash
ruby skills/skill-skill-creator/scripts/normalize_skill_catalog.rb --check
```
