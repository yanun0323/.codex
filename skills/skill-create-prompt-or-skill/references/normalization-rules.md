# Prompt and Skill Normalization Rules

Apply these rules to all skill folders discovered by scanning `skills/**/SKILL.md`.

## Prefix and Type Rules

- Folder names starting with `agents-`:
  - Rename prefix to `rule-`
  - Rename `SKILL.md` frontmatter `name` to the new `rule-*` name
  - Ensure `assets/rule-small.svg` exists
  - Set `interface.display_name` to `Rule - Xxx Xxx`
  - Set `interface.icon_small` to `./assets/rule-small.svg`

- Prompt files live under `prompts/`:
  - Use plain names such as `review.md` or `plan-task.md`
  - Do not use the `command-` prefix
  - Frontmatter must contain `description` only
  - Body should be concise and task-oriented in OpenAI Codex prompt format

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
- Prompts do not use `agents/openai.yaml` or `assets/` icons.

## Legacy Command Skills

- Existing `command-*` skill folders are legacy.
- Do not create new `command-*` skills.
- When a request uses command naming, convert it to a prompt file in `prompts/` and remove the prefix.
- Catalog normalization may skip legacy command folders instead of rewriting them as skills.

## Validation

Use check mode to validate without edits:

```bash
ruby skills/skill-create-prompt-or-skill/scripts/normalize_skill_catalog.rb --check
```
